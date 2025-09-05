"""
URL configuration for pna project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api import views

from django.urls import path, include
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r'assessments', views.AssessmentViewSet, basename='assessment')


def home(request):
    return HttpResponse("Django is working!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include("api.urls")),
    path('', home, name='sign_in'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    


]
