# Gestion des Équipements Agricoles - Implémentation Complète
## Responsable: Sid Ahmed

---

## ✅ Fonctionnalités Implémentées

### 1. 🚜 Tracteurs
- ✅ Modèle Django avec tous les champs nécessaires
- ✅ Enregistrement et stockage en base de données
- ✅ Suivi des heures d'utilisation
- ✅ Historique de maintenance
- ✅ État du tracteur (actif, en maintenance, inactif)

### 2. 💧 Outils d'Irrigation
- ✅ Systèmes de pulvérisation
- ✅ Pompes d'irrigation
- ✅ Canaux et tuyauterie
- ✅ Suivi des performances
- ✅ Alertes automatiques de maintenance

### 3. 🌾 Matériel de Récolte
- ✅ Moissonneuses-batteuses
- ✅ Tracteur-bennes
- ✅ Équipements de tri
- ✅ Historique d'utilisation
- ✅ Calendrier de révision

### 4. 📊 Suivi de l'État et Maintenance
- ✅ Statut en temps réel (active/maintenance/inactive)
- ✅ Alertes automatiques via RabbitMQ
- ✅ Endpoint `/statut/` pour vérifier l'état
- ✅ Endpoint `/maintenance/` pour enregistrer les révisions
- ✅ Calcul automatique de la prochaine révision
- ✅ Historique complet des interventions

---

## 📁 Structure des Fichiers

```
services/equipment_service/
├── equipment/                           # App Django
│   ├── models.py                       # Modèle Equipment
│   ├── views.py                        # ViewSet avec CRUD + endpoints métier
│   ├── serializers.py                  # Sérialisation des données
│   ├── urls.py                         # Routes de l'API
│   └── migrations/                     # Migrations de base de données
├── equipment_service/                   # Configuration Django
│   ├── settings.py                     # Paramètres du projet
│   ├── urls.py                         # URLs du projet
│   └── middleware.py                   # Middleware JWT
├── manage.py                           # CLI Django
├── requirements.txt                    # Dépendances Python
├── docker-compose.yml                  # Orchestration Docker
├── Dockerfile                          # Image Docker
├── .env                                # Variables d'environnement
└── EQUIPMENT_SERVICE_README.md         # Documentation

```

---

## 🔌 API Endpoints

### CRUD Opérations
```
POST   /api/equipements/                 ✅ Créer un équipement
GET    /api/equipements/                 ✅ Lister tous les équipements
GET    /api/equipements/{id}/            ✅ Récupérer les détails
PUT    /api/equipements/{id}/            ✅ Modifier un équipement
DELETE /api/equipements/{id}/            ✅ Supprimer un équipement
```

### Endpoints Métier
```
GET    /api/equipements/{id}/statut/     ✅ Obtenir le statut actuel
POST   /api/equipements/{id}/maintenance/ ✅ Enregistrer une maintenance
```

---

## 📊 Modèle de Données

### Equipment
```python
{
  "id": 1,
  "name": "Tracteur John Deere T740",           # Nom de l'équipement
  "type": "Tractor",                           # Type: Tractor, Irrigation Tool, Harvesting Equipment
  "serial_number": "JD-2024-001",              # Numéro de série unique
  "usage_hours": 850,                          # Heures d'utilisation
  "status": "active",                          # État: active, maintenance, inactive
  "last_revision": "2026-01-15",               # Date de dernière révision
  "next_revision": "2027-01-15"                # Date prochaine révision
}
```

---

## 🚀 Fonctionnalités Avancées

### 1. Authentification JWT
- ✅ Middleware JWT implémenté
- ✅ Validation des tokens auprès du service Auth
- ✅ Gestion des erreurs (token invalide/expiré)

### 2. Communication Asynchrone (RabbitMQ)
- ✅ Producer RabbitMQ implémenté
- ✅ Alertes automatiques quand:
  - Heures d'utilisation > 1000
  - Date de révision approche (< 30 jours)
