# Roadmap futuro — CMEDriver (más allá de v2)

> **Nota (2026-10-09):** este documento es **histórico**: se redactó antes de la reducción de alcance que retiró el inventario, los pagos y el chatbot (el chat quedó solo como canal entre el cliente y el motorizado) y **no refleja el alcance vigente**. Todavía lista como pendientes el chatbot con LLM real, los pagos y el inventario avanzado; esos tres ítems son ahora una mejora futura opcional (n.º 14 de la [hoja de ruta vigente](entrega/08-limitaciones-y-mejoras.md#84-hoja-de-ruta-de-mejoras-priorizada)). Prevalece la documentación de [entrega/](entrega/00-guia-de-entrega.md), en particular [entrega/01-requerimientos.md §2.4](entrega/01-requerimientos.md#24-cambios-de-alcance).

Casi todo lo que este documento proponía como "roadmap" en el MVP original ya se construyó en v2 (ver [06-cronograma.md](06-cronograma.md) para el detalle). Esta versión documenta qué de eso quedó real vs. simulado, y qué sigue siendo trabajo futuro genuino.

## Ya completado en v2 (con su alcance real)
| Idea original del roadmap MVP | Estado en v2 |
|---|---|
| WebSockets para tracking/chat | **Hecho de verdad.** Django Channels + Daphne, capa en memoria (no Redis todavía — ver abajo) |
| Chatbot con IA (LLM) | **Arquitectura real, modelo simulado.** Tool-calling real sobre los mismos endpoints; sin API key de un LLM real disponible (`MockLLMClient`, ver [03-arquitectura.md](03-arquitectura.md)) |
| Optimización de rutas | **Hecho de verdad**, con geocoding real (Nominatim) y heurística de vecino más cercano — no hay motor de ruteo comercial, pero tampoco es una simulación |
| API Key + Webhooks para integraciones | **Hecho de verdad.** Autenticación por API Key, webhooks firmados con HMAC y log de entregas |
| App móvil nativa (Capacitor) | **Configurado, build real no logrado en este entorno.** Ver limitación técnica puntual en [11-manual-distribucion.md](11-manual-distribucion.md) §4 |
| Inventario avanzado (multi-producto) | **Hecho de verdad.** Tabla `ServicioProducto`, endpoint idempotente |
| Pagos | **Arquitectura real, proveedor simulado.** `MockPaymentProvider` sin credenciales de Wompi/PayU (ver [03-arquitectura.md](03-arquitectura.md)) |

## Trabajo futuro genuino (todavía no hecho)

### Tiempo real a escala
- Migrar la capa de canales de "en memoria" a `channels_redis` para poder correr más de un proceso/worker (la capa en memoria de v2 solo sirve para un único proceso de desarrollo).
- Notificaciones push reales (web push / FCM / APNs) para cambios de estado de servicio, más allá del WebSocket (que solo notifica mientras la pestaña está abierta).

### Chatbot con LLM real
- Conectar una API key real (ej. Anthropic) reemplazando `MockLLMClient` — la arquitectura de tool-calling ya está lista para eso, es un cambio localizado a un archivo.
- NLU real para extraer entidades (dirección, fecha) en vez del parseo por reglas simples actual.

### Optimización de rutas — siguiente nivel
- Resolver un problema de ruteo de múltiples vehículos (VRP) real, con restricciones de capacidad y ventana horaria, en vez de una sola heurística de vecino más cercano por ruta.
- Un "depot" real (ubicación del centro de mensajería) como punto de partida, en vez de usar el primer servicio creado.
- Tiempos estimados de llegada (ETA) usando un proveedor de ruteo (no solo distancia en línea recta/haversine).

### Plataforma e integraciones — siguiente nivel
- OAuth2 client-credentials en vez de API Key simple, si se necesita revocación granular por scope.
- Migrar de monolito Django modular a servicios independientes si la carga lo justifica (cada app ya está diseñada para eso).
- Reintentos automáticos con backoff para webhooks fallidos (hoy es un único intento, registrado pero no reintentado).

### App móvil nativa
- Lograr el build real de Android en un entorno sin la limitación de sockets encontrada (ver troubleshooting), o vía CI (GitHub Actions con un runner Ubuntu/macOS).
- Build de iOS (requiere una máquina macOS con Xcode, no evaluado en este proyecto).
- GPS en segundo plano real (el modo navegador solo transmite con la app en primer plano).

### Pagos — siguiente nivel
- Conectar una pasarela real (Wompi, PayU, Stripe) reemplazando `MockPaymentProvider`.
- Webhooks entrantes de la pasarela (confirmación asíncrona de pago) en vez de aprobación síncrona simulada.

### Inventario avanzado — siguiente nivel
- Reglas de stock por centro con alertas de reabastecimiento automáticas.
- Descontar stock real al confirmar una línea de `ServicioProducto`.

### Pulido visual del frontend (llevar los mockups al código)
- Las pantallas del build funcional (Ionic + Angular) ya usan la paleta de color iOS (`mode: 'ios'`, `variables.scss`), pero siguen sobre los componentes Ionic por defecto (listas planas, formularios estándar) en vez del tratamiento de tarjetas/sombras/estados vacíos de los [mockups](12-mockups.md). Se probó aplicar ese tratamiento directamente a las pantallas de API Keys y Webhooks, pero no se sintió fiel al lenguaje visual de Apple buscado, así que se revirtió; el mockup de esas dos pantallas quedó actualizado como referencia para un intento futuro más cuidadoso.
