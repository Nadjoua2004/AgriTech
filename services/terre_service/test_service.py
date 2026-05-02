#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'terre_service.settings')

# Configure Django
django.setup()

# Test database connection
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("✅ Database connection successful")
except Exception as e:
    print(f"❌ Database connection failed: {e}")

# Test model import
try:
    from lands.models import Parcelle
    print("✅ Models imported successfully")
    
    # Test creating a test parcelle
    count = Parcelle.objects.count()
    print(f"📊 Current parcelles count: {count}")
    
except Exception as e:
    print(f"❌ Model error: {e}")

# Test migrations
try:
    from django.core.management import execute_from_command_line
    print("✅ Management commands available")
except Exception as e:
    print(f"❌ Management commands error: {e}")

print("🔍 Django service test completed")
