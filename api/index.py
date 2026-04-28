import os
import sys
import traceback

# Add the project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from django.core.wsgi import get_wsgi_application
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frontend.settings')
    app = get_wsgi_application()
except Exception as e:
    print("CRITICAL STARTUP ERROR IN FRONTEND:")
    traceback.print_exc()
    # Return a simple error app for Vercel to see
    def app(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [f"Startup Error: {str(e)}\n\n{traceback.format_exc()}".encode('utf-8')]
