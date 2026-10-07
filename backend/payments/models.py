import uuid

from django.conf import settings
from django.db import models


class EstadoPago(models.TextChoices):
    PENDIENTE = 'PENDIENTE', 'Pendiente'
    APROBADO = 'APROBADO', 'Aprobado'
    RECHAZADO = 'RECHAZADO', 'Rechazado'


def _generar_referencia():
    return uuid.uuid4().hex


class Pago(models.Model):
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='pagos',
        limit_choices_to={'rol': 'CLIENTE'},
    )
    # Un pago puede existir antes de que el servicio quede finalizado (p.ej. se
    # cobra al momento de la compra por chatbot, y el servicio de ENTREGA se
    # crea en la misma operacion), por eso ambas FK son nullable.
    servicio = models.ForeignKey(
        'services.Servicio', on_delete=models.SET_NULL, null=True, blank=True, related_name='pagos',
    )
    producto = models.ForeignKey(
        'inventory.Producto', on_delete=models.SET_NULL, null=True, blank=True, related_name='pagos',
    )
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=20, choices=EstadoPago.choices, default=EstadoPago.PENDIENTE)
    proveedor = models.CharField(max_length=50, default='MOCK')
    referencia = models.CharField(max_length=64, unique=True, default=_generar_referencia)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return f'Pago {self.id} ({self.estado}) - {self.referencia}'
