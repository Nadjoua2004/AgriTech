import os
import sys

sys.path.append(os.path.dirname(__file__))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_service.settings')

app = get_wsgi_application()
