import datetime
from unittest.mock import patch

from testutils import BaseAPITestCase

from services.models import EstadoServicio, Ruta, Servicio, TipoServicio

from .models import PuntoGeocodificado


class OptimizarRutaTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.ruta = Ruta.objects.create(motorizado=self.motorizado, fecha=datetime.date.today())
        # El rate-limit de Nominatim (~1.1s entre llamados reales) no aporta nada
        # en tests que ya mockean la geocodificacion; lo neutralizamos para que la
        # suite corra rapido.
        sleep_patcher = patch('optimization.views.time.sleep')
        sleep_patcher.start()
        self.addCleanup(sleep_patcher.stop)

    def _crear_servicio(self, direccion_destino, zona='Zona Test', ruta=None):
        return Servicio.objects.create(
            tipo=TipoServicio.ENTREGA,
            cliente=self.cliente,
            zona=zona,
            direccion_destino=direccion_destino,
            fecha_agenda=datetime.date.today(),
            estado=EstadoServicio.ASIGNADO,
            ruta=ruta if ruta is not None else self.ruta,
        )

    # --- permisos ---

    def test_admin_puede_optimizar(self):
        self._crear_servicio('Calle 1')
        self.autenticar(self.admin)
        with patch('optimization.views.geocodificar', return_value=(4.0, -74.0)):
            response = self.client.post(f'/api/optimizacion/rutas/{self.ruta.id}/')
        self.assertEqual(response.status_code, 200)

    def test_alistador_puede_optimizar(self):
        self._crear_servicio('Calle 1')
        self.autenticar(self.alistador)
        with patch('optimization.views.geocodificar', return_value=(4.0, -74.0)):
            response = self.client.post(f'/api/optimizacion/rutas/{self.ruta.id}/')
        self.assertEqual(response.status_code, 200)

    def test_motorizado_no_puede_optimizar(self):
        self._crear_servicio('Calle 1')
        self.autenticar(self.motorizado)
        response = self.client.post(f'/api/optimizacion/rutas/{self.ruta.id}/')
        self.assertEqual(response.status_code, 403)

    def test_cliente_no_puede_optimizar(self):
        self._crear_servicio('Calle 1')
        self.autenticar(self.cliente)
        response = self.client.post(f'/api/optimizacion/rutas/{self.ruta.id}/')
        self.assertEqual(response.status_code, 403)

    def test_ruta_inexistente_devuelve_404(self):
        self.autenticar(self.admin)
        response = self.client.post('/api/optimizacion/rutas/99999/')
        self.assertEqual(response.status_code, 404)

    # --- heuristico nearest-neighbor ---

    def test_orden_sugerido_sigue_al_vecino_mas_cercano(self):
        # Tres puntos sobre una linea recta de latitud (mismo lng). Se crean en
        # este orden (= orden "original" que usa la vista, por id ascendente):
        # inicio (lat 0.0), lejano (lat 0.05), cercano (lat 0.01). El heuristico
        # arranca en el primero creado (inicio) y desde ahi el vecino mas cercano
        # es "cercano" (0.01) y no "lejano" (0.05).
        s_inicio = self._crear_servicio('Inicio')      # lat 0.0 (primero creado -> punto de partida)
        s_lejano = self._crear_servicio('Lejano')      # lat 0.05
        s_cercano = self._crear_servicio('Cercano')    # lat 0.01

        coords = {
            s_lejano.id: (0.05, 0.0),
            s_inicio.id: (0.0, 0.0),
            s_cercano.id: (0.01, 0.0),
        }

        def side_effect(direccion):
            # direccion tiene forma "<direccion_destino>, <zona>, Colombia"; mapeamos
            # por el texto de la direccion en vez del id (mas realista).
            if direccion.startswith('Lejano'):
                return coords[s_lejano.id]
            if direccion.startswith('Inicio'):
                return coords[s_inicio.id]
            if direccion.startswith('Cercano'):
                return coords[s_cercano.id]
            return None

        self.autenticar(self.admin)
        with patch('optimization.views.geocodificar', side_effect=side_effect) as mock_geo:
            response = self.client.post(f'/api/optimizacion/rutas/{self.ruta.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_geo.call_count, 3)

        orden_ids = [p['servicio_id'] for p in response.data['orden_sugerido']]
        # Arranca en s_inicio (primero geocodificado en el orden original de la
        # queryset), y el vecino mas cercano desde ahi es s_cercano (0.01) antes
        # que s_lejano (0.05).
        self.assertEqual(orden_ids, [s_inicio.id, s_cercano.id, s_lejano.id])
        self.assertEqual(response.data['no_geocodificados'], [])
        self.assertGreater(response.data['distancia_total_km'], 0)

    def test_servicio_no_geocodificable_se_excluye_y_no_rompe_la_respuesta(self):
        s_ok = self._crear_servicio('Direccion valida')
        s_falla = self._crear_servicio('Direccion inexistente')

        def side_effect(direccion):
            if direccion.startswith('Direccion valida'):
                return (4.0, -74.0)
            return None

        self.autenticar(self.admin)
        with patch('optimization.views.geocodificar', side_effect=side_effect):
            response = self.client.post(f'/api/optimizacion/rutas/{self.ruta.id}/')

        self.assertEqual(response.status_code, 200)
        orden_ids = [p['servicio_id'] for p in response.data['orden_sugerido']]
        self.assertEqual(orden_ids, [s_ok.id])

        fallidos_ids = [f['servicio_id'] for f in response.data['no_geocodificados']]
        self.assertEqual(fallidos_ids, [s_falla.id])
        self.assertEqual(response.data['distancia_total_km'], 0.0)

    # --- cache ---

    def test_segunda_llamada_usa_el_cache_y_no_vuelve_a_geocodificar(self):
        servicio = self._crear_servicio('Calle repetida')

        self.autenticar(self.admin)
        with patch('optimization.views.geocodificar', return_value=(4.0, -74.0)) as mock_geo:
            response1 = self.client.post(f'/api/optimizacion/rutas/{self.ruta.id}/')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(mock_geo.call_count, 1)
        self.assertEqual(PuntoGeocodificado.objects.filter(servicio=servicio).count(), 1)

        with patch('optimization.views.geocodificar', return_value=(4.0, -74.0)) as mock_geo_2:
            response2 = self.client.post(f'/api/optimizacion/rutas/{self.ruta.id}/')
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(mock_geo_2.call_count, 0)
