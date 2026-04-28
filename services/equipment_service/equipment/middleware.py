import requests
from django.http import JsonResponse
from django.conf import settings
import os

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Liste des endpoints qui nécessitent une authentification
        protected_paths = ['/api/equipements/']

        if any(request.path.startswith(path) for path in protected_paths):
            # Temporairement désactiver la vérification pour les tests
            if settings.DEBUG:
                pass  # Skip authentication in debug mode
            else:
                auth_header = request.headers.get('Authorization')
                if not auth_header or not auth_header.startswith('Bearer '):
                    return JsonResponse({'error': 'Token manquant'}, status=401)

                token = auth_header.split(' ')[1]

                # Vérifier le token avec le service d'authentification
                auth_service_url = os.getenv('AUTH_SERVICE_URL', 'http://auth-service:8000')
                try:
                    response = requests.post(f'{auth_service_url}/verify-token/', json={'token': token})
                    if response.status_code != 200:
                        return JsonResponse({'error': 'Token invalide'}, status=401)
                except requests.RequestException:
                    return JsonResponse({'error': 'Erreur de vérification du token'}, status=500)

        response = self.get_response(request)
        return response