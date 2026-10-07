# SIMULADO: sin proveedor real (Wompi/PayU) configurado. Reemplazar procesar()
# por una llamada real cuando haya credenciales.
#
# Este modulo aisla toda la logica de "hablar con un proveedor de pagos"
# detras de una interfaz pequeña (PaymentProvider.procesar) para que, el dia
# que existan credenciales de un proveedor real, solo haya que:
#   1. Escribir una subclase (ej. WompiProvider) que implemente `procesar`
#      haciendo la llamada HTTP real y mapeando su respuesta a EstadoPago.
#   2. Ajustar `obtener_proveedor_pago()` para devolverla segun un flag de
#      settings, sin tocar el resto del codigo que la consume (chatbot/views,
#      chatbot/llm, etc. solo conocen la interfaz `procesar(pago) -> Pago`).
import random

from django.conf import settings

from .models import EstadoPago, Pago


class PaymentProvider:
    """Interfaz base de un proveedor de pagos."""

    def procesar(self, pago: Pago) -> Pago:
        raise NotImplementedError


class MockPaymentProvider(PaymentProvider):
    """Simula el procesamiento de un pago sin ninguna llamada de red real.

    Aprueba por defecto; simula una tasa de rechazo de ~10% (aleatoria) para
    que el demo tenga variedad de casos, tal como pasaria con un proveedor
    real (fondos insuficientes, tarjeta rechazada, etc.).
    """

    TASA_RECHAZO = 0.10

    def procesar(self, pago: Pago) -> Pago:
        pago.proveedor = 'MOCK'
        if random.random() < self.TASA_RECHAZO:
            pago.estado = EstadoPago.RECHAZADO
        else:
            pago.estado = EstadoPago.APROBADO
        pago.save()
        return pago


def obtener_proveedor_pago() -> PaymentProvider:
    """Factory de proveedor de pagos.

    Hoy siempre devuelve el proveedor simulado. Queda estructurado para leer
    un flag de settings (ej. PAYMENTS_PROVIDER='WOMPI') el dia que haya
    credenciales reales, sin cambiar la firma ni los llamadores.
    """
    proveedor = getattr(settings, 'PAYMENTS_PROVIDER', 'MOCK')
    if proveedor == 'MOCK':
        return MockPaymentProvider()
    # Punto de extension futuro: return WompiProvider(), PayUProvider(), etc.
    return MockPaymentProvider()
