from django.core import mail

from testutils import BaseAPITestCase

from .serializers import construir_uid_y_token


class AuthTests(BaseAPITestCase):
    def test_login_devuelve_tokens_y_usuario(self):
        response = self.client.post('/api/auth/login/', {
            'username': self.alistador.username,
            'password': 'clave1234',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['rol'], 'ALISTADOR')

    def test_login_con_correo_en_vez_de_username(self):
        response = self.client.post('/api/auth/login/', {
            'username': self.alistador.email,
            'password': 'clave1234',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['username'], self.alistador.username)

    def test_login_con_password_incorrecta_falla(self):
        response = self.client.post('/api/auth/login/', {
            'username': self.alistador.username,
            'password': 'incorrecta',
        })
        self.assertEqual(response.status_code, 401)

    def test_me_devuelve_usuario_autenticado(self):
        self.autenticar(self.cliente)
        response = self.client.get('/api/auth/me/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.cliente.username)


class PasswordResetTests(BaseAPITestCase):
    def test_solicitar_reset_envia_correo_si_existe(self):
        response = self.client.post('/api/auth/password-reset/', {'email': self.cliente.email})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.cliente.email, mail.outbox[0].to)

    def test_solicitar_reset_con_correo_inexistente_no_revela_nada(self):
        response = self.client.post('/api/auth/password-reset/', {'email': 'no-existe@test.local'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_confirmar_reset_cambia_password(self):
        uid, token = construir_uid_y_token(self.cliente)
        response = self.client.post('/api/auth/password-reset/confirm/', {
            'uid': uid, 'token': token, 'new_password': 'NuevaClave123!',
        })
        self.assertEqual(response.status_code, 200)

        login = self.client.post('/api/auth/login/', {
            'username': self.cliente.username, 'password': 'NuevaClave123!',
        })
        self.assertEqual(login.status_code, 200)

    def test_confirmar_reset_con_token_invalido_falla(self):
        uid, _ = construir_uid_y_token(self.cliente)
        response = self.client.post('/api/auth/password-reset/confirm/', {
            'uid': uid, 'token': 'token-invalido', 'new_password': 'NuevaClave123!',
        })
        self.assertEqual(response.status_code, 400)


class UsuariosRBACTests(BaseAPITestCase):
    def test_admin_puede_listar_usuarios(self):
        self.autenticar(self.admin)
        response = self.client.get('/api/usuarios/')
        self.assertEqual(response.status_code, 200)

    def test_no_admin_no_puede_listar_usuarios(self):
        for usuario in (self.alistador, self.motorizado, self.cliente):
            self.autenticar(usuario)
            response = self.client.get('/api/usuarios/')
            self.assertEqual(response.status_code, 403)

    def test_anonimo_no_puede_listar_usuarios(self):
        response = self.client.get('/api/usuarios/')
        self.assertEqual(response.status_code, 401)
