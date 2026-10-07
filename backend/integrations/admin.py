from django.contrib import admin

from .models import ApiKey, WebhookDelivery, WebhookEndpoint


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'prefix', 'actua_como', 'activa', 'creado_en', 'ultimo_uso')
    list_filter = ('activa',)
    search_fields = ('nombre', 'prefix')


@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'url', 'eventos', 'activo', 'creado_en')
    list_filter = ('activo',)
    search_fields = ('nombre', 'url')


@admin.register(WebhookDelivery)
class WebhookDeliveryAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'evento', 'status_code', 'exito', 'creado_en')
    list_filter = ('exito', 'evento')
    search_fields = ('endpoint__nombre', 'evento')
