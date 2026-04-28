import os
import sys

# Force absolute path resolution for Vercel
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from django.core.wsgi import get_wsgi_application
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.equipment_service.equipment_service.settings')
    app = get_wsgi_application()
except Exception as e:
    def app(environ, start_response):
        start_response('500 Error', [('Content-Type', 'text/plain')])
        return [f"Startup Error: {str(e)}".encode()]
