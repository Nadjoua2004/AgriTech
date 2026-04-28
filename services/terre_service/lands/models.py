from django.db import models

class Parcelle(models.Model):
    TYPE_SOL_CHOICES = [
        ('argileux', 'Argileux'),
        ('sableux', 'Sableux'),
        ('limoneux', 'Limoneux'),
        ('calcaire', 'Calcaire'),
        ('humifere', 'Humifère'),
        ('autre', 'Autre'),
    ]

    CULTURE_CHOICES = [
        ('ble', 'Blé'),
        ('mais', 'Maïs'),
        ('orge', 'Orge'),
        ('pomme_de_terre', 'Pomme de terre'),
        ('tomate', 'Tomate'),
        ('olive', 'Olive'),
        ('aucune', 'Aucune'),
        ('autre', 'Autre'),
    ]

    nom = models.CharField(max_length=100, unique=True)
    surface = models.DecimalField(max_digits=10, decimal_places=2)
    type_sol = models.CharField(max_length=30, choices=TYPE_SOL_CHOICES)
    culture_plantee = models.CharField(max_length=30, choices=CULTURE_CHOICES, default='aucune')
    localisation = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Données scientifiques (Agronome)
    ph = models.DecimalField(max_digits=4, decimal_places=2, default=6.8)
    nitrogen = models.IntegerField(default=42)
    moisture = models.IntegerField(default=71)

    active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom