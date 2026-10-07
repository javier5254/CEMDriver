import datetime
from unittest.mock import patch

from channels.testing import WebsocketCommunicator
from rest_framework_simplejwt.tokens import AccessToken
from testutils import BaseAPITestCase

from cmedriver.asgi import application
from optimization.models import PuntoGeocodificado
from services.models import EstadoServicio, Ruta, Servicio, TipoServicio


class TrackingTests(BaseAPITestCase):
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

    def test_motorizado_asignado_puede_reportar_posicion(self):
        self.autenticar(self.motorizado)
        r = self.client.post('/api/tracking/posicion/', {
            'servicio': self.servicio.id, 'lat': 4.65, 'lng': -74.05,
        })
        self.assertEqual(r.status_code, 201)

    def test_motorizado_no_asignado_no_puede_reportar_posicion(self):
        self.autenticar(self.otro_motorizado)
        r = self.client.post('/api/tracking/posicion/', {
            'servicio': self.servicio.id, 'lat': 4.65, 'lng': -74.05,
        })
        self.assertEqual(r.status_code, 403)

    def test_cliente_dueno_puede_ver_ultima_posicion(self):
        self.autenticar(self.motorizado)
        self.client.post('/api/tracking/posicion/', {
            'servicio': self.servicio.id, 'lat': 4.65, 'lng': -74.05,
        })

        self.autenticar(self.cliente)
        r = self.client.get('/api/tracking/ultima-posicion/', {'servicio_id': self.servicio.id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(float(r.data['lat']), 4.65)

    def test_otro_cliente_no_puede_ver_la_posicion(self):
        self.autenticar(self.motorizado)
        self.client.post('/api/tracking/posicion/', {
            'servicio': self.servicio.id, 'lat': 4.65, 'lng': -74.05,
        })

        self.autenticar(self.otro_cliente)
        r = self.client.get('/api/tracking/ultima-posicion/', {'servicio_id': self.servicio.id})
        self.assertEqual(r.status_code, 403)


class DestinoTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.servicio = Servicio.objects.create(
            tipo=TipoServicio.ENTREGA, cliente=self.cliente, zona='Zona Test',
            direccion_destino='Calle 1', fecha_agenda=datetime.date.today(),
        )
        self.ruta = Ruta.objects.create(motorizado=self.motorizado, fecha=datetime.date.today())
        self.servicio.ruta = self.ruta
        self.servicio.save()

    @patch('tracking.views.geocodificar', return_value=(4.7, -74.05))
    def test_geocodifica_y_cachea_el_destino(self, mock_geocodificar):
        self.autenticar(self.cliente)
        r = self.client.get('/api/tracking/destino/', {'servicio_id': self.servicio.id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(float(r.data['lat']), 4.7)
        mock_geocodificar.assert_called_once()

        # segunda llamada: debe usar el cache, no geocodificar de nuevo
        r2 = self.client.get('/api/tracking/destino/', {'servicio_id': self.servicio.id})
        self.assertEqual(r2.status_code, 200)
        mock_geocodificar.assert_called_once()
        self.assertEqual(PuntoGeocodificado.objects.filter(servicio=self.servicio).count(), 1)

    @patch('tracking.views.geocodificar', return_value=None)
    def test_geocoding_fallido_devuelve_404_no_500(self, mock_geocodificar):
        self.autenticar(self.cliente)
        r = self.client.get('/api/tracking/destino/', {'servicio_id': self.servicio.id})
        self.assertEqual(r.status_code, 404)

    def test_otro_cliente_no_puede_ver_el_destino(self):
        self.autenticar(self.otro_cliente)
        r = self.client.get('/api/tracking/destino/', {'servicio_id': self.servicio.id})
        self.assertEqual(r.status_code, 403)


class TrackingWebSocketTests(BaseAPITestCase):
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

    async def test_cliente_dueno_recibe_posicion_en_tiempo_real(self):
        token = str(AccessToken.for_user(self.cliente))
        comm = WebsocketCommunicator(application, f'/ws/tracking/{self.servicio.id}/?token={token}')
        connected, _ = await comm.connect()
        self.assertTrue(connected)

        from channels.db import database_sync_to_async

        @database_sync_to_async
        def reportar_posicion():
            from django.test import Client
            client = Client()
            client.force_login(self.motorizado)
            # Reutiliza el endpoint REST real para disparar el broadcast, en
            # vez de llamar a la vista directamente, para probar el camino
            # completo (POST -> guarda -> group_send).
            from rest_framework.test import APIClient
            api = APIClient()
            api.force_authenticate(user=self.motorizado)
            return api.post('/api/tracking/posicion/', {
                'servicio': self.servicio.id, 'lat': 4.71, 'lng': -74.05,
            })

        response = await reportar_posicion()
        self.assertEqual(response.status_code, 201)

        mensaje = await comm.receive_json_from(timeout=2)
        self.assertEqual(mensaje['servicio'], self.servicio.id)
        self.assertEqual(float(mensaje['lat']), 4.71)

        await comm.disconnect()

    async def test_usuario_no_autorizado_no_puede_conectarse(self):
        token = str(AccessToken.for_user(self.otro_cliente))
        comm = WebsocketCommunicator(application, f'/ws/tracking/{self.servicio.id}/?token={token}')
        connected, _ = await comm.connect()
        self.assertFalse(connected)
