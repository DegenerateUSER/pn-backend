from botocore.client import Config
import re
import os
from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from django.db import transaction
from collections import defaultdict


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        help_text="Must be a valid email address and unique"
    )
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'token')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        try:

            password = validated_data.pop('password')
            user = User(**validated_data)
            user.set_password(password)
            user.save()

            return user

        except Exception as e:
            raise ValidationError({'errors': [str(e)]})


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        whitelist_check = EmailWhitelist.objects.filter(email = email).exists()
        is_oldUser = User.objects.filter(email = email).exists()

        if not whitelist_check:
            raise ValidationError({"message": "Email not whitelisted"})
        
        if not is_oldUser:
            user = User(email=email)
            user.set_password(password)
            whitelist_role = EmailWhitelist.objects.get(email = email).role
            user.role = whitelist_role
            user.save()
        else:
            user = authenticate(username=email, password=password)




        if not user:
            raise ValidationError({'password': 'Invalid password'})
        
        if not user.is_active:
            raise ValidationError({"email":'Account is deactivated'})
        
        attrs['user'] = user
        return attrs

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = '__all__'

    def get_questions(self, obj):
        set_number = self.context.get('set_number', None)
        queryset = obj.questions.all()
        if set_number is not None:
            try:
                queryset = queryset.filter(set_number=int(set_number))
            except (TypeError, ValueError):
                pass
        return QuestionSerializer(queryset, many=True, context=self.context).data


class AssessmentSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    # Input/Output fields with custom names
    assessment_name = serializers.CharField(source='title')
    assessment_description = serializers.CharField(source='description', required=False, allow_blank=True)
    num_of_sets = serializers.IntegerField(source='total_sets', write_only=True)
    section_names = serializers.ListField(child=serializers.CharField(), write_only=True)
    section_descriptions = serializers.ListField(child=serializers.CharField(), write_only=True)
    is_electron_only = serializers.BooleanField(write_only=True)
    num_of_ai_generated_questions = serializers.IntegerField(source='ai_generated_questions', write_only=True)
    questions = serializers.ListField(write_only=True)
    attachments = serializers.ListField(required=False, allow_empty=True, write_only=True)
    
    class Meta:
        model = Assessment
        fields = [
            'id', 'assessment_name', 'assessment_description', 'assessment_type', 
            'created_by', 'created_at', 'updated_at', 'is_active', 'is_published', 
            'total_marks', 'passing_marks', 'duration', 'is_proctored', 
            'start_time', 'end_time', 'is_electron_only', 'ai_generated_questions',
            'sections',
            # Write-only fields for input
            'num_of_sets', 'section_names', 'section_descriptions', 
            'num_of_ai_generated_questions', 'questions', 'attachments'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'total_marks']

    def validate(self, attrs):
        """Validate that $n references in question_text do not exceed attachments length (1-based)."""
        attachments_from_input = attrs.get('attachments', None)
        attachments_current = None
        if getattr(self, 'instance', None) is not None:
            attachments_current = getattr(self.instance, 'attachments', None)
        attachments = attachments_from_input if attachments_from_input is not None else (attachments_current or [])
        attachments_len = len(attachments) if isinstance(attachments, list) else 0

        # Only validate when questions are provided (create or update with questions)
        questions = attrs.get('questions', None)
        if questions is None:
            return attrs

        errors = {}
        for idx, q in enumerate(questions):
            text = q.get('question_text', '') or ''
            refs = [int(n) for n in re.findall(r"\$(\d+)", text)]
            for n in refs:
                if n < 1 or n > attachments_len:
                    errors[idx] = f"question_text references ${n} but attachments length is {attachments_len}. Valid range is $1..${attachments_len if attachments_len>0 else 0}."
                    break

        if errors:
            raise serializers.ValidationError({'questions': errors})

        # Validate section marks consistency and structure
        self.validate_assessment_structure(attrs)

        return attrs

    def validate_assessment_structure(self, attrs):
        """
        Validate assessment structure requirements:
        1. Within each set, all sections should have the same net scoring potential
        2. All sets should have the same section types (structure)
        
        Note: Net scoring potential = positive_marks + negative_marks for each question
        """
        questions = attrs.get('questions', [])
        if not questions:
            return

        # Group questions by set and section
        set_section_data = defaultdict(lambda: defaultdict(list))
        
        for question in questions:
            set_number = question.get('set_number', 1)
            section_id = question.get('section_id')
            positive_marks = question.get('positive_marks', 0)
            negative_marks = question.get('negative_marks', 0)
            
            # Calculate net scoring potential (positive + negative marks)
            net_marks = positive_marks + negative_marks
            set_section_data[set_number][section_id].append(net_marks)

        # Calculate total marks per section PER SET using net scoring potential
        set_section_totals = {}
        for set_number, sections in set_section_data.items():
            set_section_totals[set_number] = {}
            for section_id, net_marks_list in sections.items():
                set_section_totals[set_number][section_id] = sum(net_marks_list)

        # Validation 1: Within each set, all sections should have the same net scoring potential
        errors = {}
        for set_number, section_totals in set_section_totals.items():
            if not section_totals:
                continue
                
            unique_totals = list(set(section_totals.values()))
            if len(unique_totals) > 1:
                section_details = []
                for section_id, total in section_totals.items():
                    section_details.append(f"Section {section_id}: {total} net marks")
                
                errors[f'set_{set_number}_marks_consistency'] = (
                    f"All sections in set {set_number} must have the same net scoring potential. "
                    f"Found different totals: {', '.join(section_details)}. "
                    f"Please ensure all sections in the same set have equal net scoring potential (positive_marks + negative_marks)."
                )

        # Validation 2: All sets should have the same section structure
        if len(set_section_totals) > 1:
            # Get section IDs from the first set as reference
            sets_list = sorted(set_section_totals.keys())
            reference_set = sets_list[0]
            reference_sections = set(set_section_totals[reference_set].keys())
            
            for set_number in sets_list[1:]:
                current_sections = set(set_section_totals[set_number].keys())
                
                if reference_sections != current_sections:
                    missing_in_current = reference_sections - current_sections
                    extra_in_current = current_sections - reference_sections
                    
                    error_msg = f"Set {set_number} has different section structure than set {reference_set}. "
                    if missing_in_current:
                        error_msg += f"Missing sections: {sorted(missing_in_current)}. "
                    if extra_in_current:
                        error_msg += f"Extra sections: {sorted(extra_in_current)}. "
                    error_msg += "All sets must have the same section types/structure."
                    
                    errors[f'set_{set_number}_structure_consistency'] = error_msg

        # Validation 3: NEW - Ensure each section has consistent marks across sets
        # This enforces that if section 1 has 50 marks in set 1, it should have 50 marks in set 2 too
        if len(set_section_totals) > 1:
            sets_list = sorted(set_section_totals.keys())
            reference_set = sets_list[0]
            reference_totals = set_section_totals[reference_set]
            
            for set_number in sets_list[1:]:
                current_totals = set_section_totals[set_number]
                
                for section_id in reference_totals:
                    if section_id in current_totals:
                        ref_marks = reference_totals[section_id]
                        curr_marks = current_totals[section_id]
                        
                        if ref_marks != curr_marks:
                            errors[f'section_{section_id}_cross_set_consistency'] = (
                                f"Section {section_id} has inconsistent net scoring potential across sets. "
                                f"Set {reference_set}: {ref_marks} net marks, Set {set_number}: {curr_marks} net marks. "
                                f"Each section must have the same net scoring potential (positive_marks + negative_marks) in every set."
                            )

        if errors:
            raise serializers.ValidationError(errors)

    def calculate_total_marks_and_duration_by_set(self, questions_data):
        """Calculate total net scoring potential and duration for each set number"""
        set_marks = defaultdict(int)
        set_duration = defaultdict(int)
        
        for question in questions_data:
            set_num = question.get('set_number', 1)
            positive_marks = question.get('positive_marks', 0)
            negative_marks = question.get('negative_marks', 0)
            # Calculate net scoring potential
            net_marks = positive_marks + negative_marks
            set_marks[set_num] += net_marks
            set_duration[set_num] += question.get('time_limit', 0)
            
        return dict(set_marks), dict(set_duration)

    def calculate_section_totals(self, questions_data, section_id, set_marks, set_duration):
        """Calculate net scoring potential and duration for a specific section ACROSS ALL SETS"""
        section_questions = [q for q in questions_data if q.get('section_id') == section_id]
        
        if not section_questions:
            return 0, 0
            
        # Calculate totals for this section's questions across ALL sets using net scoring potential
        total_marks = 0
        total_duration = 0
        
        for question in section_questions:
            positive_marks = question.get('positive_marks', 0)
            negative_marks = question.get('negative_marks', 0)
            net_marks = positive_marks + negative_marks
            total_marks += net_marks
            total_duration += question.get('time_limit', 0)
        
        return total_marks, total_duration

    @transaction.atomic
    def create(self, validated_data):
        # Extract input data
        total_sets = validated_data.pop('total_sets')  # Changed from num_of_sets
        section_names = validated_data.pop('section_names')
        section_descriptions = validated_data.pop('section_descriptions')
        is_electron_only = validated_data.pop('is_electron_only')
        ai_generated_questions = validated_data.pop('ai_generated_questions')  # Changed from num_of_ai_generated_questions
        questions_data = validated_data.pop('questions')
        attachments = validated_data.pop('attachments', [])

        # Calculate total marks and duration from questions
        set_marks, set_duration = self.calculate_total_marks_and_duration_by_set(questions_data)
        
        # Calculate assessment totals (sum across all sets)
        total_marks = sum(set_marks.values())
        duration_seconds = sum(set_duration.values())
        duration_minutes = duration_seconds // 60  # Convert to minutes

        # Create Assessment object
        assessment = Assessment.objects.create(
            created_by=self.context['request'].user,
            is_published=validated_data.get('is_published', False),
            passing_marks=validated_data.get('passing_marks', 0),
            total_marks=total_marks,
            duration=duration_minutes,
            total_sets=total_sets,  # Changed from num_of_sets
            is_proctored=validated_data.get('is_proctored', False),
            start_time=validated_data.get('start_time'),
            end_time=validated_data.get('end_time'),
            is_electron_only=is_electron_only,
            ai_generated_questions=ai_generated_questions,  # Changed from num_of_ai_generated_questions
            attachments=attachments,
            # These fields are now handled by source mapping
            **{k: v for k, v in validated_data.items() if k in ['title', 'description', 'assessment_type']}
        )

        # Create Section objects
        created_sections = {}
        for index, section_name in enumerate(section_names):
            section_description = ""
            if index < len(section_descriptions):
                section_description = section_descriptions[index]
            
            # Calculate section totals
            section_id = index + 1  # section_id in questions starts from 1
            section_total_marks, section_duration_seconds = self.calculate_section_totals(
                questions_data, section_id, set_marks, set_duration
            )
            section_duration_minutes = section_duration_seconds // 60
            
            section = Section.objects.create(
                assessment=assessment,
                name=section_name,
                description=section_description,
                section_order=index,  # 0-based index as section_order
                total_marks=section_total_marks,
                duration=section_duration_minutes
            )
            # Map section_id (1-based) to the created section object
            created_sections[section_id] = section

        # Create Question objects
        for question_index, question_data in enumerate(questions_data):
            section_id = question_data.get('section_id')
            section = created_sections.get(section_id)
            
            if not section:
                raise serializers.ValidationError(f"Invalid section_id: {section_id}")

            # Prepare correct_answer from options and correct_option_index
            options = question_data.get('options', [])
            correct_answer = None
            if options and 'correct_option_index' in question_data:
                correct_index = question_data['correct_option_index']
                if 0 <= correct_index < len(options):
                    correct_answer = options[correct_index]

            Question.objects.create(
                question_type=question_data.get('question_type', 'non-coding'),
                section=section,
                set_number=question_data.get('set_number', 1),
                question_text=question_data.get('question_text', ''),
                options=options,
                correct_answer=correct_answer,
                marks=question_data.get('positive_marks', 0),
                negative_marks=question_data.get('negative_marks', 0),
                question_order=question_index,
                description=question_data.get('description', ''),
                constraints=question_data.get('constraints', []),
                test_cases=question_data.get('test_cases', {}),
                time_limit=question_data.get('time_limit', 0)
            )

        return assessment

    @transaction.atomic  
    def update(self, instance, validated_data):
        # Handle update logic if needed
        # For now, implementing basic field updates
        
        # Extract nested data if present
        questions_data = validated_data.pop('questions', None)
        section_names = validated_data.pop('section_names', None)
        section_descriptions = validated_data.pop('section_descriptions', None)
        
        # Map input fields to model fields if needed for update
        if 'assessment_name' in validated_data:
            validated_data['title'] = validated_data.pop('assessment_name')
        if 'assessment_description' in validated_data:
            validated_data['description'] = validated_data.pop('assessment_description')
        if 'num_of_sets' in validated_data:
            instance.total_sets = validated_data.pop('num_of_sets')
        if 'is_electron_only' in validated_data:
            instance.is_electron_only = validated_data.pop('is_electron_only')
        if 'num_of_ai_generated_questions' in validated_data:
            instance.ai_generated_questions = validated_data.pop('num_of_ai_generated_questions')
            
        # Remove unused fields
        validated_data.pop('attachments', None)
        
        # Update remaining fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        # Recalculate totals if questions are updated
        if questions_data:
            set_marks, set_duration = self.calculate_total_marks_and_duration_by_set(questions_data)
            instance.total_marks = sum(set_marks.values())
            instance.duration = sum(set_duration.values()) // 60
            
            # Update sections and questions (simplified - you might want more complex logic)
            instance.sections.all().delete()  # Delete existing sections and questions
            
            # Recreate sections and questions (reuse create logic)
            if section_names:
                created_sections = {}
                for index, section_name in enumerate(section_names):
                    section_description = ""
                    if section_descriptions and index < len(section_descriptions):
                        section_description = section_descriptions[index]
                    
                    section_id = index + 1
                    section_total_marks, section_duration_seconds = self.calculate_section_totals(
                        questions_data, section_id, set_marks, set_duration
                    )
                    
                    section = Section.objects.create(
                        assessment=instance,
                        name=section_name,
                        description=section_description,
                        section_order=index,
                        total_marks=section_total_marks,
                        duration=section_duration_seconds // 60
                    )
                    # Map section_id (1-based) to the created section object
                    created_sections[section_id] = section
                
                # Recreate questions
                for question_index, question_data in enumerate(questions_data):
                    section_id = question_data.get('section_id')
                    section = created_sections.get(section_id)
                    
                    if section:
                        options = question_data.get('options', [])
                        correct_answer = None
                        if options and 'correct_option_index' in question_data:
                            correct_index = question_data['correct_option_index']
                            if 0 <= correct_index < len(options):
                                correct_answer = options[correct_index]
                        
                        Question.objects.create(
                            question_type=question_data.get('question_type', 'non-coding'),
                            section=section,
                            set_number=question_data.get('set_number', 1),
                            question_text=question_data.get('question_text', ''),
                            options=options,
                            correct_answer=correct_answer,
                            marks=question_data.get('positive_marks', 0),
                            negative_marks=question_data.get('negative_marks', 0),
                            question_order=question_index,
                            description=question_data.get('description', ''),
                            constraints=question_data.get('constraints', []),
                            test_cases=question_data.get('test_cases', {}),
                            time_limit=question_data.get('time_limit', 0)
                        )
        
        instance.save()
        return instance
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'full_name', 'email', 'created_at']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'full_name', 'phone_number', 'created_at']


