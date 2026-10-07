from django.contrib import admin

from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nombre', 'precio', 'stock', 'centro_mensajeria', 'disponible_chatbot')
    list_filter = ('centro_mensajeria', 'disponible_chatbot')
    search_fields = ('sku', 'nombre')
