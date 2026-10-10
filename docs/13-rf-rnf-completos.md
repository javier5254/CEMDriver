# RF y RNF completos — CMEDriver

> **Nota (2026-10-09):** este documento es **histórico**: se redactó antes de la reducción de alcance que retiró el inventario, los pagos y el chatbot (el chat quedó solo como canal entre el cliente y el motorizado) y **no refleja el alcance vigente**. Incluye los requerimientos retirados (RF-04, RF-18, RF-22, RF-23, RF-26 y RNF-13); los vigentes están en [entrega/01-requerimientos.md](entrega/01-requerimientos.md#4-requerimientos-funcionales-rf). Prevalece la documentación de [entrega/](entrega/00-guia-de-entrega.md), en particular [entrega/01-requerimientos.md §2.4](entrega/01-requerimientos.md#24-cambios-de-alcance).

Diligenciados con el formato de [09-formatos-historias-requisitos.md](09-formatos-historias-requisitos.md). Los criterios de verificación marcados **"Verificado"** ya fueron probados de punta a punta contra el backend real corriendo (no son solo aspiracionales).

## Requerimientos funcionales (RF)

### Administrador

| ID | Nombre | Descripción | Actor(es) | Prioridad | RN asociada | Criterio de verificación |
|---|---|---|---|---|---|---|
| RF-01 | Gestionar usuarios | El sistema debe permitir crear, editar y desactivar usuarios, asignando uno de los 4 roles (ADMIN, ALISTADOR, MOTORIZADO, CLIENTE) | Administrador | Alta | — | **Verificado**: `POST/GET/PATCH /api/usuarios/` protegido con `IsAdmin`; probado con usuario `admin` creando/listando los 4 roles |
| RF-02 | Configurar matriz de cobertura | El sistema debe permitir definir, por zona, el leadtime en días y los días/horas de agenda disponible | Administrador | Alta | RN-03 | **Verificado**: `POST /api/cobertura/` crea zona "Bogota - Chapinero" (leadtime=1, LUN-VIE); `GET /api/cobertura/agenda-disponible/?zona=` devuelve fechas calculadas correctamente |
| RF-03 | Consultar panel de servicios | El sistema debe mostrar un resumen de servicios agrupado por estado | Administrador | Media | — | **Verificado**: `GET /api/servicios/` sin filtro de rol para ADMIN devuelve todos los servicios; el dashboard del frontend los agrupa por estado |
| RF-04 | Gestionar inventario | El sistema debe permitir alta/edición de productos con stock por centro de mensajería y flag de disponibilidad en chatbot. Es responsabilidad exclusiva del administrador; el alistador solo puede **leer** el catálogo para asociar un producto a un servicio | Administrador (lectura: Alistador) | Media | RN-04 | **Verificado**: `POST /api/productos/` con rol ALISTADOR/MOTORIZADO/CLIENTE devuelve 403; con ADMIN devuelve 201; `GET /api/productos/disponibles-chatbot/` solo devuelve productos con stock>0 y flag activo |

### Alistador

| ID | Nombre | Descripción | Actor(es) | Prioridad | RN asociada | Criterio de verificación |
|---|---|---|---|---|---|---|
| RF-05 | Crear servicio manual | El sistema debe permitir crear un servicio (Entrega o Recolección) indicando cliente, dirección, producto y zona | Alistador | Alta | — | **Verificado**: `POST /api/servicios/` con `tipo=ENTREGA` exige `direccion_destino`; con `tipo=RECOLECCION` exige `direccion_origen` (validación en `ServicioCreateSerializer`) |
| RF-06 | Crear servicio vía API externa | El mismo endpoint de creación debe poder ser invocado por un sistema externo autenticado, con las mismas validaciones | Sistema externo | Media | — | El endpoint `POST /api/servicios/` no distingue el origen de la petición (UI o integración), solo el rol del token — mismo contrato para ambos casos |
| RF-07 | Asignar servicio a ruta | El sistema debe permitir asignar uno o varios servicios a una ruta con un motorizado | Alistador | Alta | — | **Verificado**: `POST /api/servicios/{id}/asignar-ruta/` cambia estado `CREADO -> ASIGNADO` y solo funciona si el estado previo es `CREADO` |
| RF-08 | Reasignar / consultar estado | El sistema debe permitir ver el estado de cada servicio y sus novedades asociadas | Alistador | Media | RN-05 | **Verificado**: la respuesta de `GET /api/servicios/{id}/` incluye el arreglo `novedades` con historial completo |

### Motorizado

| ID | Nombre | Descripción | Actor(es) | Prioridad | RN asociada | Criterio de verificación |
|---|---|---|---|---|---|---|
| RF-09 | Ver servicios asignados | El sistema debe listar únicamente los servicios de las rutas asignadas al motorizado autenticado | Motorizado | Alta | — | **Verificado**: `GET /api/servicios/` filtra por `ruta__motorizado=request.user` cuando el rol es MOTORIZADO |
| RF-10 | Recibir en centro (Entrega) | Antes de iniciar tránsito, un servicio de Entrega debe confirmarse como recibido en el centro de mensajería | Motorizado | Alta | RN-01 | **Verificado**: `POST /servicios/{id}/recibir-en-centro/` rechaza servicios de tipo RECOLECCION y solo aplica si el estado es `ASIGNADO` |
| RF-11 | Capturar evidencia (Recolección) | Un servicio de Recolección debe permitir adjuntar foto del producto y firma del cliente | Motorizado | Alta | RN-02 | **Verificado**: `POST /servicios/{id}/cerrar/` sin `foto`/`firma` devuelve 400 ("requiere foto y firma"); con ambos archivos, crea el registro `Evidencia` y cierra como `RECOLECTADO` |
| RF-12 | Iniciar tránsito / cerrar servicio | El sistema debe permitir marcar un servicio como en tránsito y luego como cerrado (entregado o recolectado) | Motorizado | Alta | RN-01, RN-02 | **Verificado**: transición `RECIBIDO_CENTRO/ASIGNADO -> EN_TRANSITO -> ENTREGADO/RECOLECTADO` probada end-to-end para ambos tipos |
| RF-13 | Registrar novedad | El sistema debe permitir registrar una novedad con una acción obligatoria: reintentar o devolver a centro | Motorizado | Alta | RN-05 | **Verificado**: `POST /servicios/{id}/novedad/` con `accion=REINTENTAR` deja el servicio en estado `NOVEDAD` (reintentable); con `accion=DEVOLVER_A_CENTRO` lo deja en `DEVUELTO` (terminal, `cerrar` ya no es posible) |
| RF-14 | Reportar posición GPS | El sistema debe recibir periódicamente la posición del motorizado mientras el servicio está en tránsito | Motorizado | Alta | RNF-06 | **Verificado**: `POST /api/tracking/posicion/` valida que el servicio pertenezca a una ruta del motorizado autenticado antes de guardar la posición |

### Cliente

| ID | Nombre | Descripción | Actor(es) | Prioridad | RN asociada | Criterio de verificación |
|---|---|---|---|---|---|---|
| RF-15 | Ver tracking en tiempo real | El sistema debe exponer la última posición conocida del motorizado para un servicio propio del cliente | Cliente | Alta | — | **Verificado**: `GET /api/tracking/ultima-posicion/?servicio_id=` devuelve 403 si el servicio no pertenece al cliente autenticado |
| RF-16 | Chatear con el motorizado | El sistema debe permitir un intercambio de mensajes de texto entre cliente y motorizado, limitado al servicio en curso | Cliente, Motorizado | Media | — | **Verificado**: `GET/POST /api/servicios/{id}/mensajes/` solo accesible al cliente dueño o al motorizado de la ruta asignada |
| RF-17 | Planificar recolección propia | El sistema debe permitir a un cliente crear su propia solicitud de recolección, validando leadtime y día disponible de su zona | Cliente | Alta | RN-03 | **Verificado**: `POST /api/servicios/planificar/` rechaza (400) una fecha que no respeta el leadtime o cuyo día de semana no está habilitado en la cobertura de la zona |
| RF-18 | Usar chatbot guiado | El sistema debe ofrecer al cliente un flujo de opciones (comprar producto / solicitar recolección) basado en el catálogo e inventario parametrizado | Cliente | Media | RN-04 | El flujo de UI reutiliza `productos/disponibles-chatbot/` y `servicios/planificar/` — ver decisión de diseño en [03-arquitectura.md](03-arquitectura.md) |

### V2 — Autenticación, tiempo real e innovación

| ID | Nombre | Descripción | Actor(es) | Prioridad | RN asociada | Criterio de verificación |
|---|---|---|---|---|---|---|
| RF-19 | Login con correo | El sistema debe permitir iniciar sesión indicando el correo registrado en vez del username | Todos | Alta | — | **Verificado**: `POST /api/auth/login/` con `username=<email>` resuelve internamente al usuario real antes de validar la contraseña |
| RF-20 | Restablecer contraseña por correo | El sistema debe permitir solicitar un enlace de un solo uso por correo para elegir una nueva contraseña | Todos | Alta | RNF-09 | **Verificado**: `POST /api/auth/password-reset/` envía el enlace (modo consola en dev); `POST /api/auth/password-reset/confirm/` con un token ya usado o inválido devuelve 400; nunca revela si el correo existe |
| RF-21 | Sugerir orden de ruta | El sistema debe sugerir un orden de visita para los servicios de una ruta, geocodificando direcciones reales y aplicando una heurística de vecino más cercano | Alistador | Media | — | **Verificado**: `POST /api/optimizacion/rutas/{id}/` devuelve el orden sugerido, la distancia estimada y las direcciones que no se pudieron geocodificar; probado con direcciones reales de Bogotá vía Nominatim |
| RF-22 | Chatbot en lenguaje libre | El cliente debe poder escribir en texto libre (no solo botones) y el sistema reconoce la intención (comprar / recolección) | Cliente | Media | RN-04, RN-03 | **Verificado**: `POST /api/chatbot/mensaje/` sostiene una conversación de varios turnos (elegir producto, dar zona/dirección, dar fecha) reutilizando la misma validación de leadtime que el endpoint REST |
| RF-23 | Pago al comprar por chatbot | Al completar una compra por el chatbot, el sistema debe generar un pago y devolver su estado | Cliente | Media | RNF-13 | **Verificado**: la compra por chatbot crea un `Pago` (proveedor simulado) y responde con `estado` APROBADO o RECHAZADO en la misma respuesta |
| RF-24 | Generar API keys | El administrador debe poder emitir API keys para que sistemas externos creen servicios sin login humano | Administrador | Media | RN-08 | **Verificado**: `POST /api/integraciones/api-keys/` devuelve la clave en texto plano solo en la respuesta de creación; nunca se puede recuperar después |
| RF-25 | Configurar webhooks | El administrador debe poder registrar endpoints externos que reciban eventos de cambio de estado de un servicio | Administrador | Media | RN-07, RNF-11 | **Verificado**: al asignar/cerrar/registrar novedad de un servicio se dispara `disparar_webhook()`, firmado con HMAC, y se registra un `WebhookDelivery`; probado con un receptor HTTP local real |
| RF-26 | Multi-producto por servicio | El alistador debe poder asociar varias líneas de producto (con cantidad) a un mismo servicio | Alistador | Baja | RN-06 | **Verificado**: `PUT /api/servicios/{id}/productos/` reemplaza la lista completa de líneas de forma idempotente |
| RF-27 | Tiempo real (tracking y chat) | El tracking GPS y el chat deben actualizarse en vivo sin recargar ni hacer polling activo | Cliente, Motorizado | Alta | RNF-10 | **Verificado**: conexión WebSocket a `ws/tracking/{id}/` y `ws/chat/{id}/`; probado en el navegador real: un mensaje/posición enviado por un lado llega al otro en menos de un segundo |

---

## Requerimientos no funcionales (RNF)

| ID | Categoría | Descripción | Métrica / umbral | Prioridad | Criterio de verificación |
|---|---|---|---|---|---|
| RNF-01 | Seguridad | Autenticación basada en JWT con expiración y renovación | Access token 8h, refresh token 1 día (`SIMPLE_JWT`) | Alta | **Verificado**: `POST /api/auth/login/` devuelve `access`+`refresh`; `POST /api/auth/refresh/` renueva el access token |
| RNF-02 | Seguridad | Autorización por rol (RBAC) en cada endpoint | Un rol no puede invocar acciones de otro rol | Alta | **Verificado**: acciones de motorizado (`cerrar`, `novedad`, etc.) devuelven 403 si el usuario autenticado no tiene rol MOTORIZADO o no es el motorizado asignado a esa ruta |
| RNF-03 | Mantenibilidad | La API debe estar documentada para soportar integraciones externas | Documentación OpenAPI accesible | Media | **Verificado**: `GET /api/schema/` y `GET /api/docs/` (Swagger) sirven la especificación completa vía `drf-spectacular` |
| RNF-04 | Auditoría | El sistema debe registrar quién y cuándo se generó cada novedad de un servicio | Cada novedad queda con `creado_en` y asociada al `servicio` | Media | **Verificado**: cada llamada a `/novedad/` crea un registro `Novedad` con timestamp, visible en el historial del servicio |
| RNF-05 | Usabilidad | El frontend debe ser usable desde un navegador móvil | Layout funcional en viewport de celular (Ionic) | Alta | **Verificado**: probado en viewport de celular (390px) en las 4 áreas; ver rediseño visual en [17-manual-herramientas.md](17-manual-herramientas.md) |
| RNF-06 | Rendimiento | El envío de posición GPS no debe exceder una petición cada 5-10 segundos | Intervalo de polling configurado en frontend | Media | Implementado como polling controlado por `setInterval`/`watchPosition` en el cliente (no push continuo) |
| RNF-07 | Seguridad | Las contraseñas deben almacenarse con hash, nunca en texto plano | Uso de `set_password()` / hasher de Django (PBKDF2 por defecto) | Alta | **Verificado**: `Usuario.set_password()` usado en `seed_data` y en `UsuarioSerializer.create/update`; nunca se guarda `password` plano en el modelo |
| RNF-08 | Mantenibilidad / escalabilidad | El backend debe estar modularizado por dominio para facilitar evolución a microservicios | 9 apps Django independientes (accounts, coverage, inventory, services, tracking, optimization, chatbot, payments, integrations) | Media | **Verificado**: cada dominio tiene sus propios `models.py`/`serializers.py`/`views.py`/`urls.py` sin imports cruzados salvo relaciones de datos explícitas |
| RNF-09 | Seguridad | El token de restablecimiento de contraseña debe ser de un solo uso y expirar | Token de Django (`PasswordResetTokenGenerator`) | Alta | **Verificado**: reusar un token tras cambiar la contraseña, o alterarlo, devuelve 400 |
| RNF-10 | Resiliencia | El tracking/chat deben degradar a polling si el WebSocket falla | Reconexión o fallback automático en el frontend | Media | **Verificado**: `tracking.page.ts`/`chat.page.ts` activan un intervalo de respaldo si el socket emite error o se cierra de forma anómala |
| RNF-11 | Seguridad | Los webhooks deben ir firmados y no deben afectar la respuesta real ante un fallo | Firma HMAC-SHA256 por payload; entrega best-effort | Alta | **Verificado**: `disparar_webhook()` nunca lanza excepción (probado con un endpoint inalcanzable); se registra el fallo en `WebhookDelivery` |
| RNF-12 | Seguridad | Las API keys deben almacenarse solo como hash | SHA-256 del key; el valor crudo no se persiste | Alta | **Verificado**: `ApiKey.key_hash`; un `GET` de la lista nunca incluye la clave cruda |
| RNF-13 | Mantenibilidad | Los módulos con dependencias externas no disponibles deben ser intercambiables | `MockLLMClient` / `MockPaymentProvider` detrás de una interfaz | Media | **Verificado**: `chatbot/llm.py` y `payments/provider.py` documentan el punto exacto de reemplazo por una integración real |

## Reglas de negocio (RN) — referencia rápida
| ID | Regla | Consecuencia si se viola |
|---|---|---|
| RN-01 | Un servicio de Entrega siempre inicia en el centro de mensajería | `iniciar-transito` rechaza (400) si el estado no es `RECIBIDO_CENTRO` o `NOVEDAD` |
| RN-02 | Una Recolección requiere foto + firma para cerrarse | `cerrar` rechaza (400) sin ambos archivos cuando `tipo=RECOLECCION` |
| RN-03 | La fecha de agenda debe respetar el leadtime de la zona | `planificar` y la asignación de agenda rechazan fechas fuera de rango |
| RN-04 | Un producto solo aparece en el chatbot si `disponible_chatbot=true` y `stock>0` | Filtrado automático en `productos/disponibles-chatbot/` |
| RN-05 | Toda novedad debe resultar en `DEVOLVER_A_CENTRO` o `REINTENTAR` | El serializer de novedad exige el campo `accion` con esos dos únicos valores posibles |
| RN-06 | Un producto con líneas de servicio asociadas no puede eliminarse del catálogo | `on_delete=PROTECT` en `ServicioProducto.producto` |
| RN-07 | Un webhook solo se dispara para los eventos a los que está suscrito | `WebhookEndpoint.suscrito_a(evento)` filtra antes de enviar |
| RN-08 | Un API key siempre actúa en nombre de un usuario ALISTADOR existente | `ApiKey.actua_como` limitado a `rol=ALISTADOR`; nunca autentica sin usuario asociado |
