import os
import sys

# Add the current directory to path so that auth_service package can be found
sys.path.append(os.path.dirname(__file__))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')

app = get_wsgi_application()
