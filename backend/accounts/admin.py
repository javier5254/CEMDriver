from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('CMEDriver', {'fields': ('rol', 'nombre', 'telefono')}),
    )
    list_display = ('username', 'nombre', 'rol', 'is_active')
    list_filter = ('rol', 'is_active')
