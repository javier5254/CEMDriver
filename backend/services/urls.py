from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RutaViewSet, ServicioViewSet
from .views_indicadores import IndicadoresView

router = DefaultRouter()
router.register('servicios', ServicioViewSet, basename='servicio')
router.register('rutas', RutaViewSet, basename='ruta')

urlpatterns = [
    path('indicadores/', IndicadoresView.as_view(), name='indicadores'),
] + router.urls
