import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from services.models import Servicio


class TrackingConsumer(AsyncWebsocketConsumer):
    """Push en tiempo real de la posicion GPS de un servicio.

    Solo lectura desde el cliente: el motorizado sigue reportando su posicion
    por REST (POST /api/tracking/posicion/); ese endpoint hace group_send()
    a este mismo grupo para difundir la posicion a quien este viendo el mapa.
    """

    async def connect(self):
        self.servicio_id = self.scope['url_route']['kwargs']['servicio_id']
        self.group_name = f'tracking_{self.servicio_id}'

        autorizado = await self._usuario_autorizado()
        if not autorizado:
            await self.close(code=4403)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # Este consumer es de solo lectura para el cliente; se ignora
        # cualquier mensaje entrante (el envio real de posicion es por REST).
        pass

    async def tracking_update(self, event):
        await self.send(text_data=json.dumps(event['data']))

    @database_sync_to_async
    def _usuario_autorizado(self):
        user = self.scope['user']
        if not user or not user.is_authenticated:
            return False
        try:
            servicio = Servicio.objects.select_related('ruta').get(pk=self.servicio_id)
        except Servicio.DoesNotExist:
            return False

        if user.rol == 'CLIENTE':
            return servicio.cliente_id == user.id
        if user.rol == 'MOTORIZADO':
            return bool(servicio.ruta and servicio.ruta.motorizado_id == user.id)
        return user.rol in ('ADMIN', 'ALISTADOR')
