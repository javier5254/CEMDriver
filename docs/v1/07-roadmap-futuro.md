# Roadmap futuro — CMEDriver (fuera del MVP)

Estas son las evoluciones naturales del proyecto una vez el MVP esté validado. Sirven también como sección de "trabajo futuro" en el informe final.

## Tiempo real de verdad
- Migrar tracking GPS y chat de polling a **WebSockets** (Django Channels + Redis) para latencia mucho menor y menos peticiones.
- Notificaciones push (web push / móvil nativo) para cambios de estado de servicio.

## Chatbot con IA
- Reemplazar el flujo de menús fijos por un chatbot conversacional usando un LLM (ej. API de Claude), manteniendo el inventario y la matriz de cobertura como "herramientas" (function calling) que el modelo puede consultar — comprar, agendar recolección, consultar estado, todo en lenguaje natural.

## Optimización de rutas
- Ruteo automático de servicios a motorizados según cercanía, capacidad y ventana horaria (en vez de asignación manual del alistador).
- Integración con proveedores de mapas para tiempos estimados de llegada (ETA).

## Plataforma e integraciones
- Publicar la API con autenticación por API Key/OAuth2 para clientes externos (e-commerce, ERPs) que quieran crear servicios automáticamente.
- Webhooks salientes (ej. `servicio.entregado`, `servicio.novedad`) para que sistemas externos reaccionen a cambios de estado.
- Migrar de monolito Django modular a servicios independientes (accounts, tracking, inventory) si la carga lo justifica.

## App móvil nativa
- Empaquetar el frontend Ionic con Capacitor para publicarlo en Google Play / App Store, habilitando GPS en segundo plano y notificaciones push nativas (limitantes reales del modo "solo navegador" del MVP).

## Inventario avanzado
- Múltiples productos por servicio (tabla intermedia `SERVICIO_PRODUCTO`).
- Reglas de stock por centro con alertas de reabastecimiento.

## Pagos
- Pasarela de pagos real (ej. Wompi, PayU) para las compras generadas desde el chatbot.
