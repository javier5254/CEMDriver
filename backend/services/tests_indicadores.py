"""Pruebas de RF-30: endpoint /api/indicadores/, seed_demo y exportar_indicadores."""
import datetime
import io
import json
import shutil
import tempfile
from collections import Counter
from decimal import Decimal
from pathlib import Path
from unittest import mock

from django.core.management import CommandError, call_command
from django.db import connection
from django.test import override_settings
from django.test.utils import CaptureQueriesContext
from django.utils import timezone
from testutils import BaseAPITestCase

from accounts.models import Usuario
from integrations.models import ApiKey, WebhookDelivery, WebhookEndpoint
from tracking.models import PosicionGPS

from .indicadores import calcular_indicadores
from .models import EstadoServicio, Evidencia, MensajeChat, Novedad, Ruta, Servicio, TipoServicio

URL = '/api/indicadores/'
ENTREGA, RECOLECCION = TipoServicio.ENTREGA, TipoServicio.RECOLECCION
ORDEN_ESTADOS = [
    'CREADO', 'ASIGNADO', 'RECIBIDO_CENTRO', 'EN_TRANSITO', 'NOVEDAD', 'ENTREGADO', 'RECOLECTADO', 'DEVUELTO',
]


class IndicadoresPermisosTests(BaseAPITestCase):
    def test_admin_y_alistador_pueden_consultar(self):
        for usuario in (self.admin, self.alistador):
            self.autenticar(usuario)
            self.assertEqual(self.client.get(URL).status_code, 200, usuario.rol)

    def test_cliente_y_motorizado_reciben_403(self):
        for usuario in (self.cliente, self.motorizado):
            self.autenticar(usuario)
            self.assertEqual(self.client.get(URL).status_code, 403, usuario.rol)

    def test_sin_token_recibe_401(self):
        self.assertEqual(self.client.get(URL).status_code, 401)

    def test_dias_invalido_devuelve_400_con_mensaje(self):
        self.autenticar(self.admin)
        for valor in ('0', '366', '-3', 'abc', '7.5'):
            respuesta = self.client.get(URL, {'dias': valor})
            self.assertEqual(respuesta.status_code, 400, valor)
            self.assertIn('entre 1 y 365', respuesta.json()['dias'][0])

    def test_dias_en_los_limites_es_valido(self):
        self.autenticar(self.admin)
        for valor in (1, 365):
            respuesta = self.client.get(URL, {'dias': valor})
            self.assertEqual(respuesta.status_code, 200)
            self.assertEqual(len(respuesta.json()['serie_diaria']), valor)


