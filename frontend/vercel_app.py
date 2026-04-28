import os
import sys
from pathlib import Path

# Set the path to the directory containing settings.py
sys.path.append(os.path.dirname(__file__))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = get_wsgi_application()
