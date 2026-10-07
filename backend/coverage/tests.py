import datetime

from testutils import BaseAPITestCase

from .models import Cobertura


class CoberturaTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.cobertura = Cobertura.objects.create(
            zona='Zona Test',
            leadtime_dias=2,
            dias_disponibles='LUN,MIE,VIE',
        )

    def test_solo_admin_puede_crear_cobertura(self):
        self.autenticar(self.alistador)
        response = self.client.post('/api/cobertura/', {
            'zona': 'Otra zona',
            'leadtime_dias': 1,
            'dias_disponibles': 'LUN,MAR',
        })
        self.assertEqual(response.status_code, 403)

    def test_cualquier_autenticado_puede_leer_cobertura(self):
        self.autenticar(self.cliente)
        response = self.client.get('/api/cobertura/')
        self.assertEqual(response.status_code, 200)

    def test_agenda_disponible_respeta_leadtime_y_dias_habiles(self):
        self.autenticar(self.cliente)
        response = self.client.get('/api/cobertura/agenda-disponible/', {'zona': 'Zona Test'})
        self.assertEqual(response.status_code, 200)

        hoy = datetime.date.today()
        primera_fecha_posible = hoy + datetime.timedelta(days=2)
        for fecha_str in response.data['fechas_disponibles']:
            fecha = datetime.date.fromisoformat(fecha_str)
            self.assertGreaterEqual(fecha, primera_fecha_posible)
            self.assertIn(fecha.weekday(), (0, 2, 4))  # LUN, MIE, VIE

    def test_agenda_disponible_zona_inexistente_devuelve_404(self):
        self.autenticar(self.cliente)
        response = self.client.get('/api/cobertura/agenda-disponible/', {'zona': 'No existe'})
        self.assertEqual(response.status_code, 404)
