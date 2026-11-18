from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAdminOAlistador

from .indicadores import calcular_indicadores
from .serializers_indicadores import IndicadoresParametrosSerializer, IndicadoresRespuestaSerializer


class IndicadoresView(APIView):
    """RF-30: indicadores operativos calculados con el ORM sobre la base de
    datos real. Solo para ADMIN y ALISTADOR."""

    permission_classes = [IsAdminOAlistador]

    @extend_schema(
        tags=['indicadores'],
        summary='Consultar indicadores operativos',
        description=(
            'Indicadores de los últimos `dias` días (por fecha de creación del servicio), '
            'calculados con agregaciones sobre la base de datos. Las tasas son proporciones '
            'entre 0 y 1 y valen null cuando no hay datos para calcularlas.'
        ),
        parameters=[IndicadoresParametrosSerializer],
        responses=IndicadoresRespuestaSerializer,
    )
    def get(self, request):
        parametros = IndicadoresParametrosSerializer(data=request.query_params)
        parametros.is_valid(raise_exception=True)
        datos = parametros.validated_data
        return Response(calcular_indicadores(
            dias=datos['dias'], zona=datos.get('zona') or None,
        ))
