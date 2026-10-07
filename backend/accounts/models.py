from django.contrib.auth.models import AbstractUser
from django.db import models


class Rol(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrador'
    ALISTADOR = 'ALISTADOR', 'Alistador'
    MOTORIZADO = 'MOTORIZADO', 'Motorizado'
    CLIENTE = 'CLIENTE', 'Cliente'


class Usuario(AbstractUser):
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.CLIENTE)
    nombre = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    # AbstractUser.email es blank=True por defecto; en CMEDriver el correo es
    # obligatorio y unico porque es un metodo de autenticacion valido (RF-19).
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.username} ({self.rol})'
