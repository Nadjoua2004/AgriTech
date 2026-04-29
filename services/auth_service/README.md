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

## 🛡️ Troubleshooting & Production Fixes

### 1. Database Connection (PostgreSQL)
Originally, the service was defaulting to local SQLite even in production. The following modifications were made to support **Neon PostgreSQL**:
- **Dependencies**: Added `dj-database-url` and `psycopg2-binary` to `requirements.txt`.
- **Configuration**: Updated `settings.py` to parse `DATABASE_URL` and load `.env` using `python-dotenv`.
- **Superuser Model**: Set `AUTH_USER_MODEL = 'accounts.User'` to resolve model clashes.

### 2. Login Issues
If login fails with "handleLogin is not defined", check for **Git conflict markers** (e.g., `<<<<<<< HEAD`) in your HTML files (especially `agritecture.html`). These markers break JavaScript execution and must be removed.

---
*AgriTech Microservices Suite*