class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    
    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("File must be a CSV file.")
        return value
    
class CSVUploadModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVUpload
        fields = [
            'id',
            'uploaded_by',
            'uploaded_at',
            'file_name',
            'total_records',
            'processed_records',
            'status',
            'errors'
        ]
        read_only_fields = ['uploaded_by', 'uploaded_at']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'role',]
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        EmailWhitelist.objects.create(role=user.role, email=user.email)
        return user


class AssessmentAssignmentSerializer(serializers.Serializer):
    assessment_id = serializers.IntegerField()
    csv_upload_id = serializers.IntegerField()
    
    def validate_assessment_id(self, value):
        try:
            assessment = Assessment.objects.get(id=value, is_active=True)
            return value
        except Assessment.DoesNotExist:
            raise serializers.ValidationError("Assessment not found or inactive")
    
    def validate_csv_upload_id(self, value):
        try:
            csv_upload = CSVUpload.objects.get(id=value)
            if csv_upload.status != 'completed':
                raise serializers.ValidationError("CSV upload must be completed successfully")
            return value
        except CSVUpload.DoesNotExist:
            raise serializers.ValidationError("CSV upload not found")

class TestCodeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    assessment_title = serializers.CharField(source='assessment.title', read_only=True)
    
    class Meta:
        model = TestCode
        fields = ['id', 'code', 'student_name', 'student_email', 'assessment_title', 
                 'created_at', 'is_used', 'used_at']
        
        
