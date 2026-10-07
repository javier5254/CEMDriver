# Diseño de API — CMEDriver (v2)

Base URL: `/api/`. Todas las rutas (excepto login/registro/reset) requieren header `Authorization: Bearer <token>` **o** `X-API-Key: <clave>` (para sistemas externos, ver [Integraciones](#integraciones-api-keys-y-webhooks)). Documentación interactiva servida en `/api/docs/` (drf-spectacular / Swagger). WebSockets documentados aparte al final.

## Auth
| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| POST | `/api/auth/login/` | público | `{username, password}` → `{access, refresh, user}`. `username` acepta el nombre de usuario **o el correo registrado** |
| POST | `/api/auth/refresh/` | público | Refresca el access token |
| GET | `/api/auth/me/` | cualquiera autenticado | Perfil del usuario actual |
| POST | `/api/auth/password-reset/` | público | `{email}` → envía un enlace de restablecimiento por correo si existe (siempre responde 200, nunca revela si el correo existe) |
| POST | `/api/auth/password-reset/confirm/` | público | `{uid, token, new_password}` → cambia la contraseña si el token es válido y no ha sido usado |

## Usuarios (accounts)
| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| GET/POST | `/api/usuarios/` | ADMIN | Listar/crear usuarios |
| GET/PATCH/DELETE | `/api/usuarios/{id}/` | ADMIN | Detalle/editar/desactivar |

## Cobertura
| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| GET/POST | `/api/cobertura/` | ADMIN (lectura: todos) | Zonas, leadtime, agenda |
| GET/PATCH/DELETE | `/api/cobertura/{id}/` | ADMIN | — |
| GET | `/api/cobertura/agenda-disponible/?zona=` | CLIENTE, ALISTADOR | Fechas válidas según leadtime |

## Inventario
El inventario es responsabilidad exclusiva del **Administrador**: solo ese rol puede crear/editar/eliminar productos. El Alistador y el Cliente solo tienen lectura (el alistador para asociar un producto a un servicio, el cliente indirectamente a través del chatbot).

| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| GET/POST | `/api/productos/` | ADMIN (crea) · cualquier autenticado (lee) | Catálogo |
| GET/PATCH/DELETE | `/api/productos/{id}/` | ADMIN | — |
| GET | `/api/productos/disponibles-chatbot/` | CLIENTE | Solo productos con `disponible_chatbot=true` y stock>0 |

## Servicios
| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| GET/POST | `/api/servicios/` | ALISTADOR (crea), todos (lectura filtrada por rol) | Crear/listar servicios |
| GET/PATCH | `/api/servicios/{id}/` | según rol | Detalle |
| POST | `/api/servicios/{id}/asignar-ruta/` | ALISTADOR | `{ruta_id}` |
| POST | `/api/servicios/{id}/recibir-en-centro/` | MOTORIZADO | Solo tipo ENTREGA |
| POST | `/api/servicios/{id}/iniciar-transito/` | MOTORIZADO | — |
| POST | `/api/servicios/{id}/cerrar/` | MOTORIZADO | Entrega: confirma entrega. Recolección: requiere `foto` + `firma` |
| POST | `/api/servicios/{id}/novedad/` | MOTORIZADO | `{tipo, detalle, accion}` |
| POST | `/api/servicios/planificar/` | CLIENTE | Crea una RECOLECCION propia validando `agenda-disponible` |
| GET/POST | `/api/servicios/{id}/mensajes/` | CLIENTE, MOTORIZADO asignado | Chat simple por servicio (además del WebSocket en tiempo real, ver más abajo) |
| PUT | `/api/servicios/{id}/productos/` | ALISTADOR | `[{producto, cantidad}, ...]` — reemplaza por completo las líneas de producto del servicio (inventario avanzado, RF-26) |

## Rutas
| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| GET/POST | `/api/rutas/` | ALISTADOR | Crear/listar rutas |
| GET/PATCH | `/api/rutas/{id}/` | ALISTADOR, MOTORIZADO asignado | — |

## Tracking
| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| POST | `/api/tracking/posicion/` | MOTORIZADO | `{servicio, lat, lng}` (llamado cada ~8s desde el navegador; el campo es `servicio`, no `servicio_id`) |
| GET | `/api/tracking/ultima-posicion/?servicio_id=` | CLIENTE, ADMIN | Última posición conocida (fetch inicial; luego se recibe por WebSocket) |

## Optimización de rutas
| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| POST | `/api/optimizacion/rutas/{ruta_id}/` | ADMIN, ALISTADOR | Geocodifica las direcciones de los servicios de la ruta (Nominatim/OpenStreetMap, con caché) y devuelve un orden de visita sugerido (vecino más cercano) + distancia estimada + direcciones no geocodificadas. No persiste ningún orden — es solo una sugerencia |

## Chatbot
El chatbot v2 sí es un endpoint real con arquitectura de tool-calling (ver [03-arquitectura.md](03-arquitectura.md) para el detalle de la simulación del modelo de lenguaje).

| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| POST | `/api/chatbot/mensaje/` | CLIENTE | `{conversacion_id?, texto}` → `{conversacion_id, respuesta, accion}`. `accion` es `null` o `{tipo: "servicio_creado"\|"pago", ...}` cuando el turno completó una compra/recolección |
| GET | `/api/chatbot/conversaciones/{id}/mensajes/` | CLIENTE (dueño) | Historial de una conversación |

## Pagos
| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| GET | `/api/pagos/{id}/` | CLIENTE (dueño), ADMIN | Estado de un pago (`PENDIENTE`/`APROBADO`/`RECHAZADO`), generado automáticamente al completar una compra por chatbot |

## Integraciones: API keys y webhooks
Solo ADMIN. Ver [03-arquitectura.md](03-arquitectura.md) para el modelo de autenticación por API key.

| Método | Endpoint | Descripción |
|---|---|---|
| GET/POST | `/api/integraciones/api-keys/` | Lista (sin la clave) / crea una API key — la clave cruda solo se devuelve **una vez**, en la respuesta de creación |
| PATCH/DELETE | `/api/integraciones/api-keys/{id}/` | Activar/desactivar o eliminar |
| GET/POST | `/api/integraciones/webhooks/` | Lista / crea un endpoint de webhook (`{nombre, url, eventos, secret?}`) |
| GET/PATCH/DELETE | `/api/integraciones/webhooks/{id}/` | Detalle/editar/eliminar |
| GET | `/api/integraciones/webhooks/{id}/entregas/` | Log de intentos de entrega (`WebhookDelivery`) |

Eventos disponibles: `servicio.creado`, `servicio.asignado`, `servicio.entregado`, `servicio.recolectado`, `servicio.novedad`, `servicio.devuelto`. Cada entrega va firmada con `X-CMEDriver-Signature` (HMAC-SHA256 sobre el cuerpo JSON, usando el `secret` del endpoint).

## WebSockets (tiempo real)
Requieren el access token JWT como query param (`?token=...`), ya que el navegador no puede mandar headers al abrir un WebSocket.

| Canal | Quién se conecta | Descripción |
|---|---|---|
| `ws://<host>/ws/tracking/<servicio_id>/?token=` | CLIENTE (dueño), MOTORIZADO asignado, ADMIN/ALISTADOR | Recibe cada posición GPS apenas se reporta por REST (solo lectura) |
| `ws://<host>/ws/chat/<servicio_id>/?token=` | CLIENTE (dueño), MOTORIZADO asignado, ADMIN/ALISTADOR | Bidireccional: enviar `{"texto": "..."}` guarda el mensaje y lo difunde a todos los conectados, incluido el autor |

Si el WebSocket no conecta o se cae, el frontend cae de vuelta a polling automáticamente (RNF-10).
