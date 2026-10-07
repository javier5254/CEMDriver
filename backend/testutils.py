"""Utilidades compartidas para la suite de pruebas (no es una app Django)."""
from rest_framework.test import APITestCase

from accounts.models import Usuario


class BaseAPITestCase(APITestCase):
    """Crea un usuario de cada rol y helpers de autenticacion para las pruebas."""

    def setUp(self):
        super().setUp()
        self.admin = self._crear_usuario('admin_test', 'ADMIN')
        self.alistador = self._crear_usuario('alistador_test', 'ALISTADOR')
        self.motorizado = self._crear_usuario('motorizado_test', 'MOTORIZADO')
        self.otro_motorizado = self._crear_usuario('motorizado_test2', 'MOTORIZADO')
        self.cliente = self._crear_usuario('cliente_test', 'CLIENTE')
        self.otro_cliente = self._crear_usuario('cliente_test2', 'CLIENTE')

    @staticmethod
    def _crear_usuario(username, rol, password='clave1234'):
        usuario = Usuario(username=username, rol=rol, nombre=username, email=f'{username}@test.local')
        usuario.set_password(password)
        usuario.save()
        return usuario

    def autenticar(self, usuario):
        self.client.force_authenticate(user=usuario)
