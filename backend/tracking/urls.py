from django.urls import path

from .views import DestinoView, ReportarPosicionView, UltimaPosicionView

urlpatterns = [
    path('tracking/posicion/', ReportarPosicionView.as_view(), name='tracking-posicion'),
    path('tracking/ultima-posicion/', UltimaPosicionView.as_view(), name='tracking-ultima-posicion'),
    path('tracking/destino/', DestinoView.as_view(), name='tracking-destino'),
]
