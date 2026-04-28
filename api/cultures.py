import os
import sys

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import using full package path
from services.cultures_service.main import app
