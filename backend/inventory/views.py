from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAdmin

from .models import Producto
from .serializers import ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('nombre')
    serializer_class = ProductoSerializer

    def get_permissions(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            # Lectura abierta a cualquier autenticado: el alistador necesita poder
            # ver el catalogo para asociar un producto a un servicio, aunque ya
            # no pueda crear/editar productos (eso quedo exclusivo del admin).
            return [IsAuthenticated()]
        return [IsAdmin()]


class ProductosDisponiblesChatbotView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        productos = Producto.objects.filter(disponible_chatbot=True, stock__gt=0).order_by('nombre')
        return Response(ProductoSerializer(productos, many=True).data)
