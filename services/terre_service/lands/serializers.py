from rest_framework import serializers
from .models import Parcelle

class ParcelleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcelle
        fields = '__all__'

    def validate_surface(self, value):
        if value <= 0:
            raise serializers.ValidationError("La surface doit être supérieure à 0.")
        return value