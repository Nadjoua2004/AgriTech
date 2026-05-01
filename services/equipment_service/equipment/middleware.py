import jwt
from django.conf import settings
from django.http import JsonResponse


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'OPTIONS':
            return self.get_response(request)

        protected_prefixes = ['/api/equipements/']

        if not any(request.path.startswith(p) for p in protected_prefixes):
            return self.get_response(request)

        # Local dev: bypass when DEBUG (legacy behaviour).
        if settings.DEBUG:
            return self.get_response(request)

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Token manquant'}, status=401)

        token = auth_header.split(' ', 1)[1].strip()
        try:
            jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=['HS256'],
            )
        except jwt.PyJWTError:
            return JsonResponse({'error': 'Token invalide'}, status=401)

        return self.get_response(request)
