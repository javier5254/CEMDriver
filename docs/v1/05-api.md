# Diseño de API — CMEDriver (MVP)

Base URL: `/api/`. Todas las rutas (excepto login) requieren header `Authorization: Bearer <token>`. Documentación interactiva servida en `/api/docs/` (drf-spectacular / Swagger).

## Auth
| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| POST | `/api/auth/login/` | público | `{username, password}` → `{access, refresh, user}` |
| POST | `/api/auth/refresh/` | público | Refresca el access token |
| GET | `/api/auth/me/` | cualquiera autenticado | Perfil del usuario actual |

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
| GET/POST | `/api/servicios/{id}/mensajes/` | CLIENTE, MOTORIZADO asignado | Chat simple por servicio |

## Rutas
| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| GET/POST | `/api/rutas/` | ALISTADOR | Crear/listar rutas |
| GET/PATCH | `/api/rutas/{id}/` | ALISTADOR, MOTORIZADO asignado | — |

## Tracking
| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| POST | `/api/tracking/posicion/` | MOTORIZADO | `{servicio_id, lat, lng}` (llamado cada 5-10s desde el navegador) |
| GET | `/api/tracking/ultima-posicion/?servicio_id=` | CLIENTE, ADMIN | Última posición conocida |

## Chatbot (implementado como flujo de frontend sobre endpoints existentes)
El chatbot del MVP no es un endpoint propio: es un flujo de UI que combina `GET /api/productos/disponibles-chatbot/`, `GET /api/cobertura/agenda-disponible/` y `POST /api/servicios/planificar/` / creación de compra, presentado como conversación por menús. Esto se documenta como decisión de diseño en [03-arquitectura.md](03-arquitectura.md).
