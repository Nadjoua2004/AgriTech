import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'terre_service.settings')
django.setup()

from lands.models import Parcelle

def seed():
    parcelles = [
        {
            "id": "Z-KKOWPBJ",
            "nom": "Parcelle A1",
            "surface": 1.5,
            "type_sol": "argileux",
            "culture_plantee": "ble",
            "ph": 6.5,
            "nitrogen": 45,
            "moisture": 60
        },
        {
            "id": "X-998877",
            "nom": "Parcelle B2",
            "surface": 2.0,
            "type_sol": "sableux",
            "culture_plantee": "mais",
            "ph": 7.0,
            "nitrogen": 30,
            "moisture": 40
        }
    ]

    for p in parcelles:
        obj, created = Parcelle.objects.update_or_create(id=p['id'], defaults=p)
        if created:
            print(f"Created {p['nom']}")
        else:
            print(f"Updated {p['nom']}")

if __name__ == '__main__':
    seed()
