from rest_framework import serializers

from .models import MensajeBot


class MensajeBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeBot
        fields = ['id', 'conversacion', 'autor', 'texto', 'function_call', 'creado_en']
        read_only_fields = fields