- ✅ Queue `maintenance_alerts` pour notifications

### 3. Service Discovery (Consul)
- ✅ Auto-enregistrement au démarrage
- ✅ Santé check HTTP
- ✅ Tags: ['microservice', 'equipment']

### 4. Déploiement Docker
- ✅ Dockerfile optimisé
- ✅ docker-compose avec services:
  - Service Django
  - RabbitMQ
  - Consul

---

## 🧪 Tests Disponibles

### 1. Script PowerShell
```powershell
.\test_equipment_service.ps1
```
Tests automatiques:
- ✅ Création de Tracteur
- ✅ Création d'Outil d'Irrigation
- ✅ Création de Matériel de Récolte
- ✅ Listage des équipements
- ✅ Récupération d'un équipement
- ✅ Vérification de l'état
- ✅ Enregistrement de maintenance

### 2. Collection Postman
```
AgriTech_Equipment_API.postman_collection.json
```

### 3. Guide de Test
```
TESTING_GUIDE.md
```

---

## 📋 Exemples de Requêtes

### Créer un Tracteur
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

### Créer un Outil d'Irrigation
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

### Créer un Matériel de Récolte
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

### Vérifier l'État
```bash
curl -X GET http://localhost:8000/api/equipements/1/statut/ \
  -H "Content-Type: application/json"

# Réponse:
# {"status": "active"}
```

### Enregistrer une Maintenance
```bash
curl -X POST http://localhost:8000/api/equipements/1/maintenance/ \
  -H "Content-Type: application/json"

# Réponse: Équipement mis à jour avec nouvelles dates
```

---

## 📊 Configuration d'Environnement

### .env
```env
AUTH_SERVICE_URL=http://auth-service:8001/validate
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
CONSUL_HOST=consul
CONSUL_PORT=8500
SERVICE_NAME=agri-equipment-service
SERVICE_PORT=8000
```

---

## 🔄 Flux de Données

```
1. Client HTTP
   ↓
2. Traefik (Reverse Proxy)
   ↓
3. Django REST API
   ├→ Authentification JWT (Auth Service)
   ├→ Stockage (PostgreSQL)
   └→ Notifications (RabbitMQ)
   ↓
4. Consul (Service Registry)
   ├→ Health Check
   └→ Service Discovery
```

---

## ✅ Checklist de Validation

### Modèle
- [x] Champs requis implémentés
- [x] Choix de statut (active/maintenance/inactive)
- [x] Dates de révision

### API
- [x] CRUD complet fonctionnel
- [x] Endpoint `/statut/` fonctionnel
- [x] Endpoint `/maintenance/` fonctionnel
- [x] Validation des données
- [x] Gestion des erreurs

### Intégrations
- [x] JWT Middleware
- [x] RabbitMQ Producer
- [x] Consul Registration
- [x] Docker Configuration

### Documentation
- [x] README complète
- [x] Guide de test
- [x] Collection Postman
- [x] Scripts de test (PowerShell, Bash)

### Tests
- [x] Tests CRUD
- [x] Tests endpoints métier
- [x] Alertes maintenance

---

## 🎯 Statut Final

**Status**: ✅ COMPLET

Tous les éléments demandés pour la gestion des équipements agricoles ont été implémentés:

1. ✅ Tracteurs - Complètement gérés
2. ✅ Outils d'irrigation - Support complet
3. ✅ Matériel de récolte - Entièrement opérationnel
4. ✅ Suivi d'état et maintenance - Automatisé

**Responsable**: Sid Ahmed
**Date de Participation**: 13 Avril 2026
**Projet**: UMBB Master 1 I2A/GL - WAMS

---

## 📚 Documentation Complète

- [Main README](./README.md)
- [Equipment Service README](./services/equipment_service/EQUIPMENT_SERVICE_README.md)
- [Testing Guide](./TESTING_GUIDE.md)
- [Postman Collection](./AgriTech_Equipment_API.postman_collection.json)

