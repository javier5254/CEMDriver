"""
ASGI config for cmedriver project.

Routea HTTP a Django normal y WebSockets (tracking GPS y chat en tiempo real)
a los consumers de Channels, con autenticacion JWT via query string.
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmedriver.settings')

django_asgi_app = get_asgi_application()

# Import despues de get_asgi_application() para que las apps ya esten cargadas
# antes de que los consumers importen modelos.
from cmedriver.ws_auth import JWTAuthMiddleware  # noqa: E402
from cmedriver.routing import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': JWTAuthMiddleware(URLRouter(websocket_urlpatterns)),
})
