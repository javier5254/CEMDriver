from django.urls import re_path

from services.consumers import ChatConsumer
from tracking.consumers import TrackingConsumer

websocket_urlpatterns = [
    re_path(r'^ws/tracking/(?P<servicio_id>\d+)/$', TrackingConsumer.as_asgi()),
    re_path(r'^ws/chat/(?P<servicio_id>\d+)/$', ChatConsumer.as_asgi()),
]
