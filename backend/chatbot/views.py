from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsCliente

from .llm import MockLLMClient
from .models import AutorMensaje, Conversacion, MensajeBot
from .serializers import MensajeBotSerializer


class MensajeChatbotView(APIView):
    """POST /api/chatbot/mensaje/ — turno de conversacion con el chatbot.

    Body: {conversacion_id?: number, texto: string}. Si no se envia
    conversacion_id, crea una Conversacion nueva para request.user. Guarda el
    mensaje del cliente, invoca al "LLM" (simulado) y guarda + devuelve su
    respuesta, incluyendo la accion resultante (servicio creado, pago, etc.)
    si el LLM invoco alguna tool.
    """

    permission_classes = [IsCliente]

    def post(self, request):
        texto = (request.data.get('texto') or '').strip()
        if not texto:
            raise ValidationError('texto es requerido.')

        conversacion_id = request.data.get('conversacion_id')
        if conversacion_id:
            try:
                conversacion = Conversacion.objects.get(pk=conversacion_id, cliente=request.user)
            except Conversacion.DoesNotExist:
                raise ValidationError('conversacion_id invalido.')
        else:
            conversacion = Conversacion.objects.create(cliente=request.user)

        MensajeBot.objects.create(conversacion=conversacion, autor=AutorMensaje.CLIENTE, texto=texto)

        resultado = MockLLMClient().responder(conversacion, texto)

        bot_msg = MensajeBot.objects.create(
            conversacion=conversacion,
            autor=AutorMensaje.BOT,
            texto=resultado['texto'],
            function_call=resultado.get('function_call'),
        )

        return Response({
            'conversacion_id': conversacion.id,
            'respuesta': bot_msg.texto,
            'accion': self._extraer_accion(resultado.get('function_call')),
        }, status=201)

    @staticmethod
    def _extraer_accion(function_call):
        if not function_call:
            return None
        tool = function_call.get('tool')
        result = function_call.get('result') or {}

        if tool == 'tool_crear_recoleccion' and result.get('ok'):
            return {'tipo': 'servicio_creado', 'servicio_id': result['servicio_id'], 'estado': result['estado']}
        if tool == 'tool_crear_compra' and result.get('servicio_id'):
            return {
                'tipo': 'pago',
                'servicio_id': result['servicio_id'],
                'pago_id': result['pago_id'],
                'estado': result['pago_estado'],
            }
        return None


class ConversacionMensajesView(APIView):
    """GET /api/chatbot/conversaciones/<id>/mensajes/ — historial de una
    conversacion, para que el frontend pueda recargarla. Solo el cliente
    dueno de la conversacion puede leerla."""

    permission_classes = [IsCliente]

    def get(self, request, id):
        try:
            conversacion = Conversacion.objects.get(pk=id)
        except Conversacion.DoesNotExist:
            return Response({'detail': 'Conversacion no encontrada.'}, status=404)

        if conversacion.cliente_id != request.user.id:
            raise PermissionDenied('No tienes acceso a esta conversacion.')

        mensajes = conversacion.mensajes.all()
        return Response(MensajeBotSerializer(mensajes, many=True).data)
