from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum

from .models import Parcelle
from .serializers import ParcelleSerializer

class ParcelleViewSet(viewsets.ModelViewSet):
    queryset = Parcelle.objects.all().order_by('-date_creation')
    serializer_class = ParcelleSerializer
    permission_classes = [permissions.AllowAny]

    def handle_exception(self, exc):
        print(f"!!! TERRE SERVICE CRASH: {str(exc)}")
        return super().handle_exception(exc)

    def perform_update(self, serializer):
        try:
            print(f"Updating parcelle: {self.get_object().id}")
            serializer.save()
        except Exception as e:
            print(f"!!! UPDATE ERROR: {str(e)}")
            raise e
