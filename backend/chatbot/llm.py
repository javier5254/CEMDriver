"""
chatbot/llm.py — "cerebro" del chatbot.

SIMULADO: no hay ninguna llamada a un LLM real (no hay API key disponible).
`MockLLMClient.responder()` decide con reglas simples de palabras clave (no
NLU real) que "tool" invocar, y arma una respuesta en texto. Lo que SI es real
es la arquitectura alrededor de esa decision:

  - Una lista de "tools": funciones Python planas (mas abajo) que envuelven la
    logica de dominio ya existente (inventario, cobertura, servicios, pagos).
  - Persistencia de historial + de la funcion invocada (MensajeBot.function_call)
    para poder auditar/demostrar el tool-calling.
  - Estado de conversacion (slot-filling) guardado en Conversacion.contexto
    entre turnos, igual que necesitaria un LLM real con "memoria" de sesion.

Para conectar un LLM real (ej. Anthropic) mas adelante, el cambio quedaria
practicamente aislado a este archivo:
  1. Declarar las mismas funciones de mas abajo como tool schemas (JSON
     schema) para la API de tool use.
  2. Reemplazar MockLLMClient por un cliente que llame a
     anthropic.Anthropic().messages.create(..., tools=tools_schema) en un loop
     hasta que el modelo devuelva texto final, ejecutando la tool que pida via
     `tool_use` en cada paso.
  3. chatbot/views.py no cambia: solo conoce `MockLLMClient().responder(...)`.

Reuso de reglas de negocio (RN-03, leadtime/dia-habil):
  tool_consultar_agenda y tool_crear_recoleccion NO reimplementan el calculo
  de fechas validas ni la validacion de leadtime. En su lugar, arman una
  request DRF "interna" (via APIRequestFactory + force_authenticate, el mismo
  mecanismo que usa el propio test suite de este proyecto) y llaman
  directamente a coverage.views.AgendaDisponibleView y a
  services.views.ServicioViewSet.planificar respectivamente. Asi, el chatbot y
  el endpoint HTTP real ejecutan exactamente el mismo codigo y no se pueden
  desincronizar (no se modifica services/views.py ni coverage/views.py).
"""
import datetime
import re

from rest_framework.test import APIRequestFactory, force_authenticate

from coverage.views import AgendaDisponibleView
from inventory.models import Producto
from payments.models import Pago
from payments.provider import obtener_proveedor_pago
from services.models import EstadoServicio, Servicio, TipoServicio
from services.views import ServicioViewSet

_factory = APIRequestFactory()


# ---------------------------------------------------------------------------
# "Tools": funciones planas que envuelven logica de dominio existente. Cada
# una es candidata directa a exponerse como tool-schema a un LLM real.
# ---------------------------------------------------------------------------

def tool_listar_productos():
    """Mismo filtro que GET /api/productos/disponibles-chatbot/
    (inventory.views.ProductosDisponiblesChatbotView)."""
    productos = Producto.objects.filter(disponible_chatbot=True, stock__gt=0).order_by('nombre')
    return [
        {'id': p.id, 'sku': p.sku, 'nombre': p.nombre, 'precio': str(p.precio), 'stock': p.stock}
        for p in productos
    ]


def tool_consultar_agenda(cliente, zona: str):
    """Reusa coverage.views.AgendaDisponibleView (RN-03) sin reimplementar el
    calculo de leadtime/dia-habil. `cliente` solo se usa para autenticar la
    request interna (la vista exige IsAuthenticated); no viaja como argumento
    "de negocio" de la tool."""
    request = _factory.get('/api/cobertura/agenda-disponible/', {'zona': zona})
    force_authenticate(request, user=cliente)
    response = AgendaDisponibleView.as_view()(request)

    if response.status_code != 200:
        detalle = response.data.get('detail') if isinstance(response.data, dict) else str(response.data)
        return {'error': detalle or 'No se pudo consultar la agenda para esa zona.'}

    return {
        'zona': response.data['zona'],
        'leadtime_dias': response.data['leadtime_dias'],
        'fechas_disponibles': response.data['fechas_disponibles'],
    }


def _mensaje_error(detalle):
    """Normaliza el `.data` de una respuesta de error de DRF (puede ser un
    dict de {campo: [errores]} o una lista de strings) a un texto legible."""
    if isinstance(detalle, dict):
        partes = []
        for campo, errores in detalle.items():
            texto = ', '.join(str(e) for e in errores) if isinstance(errores, (list, tuple)) else str(errores)
            partes.append(texto if campo == 'detail' else f'{campo}: {texto}')
        return ' | '.join(partes) if partes else 'Datos invalidos.'
    if isinstance(detalle, (list, tuple)):
        return ' | '.join(str(e) for e in detalle)
    return str(detalle)