class IndicadoresBase(BaseAPITestCase):
    """Conjunto pequeño y conocido de datos para verificar cifras exactas.

    Hoy = H. Servicios (S1..S11 dentro de 30 días; S12 fuera):

        id  tipo  estado           zona    creado  ruta  extras
        S1  ENT   ENTREGADO        Zona A  H       R1    novedad REINTENTAR (tipo libre)
        S2  ENT   ENTREGADO        Zona A  H-1     R1
        S3  ENT   DEVUELTO         Zona B  H-1     R2    REINTENTAR cliente ausente + DEVOLVER dirección errada
        S4  ENT   NOVEDAD          Zona A  H-2     R1    REINTENTAR cliente ausente
        S5  ENT   CREADO           Zona B  H       -
        S6  ENT   EN_TRANSITO      Zona B  H       R2
        S7  REC   RECOLECTADO      Zona A  H-3     R1    evidencia completa, cierre 24 h después
        S8  REC   RECOLECTADO      Zona B  H-3     R2    solo foto, cierre 48 h después
        S9  REC   DEVUELTO         Zona A  H-4     R1    DEVOLVER rechazo
        S10 REC   ASIGNADO         Zona A  H-5     R3
        S11 ENT   RECIBIDO_CENTRO  Zona B  H-5     R3
        S12 ENT   ENTREGADO        Zona A  H-40    R_vieja  REINTENTAR cliente ausente (fuera del periodo)
    """

    def setUp(self):
        super().setUp()
        self.hoy = timezone.localdate()
        self.motorizado3 = self._crear_usuario('motorizado_test3', 'MOTORIZADO')
        self._crear_datos()

    def momento(self, dias_atras, horas=10):
        dia = self.hoy - datetime.timedelta(days=dias_atras)
        return timezone.make_aware(datetime.datetime.combine(dia, datetime.time(horas)))

    def servicio(self, tipo, estado, zona, dias_atras, ruta=None):
        servicio = Servicio.objects.create(
            tipo=tipo, cliente=self.cliente, zona=zona, direccion_destino='Calle 1', direccion_origen='Calle 2',
            fecha_agenda=self.hoy, estado=estado, ruta=ruta,
        )
        Servicio.objects.filter(pk=servicio.pk).update(creado_en=self.momento(dias_atras))
        return servicio

    def novedad(self, servicio, tipo, accion):
        n = Novedad.objects.create(servicio=servicio, tipo=tipo, accion=accion)
        Novedad.objects.filter(pk=n.pk).update(creado_en=servicio.creado_en)

    def evidencia(self, servicio, horas_despues, **archivos):
        e = Evidencia.objects.create(servicio=servicio, **archivos)
        creado = Servicio.objects.get(pk=servicio.pk).creado_en
        Evidencia.objects.filter(pk=e.pk).update(capturado_en=creado + datetime.timedelta(hours=horas_despues))

    def _crear_datos(self):
        r1 = Ruta.objects.create(motorizado=self.motorizado, fecha=self.hoy)
        r2 = Ruta.objects.create(motorizado=self.otro_motorizado, fecha=self.hoy)
        r3 = Ruta.objects.create(motorizado=self.motorizado3, fecha=self.hoy - datetime.timedelta(days=5))
        r_vieja = Ruta.objects.create(motorizado=self.motorizado, fecha=self.hoy - datetime.timedelta(days=40))
        A, B = 'Zona A', 'Zona B'
        reintentar, devolver = Novedad.Accion.REINTENTAR, Novedad.Accion.DEVOLVER

        s1 = self.servicio(ENTREGA, EstadoServicio.ENTREGADO, A, 0, r1)
        self.novedad(s1, 'Portería cerrada', reintentar)
        self.servicio(ENTREGA, EstadoServicio.ENTREGADO, A, 1, r1)
        s3 = self.servicio(ENTREGA, EstadoServicio.DEVUELTO, B, 1, r2)
        self.novedad(s3, 'CLIENTE_AUSENTE', reintentar)
        self.novedad(s3, 'DIRECCION_ERRADA', devolver)
        s4 = self.servicio(ENTREGA, EstadoServicio.NOVEDAD, A, 2, r1)
        self.novedad(s4, 'CLIENTE_AUSENTE', reintentar)
        self.servicio(ENTREGA, EstadoServicio.CREADO, B, 0)
        self.s6 = self.servicio(ENTREGA, EstadoServicio.EN_TRANSITO, B, 0, r2)
        s7 = self.servicio(RECOLECCION, EstadoServicio.RECOLECTADO, A, 3, r1)
        self.evidencia(s7, 24, foto='evidencias/fotos/a.png', firma='evidencias/firmas/a.png')
        s8 = self.servicio(RECOLECCION, EstadoServicio.RECOLECTADO, B, 3, r2)
        self.evidencia(s8, 48, foto='evidencias/fotos/b.png', firma='')
        s9 = self.servicio(RECOLECCION, EstadoServicio.DEVUELTO, A, 4, r1)
        self.novedad(s9, 'RECHAZO', devolver)
        self.servicio(RECOLECCION, EstadoServicio.ASIGNADO, A, 5, r3)
        self.servicio(ENTREGA, EstadoServicio.RECIBIDO_CENTRO, B, 5, r3)
        s12 = self.servicio(ENTREGA, EstadoServicio.ENTREGADO, A, 40, r_vieja)
        self.novedad(s12, 'CLIENTE_AUSENTE', reintentar)

        # GPS: 2 en Zona B (S6) y 1 en Zona A (S4) dentro del periodo; 1 fuera.
        for servicio, moto, dias_atras in (
            (self.s6, self.otro_motorizado, 0), (self.s6, self.otro_motorizado, 0),
            (s4, self.motorizado, 2), (self.s6, self.otro_motorizado, 40),
        ):
            p = PosicionGPS.objects.create(servicio=servicio, motorizado=moto, lat=Decimal('4.65'), lng=Decimal('-74.06'))
            PosicionGPS.objects.filter(pk=p.pk).update(timestamp=self.momento(dias_atras))
        # Chat: 1 en Zona A (S1) y 1 en Zona B (S6) dentro del periodo; 1 fuera.
        for servicio, autor, dias_atras in (
            (s1, self.cliente, 0), (self.s6, self.cliente, 0), (self.s6, self.cliente, 40),
        ):
            m = MensajeChat.objects.create(servicio=servicio, autor=autor, texto='hola')
            MensajeChat.objects.filter(pk=m.pk).update(enviado_en=self.momento(dias_atras))

        # Integraciones: 2 API keys activas + 1 inactiva; 1 webhook activo + 1 inactivo.
        ApiKey.generar('llave 1', self.alistador)
        ApiKey.generar('llave 2', self.alistador)
        inactiva, _ = ApiKey.generar('llave 3', self.alistador)
        ApiKey.objects.filter(pk=inactiva.pk).update(activa=False)
        activo = WebhookEndpoint.objects.create(nombre='erp', url='http://localhost:9/a', eventos='servicio.creado')
        WebhookEndpoint.objects.create(nombre='viejo', url='http://localhost:9/b', eventos='servicio.creado', activo=False)
        # Envios: 5 dentro del periodo (4 exitosos, 1 fallido) y 1 fuera.
        for exito, dias_atras in ((True, 0), (True, 1), (True, 2), (True, 3), (False, 4), (True, 40)):
            d = WebhookDelivery.objects.create(endpoint=activo, evento='servicio.creado', payload={}, exito=exito)
            WebhookDelivery.objects.filter(pk=d.pk).update(creado_en=self.momento(dias_atras))

    def consultar(self, **parametros):
        self.autenticar(self.admin)
        respuesta = self.client.get(URL, parametros)
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        return respuesta.json()


