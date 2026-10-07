"""Envio de webhooks salientes.

Este modulo es intencionalmente stdlib-only (urllib), sin dependencias
nuevas, para mantener el footprint de la app `integrations` minimo.
"""
import hashlib
import hmac
import json
import urllib.error
import urllib.request

from .models import WebhookDelivery, WebhookEndpoint

TIMEOUT_SEGUNDOS = 3


def firmar(payload_bytes: bytes, secret: str) -> str:
    """Calcula la firma HMAC-SHA256 (hexdigest) de payload_bytes con secret.

    Como verificar un webhook del lado del receptor:
    1. Tomar el cuerpo CRUDO (bytes) de la peticion recibida, tal cual llego
       en el socket -- no un dict re-serializado, porque un re-serializado
       puede diferir en espacios/orden de llaves y no calzar con la firma.
    2. Calcular hmac.new(secret.encode(), cuerpo_crudo, hashlib.sha256).hexdigest()
       usando el mismo `secret` que se configuro para ese WebhookEndpoint.
    3. Comparar el resultado contra el header `X-CMEDriver-Signature` de la
       peticion usando hmac.compare_digest (nunca `==`, para evitar timing
       attacks).
    4. Si no coinciden, rechazar la peticion: no vino de CMEDriver o el
       cuerpo fue alterado en transito.
    """
    return hmac.new(secret.encode('utf-8'), payload_bytes, hashlib.sha256).hexdigest()


def disparar_webhook(evento: str, payload: dict) -> None:
    """Notifica a todos los WebhookEndpoint activos suscritos a `evento`.

    IMPORTANTE -- contrato de "nunca lanza": se espera que esta funcion sea
    invocada desde dentro del ciclo request/response de las transiciones de
    estado de ServicioViewSet (services/views.py). Si la URL de un tercero
    esta caida, tiene DNS roto, TLS invalido, o simplemente no responde a
    tiempo, eso NUNCA puede convertirse en un error 500 para quien esta
    usando la API real (p.ej. el motorizado cerrando un servicio). Por eso:

    - Cada endpoint se procesa en su propio try/except: una URL rota no
      afecta a los demas endpoints suscritos ni interrumpe la vista que
      llamo a esta funcion.
    - No se relanza ninguna excepcion hacia el llamador bajo ninguna
      circunstancia; los fallos solo quedan registrados en
      WebhookDelivery.error para auditoria/soporte.
    """
    try:
        endpoints = list(WebhookEndpoint.objects.filter(activo=True))
    except Exception:
        # Si ni siquiera se puede consultar la tabla, no hay nada mas que
        # hacer; nunca debe propagarse hacia el llamador real.
        return

    for endpoint in endpoints:
        try:
            if not endpoint.suscrito_a(evento):
                continue
        except Exception:
            continue

        _enviar_a_endpoint(endpoint, evento, payload)


def _enviar_a_endpoint(endpoint: WebhookEndpoint, evento: str, payload: dict) -> None:
    status_code = None
    exito = False
    error = ''
    body = json.dumps(payload, default=str).encode('utf-8')

    try:
        firma = firmar(body, endpoint.secret)
        request = urllib.request.Request(
            endpoint.url,
            data=body,
            method='POST',
            headers={
                'Content-Type': 'application/json',
                'X-CMEDriver-Signature': firma,
            },
        )
        with urllib.request.urlopen(request, timeout=TIMEOUT_SEGUNDOS) as respuesta:
            status_code = respuesta.getcode()
            exito = 200 <= status_code < 300
            if not exito:
                error = f'Respuesta HTTP {status_code}'
    except urllib.error.HTTPError as exc:
        status_code = exc.code
        error = f'HTTPError {exc.code}: {exc.reason}'
    except Exception as exc:  # noqa: BLE001 - a proposito: nunca debe escapar de aqui
        error = f'{type(exc).__name__}: {exc}'

    try:
        WebhookDelivery.objects.create(
            endpoint=endpoint,
            evento=evento,
            payload=payload,
            status_code=status_code,
            exito=exito,
            error=error,
        )
    except Exception:
        # Si ni siquiera se puede registrar la entrega, se ignora en
        # silencio: registrar auditoria nunca debe romper al llamador.
        pass
