"""Calculo de indicadores operativos de CMEDriver (RF-30).

Todas las cifras salen de agregaciones del ORM sobre la base de datos real:
no hay valores precalculados ni inventados. Si un dato no se puede calcular
(por ejemplo una tasa con denominador cero) se devuelve None.

El resultado es un diccionario serializable a JSON con un contrato fijo,
consumido por el endpoint GET /api/indicadores/, por el comando
`exportar_indicadores` y por el dashboard del frontend.
"""
import datetime

from django.db.models import Avg, Count, DurationField, Exists, ExpressionWrapper, F, OuterRef, Q
from django.db.models.functions import TruncDate
from django.utils import timezone

from integrations.models import ApiKey, WebhookDelivery, WebhookEndpoint
from tracking.models import PosicionGPS

from .models import EstadoServicio, MensajeChat, Novedad, Ruta, Servicio, TipoServicio

# Orden fijo y etiquetas legibles de los 8 estados del servicio.
ESTADOS_ORDENADOS = (
    (EstadoServicio.CREADO, 'Creado'),
    (EstadoServicio.ASIGNADO, 'Asignado a ruta'),
    (EstadoServicio.RECIBIDO_CENTRO, 'Recibido en centro'),
    (EstadoServicio.EN_TRANSITO, 'En tránsito'),
    (EstadoServicio.NOVEDAD, 'Con novedad'),
    (EstadoServicio.ENTREGADO, 'Entregado'),
    (EstadoServicio.RECOLECTADO, 'Recolectado'),
    (EstadoServicio.DEVUELTO, 'Devuelto al centro'),
)

ESTADOS_EN_CURSO = (
    EstadoServicio.CREADO,
    EstadoServicio.ASIGNADO,
    EstadoServicio.RECIBIDO_CENTRO,
    EstadoServicio.EN_TRANSITO,
    EstadoServicio.NOVEDAD,
)
ESTADOS_EXITOSOS = (EstadoServicio.ENTREGADO, EstadoServicio.RECOLECTADO)

ACCIONES_NOVEDAD = (
    (Novedad.Accion.REINTENTAR, 'Reintentar'),
    (Novedad.Accion.DEVOLVER, 'Devolver a centro'),
)

# Novedad.tipo es texto libre; la app del motorizado guarda estos codigos.
# Se muestran con una etiqueta legible; un tipo desconocido se devuelve tal cual.
ETIQUETAS_TIPO_NOVEDAD = {
    'CLIENTE_AUSENTE': 'Cliente ausente',
    'DIRECCION_ERRADA': 'Dirección errada',
    'RECHAZO': 'Rechazo del destinatario',
    'ACCESO_RESTRINGIDO': 'Acceso restringido',
    'PAQUETE_DANADO': 'Paquete dañado',
    'OTRO': 'Otro',
}

PRECISION_TASAS = 4


def _tasa(numerador, denominador):
    """Proporcion 0..1 redondeada, o None si el denominador es cero."""
    if not denominador:
        return None
    return round(numerador / denominador, PRECISION_TASAS)


def _inicio_de_dia(fecha):
    return timezone.make_aware(datetime.datetime.combine(fecha, datetime.time.min))


def _periodo(dias, ahora):
    """(desde, hasta, inicio, fin): fechas locales y limites [inicio, fin) del periodo."""
    if timezone.is_naive(ahora):
        ahora = timezone.make_aware(ahora)
    hasta = timezone.localtime(ahora).date()
    desde = hasta - datetime.timedelta(days=dias - 1)
    return desde, hasta, _inicio_de_dia(desde), _inicio_de_dia(hasta + datetime.timedelta(days=1))


def _filtro_servicio(inicio, fin, zona, prefijo=''):
    """Filtros de Servicio (periodo por creado_en y zona) aplicables tambien a
    modelos relacionados mediante `prefijo` (p. ej. 'servicio__')."""
    filtros = {f'{prefijo}creado_en__gte': inicio, f'{prefijo}creado_en__lt': fin}
    if zona:
        filtros[f'{prefijo}zona'] = zona
    return filtros


