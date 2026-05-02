from django.core.management.base import BaseCommand
from equipment.models import Equipment
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Add sample equipment data'

    def handle(self, *args, **options):
        # Clear existing equipment
        Equipment.objects.all().delete()
        
        sample_equipments = [
            {
                'name': 'Tracteur John Deere 5075',
                'type': 'Tracteur',
                'serial_number': 'JD5075-2023-001',
                'usage_hours': 450,
                'status': 'operational',
                'last_revision': date(2023, 11, 15),
                'next_revision': date(2024, 5, 15)
            },
            {
                'name': 'Moissonneuse-batteuse New Holland CR8.90',
                'type': 'Moissonneuse',
                'serial_number': 'NHCR890-2022-003',
                'usage_hours': 320,
                'status': 'operational',
                'last_revision': date(2023, 10, 1),
                'next_revision': date(2024, 4, 1)
            },
            {
                'name': 'Pulvérisateur Amazone UX 5200',
                'type': 'Pulvérisateur',
                'serial_number': 'AMUX5200-2023-002',
                'usage_hours': 180,
                'status': 'maintenance',
                'last_revision': date(2023, 12, 1),
                'next_revision': date(2024, 6, 1)
            },
            {
                'name': 'Charrue à 4 socs Kverneland',
                'type': 'Charrue',
                'serial_number': 'KV4S-2021-005',
                'usage_hours': 680,
                'status': 'operational',
                'last_revision': date(2023, 9, 15),
                'next_revision': date(2024, 3, 15)
            },
            {
                'name': 'Semoir à céréales Horsch Pronto DC',
                'type': 'Semoir',
                'serial_number': 'HRSPDC-2023-001',
                'usage_hours': 120,
                'status': 'operational',
                'last_revision': date(2023, 11, 20),
                'next_revision': date(2024, 5, 20)
            }
        ]
        
        created_count = 0
        for equipment_data in sample_equipments:
            equipment = Equipment.objects.create(**equipment_data)
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Created equipment: {equipment.name}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} equipment items')
        )
