from django.urls import path

from .views import OptimizarRutaView

urlpatterns = [
    path('optimizacion/rutas/<int:ruta_id>/', OptimizarRutaView.as_view(), name='optimizar-ruta'),
]
