from django.urls import path

from .views import PagoDetailView

urlpatterns = [
    path('pagos/<int:pk>/', PagoDetailView.as_view(), name='pago-detail'),
]
