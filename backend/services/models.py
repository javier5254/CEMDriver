from django.conf import settings
from django.db import models


class TipoServicio(models.TextChoices):
    ENTREGA = 'ENTREGA', 'Entrega'
    RECOLECCION = 'RECOLECCION', 'Recoleccion'


class EstadoServicio(models.TextChoices):
    CREADO = 'CREADO', 'Creado'
    ASIGNADO = 'ASIGNADO', 'Asignado a ruta'
    RECIBIDO_CENTRO = 'RECIBIDO_CENTRO', 'Recibido en centro'
    EN_TRANSITO = 'EN_TRANSITO', 'En transito'
    ENTREGADO = 'ENTREGADO', 'Entregado'
    RECOLECTADO = 'RECOLECTADO', 'Recolectado'
    NOVEDAD = 'NOVEDAD', 'Con novedad'
    DEVUELTO = 'DEVUELTO', 'Devuelto al centro'


class EstadoRuta(models.TextChoices):
    PLANEADA = 'PLANEADA', 'Planeada'
    EN_CURSO = 'EN_CURSO', 'En curso'
    FINALIZADA = 'FINALIZADA', 'Finalizada'


class Ruta(models.Model):
    motorizado = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='rutas',
        limit_choices_to={'rol': 'MOTORIZADO'},
    )
    fecha = models.DateField()
    estado = models.CharField(max_length=20, choices=EstadoRuta.choices, default=EstadoRuta.PLANEADA)

    def __str__(self):
        return f'Ruta {self.id} - {self.motorizado} - {self.fecha}'


class Servicio(models.Model):
    tipo = models.CharField(max_length=20, choices=TipoServicio.choices)
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='servicios',
        limit_choices_to={'rol': 'CLIENTE'},
    )
    producto = models.ForeignKey('inventory.Producto', on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios')
    zona = models.CharField(max_length=100)
    direccion_origen = models.CharField(max_length=255, blank=True)
    direccion_destino = models.CharField(max_length=255, blank=True)
    fecha_agenda = models.DateField()
    estado = models.CharField(max_length=20, choices=EstadoServicio.choices, default=EstadoServicio.CREADO)
    ruta = models.ForeignKey(Ruta, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios')
    creado_en = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios_creados',
    )

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return f'Servicio {self.id} ({self.tipo}) - {self.estado}'


class ServicioProducto(models.Model):
    """Linea de producto adicional de un servicio (inventario avanzado).

    El campo `Servicio.producto` original se mantiene para no romper flujos
    existentes (chatbot, formulario simple del alistador) que solo manejan
    un producto. Esta tabla permite, opcionalmente, asociar varios productos
    con cantidad a un mismo servicio (ej. una compra con 2 items distintos).
    """

    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='productos_detalle')
    producto = models.ForeignKey('inventory.Producto', on_delete=models.PROTECT, related_name='lineas_servicio')
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('servicio', 'producto')

    def __str__(self):
        return f'{self.servicio_id} x {self.producto.sku} ({self.cantidad})'


class Evidencia(models.Model):
    servicio = models.OneToOneField(Servicio, on_delete=models.CASCADE, related_name='evidencia')
    foto = models.ImageField(upload_to='evidencias/fotos/', blank=True, null=True)
    firma = models.ImageField(upload_to='evidencias/firmas/', blank=True, null=True)
    capturado_en = models.DateTimeField(auto_now_add=True)


class Novedad(models.Model):
    class Accion(models.TextChoices):
        DEVOLVER = 'DEVOLVER_A_CENTRO', 'Devolver a centro'
        REINTENTAR = 'REINTENTAR', 'Reintentar'

    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='novedades')
    tipo = models.CharField(max_length=100)
    detalle = models.TextField(blank=True)
    accion = models.CharField(max_length=20, choices=Accion.choices)
    creado_en = models.DateTimeField(auto_now_add=True)


class MensajeChat(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='mensajes')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensajes_enviados')
    texto = models.CharField(max_length=1000)
    enviado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['enviado_en']
