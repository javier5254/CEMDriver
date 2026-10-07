from django.contrib import admin

from .models import Cobertura


@admin.register(Cobertura)
class CoberturaAdmin(admin.ModelAdmin):
    list_display = ('zona', 'leadtime_dias', 'dias_disponibles', 'hora_inicio', 'hora_fin')
