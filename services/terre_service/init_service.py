#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'terre_service.settings')

# Configure Django
django.setup()

print("🚀 Initializing Terre Service...")

# Run migrations
try:
    print("📋 Running migrations...")
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    print("✅ Migrations completed")
except Exception as e:
    print(f"❌ Migration error: {e}")

# Add sample data
try:
    print("🌱 Adding sample parcelles...")
    execute_from_command_line(['manage.py', 'add_sample_parcelles'])
    print("✅ Sample data added")
except Exception as e:
    print(f"❌ Sample data error: {e}")

# Test the service
try:
    from lands.models import Parcelle
    count = Parcelle.objects.count()
    print(f"📊 Total parcelles: {count}")
    
    # Test API endpoint
    from lands.views import ParcelleViewSet
    print("✅ Views loaded successfully")
    
except Exception as e:
    print(f"❌ Service test error: {e}")

print("🎉 Terre Service initialization completed!")
