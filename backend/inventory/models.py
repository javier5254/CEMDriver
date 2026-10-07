from django.db import models


class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    centro_mensajeria = models.CharField(max_length=100)
    disponible_chatbot = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sku} - {self.nombre}'
