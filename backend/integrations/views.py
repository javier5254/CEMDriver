from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from accounts.permissions import IsAdmin

from .models import ApiKey, WebhookDelivery, WebhookEndpoint
from .serializers import (
    ApiKeyCreateSerializer,
    ApiKeyListSerializer,
    WebhookDeliverySerializer,
    WebhookEndpointDetailSerializer,
    WebhookEndpointListSerializer,
)


class ApiKeyViewSet(viewsets.ModelViewSet):
    """CRUD de ApiKey, solo para ADMIN. La llave cruda solo aparece una vez,
    en la respuesta de create(); nunca se puede recuperar despues."""

    queryset = ApiKey.objects.all()
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action == 'create':
            return ApiKeyCreateSerializer
        return ApiKeyListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instancia, raw_key = ApiKey.generar(
            nombre=serializer.validated_data['nombre'],
            actua_como=serializer.validated_data['actua_como'],
        )
        data = ApiKeyListSerializer(instancia).data
        data['key'] = raw_key  # unica vez que se expone: no se persiste en ningun lado.
        return Response(data, status=status.HTTP_201_CREATED)


class WebhookEndpointViewSet(viewsets.ModelViewSet):
    """CRUD de WebhookEndpoint, solo para ADMIN."""

    queryset = WebhookEndpoint.objects.all()
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action == 'list':
            return WebhookEndpointListSerializer
        return WebhookEndpointDetailSerializer


class WebhookEntregasView(ListAPIView):
    """Bitacora (solo lectura) de las entregas recientes de un WebhookEndpoint,
    para que el admin audite exitos/fallos de notificaciones salientes."""

    serializer_class = WebhookDeliverySerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return WebhookDelivery.objects.filter(
            endpoint_id=self.kwargs['endpoint_id'],
        ).order_by('-creado_en')[:200]