class SendEmailSerializer(serializers.Serializer):
    csv_upload_id = serializers.IntegerField()
    subject = serializers.CharField(max_length=255)
    content = serializers.CharField()
    content_type = serializers.ChoiceField(
        choices=[('text', 'Plain Text'), ('html', 'HTML')], 
        default='text'
    )

    def validate_csv_upload_id(self, value):
        try:
            csv_upload = CSVUpload.objects.get(id=value)
            return value
        except CSVUpload.DoesNotExist:
            raise serializers.ValidationError("CSV Upload not found.")

class EmailStatusSerializer(serializers.Serializer):
    student_email = serializers.EmailField()
    status = serializers.CharField()
    error_message = serializers.CharField(required=False, allow_blank=True)
    
class GeneratePresignedURLSerializer(serializers.Serializer):
    assessment_id = serializers.IntegerField()
    filename = serializers.CharField(max_length=255)
    
    def validate_assessment_id(self, value):
        try:
            Assessment.objects.get(id=value)
            return value
        except Assessment.DoesNotExist:
            raise serializers.ValidationError("Assessment not found.")
    
    def validate(self, attrs):
        assessment_id = attrs['assessment_id']
        filename = attrs['filename']
        
        # Check if this combination already exists and is uploaded
        existing_file = AssessmentFile.objects.filter(
            assessment_id=assessment_id,
            filename=filename
        ).first()
        
        if existing_file and existing_file.upload_status == 'uploaded':
            raise serializers.ValidationError(
                "File with this name already exists for this assessment."
            )
        
        return attrs
    