class IndicadoresCifrasTests(IndicadoresBase):
    def test_estructura_y_periodo(self):
        datos = self.consultar()
        self.assertEqual(list(datos), [
            'generado_en', 'periodo', 'resumen', 'por_estado', 'serie_diaria', 'por_zona',
            'novedades', 'evidencia', 'motorizados', 'operacion', 'integraciones',
        ])
        self.assertIsNotNone(datetime.datetime.fromisoformat(datos['generado_en']).tzinfo)
        self.assertEqual(datos['periodo'], {
            'dias': 30,
            'desde': (self.hoy - datetime.timedelta(days=29)).isoformat(),
            'hasta': self.hoy.isoformat(),
            'zona': None,
        })

    def test_resumen(self):
        self.assertEqual(self.consultar()['resumen'], {
            'servicios_total': 11, 'entregas': 7, 'recolecciones': 4,
            'en_curso': 5, 'cerrados_exitosos': 4, 'devueltos': 2,
            'tasa_exito': 0.6667,           # 4 / (4 + 2)
            'servicios_con_novedad': 4,     # S1, S3, S4, S9
            'tasa_novedad': 0.3636,         # 4 / 11
        })

    def test_por_estado_incluye_los_ocho_estados_en_orden(self):
        por_estado = self.consultar()['por_estado']
        self.assertEqual([e['estado'] for e in por_estado], ORDEN_ESTADOS)
        self.assertEqual([e['total'] for e in por_estado], [1, 1, 1, 1, 1, 2, 2, 2])
        self.assertEqual(por_estado[3], {'estado': 'EN_TRANSITO', 'etiqueta': 'En tránsito', 'total': 1})
        self.assertEqual(sum(e['total'] for e in por_estado), 11)

    def test_serie_diaria(self):
        serie = self.consultar()['serie_diaria']
        self.assertEqual(len(serie), 30)
        self.assertEqual(serie[0]['fecha'], (self.hoy - datetime.timedelta(days=29)).isoformat())
        self.assertEqual(serie[-1]['fecha'], self.hoy.isoformat())
        fechas = [fila['fecha'] for fila in serie]
        self.assertEqual(fechas, sorted(set(fechas)))
        por_dia = {f['fecha']: (f['entregas'], f['recolecciones']) for f in serie}
        esperado = {0: (3, 0), 1: (2, 0), 2: (1, 0), 3: (0, 2), 4: (0, 1), 5: (1, 1)}
        for dias_atras in range(30):
            fecha = (self.hoy - datetime.timedelta(days=dias_atras)).isoformat()
            self.assertEqual(por_dia[fecha], esperado.get(dias_atras, (0, 0)), fecha)
        self.assertEqual(sum(f['entregas'] for f in serie), 7)
        self.assertEqual(sum(f['recolecciones'] for f in serie), 4)

    def test_por_zona(self):
        self.assertEqual(self.consultar()['por_zona'], [
            {'zona': 'Zona A', 'total': 6, 'exitosos': 3, 'con_novedad': 3},
            {'zona': 'Zona B', 'total': 5, 'exitosos': 1, 'con_novedad': 1},
        ])

    def test_novedades(self):
        self.assertEqual(self.consultar()['novedades'], {
            'total': 5,
            'por_tipo': [
                {'tipo': 'Cliente ausente', 'total': 2},
                {'tipo': 'Dirección errada', 'total': 1},
                {'tipo': 'Portería cerrada', 'total': 1},       # tipo libre: se devuelve tal cual
                {'tipo': 'Rechazo del destinatario', 'total': 1},
            ],
            'por_accion': [
                {'accion': 'REINTENTAR', 'etiqueta': 'Reintentar', 'total': 3},
                {'accion': 'DEVOLVER_A_CENTRO', 'etiqueta': 'Devolver a centro', 'total': 2},
            ],
        })

    def test_evidencia(self):
        self.assertEqual(self.consultar()['evidencia'], {
            'recolecciones_cerradas': 2,
            'con_evidencia_completa': 1,    # S8 no tiene firma
            'porcentaje': 0.5,
            'horas_promedio_a_cierre': 36.0,  # (24 + 48) / 2
        })

    def test_motorizados(self):
        self.assertEqual(self.consultar()['motorizados'], [
            {'id': self.motorizado.id, 'nombre': 'motorizado_test', 'servicios': 5,
             'cerrados_exitosos': 3, 'con_novedad': 3},
            {'id': self.otro_motorizado.id, 'nombre': 'motorizado_test2', 'servicios': 3,
             'cerrados_exitosos': 1, 'con_novedad': 1},
            {'id': self.motorizado3.id, 'nombre': 'motorizado_test3', 'servicios': 2,
             'cerrados_exitosos': 0, 'con_novedad': 0},
        ])

    def test_operacion(self):
        self.assertEqual(self.consultar()['operacion'], {
            'rutas': 3, 'sin_asignar': 1, 'posiciones_gps': 3, 'mensajes_chat': 2,
        })

    def test_integraciones(self):
        self.assertEqual(self.consultar()['integraciones'], {
            'api_keys_activas': 2,
            'webhooks_activos': 1,
            'envios_webhook': {'total': 5, 'exitosos': 4, 'fallidos': 1, 'tasa_exito': 0.8},
        })


