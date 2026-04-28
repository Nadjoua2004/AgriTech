# Gestion des Équipements Agricoles - Service des Équipements

**Responsable**: Sid Ahmed

## Description

Service de gestion complète des équipements agricoles pour la plateforme AgriTech - Ferme Intelligente.

## Fonctionnalités

Le service gère les types d'équipements suivants:

### 1. **Tracteurs** 🚜
- Enregistrement et suivi des tracteurs
- Historique d'utilisation
- Spécifications techniques
- État de maintenance

### 2. **Outils d'Irrigation** 💧
- Pompes d'irrigation
- Systèmes de pulvérisation
- Canaux et tuyauterie
- Débitmètres et capteurs

### 3. **Matériel de Récolte** 🌾
- Moissonneuses-batteuses
- Tracteur-bennes
- Équipements de tri
- Outils de moisson

## Fonctionnalités Principales

### Suivi de l'État
- État actif, en maintenance, inactif
- Statut en temps réel
- Alertes automatiques
- Notifications de panne

### Suivi de la Maintenance
- Calendrier de maintenance préventive
- Historique complète des réparations
- Pièces détachées utilisées
- Coûts de maintenance
- Alertes de révision échéance

## API Endpoints

### CRUD Basique
```
GET    /api/equipements/              - Lister tous les équipements
POST   /api/equipements/              - Créer un nouvel équipement
GET    /api/equipements/{id}/         - Détails d'un équipement
PUT    /api/equipements/{id}/         - Modifier un équipement
DELETE /api/equipements/{id}/         - Supprimer un équipement
```

### Endpoints Métier
```
GET    /api/equipements/{id}/statut/         - Obtenir le statut
POST   /api/equipements/{id}/maintenance/   - Enregistrer maintenance
GET    /api/equipements/{id}/historique/    - Historique complet
POST   /api/equipements/{id}/alerte/        - Créer une alerte
```

## Modèles de Données

### Equipment
```
{
  "id": 1,
  "name": "Tracteur John Deere",
  "type": "Tractor",
  "serial_number": "JD-2024-001",
  "usage_hours": 1250,
  "status": "active",
  "last_revision": "2026-01-15",
  "next_revision": "2026-07-15",
  "description": "Tracteur agricole 75 CV",
  "specifications": {...}
}
```

## Configuration

Voir `.env` pour les variables d'environnement requises.

## Notifications RabbitMQ

Alertes automatiques envoyées via queue `maintenance_alerts`:
- Dépassement du seuil d'heures d'utilisation
- Approche de date de révision
- État de panne détecté
- Maintenance urgente requise

## Statut du Développement

- ✅ Modèle Django implémenté
- ✅ API CRUD fonctionnelle
- ✅ Middleware JWT
- ✅ Intégration RabbitMQ
- ✅ Enregistrement Consul
- ⏳ Dashboard UI
- ⏳ Rapports de maintenance
- ⏳ Analyse prédictive

## Développeur

**Sid Ahmed** - Microservice de Gestion des Équipements

Université M'Hamed Bougara - UMBB
Master 1 Informatique - Semestre 2
Projet WAMS