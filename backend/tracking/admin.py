from django.contrib import admin

from .models import PosicionGPS


@admin.register(PosicionGPS)
class PosicionGPSAdmin(admin.ModelAdmin):
    list_display = ('id', 'servicio', 'motorizado', 'lat', 'lng', 'timestamp')
    list_filter = ('motorizado',)