class IndicadoresConsultasTests(IndicadoresBase):
    def test_el_numero_de_consultas_no_crece_con_los_datos(self):
        # Sin N+1: agregar servicios, zonas, novedades y motorizados no agrega consultas.
        self.autenticar(self.admin)
        with CaptureQueriesContext(connection) as antes:
            self.assertEqual(self.client.get(URL).status_code, 200)

        ruta = Ruta.objects.filter(motorizado=self.motorizado).first()
        for i in range(15):
            servicio = self.servicio(ENTREGA, EstadoServicio.ENTREGADO, f'Zona nueva {i}', i % 5, ruta)
            self.novedad(servicio, 'RECHAZO', Novedad.Accion.DEVOLVER)

        with CaptureQueriesContext(connection) as despues:
            respuesta = self.client.get(URL)
        self.assertEqual(respuesta.json()['resumen']['servicios_total'], 26)
        self.assertEqual(len(despues), len(antes))
        self.assertLessEqual(len(despues), 20)


class IndicadoresFiltrosTests(IndicadoresBase):
    def test_dias_excluye_servicios_fuera_del_periodo(self):
        datos = self.consultar(dias=3)  # H-2 .. H
        self.assertEqual(datos['periodo']['desde'], (self.hoy - datetime.timedelta(days=2)).isoformat())
        self.assertEqual(datos['resumen']['servicios_total'], 6)  # S1, S2, S3, S4, S5, S6
        self.assertEqual(datos['resumen']['recolecciones'], 0)
        self.assertEqual(len(datos['serie_diaria']), 3)
        self.assertEqual(datos['novedades']['total'], 4)  # S1, S3 (x2), S4
        self.assertEqual(datos['evidencia']['recolecciones_cerradas'], 0)
        self.assertIsNone(datos['evidencia']['porcentaje'])
        self.assertIsNone(datos['evidencia']['horas_promedio_a_cierre'])

    def test_un_dia_solo_cuenta_hoy(self):
        datos = self.consultar(dias=1)
        self.assertEqual(datos['resumen']['servicios_total'], 3)  # S1, S5, S6
        self.assertEqual(len(datos['serie_diaria']), 1)
        self.assertEqual(datos['operacion']['rutas'], 2)  # R1 y R2 son de hoy

    def test_un_periodo_largo_incluye_los_servicios_antiguos(self):
        datos = self.consultar(dias=60)
        self.assertEqual(datos['resumen']['servicios_total'], 12)  # + S12
        self.assertEqual(datos['novedades']['total'], 6)
        self.assertEqual(datos['operacion']['rutas'], 4)
        self.assertEqual(datos['operacion']['posiciones_gps'], 4)
        self.assertEqual(datos['integraciones']['envios_webhook']['total'], 6)
        self.assertEqual(len(datos['serie_diaria']), 60)

    def test_zona_filtra_los_indicadores(self):
        datos = self.consultar(zona='Zona A')
        self.assertEqual(datos['periodo']['zona'], 'Zona A')
        self.assertEqual(datos['resumen'], {
            'servicios_total': 6, 'entregas': 3, 'recolecciones': 3,
            'en_curso': 2, 'cerrados_exitosos': 3, 'devueltos': 1,
            'tasa_exito': 0.75, 'servicios_con_novedad': 3, 'tasa_novedad': 0.5,
        })
        self.assertEqual([e['total'] for e in datos['por_estado']], [0, 1, 0, 0, 1, 2, 1, 1])
        self.assertEqual([z['zona'] for z in datos['por_zona']], ['Zona A'])
        self.assertEqual(datos['novedades']['total'], 3)  # S1, S4, S9
        self.assertEqual(datos['evidencia'], {
            'recolecciones_cerradas': 1, 'con_evidencia_completa': 1,
            'porcentaje': 1.0, 'horas_promedio_a_cierre': 24.0,
        })
        self.assertEqual([(m['servicios'], m['cerrados_exitosos'], m['con_novedad']) for m in datos['motorizados']],
                         [(5, 3, 3), (1, 0, 0)])
        self.assertEqual(datos['operacion'], {
            'rutas': 2, 'sin_asignar': 0, 'posiciones_gps': 1, 'mensajes_chat': 1,
        })
        # Las integraciones son globales: no dependen de la zona.
        self.assertEqual(datos['integraciones']['envios_webhook']['total'], 5)

    def test_zona_sin_servicios_devuelve_ceros_y_nulos(self):
        datos = self.consultar(zona='No existe')
        resumen = datos['resumen']
        self.assertEqual(resumen['servicios_total'], 0)
        self.assertIsNone(resumen['tasa_exito'])
        self.assertIsNone(resumen['tasa_novedad'])
        self.assertEqual([e['total'] for e in datos['por_estado']], [0] * 8)
        self.assertEqual(len(datos['serie_diaria']), 30)
        self.assertEqual(datos['por_zona'], [])
        self.assertEqual(datos['motorizados'], [])
        self.assertEqual(datos['novedades']['total'], 0)
        self.assertEqual(datos['novedades']['por_tipo'], [])
        self.assertEqual([a['total'] for a in datos['novedades']['por_accion']], [0, 0])

    def test_zona_vacia_equivale_a_sin_filtro(self):
        self.assertEqual(self.consultar(zona='')['resumen']['servicios_total'], 11)


