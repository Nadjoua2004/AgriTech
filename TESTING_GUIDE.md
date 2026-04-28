# Equipment Service API - Testing Guide

## 📋 Overview

This guide explains how to test the Equipment Service microservice for AgriTech.

---

## 🚀 Prerequisites

- Python 3.10+
- Virtual Environment activated
- Django dependencies installed
- Server running on `http://localhost:8000`

---

## ▶️ Quick Start

### 1. Start the Equipment Service

```bash
cd services/equipment_service

# On Windows
..\..\..\venv\Scripts\python.exe manage.py runserver

# On Linux/Mac
../../../venv/bin/python manage.py runserver
```

Server will run at: **http://localhost:8000**

---

## 🧪 Testing Methods

### Method 1: PowerShell Test Script

```powershell
# Run the automated test script
.\test_equipment_service.ps1
```

This will:
- ✅ Create 3 equipment items (Tracteur, Irrigation Tool, Harvesting Equipment)
- ✅ List all equipment
- ✅ Retrieve equipment details
- ✅ Get equipment status
- ✅ Record maintenance

---

### Method 2: Bash/Shell Test Script

```bash
# Run the automated test script
bash test_equipment_service.sh
```

---

### Method 3: Postman Collection

1. **Import Collection**:
   - Open Postman
   - Import `AgriTech_Equipment_API.postman_collection.json`

2. **Run Tests**:
   - Navigate to "Equipment Management" folder
   - Execute each request one by one
   - Check responses

---

### Method 4: Manual cURL Commands

#### Create Equipment (Tracteur)

```bash
curl -X POST http://localhost:8000/api/equipements/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tracteur John Deere T740",
    "type": "Tractor",
    "serial_number": "JD-2024-001",
    "usage_hours": 850,
    "status": "active",
    "last_revision": "2026-01-15",
    "next_revision": "2027-01-15"
  }'
```

#### Create Irrigation Tool

```bash
curl -X POST http://localhost:8000/api/equipements/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Système d'"'"'Irrigation Pivot",
    "type": "Irrigation Tool",
    "serial_number": "IRR-2024-001",
    "usage_hours": 450,
    "status": "active",
    "last_revision": "2026-02-01",
    "next_revision": "2026-08-01"
  }'
```

#### Create Harvesting Equipment

```bash
curl -X POST http://localhost:8000/api/equipements/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Moissonneuse-batteuse CLAAS",
    "type": "Harvesting Equipment",
    "serial_number": "CLAAS-2024-001",
    "usage_hours": 320,
    "status": "maintenance",
    "last_revision": "2026-03-01",
    "next_revision": "2026-09-01"
  }'
```

#### List All Equipment

```bash
curl -X GET http://localhost:8000/api/equipements/ \
  -H "Content-Type: application/json"
```

#### Get Equipment Details

```bash
curl -X GET http://localhost:8000/api/equipements/1/ \
  -H "Content-Type: application/json"
```

#### Get Equipment Status

```bash
curl -X GET http://localhost:8000/api/equipements/1/statut/ \
  -H "Content-Type: application/json"
```

#### Record Maintenance

```bash
curl -X POST http://localhost:8000/api/equipements/1/maintenance/ \
  -H "Content-Type: application/json"
```

#### Update Equipment

```bash
curl -X PUT http://localhost:8000/api/equipements/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tracteur John Deere T740 (Updated)",
    "type": "Tractor",
    "serial_number": "JD-2024-001",
    "usage_hours": 920,
    "status": "active",
    "last_revision": "2026-01-15",
    "next_revision": "2027-01-15"
  }'
```

#### Delete Equipment

```bash
curl -X DELETE http://localhost:8000/api/equipements/1/ \
  -H "Content-Type: application/json"
```

---

## 📊 Expected Responses

### Success Response (200 OK)

```json
{
  "id": 1,
  "name": "Tracteur John Deere T740",
  "type": "Tractor",
  "serial_number": "JD-2024-001",
  "usage_hours": 850,
  "status": "active",
  "last_revision": "2026-01-15",
  "next_revision": "2027-01-15"
}
```

### List Response (200 OK)

```json
[
  {
    "id": 1,
    "name": "Tracteur John Deere T740",
    "type": "Tractor",
    ...
  },
  {
    "id": 2,
    "name": "Système d'Irrigation Pivot",
    "type": "Irrigation Tool",
    ...
  }
]
```

### Status Response (200 OK)

```json
{
  "status": "active"
}
```

### Error Response (400 Bad Request)

```json
{
  "error": "Invalid data",
  "details": "..."
}
```

---

## 🐛 Troubleshooting

### Issue: Connection Refused

**Solution**: Ensure Django server is running
```bash
python manage.py runserver
```

### Issue: Page Not Found (404)

**Solution**: Check if endpoint path is correct

### Issue: Database Error

**Solution**: Apply migrations
```bash
python manage.py migrate
```

### Issue: CORS Error

**Solution**: Add allowed origin to `CORS_ALLOWED_ORIGINS` in `settings.py`

---

## ✅ Test Checklist

- [ ] POST /api/equipements/ - Create equipment
- [ ] GET /api/equipements/ - List equipment
- [ ] GET /api/equipements/{id}/ - Get details
- [ ] PUT /api/equipements/{id}/ - Update equipment
- [ ] DELETE /api/equipements/{id}/ - Delete equipment
- [ ] GET /api/equipements/{id}/statut/ - Get status
- [ ] POST /api/equipements/{id}/maintenance/ - Record maintenance

---

## 📝 API Documentation

For full API documentation, see:
- [Equipment Service README](./services/equipment_service/EQUIPMENT_SERVICE_README.md)
- [Main Project README](./README.md)

---

## 📞 Support

For issues or questions, contact the development team.

**Responsable**: Sid Ahmed
**Service**: Gestion des Équipements Agricoles
**Date**: April 13, 2026