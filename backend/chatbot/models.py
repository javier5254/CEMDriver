from django.conf import settings
from django.db import models


class Conversacion(models.Model):
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversaciones_chatbot',
        limit_choices_to={'rol': 'CLIENTE'},
    )
    # Estado de "slot-filling" en curso entre turnos (ej. a mitad de una
    # recoleccion, esperando la fecha de agenda). Lo lee y actualiza
    # chatbot.llm.MockLLMClient.responder() en cada mensaje.
    contexto = models.JSONField(default=dict, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return f'Conversacion {self.id} - {self.cliente}'


class AutorMensaje(models.TextChoices):
    CLIENTE = 'CLIENTE', 'Cliente'
    BOT = 'BOT', 'Bot'


class MensajeBot(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    autor = models.CharField(max_length=10, choices=AutorMensaje.choices)
    texto = models.TextField()
    # Registro de la "tool" invocada por el LLM simulado para este mensaje
    # (solo aplica a autor=BOT): {"tool": "...", "args": {...}, "result": {...}}.
    # Se guarda para poder demostrar la arquitectura de tool-calling.
    function_call = models.JSONField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['creado_en']

    def __str__(self):
        return f'Mensaje {self.id} ({self.autor}) - conv {self.conversacion_id}'