class CheckFileStatusSerializer(serializers.Serializer):
    assessment_id = serializers.IntegerField()
    filename = serializers.CharField(max_length=255)
    
    def validate_assessment_id(self, value):
        try:
            Assessment.objects.get(id=value)
            return value
        except Assessment.DoesNotExist:
            raise serializers.ValidationError("Assessment not found.")

class AssessmentFileSerializer(serializers.ModelSerializer):
    s3_full_url = serializers.ReadOnlyField()
    file_size_mb = serializers.SerializerMethodField()
    
    class Meta:
        model = AssessmentFile
        fields = [
            'id', 'assessment', 'filename', 's3_key', 's3_url', 'file_size', 
            'file_size_mb', 'upload_status', 'created_at', 'updated_at', 's3_full_url'
        ]
        read_only_fields = ['s3_key', 's3_url', 'file_size', 'upload_status']
    
    def get_file_size_mb(self, obj):
        if obj.file_size:
            return round(obj.file_size / (1024 * 1024), 2)
        return 0
    
class TestCodeSubmissionSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500, help_text="JWT token containing test code")
    image = serializers.ImageField(help_text="Image file to upload")
    

class QuestionResponseSerializer(serializers.Serializer):
    """Serializer for individual question response data"""
    question_id = serializers.IntegerField()
    is_attempted = serializers.BooleanField(default=False)
    selected_option_index = serializers.IntegerField(required=False, allow_null=True)
    code_answer = serializers.CharField(required=False, allow_blank=True)
    is_correct = serializers.BooleanField()
    marks_obtained = serializers.FloatField()
    total_marks = serializers.FloatField()  # Required: total marks available for this question
    time_spent = serializers.IntegerField(default=0)  # in seconds

    def validate_question_id(self, value):
        """Validate that question_id exists in database"""
        from .models import Question
        if not Question.objects.filter(id=value).exists():
            raise ValidationError(f"Question with ID {value} does not exist")
        return value

    def validate(self, data):
        """Cross-field validation"""
        if data['marks_obtained'] > data['total_marks']:
            raise ValidationError("Marks obtained cannot be greater than total marks")
        return data


