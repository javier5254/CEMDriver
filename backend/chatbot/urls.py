from django.urls import path

from .views import ConversacionMensajesView, MensajeChatbotView

urlpatterns = [
    path('chatbot/mensaje/', MensajeChatbotView.as_view(), name='chatbot-mensaje'),
    path(
        'chatbot/conversaciones/<int:id>/mensajes/',
        ConversacionMensajesView.as_view(),
        name='chatbot-conversacion-mensajes',
    ),
]
