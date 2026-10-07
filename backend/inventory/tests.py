from testutils import BaseAPITestCase

from .models import Producto


class InventarioTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.disponible = Producto.objects.create(
            sku='T-001', nombre='Disponible', precio=1000, stock=5,
            centro_mensajeria='Centro Test', disponible_chatbot=True,
        )
        Producto.objects.create(
            sku='T-002', nombre='Sin stock', precio=1000, stock=0,
            centro_mensajeria='Centro Test', disponible_chatbot=True,
        )
        Producto.objects.create(
            sku='T-003', nombre='No publicado', precio=1000, stock=10,
            centro_mensajeria='Centro Test', disponible_chatbot=False,
        )

    def test_solo_admin_puede_crear_producto(self):
        # El inventario es responsabilidad exclusiva del administrador: ni
        # alistador ni motorizado pueden crear/editar productos.
        for usuario in (self.motorizado, self.alistador, self.cliente):
            self.autenticar(usuario)
            response = self.client.post('/api/productos/', {
                'sku': 'T-004', 'nombre': 'X', 'precio': 100, 'stock': 1, 'centro_mensajeria': 'C',
            })
            self.assertEqual(response.status_code, 403)

        self.autenticar(self.admin)
        response = self.client.post('/api/productos/', {
            'sku': 'T-004', 'nombre': 'X', 'precio': 100, 'stock': 1, 'centro_mensajeria': 'C',
        })
        self.assertEqual(response.status_code, 201)

    def test_alistador_puede_leer_catalogo_para_asociar_a_servicios(self):
        self.autenticar(self.alistador)
        response = self.client.get('/api/productos/')
        self.assertEqual(response.status_code, 200)

    def test_productos_disponibles_chatbot_filtra_por_stock_y_flag(self):
        self.autenticar(self.cliente)
        response = self.client.get('/api/productos/disponibles-chatbot/')
        self.assertEqual(response.status_code, 200)
        skus = {p['sku'] for p in response.data}
        self.assertEqual(skus, {'T-001'})