class SectionResponseSerializer(serializers.Serializer):
    """Serializer for section-wise performance data"""
    section_id = serializers.IntegerField()
    set_number = serializers.IntegerField()  # Required: set number
    questions = QuestionResponseSerializer(many=True)
    time_spent = serializers.IntegerField(default=0)  # total section time in seconds

    def validate_section_id(self, value):
        """Validate that section_id exists in database"""
        from .models import Section
        if not Section.objects.filter(id=value).exists():
            raise ValidationError(f"Section with ID {value} does not exist")
        return value

    def validate_set_number(self, value):
        """Validate set number is positive"""
        if value < 1:
            raise ValidationError("Set number must be positive")
        return value

    def validate(self, data):
        """Validate section-question relationship"""
        from .models import Question
        section_id = data['section_id']
        set_number = data['set_number']
        
        for question_data in data['questions']:
            question_id = question_data['question_id']
            try:
                question = Question.objects.get(id=question_id)
                if question.section_id != section_id:
                    raise ValidationError(f"Question {question_id} does not belong to section {section_id}")
                if question.set_number != set_number:
                    raise ValidationError(f"Question {question_id} does not belong to set {set_number}")
            except Question.DoesNotExist:
                raise ValidationError(f"Question {question_id} does not exist")
        
        return data
    

class GenerateStudentReportSerializer(serializers.Serializer):
    """
    New clean serializer for generating student reports with actual performance data
    """
    # Student/User identification
    assessment_id = serializers.IntegerField()
    student_email = serializers.EmailField(required=False)
    candidate_email = serializers.EmailField(required=False)
    
    # Test session data
    started_at = serializers.DateTimeField()
    ended_at = serializers.DateTimeField()
    submitted_at = serializers.DateTimeField()
    
    # Performance data
    sections = SectionResponseSerializer(many=True)
    
    # Optional proctoring data
    window_switch_count = serializers.IntegerField(default=0)
    is_cheating = serializers.BooleanField(default=False)
    cheating_reason = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        """Validate that either student_email or candidate_email is provided"""
        if not attrs.get('student_email') and not attrs.get('candidate_email'):
            raise serializers.ValidationError(
                "Either student_email or candidate_email must be provided"
            )
        
        # Ensure only one type of user is specified
        if attrs.get('student_email') and attrs.get('candidate_email'):
            raise serializers.ValidationError(
                "Provide either student_email OR candidate_email, not both"
            )
            
        return attrs


