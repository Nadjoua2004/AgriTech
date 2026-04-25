# Cultures Microservice

A specialized service for tracking crop growth, health, and yields. This service uses **Firebase Firestore** for its data persistence and enforces strict RBAC (Role-Based Access Control).

## 🚀 Specifications
- **Technology**: FastAPI (Python)
- **Database**: Firebase Cloud Firestore
- **Authentication**: JWT verification (Shared Secret)
- **Production URL**: `https://cultures-service.onrender.com`

## 🎭 Access Control Matrix

| Action | Allowed Roles |
| :--- | :--- |
| **List Cultures** (`GET`) | All authenticated users |
| **Add Culture** (`POST`) | `admin`, `farm_manager` |
| **Delete Culture** (`DELETE`) | `admin`, `farm_manager` |
| **Update Growth** (`PATCH`) | `admin`, `farm_manager`, `quality_inspector` |

## 🛠 Setup & Local Development

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Firebase Configuration**:
   Place your `firebase-key.json` in this directory.
3. **Environment**:
   Ensure `.env` matches the global `JWT_SECRET`.
4. **Run Server**:
   ```bash
   python main.py
   ```

## 📡 API Endpoints
- `GET /api/cultures` - Fetch all crops.
- `POST /api/cultures` - Register a new crop row.
- `PATCH /api/cultures/{id}/growth` - Update growth percentage (Inspector only).
- `DELETE /api/cultures/{id}` - Remove a crop record.

---
*AgriTech Microservices Suite*
