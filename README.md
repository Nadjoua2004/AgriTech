# AgriTech Ecosystem — Microservices Platform

A modern, high-end agricultural management platform built using a microservices architecture. Each service is decoupled, using targeted database solutions and deployed on specialized providers.

## 🏗 System Architecture

| Service | Responsibility | Database | Deployment | Status |
| :--- | :--- | :--- | :--- | :--- |
| **`auth_service`** | Identity, JWT & RBAC | Neon (Postgres) | Vercel | ✅ Live |
| **`worker_service`** | HR, Tasks & Payroll | Neon (Postgres) | TBD | 🚧 Dev |
| **`cultures_service`**| Crop Growth & Health | Firebase (Firestore)| Render | ✅ Live |
| **`terre_service`** | Land & Parcel GIS | TBD | TBD | ⏳ Backlog |
| **`equipment_service`**| Machinery Inventory | TBD | TBD | ⏳ Backlog |
| **`frontend`** | Agritecture UI | Django (Statics) | Local/Vercel | ✅ Live |

## 🔑 Shared Security (JWT RBAC)

All services share a common authentication protocol:
1. **Issuer**: `auth_service` generates JWTs with custom role claims.
2. **Roles**: `admin`, `farm_manager`, `supervisor`, `agronomist`, `quality_inspector`, `field_worker`, `irrigation_worker`, `equipment_operator`.
3. **Verification**: Each microservice independently verifies tokens using the shared `JWT_SECRET`.

## 🛠 Tech Stack
- **Backend Frameworks**: Django (Auth, Workers), FastAPI (Cultures).
- **Frontend**: Django Templates + Tailwind CSS + Syne/Cabinet Grotesk Typography.
- **Databases**: PostgreSQL (Neon), NoSQL (Firebase).
- **Deployment**: Vercel (Auth), Koyeb (Cultures - planned).

---

## 📂 Service Directory

### [`/services/auth_service`](file:///c:/Users/Nadjoua/Desktop/AgriTech/services/auth_service)
The centralized gatekeeper for the entire ecosystem. Handles user registration and generates tokens with role-based permissions.

### [`/services/cultures_service`](file:///c:/Users/Nadjoua/Desktop/AgriTech/services/cultures_service)
Specialized NoSQL service for tracking crops. Integrated with Firebase for real-time health and growth updates.

### [`/services/worker_service`](file:///c:/Users/Nadjoua/Desktop/AgriTech/services/worker_service)
Relational service for managing the workforce, assigning tasks, and calculating salaries based on logged hours.

---
*Created by Antigravity © 2026*
