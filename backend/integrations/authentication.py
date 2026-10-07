from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import ApiKey


class ApiKeyAuthentication(BaseAuthentication):
    """Autenticacion por API key para sistemas externos (ERP, e-commerce)
    que necesitan crear/consultar servicios sin un login humano.

    Convencion DRF: si el header no viene, se retorna None para dejar que
    otras clases de autenticacion (o el permiso de la vista) decidan; si el
    header viene pero no corresponde a una ApiKey activa, se rechaza de
    forma explicita con AuthenticationFailed (401).

    En exito retorna (usuario, None) donde `usuario` es el `actua_como`
    configurado en la ApiKey (un Usuario con rol ALISTADOR). Esto hace que
    request.user quede igual que si un alistador hubiera iniciado sesion, y
    por lo tanto los permisos existentes (p.ej. IsAlistador en
    ServicioViewSet) funcionan sin ningun cambio adicional.
    """

    def authenticate(self, request):
        raw_key = request.headers.get('X-API-Key')
        if not raw_key:
            return None

        api_key = ApiKey.autenticar(raw_key)
        if api_key is None:
            raise AuthenticationFailed('API key invalida o inactiva.')

        api_key.ultimo_uso = timezone.now()
        api_key.save(update_fields=['ultimo_uso'])

        return (api_key.actua_como, None)

    def authenticate_header(self, request):
        # Usado por DRF para el header WWW-Authenticate en una respuesta 401.
        return 'X-API-Key'
