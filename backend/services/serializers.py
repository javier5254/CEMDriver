from rest_framework import serializers

from accounts.serializers import UsuarioResumenSerializer

from .models import EstadoServicio, Evidencia, MensajeChat, Novedad, Ruta, Servicio, TipoServicio


class RutaSerializer(serializers.ModelSerializer):
    motorizado_detalle = UsuarioResumenSerializer(source='motorizado', read_only=True)

    class Meta:
        model = Ruta
        fields = ['id', 'motorizado', 'motorizado_detalle', 'fecha', 'estado']


class EvidenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidencia
        fields = ['id', 'foto', 'firma', 'capturado_en']


class NovedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novedad
        fields = ['id', 'servicio', 'tipo', 'detalle', 'accion', 'creado_en']
        read_only_fields = ['servicio']


class MensajeChatSerializer(serializers.ModelSerializer):
    autor_detalle = UsuarioResumenSerializer(source='autor', read_only=True)

    class Meta:
        model = MensajeChat
        fields = ['id', 'servicio', 'autor', 'autor_detalle', 'texto', 'enviado_en']
        read_only_fields = ['servicio', 'autor']


class ServicioSerializer(serializers.ModelSerializer):
    cliente_detalle = UsuarioResumenSerializer(source='cliente', read_only=True)
    evidencia = EvidenciaSerializer(read_only=True)
    novedades = NovedadSerializer(many=True, read_only=True)

    class Meta:
        model = Servicio
        fields = [
            'id', 'tipo', 'cliente', 'cliente_detalle',
            'zona', 'direccion_origen', 'direccion_destino', 'fecha_agenda', 'estado',
            'ruta', 'creado_en', 'evidencia', 'novedades',
        ]
        read_only_fields = ['estado', 'creado_en']


class ServicioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = [
            'id', 'tipo', 'cliente', 'zona',
            'direccion_origen', 'direccion_destino', 'fecha_agenda',
        ]

    def validate(self, attrs):
        tipo = attrs.get('tipo')
        if tipo == TipoServicio.ENTREGA and not attrs.get('direccion_destino'):
            raise serializers.ValidationError('direccion_destino es obligatoria para un servicio de ENTREGA.')
        if tipo == TipoServicio.RECOLECCION and not attrs.get('direccion_origen'):
            raise serializers.ValidationError('direccion_origen es obligatoria para un servicio de RECOLECCION.')
        return attrs


class AsignarRutaSerializer(serializers.Serializer):
    ruta_id = serializers.PrimaryKeyRelatedField(queryset=Ruta.objects.all())


class CerrarServicioSerializer(serializers.Serializer):
    foto = serializers.ImageField(required=False)
    firma = serializers.ImageField(required=False)

    def validate(self, attrs):
        servicio: Servicio = self.context['servicio']
        if servicio.tipo == TipoServicio.RECOLECCION:
            if not attrs.get('foto') or not attrs.get('firma'):
                raise serializers.ValidationError(
                    'Un servicio de RECOLECCION requiere foto y firma para poder cerrarse.'
                )
        return attrs


class NovedadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novedad
        fields = ['tipo', 'detalle', 'accion']


class PlanificarRecoleccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'zona', 'direccion_origen', 'fecha_agenda']
