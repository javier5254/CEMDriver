# Formatos para historias de usuario y requisitos — CMEDriver

Plantillas reutilizables para documentar nuevas historias de usuario y requerimientos funcionales/no funcionales a lo largo del proyecto. Úsalas para registrar cualquier requisito nuevo o cambio de alcance de forma consistente con lo ya documentado en [02-requisitos.md](02-requisitos.md).

## 1. Formato de historia de usuario

| Campo | Contenido |
|---|---|
| **ID** | HU-XX |
| **Rol / actor** | (Administrador / Alistador / Motorizado / Cliente / Sistema externo) |
| **Historia** | Como \_\_\_, quiero \_\_\_, para \_\_\_ |
| **Criterios de aceptación** | 1. Dado \_\_\_, cuando \_\_\_, entonces \_\_\_ <br> 2. ... |
| **Prioridad** | Alta / Media / Baja |
| **Dependencias** | (otras HU o RF/RN que deben existir primero) |
| **Endpoint(s) relacionados** | (referencia a [05-api.md](05-api.md), ej. `POST /api/servicios/`) |
| **Estado** | Por hacer / En progreso / Hecho / Probado |

### Ejemplo diligenciado
| Campo | Contenido |
|---|---|
| **ID** | HU-19 |
| **Rol / actor** | Cliente |
| **Historia** | Como cliente, quiero recibir una notificación cuando mi servicio cambie de estado, para no tener que refrescar la app constantemente. |
| **Criterios de aceptación** | 1. Dado que un servicio pasa a EN_TRANSITO, cuando el cambio ocurre, entonces el cliente ve el nuevo estado en su lista de servicios sin recargar manualmente (polling). <br> 2. Dado que el servicio se cierra (ENTREGADO/RECOLECTADO), entonces desaparece de "servicios activos" y aparece en "historial". |
| **Prioridad** | Media |
| **Dependencias** | RF-15 (tracking), RF-09 (motorizado actualiza estado) |
| **Endpoint(s) relacionados** | `GET /api/servicios/` (polling) |
| **Estado** | Fuera del MVP — ver [07-roadmap-futuro.md](07-roadmap-futuro.md) |

---

## 2. Formato de requerimiento funcional (RF)

| Campo | Contenido |
|---|---|
| **ID** | RF-XX |
| **Nombre** | (nombre corto del requerimiento) |
| **Descripción** | El sistema debe permitir/hacer que \_\_\_ |
| **Actor(es)** | (quién lo usa) |
| **Prioridad** | Alta / Media / Baja |
| **Regla(s) de negocio asociada(s)** | (referencia a RN-XX en [02-requisitos.md](02-requisitos.md)) |
| **Criterio de verificación** | ¿Cómo se comprueba que está implementado? |

## 3. Formato de requerimiento no funcional (RNF)

| Campo | Contenido |
|---|---|
| **ID** | RNF-XX |
| **Categoría** | Seguridad / Rendimiento / Usabilidad / Escalabilidad / Mantenibilidad / Otro |
| **Descripción** | El sistema debe \_\_\_ |
| **Métrica / umbral medible** | (ej. "tiempo de respuesta < 500ms", "polling cada 5-10s") |
| **Prioridad** | Alta / Media / Baja |
| **Criterio de verificación** | ¿Cómo se comprueba? |

## 4. Formato de regla de negocio (RN)

| Campo | Contenido |
|---|---|
| **ID** | RN-XX |
| **Descripción** | (la regla, en una frase verificable) |
| **Aplica a** | (qué entidad/proceso) |
| **Consecuencia si se viola** | (qué error o bloqueo debe producir el sistema) |

## Convenciones generales
- Los IDs son consecutivos y **nunca se reutilizan**, incluso si un requisito se elimina (para mantener trazabilidad histórica).
- Todo RF debe poder trazarse a al menos una Historia de Usuario y, cuando aplique, a un endpoint documentado en `05-api.md`.
- Cambios de alcance durante el desarrollo se agregan como nuevas filas en `02-requisitos.md`, usando estos mismos formatos — no se reescribe la numeración existente.
