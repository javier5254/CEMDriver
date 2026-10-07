from unittest.mock import patch

from testutils import BaseAPITestCase

from .models import EstadoPago, Pago
from .provider import MockPaymentProvider


class MockPaymentProviderTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.pago = Pago.objects.create(cliente=self.cliente, monto=1000)

    def test_referencia_es_unica(self):
        otro = Pago.objects.create(cliente=self.cliente, monto=2000)
        self.assertNotEqual(self.pago.referencia, otro.referencia)

    @patch('payments.provider.random.random', return_value=0.5)
    def test_procesar_aprueba_cuando_no_cae_en_el_porcentaje_de_rechazo(self, _mock_random):
        pago = MockPaymentProvider().procesar(self.pago)
        self.assertEqual(pago.estado, EstadoPago.APROBADO)

    @patch('payments.provider.random.random', return_value=0.01)
    def test_procesar_rechaza_cuando_cae_en_el_porcentaje_simulado(self, _mock_random):
        pago = MockPaymentProvider().procesar(self.pago)
        self.assertEqual(pago.estado, EstadoPago.RECHAZADO)

    def test_procesar_nunca_deja_el_pago_en_pendiente(self):
        for _ in range(20):
            pago = Pago.objects.create(cliente=self.cliente, monto=500)
            MockPaymentProvider().procesar(pago)
            self.assertIn(pago.estado, (EstadoPago.APROBADO, EstadoPago.RECHAZADO))


class PagoDetailViewTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.pago = Pago.objects.create(cliente=self.cliente, monto=1000, estado=EstadoPago.APROBADO)

    def test_dueno_puede_leer_su_pago(self):
        self.autenticar(self.cliente)
        r = self.client.get(f'/api/pagos/{self.pago.id}/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['estado'], EstadoPago.APROBADO)
        self.assertEqual(r.data['referencia'], self.pago.referencia)

    def test_admin_puede_leer_cualquier_pago(self):
        self.autenticar(self.admin)
        r = self.client.get(f'/api/pagos/{self.pago.id}/')
        self.assertEqual(r.status_code, 200)

    def test_otro_cliente_no_puede_leer_el_pago(self):
        self.autenticar(self.otro_cliente)
        r = self.client.get(f'/api/pagos/{self.pago.id}/')
        self.assertEqual(r.status_code, 403)

    def test_alistador_no_puede_leer_el_pago(self):
        self.autenticar(self.alistador)
        r = self.client.get(f'/api/pagos/{self.pago.id}/')
        self.assertEqual(r.status_code, 403)

    def test_pago_inexistente_da_404(self):
        self.autenticar(self.admin)
        r = self.client.get('/api/pagos/9999/')
        self.assertEqual(r.status_code, 404)
