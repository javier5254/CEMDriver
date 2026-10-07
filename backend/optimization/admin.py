from django.contrib import admin

from .models import PuntoGeocodificado


@admin.register(PuntoGeocodificado)
class PuntoGeocodificadoAdmin(admin.ModelAdmin):
    list_display = ['servicio', 'lat', 'lng', 'direccion_geocodificada', 'creado_en']
    search_fields = ['direccion_geocodificada']
