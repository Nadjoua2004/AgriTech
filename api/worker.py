import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services', 'worker_service'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worker_service.settings')

app = get_wsgi_application()