class IndicadoresPeriodoLocalTests(BaseAPITestCase):
    def test_el_periodo_se_mide_en_fecha_local_del_servidor(self):
        utc = datetime.timezone.utc
        # 2026-03-15 03:00 UTC es el 14 de marzo a las 22:00 en Bogota (UTC-5).
        ahora = datetime.datetime(2026, 3, 15, 3, 0, tzinfo=utc)
        creados = {
            'dentro_dia_14': datetime.datetime(2026, 3, 15, 3, 30, tzinfo=utc),   # 14-mar 22:30 local
            'dentro_dia_13': datetime.datetime(2026, 3, 14, 4, 30, tzinfo=utc),   # 13-mar 23:30 local
            'antes_del_periodo': datetime.datetime(2026, 3, 13, 4, 30, tzinfo=utc),  # 12-mar 23:30 local
            'despues_del_periodo': datetime.datetime(2026, 3, 15, 5, 30, tzinfo=utc),  # 15-mar 00:30 local
        }
        for momento in creados.values():
            servicio = Servicio.objects.create(
                tipo=ENTREGA, cliente=self.cliente, zona='Z', direccion_destino='Calle 1',
                fecha_agenda=datetime.date(2026, 3, 14),
            )
            Servicio.objects.filter(pk=servicio.pk).update(creado_en=momento)

        datos = calcular_indicadores(dias=2, ahora=ahora)
        self.assertEqual(datos['periodo'], {'dias': 2, 'desde': '2026-03-13', 'hasta': '2026-03-14', 'zona': None})
        self.assertEqual(datos['resumen']['servicios_total'], 2)
        self.assertEqual(datos['serie_diaria'], [
            {'fecha': '2026-03-13', 'entregas': 1, 'recolecciones': 0},
            {'fecha': '2026-03-14', 'entregas': 1, 'recolecciones': 0},
        ])
        self.assertTrue(datos['generado_en'].startswith('2026-03-14T22:00:00'))
        self.assertTrue(datos['generado_en'].endswith('-05:00'))


