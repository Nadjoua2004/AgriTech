import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# Get Credentials from environment variable
FIREBASE_CONFIG = os.getenv("FIREBASE_CONFIG")

if not FIREBASE_CONFIG:
    print("ERROR: FIREBASE_CONFIG environment variable is missing.")
    exit(1)

try:
    config = json.loads(FIREBASE_CONFIG)
    cred = credentials.Certificate(config)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    crops = [
        {"name": "Wheat", "type": "Cereal", "status": "Growing", "area": "Field A"},
        {"name": "Corn", "type": "Cereal", "status": "Operational", "area": "Field B"},
        {"name": "Tomato", "type": "Vegetable", "status": "Harvest Ready", "area": "Greenhouse 1"}
    ]

    for crop in crops:
        # Check if already exists to avoid duplicates
        existing = db.collection("cultures").where("name", "==", crop["name"]).get()
        if not existing:
            db.collection("cultures").add(crop)
            print(f"Added {crop['name']}")
        else:
            print(f"Skipped {crop['name']} (already exists)")
            
    print("DONE: Seeded collection 'cultures' in agritech-cultures")
except Exception as e:
    print(f"ERROR: {e}")
