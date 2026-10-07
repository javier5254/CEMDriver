import datetime
import io

from channels.testing import WebsocketCommunicator
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework_simplejwt.tokens import AccessToken
from testutils import BaseAPITestCase

from cmedriver.asgi import application
from coverage.models import Cobertura
from inventory.models import Producto

from .models import EstadoServicio, Ruta, Servicio, TipoServicio


def imagen_de_prueba(nombre='foto.png'):
    buffer = io.BytesIO()
    Image.new('RGB', (4, 4), color='red').save(buffer, format='PNG')
    buffer.seek(0)
    return SimpleUploadedFile(nombre, buffer.read(), content_type='image/png')


class CrearServicioTests(BaseAPITestCase):
    def test_solo_alistador_puede_crear_servicio(self):
        self.autenticar(self.cliente)
        response = self.client.post('/api/servicios/', {
            'tipo': TipoServicio.ENTREGA,
            'cliente': self.cliente.id,
            'zona': 'Zona Test',
            'direccion_destino': 'Calle 1',
            'fecha_agenda': '2030-01-01',
        })
        self.assertEqual(response.status_code, 403)

    def test_entrega_sin_direccion_destino_falla(self):
        self.autenticar(self.alistador)
        response = self.client.post('/api/servicios/', {
            'tipo': TipoServicio.ENTREGA,
            'cliente': self.cliente.id,
            'zona': 'Zona Test',
            'fecha_agenda': '2030-01-01',
        })
        self.assertEqual(response.status_code, 400)

    def test_recoleccion_sin_direccion_origen_falla(self):
        self.autenticar(self.alistador)
        response = self.client.post('/api/servicios/', {
            'tipo': TipoServicio.RECOLECCION,
            'cliente': self.cliente.id,
            'zona': 'Zona Test',
            'fecha_agenda': '2030-01-01',
        })
        self.assertEqual(response.status_code, 400)

    def test_crear_servicio_valido_queda_en_creado(self):
        self.autenticar(self.alistador)
        response = self.client.post('/api/servicios/', {
            'tipo': TipoServicio.ENTREGA,
            'cliente': self.cliente.id,
            'zona': 'Zona Test',
            'direccion_destino': 'Calle 1',
            'fecha_agenda': '2030-01-01',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['estado'], EstadoServicio.CREADO)


class ServicioProductoTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.servicio = Servicio.objects.create(
            tipo=TipoServicio.ENTREGA, cliente=self.cliente, zona='Zona Test',
            direccion_destino='Calle 1', fecha_agenda=datetime.date.today(),
        )
        self.p1 = Producto.objects.create(sku='MP-1', nombre='Item 1', precio=1000, stock=10, centro_mensajeria='C')
        self.p2 = Producto.objects.create(sku='MP-2', nombre='Item 2', precio=2000, stock=10, centro_mensajeria='C')

    def test_alistador_puede_definir_lineas_de_producto(self):
        self.autenticar(self.alistador)
        r = self.client.put(f'/api/servicios/{self.servicio.id}/productos/', [
            {'producto': self.p1.id, 'cantidad': 2},
            {'producto': self.p2.id, 'cantidad': 1},
        ], format='json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data['productos_detalle']), 2)

    def test_reemplazar_lineas_es_idempotente(self):
        self.autenticar(self.alistador)
        self.client.put(f'/api/servicios/{self.servicio.id}/productos/', [
            {'producto': self.p1.id, 'cantidad': 3},
            {'producto': self.p2.id, 'cantidad': 1},
        ], format='json')
        r = self.client.put(f'/api/servicios/{self.servicio.id}/productos/', [
            {'producto': self.p1.id, 'cantidad': 5},
        ], format='json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data['productos_detalle']), 1)
        self.assertEqual(r.data['productos_detalle'][0]['cantidad'], 5)

    def test_no_alistador_no_puede_definir_lineas(self):
        self.autenticar(self.cliente)
        r = self.client.put(f'/api/servicios/{self.servicio.id}/productos/', [
            {'producto': self.p1.id, 'cantidad': 1},
        ], format='json')
        self.assertEqual(r.status_code, 403)


class CicloDeVidaEntregaTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.servicio = Servicio.objects.create(
            tipo=TipoServicio.ENTREGA, cliente=self.cliente, zona='Zona Test',
            direccion_destino='Calle 1', fecha_agenda=datetime.date.today(),
        )
        self.ruta = Ruta.objects.create(motorizado=self.motorizado, fecha=datetime.date.today())

    def test_flujo_completo_entrega(self):
        self.autenticar(self.alistador)
        r = self.client.post(f'/api/servicios/{self.servicio.id}/asignar-ruta/', {'ruta_id': self.ruta.id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['estado'], EstadoServicio.ASIGNADO)

        self.autenticar(self.motorizado)
        r = self.client.post(f'/api/servicios/{self.servicio.id}/recibir-en-centro/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['estado'], EstadoServicio.RECIBIDO_CENTRO)

        r = self.client.post(f'/api/servicios/{self.servicio.id}/iniciar-transito/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['estado'], EstadoServicio.EN_TRANSITO)

        r = self.client.post(f'/api/servicios/{self.servicio.id}/cerrar/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['estado'], EstadoServicio.ENTREGADO)

    def test_motorizado_no_asignado_no_puede_operar_el_servicio(self):
        self.servicio.estado = EstadoServicio.ASIGNADO
        self.servicio.ruta = self.ruta
        self.servicio.save()

        self.autenticar(self.otro_motorizado)
        r = self.client.post(f'/api/servicios/{self.servicio.id}/recibir-en-centro/')
        # get_queryset() ya filtra por ruta__motorizado=user, asi que el servicio
        # de otro motorizado ni siquiera es visible: 404, no 403 (evita filtrar
        # la existencia del recurso a quien no tiene acceso a el).
        self.assertEqual(r.status_code, 404)

    def test_recibir_en_centro_no_aplica_a_recoleccion(self):
        self.servicio.tipo = TipoServicio.RECOLECCION
        self.servicio.estado = EstadoServicio.ASIGNADO
        self.servicio.ruta = self.ruta
        self.servicio.save()

        self.autenticar(self.motorizado)
        r = self.client.post(f'/api/servicios/{self.servicio.id}/recibir-en-centro/')
        self.assertEqual(r.status_code, 400)


class CicloDeVidaRecoleccionTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.servicio = Servicio.objects.create(
            tipo=TipoServicio.RECOLECCION, cliente=self.cliente, zona='Zona Test',
            direccion_origen='Calle 1', fecha_agenda=datetime.date.today(),
        )
        self.ruta = Ruta.objects.create(motorizado=self.motorizado, fecha=datetime.date.today())
        self.servicio.ruta = self.ruta
        self.servicio.estado = EstadoServicio.ASIGNADO
        self.servicio.save()
        self.autenticar(self.motorizado)
        self.client.post(f'/api/servicios/{self.servicio.id}/iniciar-transito/')

    def test_cerrar_sin_evidencia_falla(self):
        r = self.client.post(f'/api/servicios/{self.servicio.id}/cerrar/')
        self.assertEqual(r.status_code, 400)

    def test_cerrar_con_evidencia_completa(self):
        r = self.client.post(f'/api/servicios/{self.servicio.id}/cerrar/', {
            'foto': imagen_de_prueba('foto.png'),
            'firma': imagen_de_prueba('firma.png'),
        }, format='multipart')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['estado'], EstadoServicio.RECOLECTADO)
        self.assertIsNotNone(r.data['evidencia'])


class NovedadTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.servicio = Servicio.objects.create(
            tipo=TipoServicio.ENTREGA, cliente=self.cliente, zona='Zona Test',
            direccion_destino='Calle 1', fecha_agenda=datetime.date.today(),
        )
        self.ruta = Ruta.objects.create(motorizado=self.motorizado, fecha=datetime.date.today())
        self.servicio.ruta = self.ruta
        self.servicio.estado = EstadoServicio.EN_TRANSITO
        self.servicio.save()
        self.autenticar(self.motorizado)

    def test_reintentar_deja_en_novedad_y_permite_reintentar_transito(self):
        r = self.client.post(f'/api/servicios/{self.servicio.id}/novedad/', {
            'tipo': 'CLIENTE_AUSENTE', 'detalle': 'Nadie en la direccion', 'accion': 'REINTENTAR',
        })
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data['estado'], EstadoServicio.NOVEDAD)

        r = self.client.post(f'/api/servicios/{self.servicio.id}/iniciar-transito/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['estado'], EstadoServicio.EN_TRANSITO)

    def test_devolver_deja_servicio_terminal(self):
        r = self.client.post(f'/api/servicios/{self.servicio.id}/novedad/', {
            'tipo': 'DIRECCION_ERRADA', 'detalle': 'No existe', 'accion': 'DEVOLVER_A_CENTRO',
        })
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data['estado'], EstadoServicio.DEVUELTO)

        r = self.client.post(f'/api/servicios/{self.servicio.id}/cerrar/')
        self.assertEqual(r.status_code, 400)


class MensajesChatTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.servicio = Servicio.objects.create(
            tipo=TipoServicio.ENTREGA, cliente=self.cliente, zona='Zona Test',
            direccion_destino='Calle 1', fecha_agenda=datetime.date.today(),
        )
        self.ruta = Ruta.objects.create(motorizado=self.motorizado, fecha=datetime.date.today())
        self.servicio.ruta = self.ruta
        self.servicio.save()

    def test_cliente_dueno_puede_enviar_y_leer_mensajes(self):
        self.autenticar(self.cliente)
        r = self.client.post(f'/api/servicios/{self.servicio.id}/mensajes/', {'texto': 'Hola'})
        self.assertEqual(r.status_code, 201)

        r = self.client.get(f'/api/servicios/{self.servicio.id}/mensajes/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)

    def test_otro_cliente_no_puede_acceder_al_chat(self):
        self.autenticar(self.otro_cliente)
        r = self.client.get(f'/api/servicios/{self.servicio.id}/mensajes/')
        # Mismo caso: el servicio no aparece en el queryset de otro_cliente -> 404.
        self.assertEqual(r.status_code, 404)

    def test_motorizado_asignado_puede_participar(self):
        self.autenticar(self.motorizado)
        r = self.client.post(f'/api/servicios/{self.servicio.id}/mensajes/', {'texto': 'En camino'})
        self.assertEqual(r.status_code, 201)


class ChatWebSocketTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.servicio = Servicio.objects.create(
            tipo=TipoServicio.ENTREGA, cliente=self.cliente, zona='Zona Test',
            direccion_destino='Calle 1', fecha_agenda=datetime.date.today(),
        )
        self.ruta = Ruta.objects.create(motorizado=self.motorizado, fecha=datetime.date.today())
        self.servicio.ruta = self.ruta
        self.servicio.save()

    async def test_mensaje_por_websocket_se_guarda_y_se_difunde(self):
        token_cliente = str(AccessToken.for_user(self.cliente))
        token_motorizado = str(AccessToken.for_user(self.motorizado))

        comm_cliente = WebsocketCommunicator(application, f'/ws/chat/{self.servicio.id}/?token={token_cliente}')
        comm_motorizado = WebsocketCommunicator(application, f'/ws/chat/{self.servicio.id}/?token={token_motorizado}')
        self.assertTrue((await comm_cliente.connect())[0])
        self.assertTrue((await comm_motorizado.connect())[0])

        await comm_motorizado.send_json_to({'texto': 'Voy en camino'})

        recibido_cliente = await comm_cliente.receive_json_from(timeout=2)
        recibido_motorizado = await comm_motorizado.receive_json_from(timeout=2)
        self.assertEqual(recibido_cliente['texto'], 'Voy en camino')
        self.assertEqual(recibido_motorizado['texto'], 'Voy en camino')

        from channels.db import database_sync_to_async
        total_mensajes = await database_sync_to_async(lambda: self.servicio.mensajes.count())()
        self.assertEqual(total_mensajes, 1)

        await comm_cliente.disconnect()
        await comm_motorizado.disconnect()

    async def test_no_autorizado_no_puede_conectarse_al_chat(self):
        token = str(AccessToken.for_user(self.otro_cliente))
        comm = WebsocketCommunicator(application, f'/ws/chat/{self.servicio.id}/?token={token}')
        connected, _ = await comm.connect()
        self.assertFalse(connected)


class PlanificarRecoleccionTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        Cobertura.objects.create(zona='Zona Test', leadtime_dias=2, dias_disponibles='LUN,MIE,VIE')
        self.autenticar(self.cliente)

    def test_planificar_respeta_leadtime(self):
        manana = datetime.date.today() + datetime.timedelta(days=1)
        r = self.client.post('/api/servicios/planificar/', {
            'zona': 'Zona Test', 'direccion_origen': 'Calle 1', 'fecha_agenda': manana.isoformat(),
        })
        self.assertEqual(r.status_code, 400)

    def test_planificar_fecha_valida_crea_recoleccion(self):
        cursor = datetime.date.today() + datetime.timedelta(days=2)
        while cursor.weekday() not in (0, 2, 4):
            cursor += datetime.timedelta(days=1)

        r = self.client.post('/api/servicios/planificar/', {
            'zona': 'Zona Test', 'direccion_origen': 'Calle 1', 'fecha_agenda': cursor.isoformat(),
        })
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data['tipo'], TipoServicio.RECOLECCION)
        self.assertEqual(r.data['estado'], EstadoServicio.CREADO)
