from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken


@database_sync_to_async
def _usuario_desde_token(token_str):
    from accounts.models import Usuario

    try:
        access = AccessToken(token_str)
        return Usuario.objects.get(pk=access['user_id'])
    except (TokenError, Usuario.DoesNotExist, KeyError):
        return AnonymousUser()


class JWTAuthMiddleware:
    """Autentica conexiones WebSocket via ?token=<access JWT> en la query string.

    Los navegadores no pueden mandar headers Authorization al abrir un
    WebSocket, asi que el access token viaja como parametro de la URL.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode()
        token = parse_qs(query_string).get('token', [None])[0]
        scope['user'] = await _usuario_desde_token(token) if token else AnonymousUser()
        return await self.app(scope, receive, send)
