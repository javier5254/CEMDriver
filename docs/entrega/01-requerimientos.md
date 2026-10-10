# Entrega — Fase 1: Documento de Requerimientos del sistema CMEDriver

> **Versión del sistema documentada:** v2 (código en `backend/` y `frontend/`), con el alcance ajustado el 2026-10-09 (ver [§2.4](#24-cambios-de-alcance)).
> **Fuentes:** [01-project-charter.md](../01-project-charter.md), [02-requisitos.md](../02-requisitos.md), [13-rf-rnf-completos.md](../13-rf-rnf-completos.md), [10-diagrama-casos-uso.md](../10-diagrama-casos-uso.md), [16-plan-pruebas.md](../16-plan-pruebas.md), y verificación directa contra `backend/*/models.py`, `views.py`, `serializers.py`, `permissions.py` y `tests.py`.
>
> **Convención de IDs (estables):** `RF-xx` requerimiento funcional, `RNF-xx` no funcional, `RN-xx` regla de negocio, `RES-xx` restricción. Los IDs `RF-01`…`RF-27`, `RNF-01`…`RNF-13` y `RN-01`…`RN-08` se **conservan** de [13-rf-rnf-completos.md](../13-rf-rnf-completos.md); los nuevos se agregan al final de cada serie y no se renumeran. Los IDs que se retiraron del alcance el 2026-10-09 (§2.4) **permanecen en su lugar**, marcados «Retirado del alcance», y no se reutilizan. Estos IDs son los que referencian el BPMN, el C4, el MER y la matriz de trazabilidad.
>
> **Convención de referencias a pruebas:** `T-XXX-nn` es un caso del [plan de pruebas](../16-plan-pruebas.md); `app/tests.py::Clase.metodo` es la prueba automatizada concreta en `backend/`. `T-UI-nn` son pruebas manuales: T-UI-01 login visual, T-UI-02 foto, T-UI-03 firma, T-UI-04 GPS real, T-UI-05 responsive.
>
> **Fuentes históricas:** los documentos de `docs/` citados arriba se redactaron antes del cambio de alcance del 2026-10-09 y todavía pueden describir inventario, pagos y chatbot (y los casos `T-INV-*`, `T-BOT-*`, `T-PAG-*` y `T-SRV-17…19` del plan de pruebas). En caso de discrepancia prevalece este documento.

---

## 1. Problema o necesidad identificada

> La problemática, la pregunta y los objetivos de esta sección son los mismos del paper del proyecto (`paper/secciones/03-introduccion.md`, §3.1 a §3.3), para que la documentación técnica y el documento académico describan el mismo sistema.

### 1.1 Contexto

El crecimiento del comercio electrónico ha trasladado buena parte de la presión logística a la **última milla**, el último tramo de la cadena de distribución. Ese crecimiento, acelerado por la pandemia, trajo retos críticos en la entrega final (Mohammad et al., 2023). Los proveedores de ese tramo enfrentan escasez de mano de obra, alza del combustible y márgenes reducidos (Janinhoff et al., 2024).

En Colombia el fenómeno es medible:

- **Comercio electrónico.** La Cámara Colombiana de Comercio Electrónico registró 684,6 millones de transacciones en 2025, 19,9 % más que en 2024, con ventas en línea de 145,4 billones de pesos (CCCE, 2025).
- **Mensajería expresa.** En el cuarto trimestre de 2025 hubo 86,2 millones de envíos de mensajería expresa, con ingresos de 785.786 millones de pesos, 12 % más que un año antes (MinTIC, 2026).
- **Costo logístico.** En la Encuesta Nacional Logística 2022 el costo logístico fue el 17,9 % de las ventas. En pequeñas empresas llegó al 24,3 % y en microempresas al 21,9 %, frente al 12,1 % en las grandes. Entre las barreras se reportaron el costo del transporte y la complejidad de la distribución urbana (DNP, 2023).
- **Digitalización parcial.** En la edición 2024 de la encuesta, solo el 23,4 % de las empresas usaba rastreo y seguimiento de pedidos (DNP, 2025).

El problema no es solo técnico. En Bogotá, la congestión y la fragmentación logística exigen decisiones apoyadas en datos (Gutierrez-Franco et al., 2021). En Medellín, la tercerización de la última milla traslada riesgos a trabajadores informales con escasa supervisión (Restrepo-Betancur et al., 2026). En la relación con el cliente, las entregas fallidas por ausencia del destinatario son un problema crítico de la última milla B2C (Seghezzi y Mangiaracina, 2023). No existe, en las fuentes revisadas, una cifra verificada de entregas fallidas en Colombia, así que su magnitud local se trata como un supuesto por validar. Para las mensajerías urbanas pequeñas se proponen el rastreo en tiempo real, las notificaciones y la geolocalización. Su adopción enfrenta barreras de infraestructura, costo, habilidades y resistencia al cambio (Boom-Cárcamo et al., 2024).

**Organización de aplicación:** Logytech Mobile, empresa multinacional de logística, en Colombia, durante el segundo semestre de 2026. En esta etapa el prototipo se construye y se modela. Su validación con la operación real se plantea para el Trabajo de Grado, y **no se afirman datos ni métricas de esa operación**.

### 1.2 Planteamiento del problema

El problema es la **ausencia de una plataforma que integre en un solo sistema la operación logística, la trazabilidad y la autogestión del cliente**, y que sea accesible para un operador de mensajería.

A partir de las fuentes y del análisis del dominio se plantea una hipótesis a validar. Los centros de mensajería operan con procesos manuales o con herramientas desconectadas entre sí, lo que se manifiesta en los problemas operativos P1 a P6 de la tabla siguiente. Cada uno se atiende con requerimientos concretos de este documento.

| # | Problema operativo (hipótesis a validar) | Cómo lo atiende CMEDriver |
|---|---|---|
| P1 | **Asignación informal de la operación.** Rutas y servicios se reparten por teléfono o mensajería instantánea, sin un registro único del estado de cada servicio. | Ciclo de vida del servicio con estados, rutas y asignación (RF-05, RF-07, RF-09, RF-10, RF-12) |
| P2 | **Cliente sin visibilidad.** El cliente no sabe dónde está su pedido ni cuándo llegará. | Tracking GPS, destino/ETA y chat en tiempo real (RF-15, RF-16, RF-27, RF-28) |
| P3 | **Sin evidencia digital.** Las recolecciones no dejan una prueba verificable (foto y firma). | Evidencia obligatoria al recolectar (RF-11, RN-02) |
| P4 | **Novedades sin trazabilidad.** Cuando una entrega falla no queda registro de la causa ni de la decisión tomada. | Registro de novedades con acción (RF-13, RN-05) |
| P5 | **Sin autoservicio de agendamiento.** El cliente no puede agendar una recolección sin llamar, y no hay reglas automáticas de cobertura (*leadtime* y días hábiles). | Planificación de recolección por el cliente y matriz de cobertura (RF-02, RF-17) |
| P6 | **Sin integración con terceros.** Un e-commerce o ERP no puede crear servicios ni enterarse de los cambios de estado. | API Key, webhooks firmados y API documentada (RF-06, RF-24, RF-25, RF-29) |

### 1.3 Pregunta de investigación

> ¿Cómo puede una plataforma orientada a API integrar la gestión de servicios de mensajería (entregas y recolecciones), la trazabilidad en tiempo real, la evidencia digital de entrega y la comunicación directa entre cliente y mensajero en las operaciones de Logytech Mobile en Colombia durante el segundo semestre de 2026?

**Necesidad:** una plataforma web y móvil, orientada a API, que centralice la creación, asignación, ejecución y seguimiento de servicios de mensajería, con evidencia digital, seguimiento en tiempo real, chat directo entre el cliente y el mensajero, agendamiento de recolecciones por el propio cliente y una API abierta a integraciones.

### 1.4 Referencias de esta sección

- Boom-Cárcamo, E., Molina-Romero, S., Galindo-Angulo, C., & del Mar Restrepo, M. (2024). Barriers and strategies for digital marketing and smart delivery in urban courier companies in developing countries. *Journal of the Knowledge Economy, 15*(4), 19203–19232. https://doi.org/10.1007/s13132-024-01823-1
- Cámara Colombiana de Comercio Electrónico. (2025). *Informe de cierre del comercio electrónico en Colombia – 2025*. https://ccce.org.co/wp-content/uploads/2017/06/V2-1-PUBLICO-INFORME-DE-CIERRE-2025.pdf
- Departamento Nacional de Planeación. (2023, 16 de noviembre). *El DNP reveló que el costo logístico nacional se ubicó en 17,9%, 5 p.p. por encima de la meta de 12,9%* [Comunicado de prensa]. https://www.dnp.gov.co/Prensa_/Noticias/Paginas/el-dnp-revelo-que-el-costo-logistico-nacional-se-ubico-en-17-9-5-p-p-por-encima-de-la-meta-de-12-9.aspx
- Departamento Nacional de Planeación. (2025, 19 de noviembre). *La logística del país avanza impulsada por las regiones: Menores costos y la logística verde se destacan en la ENL 2024 (Encuesta Nacional Logística)* [Comunicado de prensa]. https://dnp.gov.co/Prensa_/Noticias/Paginas/La-logistica-del-pais-avanza-impulsada-por-regiones-menores-costos-encuesta-nacional-logistica.aspx
- Gutierrez-Franco, E., Mejia-Argueta, C., & Rabelo, L. (2021). Data-driven methodology to support long-lasting logistics and decision making for urban last-mile operations. *Sustainability, 13*(11), Article 6230. https://doi.org/10.3390/su13116230
- Janinhoff, L., Klein, R., Sailer, D., & Schoppa, J. M. (2024). Out-of-home delivery in last-mile logistics: A review. *Computers & Operations Research, 168*, Article 106686. https://doi.org/10.1016/j.cor.2024.106686
- Ministerio de Tecnologías de la Información y las Comunicaciones. (2026). *Boletín trimestral del sector postal: Cuarto trimestre de 2025*. Colombia TIC. https://colombiatic.mintic.gov.co/679/articles-428453_presentacion_cifras.pdf
- Mohammad, W. A. M., Nazih Diab, Y., Elomri, A., & Triki, C. (2023). Innovative solutions in last mile delivery: Concepts, practices, challenges, and future directions. *Supply Chain Forum: An International Journal, 24*(2), 151–169. https://doi.org/10.1080/16258312.2023.2173488
- Restrepo-Betancur, B., Sanchez-Diaz, I., & Gonzalez-Calderon, C. A. (2026). How e-commerce influences last-mile practices that foster informality. *Transportation Research Interdisciplinary Perspectives, 39*, Article 102181. https://doi.org/10.1016/j.trip.2026.102181
- Seghezzi, A., & Mangiaracina, R. (2023). Smart home devices and B2C e-commerce: A way to reduce failed deliveries. *Industrial Management & Data Systems, 123*(5), 1624–1645. https://doi.org/10.1108/imds-10-2022-0651

---

## 2. Objetivos

### 2.1 Objetivo general
Diseñar y desarrollar un prototipo funcional temprano de una plataforma orientada a API que integre la gestión de servicios de mensajería (entregas y recolecciones), la trazabilidad en tiempo real, la evidencia digital de entrega y el chat directo entre el cliente y el mensajero en las operaciones de Logytech Mobile en Colombia durante el segundo semestre de 2026.

### 2.2 Objetivos específicos
| # | Objetivo específico | Producto verificable | Dónde se evidencia en esta entrega |
|---|---|---|---|
| OE-1 | Identificar, a partir de la literatura y del análisis del dominio, los problemas de coordinación, trazabilidad y atención al cliente en los servicios de mensajería de última milla, y derivar de ellos un conjunto priorizado de requerimientos funcionales y no funcionales. | Problemas P1–P6 y requerimientos priorizados | Este documento: §1, §4 (RF con prioridad), §5 (RNF), §6 (RN), §7 (RES) |
| OE-2 | Diseñar y documentar una arquitectura modular orientada a API (REST, comunicación en tiempo real y webhooks) que soporte los roles de administración, alistamiento, mensajería en campo y cliente, y modelarla mediante casos de uso, diagramas de clases, modelo entidad-relación, modelo C4 y mockups. | Modelo arquitectónico documentado | [02-stack](02-stack-tecnologico.md), [03-arquitectura](03-arquitectura.md), [04-MER](04-mer.md), [05-BPMN](05-bpmn.md), [06-C4](06-c4.md); casos de uso, clases y mockups en [docs/10](../10-diagrama-casos-uso.md), [docs/08](../08-diagrama-clases.md) y [docs/12](../12-mockups.md) |
| OE-3 | Implementar un prototipo funcional temprano que cubra los flujos centrales: ciclo de vida del servicio, seguimiento GPS en tiempo real, chat cliente-motorizado y evidencia digital de recolección. | Prototipo con esos flujos y pruebas automatizadas | Código en `backend/` y `frontend/`, 72 pruebas automatizadas; desglose en las metas funcionales MF-1…MF-7 (§2.3; MF-5 retirada) y [07-trazabilidad](07-trazabilidad.md) |
| OE-4 | Formular un protocolo de validación para Trabajo de Grado que especifique los criterios de evaluación, los instrumentos y los usuarios participantes. | Protocolo escrito | Se formula en el paper del proyecto (metodología). Su ejecución con la operación de Logytech Mobile corresponde al Trabajo de Grado y está fuera del alcance de esta entrega. |

### 2.3 Metas funcionales del prototipo (desglose del OE-3)
Para que cada requerimiento funcional tenga un objetivo verificable, el OE-3 se desglosa en siete metas funcionales (MF-5 se retiró el 2026-10-09; ver §2.4). La matriz de trazabilidad ([07](07-trazabilidad.md)) usa estos IDs.

| # | Meta funcional | RF relacionados |
|---|---|---|
| MF-1 | Permitir al Administrador gestionar usuarios por rol, consultar el panel de servicios y configurar la matriz de cobertura (zona, leadtime, días y horario). | RF-01, RF-02, RF-03 |
| MF-2 | Permitir al Alistador crear servicios (manualmente o vía API Key), crear rutas, asignar servicios a rutas/motorizados y obtener una sugerencia de orden de visita. | RF-05, RF-06, RF-07, RF-08, RF-21 |
| MF-3 | Permitir al Motorizado ejecutar el servicio con un flujo diferenciado por tipo (recibir en centro / recolectar con foto y firma), registrar novedades y reportar su posición GPS. | RF-09 a RF-14 |
| MF-4 | Dar al Cliente seguimiento en tiempo real (mapa, destino y ETA), chat con el motorizado y planificación de sus propias recolecciones respetando la cobertura. | RF-15, RF-16, RF-17, RF-27, RF-28 |
| MF-5 | ~~Ofrecer un chatbot conversacional conectado a inventario, cobertura y pagos (modelo de lenguaje y pasarela **simulados**).~~ **Retirada del alcance (2026-10-09).** Motivo: decisión del autor de centrar el prototipo en el ciclo operativo de mensajería (§2.4). | RF-18, RF-22, RF-23 (retirados) |
| MF-6 | Exponer una API documentada (OpenAPI) con autenticación por API Key y notificaciones salientes por webhooks firmados. | RF-24, RF-25, RF-29, RNF-03 |
| MF-7 | Garantizar seguridad básica (JWT, RBAC, hash de contraseñas y llaves) y verificar el sistema con una suite de pruebas automatizadas. | RF-19, RF-20, RNF-01, RNF-02, RNF-07, RNF-12, RNF-17 |

### 2.4 Cambios de alcance

**Fecha:** 2026-10-09. **Decisión del autor:** retirar del prototipo el inventario, los pagos y el chatbot para centrarlo en el ciclo operativo de mensajería (servicios, rutas, seguimiento GPS, evidencia digital, cobertura e integraciones). El chat queda únicamente como canal de comunicación entre el cliente y el motorizado, y el código lo hace cumplir (ver «Chat restringido» más abajo). Los IDs retirados **no se renumeran**: permanecen en su lugar, marcados «Retirado del alcance» con su motivo.

| Elemento retirado | Qué se eliminó del código | IDs retirados | IDs ajustados que siguen vigentes |
|---|---|---|---|
| Inventario | App `inventory` (`Producto`, stock, `/api/productos/`). | RF-04, RN-04 | RF-05, RNF-02, RNF-08, H-08, H-09 |
| Varios productos por servicio | Campo `Servicio.producto`, modelo `ServicioProducto` y `PUT /api/servicios/{id}/productos/`. | RF-26, RN-06 | RF-05, MF-2 |
| Pagos | App `payments` (`Pago`, proveedor simulado, `/api/pagos/`). | RF-23, RN-16, RES-07 | RN-14, RNF-02, RNF-20, RES-11, RES-15 |
| Chatbot y modelo de lenguaje simulado | App `chatbot` (`Conversacion`, `MensajeBot`, `/api/chatbot/`, LLM simulado) y su pantalla del frontend. | RF-18, RF-22, RNF-13, RES-06, MF-5 | RF-16, RF-27, RN-03, RNF-15, RNF-20, H-04, P5 |

- **Hallazgos resueltos por reducción de alcance:** H-03 y H-12 (el defecto desapareció con la funcionalidad; no hubo corrección de código). H-09 se conserva solo en lo relativo a `recibir-en-centro` e `iniciar-transito`, que no disparan webhook.
- **Actores externos retirados:** Proveedor de pagos y Modelo de lenguaje (LLM), ambos simulados (§3.2).
- **Se mantiene:** el chat cliente↔motorizado por servicio (RF-16, con `GET/POST /api/servicios/{id}/mensajes/` y el WebSocket `ChatConsumer`), la planificación de recolección del cliente (RF-17), el tracking y el chat en tiempo real (RF-27), la cobertura, el tracking GPS, la optimización de ruta, las integraciones (API Key y webhooks) y accounts/RBAC.
- **Chat restringido (cambio de código, 2026-10-09):** el acceso al chat se limitó a los dos participantes. `ServicioViewSet.mensajes` (REST) y `ChatConsumer` (WebSocket) solo admiten al **cliente dueño** del servicio y al **motorizado asignado**: ADMIN y ALISTADOR reciben 403 por REST y no pueden conectarse al WebSocket (cierre 4403); un cliente ajeno o un motorizado no asignado reciben 404 por REST (el servicio no está en su *queryset*). Antes el código también dejaba leer y escribir a ADMIN y ALISTADOR, lo que contradecía a RF-16. Lo verifican `MensajesChatTests.test_admin_y_alistador_no_pueden_leer_ni_escribir_en_el_chat`, `MensajesChatTests.test_motorizado_no_asignado_no_puede_acceder_al_chat` y `ChatWebSocketTests.test_admin_y_alistador_no_pueden_conectarse_al_chat`.
- **Cifras tras el cambio (verificadas contra el código):** 6 apps Django (`accounts`, `coverage`, `services`, `tracking`, `optimization`, `integrations`), 12 entidades persistentes y 72 pruebas automatizadas del backend, todas en verde. Antes eran 9 apps y 96 pruebas: se retiraron 27 pruebas de lo eliminado (quedaron 69) y se añadieron 3 pruebas del chat restringido (72).
- **Reincorporación:** inventario, pagos y asistente conversacional quedan como mejora futura opcional ([08-limitaciones-y-mejoras.md](08-limitaciones-y-mejoras.md), §8.4).

---

## 3. Actores y tipos de usuario

### 3.1 Actores humanos (roles del sistema)
El rol se almacena en `Usuario.rol` (`backend/accounts/models.py`, enumeración `Rol`: `ADMIN`, `ALISTADOR`, `MOTORIZADO`, `CLIENTE`). Los permisos se aplican con las clases `IsAdmin`, `IsAlistador`, `IsMotorizado`, `IsCliente` de `backend/accounts/permissions.py` y con filtros de `get_queryset()` en cada vista.

| Actor | Descripción | Permisos (verificados en código) | Área del frontend |
|---|---|---|---|
| **Administrador** (`ADMIN`) | Responsable de la configuración y supervisión de la operación del centro de mensajería. | CRUD de usuarios (`/api/usuarios/`, solo ADMIN); escritura de cobertura (`/api/cobertura/`); gestión de API Keys, webhooks y su bitácora (`/api/integraciones/…`); optimizar rutas; ver **todos** los servicios. **No participa en el chat**: recibe 403 por REST y no puede conectarse al WebSocket del chat. | `/admin`: Dashboard, Usuarios, Cobertura, API Keys, Webhooks |
| **Alistador** (`ALISTADOR`) | Operador del centro que prepara y organiza los servicios del día. | Crear servicios (`POST /api/servicios/`); crear/editar rutas (`/api/rutas/`); asignar servicio a ruta; optimizar rutas; ver todos los servicios. **No participa en el chat**: recibe 403 por REST y no puede conectarse al WebSocket del chat. | `/alistador`: Servicios, Nuevo servicio, Nueva ruta, Optimizar ruta |
| **Motorizado** (`MOTORIZADO`) | Mensajero en campo que ejecuta entregas y recolecciones. | Ver **solo** los servicios de sus rutas; recibir en centro, iniciar tránsito, cerrar y registrar novedad **solo** sobre servicios de su ruta; reportar posición GPS; chatear con el cliente de un servicio de su ruta. | `/motorizado`: Mis servicios, detalle con GPS, cámara y firma, chat |
| **Cliente** (`CLIENTE`) | Destinatario/remitente final de los servicios. | Ver **solo** sus servicios; ver tracking y destino de sus servicios; chatear con el motorizado asignado; planificar recolecciones. | `/cliente`: Mis servicios, Tracking, Chat, Planificar recolección |

Todos los roles comparten: iniciar sesión con usuario o correo, renovar el token, consultar su perfil (`/api/auth/me/`) y restablecer la contraseña por correo.

### 3.2 Actores externos (sistemas)
| Actor externo | Tipo | Descripción | Interacción / permisos | Estado real |
|---|---|---|---|---|
| **Sistema integrador** (e-commerce, ERP) | Secundario, iniciador | Crea y consulta servicios sin login humano. | Envía el header `X-API-Key`; `ApiKeyAuthentication` (`backend/integrations/authentication.py`) lo autentica **como el usuario ALISTADOR** configurado en `ApiKey.actua_como`, por lo que hereda exactamente los permisos del Alistador. | **Real** |
| **Receptor de webhooks** (sistema del tercero) | Secundario, receptor | Recibe por HTTP POST los eventos `servicio.creado`, `servicio.asignado`, `servicio.entregado`, `servicio.recolectado`, `servicio.novedad`, `servicio.devuelto`. | Cada POST lleva el header `X-CMEDriver-Signature` (HMAC-SHA256). Implementado en `backend/integrations/services.py`. | **Real** |
| **Nominatim (OpenStreetMap)** | Servicio externo | Geocodifica direcciones a coordenadas (lat, lng) para optimizar rutas y ubicar el destino en el mapa. | `https://nominatim.openstreetmap.org/search` vía `urllib` (`backend/optimization/geocoding.py`), con User-Agent propio y espera de 1,1 s entre llamadas; resultados cacheados en `PuntoGeocodificado`. | **Real** |
| **Servidor de teselas OSM** | Servicio externo | Provee el mapa base en el tracking (Leaflet). | `https://{s}.tile.openstreetmap.org/...` desde `frontend/src/app/features/cliente/tracking.page.ts`. | **Real** |
| **Servidor de correo** | Servicio externo | Envía el enlace de restablecimiento de contraseña. | `send_mail()` en `backend/accounts/views.py`. En desarrollo el backend es de **consola** (el correo se imprime en el log); un SMTP real se configura por variable de entorno `EMAIL_BACKEND`. | **Configurable** (consola en dev) |

*Los actores externos «Proveedor de pagos» y «Modelo de lenguaje (LLM)» (ambos simulados) se retiraron el 2026-10-09 junto con los pagos y el chatbot (§2.4).*

---

## 4. Requerimientos funcionales (RF)

Prioridad: **Alta** = imprescindible para el flujo operativo; **Media** = valor agregado importante; **Baja** = mejora opcional.
Estado: ✅ implementado y probado; ⚠️ implementado parcialmente (ver nota); 🖐 verificado solo manualmente.

### 4.1 Administrador

| ID | Título | Actor | Descripción ("El sistema debe…") | Prior. | Criterio de aceptación verificable | Verificación |
|---|---|---|---|---|---|---|
| RF-01 | Gestionar usuarios | Administrador | El sistema debe permitir al Administrador crear, consultar, editar y desactivar usuarios, asignando uno de los 4 roles (ADMIN, ALISTADOR, MOTORIZADO, CLIENTE) y un correo único. | Alta | (a) `GET/POST/PATCH /api/usuarios/` con token ADMIN responde 200/201; (b) con token de cualquier otro rol responde 403; (c) sin token responde 401; (d) `PATCH {is_active:false}` impide el login posterior; (e) la contraseña nunca aparece en la respuesta. | T-ACC-04, T-ACC-05, T-ACC-06 → `accounts/tests.py::UsuariosRBACTests` ⚠️ ver nota 1 |
| RF-02 | Configurar matriz de cobertura | Administrador | El sistema debe permitir definir, por zona, el leadtime en días, los días de la semana habilitados y el horario de atención, y calcular a partir de ello las fechas de agenda disponibles. | Alta | (a) Solo ADMIN puede crear/editar (`/api/cobertura/`), otro rol → 403; (b) cualquier autenticado puede leer; (c) `GET /api/cobertura/agenda-disponible/?zona=X` devuelve solo fechas ≥ hoy + leadtime, en días habilitados y dentro de 21 días; (d) zona inexistente → 404. | T-COV-01…T-COV-04 → `coverage/tests.py::CoberturaTests` ✅ |
| RF-03 | Consultar panel de servicios | Administrador | El sistema debe mostrar al Administrador un resumen de todos los servicios agrupados por estado. | Media | El dashboard de `/admin/dashboard` muestra un contador por cada estado de `EstadoServicio`, calculado sobre `GET /api/servicios/` (que para ADMIN no aplica filtro por propietario). | 🖐 Sin prueba automatizada y sin caso propio en el plan de pruebas. T-UI-01 (login visual en los 4 roles) solo verifica que el ADMIN llegue a `/admin/dashboard`, no los contadores. Verificación manual propuesta: iniciar sesión como `admin` y comparar cada contador con el conteo por `estado` de `GET /api/servicios/` |
| RF-04 | ~~Gestionar inventario~~ | — | **Retirado del alcance (2026-10-09).** Motivo: el inventario (productos y stock) se eliminó para centrar el prototipo en el ciclo operativo de mensajería (§2.4). | — | — | — |
| RF-24 | Generar API Keys | Administrador | El sistema debe permitir al Administrador emitir, activar/desactivar y eliminar API Keys asociadas a un usuario ALISTADOR, mostrando la clave en texto plano una sola vez. | Media | (a) No-ADMIN → 403; (b) la respuesta de creación incluye la clave cruda; (c) ningún `GET` posterior la incluye; (d) `actua_como` con rol distinto de ALISTADOR → 400; (e) `PATCH {activa:false}` hace que la clave sea rechazada. | T-INT-01, T-INT-02, T-INT-03 → `integrations/tests.py::ApiKeyEndpointTests`, `ApiKeyAuthenticationTests` ✅ |
| RF-25 | Configurar webhooks | Administrador | El sistema debe permitir registrar endpoints externos suscritos a eventos de servicio y enviarles un POST firmado (HMAC-SHA256) cuando ocurra un evento suscrito. | Media | (a) No-ADMIN → 403; (b) el `secret` se autogenera si se omite; (c) eventos fuera de la lista válida → 400; (d) al asignar, cerrar, registrar novedad o crear un servicio se registra un `WebhookDelivery` por endpoint activo suscrito, con firma verificable; (e) un endpoint caído no altera la respuesta de la API. | T-INT-01, T-INT-04, T-INT-05 → `integrations/tests.py::WebhookEndpointTests`, `DispararWebhookTests` ✅ |
| RF-29 | Consultar bitácora de webhooks | Administrador | El sistema debe permitir al Administrador consultar, por endpoint, el historial de intentos de entrega de webhooks (evento, código HTTP, éxito, error). | Baja | `GET /api/integraciones/webhooks/{id}/entregas/` con ADMIN → 200 con la lista; otro rol → 403. | `integrations/tests.py::WebhookEndpointTests.test_entregas_endpoint_lista_bitacora_solo_para_admin` ✅ (no tiene ID T- en el plan) |

### 4.2 Alistador y sistemas integradores

| ID | Título | Actor | Descripción ("El sistema debe…") | Prior. | Criterio de aceptación verificable | Verificación |
|---|---|---|---|---|---|---|
| RF-05 | Crear servicio manual | Alistador | El sistema debe permitir al Alistador crear un servicio de tipo ENTREGA o RECOLECCION indicando cliente, zona, fecha de agenda y la dirección correspondiente al tipo; el servicio nace en estado `CREADO`. | Alta | (a) No-ALISTADOR → 403; (b) ENTREGA sin `direccion_destino` → 400; (c) RECOLECCION sin `direccion_origen` → 400; (d) servicio válido → 201 con `estado=CREADO` y representación completa. | T-SRV-01…T-SRV-04 → `services/tests.py::CrearServicioTests` ✅ |
| RF-06 | Crear servicio vía API externa | Sistema integrador | El sistema debe permitir que un sistema externo cree servicios con el mismo endpoint y las mismas validaciones que el Alistador, autenticándose con el header `X-API-Key`. | Media | (a) Una API Key válida y activa autentica como su usuario `actua_como`; (b) una inexistente o inactiva → 401; (c) `POST /api/servicios/` con API Key válida aplica las validaciones de RF-05. | T-INT-03 → `integrations/tests.py::ApiKeyAuthenticationTests` ✅ (autenticación). ⚠️ No hay prueba end-to-end de `POST /api/servicios/` con API Key |
| RF-07 | Crear ruta y asignar servicio | Alistador | El sistema debe permitir crear rutas (motorizado + fecha) y asignar a ellas servicios en estado `CREADO`, pasando el servicio a `ASIGNADO`. | Alta | (a) `POST /api/rutas/` solo ALISTADOR; (b) `POST /api/servicios/{id}/asignar-ruta/` cambia `CREADO → ASIGNADO`; (c) desde cualquier otro estado → 400; (d) dispara el evento `servicio.asignado`. | T-SRV-05 → `services/tests.py::CicloDeVidaEntregaTests.test_flujo_completo_entrega` ✅ |
| RF-08 | Consultar estado e historial de novedades | Alistador | El sistema debe permitir consultar el estado actual de cada servicio junto con su historial de novedades (tipo, detalle, acción, fecha) y su evidencia. | Media | `GET /api/servicios/{id}/` incluye `estado`, `novedades[]` (con `creado_en`) y `evidencia`. | Cubierto indirectamente por T-SRV-09, T-SRV-10, T-SRV-11 ⚠️ ver nota 3 (la *reasignación* no existe) |
| RF-21 | Sugerir orden de ruta | Alistador, Administrador | El sistema debe sugerir un orden de visita para los servicios de una ruta, geocodificando sus direcciones con Nominatim y aplicando la heurística del vecino más cercano (distancia haversine), sin modificar los datos de la ruta. | Media | (a) MOTORIZADO o CLIENTE → 403; (b) ruta inexistente → 404; (c) el orden devuelto coincide con el vecino más cercano calculado a mano; (d) direcciones no geocodificables aparecen en `no_geocodificados` y la respuesta es 200; (e) una segunda llamada usa el caché y no vuelve a geocodificar. | T-OPT-01…T-OPT-04 → `optimization/tests.py::OptimizarRutaTests` ✅ |
| RF-26 | ~~Asociar varios productos a un servicio~~ | — | **Retirado del alcance (2026-10-09).** Motivo: la asociación de productos a servicios dependía del inventario, que se eliminó para centrar el prototipo en el ciclo operativo de mensajería (§2.4). | — | — | — |

### 4.3 Motorizado

| ID | Título | Actor | Descripción ("El sistema debe…") | Prior. | Criterio de aceptación verificable | Verificación |
|---|---|---|---|---|---|---|
| RF-09 | Ver servicios asignados | Motorizado | El sistema debe listar al Motorizado únicamente los servicios que pertenecen a rutas asignadas a él, diferenciando Entrega y Recolección. | Alta | `GET /api/servicios/` con MOTORIZADO devuelve solo servicios con `ruta.motorizado = usuario`; un servicio ajeno por id → 404. | T-SRV-06 → `services/tests.py::CicloDeVidaEntregaTests.test_motorizado_no_asignado_no_puede_operar_el_servicio` ✅ |
| RF-10 | Recibir en centro (Entrega) | Motorizado | El sistema debe exigir que un servicio de ENTREGA se confirme como recibido en el centro de mensajería (`ASIGNADO → RECIBIDO_CENTRO`) antes de iniciar tránsito. | Alta | (a) Solo aplica a ENTREGA: sobre RECOLECCION → 400; (b) solo desde `ASIGNADO`; (c) solo el motorizado de la ruta. | T-SRV-05, T-SRV-07 → `services/tests.py::CicloDeVidaEntregaTests` ✅ |
| RF-11 | Capturar evidencia (Recolección) | Motorizado | El sistema debe exigir una foto del producto y una firma digital del cliente para cerrar un servicio de RECOLECCION, y almacenarlas como `Evidencia` del servicio. | Alta | (a) `POST /api/servicios/{id}/cerrar/` sin `foto` o sin `firma` → 400; (b) con ambas → 200, `estado=RECOLECTADO` e `evidencia` en la respuesta; (c) en la app la foto se toma con la cámara y la firma en un canvas. | T-SRV-08, T-SRV-09 → `services/tests.py::CicloDeVidaRecoleccionTests`; T-UI-02, T-UI-03 (manual) ✅ |
| RF-12 | Iniciar tránsito y cerrar servicio | Motorizado | El sistema debe permitir marcar un servicio como `EN_TRANSITO` y luego cerrarlo como `ENTREGADO` (Entrega) o `RECOLECTADO` (Recolección), según las transiciones de RN-09. | Alta | (a) Entrega: `RECIBIDO_CENTRO → EN_TRANSITO → ENTREGADO`; (b) Recolección: `ASIGNADO → EN_TRANSITO → RECOLECTADO`; (c) cerrar desde un estado distinto de `EN_TRANSITO` → 400; (d) dispara `servicio.entregado`/`servicio.recolectado`. | T-SRV-05, T-SRV-09 ✅ |
| RF-13 | Registrar novedad | Motorizado | El sistema debe permitir registrar una novedad (tipo, detalle) con una acción obligatoria `REINTENTAR` o `DEVOLVER_A_CENTRO`, y actualizar el estado del servicio en consecuencia. | Alta | (a) `REINTENTAR` → estado `NOVEDAD`, que permite volver a `iniciar-transito`; (b) `DEVOLVER_A_CENTRO` → estado `DEVUELTO` (terminal) y `cerrar` posterior → 400; (c) sobre un servicio cerrado → 400; (d) cada novedad queda con fecha. | T-SRV-10, T-SRV-11 → `services/tests.py::NovedadTests` ✅ |
| RF-14 | Reportar posición GPS | Motorizado | El sistema debe recibir periódicamente la posición GPS del motorizado para un servicio de su ruta y difundirla en vivo a quien esté viendo el tracking. | Alta | (a) `POST /api/tracking/posicion/` del motorizado asignado → 201; (b) de un motorizado no asignado → 403; (c) la app envía como máximo una posición cada 8 s mientras el servicio está en tránsito. | T-TRK-01, T-TRK-02 → `tracking/tests.py::TrackingTests`; T-UI-04 (manual) ✅ ⚠️ ver nota 4 |

### 4.4 Cliente

| ID | Título | Actor | Descripción ("El sistema debe…") | Prior. | Criterio de aceptación verificable | Verificación |
|---|---|---|---|---|---|---|
| RF-15 | Ver tracking del motorizado | Cliente | El sistema debe mostrar al Cliente, en un mapa, la última posición conocida del motorizado de uno de sus servicios. | Alta | (a) `GET /api/tracking/ultima-posicion/?servicio_id=` del cliente dueño → 200 con la última posición reportada; (b) de otro cliente → 403; (c) sin posiciones → 404. | T-TRK-03, T-TRK-04 → `tracking/tests.py::TrackingTests` ✅ |
| RF-16 | Chatear con el motorizado | Cliente, Motorizado | El sistema debe permitir el intercambio de mensajes de texto (≤ 1000 caracteres) entre el cliente dueño y el motorizado asignado, dentro del contexto de un servicio. Es el único chat del sistema: conecta exclusivamente a esas dos personas (ni ADMIN ni ALISTADOR participan) y no existe asistente automático. | Media | (a) Cliente dueño envía (201) y lee (200) mensajes; (b) otro cliente o un motorizado no asignado → 404 (el servicio no está en su *queryset*); (c) motorizado asignado puede enviar (201); (d) ADMIN y ALISTADOR → 403 al leer y al escribir, y no pueden conectarse al WebSocket del chat. | T-SRV-12…T-SRV-14 → `services/tests.py::MensajesChatTests` (5 pruebas, cubren (a)–(d)) y `ChatWebSocketTests.test_admin_y_alistador_no_pueden_conectarse_al_chat` ✅ ⚠️ ver nota 6 |
| RF-17 | Planificar recolección propia | Cliente | El sistema debe permitir al Cliente crear su propia solicitud de RECOLECCION, validando que la zona tenga cobertura y que la fecha respete el leadtime y los días habilitados (RN-03). Es el único flujo con el que el cliente crea un servicio por sí mismo. | Alta | (a) Fecha antes de hoy + leadtime → 400; (b) día no habilitado → 400; (c) zona sin cobertura → 400; (d) fecha válida → 201 con `tipo=RECOLECCION`, `estado=CREADO` y `cliente` = usuario autenticado. | T-SRV-15, T-SRV-16 → `services/tests.py::PlanificarRecoleccionTests` ✅ ⚠️ ver nota 7 (H-13) |
| RF-18 | ~~Usar chatbot guiado con catálogo~~ | — | **Retirado del alcance (2026-10-09).** Motivo: el chatbot guiado y el catálogo para el chatbot se eliminaron para centrar el prototipo en el ciclo operativo de mensajería (§2.4). | — | — | — |
| RF-22 | ~~Chatbot en lenguaje libre~~ | — | **Retirado del alcance (2026-10-09).** Motivo: el chatbot de lenguaje libre y su modelo de lenguaje simulado se eliminaron para centrar el prototipo en el ciclo operativo de mensajería (§2.4). | — | — | — |
| RF-23 | ~~Generar pago al comprar por chatbot~~ | — | **Retirado del alcance (2026-10-09).** Motivo: los pagos y la compra por chatbot se eliminaron para centrar el prototipo en el ciclo operativo de mensajería (§2.4). | — | — | — |
| RF-27 | Tracking y chat en tiempo real | Cliente, Motorizado | El sistema debe actualizar en vivo el tracking y el chat cliente-motorizado mediante WebSockets autenticados con JWT, y degradar automáticamente a consulta periódica (polling) si el socket falla. | Alta | (a) Una posición o mensaje enviado llega a los otros conectados al mismo servicio; (b) un usuario no autorizado no logra el *handshake* (cierre 4403): al chat solo se conectan el cliente dueño y el motorizado asignado (ADMIN, ALISTADOR, otros clientes y otros motorizados quedan fuera); al tracking también pueden conectarse ADMIN y ALISTADOR (solo lectura); (c) si el socket falla, el frontend consulta cada 8 s (tracking) / 5 s (chat). | T-SRV-20, T-SRV-21, T-TRK-05, T-TRK-06 → `services/tests.py::ChatWebSocketTests` (3), `tracking/tests.py::TrackingWebSocketTests` (2) ✅ |
| RF-28 | Ver destino y ETA en el mapa | Cliente, Motorizado | El sistema debe geocodificar la dirección de destino (Entrega) u origen (Recolección) de un servicio, mostrarla en el mapa de tracking y calcular un tiempo estimado de llegada aproximado. | Baja | (a) `GET /api/tracking/destino/?servicio_id=` devuelve lat/lng y la cachea; (b) si Nominatim falla → 404, nunca 500; (c) otro cliente → 403. | `tracking/tests.py::DestinoTests` (3 pruebas, sin ID T- en el plan) ✅ |

### 4.5 Todos los usuarios

| ID | Título | Actor | Descripción ("El sistema debe…") | Prior. | Criterio de aceptación verificable | Verificación |
|---|---|---|---|---|---|---|
| RF-19 | Iniciar sesión con usuario o correo | Todos | El sistema debe autenticar al usuario con su nombre de usuario **o** su correo y contraseña, y devolver un token de acceso, uno de renovación y los datos básicos del usuario (incluido el rol). | Alta | (a) Credenciales válidas → 200 con `access`, `refresh`, `user.rol`; (b) contraseña incorrecta → 401; (c) usar el correo en lugar del usuario → 200 con el usuario correcto; (d) `GET /api/auth/me/` → 200 con el usuario actual. | T-ACC-01, T-ACC-02, T-ACC-03, T-ACC-07 → `accounts/tests.py::AuthTests` ✅ |
| RF-20 | Restablecer contraseña por correo | Todos | El sistema debe enviar, a solicitud, un enlace de un solo uso al correo registrado para definir una nueva contraseña, sin revelar si el correo existe. | Alta | (a) Correo existente → 200 y 1 correo enviado; (b) correo inexistente → 200 y 0 correos; (c) token válido → 200 y la nueva contraseña permite login; (d) token inválido o ya usado → 400. | T-ACC-08…T-ACC-11 → `accounts/tests.py::PasswordResetTests` ✅ |

**Notas de verificación (estado real frente a la documentación):**
1. **RF-01:** la desactivación por `PATCH is_active=false` funciona, pero el botón "Desactivar/eliminar" del frontend (`usuarios-list.page.ts`) envía un `DELETE` (borrado físico). Un usuario con servicios o rutas asociados está protegido por `on_delete=PROTECT`, por lo que el borrado fallaría. Además, crear un usuario sin contraseña invoca `Usuario.objects.make_random_password()`, método eliminado en Django 5.1 (el proyecto usa Django 6.1.1), lo que provocaría un error 500. Ninguno de los dos casos tiene prueba automatizada.
2. **RF-04:** *retirada del alcance (2026-10-09); la nota ya no aplica.* Se refería a que el inventario no tenía pantalla en el frontend del Administrador.
3. **RF-08:** la historia de usuario original pedía también *reasignar* el servicio. No existe esa operación: `asignar-ruta` solo funciona desde `CREADO`, por lo que un servicio en `NOVEDAD` no puede moverse a otra ruta.
4. **RF-14:** el backend no valida que el servicio esté `EN_TRANSITO` al recibir una posición; la restricción solo la aplica la app del motorizado.
5. **RF-22/RF-23:** *retiradas del alcance (2026-10-09); la nota ya no aplica.* Se refería a la compra por chatbot (no revalidaba el leadtime, no descontaba stock y no disparaba el webhook `servicio.creado`).
6. **RF-16:** el límite de 1000 caracteres solo se valida en la API REST (`MensajeChatSerializer`, `max_length=1000`). `ChatConsumer._guardar_mensaje` guarda por WebSocket sin revisar la longitud (SQLite no impone el límite de `varchar`). La app envía el chat solo por REST, así que únicamente lo alcanza un cliente WebSocket directo. No tiene prueba.
7. **RF-17:** `PlanificarRecoleccionSerializer` no exige `direccion_origen` y `ServicioViewSet.planificar` la lee con `data['direccion_origen']`: sin el campo la API responde 500 y con cadena vacía crea una recolección sin origen (H-13, RN-13). La app lo evita, porque deshabilita el envío con la dirección vacía. Además, los criterios (b) «día no habilitado» y (c) «zona sin cobertura» de RF-17 no tienen prueba automatizada (solo (a) y (d); ver 07 §g.2, ítem 5).

---

## 5. Requerimientos no funcionales (RNF)

| ID | Categoría | Requerimiento | Métrica / criterio verificable | Prior. | Evidencia / verificación |
|---|---|---|---|---|---|
| RNF-01 | Seguridad — autenticación | Autenticación basada en JWT con expiración y renovación. | Access token = 8 h, refresh token = 1 día (`SIMPLE_JWT` en `backend/cmedriver/settings.py`); `POST /api/auth/refresh/` emite un nuevo access. Toda la API exige autenticación por defecto (`DEFAULT_PERMISSION_CLASSES = IsAuthenticated`) salvo login y reset. | Alta | T-ACC-01, T-ACC-06 |
| RNF-02 | Seguridad — autorización | Control de acceso por rol (RBAC) en cada endpoint y filtrado de datos por propietario. | Ninguna acción de un rol es ejecutable por otro: 100 % de las pruebas de permisos devuelven 403/404 para el rol no autorizado. | Alta | T-ACC-05, T-COV-01, T-SRV-01, T-SRV-06, T-SRV-13, T-TRK-02, T-TRK-04, T-OPT-01, T-INT-01 ⚠️ ver hallazgo H-01 |
| RNF-03 | Mantenibilidad / interoperabilidad | API documentada para integraciones. | `GET /api/schema/` (OpenAPI 3) y `GET /api/docs/` (Swagger UI) disponibles vía `drf-spectacular`. | Media | Inspección manual |
| RNF-04 | Auditoría | Registro de cuándo se generó cada novedad, evidencia, mensaje y entrega de webhook. | `Novedad.creado_en`, `Evidencia.capturado_en`, `MensajeChat.enviado_en`, `WebhookDelivery.creado_en`, `Servicio.creado_por`. | Media | T-SRV-10, T-INT-04 ⚠️ ver hallazgo H-06 |
| RNF-05 | Usabilidad | El frontend debe ser usable desde un navegador móvil. | Las 4 áreas funcionan sin desplazamiento horizontal en un viewport de 390 px de ancho (Ionic + Angular, estilo iOS). | Alta | T-UI-05 (manual) |
| RNF-06 | Rendimiento / consumo | El envío de posición GPS no debe exceder una petición cada 5-10 s por motorizado. | Intervalo fijo de 8 000 ms en `frontend/src/app/features/motorizado/servicio-detail.page.ts`. | Media | Inspección de código; T-UI-04 |
| RNF-07 | Seguridad — credenciales | Contraseñas almacenadas solo con hash. | Uso de `set_password()` (PBKDF2 por defecto de Django) y validadores de contraseña de Django en creación y reset; el campo `password` es `write_only`. | Alta | T-ACC-10 |
| RNF-08 | Mantenibilidad / escalabilidad | Backend modular por dominio. | 6 apps Django independientes: `accounts`, `coverage`, `services`, `tracking`, `optimization`, `integrations`, cada una con sus `models/serializers/views/urls/tests`. | Media | Inspección de estructura |
| RNF-09 | Seguridad | Token de restablecimiento de contraseña de un solo uso y con expiración. | `default_token_generator` de Django: el token se invalida al cambiar la contraseña; alterado o reutilizado → 400. | Alta | T-ACC-11 |
| RNF-10 | Resiliencia | Tracking y chat degradan a polling si el WebSocket falla. | Respaldo automático a 8 s (tracking) y 5 s (chat) en `tracking.page.ts` / `chat.page.ts`. | Media | Inspección de código; prueba manual |
| RNF-11 | Seguridad / resiliencia | Webhooks firmados y entrega *best-effort*. | Firma HMAC-SHA256 en `X-CMEDriver-Signature`; timeout de 3 s; `disparar_webhook()` nunca propaga excepciones. | Alta | T-INT-04, T-INT-05 |
| RNF-12 | Seguridad | API Keys almacenadas solo como hash. | Se persiste `key_hash` (SHA-256) y un `prefix` de 8 caracteres; la clave cruda solo existe en la respuesta de creación. | Alta | T-INT-02 |
| RNF-13 | ~~Mantenibilidad / portabilidad de proveedores~~ | **Retirado del alcance (2026-10-09).** Motivo: solo se refería a los proveedores simulados `MockLLMClient` y `MockPaymentProvider`, eliminados junto con el chatbot y los pagos (§2.4). | — | — | — |
| RNF-14 | Portabilidad | El cliente debe funcionar en navegadores modernos de escritorio y móvil, y poder empaquetarse para Android. | App web Ionic/Angular; proyecto Capacitor para Android configurado (`npx cap add android` y `sync` exitosos). Build de APK **no verificado** en el entorno de desarrollo; iOS no evaluado. | Media | [11-manual-distribucion.md](../11-manual-distribucion.md) |
| RNF-15 | Disponibilidad / tolerancia a fallos | Una falla de un servicio externo (Nominatim, receptor de webhook) no debe producir errores 500. | Geocodificación fallida → dirección en `no_geocodificados` (200) o 404 controlado; webhook caído → registro con `exito=False`. | Alta | T-OPT-03, T-INT-05, `tracking/tests.py::DestinoTests.test_geocoding_fallido_devuelve_404_no_500` |
| RNF-16 | Rendimiento — tiempo real | Latencia de difusión de mensajes de chat y posiciones. | < 1 s entre emisor y receptor conectados al mismo servicio en red local (Django Channels + Daphne). | Media | T-SRV-20, T-TRK-05; prueba manual en navegador |
| RNF-17 | Calidad / mantenibilidad | El backend debe contar con una suite de pruebas automatizadas que se ejecute en un comando. | `manage.py test` (o `run_tests.ps1` / `run_tests.sh`) ejecuta 72 pruebas en BD aislada, todas en verde, en pocos segundos; cada RF de prioridad Alta tiene al menos una prueba automatizada o manual asociada. | Alta | [16-plan-pruebas.md](../16-plan-pruebas.md) |
| RNF-18 | Seguridad — configuración | Configuración sensible por variables de entorno y arranque seguro en producción. | Con `DJANGO_DEBUG=False` el sistema no arranca sin `DJANGO_SECRET_KEY`; CORS restringido a los orígenes de `CORS_ALLOWED_ORIGINS` cuando DEBUG está apagado; `ALLOWED_HOSTS` por entorno. | Alta | `backend/cmedriver/settings.py` |
| RNF-19 | Localización | Idioma y zona horaria de Colombia. | `LANGUAGE_CODE='es-co'`, `TIME_ZONE='America/Bogota'`, `USE_TZ=True`; textos de la interfaz en español. | Baja | `backend/cmedriver/settings.py` |
| RNF-20 | Privacidad | Los datos personales (dirección, ubicación, firma, foto, chat) solo deben ser visibles para el titular y los roles operativos autorizados. | Cliente ajeno → 403/404 en servicios, tracking, destino y chat; el chat tampoco es accesible a ADMIN ni a ALISTADOR (403 por REST, sin acceso al WebSocket). | Alta | T-SRV-13, T-TRK-04, `MensajesChatTests.test_admin_y_alistador_no_pueden_leer_ni_escribir_en_el_chat` ⚠️ ver hallazgos H-01 y H-07 y RES-11 |

---

## 6. Reglas de negocio (RN)

Todas verificadas contra el código. "Dónde se aplica" indica el archivo (y función/clase) que hace cumplir la regla.

| ID | Regla de negocio | Consecuencia si se viola | Dónde se aplica | Prueba |
|---|---|---|---|---|
| RN-01 | Un servicio de **Entrega** siempre inicia en el centro de mensajería: debe pasar por `RECIBIDO_CENTRO` antes de `EN_TRANSITO`. `recibir-en-centro` solo aplica a Entrega. | 400 en `recibir-en-centro` sobre Recolección o fuera de `ASIGNADO`; 400 en `iniciar-transito` desde un estado no permitido. | `backend/services/views.py` → `ServicioViewSet.recibir_en_centro`, `iniciar_transito` | T-SRV-05, T-SRV-07 (⚠️ hallazgo H-02) |
| RN-02 | Una **Recolección** requiere foto del producto **y** firma del cliente para cerrarse como `RECOLECTADO`. La Entrega no exige evidencia. | 400 "requiere foto y firma". | `backend/services/serializers.py` → `CerrarServicioSerializer.validate`; `backend/services/views.py` → `cerrar` | T-SRV-08, T-SRV-09 |
| RN-03 | La fecha de agenda solicitada por el cliente debe ser ≥ hoy + `leadtime_dias` de la zona y caer en un día de `dias_disponibles`. La agenda ofrecida abarca como máximo 21 días. | 400 al planificar; las fechas no válidas no se ofrecen. | `backend/services/views.py` → `planificar`; `backend/coverage/views.py` → `AgendaDisponibleView` (`HORIZONTE_DIAS=21`) | T-SRV-15, T-SRV-16, T-COV-03 (⚠️ hallazgo H-04) |
| RN-04 | ~~Un producto solo se ofrece por el chatbot si `disponible_chatbot = true` y `stock > 0`.~~ **Retirado del alcance (2026-10-09).** Motivo: el inventario y el chatbot se eliminaron para centrar el prototipo en el ciclo operativo de mensajería (§2.4). | — | — | — |
| RN-05 | Toda novedad debe resultar en `REINTENTAR` (estado `NOVEDAD`, reintentable) o `DEVOLVER_A_CENTRO` (estado `DEVUELTO`, terminal). | 400 si `accion` falta o no es uno de los dos valores. | `backend/services/models.py` → `Novedad.Accion`; `backend/services/views.py` → `novedad` | T-SRV-10, T-SRV-11 |
| RN-06 | ~~Un producto con líneas de servicio asociadas no puede eliminarse del catálogo.~~ **Retirado del alcance (2026-10-09).** Motivo: `ServicioProducto` y el catálogo de productos se eliminaron para centrar el prototipo en el ciclo operativo de mensajería (§2.4). | — | — | — |
| RN-07 | Un webhook solo se envía a endpoints **activos** suscritos al evento ocurrido. | No se envía ni se registra entrega. | `backend/integrations/models.py` → `WebhookEndpoint.suscrito_a`; `backend/integrations/services.py` → `disparar_webhook` | `integrations/tests.py::DispararWebhookTests.test_evento_no_suscrito_no_genera_entrega`, `test_endpoint_inactivo_no_recibe_webhooks` |
| RN-08 | Una API Key siempre actúa en nombre de un usuario **ALISTADOR** existente y debe estar activa. | 400 al crearla con otro rol; 401 al usarla si es inválida o inactiva. | `backend/integrations/serializers.py` → `ApiKeyCreateSerializer.validate_actua_como`; `backend/integrations/authentication.py` | `integrations/tests.py::ApiKeyEndpointTests.test_actua_como_debe_ser_alistador`, T-INT-03 |
| RN-09 | **Ciclo de vida del servicio.** Solo se permiten estas transiciones: `CREADO→ASIGNADO` (asignar ruta); Entrega: `ASIGNADO→RECIBIDO_CENTRO→EN_TRANSITO→ENTREGADO`; Recolección: `ASIGNADO→EN_TRANSITO→RECOLECTADO`; desde cualquier estado no terminal posterior a la asignación: `→NOVEDAD` (reintentar) o `→DEVUELTO` (devolver); `NOVEDAD→EN_TRANSITO`. `ENTREGADO`, `RECOLECTADO` y `DEVUELTO` son **terminales**. El estado no es editable directamente (`read_only`). | 400 en cualquier transición no listada. | `backend/services/views.py` → acciones de `ServicioViewSet`; `backend/services/serializers.py` → `ServicioSerializer.read_only_fields` | T-SRV-05, T-SRV-09, T-SRV-10, T-SRV-11 |
| RN-10 | Un servicio solo puede asignarse a una ruta si está en estado `CREADO`. | 400 "Solo se puede asignar ruta a un servicio en estado CREADO". | `backend/services/views.py` → `asignar_ruta` | T-SRV-05 |
| RN-11 | Solo el motorizado dueño de la ruta del servicio puede operarlo (recibir, transitar, cerrar, novedad) y reportar posición para él. | 403 / 404. | `backend/services/views.py` → `_motorizado_autorizado`, `get_queryset`; `backend/tracking/views.py` → `ReportarPosicionView` | T-SRV-06, T-TRK-02 |
| RN-12 | Un servicio en estado terminal no admite novedades ni cierre. | 400 "ya está cerrado". | `backend/services/views.py` → `novedad`, `cerrar` | T-SRV-11 |
| RN-13 | Un servicio de Entrega requiere `direccion_destino`; uno de Recolección requiere `direccion_origen`. **Solo se aplica en `POST /api/servicios/`**: `planificar` (RF-17) no la hace cumplir (H-13). | 400 en `POST /api/servicios/`. En `planificar` no hay rechazo: sin el campo la API responde 500 y con cadena vacía crea la recolección sin origen. | `backend/services/serializers.py` → `ServicioCreateSerializer.validate`. **No la aplican** `PlanificarRecoleccionSerializer` (acepta el campo vacío) ni `ServicioViewSet.planificar` | T-SRV-02, T-SRV-03 (solo `POST /api/servicios/`; `planificar` sin prueba) |
| RN-14 | **Visibilidad por propietario.** El cliente solo ve sus servicios, tracking, destino y chat; el motorizado solo los servicios de sus rutas. El chat de un servicio solo lo leen y escriben su cliente dueño y su motorizado asignado (ADMIN y ALISTADOR no). | 403 o 404 (no se revela la existencia del recurso). | `backend/services/views.py` → `get_queryset`, `mensajes`; `backend/services/consumers.py`, `backend/tracking/consumers.py`; `backend/tracking/views.py` | T-SRV-13, T-SRV-21, T-TRK-04, T-TRK-06, `MensajesChatTests.test_admin_y_alistador_no_pueden_leer_ni_escribir_en_el_chat` |
| RN-15 | Solo puede planificarse (o consultar agenda de) una zona con cobertura configurada; la zona es única en la matriz. | 400 al planificar; 404 en agenda disponible. | `backend/coverage/models.py` (`zona unique`); `backend/services/views.py` → `planificar`; `backend/coverage/views.py` | T-COV-04 |
| RN-16 | ~~Un pago procesado termina en `APROBADO` o `RECHAZADO`, nunca queda `PENDIENTE`; su referencia es única.~~ **Retirado del alcance (2026-10-09).** Motivo: los pagos se eliminaron para centrar el prototipo en el ciclo operativo de mensajería (§2.4). | — | — | — |
| RN-17 | Cada servicio tiene como máximo **una** evidencia; recapturarla la reemplaza. | — | `backend/services/models.py` → `Evidencia.servicio` (`OneToOneField`); `views.py` → `update_or_create` | T-SRV-09 |
| RN-18 | El correo de cada usuario es obligatorio y único, porque es credencial de acceso. | 400 por duplicado. | `backend/accounts/models.py` → `Usuario.email (unique=True)` | T-ACC-07 |
| RN-19 | La solicitud de restablecimiento de contraseña siempre responde lo mismo, exista o no el correo. | — (protección contra enumeración de usuarios) | `backend/accounts/views.py` → `PasswordResetRequestView` | T-ACC-09 |

**Diagrama de estados resumido (RN-09):**

```
CREADO --asignar-ruta--> ASIGNADO
ASIGNADO --recibir-en-centro (solo ENTREGA)--> RECIBIDO_CENTRO --iniciar-transito--> EN_TRANSITO
ASIGNADO --iniciar-transito (solo RECOLECCION)--> EN_TRANSITO
EN_TRANSITO --cerrar--> ENTREGADO | RECOLECTADO (requiere foto+firma)   [terminal]
{ASIGNADO, RECIBIDO_CENTRO, EN_TRANSITO, NOVEDAD} --novedad REINTENTAR--> NOVEDAD --iniciar-transito--> EN_TRANSITO
{ASIGNADO, RECIBIDO_CENTRO, EN_TRANSITO, NOVEDAD} --novedad DEVOLVER_A_CENTRO--> DEVUELTO   [terminal]
```

---

## 7. Restricciones del sistema (RES)

| ID | Tipo | Restricción | Impacto |
|---|---|---|---|
| RES-01 | Técnica — tecnología | Backend en Python con Django 6.1, Django REST Framework 3.18, SimpleJWT, Django Channels 4 + Daphne (ASGI) y drf-spectacular. Frontend en Ionic 9 + Angular 22, Leaflet (mapas), signature_pad (firma) y Capacitor 8. | Las decisiones de diseño y de despliegue quedan acotadas a este stack. |
| RES-02 | Técnica — base de datos | Se usa **SQLite** (`backend/db.sqlite3`) en desarrollo; no hay configuración de PostgreSQL u otro motor. | Concurrencia de escritura limitada; no apta para producción multiusuario sin migrar el motor. |
| RES-03 | Técnica — tiempo real | La capa de canales es `InMemoryChannelLayer`. | El tiempo real solo funciona con un único proceso servidor; escalar horizontalmente requiere Redis (no configurado). |
| RES-04 | Técnica — despliegue | La URL de la API del frontend está fija en `http://localhost:8000/api` (también en `environment.prod.ts`); los WebSockets se autentican con el JWT en la *query string*. | Requiere ajustar la configuración para desplegar fuera de localhost; el token en la URL puede quedar en logs, se recomienda HTTPS/WSS. |
| RES-05 | Dependencia externa — Nominatim | Política de uso de Nominatim: máximo 1 solicitud por segundo, User-Agent identificable, sin SLA. El sistema espera 1,1 s entre llamadas no cacheadas, usa timeout de 5 s y agrega ", Colombia" a la consulta. | Optimizar una ruta de N servicios sin caché tarda al menos ~1,1·N s; la calidad del resultado depende de la escritura de la dirección; requiere Internet. |
| RES-06 | ~~Dependencia externa — LLM simulado~~ | **Retirado del alcance (2026-10-09).** Motivo: el chatbot y su modelo de lenguaje simulado se eliminaron para centrar el prototipo en el ciclo operativo de mensajería (§2.4). | — |
| RES-07 | ~~Dependencia externa — pagos simulados~~ | **Retirado del alcance (2026-10-09).** Motivo: los pagos y su proveedor simulado se eliminaron para centrar el prototipo en el ciclo operativo de mensajería (§2.4). | — |
| RES-08 | Dependencia externa — correo | En desarrollo el correo se envía a la consola (`console.EmailBackend`); un envío real requiere configurar un servidor SMTP por variables de entorno. | La recuperación de contraseña solo es utilizable de punta a punta con SMTP configurado. |
| RES-09 | Dependencia externa — mapas | El mapa base usa teselas públicas de OpenStreetMap. | Requiere conexión a Internet y respetar la política de uso de teselas de OSM; el ETA es una estimación en línea recta, no un ruteo real. |
| RES-10 | Dispositivo | El motorizado necesita un dispositivo con **GPS** y navegador con API de Geolocalización (contexto seguro: HTTPS o localhost) y permiso de ubicación concedido; **cámara** (input `capture="environment"`) para la foto y pantalla táctil (o mouse) para la firma. | Sin permisos de ubicación o cámara no puede ejecutar RF-11 ni RF-14. |
| RES-11 | Legal — protección de datos | El sistema trata datos personales (nombre, correo, teléfono, direcciones, ubicación GPS en tiempo real, foto, firma y mensajes de chat), por lo que una operación real en Colombia queda sujeta a la **Ley 1581 de 2012** (Habeas Data) y su Decreto reglamentario 1377 de 2013 (compilado en el Decreto 1074 de 2015): autorización previa e informada del titular, finalidad declarada, política de tratamiento y derechos de consulta, actualización y supresión. | **La versión actual no implementa** aviso de privacidad, registro de autorización ni procedimiento de supresión; es requisito previo a cualquier uso con datos reales. Los datos de demostración son ficticios. |
| RES-12 | Legal — firma | La firma capturada en canvas es una firma electrónica simple (imagen), no una firma digital certificada en los términos de la Ley 527 de 1999. | Sirve como evidencia operativa de recolección, con valor probatorio limitado. |
| RES-13 | Alcance funcional | La optimización de rutas es para **un solo vehículo**, usa distancia en línea recta (haversine), parte del primer servicio de la ruta (no hay coordenada del centro) y **no persiste** el orden sugerido. | Es una sugerencia; no considera tráfico, ventanas horarias ni capacidad. |
| RES-14 | Distribución | El empaquetado nativo con Capacitor está configurado para Android, pero el build del APK no se verificó en la máquina de desarrollo (error de Gradle/JDK 21 en Windows); iOS requiere macOS + Xcode y no fue evaluado. | La entrega se valida como aplicación web responsive. |
| RES-15 | Académica — tiempo y autoría | Proyecto universitario de Ingeniería de Software (UNINPAHU), planificado en 17 semanas ([06-cronograma.md](../06-cronograma.md)), desarrollado por **un único integrante** (Javier Esteban Mora Osorio) y sin presupuesto. | Se priorizan servicios gratuitos. El ruteo multi-vehículo y otras mejoras quedan en el [roadmap](../07-roadmap-futuro.md) (anterior al cambio de alcance); inventario, pagos y asistente conversacional se retiraron del alcance (§2.4) y figuran como mejora futura opcional en [08-limitaciones-y-mejoras.md](08-limitaciones-y-mejoras.md) §8.4. |

---

## 8. Hallazgos: inconsistencias entre documentación y código

Detectadas al verificar este documento. No se modificó código; se registran para la matriz de trazabilidad y el plan de mejora. Tras el cambio de alcance del 2026-10-09, H-03 y H-12 quedaron resueltos por reducción de alcance (§2.4) y H-09 se conserva solo en lo relativo a los eventos de webhook. H-13 se detectó en la revisión posterior a ese cambio y se comprobó ejecutando la API contra una base de datos de pruebas aislada.

| ID | Hallazgo | Ubicación | Afecta |
|---|---|---|---|
| H-01 | `ServicioViewSet` es un `ModelViewSet`: `PUT/PATCH/DELETE /api/servicios/{id}/` solo exigen `IsAuthenticated`. Un cliente puede editar campos (zona, direcciones, ruta, fecha) o borrar sus propios servicios, y un motorizado los de su ruta; solo `estado` es de solo lectura. Además, `GET /api/rutas/` muestra **todas** las rutas a un cliente. | `backend/services/views.py` | RNF-02, RNF-20 |
| H-02 | Hueco en RN-01: una Entrega en `ASIGNADO` puede recibir una novedad `REINTENTAR` → `NOVEDAD` → `iniciar-transito`, saltándose `RECIBIDO_CENTRO`. | `backend/services/views.py` (`novedad`, `iniciar_transito`) | RN-01, RN-09 |
| H-03 | **Resuelto por reducción de alcance (2026-10-09).** El plan de pruebas decía `T-INV-02: Alistador crea producto → 201` mientras el código exigía ADMIN; el inventario y su caso de prueba se eliminaron del prototipo. | `docs/16-plan-pruebas.md` (histórico) | RF-04 (retirado) |
| H-04 | El caso de uso "Crear servicio «include» Validar cobertura y leadtime" ([10-diagrama-casos-uso.md](../10-diagrama-casos-uso.md)) no se cumple: `POST /api/servicios/` (Alistador/API Key) no valida cobertura ni leadtime; solo lo hace `planificar` (RF-17). (La parte de la compra por chatbot dejó de aplicar el 2026-10-09.) | `backend/services/serializers.py` | RN-03, RF-05 |
| H-05 | El plan de pruebas y el cronograma hablan de **93** pruebas; hoy existen **72** métodos `test_*` (96 antes del 2026-10-09: se retiraron 27 del inventario, los pagos y el chatbot y se añadieron 3 del chat restringido; además, p. ej. `tracking/tests.py::DestinoTests` y la bitácora de webhooks no tienen ID `T-`). | `docs/16-plan-pruebas.md`, `backend/*/tests.py` | RNF-17 |
| H-06 | RNF-04 en [02-requisitos.md](../02-requisitos.md) promete auditoría de cambios de estado (quién, cuándo, qué estado); el código solo registra novedades, evidencia y `creado_por`, no un historial de transiciones. | `backend/services/models.py` | RNF-04 |
| H-07 | Con `DEBUG=True` los archivos de `/media/` (fotos y firmas de evidencia) se sirven sin autenticación a quien conozca la URL. | `backend/cmedriver/urls.py` | RNF-20, RES-11 |
| H-08 | RF-08 (reasignar) no implementado; la desactivación de usuarios en el frontend hace `DELETE` y la creación sin contraseña usa `make_random_password()` (eliminado en Django 5.1). (La parte «RF-04 sin pantalla en el frontend» quedó resuelta por reducción de alcance, 2026-10-09.) | ver notas 1 y 3 de la sección 4 | RF-01, RF-08 |
| H-09 | `recibir-en-centro` e `iniciar-transito` no disparan eventos de webhook (no existen en `EVENTOS_WEBHOOK`). (Las partes «la compra por chatbot no descuenta stock» y «no dispara `servicio.creado`» quedaron resueltas por reducción de alcance, 2026-10-09.) | `backend/services/views.py`, `backend/integrations/models.py` | RF-25 |
| H-10 | El charter (§5) menciona "Login con 3 roles + vista de Cliente", pero el sistema tiene 4 roles con login propio (incluido CLIENTE). | `docs/01-project-charter.md` vs `backend/accounts/models.py` | Actores |
| H-11 | El backend permite `NOVEDAD → EN_TRANSITO` (`iniciar_transito` acepta `NOVEDAD` para ambos tipos), pero la app del motorizado oculta "Iniciar tránsito" y "Novedad" cuando el servicio está en `NOVEDAD`: `puedeIniciarTransito()` solo devuelve verdadero en `RECIBIDO_CENTRO` (Entrega) o `ASIGNADO` (Recolección), y `puedeRegistrarNovedad()` solo en `ASIGNADO`, `RECIBIDO_CENTRO` o `EN_TRANSITO`. Un servicio con novedad `REINTENTAR` queda detenido desde la app. | `frontend/src/app/features/motorizado/servicio-detail.page.ts` vs `backend/services/views.py` (`iniciar_transito`) | RF-13, RN-05, RN-09 |
| H-12 | **Resuelto por reducción de alcance (2026-10-09).** La compra por chatbot creaba la ENTREGA antes de procesar el pago y no la revertía si el pago quedaba `RECHAZADO`; el chatbot y los pagos se eliminaron del prototipo. | `backend/chatbot/llm.py` (código eliminado) | RF-23, RN-16 (retirados) |
| H-13 | `POST /api/servicios/planificar/` no valida `direccion_origen`. `PlanificarRecoleccionSerializer` es un `ModelSerializer` sobre `Servicio.direccion_origen` (`blank=True`), que no la exige, y `ServicioViewSet.planificar` luego lee `data['direccion_origen']`. Comprobado en una base de datos de pruebas aislada: sin el campo la API responde **500** (`KeyError`) y con `""` responde 201 y crea una RECOLECCION sin dirección de origen. **RN-13 no se cumple en `planificar`**: solo la aplica `ServicioCreateSerializer` (`POST /api/servicios/`). La app lo evita (`shared/planificar-form.component.ts` deshabilita el envío con la dirección vacía), así que solo se alcanza llamando a la API directamente. No tiene prueba. | `backend/services/serializers.py` (`PlanificarRecoleccionSerializer`); `backend/services/views.py` (`planificar`) | RF-17, RN-13, RNF-15 |

---

## 9. Índice de IDs

Vigencia tras el cambio de alcance del 2026-10-09: **RF** 24 vigentes de 29 (5 retirados: RF-04, RF-18, RF-22, RF-23, RF-26); **RNF** 19 de 20 (RNF-13 retirado); **RN** 16 de 19 (RN-04, RN-06, RN-16 retirados); **RES** 13 de 15 (RES-06, RES-07 retiradas); **metas funcionales** 6 de 7 (MF-5 retirada); **hallazgos** 11 abiertos de 13 (H-03 y H-12 resueltos por reducción de alcance, H-09 parcial; H-13 se añadió tras el cambio de alcance). Los IDs retirados se marcan «(retirado)».

### Requerimientos funcionales
| ID | Título corto |
|---|---|
| RF-01 | Gestionar usuarios |
| RF-02 | Configurar matriz de cobertura |
| RF-03 | Consultar panel de servicios |
| RF-04 | ~~Gestionar inventario~~ (retirado) |
| RF-05 | Crear servicio manual |
| RF-06 | Crear servicio vía API externa |
| RF-07 | Crear ruta y asignar servicio |
| RF-08 | Consultar estado e historial de novedades |
| RF-09 | Ver servicios asignados |
| RF-10 | Recibir en centro (Entrega) |
| RF-11 | Capturar evidencia (Recolección) |
| RF-12 | Iniciar tránsito y cerrar servicio |
| RF-13 | Registrar novedad |
| RF-14 | Reportar posición GPS |
| RF-15 | Ver tracking del motorizado |
| RF-16 | Chatear con el motorizado |
| RF-17 | Planificar recolección propia |
| RF-18 | ~~Usar chatbot guiado con catálogo~~ (retirado) |
| RF-19 | Iniciar sesión con usuario o correo |
| RF-20 | Restablecer contraseña por correo |
| RF-21 | Sugerir orden de ruta |
| RF-22 | ~~Chatbot en lenguaje libre (simulado)~~ (retirado) |
| RF-23 | ~~Generar pago al comprar por chatbot (simulado)~~ (retirado) |
| RF-24 | Generar API Keys |
| RF-25 | Configurar webhooks |
| RF-26 | ~~Asociar varios productos a un servicio~~ (retirado) |
| RF-27 | Tracking y chat en tiempo real |
| RF-28 | Ver destino y ETA en el mapa |
| RF-29 | Consultar bitácora de webhooks |

### Requerimientos no funcionales
RNF-01 JWT · RNF-02 RBAC · RNF-03 API documentada · RNF-04 Auditoría · RNF-05 Usabilidad móvil · RNF-06 Frecuencia GPS · RNF-07 Hash de contraseñas · RNF-08 Modularidad · RNF-09 Token de reset de un uso · RNF-10 Degradación a polling · RNF-11 Webhooks firmados · RNF-12 API Keys con hash · RNF-13 Proveedores intercambiables (retirado) · RNF-14 Portabilidad · RNF-15 Tolerancia a fallos externos · RNF-16 Latencia tiempo real · RNF-17 Suite de pruebas · RNF-18 Configuración segura · RNF-19 Localización · RNF-20 Privacidad.

### Reglas de negocio
RN-01 Entrega inicia en centro · RN-02 Evidencia obligatoria en Recolección · RN-03 Leadtime y días hábiles · RN-04 Producto visible en chatbot (retirado) · RN-05 Novedad con acción · RN-06 Producto protegido (retirado) · RN-07 Webhook por suscripción · RN-08 API Key actúa como Alistador · RN-09 Ciclo de vida del servicio · RN-10 Asignación solo desde CREADO · RN-11 Solo el motorizado asignado opera · RN-12 Estados terminales · RN-13 Dirección según tipo · RN-14 Visibilidad por propietario · RN-15 Zona con cobertura · RN-16 Resultado de pago (retirado) · RN-17 Una evidencia por servicio · RN-18 Correo único · RN-19 Reset sin enumeración.

### Hallazgos
H-01 Servicio editable/borrable por cualquier autenticado · H-02 Entrega puede saltarse el centro · H-03 T-INV-02 contradice el código (resuelto por reducción de alcance) · H-04 Sin validación de cobertura al crear · H-05 Conteo de pruebas desactualizado · H-06 Sin auditoría de transiciones · H-07 Media sin autenticación · H-08 Reasignar y desactivación de usuarios (la pantalla de inventario se retiró) · H-09 Eventos de webhook faltantes (la parte de stock y chatbot, resuelta por reducción de alcance) · H-10 Charter con 3 roles · H-11 App no reanuda un servicio en NOVEDAD · H-12 Compra no revierte la entrega con pago rechazado (resuelto por reducción de alcance) · H-13 `planificar` no valida `direccion_origen` (500 o origen vacío; RN-13 incumplida en ese endpoint).

### Restricciones
RES-01 Stack tecnológico · RES-02 SQLite · RES-03 Canales en memoria · RES-04 Configuración de despliegue · RES-05 Límite de Nominatim · RES-06 LLM simulado (retirado) · RES-07 Pagos simulados (retirado) · RES-08 Correo en consola · RES-09 Teselas OSM · RES-10 GPS y cámara · RES-11 Ley 1581 de 2012 · RES-12 Firma electrónica simple · RES-13 Alcance de la optimización · RES-14 Build nativo no verificado · RES-15 Tiempo y autoría individual.