def _resumen(por_estado, por_tipo, servicios_con_novedad):
    total = sum(por_estado.values())
    exitosos = sum(por_estado.get(e, 0) for e in ESTADOS_EXITOSOS)
    devueltos = por_estado.get(EstadoServicio.DEVUELTO, 0)
    return {
        'servicios_total': total,
        'entregas': por_tipo.get(TipoServicio.ENTREGA, 0),
        'recolecciones': por_tipo.get(TipoServicio.RECOLECCION, 0),
        'en_curso': sum(por_estado.get(e, 0) for e in ESTADOS_EN_CURSO),
        'cerrados_exitosos': exitosos,
        'devueltos': devueltos,
        'tasa_exito': _tasa(exitosos, exitosos + devueltos),
        'servicios_con_novedad': servicios_con_novedad,
        'tasa_novedad': _tasa(servicios_con_novedad, total),
    }


def _serie_diaria(servicios, desde, hasta):
    filas = (
        servicios.annotate(dia=TruncDate('creado_en', tzinfo=timezone.get_current_timezone()))
        .order_by()
        .values('dia', 'tipo')
        .annotate(total=Count('id'))
    )
    conteo = {(f['dia'], f['tipo']): f['total'] for f in filas}
    serie = []
    for desplazamiento in range((hasta - desde).days + 1):
        dia = desde + datetime.timedelta(days=desplazamiento)
        serie.append({
            'fecha': dia.isoformat(),
            'entregas': conteo.get((dia, TipoServicio.ENTREGA), 0),
            'recolecciones': conteo.get((dia, TipoServicio.RECOLECCION), 0),
        })
    return serie


def _por_zona(servicios, con_novedad):
    novedades_por_zona = dict(
        con_novedad.order_by().values_list('zona').annotate(total=Count('id')),
    )
    filas = (
        servicios.order_by()
        .values('zona')
        .annotate(
            total=Count('id'),
            exitosos=Count('id', filter=Q(estado__in=ESTADOS_EXITOSOS)),
        )
    )
    zonas = [
        {
            'zona': f['zona'],
            'total': f['total'],
            'exitosos': f['exitosos'],
            'con_novedad': novedades_por_zona.get(f['zona'], 0),
        }
        for f in filas
    ]
    zonas.sort(key=lambda z: (-z['total'], z['zona']))
    return zonas


def _novedades(inicio, fin, zona):
    novedades = Novedad.objects.filter(**_filtro_servicio(inicio, fin, zona, 'servicio__'))
    por_tipo_crudo = novedades.order_by().values_list('tipo').annotate(total=Count('id'))
    por_tipo = {}
    for tipo, total in por_tipo_crudo:
        etiqueta = ETIQUETAS_TIPO_NOVEDAD.get(tipo, tipo)
        por_tipo[etiqueta] = por_tipo.get(etiqueta, 0) + total
    por_accion = dict(novedades.order_by().values_list('accion').annotate(total=Count('id')))
    return {
        'total': sum(por_tipo.values()),
        'por_tipo': [
            {'tipo': tipo, 'total': total}
            for tipo, total in sorted(por_tipo.items(), key=lambda t: (-t[1], t[0]))
        ],
        'por_accion': [
            {'accion': accion, 'etiqueta': etiqueta, 'total': por_accion.get(accion, 0)}
            for accion, etiqueta in ACCIONES_NOVEDAD
        ],
    }


def _evidencia(servicios):
    # Una evidencia es completa cuando tiene foto Y firma (RF-12).
    completa = (
        Q(evidencia__foto__isnull=False) & ~Q(evidencia__foto='')
        & Q(evidencia__firma__isnull=False) & ~Q(evidencia__firma='')
    )
    datos = servicios.filter(estado=EstadoServicio.RECOLECTADO).order_by().aggregate(
        cerradas=Count('id'),
        completas=Count('id', filter=completa),
        duracion=Avg(ExpressionWrapper(
            F('evidencia__capturado_en') - F('creado_en'), output_field=DurationField(),
        )),
    )
    cerradas = datos['cerradas']
    return {
        'recolecciones_cerradas': cerradas,
        'con_evidencia_completa': datos['completas'],
        'porcentaje': _tasa(datos['completas'], cerradas),  # proporcion 0..1, como las demas tasas
        'horas_promedio_a_cierre': (
            round(datos['duracion'].total_seconds() / 3600, 2) if datos['duracion'] is not None else None
        ),
    }


