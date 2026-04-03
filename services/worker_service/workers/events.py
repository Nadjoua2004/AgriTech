import json
import logging
import os
import pika
from datetime import datetime
from decimal import Decimal

logger = logging.getLogger(__name__)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DecimalEncoder, self).default(obj)

def _publish(queue_name, payload):
    rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost/')
    try:
        parameters = pika.URLParameters(rabbitmq_url)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(payload, cls=DecimalEncoder)
        )
        connection.close()
    except Exception as e:
        # If RabbitMQ is down, log the error but don't crash
        logger.error(f"Failed to publish to {queue_name}: {e}")

def publish_task_completed(worker_id, land_id, culture_id, date):
    """
    Event 1 — When a task is marked as done
    """
    payload = {
        "worker_id": worker_id,
        "land_id": land_id,
        "culture_id": culture_id,
        "date": date.isoformat() if hasattr(date, 'isoformat') else date,
        "timestamp": datetime.now().isoformat()
    }
    _publish("task.completed", payload)

def publish_salary_calculated(worker_id, month, total_amount):
    """
    Event 2 — When a salary is calculated
    """
    payload = {
        "worker_id": worker_id,
        "month": month.isoformat() if hasattr(month, 'isoformat') else month,
        "total_amount": total_amount,
        "timestamp": datetime.now().isoformat()
    }
    _publish("salary.paid", payload)

def publish_worker_created(worker_id, worker_type, zone):
    """
    Event 3 — When a new worker is created
    """
    payload = {
        "worker_id": worker_id,
        "worker_type": worker_type,
        "zone": zone,
        "timestamp": datetime.now().isoformat()
    }
    _publish("worker.created", payload)
