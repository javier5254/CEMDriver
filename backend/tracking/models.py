from django.conf import settings
from django.db import models

from services.models import Servicio


class PosicionGPS(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='posiciones')
    motorizado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posiciones')
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
