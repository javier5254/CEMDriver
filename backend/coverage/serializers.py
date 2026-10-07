from rest_framework import serializers

from .models import Cobertura


class CoberturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cobertura
        fields = ['id', 'zona', 'leadtime_dias', 'dias_disponibles', 'hora_inicio', 'hora_fin']
