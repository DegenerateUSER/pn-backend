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
import requests as req
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
        """Create a new assessment"""
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
        """Get all assessments or a specific assessment by ID"""
        try:
            assessment_id = request.query_params.get('id')
            
            if assessment_id:
                # Get specific assessment
                assessment = get_object_or_404(SampleJSON, id=assessment_id)
                return Response({
                    "id": assessment.id,
                    "data": assessment.data
                }, status=status.HTTP_200_OK)
            else:
                # Get all assessments
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
        """Update an existing assessment"""
        try:
            assessment_id = request.query_params.get('id')
            if not assessment_id:
                return Response({"error": "Assessment ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            assessment = get_object_or_404(SampleJSON, id=assessment_id)
            data = json.loads(request.body)
            
            # Update the assessment data
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
        """Partially update an existing assessment"""
        try:
            assessment_id = request.query_params.get('id')
            if not assessment_id:
                return Response({"error": "Assessment ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            assessment = get_object_or_404(SampleJSON, id=assessment_id)
            data = json.loads(request.body)
            
            # Merge with existing data for partial update
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
        """Delete an assessment"""
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
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Pass set_number from query params to serializer so nested questions can be filtered
        context['set_number'] = self.request.query_params.get('set_number')
        return context

    def get_queryset(self):
        """Filter assessments by the current user with optional filters"""
        queryset = Assessment.objects.filter(created_by=self.request.user)
        
        # Optional query parameters for filtering
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
        """Create a new assessment"""
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
        """Retrieve a specific assessment"""
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
        """Update an assessment"""
        try:
            partial = kwargs.pop('partial', False)
            assessment = self.get_object()
            
            # Check if assessment is already published and restrict certain updates
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
        """Delete an assessment"""
        try:
            assessment = self.get_object()
            
            # Check if assessment can be deleted (e.g., not if it has submissions)
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
        """Publish an assessment"""
        try:
            assessment = self.get_object()
            
            # Validation before publishing
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
        """Unpublish an assessment"""
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
        """Create a copy of an assessment"""
        try:
            original_assessment = self.get_object()
            
            with transaction.atomic():
                # Create new assessment
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
                
                # Copy sections and questions
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
        """Get assessment statistics for the current user"""
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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def all_assessments(self, request):
        """Admin endpoint to view all assessments (for debugging/admin purposes)"""
        # Check if user is admin or has appropriate role
        if not request.user.role in ['admin', 'assessment_manager']:
            return Response(
                {'error': 'Permission denied. Admin access required.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            # Get ALL assessments regardless of creator
            all_assessments = Assessment.objects.all().select_related('created_by')
            
            # Apply optional filters
            assessment_type = request.query_params.get('type', None)
            is_published = request.query_params.get('is_published', None)
            search = request.query_params.get('search', None)
            
            if assessment_type:
                all_assessments = all_assessments.filter(assessment_type=assessment_type)
            if is_published is not None:
                all_assessments = all_assessments.filter(is_published=is_published.lower() == 'true')
            if search:
                all_assessments = all_assessments.filter(title__icontains=search)
            
            # Paginate results
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(all_assessments, request)
            
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return paginator.get_paginated_response({
                    'message': 'All assessments retrieved successfully',
                    'total_count': all_assessments.count(),
                    'data': serializer.data
                })
            
            serializer = self.get_serializer(all_assessments, many=True)
            return Response({
                'message': 'All assessments retrieved successfully',
                'total_count': all_assessments.count(),
                'data': serializer.data
            })
            
        except Exception as e:
            return Response(
                {
                    'error': 'Failed to retrieve assessments',
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

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]



class CSVUploadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing CSV uploads.
    GET /api/students-list/ - List all uploads
    GET /api/students-list/{id}/ - Get specific upload
    DELETE /api/students-list/{id}/ - Delete specific upload
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
    
class GenerateStudentReportView(APIView):
    """
    Generate a comprehensive student report for an assessment attempt and
    optionally analyze weaknesses using Gemini (if GEMINI_API_KEY is set).
    Supports both User and Student-based reports.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if this is the new enhanced format or legacy format
        if 'sections' in request.data:
            # NEW: Enhanced format with actual performance data
            return self._handle_enhanced_request(request)
        else:
            # LEGACY: Simple format for backward compatibility
            return self._handle_legacy_request(request)
    
    def _handle_enhanced_request(self, request):
        """Handle new enhanced request with actual performance data"""
        serializer = GenerateStudentReportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'error': 'Invalid data provided',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        
        try:
            # Get assessment
            assessment = Assessment.objects.select_related().get(id=data['assessment_id'])
            
            # Get student or user
            student = None
            candidate = None
            
            if data.get('student_email'):
                student = Student.objects.get(email=data['student_email'])
                participant_type = 'student'
            else:
                candidate = User.objects.get(email=data['candidate_email'])
                participant_type = 'user'
            
            # Calculate report metrics from real data
            report_data = self._calculate_report_metrics(data, assessment)
            
            # Create report record
            report = self._create_report_record(
                assessment, student, candidate, data, report_data
            )
            
            # Generate comprehensive response
            response_data = self._generate_enhanced_response(
                report, assessment, student, candidate, report_data, data
            )
            
            return Response({
                'message': 'Student report generated successfully',
                'report_id': report.id,
                'participant_type': participant_type,
                **response_data
            }, status=status.HTTP_201_CREATED)
            
        except Assessment.DoesNotExist:
            return Response({
                'error': 'Assessment not found',
                'assessment_id': data['assessment_id']
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Student.DoesNotExist:
            return Response({
                'error': 'Student not found',
                'email': data.get('student_email')
            }, status=status.HTTP_404_NOT_FOUND)
            
        except User.DoesNotExist:
            return Response({
                'error': 'User not found',
                'email': data.get('candidate_email')
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                'error': 'Failed to generate report',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _handle_legacy_request(self, request):
        """Handle legacy request format for backward compatibility"""
        req = GenerateStudentReportRequestSerializer(data=request.data)
        if not req.is_valid():
            return Response({'error': 'Invalid data', 'details': req.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = req.validated_data

        # Resolve report
        report = None
        try:
            if data.get('report_id'):
                report = Report.objects.select_related('assessment', 'candidate', 'student').get(id=data['report_id'])
            else:
                assessment = Assessment.objects.get(id=data['assessment_id'])
                
                # Handle Student-based reports (NEW)
                if data.get('student_email'):
                    student = Student.objects.get(email=data['student_email'])
                    report = Report.objects.select_related('assessment', 'student').filter(
                        assessment=assessment, student=student
                    ).order_by('-submitted_at', '-ended_at', '-started_at').first()
                    
                    # If no report exists, create a mock report for demonstration
                    if not report:
                        report = self._create_mock_student_report(assessment, student)
                        
                # Handle User-based reports (EXISTING)
                else:
                    candidate = None
                    if data.get('candidate_id'):
                        candidate = User.objects.get(id=data['candidate_id'])
                    elif data.get('candidate_email'):
                        candidate = User.objects.get(email=data['candidate_email'])
                    report = Report.objects.select_related('assessment', 'candidate').filter(
                        assessment=assessment, candidate=candidate
                    ).order_by('-submitted_at', '-ended_at', '-started_at').first()
                    
                if not report:
                    return Response({'error': 'Report not found for candidate and assessment'}, status=status.HTTP_404_NOT_FOUND)
                    
        except (Report.DoesNotExist, Assessment.DoesNotExist, User.DoesNotExist, Student.DoesNotExist):
            return Response({'error': 'Specified entities not found'}, status=status.HTTP_404_NOT_FOUND)

        # Load attempts with question context
        attempts = list(QuestionAttempt.objects.filter(report=report).select_related('question', 'question__section'))
        assessment = report.assessment

        total_marks_assessment = assessment.total_marks or 0
        obtained_marks_report = report.obtained_marks if report.obtained_marks is not None else None
        obtained_marks = obtained_marks_report if obtained_marks_report is not None else sum((a.marks_obtained or 0) for a in attempts)

        # Compute negative penalties and questions left
        negative_scored = sum(
            -(a.marks_obtained or 0)
            for a in attempts
            if bool(a.is_attempted) and not bool(a.is_correct) and (a.marks_obtained or 0) < 0
        )
        questions_left = sum(1 for a in attempts if not bool(a.is_attempted))

        # Per-section breakdown
        sections = list(assessment.sections.all())
        section_stats = {s.id: {
            'section_id': s.id,
            'section_name': s.name,
            'total_questions': 0,
            'attempted': 0,
            'correct': 0,
            'wrong': 0,
            'marks_obtained': 0,
            'total_marks': s.total_marks,
        } for s in sections}

        # Type breakdown
        type_stats = {
            'coding': {'attempted': 0, 'correct': 0, 'wrong': 0, 'marks_obtained': 0},
            'non-coding': {'attempted': 0, 'correct': 0, 'wrong': 0, 'marks_obtained': 0}
        }

        # Question details and topic breakdown
        question_details = []
        topics_correct = {}
        topics_negative = {}
        topics_left = {}

        for a in attempts:
            q = a.question
            if not q:
                continue
            sec = q.section
            if sec and sec.id in section_stats:
                section_stats[sec.id]['total_questions'] += 1
                if a.is_attempted:
                    section_stats[sec.id]['attempted'] += 1
                if a.is_correct:
                    section_stats[sec.id]['correct'] += 1
                else:
                    if a.is_attempted:
                        section_stats[sec.id]['wrong'] += 1
                section_stats[sec.id]['marks_obtained'] += (a.marks_obtained or 0)

            # Topic aggregation keyed by section name
            section_name = sec.name if sec else 'Unknown'
            if bool(a.is_attempted) and bool(a.is_correct):
                topics_correct.setdefault(section_name, []).append(q.id)
            elif bool(a.is_attempted) and not bool(a.is_correct):
                topics_negative.setdefault(section_name, []).append(q.id)
            elif not bool(a.is_attempted):
                topics_left.setdefault(section_name, []).append(q.id)

            qtype = (q.question_type or 'non-coding')
            if qtype in type_stats:
                if a.is_attempted:
                    type_stats[qtype]['attempted'] += 1
                if a.is_correct:
                    type_stats[qtype]['correct'] += 1
                else:
                    if a.is_attempted:
                        type_stats[qtype]['wrong'] += 1
                type_stats[qtype]['marks_obtained'] += (a.marks_obtained or 0)

            question_details.append({
                'question_id': q.id,
                'section_id': sec.id if sec else None,
                'section_name': sec.name if sec else None,
                'question_order': q.question_order,
                'question_type': qtype,
                'is_attempted': bool(a.is_attempted),
                'is_correct': bool(a.is_correct),
                'marks_obtained': a.marks_obtained or 0,
                'time_taken': a.time_taken,
            })

        # Compute overall
        percentage = round((obtained_marks / total_marks_assessment) * 100, 2) if total_marks_assessment else 0

        # Identify weakest areas (preliminary local heuristic)
        weakest_sections = sorted(section_stats.values(), key=lambda s: (s['correct'] / s['attempted']) if s['attempted'] else 0)
        weakest_types = sorted([
            {'type': t, **stats} for t, stats in type_stats.items()
        ], key=lambda t: (t['correct'] / t['attempted']) if t['attempted'] else 0)

        summary = {
            'report_id': report.id,
            'candidate': {
                'id': report.candidate.id if report.candidate else report.student.id,
                'email': report.candidate.email if report.candidate else report.student.email,
                'name': getattr(report.candidate, 'full_name', None) if report.candidate else report.student.full_name,
                'type': 'user' if report.candidate else 'student'
            },
            'assessment': {
                'id': assessment.id,
                'title': assessment.title,
                'type': assessment.assessment_type,
                'total_marks': total_marks_assessment,
            },
            'score': {
                'marks_scored': obtained_marks,
                'total_marks': total_marks_assessment,
                'percentage': percentage,
                'negative_scored': negative_scored,
                'questions_left': questions_left,
            },
            'by_section': list(section_stats.values()),
            'by_type': type_stats,
            'questions': question_details,
            'topics_breakdown': {
                'correct_by_topic': topics_correct,
                'negative_by_topic': topics_negative,
                'left_by_topic': topics_left,
            }
        }

        # Optional Gemini analysis
        analysis = None
        try:
            import os
            api_key = os.environ.get('GEMINI_API_KEY')
            if api_key:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = (
                        "You are an education analyst. Given this JSON with a student's assessment performance and topics breakdown, "
                        "identify the student's weak topics and explain why. Use both accuracy and negative scoring signals. "
                        "Provide: weak_topics (array of {topic, reason}), quick_tips (5 concise bullet tips), and study_plan (3-5 steps). "
                        "Respond in JSON only with keys: weak_topics, quick_tips, study_plan.\n\n"
                        f"DATA: {json.dumps(summary)}"
                    )
                    res = model.generate_content(prompt)
                    # Some SDKs return text; ensure we parse JSON if present
                    import json as _json
                    text = getattr(res, 'text', None) or (res.candidates[0].content.parts[0].text if getattr(res, 'candidates', None) else None)
                    if text:
                        # Attempt to extract JSON portion
                        try:
                            analysis = _json.loads(text)
                        except Exception:
                            # Fallback: find first JSON-like block
                            import re
                            m = re.search(r"\{[\s\S]*\}", text)
                            if m:
                                analysis = _json.loads(m.group(0))
                except Exception as e:
                    analysis = {'error': 'gemini_analysis_failed', 'details': str(e)}
        except Exception:
            analysis = None

        response = {
            'message': 'Student report generated successfully',
            'summary': summary,
            'analysis': analysis or {'info': 'Set GEMINI_API_KEY to enable AI analysis'}
        }

        return Response(response, status=status.HTTP_200_OK)
    
    def _create_mock_student_report(self, assessment, student):
        """Create a mock report for demonstration when no actual report exists for a student"""
        from django.utils import timezone
        
        # Create a mock report for the student
        report = Report.objects.create(
            assessment=assessment,
            student=student,
            started_at=timezone.now(),
            ended_at=timezone.now(),
            submitted_at=timezone.now(),
            obtained_marks=0,
            status='completed'
        )
        
        return report

    def _calculate_report_metrics(self, data, assessment):
        """Calculate comprehensive metrics from actual performance data"""
        sections_data = data['sections']
        total_marks = 0
        total_obtained = 0
        total_questions = 0
        total_attempted = 0
        total_correct = 0
        total_wrong = 0
        total_time_spent = 0
        
        section_stats = []
        question_details = []
        
        # Create a mapping of section IDs to section names from the assessment
        section_name_map = {section.id: section.name for section in assessment.sections.all()}
        
        for section_data in sections_data:
            section_id = section_data['section_id']
            section_name = section_name_map.get(section_id, f"Section {section_id}")
            
            section_marks = 0
            section_obtained = 0
            section_questions = len(section_data['questions'])
            section_attempted = 0
            section_correct = 0
            section_wrong = 0
            section_time = section_data.get('time_spent', 0)
            
            for question_data in section_data['questions']:
                # Get marks from request (now required)
                question_marks = question_data.get('total_marks', 0)
                obtained_marks = question_data.get('marks_obtained', 0)
                is_attempted = question_data.get('is_attempted', False)
                is_correct = question_data.get('is_correct', False)
                time_spent = question_data.get('time_spent', 0)
                
                section_marks += question_marks
                section_obtained += obtained_marks
                
                if is_attempted:
                    section_attempted += 1
                    if is_correct:
                        section_correct += 1
                    else:
                        section_wrong += 1
                
                # Store question details
                question_details.append({
                    'question_id': question_data.get('question_id'),
                    'section_id': section_id,
                    'section_name': section_name,
                    'set_number': section_data.get('set_number', 1),
                    'question_text': question_data.get('question_text', ''),
                    'total_marks': question_marks,
                    'marks_obtained': obtained_marks,
                    'is_attempted': is_attempted,
                    'is_correct': is_correct,
                    'time_spent_seconds': time_spent,
                    'selected_option': question_data.get('selected_option'),
                    'correct_option': question_data.get('correct_option')
                })
            
            total_marks += section_marks
            total_obtained += section_obtained
            total_questions += section_questions
            total_attempted += section_attempted
            total_correct += section_correct
            total_wrong += section_wrong
            total_time_spent += section_time
            
            # Store section stats
            section_stats.append({
                'section_id': section_id,
                'section_name': section_name,
                'set_number': section_data.get('set_number', 1),
                'total_questions': section_questions,
                'attempted': section_attempted,
                'correct': section_correct,
                'wrong': section_wrong,
                'marks_obtained': section_obtained,
                'total_marks': section_marks,
                'time_spent_seconds': section_time,
                'accuracy': round((section_correct / section_attempted * 100), 2) if section_attempted > 0 else 0
            })
        
        # Calculate overall metrics
        percentage = round((total_obtained / total_marks * 100), 2) if total_marks > 0 else 0
        accuracy = round((total_correct / total_attempted * 100), 2) if total_attempted > 0 else 0
        questions_left = total_questions - total_attempted
        
        return {
            'total_marks': total_marks,
            'total_obtained': total_obtained,
            'percentage': percentage,
            'total_questions': total_questions,
            'total_attempted': total_attempted,
            'total_correct': total_correct,
            'total_wrong': total_wrong,
            'questions_left': questions_left,
            'accuracy': accuracy,
            'total_time_spent': total_time_spent,
            'section_stats': section_stats,
            'question_details': question_details
        }

    def _create_report_record(self, assessment, student, candidate, request_data, report_data):
        """Create a new report record in the database"""
        from django.utils import timezone
        import uuid
        
        # Generate a unique ID for the report
        report_id = str(uuid.uuid4())
        
        report = Report.objects.create(
            id=report_id,
            assessment=assessment,
            student=student,
            candidate=candidate,
            started_at=request_data.get('started_at'),
            ended_at=request_data.get('ended_at'),
            submitted_at=request_data.get('submitted_at'),
            total_marks=report_data['total_marks'],
            obtained_marks=report_data['total_obtained'],
            percentage=report_data['percentage'],
            percentile=0.0,  # Default value, can be calculated later if needed
            status='completed'
        )
        
        return report

    def _generate_enhanced_response(self, report, assessment, student, candidate, report_data, request_data):
        """Generate comprehensive response with all metrics and analysis"""
        participant_info = {
            'id': student.id if student else candidate.id,
            'email': student.email if student else candidate.email,
            'name': student.full_name if student else getattr(candidate, 'full_name', candidate.email),
            'type': 'student' if student else 'user'
        }
        
        # Enhanced performance analysis
        performance_analysis = self._analyze_performance(report_data)
        
        # Time analysis
        time_analysis = self._analyze_time_management(report_data, assessment)
        
        # Generate Gemini AI tips for the student
        ai_tips = self._generate_ai_tips(report_data, assessment, participant_info)
        
        return {
            'summary': {
                'total_marks': report_data['total_marks'],
                'marks_obtained': report_data['total_obtained'],
                'percentage': report_data['percentage'],
                'accuracy': report_data['accuracy'],
                'total_questions': report_data['total_questions'],
                'attempted': report_data['total_attempted'],
                'correct': report_data['total_correct'],
                'wrong': report_data['total_wrong'],
                'not_attempted': report_data['questions_left'],
                'total_time_spent_seconds': report_data['total_time_spent']
            },
            'participant': participant_info,
            'assessment': {
                'id': assessment.id,
                'title': assessment.title,
                'description': assessment.description,
                'total_marks': assessment.total_marks,
                'duration': assessment.duration
            },
            'sections': report_data['section_stats'],
            'questions': report_data['question_details'],
            'performance_analysis': performance_analysis,
            'time_analysis': time_analysis,
            'recommendations': self._generate_recommendations(report_data),
            'ai_tips': ai_tips  # New: Gemini AI-powered tips
        }

    def _analyze_performance(self, report_data):
        """Analyze performance patterns and provide insights"""
        analysis = {
            'grade': self._calculate_grade(report_data['percentage']),
            'performance_level': self._get_performance_level(report_data['percentage']),
            'strength_areas': [],
            'improvement_areas': [],
            'consistency': self._calculate_consistency(report_data['section_stats'])
        }
        
        # Identify strong and weak sections
        for section in report_data['section_stats']:
            if section['accuracy'] >= 80:
                analysis['strength_areas'].append({
                    'section': section['section_name'],
                    'accuracy': section['accuracy'],
                    'score': f"{section['marks_obtained']}/{section['total_marks']}"
                })
            elif section['accuracy'] < 50 and section['attempted'] > 0:
                analysis['improvement_areas'].append({
                    'section': section['section_name'],
                    'accuracy': section['accuracy'],
                    'score': f"{section['marks_obtained']}/{section['total_marks']}"
                })
        
        return analysis

    def _analyze_time_management(self, report_data, assessment):
        """Analyze time management patterns"""
        total_time_available = assessment.duration * 60  # Convert to seconds
        time_used = report_data['total_time_spent']
        time_efficiency = (time_used / total_time_available * 100) if total_time_available > 0 else 0
        
        return {
            'time_used_seconds': time_used,
            'time_available_seconds': total_time_available,
            'time_efficiency_percentage': round(time_efficiency, 2),
            'average_time_per_question': round(time_used / report_data['total_attempted'], 2) if report_data['total_attempted'] > 0 else 0,
            'time_management_rating': self._get_time_management_rating(time_efficiency)
        }

    def _calculate_grade(self, percentage):
        """Calculate letter grade based on percentage"""
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B+'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'

    def _get_performance_level(self, percentage):
        """Get performance level description"""
        if percentage >= 85:
            return 'Excellent'
        elif percentage >= 70:
            return 'Good'
        elif percentage >= 55:
            return 'Average'
        elif percentage >= 40:
            return 'Below Average'
        else:
            return 'Poor'

    def _calculate_consistency(self, section_stats):
        """Calculate performance consistency across sections"""
        if not section_stats:
            return 0
        
        accuracies = [s['accuracy'] for s in section_stats if s['attempted'] > 0]
        if not accuracies:
            return 0
        
        avg_accuracy = sum(accuracies) / len(accuracies)
        variance = sum((acc - avg_accuracy) ** 2 for acc in accuracies) / len(accuracies)
        consistency_score = max(0, 100 - variance)  # Higher score = more consistent
        
        return round(consistency_score, 2)

    def _get_time_management_rating(self, time_efficiency):
        """Rate time management efficiency"""
        if time_efficiency <= 70:
            return 'Excellent - Efficient use of time'
        elif time_efficiency <= 85:
            return 'Good - Well managed'
        elif time_efficiency <= 95:
            return 'Average - Could be more efficient'
        else:
            return 'Poor - Time management needs improvement'

    def _generate_recommendations(self, report_data):
        """Generate personalized recommendations based on performance"""
        recommendations = []
        
        # Accuracy-based recommendations
        if report_data['accuracy'] < 60:
            recommendations.append("Focus on understanding concepts better before attempting questions")
        
        # Attempt rate recommendations
        attempt_rate = (report_data['total_attempted'] / report_data['total_questions']) * 100
        if attempt_rate < 80:
            recommendations.append("Try to attempt more questions to maximize your score potential")
        
        # Section-specific recommendations
        weak_sections = [s for s in report_data['section_stats'] if s['accuracy'] < 50 and s['attempted'] > 0]
        if weak_sections:
            section_names = ', '.join([s['section_name'] for s in weak_sections])
            recommendations.append(f"Review and practice more in: {section_names}")
        
        # Time management recommendations
        avg_time_per_question = report_data['total_time_spent'] / report_data['total_attempted'] if report_data['total_attempted'] > 0 else 0
        if avg_time_per_question > 120:  # More than 2 minutes per question
            recommendations.append("Work on improving your speed while maintaining accuracy")
        
        return recommendations

    def _generate_ai_tips(self, report_data, assessment, participant_info):
        """Generate personalized AI-powered tips using Gemini"""
        try:
            import google.generativeai as genai
            from django.conf import settings
            
            # Configure Gemini
            api_key = getattr(settings, 'GEMINI_API_KEY', None)
            if not api_key:
                return {
                    'available': False,
                    'message': 'AI tips not available - API key not configured',
                    'tips': []
                }
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Prepare performance summary for AI analysis
            performance_summary = {
                'percentage': report_data['percentage'],
                'accuracy': report_data['accuracy'],
                'total_questions': report_data['total_questions'],
                'attempted': report_data['total_attempted'],
                'correct': report_data['total_correct'],
                'wrong': report_data['total_wrong'],
                'sections': [{
                    'name': section['section_name'],
                    'accuracy': section['accuracy'],
                    'attempted': section['attempted'],
                    'total_questions': section['total_questions']
                } for section in report_data['section_stats']]
            }
            
            # Create prompt for Gemini
            prompt = f"""
            You are an educational AI assistant helping a student improve their performance. 
            
            Student Details:
            - Name: {participant_info['name']}
            - Assessment: {assessment.title}
            
            Performance Summary:
            - Overall Score: {report_data['percentage']:.1f}%
            - Accuracy: {report_data['accuracy']:.1f}%
            - Questions Attempted: {report_data['total_attempted']}/{report_data['total_questions']}
            - Correct Answers: {report_data['total_correct']}
            - Wrong Answers: {report_data['total_wrong']}
            
            Section-wise Performance:
            {chr(10).join([f"- {section['section_name']}: {section['accuracy']:.1f}% accuracy ({section['attempted']}/{section['total_questions']} attempted)" for section in report_data['section_stats']])}
            
            Based on this performance data, provide:
            1. 3-5 specific, actionable study tips
            2. Areas of strength to maintain
            3. Areas needing improvement with concrete steps
            4. Motivational message based on their performance level
            
            Keep the response encouraging, specific, and practical. Format as a JSON with keys: strengths, improvements, study_tips, motivation
            """
            
            response = model.generate_content(prompt)
            
            # Try to parse JSON response, fallback to structured text
            try:
                import json
                ai_response = json.loads(response.text)
            except:
                # Fallback: structure the response manually
                ai_response = {
                    'strengths': ['Completed the assessment'],
                    'improvements': ['Continue practicing'],
                    'study_tips': [response.text[:500] + '...' if len(response.text) > 500 else response.text],
                    'motivation': 'Keep working hard and you will improve!'
                }
            
            return {
                'available': True,
                'generated_by': 'Gemini AI',
                'tips': ai_response
            }
            
        except Exception as e:
            return {
                'available': False,
                'error': f'Failed to generate AI tips: {str(e)}',
                'tips': {
                    'study_tips': ['Review your incorrect answers', 'Practice more questions in weak areas'],
                    'motivation': 'Every mistake is a learning opportunity!'
                }
            }
        
class RunCodeView(APIView):
    """
    API endpoint to execute code using JDoodle API
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Validate input data using serializer
        serializer = RunCodeSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get validated data
        validated_data = serializer.validated_data
        
        # Get JDoodle credentials from environment variables
        # (Already validated in serializer)
        client_id = os.getenv('JDOODLE_CLIENT_ID')
        client_secret = os.getenv('JDOODLE_SECRET_KEY')
        
        # Prepare payload for JDoodle API
        payload = {
            "clientId": client_id,
            "clientSecret": client_secret,
            "script": validated_data['script'],
            "stdin": validated_data.get('stdin', ''),
            "language": validated_data['language'],
            "versionIndex": validated_data['versionIndex'],
            "compileOnly": False
        }
        
        try:
            # Make request to JDoodle API
            response = req.post(
                "https://api.jdoodle.com/v1/execute",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30  # 30 second timeout
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Get response data
            jdoodle_response = response.json()
            
            # Remove unwanted fields from response
            filtered_response = {
                key: value for key, value in jdoodle_response.items() 
                if key not in ['projectKey', 'isCompiled']
            }
            
            return Response(filtered_response, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(e)
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class SubmitCodeView(APIView):
    """
    API endpoint to submit code and validate against test cases
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Get query parameter for test type
        test_type = request.query_params.get('type', 'example').lower()
        
        if test_type not in ['example', 'all']:
            return Response(
                {'error': 'Invalid test type. Use "example" or "all"'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate input data using serializer
        serializer = SubmitCodeSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validated_data = serializer.validated_data
        question_id = validated_data['question_id']
        
        # Get the question object
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response(
                {'error': f'Question with ID {question_id} not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if it's a coding question (already validated in serializer, but double-check)
        if question.question_type != 'coding':
            return Response(
                {'error': 'This question is not a coding question'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get test cases from question
        test_cases_data = question.test_cases
        
        if not test_cases_data:
            return Response(
                {'error': 'No test cases found for this question'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Select test cases based on query parameter
        if test_type == 'example':
            test_cases = test_cases_data.get('examples', [])
        else:  # test_type == 'all'
            test_cases = test_cases_data.get('hidden', [])
        
        if not test_cases:
            return Response(
                {'error': f'No {test_type} test cases found for this question'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Execute code against test cases
        result = self.run_test_cases(validated_data, test_cases)
        
        return Response(result, status=status.HTTP_200_OK)
    
    def run_test_cases(self, validated_data, test_cases):
        """
        Run the submitted code against test cases
        """
        # Get JDoodle credentials
        client_id = os.getenv('JDOODLE_CLIENT_ID')
        client_secret = os.getenv('JDOODLE_SECRET_KEY')
        
        passed_count = 0
        failed_count = 0
        test_results = []
        
        for i, test_case in enumerate(test_cases):
            input_data = test_case.get('input', '')
            expected_output = test_case.get('output', '').strip()
            
            # Prepare payload for JDoodle API
            payload = {
                "clientId": client_id,
                "clientSecret": client_secret,
                "script": validated_data['script'],
                "stdin": input_data,
                "language": validated_data['language'],
                "versionIndex": validated_data['versionIndex'],
                "compileOnly": False
            }
            
            try:
                # Make request to JDoodle API
                response = req.post(
                    "https://api.jdoodle.com/v1/execute",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                response.raise_for_status()
                jdoodle_response = response.json()
                
                # Check if execution was successful
                if not jdoodle_response.get('isExecutionSuccess', False):
                    failed_count += 1
                    test_results.append({
                        'test_case_number': i + 1,
                        'input': input_data,
                        'expected_output': expected_output,
                        'actual_output': None,
                        'passed': False,
                        'error': jdoodle_response.get('error', 'Execution failed'),
                        'execution_time': jdoodle_response.get('cpuTime', 'N/A'),
                        'memory_used': jdoodle_response.get('memory', 'N/A')
                    })
                    continue
                
                # Get actual output and clean it
                actual_output = jdoodle_response.get('output', '').strip()
                
                # Compare outputs
                is_passed = actual_output == expected_output
                
                if is_passed:
                    passed_count += 1
                else:
                    failed_count += 1
                
                test_results.append({
                    'test_case_number': i + 1,
                    'input': input_data,
                    'expected_output': expected_output,
                    'actual_output': actual_output,
                    'passed': is_passed,
                    'error': jdoodle_response.get('error'),
                    'execution_time': jdoodle_response.get('cpuTime', 'N/A'),
                    'memory_used': jdoodle_response.get('memory', 'N/A')
                })
                
            except requests.exceptions.Timeout:
                failed_count += 1
                test_results.append({
                    'test_case_number': i + 1,
                    'input': input_data,
                    'expected_output': expected_output,
                    'actual_output': None,
                    'passed': False,
                    'error': 'Execution timeout',
                    'execution_time': 'Timeout',
                    'memory_used': 'N/A'
                })
                
            except Exception as e:
                failed_count += 1
                test_results.append({
                    'test_case_number': i + 1,
                    'input': input_data,
                    'expected_output': expected_output,
                    'actual_output': None,
                    'passed': False,
                    'error': f'API Error: {str(e)}',
                    'execution_time': 'N/A',
                    'memory_used': 'N/A'
                })
        
        return {
            'total_test_cases': len(test_cases),
            'passed_count': passed_count,
            'failed_count': failed_count,
            'success_rate': f"{(passed_count / len(test_cases)) * 100:.1f}%",
            'overall_result': 'PASSED' if failed_count == 0 else 'FAILED',
            'test_results': test_results
        }


class ProctoringResultsView(APIView):
    """
    API endpoint to get all proctoring results or filter them
    """
    permission_classes = [AllowAny]  # You may want to change this to IsAuthenticated
    
    def get(self, request):
        try:
            from .utils import ProctoringDynamoDBHandler
            
            handler = ProctoringDynamoDBHandler()
            
            # Get query parameters for filtering
            filter_params = {}
            
            session_id = request.query_params.get('session_id')
            risk_score = request.query_params.get('risk_score')
            min_risk_score = request.query_params.get('min_risk_score')
            max_risk_score = request.query_params.get('max_risk_score')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            has_flags = request.query_params.get('has_flags')
            
            if session_id:
                filter_params['session_id'] = session_id
            if risk_score:
                filter_params['risk_score'] = int(risk_score)
            if min_risk_score:
                filter_params['min_risk_score'] = int(min_risk_score)
            if max_risk_score:
                filter_params['max_risk_score'] = int(max_risk_score)
            if start_date:
                filter_params['start_date'] = start_date
            if end_date:
                filter_params['end_date'] = end_date
            if has_flags and has_flags.lower() == 'true':
                filter_params['has_flags'] = True
            
            # Query results based on filters
            if filter_params:
                result = handler.query_proctoring_results_by_filter(filter_params)
            else:
                result = handler.get_all_proctoring_results()
            
            if result['success']:
                return Response({
                    'success': True,
                    'data': result['data'],
                    'count': result['count']
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': result['error']
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProctoringResultDetailView(APIView):
    """
    API endpoint to get a specific proctoring result by session ID
    """
    permission_classes = [AllowAny]  # You may want to change this to IsAuthenticated
    
    def get(self, request, session_id):
        try:
            from .utils import ProctoringDynamoDBHandler
            
            handler = ProctoringDynamoDBHandler()
            result = handler.get_proctoring_result_by_session_id(session_id)
            
            if result['success']:
                return Response({
                    'success': True,
                    'data': result['data']
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': result['error']
                }, status=status.HTTP_404_NOT_FOUND if 'not found' in result['error'].lower() else status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)