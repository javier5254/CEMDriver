from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsMotorizado
from optimization.geocoding import geocodificar
from optimization.models import PuntoGeocodificado
from services.models import Servicio, TipoServicio

from .models import PosicionGPS
from .serializers import PosicionGPSSerializer


class ReportarPosicionView(APIView):
    permission_classes = [IsMotorizado]

    def post(self, request):
        serializer = PosicionGPSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        servicio = serializer.validated_data['servicio']
        if not servicio.ruta or servicio.ruta.motorizado_id != request.user.id:
            raise PermissionDenied('Este servicio no esta asignado a tu ruta.')
        posicion = serializer.save(motorizado=request.user)

        data = PosicionGPSSerializer(posicion).data
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                f'tracking_{servicio.id}', {'type': 'tracking_update', 'data': data},
            )

        return Response(data, status=201)


class UltimaPosicionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        servicio_id = request.query_params.get('servicio_id')
        if not servicio_id:
            raise ValidationError('servicio_id es requerido.')
        try:
            servicio = Servicio.objects.get(pk=servicio_id)
        except Servicio.DoesNotExist:
            return Response({'detail': 'Servicio no encontrado.'}, status=404)

        user = request.user
        if user.rol == 'CLIENTE' and servicio.cliente_id != user.id:
            raise PermissionDenied('No tienes acceso al tracking de este servicio.')

        posicion = servicio.posiciones.first()
        if not posicion:
            return Response({'detail': 'Aun no hay posicion registrada para este servicio.'}, status=404)
        return Response(PosicionGPSSerializer(posicion).data)


class DestinoView(APIView):
    """Coordenadas del punto de destino (ENTREGA) u origen (RECOLECCION) de un
    servicio, para mostrarlo en el mapa de tracking junto a la posicion del
    motorizado. Reutiliza el mismo geocoding + cache que la optimizacion de
    rutas (`optimization`), en vez de duplicar esa logica."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        servicio_id = request.query_params.get('servicio_id')
        if not servicio_id:
            raise ValidationError('servicio_id es requerido.')
        try:
            servicio = Servicio.objects.get(pk=servicio_id)
        except Servicio.DoesNotExist:
            return Response({'detail': 'Servicio no encontrado.'}, status=404)

        user = request.user
        if user.rol == 'CLIENTE' and servicio.cliente_id != user.id:
            raise PermissionDenied('No tienes acceso a este servicio.')
        if user.rol == 'MOTORIZADO' and (not servicio.ruta or servicio.ruta.motorizado_id != user.id):
            raise PermissionDenied('No tienes acceso a este servicio.')

        punto = PuntoGeocodificado.objects.filter(servicio=servicio).first()
        if not punto:
            direccion = servicio.direccion_destino if servicio.tipo == TipoServicio.ENTREGA else servicio.direccion_origen
            if not direccion:
                return Response({'detail': 'El servicio no tiene una direccion para geocodificar.'}, status=404)

            resultado = geocodificar(f'{direccion}, {servicio.zona}, Colombia')
            if not resultado:
                return Response({'detail': 'No se pudo geocodificar la direccion del servicio.'}, status=404)

            lat, lng = resultado
            punto = PuntoGeocodificado.objects.create(
                servicio=servicio, lat=lat, lng=lng, direccion_geocodificada=direccion,
            )

        return Response({
            'servicio_id': servicio.id,
            'lat': punto.lat,
            'lng': punto.lng,
            'direccion': punto.direccion_geocodificada,
        })
