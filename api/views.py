from .models import *
from .serializers import *
from .utils import generate_jwt_tokens
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .authentication import *
import os
import string
import random
from google.oauth2 import id_token
from google.auth.transport import requests
from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils.dateparse import parse_datetime
from .models import Assessment, Section, Question
from .serializers import *

import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
import csv
import io
from api.authentication import *
from django.core.mail import send_mail
from typing import List, Dict
from django.conf import settings
from api.utils import *
from datetime import timedelta

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """This is called after validation but before saving"""
        user = serializer.save()
        user.token = generate_jwt_tokens(user)
        return user


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']

        token = generate_jwt_tokens(user)
        
        return Response({'token': token}, status=status.HTTP_201_CREATED)


#to be cleaned and serializer needs to be added here
@method_decorator(csrf_exempt, name='dispatch')
class ResetPasswordView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

 

    def post(self, request):
        print(request.user)
        if isinstance(request.user, AnonymousUser):
            return Response({"error":"Please add the valid token"}, status=status.HTTP_400_BAD_REQUEST)
        user_id = request.user.id
        new_password = request.data.get("new_password")

        if not user_id or not new_password:
            return Response(
                {"error": "new_password is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password has been reset successfully"},
            status=status.HTTP_200_OK
        )
    
@csrf_exempt
def sign_in(request):
    return render(request, 'sign_in.html')
     
@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']
 
    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['OAUTH_CLIENT_ID']
        )
        print(user_data)
    except Exception as e:
        return JsonResponse({"error":e}, status=status.HTTP_403_FORBIDDEN)
    
    whitelist_check = EmailWhitelist.objects.filter(email = user_data['email']).exists()

    if not whitelist_check:
            return JsonResponse({"error":"Email not whielisted"}, status=status.HTTP_401_UNAUTHORIZED)

    is_oldUser = User.objects.filter(email = user_data['email']).exists()
    if not is_oldUser:
        user = User(email=user_data['email'])
        whitelist_role = EmailWhitelist.objects.get(email = user_data['email']).role
        user.role = whitelist_role
        user.save()

    token = generate_jwt_tokens(user)
        
    return JsonResponse({'token': token}, status=status.HTTP_201_CREATED)



class AssessmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = json.loads(request.body)
            assessment = SampleJSON(data=data)
            assessment.save()
            return Response({"message": "Assessment created successfully"}, status=status.HTTP_201_CREATED)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        try:
            assessment_id = request.query_params.get('id')
            
            if assessment_id:
                
                assessment = get_object_or_404(SampleJSON, id=assessment_id)
                return Response({
                    "id": assessment.id,
                    "data": assessment.data
                }, status=status.HTTP_200_OK)
            else:
              
                assessments = SampleJSON.objects.all()
                assessments_data = []
                for assessment in assessments:
                    assessments_data.append({
                        "id": assessment.id,
                        "data": assessment.data,
                    })
                return Response({
                    "assessments": assessments_data,
                    "count": len(assessments_data)
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
       
        try:
            assessment_id = request.query_params.get('id')
            if not assessment_id:
                return Response({"error": "Assessment ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            assessment = get_object_or_404(SampleJSON, id=assessment_id)
            data = json.loads(request.body)
            
            
            assessment.data = data
            assessment.save()
            
            return Response({
                "message": "Assessment updated successfully",
                "id": assessment.id,
                "data": assessment.data
            }, status=status.HTTP_200_OK)
            
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request):
        
        try:
            assessment_id = request.query_params.get('id')
            if not assessment_id:
                return Response({"error": "Assessment ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            assessment = get_object_or_404(SampleJSON, id=assessment_id)
            data = json.loads(request.body)
            
            
            if hasattr(assessment, 'data') and isinstance(assessment.data, dict):
                assessment.data.update(data)
            else:
                assessment.data = data
                
            assessment.save()
            
            return Response({
                "message": "Assessment partially updated successfully",
                "id": assessment.id,
                "data": assessment.data
            }, status=status.HTTP_200_OK)
            
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request):
        try:
            assessment_id = request.query_params.get('id')
            if not assessment_id:
                return Response({"error": "Assessment ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            assessment = get_object_or_404(SampleJSON, id=assessment_id)
            assessment_data = {
                "id": assessment.id,
                "data": assessment.data
            }
            
            assessment.delete()
            
            return Response({
                "message": "Assessment deleted successfully",
                "deleted_assessment": assessment_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class AssessmentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class AssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = AssessmentPagination
    
    def get_queryset(self):
        
        queryset = Assessment.objects.filter(created_by=self.request.user)
        
        
        assessment_type = self.request.query_params.get('type', None)
        is_published = self.request.query_params.get('is_published', None)
        is_active = self.request.query_params.get('is_active', None)
        search = self.request.query_params.get('search', None)
        
        if assessment_type:
            queryset = queryset.filter(assessment_type=assessment_type)
        if is_published is not None:
            queryset = queryset.filter(is_published=is_published.lower() == 'true')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        if search:
            queryset = queryset.filter(title__icontains=search)
            
        return queryset.select_related('created_by').prefetch_related(
            'sections__questions'
        ).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        try:
            print("requewst received")
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                assessment = serializer.save()
                return Response(
                    {
                        'message': 'Assessment created successfully',
                        'assessment_id': assessment.id,
                        'data': AssessmentSerializer(assessment).data
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    'error': 'Validation failed',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'error': 'Failed to create assessment',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
       
        try:
            assessment = self.get_object()
            serializer = self.get_serializer(assessment)
            return Response({
                'message': 'Assessment retrieved successfully',
                'data': serializer.data
            })
        except Assessment.DoesNotExist:
            return Response(
                {
                    'error': 'Assessment not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            assessment = self.get_object()
            
            
            if assessment.is_published and 'questions' in request.data:
                return Response(
                    {
                        'error': 'Cannot modify questions of a published assessment'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = self.get_serializer(assessment, data=request.data, partial=partial)
            if serializer.is_valid():
                assessment = serializer.save()
                return Response({
                    'message': 'Assessment updated successfully',
                    'data': AssessmentSerializer(assessment).data
                })
            return Response(
                {
                    'error': 'Validation failed',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Assessment.DoesNotExist:
            return Response(
                {
                    'error': 'Assessment not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'error': 'Failed to update assessment',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        
        try:
            assessment = self.get_object()
            
            
            if assessment.is_published:
                return Response(
                    {
                        'error': 'Cannot delete a published assessment'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            assessment_title = assessment.title
            assessment.delete()
            
            return Response({
                'message': f'Assessment "{assessment_title}" deleted successfully'
            })
        except Assessment.DoesNotExist:
            return Response(
                {
                    'error': 'Assessment not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
       
        try:
            assessment = self.get_object()
            
          
            if not assessment.sections.exists():
                return Response(
                    {
                        'error': 'Cannot publish assessment without sections'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not any(section.questions.exists() for section in assessment.sections.all()):
                return Response(
                    {
                        'error': 'Cannot publish assessment without questions'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            assessment.is_published = True
            assessment.save()
            
            return Response({
                'message': 'Assessment published successfully',
                'data': AssessmentSerializer(assessment).data
            })
        except Assessment.DoesNotExist:
            return Response(
                {
                    'error': 'Assessment not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        try:
            assessment = self.get_object()
            assessment.is_published = False
            assessment.save()
            
            return Response({
                'message': 'Assessment unpublished successfully',
                'data': AssessmentSerializer(assessment).data
            })
        except Assessment.DoesNotExist:
            return Response(
                {
                    'error': 'Assessment not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):

        try:
            original_assessment = self.get_object()
            
            with transaction.atomic():

                new_assessment = Assessment.objects.create(
                    title=f"{original_assessment.title} (Copy)",
                    description=original_assessment.description,
                    assessment_type=original_assessment.assessment_type,
                    created_by=request.user,
                    is_published=False,  # Copies are always unpublished
                    total_marks=original_assessment.total_marks,
                    passing_marks=original_assessment.passing_marks,
                    duration=original_assessment.duration,
                    total_sets=original_assessment.total_sets,
                    is_proctored=original_assessment.is_proctored,
                    start_time=original_assessment.start_time,
                    end_time=original_assessment.end_time,
                    is_electron_only=original_assessment.is_electron_only,
                    ai_generated_questions=original_assessment.ai_generated_questions
                )
                
              
                for section in original_assessment.sections.all():
                    new_section = Section.objects.create(
                        assessment=new_assessment,
                        name=section.name,
                        description=section.description,
                        section_order=section.section_order,
                        total_marks=section.total_marks,
                        duration=section.duration
                    )
                    
                    for question in section.questions.all():
                        Question.objects.create(
                            section=new_section,
                            set_number=question.set_number,
                            question_text=question.question_text,
                            question_type=question.question_type,
                            options=question.options,
                            correct_answer=question.correct_answer,
                            marks=question.marks,
                            negative_marks=question.negative_marks,
                            question_order=question.question_order,
                            description=question.description,
                            constraints=question.constraints,
                            expected_output=question.expected_output,
                            test_cases=question.test_cases,
                            time_limit=question.time_limit
                        )
            
            return Response({
                'message': 'Assessment duplicated successfully',
                'data': AssessmentSerializer(new_assessment).data
            })
        except Assessment.DoesNotExist:
            return Response(
                {
                    'error': 'Assessment not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'error': 'Failed to duplicate assessment',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def statistics(self, request):

        try:
            user_assessments = self.get_queryset()
            
            stats = {
                'total_assessments': user_assessments.count(),
                'published_assessments': user_assessments.filter(is_published=True).count(),
                'draft_assessments': user_assessments.filter(is_published=False).count(),
                'active_assessments': user_assessments.filter(is_active=True).count(),
                'by_type': {
                    'coding': user_assessments.filter(assessment_type='coding').count(),
                    'non-coding': user_assessments.filter(assessment_type='non-coding').count(),
                    'mix': user_assessments.filter(assessment_type='mix').count(),
                },
                'proctored_assessments': user_assessments.filter(is_proctored=True).count(),
                'recent_assessments': user_assessments.filter(
                    created_at__gte=timezone.now() - timezone.timedelta(days=30)
                ).count()
            }
            
            return Response({
                'message': 'Statistics retrieved successfully',
                'data': stats
            })
        except Exception as e:
            return Response(
                {
                    'error': 'Failed to retrieve statistics',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StudentCSVUploadView(APIView):
    """
    API endpoint to upload CSV file containing student data (name, email)
    Expected CSV format:
    name,email
    John Doe,john@example.com
    Jane Smith,jane@example.com
    """
    parser_classes = [MultiPartParser]
    
    def post(self, request, *args, **kwargs):
        serializer = CSVUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid file format', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        csv_file = serializer.validated_data['file']
        
        try:
            # Read CSV file
            decoded_file = csv_file.read().decode('utf-8')
                        

            csv_data = csv.DictReader(io.StringIO(decoded_file))
            
            # Validate required columns
            required_columns = {'name', 'email'}
            if not required_columns.issubset(csv_data.fieldnames):
                return Response(
                    {'error': f'CSV must contain columns: {", ".join(required_columns)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return self.process_csv_data(csv_data, request.user, csv_file.name)
            
        except Exception as e:
            return Response(
                {'error': 'Failed to process CSV file', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    # def process_csv_data(self, csv_data, user, name):
        """Process CSV data and create students"""
        created_students = []
        skipped_students = []
        errors = []
        
        csv_upload = CSVUpload.objects.create(
                uploaded_by=user,
                file_name=name,
                total_records = sum(1 for row in csv_data),
                processed_records=0,
                status='processing'
            )
        
        # Process CSV data in a transaction
        with transaction.atomic():
            for row_number, row in enumerate(csv_data, start=2):  # Start at 2 for header
                try:
                    print("aa bhi rha h?")
                    full_name = row.get('name', '').strip()
                    email = row.get('email', '').strip().lower()
                    
                    # Validate data
                    if not full_name or not email:
                        errors.append({
                            'row': row_number,
                            'error': 'Name and email are required fields'
                        })
                        continue
                    
                    # Check if student already exists
                    if Student.objects.filter(email=email).exists():
                        skipped_students.append({
                            'name': full_name,
                            'email': email,
                            'reason': 'Email already exists'
                        })
                        continue
                    
                    # Create student
                    student = Student.objects.create(full_name=full_name, email=email, csv_upload=csv_upload)
                    created_students.append(StudentSerializer(student).data)
                    
                except Exception as e:
                    errors.append({
                        'row': row_number,
                        'error': str(e)
                    })
        
        # Prepare response
        result = {
            'message': 'CSV processing completed',
            'summary': {
                'total_processed': len(created_students) + len(skipped_students) + len(errors),
                'created': len(created_students),
                'skipped': len(skipped_students),
                'errors': len(errors)
            },
            'created_students': created_students,
            'skipped_students': skipped_students,
            'errors': errors
        }
        csv_upload.processed_records = result['summary']['total_processed']
        csv_upload.status = 'completed' if not result['errors'] else 'completed_with_errors'
        csv_upload.errors = result['errors'] if result['errors'] else None
        csv_upload.save()
        
        
        return Response(result, status=status.HTTP_201_CREATED)
    def process_csv_data(self, csv_data, user, name):
        """Process CSV data and create students"""
        created_students = []
        skipped_students = []
        errors = []
        
        # Convert csv_data to list to avoid iterator exhaustion
        csv_rows = list(csv_data)
        
        csv_upload = CSVUpload.objects.create(
            uploaded_by=user,
            file_name=name,
            total_records=len(csv_rows),  # Use len() on the list instead
            processed_records=0,
            status='processing'
        )
        
        # Process CSV data in a transaction
        with transaction.atomic():
            for row_number, row in enumerate(csv_rows, start=2):  # Start at 2 for header
                try:
                    print("aa bhi rha h?")
                    full_name = row.get('name', '').strip()
                    email = row.get('email', '').strip().lower()
                    
                    # Validate data
                    if not full_name or not email:
                        errors.append({
                            'row': row_number,
                            'error': 'Name and email are required fields'
                        })
                        continue
                    
                    # Check if student already exists
                    if Student.objects.filter(email=email).exists():
                        skipped_students.append({
                            'name': full_name,
                            'email': email,
                            'reason': 'Email already exists'
                        })
                        continue
                    
                    # Create student
                    student = Student.objects.create(full_name=full_name, email=email, csv_upload=csv_upload)
                    created_students.append(StudentSerializer(student).data)
                    
                except Exception as e:
                    errors.append({
                        'row': row_number,
                        'error': str(e)
                    })
        
        # Prepare response
        result = {
            'message': 'CSV processing completed',
            'summary': {
                'total_processed': len(created_students) + len(skipped_students) + len(errors),
                'created': len(created_students),
                'skipped': len(skipped_students),
                'errors': len(errors)
            },
            'created_students': created_students,
            'skipped_students': skipped_students,
            'errors': errors
        }
        csv_upload.processed_records = result['summary']['total_processed']
        csv_upload.status = 'completed' if not result['errors'] else 'completed_with_errors'
        csv_upload.errors = result['errors'] if result['errors'] else None
        csv_upload.save()
        
        return Response(result, status=status.HTTP_201_CREATED)
    
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        role = self.request.query_params.get('role', None)
        if role in ['assessment_manager', 'proctor']:
            return User.objects.filter(role=role)
        return User.objects.filter(role__in=['assessment_manager', 'proctor'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'status': 'success',
                'message': 'User created successfully',
                'data': UserCreateSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': 'Failed to create user',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]



class CSVUploadViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing CSV uploads.
    GET /api/csv-uploads/ - List all uploads
    GET /api/csv-uploads/{id}/ - Get specific upload
    """
    serializer_class = CSVUploadModelSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return uploads for the current user"""
        return CSVUpload.objects.filter(
            uploaded_by=self.request.user
        ).order_by('-uploaded_at')

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        upload = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(upload)
        return Response(serializer.data)

class AssignAssessmentToCSVView(APIView):
    """
    API endpoint to assign an assessment to all students from a CSV upload.
    This will create unique test codes for each student-assessment pair.
    """
    
    def post(self, request, *args, **kwargs):
        serializer = AssessmentAssignmentSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid data', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        assessment_id = serializer.validated_data['assessment_id']
        csv_upload_id = serializer.validated_data['csv_upload_id']
        
        try:
            assessment = Assessment.objects.get(id=assessment_id)
            csv_upload = CSVUpload.objects.get(id=csv_upload_id)
            
            # Check if this assessment is already assigned to this CSV upload
            existing_codes = TestCode.objects.filter(
                assessment=assessment,
                student__csv_upload=csv_upload
            ).exists()
            
            if existing_codes:
                return Response(
                    {'error': 'Assessment already assigned to students from this CSV upload'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return self.create_test_codes(assessment, csv_upload)
            
        except Exception as e:
            return Response(
                {'error': 'Failed to assign assessment', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create_test_codes(self, assessment, csv_upload):
        """Create unique test codes for all students in the CSV upload"""
        
        # Get all students from this CSV upload
        students = Student.objects.filter(csv_upload=csv_upload)
        
        if not students.exists():
            return Response(
                {'error': 'No students found in the specified CSV upload'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_codes = []
        skipped_codes = []
        errors = []
        
        # Generate universal code for assessment if not exists
        if not assessment.universal_code:
            assessment.universal_code = self.generate_universal_code()
            assessment.save()
        
        with transaction.atomic():
            for student in students:
                try:
                    # Check if test code already exists for this student-assessment pair
                    existing_code = TestCode.objects.filter(
                        student=student,
                        assessment=assessment
                    ).first()
                    
                    if existing_code:
                        skipped_codes.append({
                            'student_email': student.email,
                            'student_name': student.full_name,
                            'existing_code': existing_code.code,
                            'reason': 'Test code already exists'
                        })
                        continue
                    
                    # Generate unique test code
                    unique_code = self.generate_unique_test_code()
                    
                    # Create test code
                    test_code = TestCode.objects.create(
                        code=unique_code,
                        student=student,
                        assessment=assessment
                    )
                    
                    created_codes.append(TestCodeSerializer(test_code).data)
                    
                except Exception as e:
                    errors.append({
                        'student_email': student.email,
                        'student_name': student.full_name,
                        'error': str(e)
                    })
        
        # Prepare response
        response_data = {
            'message': 'Assessment assignment completed',
            'assessment': {
                'id': assessment.id,
                'title': assessment.title,
                'universal_code': assessment.universal_code
            },
            'csv_upload': {
                'id': csv_upload.id,
                'file_name': csv_upload.file_name,
                'total_students': csv_upload.processed_records
            },
            'summary': {
                'total_students': students.count(),
                'codes_created': len(created_codes),
                'codes_skipped': len(skipped_codes),
                'errors': len(errors)
            },
            'created_test_codes': created_codes,
            'skipped_codes': skipped_codes,
            'errors': errors
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def generate_unique_test_code(self, length=8):
        """Generate a unique test code"""
        characters = string.ascii_uppercase + string.digits
        
        while True:
            code = ''.join(random.choice(characters) for _ in range(length))
            # Ensure uniqueness
            if not TestCode.objects.filter(code=code).exists():
                return code
    
    def generate_universal_code(self, length=12):
        """Generate a universal code for the assessment"""
        characters = string.ascii_uppercase + string.digits
        return 'UNIV-' + ''.join(random.choice(characters) for _ in range(length))

class GetAssessmentTestCodesView(APIView):
    """
    API endpoint to get all test codes for a specific assessment
    """
    
    def get(self, request, assessment_id, *args, **kwargs):
        try:
            assessment = Assessment.objects.get(id=assessment_id, is_active=True)
        except Assessment.DoesNotExist:
            return Response(
                {'error': 'Assessment not found or inactive'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get query parameters for filtering
        csv_upload_id = request.query_params.get('csv_upload_id')
        is_used = request.query_params.get('is_used')
        
        # Base queryset
        test_codes = TestCode.objects.filter(assessment=assessment).select_related(
            'student', 'assessment'
        )
        
        # Apply filters
        if csv_upload_id:
            test_codes = test_codes.filter(student__csv_upload_id=csv_upload_id)
        
        if is_used is not None:
            is_used_bool = is_used.lower() in ['true', '1']
            test_codes = test_codes.filter(is_used=is_used_bool)
        
        # Serialize data
        serialized_codes = TestCodeSerializer(test_codes, many=True).data
        
        response_data = {
            'assessment': {
                'id': assessment.id,
                'title': assessment.title,
                'universal_code': assessment.universal_code
            },
            'total_codes': test_codes.count(),
            'test_codes': serialized_codes
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

class GetCSVUploadTestCodesView(APIView):
    """
    API endpoint to get all test codes for students from a specific CSV upload
    """
    
    def get(self, request, csv_upload_id, *args, **kwargs):
        try:
            csv_upload = CSVUpload.objects.get(id=csv_upload_id)
        except CSVUpload.DoesNotExist:
            return Response(
                {'error': 'CSV upload not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get query parameters for filtering
        assessment_id = request.query_params.get('assessment_id')
        is_used = request.query_params.get('is_used')
        
        # Base queryset
        test_codes = TestCode.objects.filter(
            student__csv_upload=csv_upload
        ).select_related('student', 'assessment')
        
        # Apply filters
        if assessment_id:
            test_codes = test_codes.filter(assessment_id=assessment_id)
        
        if is_used is not None:
            is_used_bool = is_used.lower() in ['true', '1']
            test_codes = test_codes.filter(is_used=is_used_bool)
        
        # Serialize data
        serialized_codes = TestCodeSerializer(test_codes, many=True).data
        
        response_data = {
            'csv_upload': {
                'id': csv_upload.id,
                'file_name': csv_upload.file_name,
                'uploaded_by': csv_upload.uploaded_by.username,
                'uploaded_at': csv_upload.uploaded_at
            },
            'total_codes': test_codes.count(),
            'test_codes': serialized_codes
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    
class SendBulkEmailView(APIView):
    """
    Send email to all students associated with a CSV upload
    """
    
    def post(self, request):
        serializer = SendEmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid data', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        csv_upload_id = serializer.validated_data['csv_upload_id']
        subject = serializer.validated_data['subject']
        content = serializer.validated_data['content']
        content_type = serializer.validated_data['content_type']
        
        try:
            # Get CSV upload and related students
            csv_upload = CSVUpload.objects.get(id=csv_upload_id)
            students = Student.objects.filter(csv_upload=csv_upload)
            
            if not students.exists():
                return Response(
                    {'error': 'No students found for this CSV upload'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Send emails
            email_results = self._send_bulk_emails(
                students=students,
                subject=subject,
                content=content,
                content_type=content_type
            )
            
            # Update CSV upload with email sending results
            self._update_csv_upload_status(csv_upload, email_results)
            
            # Prepare response
            successful_sends = len([r for r in email_results if r['status'] == 'success'])
            total_students = len(email_results)
            
            return Response({
                'message': f'Email sending completed',
                'csv_upload_id': csv_upload_id,
                'total_students': total_students,
                'successful_sends': successful_sends,
                'failed_sends': total_students - successful_sends,
                'results': email_results
            }, status=status.HTTP_200_OK)
            
        except CSVUpload.DoesNotExist:
            return Response(
                {'error': 'CSV Upload not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error sending bulk emails: {str(e)}")
            return Response(
                {'error': 'Internal server error occurred'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _send_bulk_emails(self, students, subject: str, content: str, content_type: str) -> List[Dict]:
        """
        Send emails to all students and return results
        """
        results = []
        from_email = settings.DEFAULT_FROM_EMAIL
        
        for student in students:
            try:
                if content_type == 'html':
                    success = send_mail(
                        subject=subject,
                        message='',  # Plain text version (empty for HTML-only)
                        from_email=from_email,
                        recipient_list=[student.email],
                        html_message=content,
                        fail_silently=False
                    )
                else:
                    success = send_mail(
                        subject=subject,
                        message=content,
                        from_email=from_email,
                        recipient_list=[student.email],
                        fail_silently=False
                    )
                
                results.append({
                    'student_email': student.email,
                    'student_name': student.full_name,
                    'status': 'success' if success else 'failed',
                    'error_message': ''
                })
                
                print(f"Email sent successfully to {student.email}")
                
            except Exception as e:
                error_msg = str(e)
                results.append({
                    'student_email': student.email,
                    'student_name': student.full_name,
                    'status': 'failed',
                    'error_message': error_msg
                })
                print(f"Failed to send email to {student.email}: {error_msg}")
        
        return results
    
    def _update_csv_upload_status(self, csv_upload: CSVUpload, email_results: List[Dict]):
        """
        Update CSV upload with email sending results
        """
        successful_sends = len([r for r in email_results if r['status'] == 'success'])
        failed_sends = len([r for r in email_results if r['status'] == 'failed'])
        
        # Store email results in the errors field for tracking
        email_summary = {
            'email_sent_at': str(timezone.now()),
            'successful_sends': successful_sends,
            'failed_sends': failed_sends,
            'failed_emails': [r for r in email_results if r['status'] == 'failed']
        }
        
        with transaction.atomic():
            csv_upload.errors = csv_upload.errors or {}
            csv_upload.errors['email_results'] = email_summary
            csv_upload.save()

class GetStudentsByCSVUploadView(APIView):
    """
    Get all students for a specific CSV upload (for preview before sending)
    """
    
    def get(self, request, csv_upload_id):
        try:
            csv_upload = CSVUpload.objects.get(id=csv_upload_id)
            students = Student.objects.filter(csv_upload=csv_upload)
            
            student_data = [{
                'id': student.id,
                'email': student.email,
                'full_name': student.full_name,
                'created_at': student.created_at
            } for student in students]
            
            return Response({
                'csv_upload_id': csv_upload_id,
                'csv_upload_info': {
                    'file_name': csv_upload.file_name,
                    'uploaded_by': csv_upload.uploaded_by.username,
                    'uploaded_at': csv_upload.uploaded_at,
                    'total_records': csv_upload.total_records,
                },
                'students': student_data,
                'total_students': len(student_data)
            }, status=status.HTTP_200_OK)
            
        except CSVUpload.DoesNotExist:
            return Response(
                {'error': 'CSV Upload not found'},
                status=status.HTTP_404_NOT_FOUND
            )
            
# class GeneratePresignedURLView(APIView):
#     """
#     API to generate presigned URL for file upload
#     Takes assessment_id and filename, generates presigned URL if combination is unique
#     """
    
#     def post(self, request):
#         serializer = GeneratePresignedURLSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(
#                 {'error': 'Invalid data', 'details': serializer.errors},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         assessment_id = serializer.validated_data['assessment_id']
#         filename = serializer.validated_data['filename']
        
#         try:
#             print("reached 1")
#             assessment = Assessment.objects.get(id=assessment_id)
#             s3_handler = AssessmentS3Handler()
            
#             # Generate presigned URL
#             presigned_url, s3_key = s3_handler.generate_assessment_presigned_url(
#                 assessment_id, filename
#             )
            
#             if not presigned_url:
#                 return Response(
#                     {'error': 'Failed to generate presigned URL'},
#                     status=status.HTTP_500_INTERNAL_SERVER_ERROR
#                 )
            
#             # Calculate expiration time
#             expiration_seconds = int(os.getenv('PRESIGNED_URL_EXPIRATION_TIME', 3600))
#             expires_at = timezone.now() + timedelta(seconds=expiration_seconds)
#             print("reached 2")
            
#             # Create or update AssessmentFile record
#             assessment_file, created = AssessmentFile.objects.get_or_create(
#                 assessment=assessment,
#                 filename=filename,
#                 defaults={
#                     's3_key': s3_key,
#                     'upload_status': 'pending',
#                     'presigned_url': presigned_url,
#                     'presigned_url_expires': expires_at
#                 }
#             )
#             print("reached 3")
            
            
#             if not created:
#                 # Update existing record
#                 print("reached 4")
                
#                 assessment_file.s3_key = s3_key
#                 assessment_file.upload_status = 'pending'
#                 assessment_file.presigned_url = presigned_url
#                 assessment_file.presigned_url_expires = expires_at
#                 assessment_file.file_size = 0  # Reset file size
#                 assessment_file.save()
#                 print("reached 5")
                
            
#             return Response({
#                 'message': 'Presigned URL generated successfully',
#                 'presigned_url': presigned_url,
#                 'expires_at': expires_at,
#                 'expires_in_seconds': expiration_seconds,
#                 'assessment_file_id': assessment_file.id,
#                 's3_path': s3_key,
#                 'upload_instructions': {
#                     'method': 'PUT',
#                     'url': presigned_url,
#                     'headers': {
#                         'Content-Type': 'application/octet-stream'
#                     }
#                 }
#             }, status=status.HTTP_201_CREATED)
            
#         except Assessment.DoesNotExist:
#             return Response(
#                 {'error': 'Assessment not found'},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         except Exception as e:
#             return Response(
#                 {'error': f'Internal server error: {str(e)}'},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

class GeneratePresignedURLView(APIView):
    def post(self, request):
        serializer = GeneratePresignedURLSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid data', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        assessment_id = serializer.validated_data['assessment_id']
        filename = serializer.validated_data['filename']
        
        # Detect content type from filename
        import mimetypes
        content_type, _ = mimetypes.guess_type(filename)
        if not content_type:
            content_type = 'application/octet-stream'
        
        try:
            assessment = Assessment.objects.get(id=assessment_id)
            s3_handler = AssessmentS3Handler()
            
            # Generate presigned URL with proper content type
            presigned_url, s3_key = s3_handler.generate_assessment_presigned_url(
                assessment_id, filename, content_type
            )
            
            if not presigned_url:
                return Response(
                    {'error': 'Failed to generate presigned URL'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Calculate expiration time
            expiration_seconds = int(os.getenv('PRESIGNED_URL_EXPIRATION_TIME', 3600))
            expires_at = timezone.now() + timedelta(seconds=expiration_seconds)
            
            # Create or update AssessmentFile record
            assessment_file, created = AssessmentFile.objects.get_or_create(
                assessment=assessment,
                filename=filename,
                defaults={
                    's3_key': s3_key,
                    'upload_status': 'pending',
                    'presigned_url': presigned_url,
                    'presigned_url_expires': expires_at
                }
            )
            
            if not created:
                # Update existing record
                assessment_file.s3_key = s3_key
                assessment_file.upload_status = 'pending'
                assessment_file.presigned_url = presigned_url
                assessment_file.presigned_url_expires = expires_at
                assessment_file.file_size = 0
                assessment_file.save()
            
            return Response({
                'message': 'Presigned URL generated successfully',
                'presigned_url': presigned_url,
                'expires_at': expires_at,
                'expires_in_seconds': expiration_seconds,
                'assessment_file_id': assessment_file.id,
                's3_path': s3_key,
                'upload_instructions': {
                    'method': 'PUT',
                    'url': presigned_url,
                    'headers': {
                        'Content-Type': content_type  # Use detected content type
                    }
                }
            }, status=status.HTTP_201_CREATED)
            
        except Assessment.DoesNotExist:
            return Response(
                {'error': 'Assessment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Internal server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CheckFileStatusView(APIView):
    """
    API to check if file is uploaded and get file size
    Takes assessment_id and filename, checks S3 and updates database
    """
    
    def get(self, request):
        serializer = CheckFileStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid data', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        assessment_id = serializer.validated_data['assessment_id']
        filename = serializer.validated_data['filename']
        
        try:
            # Get the AssessmentFile record
            try:
                assessment_file = AssessmentFile.objects.get(
                    assessment_id=assessment_id,
                    filename=filename
                )
            except AssessmentFile.DoesNotExist:
                return Response(
                    {'error': 'No upload record found for this assessment and filename combination'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Check if file exists in S3
            s3_handler = AssessmentS3Handler()
            file_size = s3_handler.check_file_exists_and_size(assessment_file.s3_key)
            
            if file_size is not None:
                # File exists, update the record
                assessment_file.file_size = file_size
                assessment_file.upload_status = 'uploaded'
                assessment_file.s3_url = assessment_file.s3_full_url
                assessment_file.save()
                
                return Response({
                    'message': 'File found and record updated',
                    'file_uploaded': True,
                    'file_size_bytes': file_size,
                    'file_size_mb': round(file_size / (1024 * 1024), 2),
                    'file_size_kb': round(file_size / 1024, 2),
                    'assessment_file_id': assessment_file.id,
                    's3_url': assessment_file.s3_url,
                    'upload_status': assessment_file.upload_status,
                    'uploaded_at': assessment_file.updated_at
                }, status=status.HTTP_200_OK)
            else:
                # File doesn't exist
                assessment_file.upload_status = 'pending'
                assessment_file.save()
                
                return Response({
                    'message': 'File not found in S3',
                    'file_uploaded': False,
                    'file_size_bytes': 0,
                    'upload_status': assessment_file.upload_status,
                    'presigned_url_expired': (
                        assessment_file.presigned_url_expires and 
                        timezone.now() > assessment_file.presigned_url_expires
                    ) if assessment_file.presigned_url_expires else None
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response(
                {'error': f'Internal server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ListAssessmentFilesView(APIView):
    """
    API to list all files for an assessment
    """
    
    def get(self, request, assessment_id):
        try:
            assessment = Assessment.objects.get(id=assessment_id)
            files = AssessmentFile.objects.filter(assessment=assessment)
            serializer = AssessmentFileSerializer(files, many=True)
            
            return Response({
                'assessment_id': assessment_id,
                'assessment_title': assessment.title,
                'files': serializer.data,
                'total_files': files.count(),
                'uploaded_files': files.filter(upload_status='uploaded').count(),
                'pending_files': files.filter(upload_status='pending').count()
            }, status=status.HTTP_200_OK)
            
        except Assessment.DoesNotExist:
            return Response(
                {'error': 'Assessment not found'},
                status=status.HTTP_404_NOT_FOUND
            )


s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_LAMBDA_REGION_NAME
)


def decode_test_code_token(token):
    """
    Decode JWT token to extract test code
    """
    try:
        # Decode JWT token (adjust secret key and algorithm as needed)
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload.get('test_code'), None
    except jwt.ExpiredSignatureError:
        return None, "Token has expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"
    except Exception as e:
        return None, f"Token decode error: {str(e)}"

def upload_image_to_s3(image_file, test_code):
    """
    Upload image to S3 bucket
    """
    try:
        # Generate unique filename
        file_extension = image_file.name.split('.')[-1]
        filename = f"test_submissions/{test_code}_{uuid.uuid4().hex}.{file_extension}"
        
        # Upload to S3
        s3_client.upload_fileobj(
            image_file,
            settings.AWS_S3_BUCKET_NAME,
            filename,
            ExtraArgs={
                'ContentType': image_file.content_type,
                'Metadata': {
                    'test_code': test_code,
                    'uploaded_at': datetime.now().isoformat()
                }
            }
        )
        
        # Generate S3 URL
        s3_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{filename}"
        return s3_url, None
        
    except ClientError as e:
        return None, f"S3 upload error: {str(e)}"
    except Exception as e:
        return None, f"Upload error: {str(e)}"

def call_lambda_function(test_code_obj, s3_url):
    """
    Call AWS Lambda function for processing
    """
    try:
        payload = {
            'test_code': test_code_obj.code,
            'student_id': test_code_obj.student.id,
            'student_email': test_code_obj.student.email,
            'assessment_id': test_code_obj.assessment.id,
            's3_url': s3_url,
            'submission_time': timezone.now().isoformat()
        }
        
        response = lambda_client.invoke(
            FunctionName=settings.AWS_LAMBDA_FUNCTION_NAME,
            InvocationType='RequestResponse',  # Synchronous call
            Payload=json.dumps(payload)
        )
        
        # Parse Lambda response
        response_payload = json.loads(response['Payload'].read())
        return response_payload, None
        
    except ClientError as e:
        return None, f"Lambda invocation error: {str(e)}"
    except Exception as e:
        return None, f"Lambda call error: {str(e)}"

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_student_image(request):
    """
    API endpoint to submit test code with image
    """
    serializer = TestCodeSubmissionSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'success': False, 'message': 'Invalid request data', 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    token = serializer.validated_data['token']
    image_file = serializer.validated_data['image']
    
    # Step 1: Decode JWT token to get test code
    test_code, token_error = decode_test_code_token(token)
    if token_error:
        return Response(
            {'success': False, 'message': token_error},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Step 2: Validate test code exists and is active
    try:
        test_code_obj = TestCode.objects.get(code=test_code, is_active=True)
    except TestCode.DoesNotExist:
        return Response(
            {'success': False, 'message': 'Invalid  test code'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Step 3: Upload image to S3
    s3_url, upload_error = upload_image_to_s3(image_file, test_code)
    if upload_error:
        return Response(
            {'success': False, 'message': upload_error},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Step 4: Call Lambda function
    lambda_response, lambda_error = call_lambda_function(test_code_obj, s3_url)
    if lambda_error:
        return Response(
            {'success': False, 'message': lambda_error},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Step 6: Return success response
    response_data = {
        'success': True,
        'message': 'Image Sent Successfully!',
    }
    
 
    return Response(response_data, status=status.HTTP_201_CREATED)
    