def tool_crear_recoleccion(cliente, zona, direccion_origen, fecha_agenda, producto=None):
    """Crea una RECOLECCION reusando POST /api/servicios/planificar/
    (services.views.ServicioViewSet.planificar) en vez de reimplementar su
    validacion de leadtime/dia-habil: se construye una request DRF interna
    contra la misma vista, autenticada como `cliente`, de modo que el chatbot
    y el endpoint HTTP real ejecutan exactamente el mismo codigo."""
    if isinstance(fecha_agenda, (datetime.date, datetime.datetime)):
        fecha_agenda = fecha_agenda.isoformat()

    payload = {'zona': zona, 'direccion_origen': direccion_origen, 'fecha_agenda': fecha_agenda}
    if producto is not None:
        payload['producto'] = producto.id if hasattr(producto, 'id') else producto

    request = _factory.post('/api/servicios/planificar/', payload, format='json')
    force_authenticate(request, user=cliente)
    response = ServicioViewSet.as_view({'post': 'planificar'})(request)

    if response.status_code == 201:
        data = response.data
        return {'ok': True, 'servicio_id': data['id'], 'estado': data['estado'], 'fecha_agenda': data['fecha_agenda']}
    return {'ok': False, 'error': _mensaje_error(response.data)}


def tool_crear_compra(cliente, producto: Producto, direccion_destino: str, zona: str, fecha_agenda):
    """Crea un Servicio tipo ENTREGA para la compra de un producto por
    chatbot y procesa el pago de inmediato (para el MVP no existe una etapa
    de "carrito" separada: comprar = agendar entrega + pagar en el mismo paso).

    No hay un endpoint existente de "creacion de servicio por el propio
    cliente" para ENTREGA (POST /api/servicios/ es exclusivo de ALISTADOR, y
    /planificar/ siempre crea RECOLECCION), asi que aqui se construye el
    Servicio directamente via ORM, replicando el unico requisito que exige
    ServicioCreateSerializer.validate() para ENTREGA (direccion_destino
    obligatoria) mas la verificacion de disponibilidad del producto.
    """
    if isinstance(fecha_agenda, (datetime.date, datetime.datetime)):
        fecha_agenda = fecha_agenda if isinstance(fecha_agenda, datetime.date) else fecha_agenda.date()
    else:
        fecha_agenda = datetime.date.fromisoformat(fecha_agenda)

    if not producto.disponible_chatbot or producto.stock <= 0:
        return {'error': f'"{producto.nombre}" ya no esta disponible por el chatbot en este momento.'}
    if not direccion_destino:
        return {'error': 'Falta la direccion de entrega.'}

    servicio = Servicio.objects.create(
        tipo=TipoServicio.ENTREGA,
        cliente=cliente,
        producto=producto,
        zona=zona,
        direccion_destino=direccion_destino,
        fecha_agenda=fecha_agenda,
        estado=EstadoServicio.CREADO,
    )

    pago = Pago.objects.create(cliente=cliente, servicio=servicio, producto=producto, monto=producto.precio)
    pago = obtener_proveedor_pago().procesar(pago)

    return {
        'servicio_id': servicio.id,
        'servicio_estado': servicio.estado,
        'pago_id': pago.id,
        'pago_estado': pago.estado,
        'pago_referencia': pago.referencia,
    }


# ---------------------------------------------------------------------------
# "LLM" simulado: matching de palabras clave + maquina de estados simple
# guardada en Conversacion.contexto.
# ---------------------------------------------------------------------------

SALUDOS = ('hola', 'buenas', 'buenos dias', 'buenas tardes', 'buenas noches', 'ola', 'menu', 'ayuda')
KEYWORDS_COMPRA = ('comprar', 'compra', 'producto', 'catalogo', 'catálogo')
KEYWORDS_RECOLECCION = ('recolec', 'recoger', 'recojan', 'recogida', 'pasen por', 'pasar por')
FECHA_RE = re.compile(r'(\d{4}-\d{2}-\d{2})')

MENSAJE_SALUDO = (
    'Hola! Soy el asistente virtual de CMEDriver. Puedo ayudarte a: '
    '1) comprar un producto y agendar su entrega, o '
    '2) solicitar una recoleccion de un paquete tuyo. '
    'Cuentame que necesitas (ej. "quiero comprar" o "quiero que recojan un paquete").'
)
MENSAJE_FALLBACK = (
    'No estoy seguro de haber entendido. Puedo ayudarte a comprar un producto o a '
    'solicitar una recoleccion. ¿Cual de las dos opciones necesitas?'
)


