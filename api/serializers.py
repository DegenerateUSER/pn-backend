from botocore.client import Config
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
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Section
        fields = '__all__'


class AssessmentSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    # Input/Output fields with custom names
    assessment_name = serializers.CharField(source='title')
    assessment_description = serializers.CharField(source='description', required=False, allow_blank=True)
    set_number = serializers.IntegerField(write_only=True)
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
            'total_marks', 'passing_marks', 'duration', 'set_number', 'is_proctored', 
            'start_time', 'end_time', 'is_electron_only', 'ai_generated_questions',
            'sections',
            # Write-only fields for input
            'num_of_sets', 'section_names', 'section_descriptions', 
            'num_of_ai_generated_questions', 'questions', 'attachments'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def calculate_total_marks_and_duration_by_set(self, questions_data):
        """Calculate total marks and duration for each set number"""
        set_marks = defaultdict(int)
        set_duration = defaultdict(int)
        
        for question in questions_data:
            set_num = question.get('set_number', 1)
            set_marks[set_num] += question.get('positive_marks', 0)
            set_duration[set_num] += question.get('time_limit', 0)
            
        return dict(set_marks), dict(set_duration)

    def calculate_section_totals(self, questions_data, section_id, set_marks, set_duration):
        """Calculate total marks and duration for a specific section"""
        section_questions = [q for q in questions_data if q.get('section_id') == section_id]
        
        if not section_questions:
            return 0, 0
            
        # Get the set_number from the first question of this section
        set_number = section_questions[0].get('set_number', 1)
        
        # Calculate totals for this section's questions only
        total_marks = sum(q.get('positive_marks', 0) for q in section_questions)
        total_duration = sum(q.get('time_limit', 0) for q in section_questions)
        
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
    
