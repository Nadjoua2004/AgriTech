import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services', 'auth_service'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')

app = get_wsgi_application()