class MockLLMClient:
    """Ver docstring del modulo. `responder` es el unico metodo publico."""

    def responder(self, conversacion, mensaje_nuevo: str) -> dict:
        texto = (mensaje_nuevo or '').strip()
        texto_low = texto.lower()
        contexto = dict(conversacion.contexto or {})

        # 1. Continuar un flujo en curso (slot-filling), sin importar el texto.
        if contexto.get('intencion') == 'recoleccion':
            return self._continuar_recoleccion(conversacion, contexto, texto)
        if contexto.get('intencion') == 'comprar':
            return self._continuar_compra(conversacion, contexto, texto)

        # 2. Saludo / mensaje vacio -> menu de opciones.
        if not texto or any(s in texto_low for s in SALUDOS):
            self._guardar_contexto(conversacion, {})
            return self._respuesta(MENSAJE_SALUDO)

        # 3. Deteccion de intencion nueva: compra.
        productos = tool_listar_productos()
        producto_mencionado = self._buscar_producto_mencionado(texto_low, productos)
        if producto_mencionado or any(k in texto_low for k in KEYWORDS_COMPRA):
            return self._iniciar_compra(conversacion, producto_mencionado, productos)

        # 4. Deteccion de intencion nueva: recoleccion.
        if any(k in texto_low for k in KEYWORDS_RECOLECCION):
            return self._iniciar_recoleccion(conversacion)

        # 5. Fallback amigable (nunca un error 500: si no reconocemos nada,
        # simplemente pedimos que aclare).
        return self._respuesta(MENSAJE_FALLBACK)

    # -- helpers de estado -------------------------------------------------

    @staticmethod
    def _respuesta(texto, function_call=None):
        return {'texto': texto, 'function_call': function_call}

    @staticmethod
    def _guardar_contexto(conversacion, contexto):
        conversacion.contexto = contexto
        conversacion.save(update_fields=['contexto'])

    @staticmethod
    def _buscar_producto_mencionado(texto_low, productos):
        for p in productos:
            if p['nombre'].lower() in texto_low:
                return p
        return None

    @staticmethod
    def _separar_zona_direccion(texto):
        """Simplificacion deliberada: en vez de NLU real para extraer
        entidades libres, se le pide al usuario "zona, direccion" en un solo
        mensaje separado por coma. Es la misma clase de heuristica de
        parsing simple que ya usa el resto del MVP (menus/valores exactos)."""
        partes = [p.strip() for p in texto.split(',', 1)]
        if len(partes) == 2 and partes[0] and partes[1]:
            return partes[0], partes[1]
        return None, None

    # -- flujo de compra -----------------------------------------------------

    def _iniciar_compra(self, conversacion, producto_mencionado, productos):
        if not productos:
            self._guardar_contexto(conversacion, {})
            return self._respuesta(
                'Por ahora no tenemos productos disponibles para comprar por el chatbot. Lo siento.',
                function_call={'tool': 'tool_listar_productos', 'args': {}, 'result': productos},
            )

        if not producto_mencionado:
            listado = '\n'.join(f"- {p['nombre']} (${p['precio']})" for p in productos)
            self._guardar_contexto(conversacion, {'intencion': 'comprar'})
            return self._respuesta(
                f'Estos son los productos disponibles:\n{listado}\n¿Cual te interesa?',
                function_call={'tool': 'tool_listar_productos', 'args': {}, 'result': productos},
            )

        self._guardar_contexto(conversacion, {
            'intencion': 'comprar',
            'producto_id': producto_mencionado['id'],
            'producto_nombre': producto_mencionado['nombre'],
        })
        return self._respuesta(
            f"Perfecto, {producto_mencionado['nombre']} cuesta ${producto_mencionado['precio']}. "
            '¿En que zona y a que direccion quieres recibirlo? '
            '(respondeme como "Zona Norte, Calle 10 # 5-20")'
        )

    def _continuar_compra(self, conversacion, contexto, texto):
        if not contexto.get('producto_id'):
            # Todavia no sabemos que producto quiere: este turno es su
            # respuesta al listado (nombre del producto), no zona/direccion.
            productos = tool_listar_productos()
            producto_mencionado = self._buscar_producto_mencionado(texto.lower(), productos)
            return self._iniciar_compra(conversacion, producto_mencionado, productos)

        if not contexto.get('zona') or not contexto.get('direccion'):
            return self._pedir_zona_y_agenda(conversacion, contexto, texto, campo_direccion='direccion')

        match = FECHA_RE.search(texto)
        if not match:
            return self._respuesta('No reconoci una fecha valida. Escribela en formato AAAA-MM-DD, por favor.')

        producto = Producto.objects.filter(pk=contexto['producto_id']).first()
        if not producto:
            self._guardar_contexto(conversacion, {})
            return self._respuesta(
                'El producto seleccionado ya no esta disponible. Empecemos de nuevo, ¿que deseas comprar?'
            )

        fecha_txt = match.group(1)
        resultado = tool_crear_compra(
            cliente=conversacion.cliente,
            producto=producto,
            direccion_destino=contexto['direccion'],
            zona=contexto['zona'],
            fecha_agenda=fecha_txt,
        )
        function_call = {
            'tool': 'tool_crear_compra',
            'args': {
                'producto_id': producto.id, 'zona': contexto['zona'],
                'direccion_destino': contexto['direccion'], 'fecha_agenda': fecha_txt,
            },
            'result': resultado,
        }

        if resultado.get('error'):
            # No reseteamos el contexto: puede reintentar con otro dato.
            return self._respuesta(resultado['error'], function_call=function_call)

        self._guardar_contexto(conversacion, {})
        return self._respuesta(
            f"Listo! Cree tu servicio de entrega #{resultado['servicio_id']} para el {fecha_txt}. "
            f"El pago quedo {resultado['pago_estado']}.",
            function_call=function_call,
        )

    # -- flujo de recoleccion -------------------------------------------------

    def _iniciar_recoleccion(self, conversacion):
        self._guardar_contexto(conversacion, {'intencion': 'recoleccion'})
        return self._respuesta(
            'Con gusto. Para agendar la recoleccion necesito la zona y la direccion donde '
            'debemos recoger el paquete. Respondeme como "Zona Norte, Calle 10 # 5-20"'
        )

    def _continuar_recoleccion(self, conversacion, contexto, texto):
        if not contexto.get('zona') or not contexto.get('direccion'):
            return self._pedir_zona_y_agenda(conversacion, contexto, texto, campo_direccion='direccion')

        match = FECHA_RE.search(texto)
        if not match:
            return self._respuesta('No reconoci una fecha valida. Escribela en formato AAAA-MM-DD, por favor.')

        fecha_txt = match.group(1)
        resultado = tool_crear_recoleccion(
            cliente=conversacion.cliente,
            zona=contexto['zona'],
            direccion_origen=contexto['direccion'],
            fecha_agenda=fecha_txt,
        )
        function_call = {
            'tool': 'tool_crear_recoleccion',
            'args': {'zona': contexto['zona'], 'direccion_origen': contexto['direccion'], 'fecha_agenda': fecha_txt},
            'result': resultado,
        }

        if not resultado.get('ok'):
            # No reseteamos el contexto (RN-03): puede intentar con otra fecha
            # sin tener que repetir zona/direccion.
            return self._respuesta(
                f"No fue posible agendar esa fecha: {resultado['error']} ¿Quieres intentar con otra fecha?",
                function_call=function_call,
            )

        self._guardar_contexto(conversacion, {})
        return self._respuesta(
            f"Listo! Tu recoleccion quedo registrada como el servicio #{resultado['servicio_id']} "
            f"para el {resultado['fecha_agenda']}.",
            function_call=function_call,
        )

    # -- compartido: zona + direccion -> consulta de agenda -------------------

    def _pedir_zona_y_agenda(self, conversacion, contexto, texto, campo_direccion):
        zona, direccion = self._separar_zona_direccion(texto)
        if not zona or not direccion:
            return self._respuesta(
                'Necesito la zona y la direccion juntas, separadas por coma. '
                'Ej: "Zona Norte, Calle 10 # 5-20"'
            )

        contexto['zona'] = zona
        contexto[campo_direccion] = direccion
        self._guardar_contexto(conversacion, contexto)

        agenda = tool_consultar_agenda(conversacion.cliente, zona)
        function_call = {'tool': 'tool_consultar_agenda', 'args': {'zona': zona}, 'result': agenda}

        if agenda.get('error'):
            self._guardar_contexto(conversacion, {})
            return self._respuesta(agenda['error'], function_call=function_call)

        fechas = agenda['fechas_disponibles'][:5]
        contexto['fechas_sugeridas'] = fechas
        self._guardar_contexto(conversacion, contexto)

        fechas_txt = ', '.join(fechas) if fechas else '(no hay fechas disponibles en las proximas semanas)'
        return self._respuesta(
            f"Estas son las fechas disponibles para la zona {zona} "
            f"(leadtime de {agenda['leadtime_dias']} dia(s)): {fechas_txt}. "
            '¿Cual prefieres? (formato AAAA-MM-DD)',
            function_call=function_call,
        )
