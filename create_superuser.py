import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pna.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Delete existing superuser if exists
User.objects.filter(email='admin@example.com').delete()

# Create new superuser - this model uses email as USERNAME_FIELD
user = User(
    email='admin@example.com',
    first_name='Admin',
    last_name='User',
    is_staff=True,
    is_superuser=True,
    is_active=True,
    role='admin'
)
user.set_password('admin')
user.save()

print(f"Superuser created successfully: {user.email}")
print(f"Email: admin@example.com")
print(f"Password: admin")
print(f"Admin URL: http://127.0.0.1:8000/admin/")
