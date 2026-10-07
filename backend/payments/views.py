from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Pago
from .serializers import PagoSerializer


class PagoDetailView(APIView):
    """Consulta el estado actual de un pago. Solo el cliente dueno del pago o
    un ADMIN pueden verlo (mismo criterio de propiedad que tracking.views.UltimaPosicionView)."""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            pago = Pago.objects.get(pk=pk)
        except Pago.DoesNotExist:
            return Response({'detail': 'Pago no encontrado.'}, status=404)

        user = request.user
        es_dueno = user.rol == 'CLIENTE' and pago.cliente_id == user.id
        if not (es_dueno or user.rol == 'ADMIN'):
            raise PermissionDenied('No tienes acceso a este pago.')

        return Response(PagoSerializer(pago).data)
