from rest_framework import serializers

from .models import Pago


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = [
            'id', 'cliente', 'servicio', 'producto', 'monto', 'estado',
            'proveedor', 'referencia', 'creado_en', 'actualizado_en',
        ]
        read_only_fields = fields
