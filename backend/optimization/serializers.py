from rest_framework import serializers

from .models import PuntoGeocodificado


class PuntoGeocodificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuntoGeocodificado
        fields = ['id', 'servicio', 'lat', 'lng', 'direccion_geocodificada', 'creado_en']


# La respuesta de POST /api/optimizacion/rutas/<id>/ no mapea 1-a-1 a un modelo
# (combina orden sugerido + distancia + fallos de geocodificacion), asi que se
# arma como dict plano en la vista -- igual que coverage.views.AgendaDisponibleView
# hace con su respuesta calculada. Con fines de documentacion, la forma es:
#
# {
#   "ruta_id": int,
#   "orden_sugerido": [{"servicio_id": int, "lat": float, "lng": float, "direccion": str}, ...],
#   "distancia_total_km": float,
#   "no_geocodificados": [{"servicio_id": int, "direccion": str}, ...],
# }
