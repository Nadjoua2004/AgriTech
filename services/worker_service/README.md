# Worker Microservice

The core of your team management. Handles workforce assignments, task tracking, and salary calculations.

## 🚀 Specifications
- **Technology**: Django / REST Framework
- **Database**: Neon (Postgres)
- **Authentication**: JWT verification (Internal middleware)
- **Port**: 8004

## 🎭 Access Control Matrix

| Role | Access Level | Responsibilities |
| :--- | :--- | :--- |
| **farm_manager** | Full Admin | Worker CRUD, Salaries, Full Task Control |
| **supervisor** | Operational | Task assignment, Worker summary view |
| **agronomist** | Read-Only | Audit worker progress and task health |
| **field_worker** (+) | Self-Service | Log own hours, Update own task status |

## 🛠 Setup & Local Development
1. **Migrations**: `python manage.py migrate`
2. **Environment**: Ensure `DATABASE_URL` points to Neon.
3. **Run Server**: `python manage.py runserver 8004`

---
*AgriTech Microservices Suite*
