from django.db import models

class Equipment(models.Model):
    STATUS_CHOICES = [
        ('operational', 'Opérationnel'),
        ('maintenance', 'En maintenance'),
        ('broken', 'Cassé'),
        ('retired', 'Retiré'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nom de l'équipement")
    type = models.CharField(max_length=50, verbose_name="Type d'équipement")
    serial_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro de série")
    usage_hours = models.IntegerField(default=0, verbose_name="Heures d'utilisation")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='operational', verbose_name="Statut")
    last_revision = models.DateField(null=True, blank=True, verbose_name="Dernière révision")
    next_revision = models.DateField(null=True, blank=True, verbose_name="Prochaine révision")

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    class Meta:
        verbose_name = "Équipement"
        verbose_name_plural = "Équipements"