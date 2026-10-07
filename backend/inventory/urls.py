from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProductosDisponiblesChatbotView, ProductoViewSet

router = DefaultRouter()
router.register('productos', ProductoViewSet, basename='producto')

urlpatterns = [
    path('productos/disponibles-chatbot/', ProductosDisponiblesChatbotView.as_view(), name='productos-disponibles-chatbot'),
] + router.urls
