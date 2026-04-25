from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('farm_manager', 'Farm Manager'),
        ('supervisor', 'Supervisor'),
        ('agronomist', 'Agronomist'),
        ('quality_inspector', 'Quality Inspector'),
        ('field_worker', 'Field Worker'),
        ('irrigation_worker', 'Irrigation Worker'),
        ('equipment_operator', 'Equipment Operator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='field_worker')

    def __str__(self):
        return f"{self.username} - {self.role}"
