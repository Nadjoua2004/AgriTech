import os
import sys
import django
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'auth_service'))
load_dotenv(os.path.join(os.path.dirname(__file__), 'services', 'auth_service', '.env'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

roles = [
    'admin', 'farm_manager', 'supervisor', 'agronomist', 
    'quality_inspector', 'field_worker', 'irrigation_worker', 'equipment_operator'
]

print("Creating/Updating test users for all roles...")

for role_name in roles:
    username = f"test_{role_name}"
    email = f"{username}@agritech.com"
    password = "password123"
    
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    user.set_password(password)
    user.role = role_name
    if role_name == 'admin':
        user.is_staff = True
        user.is_superuser = True
    user.save()
    
    status = "Created" if created else "Updated"
    print(f"- {status} {username} (Role: {role_name})")

print("\nAll test users are ready! Password for all: password123")
