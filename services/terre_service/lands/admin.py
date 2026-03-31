from django.contrib import admin
from .models import Parcelle

@admin.register(Parcelle)
class ParcelleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'surface', 'type_sol', 'culture_plantee', 'active', 'date_creation')
    list_filter = ('type_sol', 'culture_plantee', 'active')
    search_fields = ('nom', 'type_sol', 'culture_plantee')