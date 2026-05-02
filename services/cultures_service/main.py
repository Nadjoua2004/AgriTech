import os
import jwt
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Header, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore
import json
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
JWT_SECRET = os.getenv("JWT_SECRET", "django-insecure-agritech-production-key-change-me-2024")
ALGORITHM = "HS256"
FIREBASE_KEY_PATH = os.getenv("FIREBASE_CREDENTIALS_JSON", "firebase-key.json")
FIREBASE_CONFIG = os.getenv("FIREBASE_CONFIG") # Entire JSON as string

# --- FIREBASE INIT ---
import signal
import sys

def timeout_handler(signum, frame):
    raise TimeoutError("Firebase initialization timed out")

try:
    if FIREBASE_CONFIG:
        # For Cloud Deployment (Koyeb/Railway)
        print("🔧 Attempting Firebase initialization from FIREBASE_CONFIG...")
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(10)  # 10 second timeout
        
        config_dict = json.loads(FIREBASE_CONFIG)
        cred = credentials.Certificate(config_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        USE_FIREBASE = True
        
        signal.alarm(0)  # Cancel timeout
        print("✅ Firebase initialized successfully from FIREBASE_CONFIG")
        
    elif os.path.exists(FIREBASE_KEY_PATH):
        # For Local Development
        print("🔧 Attempting Firebase initialization from file...")
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(10)  # 10 second timeout
        
        cred = credentials.Certificate(FIREBASE_KEY_PATH)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        USE_FIREBASE = True
        
        signal.alarm(0)  # Cancel timeout
        print("✅ Firebase initialized successfully from file")
        
    else:
        print(f"WARNING: No Firebase config found. Running in Mock Mode.")
        USE_FIREBASE = False
        mock_db = [
            {
                "id": "1",
                "name": "Tomatoes",
                "variety": "Cherry",
                "growth": 75,
                "days_left": 15,
                "yield_est": "2.5 kg",
                "health": "Good",
                "emoji": "🍅",
                "zone": 1
            },
            {
                "id": "2", 
                "name": "Lettuce",
                "variety": "Romaine",
                "growth": 45,
                "days_left": 20,
                "yield_est": "1.8 kg",
                "health": "Excellent",
                "emoji": "🥬",
                "zone": 2
            }
        ]
        
except (json.JSONDecodeError, Exception, TimeoutError) as e:
    print(f"❌ Firebase Init Error: {e}")
    print("⚠️ Falling back to Mock Mode - Service will continue without Firebase")
    USE_FIREBASE = False
    mock_db = [
        {
            "id": "1",
            "name": "Tomatoes",
            "variety": "Cherry",
            "growth": 75,
            "days_left": 15,
            "yield_est": "2.5 kg",
            "health": "Good",
            "emoji": "🍅",
            "zone": 1
        },
        {
            "id": "2", 
            "name": "Lettuce",
            "variety": "Romaine",
            "growth": 45,
            "days_left": 20,
            "yield_est": "1.8 kg",
            "health": "Excellent",
            "emoji": "🥬",
            "zone": 2
        }
    ]
    signal.alarm(0)  # Ensure timeout is cancelled

if USE_FIREBASE:
    print("✅ Database Connected: Firebase Firestore is active.")
else:
    print("⚠️ Database Warning: Running in Mock Mode (No Firebase).")

app = FastAPI(title="AgriTech Cultures Service")

@app.on_event("startup")
async def startup_event():
    print("🚀 Culture Service Starting Up...")
    print(f"📊 Firebase Connected: {USE_FIREBASE}")
    print(f"📝 Mock Data Items: {len(mock_db) if not USE_FIREBASE else 'N/A'}")
    print("✅ All endpoints registered:")
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            print(f"   {route.methods} {route.path}")

_origins_raw = os.getenv("ALLOWED_ORIGINS", "*").strip()
_origins = [o.strip() for o in _origins_raw.split(",") if o.strip()]
# Browsers reject allow_credentials=True together with Access-Control-Allow-Origin: *.
_cors_credentials = True
if not _origins or _origins == ["*"]:
    _origins = ["*"]
    _cors_credentials = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=_cors_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---
class Culture(BaseModel):
    id: Optional[str] = None
    name: str
    variety: str
    growth: int
    days_left: int
    yield_est: str
    health: str
    emoji: str
    zone: int

class GrowthUpdate(BaseModel):
    growth: int

# --- AUTH HELPERS ---
def get_user_data(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload # Returns {user_id, role, username}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def require_roles(roles: List[str]):
    def role_checker(user_data=Depends(get_user_data)):
        if user_data.get("role") not in roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user_data
    return role_checker

# --- ENDPOINTS ---

@app.get("/api/cultures", response_model=List[Culture])
async def get_cultures(user_data=Depends(get_user_data)):
    if USE_FIREBASE:
        docs = db.collection("cultures").stream()
        return [ {**doc.to_dict(), "id": doc.id} for doc in docs ]
    return mock_db

@app.post("/api/cultures", response_model=Culture)
async def add_culture(culture: Culture, user_data=Depends(require_roles(["admin", "farm_manager"]))):
    culture_data = culture.model_dump(exclude={"id"})
    if USE_FIREBASE:
        update_time, doc_ref = db.collection("cultures").add(culture_data)
        return {**culture_data, "id": doc_ref.id}
    
    new_id = str(len(mock_db) + 1)
    new_culture = {**culture_data, "id": new_id}
    mock_db.append(new_culture)
    return new_culture

@app.put("/api/cultures/{culture_id}")
async def update_culture(culture_id: str, culture: Culture, user_data=Depends(require_roles(["admin", "farm_manager"]))):
    culture_data = culture.model_dump(exclude={"id"})
    if USE_FIREBASE:
        doc_ref = db.collection("cultures").document(culture_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Culture not found")
        doc_ref.set(culture_data, merge=True)
        return {**culture_data, "id": culture_id}
    
    for i, c in enumerate(mock_db):
        if c["id"] == culture_id:
            mock_db[i] = {**culture_data, "id": culture_id}
            return mock_db[i]
    raise HTTPException(status_code=404, detail="Culture not found")

@app.patch("/api/cultures/{culture_id}/growth")
async def update_growth(culture_id: str, update: GrowthUpdate, user_data=Depends(require_roles(["admin", "farm_manager", "quality_inspector"]))):
    if USE_FIREBASE:
        doc_ref = db.collection("cultures").document(culture_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Culture not found")
        doc_ref.update({"growth": update.growth})
        return {"status": "success", "growth": update.growth}
    
    # Mock update
    for c in mock_db:
        if c["id"] == culture_id:
            c["growth"] = update.growth
            return {"status": "success", "growth": update.growth}
    raise HTTPException(status_code=404, detail="Culture not found")

@app.delete("/api/cultures/{culture_id}")
async def delete_culture(culture_id: str, user_data=Depends(require_roles(["admin", "farm_manager"]))):
    if USE_FIREBASE:
        doc_ref = db.collection("cultures").document(culture_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Culture not found")
        doc_ref.delete()
        return {"status": "deleted"}
    
    # Mock delete
    global mock_db
    mock_db = [c for c in mock_db if c["id"] != culture_id]
    return {"status": "deleted"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "cultures-service",
        "firebase_connected": USE_FIREBASE,
        "version": "1.0.0"
    }

@app.get("/api/cultures/public")
async def get_cultures_public():
    """Public endpoint for testing without authentication"""
    return mock_db

@app.get("/api/debug/auth")
async def debug_auth(user_data=Depends(get_user_data)):
    return {
        "status": "Authenticated",
        "user": user_data,
        "firebase_connected": USE_FIREBASE
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
