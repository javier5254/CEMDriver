"""Datos de demostración realistas y reproducibles para el dashboard de indicadores.

Simula ~2 meses de operación de una mensajería en Bogotá: usuarios, zonas de
cobertura, servicios con estados coherentes con la máquina de estados del
sistema, rutas, novedades, evidencias (foto y firma), posiciones GPS, chat y
envíos de webhooks. Todo se marca como demo (usuarios `demo_*`, nombres
`[DEMO]`) para poder borrarlo con --reset sin tocar datos reales.

IMPORTANTE: son datos de DEMOSTRACIÓN generados con una semilla; no
corresponden a operaciones reales de Logytech Mobile. Las cuentas demo usan
una contraseña conocida y solo sirven para desarrollo local.
"""
import datetime
import io
import math
import random
from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont

from accounts.models import Usuario
from coverage.models import Cobertura
from coverage.views import DIAS_ORDEN
from integrations.models import EVENTOS_WEBHOOK, ApiKey, WebhookDelivery, WebhookEndpoint
from services.models import (
    EstadoRuta,
    EstadoServicio,
    Evidencia,
    MensajeChat,
    Novedad,
    Ruta,
    Servicio,
    TipoServicio,
)
from tracking.models import PosicionGPS

PREFIJO_DEMO = 'demo_'
MARCA_DEMO = '[DEMO]'
PASSWORD_DEMO = 'demo1234'  # solo desarrollo: cuentas de demostración

# Punto de partida ficticio de los motorizados (zona de Puente Aranda).
DEPOSITO = (4.6290, -74.1040)

ZONAS = (
    {'nombre': 'Bogota - Chapinero', 'leadtime': 1, 'dias': 'LUN,MAR,MIE,JUE,VIE', 'peso': 24,
     'centro': (4.6533, -74.0640), 'calles': (53, 72), 'carreras': (5, 15), 'sufijo': ''},
    {'nombre': 'Bogota - Suba', 'leadtime': 2, 'dias': 'LUN,MIE,VIE', 'peso': 20,
     'centro': (4.7410, -74.0830), 'calles': (127, 150), 'carreras': (55, 100), 'sufijo': ''},
    {'nombre': 'Bogota - Usaquen', 'leadtime': 1, 'dias': 'LUN,MAR,MIE,JUE,VIE', 'peso': 17,
     'centro': (4.6950, -74.0300), 'calles': (100, 140), 'carreras': (5, 19), 'sufijo': ''},
    {'nombre': 'Bogota - Teusaquillo', 'leadtime': 1, 'dias': 'LUN,MAR,MIE,JUE,VIE,SAB', 'peso': 14,
     'centro': (4.6360, -74.0800), 'calles': (34, 53), 'carreras': (13, 30), 'sufijo': ''},
    {'nombre': 'Bogota - Fontibon', 'leadtime': 2, 'dias': 'LUN,MIE,VIE', 'peso': 13,
     'centro': (4.6700, -74.1450), 'calles': (17, 26), 'carreras': (96, 120), 'sufijo': ''},
    {'nombre': 'Bogota - Kennedy', 'leadtime': 2, 'dias': 'MAR,JUE,SAB', 'peso': 12,
     'centro': (4.6270, -74.1560), 'calles': (36, 48), 'carreras': (68, 86), 'sufijo': ' Sur'},
)
# Las dos zonas de seed_data se crean con los mismos valores si no existen.
ZONAS_BASE = ('Bogota - Chapinero', 'Bogota - Suba')

COMPLEMENTOS = ('', '', '', 'Apto 502', 'Apto 301', 'Oficina 704', 'Local 12', 'Torre 2 Apto 1104',
                'Casa 3', 'Bodega 5', 'Piso 2', 'Interior 4')

MOTORIZADOS = (
    ('demo_moto1', 'Andrés Felipe Rojas', 32),
    ('demo_moto2', 'Jhon Alexander Gómez', 27),
    ('demo_moto3', 'Wilmer Eduardo Cárdenas', 23),
    ('demo_moto4', 'Diego Armando Parra', 18),
)
CLIENTES = (
    ('demo_cliente1', 'Camila Andrea Vargas', 22),
    ('demo_cliente2', 'Juan Sebastián Ortiz', 18),
    ('demo_cliente3', 'Laura Valentina Pardo', 15),
    ('demo_cliente4', 'Carlos Eduardo Herrera', 12),
    ('demo_cliente5', 'Daniela Rincón Mejía', 10),
    ('demo_cliente6', 'Santiago Quintero', 9),
    ('demo_cliente7', 'Paola Andrea Castaño', 8),
    ('demo_cliente8', 'Felipe Cárdenas Duarte', 6),
)

# Volumen relativo por día de la semana (lunes=0): más entre semana.
PESO_SEMANA = (1.0, 1.1, 1.1, 1.05, 1.0, 0.45, 0.08)

ESTADOS_ABIERTOS_HOY = (
    (EstadoServicio.CREADO, 10),
    (EstadoServicio.ASIGNADO, 22),
    (EstadoServicio.RECIBIDO_CENTRO, 25),
    (EstadoServicio.EN_TRANSITO, 43),
)
ESTADOS_ABIERTOS_ANTES = (
    (EstadoServicio.ASIGNADO, 55),
    (EstadoServicio.RECIBIDO_CENTRO, 30),
    (EstadoServicio.EN_TRANSITO, 15),
)
# Probabilidad de que un servicio con agenda hace N días siga abierto.
PROB_ABIERTO_POR_EDAD = {0: 1.0, 1: 0.6, 2: 0.2}
# Destino de los servicios ya resueltos (el resto se cierra con éxito): cuotas sobre ese grupo.
PROP_DEVUELTOS = 0.065
PROP_NOVEDAD_ABIERTA = 0.04
PROP_REZAGADOS = 0.07

