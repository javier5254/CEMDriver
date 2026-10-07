import datetime

from testutils import BaseAPITestCase

from coverage.models import Cobertura
from inventory.models import Producto
from payments.models import EstadoPago, Pago
from services.models import EstadoServicio, Servicio, TipoServicio


class ChatbotComprarTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        Cobertura.objects.create(
            zona='Zona Test', leadtime_dias=1, dias_disponibles='LUN,MAR,MIE,JUE,VIE,SAB,DOM',
        )
        self.producto = Producto.objects.create(
            sku='CB-001', nombre='Termo', precio=25000, stock=5,
            centro_mensajeria='Centro Test', disponible_chatbot=True,
        )
        self.autenticar(self.cliente)

    @staticmethod
    def _fecha_valida(dias=2):
        return (datetime.date.today() + datetime.timedelta(days=dias)).isoformat()

    def test_flujo_completo_de_compra_crea_servicio_y_pago(self):
        r1 = self.client.post('/api/chatbot/mensaje/', {'texto': 'Quiero comprar Termo'}, format='json')
        self.assertEqual(r1.status_code, 201)
        conversacion_id = r1.data['conversacion_id']
        self.assertIn('zona', r1.data['respuesta'].lower())
        self.assertIsNone(r1.data['accion'])

        r2 = self.client.post('/api/chatbot/mensaje/', {
            'conversacion_id': conversacion_id,
            'texto': 'Zona Test, Calle 10 # 5-20',
        }, format='json')
        self.assertEqual(r2.status_code, 201)
        self.assertIsNone(r2.data['accion'])

        r3 = self.client.post('/api/chatbot/mensaje/', {
            'conversacion_id': conversacion_id,
            'texto': self._fecha_valida(),
        }, format='json')
        self.assertEqual(r3.status_code, 201)
        self.assertIsNotNone(r3.data['accion'])
        self.assertEqual(r3.data['accion']['tipo'], 'pago')

        servicio = Servicio.objects.get(pk=r3.data['accion']['servicio_id'])
        self.assertEqual(servicio.tipo, TipoServicio.ENTREGA)
        self.assertEqual(servicio.producto_id, self.producto.id)
        self.assertEqual(servicio.cliente_id, self.cliente.id)

        pago = Pago.objects.get(pk=r3.data['accion']['pago_id'])
        self.assertEqual(pago.servicio_id, servicio.id)
        self.assertEqual(pago.producto_id, self.producto.id)
        self.assertIn(pago.estado, (EstadoPago.APROBADO, EstadoPago.RECHAZADO))

    def test_producto_mencionado_directamente_salta_el_listado(self):
        r = self.client.post('/api/chatbot/mensaje/', {'texto': 'comprar Termo'}, format='json')
        self.assertEqual(r.status_code, 201)
        # No debe listar el catalogo completo, sino ir directo a pedir zona/direccion.
        self.assertNotIn('sku', str(r.data.get('accion')))

    def test_elegir_producto_en_un_turno_separado_completa_la_compra(self):
        # Regresion: pedir "quiero comprar" sin nombrar el producto (se lista
        # el catalogo), y elegirlo en el SIGUIENTE mensaje, en vez de en el
        # mismo turno. Antes de la correccion esto perdia el producto_id en
        # el contexto y el turno de la fecha reventaba con KeyError.
        r1 = self.client.post('/api/chatbot/mensaje/', {'texto': 'quiero comprar'}, format='json')
        self.assertEqual(r1.status_code, 201)
        conversacion_id = r1.data['conversacion_id']
        self.assertIn('termo', r1.data['respuesta'].lower())

        r2 = self.client.post('/api/chatbot/mensaje/', {
            'conversacion_id': conversacion_id, 'texto': 'Termo',
        }, format='json')
        self.assertEqual(r2.status_code, 201)
        self.assertIn('zona', r2.data['respuesta'].lower())

        r3 = self.client.post('/api/chatbot/mensaje/', {
            'conversacion_id': conversacion_id, 'texto': 'Zona Test, Calle 10 # 5-20',
        }, format='json')
        self.assertEqual(r3.status_code, 201)

        r4 = self.client.post('/api/chatbot/mensaje/', {
            'conversacion_id': conversacion_id, 'texto': self._fecha_valida(),
        }, format='json')
        self.assertEqual(r4.status_code, 201)
        self.assertIsNotNone(r4.data['accion'])
        self.assertEqual(r4.data['accion']['tipo'], 'pago')

        servicio = Servicio.objects.get(pk=r4.data['accion']['servicio_id'])
        self.assertEqual(servicio.producto_id, self.producto.id)


class ChatbotRecoleccionTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        Cobertura.objects.create(
            zona='Zona Test', leadtime_dias=3, dias_disponibles='LUN,MAR,MIE,JUE,VIE,SAB,DOM',
        )
        self.autenticar(self.cliente)

    def test_recoleccion_rechaza_fecha_que_viola_el_leadtime_sin_500(self):
        r1 = self.client.post('/api/chatbot/mensaje/', {'texto': 'Quiero que recojan un paquete'}, format='json')
        self.assertEqual(r1.status_code, 201)
        conv_id = r1.data['conversacion_id']

        r2 = self.client.post('/api/chatbot/mensaje/', {
            'conversacion_id': conv_id, 'texto': 'Zona Test, Calle 1',
        }, format='json')
        self.assertEqual(r2.status_code, 201)

        fecha_muy_pronto = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
        r3 = self.client.post('/api/chatbot/mensaje/', {
            'conv': None, 'conversacion_id': conv_id, 'texto': fecha_muy_pronto,
        }, format='json')
        self.assertEqual(r3.status_code, 201)  # nunca un 500, el rechazo va en la respuesta del bot
        self.assertIsNone(r3.data['accion'])
        self.assertIn('leadtime', r3.data['respuesta'].lower())
        self.assertEqual(Servicio.objects.filter(tipo=TipoServicio.RECOLECCION).count(), 0)

    def test_recoleccion_con_fecha_valida_crea_el_servicio(self):
        r1 = self.client.post('/api/chatbot/mensaje/', {'texto': 'Necesito una recoleccion'}, format='json')
        conv_id = r1.data['conversacion_id']

        self.client.post('/api/chatbot/mensaje/', {
            'conversacion_id': conv_id, 'texto': 'Zona Test, Calle 1',
        }, format='json')

        fecha_valida = (datetime.date.today() + datetime.timedelta(days=4)).isoformat()
        r3 = self.client.post('/api/chatbot/mensaje/', {
            'conversacion_id': conv_id, 'texto': fecha_valida,
        }, format='json')
        self.assertEqual(r3.status_code, 201)
        self.assertEqual(r3.data['accion']['tipo'], 'servicio_creado')

        servicio = Servicio.objects.get(pk=r3.data['accion']['servicio_id'])
        self.assertEqual(servicio.tipo, TipoServicio.RECOLECCION)
        self.assertEqual(servicio.estado, EstadoServicio.CREADO)
        self.assertEqual(servicio.zona, 'Zona Test')
        self.assertEqual(servicio.direccion_origen, 'Calle 1')

    def test_puede_reintentar_con_otra_fecha_tras_un_rechazo(self):
        r1 = self.client.post('/api/chatbot/mensaje/', {'texto': 'recoleccion por favor'}, format='json')
        conv_id = r1.data['conversacion_id']
        self.client.post('/api/chatbot/mensaje/', {
            'conversacion_id': conv_id, 'texto': 'Zona Test, Calle 1',
        }, format='json')

        fecha_muy_pronto = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
        r_rechazo = self.client.post('/api/chatbot/mensaje/', {
            'conversacion_id': conv_id, 'texto': fecha_muy_pronto,
        }, format='json')
        self.assertIsNone(r_rechazo.data['accion'])

        fecha_valida = (datetime.date.today() + datetime.timedelta(days=5)).isoformat()
        r_ok = self.client.post('/api/chatbot/mensaje/', {
            'conversacion_id': conv_id, 'texto': fecha_valida,
        }, format='json')
        self.assertEqual(r_ok.data['accion']['tipo'], 'servicio_creado')


class ChatbotSaludoYFallbackTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.autenticar(self.cliente)

    def test_saludo_ofrece_el_menu_de_opciones(self):
        r = self.client.post('/api/chatbot/mensaje/', {'texto': 'Hola'}, format='json')
        self.assertEqual(r.status_code, 201)
        self.assertIsNone(r.data['accion'])
        self.assertIn('comprar', r.data['respuesta'].lower())
        self.assertIn('recol', r.data['respuesta'].lower())

    def test_mensaje_no_reconocido_da_una_respuesta_amigable_sin_500(self):
        r = self.client.post('/api/chatbot/mensaje/', {'texto': 'asdkjaslkdjaslkd zzz'}, format='json')
        self.assertEqual(r.status_code, 201)
        self.assertIsNone(r.data['accion'])
        self.assertTrue(len(r.data['respuesta']) > 0)

    def test_texto_vacio_es_rechazado_con_400_no_con_500(self):
        r = self.client.post('/api/chatbot/mensaje/', {'texto': ''}, format='json')
        self.assertEqual(r.status_code, 400)


class ChatbotPermisosTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.autenticar(self.cliente)
        r = self.client.post('/api/chatbot/mensaje/', {'texto': 'hola'}, format='json')
        self.conv_id = r.data['conversacion_id']

    def test_dueno_puede_leer_su_historial(self):
        r = self.client.get(f'/api/chatbot/conversaciones/{self.conv_id}/mensajes/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 2)  # mensaje del cliente + respuesta del bot

    def test_otro_cliente_no_puede_leer_la_conversacion_ajena(self):
        self.autenticar(self.otro_cliente)
        r = self.client.get(f'/api/chatbot/conversaciones/{self.conv_id}/mensajes/')
        self.assertEqual(r.status_code, 403)

    def test_roles_distintos_de_cliente_no_pueden_usar_el_chatbot(self):
        for usuario in (self.admin, self.alistador, self.motorizado):
            self.autenticar(usuario)
            r = self.client.post('/api/chatbot/mensaje/', {'texto': 'hola'}, format='json')
            self.assertEqual(r.status_code, 403)