# Keep the old serializer for backward compatibility (deprecated)
class GenerateStudentReportRequestSerializer(serializers.Serializer):
    """DEPRECATED: Use GenerateStudentReportSerializer instead"""
    report_id = serializers.CharField(required=False)
    assessment_id = serializers.IntegerField(required=False)
    candidate_id = serializers.IntegerField(required=False)
    candidate_email = serializers.EmailField(required=False)
    student_email = serializers.EmailField(required=False)

    def validate(self, attrs):
        if not attrs.get('report_id') and not (attrs.get('assessment_id') and (attrs.get('candidate_id') or attrs.get('candidate_email') or attrs.get('student_email'))):
            raise serializers.ValidationError(
                "Provide either report_id OR assessment_id with candidate_id/candidate_email/student_email"
            )
        return attrs

class RunCodeSerializer(serializers.Serializer):
    """
    Serializer for code execution request with validation
    """
    script = serializers.CharField(
        help_text="The code to execute",
        error_messages={
            'required': 'Script is required',
            'blank': 'Script cannot be empty'
        }
    )
    language = serializers.CharField(
        help_text="Programming language (e.g., python3, java, cpp, javascript, etc.)",
        error_messages={
            'required': 'Language is required',
            'blank': 'Language cannot be empty'
        }
    )
    versionIndex = serializers.CharField(
        help_text="Language version index (e.g., '3' for Python 3, '0' for latest)",
        error_messages={
            'required': 'Version index is required',
            'blank': 'Version index cannot be empty'
        }
    )
    stdin = serializers.CharField(
        required=False, 
        allow_blank=True, 
        default="",
        help_text="Input for the program (optional)"
    )
    
    def validate(self, attrs):
        """
        Validate the entire serializer data and check for JDoodle credentials
        """
        # Check for JDoodle credentials in environment variables
        client_id = os.getenv('JDOODLE_CLIENT_ID')
        client_secret = os.getenv('JDOODLE_SECRET_KEY')
        
        if not client_id:
            raise ValidationError({
                'configuration_error': 'JDOODLE_CLIENT_ID not found in environment variables'
            })
        
        if not client_secret:
            raise ValidationError({
                'configuration_error': 'JDOODLE_SECRET_KEY not found in environment variables'
            })
        
        # Validate client_id format (should be alphanumeric)
        if not client_id.replace('-', '').replace('_', '').isalnum():
            raise ValidationError({
                'configuration_error': 'Invalid JDOODLE_CLIENT_ID format'
            })
        
        return attrs
    
    def validate_script(self, value):
        """
        Validate script field
        """
        if not value or not value.strip():
            raise ValidationError("Script cannot be empty or contain only whitespace")
        
        # Optional: Check script length (JDoodle has limits)
        if len(value) > 50000:  # 50KB limit
            raise ValidationError("Script is too long. Maximum length is 50,000 characters")
        
        return value.strip()
    
    def validate_language(self, value):
        """
        Validate language field
        """
        if not value or not value.strip():
            raise ValidationError("Language cannot be empty")
        
        # List of supported languages (you can expand this)
        supported_languages = [
            'python3', 'python2', 'java', 'cpp', 'cpp14', 'cpp17',
            'c', 'csharp', 'php', 'perl', 'ruby', 'go', 'scala',
            'bash', 'sql', 'pascal', 'fsharp', 'clojure', 'haskell',
            'lua', 'erlang', 'rust', 'dart', 'r', 'groovy', 'kotlin',
            'swift', 'javascript', 'nodejs', 'coffeescript'
        ]
        
        if value.lower() not in supported_languages:
            raise ValidationError(
                f"Unsupported language '{value}'. "
                f"Supported languages: {', '.join(supported_languages[:10])}... "
                f"(and {len(supported_languages)-10} more)"
            )
        
        return value.lower()
    
    def validate_versionIndex(self, value):
        """
        Validate versionIndex field
        """
        if not value or not value.strip():
            raise ValidationError("Version index cannot be empty")
        
        # Check if it's a valid number (most version indices are numeric)
        if not value.isdigit():
            raise ValidationError("Version index should be a numeric value")
        
        # Check reasonable range (most languages have version indices 0-10)
        version_int = int(value)
        if version_int < 0 or version_int > 20:
            raise ValidationError("Version index should be between 0 and 20")
        
        return value
    
    def validate_stdin(self, value):
        """
        Validate stdin field
        """
        # Optional: Limit stdin size
        if value and len(value) > 10000:  # 10KB limit for input
            raise ValidationError("Input is too long. Maximum length is 10,000 characters")
        
        return value if value else ""
    
    
