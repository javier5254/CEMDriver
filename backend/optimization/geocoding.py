"""Geocodificacion de direcciones usando la API publica de Nominatim (OpenStreetMap).

Solo se usa la libreria estandar (urllib) para no agregar `requests` como
dependencia nueva del proyecto.
"""
import json
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError

NOMINATIM_SEARCH_URL = 'https://nominatim.openstreetmap.org/search'

# Nominatim exige un User-Agent descriptivo (politica de uso de OSM); no usar
# el user-agent por defecto de urllib.
USER_AGENT = 'CMEDriver-Academic-Project/1.0 (contacto@cmedriver.local)'

TIMEOUT_SEGUNDOS = 5

# Politica de Nominatim: maximo 1 solicitud/segundo. Los llamadores que geocodifican
# varias direcciones en un ciclo deben esperar esto entre llamados que SI golpean la
# red (no hace falta esperar en un cache hit).
RATE_LIMIT_SEGUNDOS = 1.1


def geocodificar(direccion: str) -> tuple[float, float] | None:
    """Geocodifica una direccion usando Nominatim.

    Devuelve una tupla (lat, lng) o `None` si algo falla: sin resultados, error
    de red, timeout o respuesta inesperada. Nunca lanza una excepcion, para que
    quien la llama pueda seguir procesando el resto de direcciones aunque esta
    en particular falle.
    """
    if not direccion or not direccion.strip():
        return None

    query = urllib.parse.urlencode({'format': 'json', 'q': direccion, 'limit': 1})
    url = f'{NOMINATIM_SEARCH_URL}?{query}'
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})

    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SEGUNDOS) as response:
            payload = response.read().decode('utf-8')
    except (URLError, HTTPError, TimeoutError, OSError):
        return None

    try:
        resultados = json.loads(payload)
    except (ValueError, TypeError):
        return None

    if not resultados:
        return None

    try:
        primero = resultados[0]
        return float(primero['lat']), float(primero['lon'])
    except (KeyError, ValueError, TypeError, IndexError):
        return None
