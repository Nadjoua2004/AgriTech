import os
import jwt
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Header, Depends, status, Response
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
ENABLE_FIREBASE = os.getenv("ENABLE_FIREBASE", "false").lower() == "true"

try:
    if ENABLE_FIREBASE and FIREBASE_CONFIG:
        # For Cloud Deployment
        print("🔧 Initializing Firebase from FIREBASE_CONFIG...")
        config_dict = json.loads(FIREBASE_CONFIG)
        cred = credentials.Certificate(config_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        USE_FIREBASE = True
        print("✅ Firebase initialized successfully")
    elif os.path.exists(FIREBASE_KEY_PATH):
        # For Local Development
        print("🔧 Initializing Firebase from file...")
        cred = credentials.Certificate(FIREBASE_KEY_PATH)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        USE_FIREBASE = True
        print("✅ Firebase initialized successfully from file")
    else:
        if ENABLE_FIREBASE:
            print("WARNING: ENABLE_FIREBASE is true but FIREBASE_CONFIG is missing.")
        USE_FIREBASE = False
        mock_db = [] 
except Exception as e:
    print(f"❌ Firebase Init Error: {e}")
    print("⚠️ Falling back to Mock Mode - Service will continue without Firebase")
    USE_FIREBASE = False
    mock_db = []

if USE_FIREBASE:
    print("✅ Database Connected: Firebase Firestore is active.")
else:
    print("⚠️ Database Warning: Running in Mock Mode (No Firebase).")

app = FastAPI(title="AgriTech Cultures Service", redirect_slashes=False)

# --- MIDDLEWARE ---
@app.middleware("http")
async def log_requests(request, call_next):
    # Handle OPTIONS preflight manually
    if request.method == "OPTIONS":
        response = Response()
        response.status_code = 204
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response

    print(f"📥 Incoming Request: {request.method} {request.url}")
    response = await call_next(request)
    
    # Brute force CORS headers onto every response
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    
    print(f"📤 Response Status: {response.status_code}")
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("🚀 Culture Service Starting Up...")
    print(f"📊 Firebase Connected: {USE_FIREBASE}")
    print(f"📝 Mock Data Items: {len(mock_db) if not USE_FIREBASE else 'N/A'}")
    print("✅ All endpoints registered:")
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            print(f"   {route.methods} {route.path}")

# --- MODELS ---
class Culture(BaseModel):
    id: Optional[str] = None
    name: str
    variety: Optional[str] = "Unknown"
    growth: Optional[int] = 0
    days_left: Optional[int] = 0
    yield_est: Optional[str] = "N/A"
    health: Optional[str] = "Good"
    emoji: Optional[str] = "🌱"
    zone: Optional[int] = 1

class GrowthUpdate(BaseModel):
    growth: int

@app.get("/")
async def root():
    return {"status": "online", "message": "AgriTech Cultures Service is running", "database": USE_FIREBASE}

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

@app.patch("/api/cultures/{culture_id}")
async def patch_culture(culture_id: str, data: dict, user_data=Depends(require_roles(["admin", "farm_manager", "quality_inspector"]))):
    if USE_FIREBASE:
        doc_ref = db.collection("cultures").document(culture_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Culture not found")
        doc_ref.update(data)
        return {"id": culture_id, **data}
    
    for i, c in enumerate(mock_db):
        if c["id"] == culture_id:
            mock_db[i].update(data)
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
    if USE_FIREBASE:
        try:
            docs = db.collection("cultures").stream()
            return [ {**doc.to_dict(), "id": doc.id} for doc in docs ]
        except Exception as e:
            print(f"Error fetching from Firebase: {e}")
            return []
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
