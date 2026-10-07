import hashlib
import secrets

from django.conf import settings
from django.db import models

# Eventos validos que un WebhookEndpoint puede suscribir. Se mantienen como
# tupla simple (no TextChoices) porque WebhookEndpoint.eventos guarda una
# lista separada por comas en un solo CharField, no un valor unico.
EVENTOS_WEBHOOK = (
    'servicio.creado',
    'servicio.asignado',
    'servicio.entregado',
    'servicio.recolectado',
    'servicio.novedad',
    'servicio.devuelto',
)


class ApiKey(models.Model):
    """Credencial para que sistemas externos (e-commerce, ERP) usen la API
    sin un login humano. La llave cruda (raw_key) solo se conoce en el
    momento de ApiKey.generar(): a partir de ahi solo se guarda su hash
    SHA-256 (key_hash), nunca el valor original, siguiendo el patron
    estandar de "se muestra una sola vez" de las API keys.
    """

    nombre = models.CharField(max_length=150)
    key_hash = models.CharField(max_length=64, unique=True, editable=False)
    prefix = models.CharField(max_length=8, editable=False)
    actua_como = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'ALISTADOR'},
        related_name='api_keys',
        help_text='Usuario ALISTADOR en cuyo nombre actua esta llave para efectos de permisos.',
    )
    activa = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    ultimo_uso = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return f'{self.nombre} ({self.prefix}...)'

    @staticmethod
    def _hash(raw_key: str) -> str:
        return hashlib.sha256(raw_key.encode('utf-8')).hexdigest()

    @classmethod
    def generar(cls, nombre: str, actua_como):
        """Crea una ApiKey nueva y devuelve (instancia, raw_key).

        raw_key es la unica vez que el valor en texto plano existe: no se
        persiste en ningun campo, solo su hash. Si el llamador lo pierde, la
        unica opcion es generar una llave nueva.
        """
        raw_key = secrets.token_urlsafe(32)
        instancia = cls.objects.create(
            nombre=nombre,
            key_hash=cls._hash(raw_key),
            prefix=raw_key[:8],
            actua_como=actua_como,
        )
        return instancia, raw_key

    @classmethod
    def autenticar(cls, raw_key: str):
        """Devuelve la ApiKey activa que corresponde a raw_key, o None."""
        if not raw_key:
            return None
        try:
            return cls.objects.select_related('actua_como').get(
                key_hash=cls._hash(raw_key), activa=True,
            )
        except cls.DoesNotExist:
            return None


class WebhookEndpoint(models.Model):
    """URL de un tercero que quiere ser notificado de eventos de servicios
    (p.ej. un ERP que quiere saber cuando un pedido se entrego)."""

    nombre = models.CharField(max_length=150)
    url = models.URLField()
    secret = models.CharField(
        max_length=100,
        blank=True,
        help_text='Usado para firmar (HMAC-SHA256) cada webhook enviado. Se autogenera si se deja vacio.',
    )
    eventos = models.CharField(
        max_length=300,
        help_text='Lista separada por comas, p.ej. "servicio.entregado,servicio.novedad".',
    )
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.secret:
            self.secret = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    def lista_eventos(self):
        return [e.strip() for e in self.eventos.split(',') if e.strip()]

    def suscrito_a(self, evento: str) -> bool:
        return evento in self.lista_eventos()


class WebhookDelivery(models.Model):
    """Bitacora de auditoria: un registro por cada intento de POST a un
    WebhookEndpoint, exitoso o no."""

    endpoint = models.ForeignKey(WebhookEndpoint, on_delete=models.CASCADE, related_name='entregas')
    evento = models.CharField(max_length=100)
    payload = models.JSONField()
    status_code = models.IntegerField(null=True, blank=True)
    exito = models.BooleanField(default=False)
    error = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        resultado = 'OK' if self.exito else 'FALLO'
        return f'{self.endpoint_id}:{self.evento} ({resultado})'
