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

try:
    admin, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@agritech.com'})
    admin.set_password('admin123')
    admin.role = 'admin'
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    if created:
        print("Created new admin user: admin / admin123")
    else:
        print("Updated existing admin user password to: admin123")
except Exception as e:
    print(f"Error: {e}")
