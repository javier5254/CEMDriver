import hashlib
import json
from unittest.mock import MagicMock, patch

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from testutils import BaseAPITestCase

from .authentication import ApiKeyAuthentication
from .models import ApiKey, WebhookDelivery, WebhookEndpoint
from .services import disparar_webhook, firmar


class ApiKeyEndpointTests(BaseAPITestCase):
    def test_solo_admin_puede_crear_api_key(self):
        for usuario in (self.motorizado, self.alistador, self.cliente):
            self.autenticar(usuario)
            response = self.client.post('/api/integraciones/api-keys/', {
                'nombre': 'Tienda XYZ', 'actua_como': self.alistador.id,
            })
            self.assertEqual(response.status_code, 403)

    def test_solo_admin_puede_listar_api_keys(self):
        self.autenticar(self.motorizado)
        response = self.client.get('/api/integraciones/api-keys/')
        self.assertEqual(response.status_code, 403)

    def test_admin_puede_crear_api_key_y_recibe_la_llave_una_sola_vez(self):
        self.autenticar(self.admin)
        response = self.client.post('/api/integraciones/api-keys/', {
            'nombre': 'Tienda XYZ', 'actua_como': self.alistador.id,
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('key', response.data)
        raw_key = response.data['key']
        self.assertGreater(len(raw_key), 20)
        self.assertEqual(response.data['prefix'], raw_key[:8])

        # La llave cruda nunca se vuelve a exponer en el listado.
        response_list = self.client.get('/api/integraciones/api-keys/')
        self.assertEqual(response_list.status_code, 200)
        for item in response_list.data:
            self.assertNotIn('key', item)
            self.assertNotIn('key_hash', item)

        # En BD solo se guarda el hash, nunca la llave cruda.
        api_key = ApiKey.objects.get(nombre='Tienda XYZ')
        self.assertNotEqual(api_key.key_hash, raw_key)
        self.assertEqual(api_key.key_hash, hashlib.sha256(raw_key.encode()).hexdigest())

    def test_actua_como_debe_ser_alistador(self):
        self.autenticar(self.admin)
        response = self.client.post('/api/integraciones/api-keys/', {
            'nombre': 'Invalida', 'actua_como': self.cliente.id,
        })
        self.assertEqual(response.status_code, 400)

    def test_patch_permite_alternar_activa(self):
        self.autenticar(self.admin)
        instancia, _raw = ApiKey.generar(nombre='Original', actua_como=self.alistador)
        response = self.client.patch(
            f'/api/integraciones/api-keys/{instancia.id}/', {'activa': False}, format='json',
        )
        self.assertEqual(response.status_code, 200)
        instancia.refresh_from_db()
        self.assertFalse(instancia.activa)

    def test_delete_elimina_la_llave(self):
        self.autenticar(self.admin)
        instancia, _raw = ApiKey.generar(nombre='Borrar', actua_como=self.alistador)
        response = self.client.delete(f'/api/integraciones/api-keys/{instancia.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(ApiKey.objects.filter(id=instancia.id).exists())


class WebhookEndpointTests(BaseAPITestCase):
    def test_solo_admin_puede_gestionar_webhooks(self):
        for usuario in (self.motorizado, self.alistador, self.cliente):
            self.autenticar(usuario)
            response = self.client.post('/api/integraciones/webhooks/', {
                'nombre': 'ERP Cliente', 'url': 'https://erp.example.com/hook',
                'eventos': 'servicio.entregado',
            })
            self.assertEqual(response.status_code, 403)

    def test_admin_puede_crear_webhook_y_secret_se_autogenera(self):
        self.autenticar(self.admin)
        response = self.client.post('/api/integraciones/webhooks/', {
            'nombre': 'ERP Cliente', 'url': 'https://erp.example.com/hook',
            'eventos': 'servicio.entregado,servicio.novedad',
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['secret'])

        # El listado no expone el secret...
        response_list = self.client.get('/api/integraciones/webhooks/')
        self.assertEqual(response_list.status_code, 200)
        for item in response_list.data:
            self.assertNotIn('secret', item)

        # ...pero el detalle si (decision documentada en serializers.py).
        endpoint_id = response.data['id']
        response_detail = self.client.get(f'/api/integraciones/webhooks/{endpoint_id}/')
        self.assertEqual(response_detail.status_code, 200)
        self.assertIn('secret', response_detail.data)
        self.assertEqual(response_detail.data['secret'], response.data['secret'])

    def test_eventos_invalidos_son_rechazados(self):
        self.autenticar(self.admin)
        response = self.client.post('/api/integraciones/webhooks/', {
            'nombre': 'ERP Cliente', 'url': 'https://erp.example.com/hook',
            'eventos': 'servicio.no_existe',
        })
        self.assertEqual(response.status_code, 400)

    def test_entregas_endpoint_lista_bitacora_solo_para_admin(self):
        endpoint = WebhookEndpoint.objects.create(
            nombre='ERP', url='https://erp.example.com/hook', eventos='servicio.entregado',
        )
        WebhookDelivery.objects.create(
            endpoint=endpoint, evento='servicio.entregado', payload={'id': 1},
            status_code=200, exito=True,
        )

        self.autenticar(self.alistador)
        response = self.client.get(f'/api/integraciones/webhooks/{endpoint.id}/entregas/')
        self.assertEqual(response.status_code, 403)

        self.autenticar(self.admin)
        response = self.client.get(f'/api/integraciones/webhooks/{endpoint.id}/entregas/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['evento'], 'servicio.entregado')


class ApiKeyAuthenticationTests(BaseAPITestCase):
    @staticmethod
    def _request_con_header(raw_key=None):
        factory = APIRequestFactory()
        kwargs = {}
        if raw_key is not None:
            kwargs['HTTP_X_API_KEY'] = raw_key
        django_request = factory.get('/api/servicios/', **kwargs)
        return Request(django_request)

    def test_sin_header_retorna_none(self):
        auth = ApiKeyAuthentication()
        self.assertIsNone(auth.authenticate(self._request_con_header()))

    def test_llave_valida_autentica_como_actua_como_y_actualiza_ultimo_uso(self):
        instancia, raw_key = ApiKey.generar(nombre='Tienda', actua_como=self.alistador)
        self.assertIsNone(instancia.ultimo_uso)

        auth = ApiKeyAuthentication()
        usuario, aux = auth.authenticate(self._request_con_header(raw_key))
        self.assertEqual(usuario.id, self.alistador.id)
        self.assertIsNone(aux)

        instancia.refresh_from_db()
        self.assertIsNotNone(instancia.ultimo_uso)

    def test_llave_inexistente_lanza_authentication_failed(self):
        auth = ApiKeyAuthentication()
        with self.assertRaises(AuthenticationFailed):
            auth.authenticate(self._request_con_header('llave-que-no-existe'))

    def test_llave_inactiva_es_rechazada(self):
        instancia, raw_key = ApiKey.generar(nombre='Tienda', actua_como=self.alistador)
        instancia.activa = False
        instancia.save()

        auth = ApiKeyAuthentication()
        with self.assertRaises(AuthenticationFailed):
            auth.authenticate(self._request_con_header(raw_key))


class DispararWebhookTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.endpoint = WebhookEndpoint.objects.create(
            nombre='ERP', url='https://erp.example.com/hook',
            eventos='servicio.entregado,servicio.novedad',
        )

    def test_evento_no_suscrito_no_genera_entrega(self):
        disparar_webhook('servicio.creado', {'id': 1})
        self.assertEqual(WebhookDelivery.objects.count(), 0)

    @patch('integrations.services.urllib.request.urlopen')
    def test_endpoint_inactivo_no_recibe_webhooks(self, mock_urlopen):
        self.endpoint.activo = False
        self.endpoint.save()
        disparar_webhook('servicio.entregado', {'id': 1})
        mock_urlopen.assert_not_called()
        self.assertEqual(WebhookDelivery.objects.count(), 0)

    @patch('integrations.services.urllib.request.urlopen')
    def test_envio_exitoso_registra_entrega_y_firma_correcta(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        payload = {'servicio_id': 42, 'estado': 'ENTREGADO'}
        disparar_webhook('servicio.entregado', payload)

        self.assertEqual(mock_urlopen.call_count, 1)
        entrega = WebhookDelivery.objects.get()
        self.assertTrue(entrega.exito)
        self.assertEqual(entrega.status_code, 200)
        self.assertEqual(entrega.evento, 'servicio.entregado')
        self.assertEqual(entrega.payload, payload)
        self.assertEqual(entrega.error, '')

        sent_request = mock_urlopen.call_args[0][0]
        body_bytes = sent_request.data
        self.assertEqual(json.loads(body_bytes), payload)

        headers_lower = {k.lower(): v for k, v in sent_request.headers.items()}
        firma_enviada = headers_lower.get('x-cmedriver-signature')
        firma_esperada = firmar(body_bytes, self.endpoint.secret)
        self.assertEqual(firma_enviada, firma_esperada)

    @patch('integrations.services.urllib.request.urlopen')
    def test_fallo_de_red_no_propaga_excepcion_y_registra_error(self, mock_urlopen):
        mock_urlopen.side_effect = ConnectionError('conexion rechazada')

        try:
            disparar_webhook('servicio.entregado', {'servicio_id': 1})
        except Exception as exc:  # pragma: no cover - esto NO deberia pasar nunca
            self.fail(f'disparar_webhook no debe propagar excepciones, pero lanzo: {exc}')

        entrega = WebhookDelivery.objects.get()
        self.assertFalse(entrega.exito)
        self.assertIsNone(entrega.status_code)
        self.assertIn('conexion rechazada', entrega.error)

    @patch('integrations.services.urllib.request.urlopen')
    def test_multiples_endpoints_suscritos_reciben_el_evento(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        WebhookEndpoint.objects.create(
            nombre='Otro ERP', url='https://otro.example.com/hook', eventos='servicio.entregado',
        )
        disparar_webhook('servicio.entregado', {'id': 1})
        self.assertEqual(mock_urlopen.call_count, 2)
        self.assertEqual(WebhookDelivery.objects.count(), 2)
