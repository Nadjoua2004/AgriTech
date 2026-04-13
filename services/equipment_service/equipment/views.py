from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
import pika
import json
import os
from .models import Equipment
from .serializers import EquipmentSerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    @action(detail=True, methods=['post'])
    def statut(self, request, pk=None):
        equipment = self.get_object()
        new_status = request.data.get('status')
        if new_status not in ['operational', 'maintenance', 'broken', 'retired']:
            return Response({'error': 'Statut invalide'}, status=status.HTTP_400_BAD_REQUEST)

        equipment.status = new_status
        equipment.save()

        # Envoyer un message RabbitMQ pour alerte maintenance si nécessaire
        if new_status == 'broken':
            self._send_maintenance_alert(equipment)

        serializer = self.get_serializer(equipment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def maintenance(self, request, pk=None):
        equipment = self.get_object()
        equipment.status = 'operational'
        equipment.last_revision = timezone.now().date()
        # Calculer la prochaine révision (exemple: tous les 6 mois)
        equipment.next_revision = equipment.last_revision.replace(month=equipment.last_revision.month + 6)
        equipment.save()

        serializer = self.get_serializer(equipment)
        return Response(serializer.data)

    def _send_maintenance_alert(self, equipment):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=os.getenv('RABBITMQ_HOST', 'rabbitmq'),
                port=int(os.getenv('RABBITMQ_PORT', 5672))
            ))
            channel = connection.channel()
            channel.queue_declare(queue='maintenance_alerts')

            message = {
                'equipment_id': equipment.id,
                'equipment_name': equipment.name,
                'serial_number': equipment.serial_number,
                'status': equipment.status,
                'timestamp': str(timezone.now())
            }

            channel.basic_publish(
                exchange='',
                routing_key='maintenance_alerts',
                body=json.dumps(message)
            )
            connection.close()
        except Exception as e:
            print(f"Erreur envoi RabbitMQ: {e}")