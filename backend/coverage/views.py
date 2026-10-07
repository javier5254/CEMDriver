import datetime

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAdmin

from .models import Cobertura
from .serializers import CoberturaSerializer

DIAS_ORDEN = ['LUN', 'MAR', 'MIE', 'JUE', 'VIE', 'SAB', 'DOM']
HORIZONTE_DIAS = 21


class CoberturaViewSet(viewsets.ModelViewSet):
    queryset = Cobertura.objects.all().order_by('zona')
    serializer_class = CoberturaSerializer

    def get_permissions(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [IsAuthenticated()]
        return [IsAdmin()]


class AgendaDisponibleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        zona = request.query_params.get('zona')
        try:
            cobertura = Cobertura.objects.get(zona=zona)
        except Cobertura.DoesNotExist:
            return Response({'detail': 'Zona sin cobertura configurada.'}, status=404)

        dias_validos = set(cobertura.dias_codigos())
        hoy = datetime.date.today()
        primera_fecha_posible = hoy + datetime.timedelta(days=cobertura.leadtime_dias)

        fechas = []
        cursor = primera_fecha_posible
        limite = hoy + datetime.timedelta(days=HORIZONTE_DIAS)
        while cursor <= limite:
            codigo_dia = DIAS_ORDEN[cursor.weekday()]
            if codigo_dia in dias_validos:
                fechas.append(cursor.isoformat())
            cursor += datetime.timedelta(days=1)

        return Response({
            'zona': zona,
            'leadtime_dias': cobertura.leadtime_dias,
            'hora_inicio': cobertura.hora_inicio,
            'hora_fin': cobertura.hora_fin,
            'fechas_disponibles': fechas,
        })