# Tipos de novedad: los códigos son los que guarda la app del motorizado.
NOVEDAD_REINTENTAR = (
    ('CLIENTE_AUSENTE', 50), ('ACCESO_RESTRINGIDO', 25), ('DIRECCION_ERRADA', 25),
)
NOVEDAD_DEVOLVER = {
    TipoServicio.ENTREGA: (
        ('DIRECCION_ERRADA', 28), ('RECHAZO', 30), ('PAQUETE_DANADO', 18), ('CLIENTE_AUSENTE', 24),
    ),
    TipoServicio.RECOLECCION: (
        ('DIRECCION_ERRADA', 35), ('PAQUETE_DANADO', 25), ('CLIENTE_AUSENTE', 25), ('ACCESO_RESTRINGIDO', 15),
    ),
}
DETALLES_NOVEDAD = {
    'CLIENTE_AUSENTE': (
        'No hay nadie en la dirección y el cliente no contesta el teléfono.',
        'La portería informa que el cliente salió; se intentó llamar sin respuesta.',
        'Se esperó 15 minutos en la dirección sin que nadie atendiera.',
    ),
    'DIRECCION_ERRADA': (
        'La nomenclatura indicada no existe en el barrio.',
        'La dirección corresponde a otra localidad y el cliente no confirma la correcta.',
        'No se encontró el predio con los datos del servicio.',
    ),
    'RECHAZO': (
        'El destinatario no reconoce el pedido y lo rechaza.',
        'El destinatario rechaza el envío por la demora en la entrega.',
    ),
    'ACCESO_RESTRINGIDO': (
        'La administración del conjunto no autoriza el ingreso sin pre-registro.',
        'Vía cerrada por obra: no hay acceso a la dirección.',
    ),
    'PAQUETE_DANADO': (
        'El empaque presenta golpes visibles y no se puede continuar el servicio.',
        'El paquete llegó húmedo al punto de entrega.',
    ),
}

GUIONES_NORMALES = {
    TipoServicio.ENTREGA: (
        (
            (True, 'Buen día, soy {m}, llevo su pedido. Estoy a unos 15 minutos de la dirección.'),
            (False, 'Hola, gracias por avisar. Si no alcanzo a bajar lo recibe la portería.'),
            (True, 'Perfecto, ya estoy llegando.'),
        ),
        (
            (True, 'Hola {c}, voy en camino con su entrega. ¿Hay alguien para recibir?'),
            (False, 'Sí, estoy en casa. Es el apartamento del segundo piso.'),
            (True, 'Listo, llego en 10 minutos.'),
            (False, 'Gracias, quedo atento.'),
        ),
    ),
    TipoServicio.RECOLECCION: (
        (
            (True, 'Buen día, voy a recoger su paquete. ¿Me confirma que ya está listo?'),
            (False, 'Sí, ya está empacado y rotulado. Se lo entrego en la recepción.'),
            (True, 'Gracias. Estoy por la zona, llego en 10 minutos.'),
        ),
        (
            (True, 'Hola, soy {m} de CMEDriver. Paso por el paquete a la dirección del servicio.'),
            (False, 'Hola, claro. Pregunte por {c} en la entrada.'),
            (True, 'Listo, ya casi llego.'),
        ),
    ),
}
GUIONES_NOVEDAD = (
    (
        (True, 'Estoy en la dirección y nadie me atiende. ¿Se encuentra?'),
        (False, 'Estoy saliendo de una reunión, ¿puede esperar unos 20 minutos?'),
        (True, 'Puedo reintentar más tarde dentro de la ruta; avíseme si hay alguien.'),
    ),
    (
        (True, 'La dirección no aparece en el sector. ¿Me envía una referencia?'),
        (False, 'Es diagonal al parque principal, hay un portón gris.'),
        (True, 'Gracias, ya registro la novedad en la app.'),
    ),
)

ERRORES_WEBHOOK = (
    (500, 'HTTPError 500: Internal Server Error'),
    (502, 'HTTPError 502: Bad Gateway'),
    (503, 'HTTPError 503: Service Unavailable'),
    (504, 'HTTPError 504: Gateway Time-out'),
    (None, 'TimeoutError: timed out'),
    (None, 'URLError: <urlopen error [Errno 111] Connection refused>'),
)
PROB_EXITO_WEBHOOK = 0.945


@dataclass
class PlanServicio:
    """Servicio planificado en memoria antes de persistirlo."""

    tipo: str
    cliente: Usuario
    zona: dict
    direccion: str
    creado: datetime.datetime
    fecha_agenda: datetime.date
    estado: str
    novedades: list = field(default_factory=list)  # (tipo, accion, detalle, momento)
    t_asignacion: datetime.datetime | None = None
    t_cierre: datetime.datetime | None = None
    moto: Usuario | None = None
    ruta: Ruta | None = None
    servicio: Servicio | None = None


