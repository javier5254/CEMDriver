from django.contrib import admin

from .models import Evidencia, MensajeChat, Novedad, Ruta, Servicio, ServicioProducto


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('id', 'motorizado', 'fecha', 'estado')
    list_filter = ('estado', 'fecha')


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'cliente', 'zona', 'estado', 'fecha_agenda', 'ruta')
    list_filter = ('tipo', 'estado', 'zona')
    search_fields = ('cliente__username', 'direccion_origen', 'direccion_destino')


@admin.register(Novedad)
class NovedadAdmin(admin.ModelAdmin):
    list_display = ('id', 'servicio', 'tipo', 'accion', 'creado_en')


@admin.register(Evidencia)
class EvidenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'servicio', 'capturado_en')


@admin.register(MensajeChat)
class MensajeChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'servicio', 'autor', 'enviado_en')


@admin.register(ServicioProducto)
class ServicioProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'servicio', 'producto', 'cantidad')
