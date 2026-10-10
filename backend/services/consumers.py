import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import MensajeChat, Servicio
from .serializers import MensajeChatSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    """Chat en tiempo real entre cliente y motorizado para un servicio.

    Solo participan el cliente dueno del servicio y el motorizado asignado.

    Bidireccional: un mensaje enviado por WebSocket se guarda igual que uno
    enviado por REST (POST /api/servicios/{id}/mensajes/) y se difunde a
    todos los conectados al mismo servicio, incluyendo al propio autor (asi
    todas las pestanas/dispositivos quedan sincronizados).
    """

    async def connect(self):
        self.servicio_id = self.scope['url_route']['kwargs']['servicio_id']
        self.group_name = f'chat_{self.servicio_id}'

        if not await self._usuario_autorizado():
            await self.close(code=4403)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return
        try:
            data = json.loads(text_data)
            texto = (data.get('texto') or '').strip()
        except (json.JSONDecodeError, AttributeError):
            return
        if not texto:
            return

        mensaje = await self._guardar_mensaje(texto)
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat_message',
            'data': mensaje,
        })

    async def chat_message(self, event):
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
        # El chat es solo entre el cliente del servicio y el motorizado asignado.
        return False

    @database_sync_to_async
    def _guardar_mensaje(self, texto):
        mensaje = MensajeChat.objects.create(
            servicio_id=self.servicio_id,
            autor=self.scope['user'],
            texto=texto,
        )
        return MensajeChatSerializer(mensaje).data
