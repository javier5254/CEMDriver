"""Heuristico de vecino mas cercano (nearest neighbor) sobre distancia haversine.

Aislado de views.py para poder probarlo sin tocar la base de datos ni la red.
"""
import math


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Distancia en linea recta (km) entre dos coordenadas geograficas."""
    radio_tierra_km = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radio_tierra_km * math.asin(math.sqrt(a))


def ordenar_nearest_neighbor(puntos: list[dict]) -> tuple[list[dict], float]:
    """Ordena `puntos` (cada uno con al menos 'lat' y 'lng') con el heuristico
    del vecino mas cercano.

    Simplificacion (MVP): no existe en el sistema un "deposito"/ubicacion de
    partida real (el centro de mensajeria y el motorizado no tienen una
    coordenada fija registrada como origen de la ruta). Por eso el heuristico
    arranca desde el primer punto geocodificado en el orden original (tal como
    llega de la base de datos) en vez de partir de una ubicacion real. Una
    evolucion natural seria usar la ultima PosicionGPS conocida del motorizado,
    o una coordenada fija del centro de mensajeria, como punto de partida.

    Devuelve (orden, distancia_total_km) con la distancia total redondeada a 2
    decimales.
    """
    if not puntos:
        return [], 0.0

    restantes = list(puntos)
    actual = restantes.pop(0)
    orden = [actual]
    distancia_total = 0.0

    while restantes:
        siguiente = min(
            restantes,
            key=lambda p: haversine_km(actual['lat'], actual['lng'], p['lat'], p['lng']),
        )
        distancia_total += haversine_km(actual['lat'], actual['lng'], siguiente['lat'], siguiente['lng'])
        restantes.remove(siguiente)
        orden.append(siguiente)
        actual = siguiente

    return orden, round(distancia_total, 2)
