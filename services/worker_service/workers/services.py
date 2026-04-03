import os
import requests
import jwt
from .mock_data import MOCK_LANDS, MOCK_CULTURES, MOCK_EQUIPMENTS
import logging

logger = logging.getLogger(__name__)

# Helper to check if we should mock
def is_mock(env_var_name):
    # USE_MOCK_AUTH=true defaults for development
    return os.getenv(env_var_name, 'true').lower() == 'true'

def get_land_details(land_id: int) -> dict | None:
    if is_mock('USE_MOCK_LAND'):
        return MOCK_LANDS.get(land_id)
    
    url = f"{os.getenv('LAND_SERVICE_URL')}/lands/{land_id}/"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"Error calling Land Service: {e}")
    return None

def get_culture_details(culture_id: int) -> dict | None:
    if is_mock('USE_MOCK_CULTURE'):
        return MOCK_CULTURES.get(culture_id)
    
    url = f"{os.getenv('CULTURE_SERVICE_URL')}/cultures/{culture_id}/"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"Error calling Culture Service: {e}")
    return None

def get_equipment_details(equipment_id: int) -> dict | None:
    if is_mock('USE_MOCK_EQUIPMENT'):
        return MOCK_EQUIPMENTS.get(equipment_id)
    
    url = f"{os.getenv('EQUIPMENT_SERVICE_URL')}/equipments/{equipment_id}/"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"Error calling Equipment Service: {e}")
    return None

def validate_jwt_token(token: str) -> dict | None:
    if is_mock('USE_MOCK_AUTH'):
        # Just return the payload blindly or rely on request headers in permissions mapping
        pass
        
    url = f"{os.getenv('AUTH_SERVICE_URL')}/verify/"
    try:
        response = requests.post(url, json={'token': token}, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"Error validating token with Auth Service: {e}")
    
    # Alternatively attempt to decode if we have the secret key shared
    # return jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
    return None
