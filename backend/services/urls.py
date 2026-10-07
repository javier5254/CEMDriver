from rest_framework.routers import DefaultRouter

from .views import RutaViewSet, ServicioViewSet

router = DefaultRouter()
router.register('servicios', ServicioViewSet, basename='servicio')
router.register('rutas', RutaViewSet, basename='ruta')

urlpatterns = router.urls
