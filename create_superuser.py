#!/usr/bin/env python
import os
import django
import sys

# Add the project root to Python path
sys.path.append('/Users/tusharteotia/Downloads/tushar_server-main 2')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pna.settings')
django.setup()

from api.models import User

def create_superuser():
    email = 'admin@example.com'
    password = 'admin'
    
    # Check if user already exists
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        print(f'User already exists! Email: {user.email}, Role: {user.role}, Is Staff: {user.is_staff}, Is Superuser: {user.is_superuser}')
        return user
    
    # Create superuser manually
    user = User(
        email=email,
        role='admin',
        is_staff=True,
        is_superuser=True,
        is_active=True
    )
    user.set_password(password)
    user.save()
    
    print(f'Superuser created successfully! Email: {email}, Role: admin')
    return user

if __name__ == '__main__':
    create_superuser()
