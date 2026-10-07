from django.db import models

from services.models import Servicio


class PuntoGeocodificado(models.Model):
    """Cache de coordenadas geocodificadas por servicio.

    Evita volver a golpear la API publica de geocodificacion (Nominatim/OSM) en
    cada corrida de optimizacion de ruta: si ya conocemos las coordenadas de la
    direccion de un servicio, las reutilizamos en vez de re-geocodificar.
    """
    servicio = models.OneToOneField(Servicio, on_delete=models.CASCADE, related_name='punto_geocodificado')
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    direccion_geocodificada = models.CharField(max_length=255)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Punto geocodificado'
        verbose_name_plural = 'Puntos geocodificados'

    def __str__(self):
        return f'Punto(servicio={self.servicio_id}) -> ({self.lat}, {self.lng})'