# Miercoles 17-jun-2026, 15:30 en Bogota. Fijar "ahora" hace deterministas las pruebas que
# comparan dos ejecuciones de seed_demo (los instantes de hoy dependen de la hora).
AHORA_FIJA = datetime.datetime(2026, 6, 17, 20, 30, tzinfo=datetime.timezone.utc)


class UsaMediaTemporal(BaseAPITestCase):
    """Redirige MEDIA_ROOT a una carpeta temporal (para no ensuciar backend/media) y
    congela timezone.now() en `self.ahora`."""

    def setUp(self):
        super().setUp()
        self.carpeta = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.carpeta, ignore_errors=True)
        sobreescritura = override_settings(MEDIA_ROOT=self.carpeta)
        sobreescritura.enable()
        self.addCleanup(sobreescritura.disable)
        self.ahora = AHORA_FIJA
        self.enterContext(mock.patch('django.utils.timezone.now', side_effect=lambda: self.ahora))

    def sembrar(self, **opciones):
        salida = io.StringIO()
        call_command('seed_demo', stdout=salida, **opciones)
        return salida.getvalue()

    @staticmethod
    def demo():
        return Servicio.objects.filter(cliente__username__startswith='demo_')

    @staticmethod
    def instantanea():
        return {
            'estados': Counter(Servicio.objects.values_list('estado', flat=True)),
            'tipos': Counter(Servicio.objects.values_list('tipo', flat=True)),
            'zonas': Counter(Servicio.objects.values_list('zona', flat=True)),
            **{
                modelo.__name__: modelo.objects.count()
                for modelo in (
                    Usuario, Ruta, Novedad, Evidencia, PosicionGPS, MensajeChat,
                    ApiKey, WebhookEndpoint, WebhookDelivery,
                )
            },
        }


