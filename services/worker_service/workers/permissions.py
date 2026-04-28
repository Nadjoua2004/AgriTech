from rest_framework import permissions
import jwt
from django.conf import settings
from .services import validate_jwt_token
import os

def decode_jwt_from_request(request):
    """
    decode_jwt_from_request(request) -> returns {user_id, role}
    """
    if os.getenv('USE_MOCK_AUTH', 'true').lower() == 'true':
        mock_role = request.headers.get('X-Mock-Role', 'supervisor')
        mock_user = request.headers.get('X-Mock-UserId', '1') # Default supervisor user
        return {'user_id': int(mock_user), 'role': mock_role}

    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    
    val_res = validate_jwt_token(token)
    if val_res and 'role' in val_res and 'user_id' in val_res:
         return {'user_id': val_res['user_id'], 'role': val_res['role']}
         
    try:
        # Fallback to local decode
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return {'user_id': payload.get('user_id'), 'role': payload.get('role')}
    except jwt.PyJWTError:
        return None

def is_manager(role):
    return role == 'farm_manager'

def is_supervisor_or_above(role):
    return role in ['farm_manager', 'supervisor']

def is_worker_only(role):
    return role in ['field_worker', 'irrigation_worker', 'equipment_operator']

class JWTRolePermission(permissions.BasePermission):
    """
    farm_manager     → full access (read + write + delete everything)
    supervisor       → can assign tasks, view all workers, log hours
    agronomist       → read-only on workers and tasks
    field_worker     → can only see their OWN tasks and hours (filter by user_id)
    irrigation_worker → same as field_worker
    equipment_operator → same as field_worker
    """
    def has_permission(self, request, view):
        user_data = decode_jwt_from_request(request)
        if not user_data:
            return False
            
        request.user_data = user_data # Attach to request
        role = user_data.get('role')
        
        # Read-only operations allowed for agronomists, supervisors, managers
        if request.method in permissions.SAFE_METHODS:
            return True

        if is_supervisor_or_above(role):
            return True
            
        return True # Default to true here, view-level and object-level permissions manage the rest.

    def has_object_permission(self, request, view, obj):
        user_data = getattr(request, 'user_data', None)
        if not user_data:
            return False
            
        role = user_data.get('role')
        user_id = user_data.get('user_id')

        if is_supervisor_or_above(role):
            return True

        if role in ['agronomist', 'quality_inspector']:
            return request.method in permissions.SAFE_METHODS
            
        # Specific model limitations (workers only read/edit their own data)
        # Note: Handled mostly in ViewSet get_queryset methods,
        # but here we can block writes to other users records.
        if is_worker_only(role):
            # A worker can only edit tasks/hours assigned to them
            if hasattr(obj, 'worker') and obj.worker.user_id == user_id:
                return True
            if hasattr(obj, 'user_id') and obj.user_id == user_id:
                return True
            return False

        # Catch-all
        return False
