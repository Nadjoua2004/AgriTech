# Auth Microservice

The identity provider for the Petri platform. Handles user accounts, role management, and JWT issuance with custom claims.

## 🚀 Specifications
- **Technology**: Django / SimpleJWT
- **Database**: Neon (Postgres)
- **Deployment**: Vercel
- **Port**: 8000

## 🎭 Role Manifest
All roles defined here are propagated via JWT claims:
- `farm_manager` (Superuser)
- `supervisor`
- `agronomist`
- `quality_inspector`
- `field_worker`
- ... (others)

## 🛠 Setup & Local Development
1. **Migrations**: `python manage.py migrate`
2. **Environment**: Managed via `.env` (Neon Connection).
3. **Run Server**: `python manage.py runserver 8000`

---
*AgriTech Microservices Suite*
