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

    @action(detail=False, methods=['get'])
    def actives(self, request):
        parcelles = Parcelle.objects.filter(active=True)
        serializer = self.get_serializer(parcelles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def inactives(self, request):
        parcelles = Parcelle.objects.filter(active=False)
        serializer = self.get_serializer(parcelles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        total_parcelles = Parcelle.objects.count()
        total_surface = Parcelle.objects.aggregate(total=Sum('surface'))['total'] or 0
        nb_actives = Parcelle.objects.filter(active=True).count()
        nb_inactives = Parcelle.objects.filter(active=False).count()

        return Response({
            "total_parcelles": total_parcelles,
            "total_surface": total_surface,
            "parcelles_actives": nb_actives,
            "parcelles_inactives": nb_inactives,
        })