def _motorizados(servicios, con_novedad):
    campo = 'ruta__motorizado'
    novedades_por_moto = dict(
        con_novedad.order_by().filter(ruta__motorizado__isnull=False)
        .values_list(campo).annotate(total=Count('id')),
    )
    filas = (
        servicios.filter(ruta__motorizado__isnull=False).order_by()
        .values(campo, f'{campo}__nombre', f'{campo}__username')
        .annotate(
            total=Count('id'),
            exitosos=Count('id', filter=Q(estado__in=ESTADOS_EXITOSOS)),
        )
    )
    motorizados = [
        {
            'id': f[campo],
            'nombre': f[f'{campo}__nombre'] or f[f'{campo}__username'],
            'servicios': f['total'],
            'cerrados_exitosos': f['exitosos'],
            'con_novedad': novedades_por_moto.get(f[campo], 0),
        }
        for f in filas
    ]
    motorizados.sort(key=lambda m: (-m['servicios'], m['nombre'], m['id']))
    return motorizados


def _operacion(desde, hasta, inicio, fin, zona, sin_asignar):
    rutas = Ruta.objects.filter(fecha__gte=desde, fecha__lte=hasta)
    posiciones = PosicionGPS.objects.filter(timestamp__gte=inicio, timestamp__lt=fin)
    mensajes = MensajeChat.objects.filter(enviado_en__gte=inicio, enviado_en__lt=fin)
    if zona:
        # Las rutas no tienen zona propia: se cuentan las que llevan servicios de la zona.
        rutas = rutas.filter(servicios__zona=zona).distinct()
        posiciones = posiciones.filter(servicio__zona=zona)
        mensajes = mensajes.filter(servicio__zona=zona)
    return {
        'rutas': rutas.count(),
        'sin_asignar': sin_asignar,
        'posiciones_gps': posiciones.count(),
        'mensajes_chat': mensajes.count(),
    }


def _integraciones(inicio, fin):
    envios = WebhookDelivery.objects.filter(creado_en__gte=inicio, creado_en__lt=fin).aggregate(
        total=Count('id'), exitosos=Count('id', filter=Q(exito=True)),
    )
    return {
        'api_keys_activas': ApiKey.objects.filter(activa=True).count(),
        'webhooks_activos': WebhookEndpoint.objects.filter(activo=True).count(),
        'envios_webhook': {
            'total': envios['total'],
            'exitosos': envios['exitosos'],
            'fallidos': envios['total'] - envios['exitosos'],
            'tasa_exito': _tasa(envios['exitosos'], envios['total']),
        },
    }


def calcular_indicadores(dias=30, zona=None, ahora=None):
    """Calcula los indicadores operativos de los ultimos `dias` dias.

    - `dias`: tamano del periodo (el dia actual cuenta como el ultimo). El
      periodo se mide en fecha local del servidor (settings.TIME_ZONE) sobre
      Servicio.creado_en.
    - `zona`: texto exacto de Servicio.zona para filtrar (opcional).
    - `ahora`: instante de referencia (por defecto, el actual); permite pruebas
      deterministas.

    Los indicadores de integraciones (API keys y webhooks) son globales: no se
    filtran por zona.
    """
    ahora = ahora or timezone.now()
    desde, hasta, inicio, fin = _periodo(dias, ahora)

    servicios = Servicio.objects.filter(**_filtro_servicio(inicio, fin, zona))
    por_estado = dict(servicios.order_by().values_list('estado').annotate(total=Count('id')))
    por_tipo = dict(servicios.order_by().values_list('tipo').annotate(total=Count('id')))

    con_novedad = servicios.filter(Exists(Novedad.objects.filter(servicio=OuterRef('pk'))))
    servicios_con_novedad = con_novedad.count()

    return {
        'generado_en': timezone.localtime(ahora).isoformat(),
        'periodo': {
            'dias': dias,
            'desde': desde.isoformat(),
            'hasta': hasta.isoformat(),
            'zona': zona or None,
        },
        'resumen': _resumen(por_estado, por_tipo, servicios_con_novedad),
        'por_estado': [
            {'estado': estado, 'etiqueta': etiqueta, 'total': por_estado.get(estado, 0)}
            for estado, etiqueta in ESTADOS_ORDENADOS
        ],
        'serie_diaria': _serie_diaria(servicios, desde, hasta),
        'por_zona': _por_zona(servicios, con_novedad),
        'novedades': _novedades(inicio, fin, zona),
        'evidencia': _evidencia(servicios),
        'motorizados': _motorizados(servicios, con_novedad),
        'operacion': _operacion(
            desde, hasta, inicio, fin, zona, por_estado.get(EstadoServicio.CREADO, 0),
        ),
        'integraciones': _integraciones(inicio, fin),
    }