def elegir(rng, pares):
    """Elección ponderada sobre una secuencia de (valor, peso)."""
    return rng.choices([v for v, _ in pares], weights=[p for _, p in pares])[0]


class Command(BaseCommand):
    help = (
        'Carga datos de demostración (usuarios demo_*, servicios, rutas, novedades, evidencias, GPS, '
        'chat y webhooks) para el dashboard de indicadores. Reproducible con --semilla.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--dias', type=int, default=60, help='Días de operación a simular (por defecto 60).')
        parser.add_argument('--servicios', type=int, default=240, help='Cantidad de servicios (por defecto 240).')
        parser.add_argument('--semilla', type=int, default=2026, help='Semilla del generador (por defecto 2026).')
        parser.add_argument(
            '--reset', action='store_true',
            help='Borra solo lo creado por seed_demo (usuarios demo_*, [DEMO]) y lo recrea.',
        )

    def handle(self, *args, **opciones):
        dias, cantidad = opciones['dias'], opciones['servicios']
        if not 1 <= dias <= 365:
            raise CommandError('--dias debe estar entre 1 y 365.')
        if cantidad < 1:
            raise CommandError('--servicios debe ser un entero positivo.')

        if opciones['reset']:
            with transaction.atomic():
                self._borrar_demo()
            self.stdout.write('Datos demo anteriores eliminados.')
        elif Usuario.objects.filter(username__startswith=PREFIJO_DEMO).exists():
            self.stdout.write(self.style.WARNING(
                'Ya existen datos de demostración (usuarios demo_*). No se hizo ningún cambio; '
                'use --reset para borrarlos y recrearlos.'
            ))
            return

        ahora = timezone.now().replace(microsecond=0)
        with transaction.atomic():
            resumen = self._crear_demo(opciones['semilla'], dias, cantidad, ahora)
        self._imprimir_resumen(resumen, dias)

    # ------------------------------------------------------------------ reset

    def _borrar_demo(self):
        servicios = Servicio.objects.filter(cliente__username__startswith=PREFIJO_DEMO)
        for evidencia in Evidencia.objects.filter(servicio__in=servicios):
            if evidencia.foto:
                evidencia.foto.delete(save=False)
            if evidencia.firma:
                evidencia.firma.delete(save=False)
        servicios.delete()  # en cascada: evidencia, novedades, chat, GPS, puntos geocodificados
        Ruta.objects.filter(motorizado__username__startswith=PREFIJO_DEMO).delete()
        ApiKey.objects.filter(nombre__startswith=MARCA_DEMO).delete()
        WebhookEndpoint.objects.filter(nombre__startswith=MARCA_DEMO).delete()
        # Las coberturas se conservan: son configuración inofensiva y no llevan marca demo.
        Usuario.objects.filter(username__startswith=PREFIJO_DEMO).delete()

    # --------------------------------------------------------------- creación

    def _crear_demo(self, semilla, dias, cantidad, ahora):
        # Un generador por componente, derivado de la semilla: los datos de cada parte no
        # dependen de cuántos números aleatorios consumió otra (p. ej. según la hora).
        def generador(nombre):
            return random.Random(f'{semilla}:{nombre}')

        hoy = timezone.localdate(ahora)
        self._crear_cobertura()
        usuarios = self._crear_usuarios(generador('usuarios'))
        planes = self._planificar(generador('servicios'), dias, cantidad, ahora, hoy, usuarios)
        self._asignar_rutas(generador('rutas'), planes, usuarios['motos'], hoy)
        self._persistir_servicios(planes, usuarios['alistador'])
        self._persistir_novedades(planes)
        n_evidencias = self._persistir_evidencias(generador('evidencias'), planes)
        n_posiciones = self._persistir_gps(generador('gps'), planes, ahora, hoy)
        n_mensajes = self._persistir_chat(generador('chat'), planes, ahora, hoy)
        webhook = self._persistir_integraciones(generador('webhooks'), planes, usuarios['alistador'], dias, ahora)
        return {
            'usuarios': usuarios,
            'planes': planes,
            'evidencias': n_evidencias,
            'posiciones': n_posiciones,
            'mensajes': n_mensajes,
            'webhook': webhook,
        }

    def _crear_cobertura(self):
        for zona in ZONAS:
            Cobertura.objects.get_or_create(
                zona=zona['nombre'],
                defaults={'leadtime_dias': zona['leadtime'], 'dias_disponibles': zona['dias']},
            )

    def _crear_usuarios(self, rng):
        clave = make_password(PASSWORD_DEMO)  # un solo hash: el hasheo real es lento

        def crear(username, nombre, rol):
            telefono = f'3{rng.choice([0, 1, 2])}{rng.randint(0, 9)}{rng.randint(1000000, 9999999)}'
            return Usuario.objects.create(
                username=username, nombre=nombre, rol=rol, telefono=telefono,
                email=f'{username}@demo.cmedriver.local', password=clave,
            )

        return {
            'admin': crear('demo_admin', 'Marcela Torres (demo)', 'ADMIN'),
            'alistador': crear('demo_alistador1', 'Hernán Beltrán (demo)', 'ALISTADOR'),
            'motos': [crear(u, n, 'MOTORIZADO') for u, n, _ in MOTORIZADOS],
            'clientes': [crear(u, n, 'CLIENTE') for u, n, _ in CLIENTES],
        }

    # ------------------------------------------------------------ planificación

    def _planificar(self, rng, dias, cantidad, ahora, hoy, usuarios):
        dias_lista = [hoy - datetime.timedelta(days=dias - 1 - i) for i in range(dias)]
        pesos_dia = [
            PESO_SEMANA[d.weekday()] * (0.85 + 0.35 * i / max(dias - 1, 1)) * rng.uniform(0.85, 1.15)
            for i, d in enumerate(dias_lista)
        ]
        pesos_cliente = [(c, p) for c, (_, _, p) in zip(usuarios['clientes'], CLIENTES)]
        pesos_zona = [(z, z['peso']) for z in ZONAS]

        planes = []
        for dia, cuantos in zip(dias_lista, self._repartir(cantidad, pesos_dia)):
            for _ in range(cuantos):
                tipo = TipoServicio.ENTREGA if rng.random() < 0.65 else TipoServicio.RECOLECCION
                zona = elegir(rng, pesos_zona)
                cliente = elegir(rng, pesos_cliente)
                creado = self._instante_creacion(rng, dia, ahora)
                agenda = self._fecha_agenda(rng, tipo, dia, zona)
                estado = self._estado_final(rng, tipo, agenda, hoy)
                planes.append(PlanServicio(
                    tipo=tipo, cliente=cliente, zona=zona, direccion=self._direccion(rng, zona),
                    creado=creado, fecha_agenda=agenda, estado=estado,
                ))
        self._repartir_destinos(rng, planes)
        planes.sort(key=lambda p: p.creado)
        self._asegurar_operacion_del_dia(planes, hoy)
        for plan in planes:
            self._completar_historia(rng, plan, ahora)
        return planes

    @staticmethod
    def _asegurar_operacion_del_dia(planes, hoy):
        """Garantiza (si hay servicios agendados para hoy) al menos 2 en EN_TRANSITO y 2 en
        RECIBIDO_CENTRO, para que el tablero muestre todas las etapas intermedias."""
        etapas = ((EstadoServicio.EN_TRANSITO, False), (EstadoServicio.RECIBIDO_CENTRO, True))
        for estado, solo_entregas in etapas:
            existentes = sum(1 for p in planes if p.estado == estado and p.fecha_agenda == hoy)
            candidatos = [
                p for p in reversed(planes)  # los más recientes primero
                if p.fecha_agenda == hoy
                and p.estado in (EstadoServicio.CREADO, EstadoServicio.ASIGNADO)
                and (not solo_entregas or p.tipo == TipoServicio.ENTREGA)
            ]
            for plan in candidatos[:max(0, 2 - existentes)]:
                plan.estado = estado

    @staticmethod
    def _repartir(total, pesos):
        """Reparte `total` en enteros proporcionales a `pesos` (mayor resto)."""
        suma = sum(pesos)
        exactos = [total * p / suma for p in pesos]
        base = [math.floor(x) for x in exactos]
        faltan = total - sum(base)
        for i in sorted(range(len(pesos)), key=lambda i: exactos[i] - base[i], reverse=True)[:faltan]:
            base[i] += 1
        return base

    @staticmethod
    def _aware(dia, hora, minuto=0):
        return timezone.make_aware(datetime.datetime.combine(dia, datetime.time(hora, minuto)))

    def _instante_creacion(self, rng, dia, ahora):
        inicio = self._aware(dia, 7)
        fin = self._aware(dia, 18, 30)
        if fin > ahora:  # el día de hoy: nada de servicios "creados en el futuro"
            medianoche = self._aware(dia, 0)
            fin = max(ahora - datetime.timedelta(minutes=25), medianoche)
            inicio = max(min(inicio, fin - datetime.timedelta(hours=1)), medianoche)
        ventana = max((fin - inicio).total_seconds(), 1)
        segundos = rng.triangular(0, ventana, ventana * 0.4)
        return inicio + datetime.timedelta(seconds=int(segundos))

    @staticmethod
    def _siguiente_dia_valido(fecha, codigos):
        while DIAS_ORDEN[fecha.weekday()] not in codigos:
            fecha += datetime.timedelta(days=1)
        return fecha

    def _fecha_agenda(self, rng, tipo, dia, zona):
        un_dia = datetime.timedelta(days=1)
        if tipo == TipoServicio.RECOLECCION:
            # Mismo criterio que POST /api/servicios/planificar/: leadtime y días válidos de la zona.
            codigos = zona['dias'].split(',')
            fecha = self._siguiente_dia_valido(dia + datetime.timedelta(days=zona['leadtime']), codigos)
            if rng.random() < 0.25:
                fecha = self._siguiente_dia_valido(fecha + un_dia, codigos)
            return fecha
        fecha = dia if rng.random() < 0.7 else dia + un_dia
        return fecha + un_dia if fecha.weekday() == 6 else fecha

    def _estado_final(self, rng, tipo, agenda, hoy):
        """Estado actual del servicio, coherente con el tiempo transcurrido desde su agenda.

        Devuelve None para los servicios ya resueltos: su destino final (cerrado, devuelto,
        con novedad abierta o rezagado) se reparte por cuotas en `_repartir_destinos`."""
        edad = (hoy - agenda).days
        if edad < 0:  # agenda futura: aún sin operar
            return EstadoServicio.CREADO if rng.random() < 0.5 else EstadoServicio.ASIGNADO
        if rng.random() < PROB_ABIERTO_POR_EDAD.get(edad, 0.0):
            estado = elegir(rng, ESTADOS_ABIERTOS_HOY if edad == 0 else ESTADOS_ABIERTOS_ANTES)
            if tipo == TipoServicio.RECOLECCION and estado == EstadoServicio.RECIBIDO_CENTRO:
                return EstadoServicio.ASIGNADO  # la recolección no pasa por el centro al inicio
            return estado
        return None

    @staticmethod
    def _repartir_destinos(rng, planes):
        """Asigna el destino final de los servicios ya resueltos con cuotas fijas (no por
        sorteo individual), para que las proporciones no dependan del azar de la semilla."""
        resueltos = [p for p in planes if p.estado is None]
        cuotas = (
            (EstadoServicio.DEVUELTO, round(len(resueltos) * PROP_DEVUELTOS)),
            (EstadoServicio.NOVEDAD, round(len(resueltos) * PROP_NOVEDAD_ABIERTA)),
            (None, round(len(resueltos) * PROP_REZAGADOS)),  # rezagados: nunca se completaron
        )
        rng.shuffle(resueltos)
        inicio = 0
        for estado, cuota in cuotas:
            for plan in resueltos[inicio:inicio + cuota]:
                plan.estado = estado or (
                    EstadoServicio.CREADO if rng.random() < 0.45 else EstadoServicio.ASIGNADO
                )
            inicio += cuota
        for plan in resueltos[inicio:]:
            plan.estado = EstadoServicio.ENTREGADO if plan.tipo == TipoServicio.ENTREGA else EstadoServicio.RECOLECTADO

    def _direccion(self, rng, zona):
        via, ancho = ('Calle', 'calles') if rng.random() < 0.55 else ('Carrera', 'carreras')
        principal = rng.randint(*zona[ancho])
        cruce = rng.randint(*zona['carreras' if via == 'Calle' else 'calles'])
        sufijo = zona['sufijo'] if via == 'Calle' else ''
        complemento = rng.choice(COMPLEMENTOS)
        texto = f'{via} {principal}{sufijo} # {cruce}-{rng.randint(10, 99)}'
        if complemento:
            texto += f', {complemento}'
        return f'{texto}, Bogota'

    def _momentos(self, rng, dia, minimo, ahora, cantidad):
        """`cantidad` instantes ordenados del día `dia`, posteriores a `minimo` y no futuros."""
        un_minuto = datetime.timedelta(minutes=1)
        inferior = max(minimo + datetime.timedelta(minutes=30), self._aware(dia, 8, 30))
        superior = max(self._aware(dia, 18, 30), inferior + datetime.timedelta(minutes=10))
        superior = min(superior, ahora - un_minuto)
        inferior = min(inferior, superior)
        ventana = int((superior - inferior).total_seconds())
        momentos = sorted(inferior + datetime.timedelta(seconds=rng.randint(0, ventana)) for _ in range(cantidad))
        return [min(max(m, minimo + un_minuto), ahora) for m in momentos]

    def _completar_historia(self, rng, plan, ahora):
        """Novedades, hora de asignación y de cierre acordes al estado final."""
        acciones = []
        if plan.estado == EstadoServicio.DEVUELTO:
            if rng.random() < 0.3:
                acciones.append(Novedad.Accion.REINTENTAR)
            acciones.append(Novedad.Accion.DEVOLVER)
        elif plan.estado == EstadoServicio.NOVEDAD:
            if rng.random() < 0.25:
                acciones.append(Novedad.Accion.REINTENTAR)
            acciones.append(Novedad.Accion.REINTENTAR)
        elif plan.estado in (EstadoServicio.ENTREGADO, EstadoServicio.RECOLECTADO) and rng.random() < 0.07:
            acciones.append(Novedad.Accion.REINTENTAR)  # falló el primer intento y luego se cerró

        cierra = plan.estado in (EstadoServicio.ENTREGADO, EstadoServicio.RECOLECTADO)
        if acciones or cierra:
            momentos = self._momentos(rng, plan.fecha_agenda, plan.creado, ahora, len(acciones) + int(cierra))
            for accion, momento in zip(acciones, momentos):
                if accion == Novedad.Accion.REINTENTAR:
                    tipo = elegir(rng, NOVEDAD_REINTENTAR)
                else:
                    tipo = elegir(rng, NOVEDAD_DEVOLVER[plan.tipo])
                plan.novedades.append((tipo, accion, rng.choice(DETALLES_NOVEDAD[tipo]), momento))
            if cierra:
                plan.t_cierre = momentos[-1]

        if plan.estado != EstadoServicio.CREADO:
            asignacion = plan.creado + datetime.timedelta(minutes=rng.randint(15, 180))
            if plan.novedades:
                asignacion = min(asignacion, plan.novedades[0][3] - datetime.timedelta(minutes=5))
            if plan.t_cierre:
                asignacion = min(asignacion, plan.t_cierre - datetime.timedelta(minutes=5))
            plan.t_asignacion = min(max(asignacion, plan.creado + datetime.timedelta(minutes=5)), ahora)

    # ------------------------------------------------------------------ rutas

    def _asignar_rutas(self, rng, planes, motos, hoy):
        """Una ruta por motorizado y fecha, con los servicios que operan ese día."""
        pesos_moto = {m.id: p for m, (_, _, p) in zip(motos, MOTORIZADOS)}
        por_fecha = {}
        for plan in planes:
            if plan.estado != EstadoServicio.CREADO:
                por_fecha.setdefault(plan.fecha_agenda, []).append(plan)

        for fecha in sorted(por_fecha):
            del_dia = por_fecha[fecha]
            activos_n = min(len(motos), max(1, math.ceil(len(del_dia) / 3)))
            # Muestreo ponderado sin reemplazo (Efraimidis-Spirakis).
            activos = sorted(
                motos, key=lambda m: rng.random() ** (1.0 / pesos_moto[m.id]), reverse=True,
            )[:activos_n]
            pesos = [(m, pesos_moto[m.id]) for m in activos]
            for plan in del_dia:
                plan.moto = elegir(rng, pesos)

            rutas = {}
            for plan in del_dia:
                if plan.moto.id not in rutas:
                    rutas[plan.moto.id] = Ruta.objects.create(
                        motorizado=plan.moto, fecha=fecha, estado=self._estado_ruta(fecha, hoy, del_dia, plan.moto),
                    )
                plan.ruta = rutas[plan.moto.id]

    @staticmethod
    def _estado_ruta(fecha, hoy, del_dia, moto):
        if fecha < hoy:
            return EstadoRuta.FINALIZADA
        if fecha > hoy:
            return EstadoRuta.PLANEADA
        en_marcha = (EstadoServicio.RECIBIDO_CENTRO, EstadoServicio.EN_TRANSITO, EstadoServicio.NOVEDAD)
        if any(p.moto == moto and p.estado in en_marcha for p in del_dia):
            return EstadoRuta.EN_CURSO
        return EstadoRuta.PLANEADA

    # ------------------------------------------------------------ persistencia

    def _persistir_servicios(self, planes, alistador):
        for plan in planes:
            es_entrega = plan.tipo == TipoServicio.ENTREGA
            servicio = Servicio.objects.create(
                tipo=plan.tipo, cliente=plan.cliente, zona=plan.zona['nombre'],
                direccion_origen='' if es_entrega else plan.direccion,
                direccion_destino=plan.direccion if es_entrega else '',
                fecha_agenda=plan.fecha_agenda, estado=plan.estado, ruta=plan.ruta,
                creado_por=alistador if es_entrega else None,
            )
            # creado_en es auto_now_add: se corrige hacia atrás con update().
            Servicio.objects.filter(pk=servicio.pk).update(creado_en=plan.creado)
            plan.servicio = servicio

    def _persistir_novedades(self, planes):
        for plan in planes:
            for tipo, accion, detalle, momento in plan.novedades:
                novedad = Novedad.objects.create(servicio=plan.servicio, tipo=tipo, accion=accion, detalle=detalle)
                Novedad.objects.filter(pk=novedad.pk).update(creado_en=momento)

    def _persistir_evidencias(self, rng, planes):
        recolectadas = [p for p in planes if p.estado == EstadoServicio.RECOLECTADO]
        # Unas pocas con solo foto o solo firma (≈ 5 %) para que el indicador no sea 100 %.
        n_incompletas = 0
        if len(recolectadas) >= 5:
            n_incompletas = max(1 if len(recolectadas) < 12 else 2, round(len(recolectadas) * 0.05))
        incompletas = {id(p): i % 2 for i, p in enumerate(rng.sample(recolectadas, n_incompletas))}

        for plan in recolectadas:
            falta = incompletas.get(id(plan))  # 0: sin firma, 1: sin foto, None: completa
            evidencia = Evidencia(servicio=plan.servicio)
            if falta != 1:
                evidencia.foto.save(
                    f'demo_foto_{plan.servicio.id}.png', ContentFile(self._png(self._imagen_foto(rng, plan.servicio.id))),
                    save=False,
                )
            if falta != 0:
                evidencia.firma.save(
                    f'demo_firma_{plan.servicio.id}.png', ContentFile(self._png(self._imagen_firma(rng))), save=False,
                )
            evidencia.save()
            Evidencia.objects.filter(pk=evidencia.pk).update(capturado_en=plan.t_cierre)
        return len(recolectadas)

    @staticmethod
    def _png(imagen):
        buffer = io.BytesIO()
        imagen.save(buffer, format='PNG', optimize=True)
        return buffer.getvalue()

    @staticmethod
    def _fuente(tamano):
        try:
            return ImageFont.load_default(size=tamano)
        except (TypeError, OSError):
            return ImageFont.load_default()

    def _imagen_foto(self, rng, servicio_id):
        """Foto de demostración: un paquete con etiqueta sobre una mesa."""
        imagen = Image.new('RGB', (480, 320), rng.choice([(226, 232, 240), (231, 229, 222), (222, 236, 232)]))
        dibujo = ImageDraw.Draw(imagen)
        dibujo.rectangle((0, 230, 480, 320), fill=(168, 150, 128))
        x0, y0 = 130 + rng.randint(-20, 20), 80 + rng.randint(-10, 10)
        dibujo.rectangle((x0, y0, x0 + 220, y0 + 150), fill=(196, 154, 108), outline=(140, 104, 64), width=3)
        dibujo.rectangle((x0 + 95, y0, x0 + 125, y0 + 150), fill=(222, 190, 140))
        dibujo.rectangle((x0 + 20, y0 + 40, x0 + 85, y0 + 100), fill='white', outline=(80, 80, 80))
        dibujo.text((x0 + 26, y0 + 50), f'CME #{servicio_id}', fill=(30, 30, 30), font=self._fuente(12))
        dibujo.text((x0 + 26, y0 + 72), 'DEMO', fill=(180, 40, 40), font=self._fuente(14))
        return imagen

    def _imagen_firma(self, rng):
        """Firma de demostración: un trazo suave sobre fondo blanco."""
        imagen = Image.new('RGB', (320, 120), 'white')
        dibujo = ImageDraw.Draw(imagen)
        dibujo.line((16, 98, 304, 98), fill=(200, 200, 200), width=1)
        fase = rng.uniform(0, math.pi)
        puntos = [
            (24 + i * 6, 62 + 26 * math.sin(fase + i * 0.55) * math.exp(-i / 70) + rng.uniform(-5, 5))
            for i in range(46)
        ]
        dibujo.line(puntos, fill=(20, 40, 110), width=2, joint='curve')
        return imagen

    def _persistir_gps(self, rng, planes, ahora, hoy):
        total = 0
        for plan in planes:
            if plan.ruta is None:
                continue
            if plan.estado == EstadoServicio.EN_TRANSITO:
                if plan.fecha_agenda == hoy:
                    fin = ahora - datetime.timedelta(minutes=rng.randint(1, 6))
                else:  # última posición conocida del día de la ruta
                    fin = min(self._aware(plan.fecha_agenda, 17, 30), ahora - datetime.timedelta(minutes=2))
                cantidad, progreso = rng.randint(6, 14), rng.uniform(0.55, 0.95)
            elif (
                plan.t_cierre
                and (hoy - plan.fecha_agenda).days <= 14
                and rng.random() < 0.4
            ):
                fin = plan.t_cierre
                cantidad, progreso = rng.randint(5, 9), 1.0
            else:
                continue

            separacion = datetime.timedelta(minutes=4)
            disponibles = int((fin - (plan.creado + datetime.timedelta(minutes=15))) / separacion) + 1
            cantidad = min(cantidad, disponibles)
            if cantidad < 2:
                continue
            for i, (lat, lng) in enumerate(self._trayectoria(rng, plan.zona, cantidad, progreso)):
                posicion = PosicionGPS.objects.create(servicio=plan.servicio, motorizado=plan.moto, lat=lat, lng=lng)
                PosicionGPS.objects.filter(pk=posicion.pk).update(
                    timestamp=fin - separacion * (cantidad - 1 - i),
                )
                total += 1
        return total

    @staticmethod
    def _trayectoria(rng, zona, cantidad, progreso):
        """Recorrido suave desde el punto de partida hacia la zona de destino."""
        lat0, lng0 = DEPOSITO
        lat1 = zona['centro'][0] + rng.uniform(-0.012, 0.012)
        lng1 = zona['centro'][1] + rng.uniform(-0.012, 0.012)
        fase = rng.uniform(0, math.pi)
        puntos = []
        for i in range(cantidad):
            avance = progreso * (i + 1) / cantidad
            lat = lat0 + (lat1 - lat0) * avance + 0.0012 * math.sin(fase + i * 0.9) + rng.uniform(-0.0002, 0.0002)
            lng = lng0 + (lng1 - lng0) * avance + 0.0012 * math.cos(fase + i * 0.9) + rng.uniform(-0.0002, 0.0002)
            puntos.append((Decimal(f'{lat:.6f}'), Decimal(f'{lng:.6f}')))
        return puntos

    def _persistir_chat(self, rng, planes, ahora, hoy):
        total = 0
        for plan in planes:
            if plan.ruta is None:
                continue
            con_novedad = bool(plan.novedades)
            if plan.estado == EstadoServicio.EN_TRANSITO:
                referencia, probabilidad = ahora - datetime.timedelta(minutes=2), 0.7
                if plan.fecha_agenda != hoy:
                    referencia = min(self._aware(plan.fecha_agenda, 17, 30), referencia)
            elif plan.estado in (EstadoServicio.NOVEDAD, EstadoServicio.DEVUELTO):
                referencia, probabilidad = plan.novedades[-1][3], 0.35
            elif plan.t_cierre and (hoy - plan.fecha_agenda).days <= 21:
                referencia, probabilidad = plan.t_cierre, 0.22
            else:
                continue
            if rng.random() >= probabilidad:
                continue

            if con_novedad:
                guion = rng.choice(GUIONES_NOVEDAD)
            else:
                guion = rng.choice(GUIONES_NORMALES[plan.tipo])
            nombres = {'m': plan.moto.nombre.split()[0], 'c': plan.cliente.nombre.split()[0]}

            inicio = max(referencia - datetime.timedelta(minutes=100), plan.creado + datetime.timedelta(minutes=10))
            fin = referencia - datetime.timedelta(minutes=3)
            if fin <= inicio:
                continue
            ventana = int((fin - inicio).total_seconds())
            momentos = sorted(inicio + datetime.timedelta(seconds=rng.randint(0, ventana)) for _ in guion)
            for (de_moto, texto), momento in zip(guion, momentos):
                mensaje = MensajeChat.objects.create(
                    servicio=plan.servicio,
                    autor=plan.moto if de_moto else plan.cliente,
                    texto=texto.format(**nombres),
                )
                MensajeChat.objects.filter(pk=mensaje.pk).update(enviado_en=momento)
                total += 1
        return total

    def _persistir_integraciones(self, rng, planes, alistador, dias, ahora):
        inicio_periodo = ahora - datetime.timedelta(days=dias)
        llave, llave_cruda = ApiKey.generar(f'{MARCA_DEMO} Tienda en línea (demo)', actua_como=alistador)
        ApiKey.objects.filter(pk=llave.pk).update(
            creado_en=inicio_periodo, ultimo_uso=ahora - datetime.timedelta(hours=3),
        )
        # Puerto 9 (discard) en localhost: si alguien opera con la app mientras el webhook
        # demo está activo, la conexión se rechaza al instante en vez de esperar un timeout.
        endpoint = WebhookEndpoint.objects.create(
            nombre=f'{MARCA_DEMO} ERP de la tienda (demo)',
            url='http://127.0.0.1:9/cmedriver-demo/webhook',
            eventos=','.join(EVENTOS_WEBHOOK),
        )
        WebhookEndpoint.objects.filter(pk=endpoint.pk).update(creado_en=inicio_periodo)

        exitosos = fallidos = 0
        for plan in planes:
            for evento, estado, momento in self._eventos_webhook(plan):
                exito = rng.random() < PROB_EXITO_WEBHOOK
                if exito:
                    status_code, error = rng.choice([200, 200, 200, 200, 202, 204]), ''
                else:
                    status_code, error = rng.choice(ERRORES_WEBHOOK)
                payload = {
                    'id': plan.servicio.id, 'tipo': plan.tipo, 'cliente': plan.cliente.id,
                    'zona': plan.zona['nombre'], 'estado': estado, 'fecha_agenda': plan.fecha_agenda.isoformat(),
                }
                entrega = WebhookDelivery.objects.create(
                    endpoint=endpoint, evento=evento, payload=payload,
                    status_code=status_code, exito=exito, error=error,
                )
                WebhookDelivery.objects.filter(pk=entrega.pk).update(
                    creado_en=min(momento + datetime.timedelta(seconds=rng.randint(1, 4)), ahora),
                )
                exitosos += exito
                fallidos += not exito
        return {'llave': llave_cruda, 'exitosos': exitosos, 'fallidos': fallidos}

    @staticmethod
    def _eventos_webhook(plan):
        """(evento, estado en ese momento, instante) que habría emitido el sistema."""
        eventos = [('servicio.creado', EstadoServicio.CREADO, plan.creado)]
        if plan.t_asignacion:
            eventos.append(('servicio.asignado', EstadoServicio.ASIGNADO, plan.t_asignacion))
        for _, accion, _, momento in plan.novedades:
            devuelto = accion == Novedad.Accion.DEVOLVER
            eventos.append(('servicio.novedad', EstadoServicio.DEVUELTO if devuelto else EstadoServicio.NOVEDAD, momento))
            if devuelto:
                eventos.append(('servicio.devuelto', EstadoServicio.DEVUELTO, momento))
        if plan.t_cierre:
            entregado = plan.tipo == TipoServicio.ENTREGA
            eventos.append((
                'servicio.entregado' if entregado else 'servicio.recolectado', plan.estado, plan.t_cierre,
            ))
        return eventos

    # ---------------------------------------------------------------- resumen

    def _imprimir_resumen(self, resumen, dias):
        planes = resumen['planes']
        usuarios = resumen['usuarios']
        estados = Counter(p.estado for p in planes)
        tipos = Counter(p.tipo for p in planes)
        n_novedades = sum(len(p.novedades) for p in planes)
        n_rutas = len({p.ruta.id for p in planes if p.ruta})
        webhook = resumen['webhook']
        envios = webhook['exitosos'] + webhook['fallidos']
        escribir = self.stdout.write

        escribir(self.style.SUCCESS(f'Datos de demostración creados ({dias} días de operación simulada).'))
        escribir('')
        escribir(
            f'Usuarios: {len(usuarios["motos"])} motorizados, {len(usuarios["clientes"])} clientes, '
            '1 alistador y 1 administrador (todos con prefijo demo_).'
        )
        escribir(f'Servicios: {len(planes)} ({tipos[TipoServicio.ENTREGA]} entregas, {tipos[TipoServicio.RECOLECCION]} recolecciones)')
        for estado in EstadoServicio:
            escribir(f'  {estado.value:<16}{estados[estado.value]:>5}')
        escribir(f'Rutas: {n_rutas}   Novedades: {n_novedades}   Evidencias: {resumen["evidencias"]}')
        escribir(f'Posiciones GPS: {resumen["posiciones"]}   Mensajes de chat: {resumen["mensajes"]}')
        porcentaje = 100 * webhook['exitosos'] / envios if envios else 0
        escribir(f'Envíos de webhook: {envios} ({webhook["exitosos"]} exitosos, {webhook["fallidos"]} fallidos, {porcentaje:.1f} %)')
        escribir('')
        escribir(self.style.WARNING(
            f'Credenciales DEMO (solo desarrollo): demo_admin, demo_alistador1, demo_moto1..{len(usuarios["motos"])}, '
            f'demo_cliente1..{len(usuarios["clientes"])}  /  contraseña: {PASSWORD_DEMO}'
        ))
        escribir(f'API key demo (se muestra una sola vez): {webhook["llave"]}')
        escribir('Indicadores: GET /api/indicadores/ o `python manage.py exportar_indicadores`.')
