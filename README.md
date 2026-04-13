# AgriTech - Pipeline Microservices Complet

Plateforme complète de gestion pour ferme agricole intelligente (AgriSmart).

## 📋 Structure du Projet

```
services/
├── auth_service/                # Service d'Authentification
│   ├── accounts/               # App Django
│   ├── manage.py
│   └── requirements.txt
├── cultures_service/            # Service de Gestion des Cultures
│   ├── crops/                  # App Django
│   ├── manage.py
│   └── requirements.txt
├── equipment_service/           # Service de Gestion des Équipements ⭐ (Sid Ahmed)
│   ├── equipment/              # App Django
│   ├── EQUIPMENT_SERVICE_README.md
│   ├── manage.py
│   └── requirements.txt
├── terre_service/               # Service de Gestion des Terres
│   ├── lands/                  # App Django
│   ├── manage.py
│   └── requirements.txt
└── worker_service/              # Service de Gestion du Personnel
    ├── workers/                # App Django
    ├── manage.py
    └── requirements.txt
```

## 👥 Équipe et Responsabilités

| Équipier | Service | Responsabilités | Statut |
|----------|---------|-----------------|--------|
| **Sid Ahmed** | **equipment_service** | **Gestion des équipements** | ✅ |
| | | Tracteurs, Outils d'irrigation, Matériel de récolte | |
| | | Suivi d'état et maintenance | |
| | | | |

## 🎯 Services

### 1. Equipment Service (Sid Ahmed) ⭐

**Description**: Gestion complète des équipements agricoles

**Ressources**:
- [Documentation Détaillée](./services/equipment_service/EQUIPMENT_SERVICE_README.md)

**Équipements gérés**:
- 🚜 **Tracteurs**
- 💧 **Outils d'Irrigation**
- 🌾 **Matériel de Récolte**

**Fonctionnalités clés**:
- CRUD complet
- Suivi d'état en temps réel
- Maintenance automatisée
- Alertes RabbitMQ
- API REST

### 2. Auth Service

Service centralisé d'authentification et autorisation.

### 3. Cultures Service

Gestion des cultures et données de cultivation.

### 4. Terre Service

Gestion des terres et données pédologiques.

### 5. Worker Service

Gestion du personnel agricole et données de travail.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│          Interface Web Frontend                 │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────┴──────────────────┐
│     Traefik (Reverse Proxy)         │
│     Load Balancer                   │
└──────────────────┬──────────────────┘
    ┌──────────────┼──────────────────┐
    │              │                  │  
    ▼              ▼                  ▼
┌────────┐   ┌────────┐   ┌────────┐
│Auth    │   │Equipment│   │Cultures│  etc.
│Service │   │Service │   │Service │
└────────┘   └────────┘   └────────┘
    │              │                  │
    └──────────────┼──────────────────┘
                   │
       ┌───────────┼───────────┐
       │           │           │
       ▼          ▼           ▼
   ┌────────┐ ┌──────────┐ ┌────────┐
   │PostgreSQL  │RabbitMQ │ │Consul  │
   └────────┘ └──────────┘ └────────┘
```

## 🚀 Démarrage Local

### Prerequisites
- Python 3.10+
- PostgreSQL
- RabbitMQ
- Consul

### Installation

1. **Cloner le projet**:
```bash
git clone https://github.com/Nadjoua2004/AgriTech.git
cd AgriTech
```

2. **Pour chaque service**:
```bash
cd services/equipment_service
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 📚 Documentation

- [Equipment Service](./services/equipment_service/EQUIPMENT_SERVICE_README.md) - Gestion des équipements
- [API Documentation](./docs/api.md) - (À venir)
- [Guide de Déploiement](./docs/deployment.md) - (À venir)

## 🔐 Sécurité

- JWT Authentication
- Service-to-service communication via Consul
- Rate limiting via Traefik
- Environment variables encryption

## 📊 Monitoring

- Health checks via Consul
- Logs centralisés (ELK Stack - À implémenter)
- Metrics via Prometheus (À implémenter)

## 🧪 Tests

```bash
cd services/[service-name]
pytest
```

## 📞 Support

Pour des questions ou problèmes, contactez l'équipe de développement.

## 📄 Licence

UMBB Master 1 I2A/GL - Projet WAMS
Université M'Hamed Bougara

---

**Dernière mise à jour**: 13 Avril 2026
**Équipe**: AgriTech Development Team
**Responsable Principal**: Sid Ahmed (Equipment Service)