class SeedDemoTests(UsaMediaTemporal):
    def test_crea_usuarios_servicios_y_el_endpoint_los_refleja(self):
        salida = self.sembrar(servicios=30, dias=14, semilla=1)

        self.assertEqual(self.demo().count(), 30)
        self.assertEqual(Usuario.objects.filter(username__startswith='demo_', rol='MOTORIZADO').count(), 4)
        self.assertEqual(Usuario.objects.filter(username__startswith='demo_', rol='CLIENTE').count(), 8)
        self.assertTrue(Usuario.objects.get(username='demo_moto1').check_password('demo1234'))
        self.assertIn('demo1234', salida)
        self.assertIn('Servicios: 30', salida)

        self.autenticar(Usuario.objects.get(username='demo_admin'))
        respuesta = self.client.get(URL, {'dias': 14})
        self.assertEqual(respuesta.status_code, 200)
        datos = respuesta.json()
        self.assertEqual(datos['resumen']['servicios_total'], 30)
        self.assertEqual(sum(e['total'] for e in datos['por_estado']), 30)
        self.assertEqual(sum(f['entregas'] + f['recolecciones'] for f in datos['serie_diaria']), 30)
        self.assertEqual(datos['resumen']['entregas'] + datos['resumen']['recolecciones'], 30)
        self.assertGreater(datos['novedades']['total'], 0)
        self.assertEqual(datos['integraciones']['api_keys_activas'], 1)
        self.assertEqual(datos['integraciones']['webhooks_activos'], 1)
        self.assertGreater(datos['integraciones']['envios_webhook']['total'], 0)

    def test_valores_por_defecto_generan_la_operacion_completa(self):
        self.sembrar(semilla=7)
        self.assertEqual(self.demo().count(), 240)
        datos = calcular_indicadores(dias=60)
        resumen = datos['resumen']
        self.assertEqual(resumen['servicios_total'], 240)
        self.assertTrue(0.6 < resumen['cerrados_exitosos'] / 240 < 0.9)
        self.assertGreater(resumen['devueltos'], 0)
        self.assertGreater(resumen['entregas'], resumen['recolecciones'])
        self.assertEqual(len(datos['por_zona']), 6)
        self.assertEqual(len(datos['motorizados']), 4)
        self.assertGreater(datos['evidencia']['recolecciones_cerradas'], 0)
        self.assertLess(datos['evidencia']['porcentaje'], 1)
        self.assertGreater(datos['operacion']['posiciones_gps'], 0)
        self.assertGreater(datos['operacion']['mensajes_chat'], 0)

    def test_sin_reset_no_duplica(self):
        self.sembrar(servicios=30, dias=14, semilla=1)
        antes = self.instantanea()
        salida = self.sembrar(servicios=30, dias=14, semilla=1)
        self.assertIn('Ya existen datos de demostración', salida)
        self.assertEqual(self.instantanea(), antes)

    def test_reset_recrea_el_mismo_estado(self):
        self.sembrar(servicios=40, dias=20, semilla=3)
        antes = self.instantanea()
        self.sembrar(servicios=40, dias=20, semilla=3, reset=True)
        self.assertEqual(self.instantanea(), antes)
        self.sembrar(servicios=40, dias=20, semilla=3, reset=True)
        self.assertEqual(self.instantanea(), antes)

    def test_la_misma_semilla_es_reproducible_y_otra_cambia_los_datos(self):
        self.sembrar(servicios=60, dias=20, semilla=5)
        direcciones = list(self.demo().order_by('creado_en', 'id').values_list('zona', 'tipo', 'estado', 'direccion_destino'))
        self.sembrar(servicios=60, dias=20, semilla=5, reset=True)
        self.assertEqual(
            list(self.demo().order_by('creado_en', 'id').values_list('zona', 'tipo', 'estado', 'direccion_destino')),
            direcciones,
        )
        self.sembrar(servicios=60, dias=20, semilla=6, reset=True)
        self.assertNotEqual(
            list(self.demo().order_by('creado_en', 'id').values_list('zona', 'tipo', 'estado', 'direccion_destino')),
            direcciones,
        )

    def test_reset_no_toca_datos_que_no_son_demo(self):
        servicio = Servicio.objects.create(
            tipo=ENTREGA, cliente=self.cliente, zona='Zona Real', direccion_destino='Calle 1',
            fecha_agenda=datetime.date.today(),
        )
        llave, _ = ApiKey.generar('Llave real', self.alistador)
        webhook = WebhookEndpoint.objects.create(nombre='ERP real', url='http://localhost:9/x', eventos='servicio.creado')

        self.sembrar(servicios=20, dias=10, semilla=1)
        self.sembrar(servicios=20, dias=10, semilla=1, reset=True)

        self.assertTrue(Servicio.objects.filter(pk=servicio.pk).exists())
        self.assertTrue(ApiKey.objects.filter(pk=llave.pk).exists())
        self.assertTrue(WebhookEndpoint.objects.filter(pk=webhook.pk).exists())
        self.assertTrue(Usuario.objects.filter(pk=self.cliente.pk).exists())

    def test_reset_elimina_los_archivos_de_evidencia_demo(self):
        self.sembrar(servicios=80, dias=30, semilla=2)
        archivos = list(Path(self.carpeta).rglob('*.png'))
        self.assertTrue(archivos)
        self.assertTrue(all(a.name.startswith('demo_') for a in archivos))
        self.sembrar(servicios=1, dias=1, semilla=2, reset=True)
        self.assertEqual(list(Path(self.carpeta).rglob('*.png')), [])

    def test_parametros_invalidos(self):
        for opciones in ({'dias': 0}, {'dias': 366}, {'servicios': 0}):
            with self.assertRaises(CommandError):
                self.sembrar(**opciones)
        self.assertFalse(Usuario.objects.filter(username__startswith='demo_').exists())

    def test_estados_coherentes_con_la_maquina_de_estados(self):
        self.sembrar(servicios=160, dias=40, semilla=11)
        estados = self.verificar_coherencia(160)
        self.assertTrue({'ENTREGADO', 'RECOLECTADO', 'DEVUELTO', 'NOVEDAD', 'EN_TRANSITO'} <= estados, estados)

    def test_funciona_a_cualquier_hora_del_dia_sin_fechas_futuras(self):
        # Incluye la madrugada (casi sin horas transcurridas hoy) y el cierre del dia.
        for hora, minuto in ((0, 5), (6, 30), (8, 0), (12, 0), (23, 50)):
            self.ahora = AHORA_FIJA.replace(hour=(hora + 5) % 24, minute=minuto)
            self.sembrar(servicios=60, dias=10, semilla=4, reset=True)
            self.verificar_coherencia(60)

    def verificar_coherencia(self, cantidad):
        """Comprueba que lo sembrado respeta la maquina de estados y no tiene fechas futuras."""
        ahora = timezone.now()
        servicios = list(self.demo().select_related('ruta__motorizado').prefetch_related('novedades', 'posiciones'))
        self.assertEqual(len(servicios), cantidad)
        estados = {s.estado for s in servicios}

        for s in servicios:
            self.assertLessEqual(s.creado_en, ahora, s.id)
            novedades = sorted(s.novedades.all(), key=lambda n: (n.creado_en, n.id))
            if s.tipo == ENTREGA:
                self.assertTrue(s.direccion_destino, s.id)
            else:
                self.assertTrue(s.direccion_origen, s.id)
                self.assertNotEqual(s.estado, EstadoServicio.RECIBIDO_CENTRO, s.id)
            if s.estado == EstadoServicio.CREADO:
                self.assertIsNone(s.ruta, s.id)
            else:
                self.assertIsNotNone(s.ruta, s.id)
                self.assertTrue(s.ruta.motorizado.username.startswith('demo_moto'), s.id)
            if s.estado == EstadoServicio.DEVUELTO:
                self.assertEqual(novedades[-1].accion, Novedad.Accion.DEVOLVER, s.id)
            if s.estado == EstadoServicio.NOVEDAD:
                self.assertEqual(novedades[-1].accion, Novedad.Accion.REINTENTAR, s.id)
            if s.estado in (EstadoServicio.ENTREGADO, EstadoServicio.RECOLECTADO, EstadoServicio.EN_TRANSITO):
                self.assertTrue(all(n.accion == Novedad.Accion.REINTENTAR for n in novedades), s.id)
            for n in novedades:
                self.assertGreaterEqual(n.creado_en, s.creado_en, s.id)
                self.assertLessEqual(n.creado_en, ahora, s.id)
            self.assertEqual(
                hasattr(s, 'evidencia'), s.estado == EstadoServicio.RECOLECTADO, f'evidencia del servicio {s.id}',
            )
            if hasattr(s, 'evidencia'):
                self.assertGreater(s.evidencia.capturado_en, s.creado_en, s.id)
                self.assertLessEqual(s.evidencia.capturado_en, ahora, s.id)
            for p in s.posiciones.all():
                self.assertGreater(p.timestamp, s.creado_en, s.id)
                self.assertLessEqual(p.timestamp, ahora, s.id)
                self.assertEqual(p.motorizado_id, s.ruta.motorizado_id, s.id)
                self.assertTrue(Decimal('4.5') < p.lat < Decimal('4.8'), s.id)
                self.assertTrue(Decimal('-74.3') < p.lng < Decimal('-73.9'), s.id)
        for m in MensajeChat.objects.select_related('servicio'):
            self.assertGreater(m.enviado_en, m.servicio.creado_en)
            self.assertLessEqual(m.enviado_en, ahora)
        for d in WebhookDelivery.objects.all():
            self.assertLessEqual(d.creado_en, ahora)
        return estados

    def test_las_evidencias_son_imagenes_validas_y_algunas_incompletas(self):
        from PIL import Image

        self.sembrar(servicios=240, dias=60, semilla=2026)
        evidencias = list(Evidencia.objects.all())
        self.assertTrue(evidencias)
        for e in evidencias:
            for campo in (e.foto, e.firma):
                if campo:
                    with Image.open(campo.path) as imagen:
                        imagen.verify()
        incompletas = [e for e in evidencias if not (e.foto and e.firma)]
        self.assertTrue(0 < len(incompletas) < len(evidencias) * 0.15)


