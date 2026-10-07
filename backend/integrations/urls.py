from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ApiKeyViewSet, WebhookEndpointViewSet, WebhookEntregasView

router = DefaultRouter()
router.register('integraciones/api-keys', ApiKeyViewSet, basename='api-key')
router.register('integraciones/webhooks', WebhookEndpointViewSet, basename='webhook')

urlpatterns = [
    path(
        'integraciones/webhooks/<int:endpoint_id>/entregas/',
        WebhookEntregasView.as_view(),
        name='webhook-entregas',
    ),
] + router.urls
