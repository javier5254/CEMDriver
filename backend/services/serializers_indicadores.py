"""Serializadores de GET /api/indicadores/.

Los parametros de consulta se validan con IndicadoresParametrosSerializer. Los
demas serializadores solo describen la respuesta para la documentacion OpenAPI
(drf-spectacular); el JSON real lo arma services/indicadores.py.
"""
from rest_framework import serializers


class IndicadoresParametrosSerializer(serializers.Serializer):
    dias = serializers.IntegerField(
        required=False, default=30, min_value=1, max_value=365,
        help_text='Tamaño del periodo en días (1 a 365). El día actual cuenta como el último.',
        error_messages={
            'invalid': 'dias debe ser un número entero entre 1 y 365.',
            'min_value': 'dias debe ser un número entero entre 1 y 365.',
            'max_value': 'dias debe ser un número entero entre 1 y 365.',
        },
    )
    zona = serializers.CharField(
        required=False, allow_blank=True,
        help_text='Texto exacto de Servicio.zona para filtrar los indicadores (opcional).',
    )


class PeriodoSerializer(serializers.Serializer):
    dias = serializers.IntegerField()
    desde = serializers.DateField()
    hasta = serializers.DateField()
    zona = serializers.CharField(allow_null=True)


class ResumenSerializer(serializers.Serializer):
    servicios_total = serializers.IntegerField()
    entregas = serializers.IntegerField()
    recolecciones = serializers.IntegerField()
    en_curso = serializers.IntegerField()
    cerrados_exitosos = serializers.IntegerField()
    devueltos = serializers.IntegerField()
    tasa_exito = serializers.FloatField(allow_null=True)
    servicios_con_novedad = serializers.IntegerField()
    tasa_novedad = serializers.FloatField(allow_null=True)


class PorEstadoSerializer(serializers.Serializer):
    estado = serializers.CharField()
    etiqueta = serializers.CharField()
    total = serializers.IntegerField()


class SerieDiariaSerializer(serializers.Serializer):
    fecha = serializers.DateField()
    entregas = serializers.IntegerField()
    recolecciones = serializers.IntegerField()


class PorZonaSerializer(serializers.Serializer):
    zona = serializers.CharField()
    total = serializers.IntegerField()
    exitosos = serializers.IntegerField()
    con_novedad = serializers.IntegerField()


class NovedadPorTipoSerializer(serializers.Serializer):
    tipo = serializers.CharField()
    total = serializers.IntegerField()


class NovedadPorAccionSerializer(serializers.Serializer):
    accion = serializers.CharField()
    etiqueta = serializers.CharField()
    total = serializers.IntegerField()


class NovedadesIndicadorSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    por_tipo = NovedadPorTipoSerializer(many=True)
    por_accion = NovedadPorAccionSerializer(many=True)


class EvidenciaIndicadorSerializer(serializers.Serializer):
    recolecciones_cerradas = serializers.IntegerField()
    con_evidencia_completa = serializers.IntegerField()
    porcentaje = serializers.FloatField(
        allow_null=True, help_text='Proporción entre 0 y 1 (como las demás tasas), no un valor de 0 a 100.',
    )
    horas_promedio_a_cierre = serializers.FloatField(allow_null=True)


class MotorizadoIndicadorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    servicios = serializers.IntegerField()
    cerrados_exitosos = serializers.IntegerField()
    con_novedad = serializers.IntegerField()


class OperacionSerializer(serializers.Serializer):
    rutas = serializers.IntegerField()
    sin_asignar = serializers.IntegerField()
    posiciones_gps = serializers.IntegerField()
    mensajes_chat = serializers.IntegerField()


class EnviosWebhookSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    exitosos = serializers.IntegerField()
    fallidos = serializers.IntegerField()
    tasa_exito = serializers.FloatField(allow_null=True)


class IntegracionesSerializer(serializers.Serializer):
    api_keys_activas = serializers.IntegerField()
    webhooks_activos = serializers.IntegerField()
    envios_webhook = EnviosWebhookSerializer()


class IndicadoresRespuestaSerializer(serializers.Serializer):
    generado_en = serializers.DateTimeField()
    periodo = PeriodoSerializer()
    resumen = ResumenSerializer()
    por_estado = PorEstadoSerializer(many=True)
    serie_diaria = SerieDiariaSerializer(many=True)
    por_zona = PorZonaSerializer(many=True)
    novedades = NovedadesIndicadorSerializer()
    evidencia = EvidenciaIndicadorSerializer()
    motorizados = MotorizadoIndicadorSerializer(many=True)
    operacion = OperacionSerializer()
    integraciones = IntegracionesSerializer()
