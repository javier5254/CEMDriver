from rest_framework import serializers

from .models import EVENTOS_WEBHOOK, ApiKey, WebhookDelivery, WebhookEndpoint


class ApiKeyListSerializer(serializers.ModelSerializer):
    """Usado para list/retrieve/update: nunca incluye key_hash ni la llave
    cruda. Solo `activa` es editable (para poder revocar la llave); el
    resto de campos son de solo lectura una vez creada la llave."""

    class Meta:
        model = ApiKey
        fields = ['id', 'nombre', 'prefix', 'actua_como', 'activa', 'creado_en', 'ultimo_uso']
        read_only_fields = ['id', 'nombre', 'prefix', 'actua_como', 'creado_en', 'ultimo_uso']


class ApiKeyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiKey
        fields = ['id', 'nombre', 'actua_como']

    def validate_actua_como(self, usuario):
        if usuario.rol != 'ALISTADOR':
            raise serializers.ValidationError('actua_como debe ser un usuario con rol ALISTADOR.')
        return usuario


class WebhookEndpointListSerializer(serializers.ModelSerializer):
    """Usado en el listado: no incluye `secret` (ver WebhookEndpointDetailSerializer
    para la justificacion de por que si se expone en retrieve/create)."""

    class Meta:
        model = WebhookEndpoint
        fields = ['id', 'nombre', 'url', 'eventos', 'activo', 'creado_en']


class WebhookEndpointDetailSerializer(serializers.ModelSerializer):
    """Usado en create/retrieve/update. Incluye `secret`: a diferencia de
    ApiKey (donde solo se guarda un hash irrecuperable), el secret de un
    webhook debe poder consultarse de nuevo para que el admin configure la
    verificacion de firma en el sistema receptor -- por eso aqui se guarda
    en texto plano y se opta por mostrarlo (el endpoint completo ya esta
    restringido a IsAdmin)."""

    class Meta:
        model = WebhookEndpoint
        fields = ['id', 'nombre', 'url', 'secret', 'eventos', 'activo', 'creado_en']
        read_only_fields = ['secret', 'creado_en']

    def validate_eventos(self, value):
        eventos = [e.strip() for e in value.split(',') if e.strip()]
        if not eventos:
            raise serializers.ValidationError('Debe indicar al menos un evento.')
        invalidos = [e for e in eventos if e not in EVENTOS_WEBHOOK]
        if invalidos:
            raise serializers.ValidationError(
                f'Eventos invalidos: {", ".join(invalidos)}. '
                f'Validos: {", ".join(EVENTOS_WEBHOOK)}.'
            )
        return ','.join(eventos)


class WebhookDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookDelivery
        fields = ['id', 'endpoint', 'evento', 'payload', 'status_code', 'exito', 'error', 'creado_en']