class ExportarIndicadoresTests(IndicadoresBase):
    def test_escribe_un_json_valido_en_la_ruta_indicada(self):
        with tempfile.TemporaryDirectory() as carpeta:
            destino = Path(carpeta) / 'datos' / 'anidada' / 'indicadores.json'
            salida = io.StringIO()
            call_command('exportar_indicadores', dias=30, salida=str(destino), stdout=salida)
            self.assertTrue(destino.exists())
            self.assertIn('indicadores.json', salida.getvalue())
            contenido = json.loads(destino.read_text(encoding='utf-8'))

        esperado = calcular_indicadores(dias=30)
        for datos in (contenido, esperado):
            datos.pop('generado_en')
        self.assertEqual(contenido, esperado)
        self.assertEqual(contenido['resumen']['servicios_total'], 11)

    def test_el_json_conserva_los_acentos(self):
        with tempfile.TemporaryDirectory() as carpeta:
            destino = Path(carpeta) / 'indicadores.json'
            call_command('exportar_indicadores', salida=str(destino), stdout=io.StringIO())
            texto = destino.read_text(encoding='utf-8')
        self.assertIn('En tránsito', texto)
        self.assertIn('Dirección errada', texto)

    def test_sin_salida_imprime_el_json_por_stdout(self):
        salida = io.StringIO()
        call_command('exportar_indicadores', dias=7, zona='Zona A', stdout=salida)
        datos = json.loads(salida.getvalue())
        self.assertEqual(datos['periodo']['dias'], 7)
        self.assertEqual(datos['periodo']['zona'], 'Zona A')
        self.assertEqual(len(datos['serie_diaria']), 7)
        self.assertEqual(datos['resumen']['servicios_total'], 6)

    def test_dias_fuera_de_rango_falla(self):
        for dias in (0, 366):
            with self.assertRaises(CommandError):
                call_command('exportar_indicadores', dias=dias, stdout=io.StringIO())
