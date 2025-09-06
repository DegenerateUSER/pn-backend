from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CSVUploadViewSet
from . import views

router = DefaultRouter()
router.register(r'assessments', views.AssessmentViewSet, basename='assessment')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'students', views.StudentViewSet, basename='student')
router.register(r'students-list', CSVUploadViewSet, basename='get-students-list')

urlpatterns = [
    # Singular assessment endpoints
    path('assessment', views.AssessmentViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='assessment-collection'),
    path('assessment/<int:pk>', views.AssessmentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='assessment-detail'),
    path('register/', views.SignupView.as_view(), name='Register'),
    path('login/', views.LoginView.as_view(), name='Login'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('uploadStudents/', views.StudentCSVUploadView.as_view(), name="upload students"),
    path('assign-assessment/', views.AssignAssessmentToCSVView.as_view(), name='assign-assessment'),
    path('assessments/<int:assessment_id>/test-codes/', views.GetAssessmentTestCodesView.as_view(), name='assessment-test-codes'),
    path('csv-uploads/<int:csv_upload_id>/test-codes/', views.GetCSVUploadTestCodesView.as_view(), name='csv-upload-test-codes'),
    path('sendEmail/', views.SendBulkEmailView.as_view(), name="send bulk emails"),
    path('upload/', views.GeneratePresignedURLView.as_view(), name="generate presigned url"),
    path('fileStatus/', views.CheckFileStatusView.as_view(), name = "check file status"),
    path('files/<int:assessment_id>', views.ListAssessmentFilesView.as_view(), name="get files for an assessment"),
    path('uploadStudentImage/', views.upload_student_image, name="upload student image for processing"), #proctoring module
    path('', include(router.urls)),
    
    #patch assessment work
    #proctoring module (calculating confidence percentage, video call)
    #sample report generation
]