class SubmitCodeSerializer(serializers.Serializer):
    """
    Serializer for code submission with test case validation
    """
    script = serializers.CharField(
        help_text="The code to execute",
        error_messages={
            'required': 'Script is required',
            'blank': 'Script cannot be empty'
        }
    )
    language = serializers.CharField(
        help_text="Programming language (e.g., python3, java, cpp, javascript, etc.)",
        error_messages={
            'required': 'Language is required',
            'blank': 'Language cannot be empty'
        }
    )
    versionIndex = serializers.CharField(
        help_text="Language version index (e.g., '3' for Python 3, '0' for latest)",
        error_messages={
            'required': 'Version index is required',
            'blank': 'Version index cannot be empty'
        }
    )
    question_id = serializers.IntegerField(
        help_text="ID of the question to validate against",
        error_messages={
            'required': 'Question ID is required'
        }
    )
    
    def validate(self, attrs):
        """
        Validate the entire serializer data and check for JDoodle credentials
        """
        # Check for JDoodle credentials in environment variables
        client_id = os.getenv('JDOODLE_CLIENT_ID')
        client_secret = os.getenv('JDOODLE_SECRET_KEY')
        
        if not client_id:
            raise ValidationError({
                'configuration_error': 'JDOODLE_CLIENT_ID not found in environment variables'
            })
        
        if not client_secret:
            raise ValidationError({
                'configuration_error': 'JDOODLE_SECRET_KEY not found in environment variables'
            })
        
        return attrs
    
    def validate_question_id(self, value):
        """
        Validate that the question exists and is a coding question
        """
        try:
            question = Question.objects.get(id=value)
        except Question.DoesNotExist:
            raise ValidationError(f"Question with ID {value} does not exist")
        
        if question.question_type != 'coding':
            raise ValidationError(f"Question with ID {value} is not a coding question")
        
        return value
    
    def validate_script(self, value):
        """
        Validate script field
        """
        if not value or not value.strip():
            raise ValidationError("Script cannot be empty or contain only whitespace")
        
        if len(value) > 50000:  # 50KB limit
            raise ValidationError("Script is too long. Maximum length is 50,000 characters")
        
        return value.strip()
    
    def validate_language(self, value):
        """
        Validate language field
        """
        if not value or not value.strip():
            raise ValidationError("Language cannot be empty")
        
        supported_languages = [
            'python3', 'python2', 'java', 'cpp', 'cpp14', 'cpp17',
            'c', 'csharp', 'php', 'perl', 'ruby', 'go', 'scala',
            'bash', 'sql', 'pascal', 'fsharp', 'clojure', 'haskell',
            'lua', 'erlang', 'rust', 'dart', 'r', 'groovy', 'kotlin',
            'swift', 'javascript', 'nodejs', 'coffeescript'
        ]
        
        if value.lower() not in supported_languages:
            raise ValidationError(
                f"Unsupported language '{value}'. "
                f"Supported languages: {', '.join(supported_languages[:10])}... "
                f"(and {len(supported_languages)-10} more)"
            )
        
        return value.lower()
    
    def validate_versionIndex(self, value):
        """
        Validate versionIndex field
        """
        if not value or not value.strip():
            raise ValidationError("Version index cannot be empty")
        
        if not value.isdigit():
            raise ValidationError("Version index should be a numeric value")
        
        version_int = int(value)
        if version_int < 0 or version_int > 20:
            raise ValidationError("Version index should be between 0 and 20")
        
        return value