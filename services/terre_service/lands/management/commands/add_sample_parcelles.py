from django.core.management.base import BaseCommand
from lands.models import Parcelle

class Command(BaseCommand):
    help = 'Add sample parcelles data'

    def handle(self, *args, **options):
        # Clear existing parcelles
        Parcelle.objects.all().delete()
        
        sample_parcelles = [
            {
                'nom': 'Z-YFG81',
                'surface': 15.50,
                'type_sol': 'argileux',
                'culture_plantee': 'ble',
                'localisation': 'Nord du terrain',
                'latitude': 48.8566,
                'longitude': 2.3522,
                'ph': 6.5,
                'nitrogen': 45,
                'moisture': 68
            },
            {
                'nom': 'A-ABC12',
                'surface': 22.75,
                'type_sol': 'limoneux',
                'culture_plantee': 'mais',
                'localisation': 'Sud-Est',
                'latitude': 48.8566,
                'longitude': 2.3522,
                'ph': 7.2,
                'nitrogen': 38,
                'moisture': 72
            },
            {
                'nom': 'B-XYZ99',
                'surface': 18.25,
                'type_sol': 'sableux',
                'culture_plantee': 'tomate',
                'localisation': 'Zone Ouest',
                'latitude': 48.8566,
                'longitude': 2.3522,
                'ph': 6.8,
                'nitrogen': 42,
                'moisture': 71
            }
        ]
        
        created_count = 0
        for parcelle_data in sample_parcelles:
            parcelle = Parcelle.objects.create(**parcelle_data)
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Created parcelle: {parcelle.nom}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} parcelles')
        )
