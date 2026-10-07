import time

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAdmin, IsAlistador
from services.models import Ruta, Servicio, TipoServicio

from .geocoding import RATE_LIMIT_SEGUNDOS, geocodificar
from .heuristica import ordenar_nearest_neighbor
from .models import PuntoGeocodificado


class OptimizarRutaView(APIView):
    """Sugiere un orden de visita eficiente para los servicios de una ruta.

    Es de solo lectura/asesoria: no persiste ningun orden en `Servicio` ni en
    `Ruta` -- unicamente calcula y devuelve una sugerencia para que el
    alistador/administrador la revise.
    """
    permission_classes = [IsAdmin | IsAlistador]

    def post(self, request, ruta_id):
        ruta = get_object_or_404(Ruta, pk=ruta_id)
        # `Servicio.Meta.ordering` es `-creado_en` (para listados en la app de
        # servicios), pero aqui queremos el orden "original" de creacion de los
        # servicios de la ruta (mas antiguo primero) como punto de partida del
        # heuristico, asi que lo forzamos explicitamente por id ascendente.
        servicios = Servicio.objects.filter(ruta_id=ruta.id).order_by('id')

        puntos = []
        no_geocodificados = []

        for servicio in servicios:
            direccion_base = (
                servicio.direccion_destino
                if servicio.tipo == TipoServicio.ENTREGA
                else servicio.direccion_origen
            )
            direccion_query = f'{direccion_base}, {servicio.zona}, Colombia'

            cache = PuntoGeocodificado.objects.filter(servicio=servicio).first()
            if cache is not None:
                lat, lng = float(cache.lat), float(cache.lng)
            else:
                resultado = geocodificar(direccion_query)
                # Solo esperamos el rate-limit de Nominatim cuando de verdad
                # golpeamos la red (los cache hits no tienen que esperar).
                time.sleep(RATE_LIMIT_SEGUNDOS)
                if resultado is None:
                    no_geocodificados.append({'servicio_id': servicio.id, 'direccion': direccion_query})
                    continue
                lat, lng = resultado
                PuntoGeocodificado.objects.create(
                    servicio=servicio,
                    lat=lat,
                    lng=lng,
                    direccion_geocodificada=direccion_query,
                )

            puntos.append({
                'servicio_id': servicio.id,
                'lat': lat,
                'lng': lng,
                'direccion': direccion_query,
            })

        orden_sugerido, distancia_total_km = ordenar_nearest_neighbor(puntos)

        return Response({
            'ruta_id': ruta.id,
            'orden_sugerido': orden_sugerido,
            'distancia_total_km': distancia_total_km,
            'no_geocodificados': no_geocodificados,
        })
