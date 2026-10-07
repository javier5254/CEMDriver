from rest_framework import serializers

from .models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'sku', 'nombre', 'descripcion', 'precio', 'stock', 'centro_mensajeria', 'disponible_chatbot']
