from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import AgendaDisponibleView, CoberturaViewSet

router = DefaultRouter()
router.register('cobertura', CoberturaViewSet, basename='cobertura')

urlpatterns = [
    path('cobertura/agenda-disponible/', AgendaDisponibleView.as_view(), name='agenda-disponible'),
] + router.urls
