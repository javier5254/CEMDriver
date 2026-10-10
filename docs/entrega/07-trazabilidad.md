# Fase 6b — Matriz de trazabilidad

> **Objetivo:** demostrar que cada necesidad del problema se convierte en requerimientos, que esos requerimientos aparecen en el proceso (BPMN), en la arquitectura (C4), en los datos (MER) y en el código, y que el código está verificado por pruebas.
> **Insumos:** [01-requerimientos.md](01-requerimientos.md) (problema, OE-1…OE-4, metas funcionales MF-1…MF-7 que desglosan el OE-3 —MF-5 retirada—, RF-01…RF-29 —24 vigentes—, RNF-01…RNF-20 —19 vigentes—, RN-01…RN-19 —16 vigentes—, hallazgos H-01…H-13 —H-03 y H-12 resueltos por reducción de alcance; H-13 posterior a ese cambio—), [02-stack-tecnologico.md](02-stack-tecnologico.md), [03-arquitectura.md](03-arquitectura.md) (nombres canónicos; 6 apps), [04-mer.md](04-mer.md) (12 entidades), [05-bpmn.md](05-bpmn.md) (IDs de actividades y gateways), [06-c4.md](06-c4.md) (N2 contenedores, N3 componentes —6 apps—, N4 clases de `services`), [16-plan-pruebas.md](../16-plan-pruebas.md) (IDs `T-…`; documento histórico que conserva casos obsoletos, ver §g.2).
> **Verificación:** cada endpoint, archivo, clase, función y prueba citada se comprobó contra el código actual (`backend/*/urls.py`, `views.py`, `serializers.py`, `models.py`, `tests.py`, `cmedriver/routing.py` y `frontend/src/app`) y contra el archivo `docs/diagrams/src/bpmn-ciclo-servicio.bpmn`. El conteo de pruebas (72 métodos `test_*`) y el de clases de prueba se hicieron con `grep` sobre los `tests.py`. Los comportamientos de `planificar` y del chat que se señalan en §g.2 se comprobaron además con una ejecución puntual contra una base de datos de pruebas aislada (no se modificó código ni datos).

---

## Cambios de alcance (2026-10-09)

El autor retiró del proyecto el **inventario, los pagos y el chatbot** ([01 §2.4](01-requerimientos.md#24-cambios-de-alcance)); el chat queda solo para la comunicación cliente↔motorizado. Efecto en esta matriz:

- **Retirados (conservan su fila de una línea, sin renumerar):** RF-04, RF-18, RF-22, RF-23, RF-26 · RN-04, RN-06, RN-16 · RNF-13 · MF-5 (y RES-06, RES-07). No cuentan en ninguna métrica de §g. Los hallazgos H-03 y H-12 quedaron resueltos por reducción de alcance; H-09 sigue vigente solo para `recibir-en-centro` e `iniciar-transito`.
- **Vigentes:** 24 de 29 RF, 16 de 19 RN, 19 de 20 RNF y 6 de 7 MF. Todas las cifras de §g se recalcularon sobre los vigentes.
- **Modelos:** MER de 12 entidades (antes 17); backend de 6 apps (antes 9); C4 N1 con 5 sistemas externos (antes 7); BPMN sin `GW_QueSolicita`, `UT_Comprar`, `ST_CrearCompra`, `GW_MergeCreado` ni `TA_Compra` (`SE_Cliente` → `UT_Planificar` directo).
- **Pruebas:** 72 métodos `test_*` (antes 96: se retiraron 27 de lo eliminado y se añadieron 3 del chat restringido a cliente y motorizado). Los casos T-INV-01…03, T-BOT-01…09, T-PAG-01…03 y T-SRV-17…19 del plan de pruebas quedan obsoletos y ninguna fila vigente los cita.
- **P5 redefinido:** «sin autoservicio de agendamiento ni reglas de cobertura» (planificar una recolección y matriz de cobertura), sin chatbot ni compras.
- **Filas vigentes ajustadas:** RF-05, RF-16, RF-17, RF-25, RF-27, RN-03, RN-14, RNF-02, RNF-08, RNF-15, RNF-17, RNF-20, el desglose de OE-3 y el ejemplo narrado (§f, sin cambios de fondo).
- **Hallazgos de esta revisión** (marcados «nuevo» en §g.2): chat por WebSocket sin validación de longitud, `planificar` sin exigir `direccion_origen` (registrado como **H-13** y **LIM-39**; deja **RN-13 en estado Parcial**, antes Implementado), casos obsoletos del plan de pruebas y códigos 403 del plan que las pruebas reales verifican como 404. Dos huecos de la revisión anterior quedaron **resueltos** (marcados «resuelto» en §g.2): el acceso de ADMIN y ALISTADOR al chat (el código lo restringió al cliente dueño y al motorizado asignado y hay 3 pruebas nuevas) y el gateway `GW_MergeOpt` (ya figura en 05 §5).

---

## a. Cómo leer la matriz

Cada fila sigue la cadena **Necesidad → Requerimiento → Proceso → Arquitectura → Datos → Código → Prueba**:

| Columna | Qué contiene | Fuente |
|---|---|---|
| **RF** | ID estable del requerimiento funcional. | 01-requerimientos.md §4 |
| **Necesidad / OE** | Problema del §1 que atiende (P1…P6) y meta funcional (MF-1…MF-7, sin MF-5) del OE-3. | 01-requerimientos.md §1, §2.2 y §2.3 |
| **BPMN** | ID de la(s) actividad(es) del proceso "Ciclo de vida de un servicio" que lo ejecutan; *fuera del proceso modelado* si es configuración, autenticación o consulta transversal. | 05-bpmn.md §4–§5 |
| **C4 N2** | Contenedor(es) con nombre canónico. "App" = App CMEDriver, "API" = API REST CMEDriver, "Tiempo real" = Servicio de tiempo real. | 06-c4.md §3 |
| **C4 N3** | Componente(s) (apps Django o componentes transversales). | 06-c4.md §4 |
| **MER** | Entidad(es) que el RF lee o escribe. | 04-mer.md |
| **Código backend** | Método HTTP + ruta real y `archivo:Clase.método` (rutas relativas a `backend/`). | `urls.py`, `views.py` |
| **Frontend** | Página y servicio Angular que lo consumen (rutas relativas a `frontend/src/app/`). | `app.routes.ts`, `core/services` |
| **Prueba** | ID del plan (`T-…`) y prueba automatizada `app/tests.py::Clase.metodo`. | 16-plan-pruebas.md, `tests.py` |
| **Estado** | **Implementado** (cumple el criterio de aceptación), **Parcial** (algún criterio no se cumple; referencia al hallazgo H-xx o a §g.2), **Simulado** (la arquitectura es real pero el proveedor externo es un *mock*; desde el 2026-10-09 ningún elemento vigente tiene este estado) o **Retirado del alcance (2026-10-09)** (fila de una línea, sin datos de BPMN, C4 ni código). | Verificación en código |

Problemas del §1 de 01-requerimientos.md: **P1** asignación informal · **P2** cliente sin visibilidad · **P3** sin evidencia digital · **P4** novedades sin trazabilidad · **P5** sin autoservicio de agendamiento ni reglas de cobertura · **P6** sin integración con terceros.

---

## b. Cadena de alto nivel: Problema → Objetivos → RF

**Objetivos específicos (OE-1…OE-4, iguales a los del paper) → evidencia en la entrega:**

| Objetivo específico | Cómo se cumple | Evidencia |
|---|---|---|
| OE-1 Identificar problemas y derivar requerimientos priorizados | Problemas P1–P6 derivados de la literatura y del dominio; RF con prioridad, RNF, RN y RES | [01 §1](01-requerimientos.md#1-problema-o-necesidad-identificada), §4–§7 |
| OE-2 Diseñar y documentar la arquitectura y modelarla | Arquitectura orientada a API (REST, WebSocket, webhooks), MER, BPMN, C4 N1–N4, casos de uso, clases y mockups | [02](02-stack-tecnologico.md), [03](03-arquitectura.md), [04](04-mer.md), [05](05-bpmn.md), [06](06-c4.md) |
| OE-3 Implementar el prototipo funcional temprano | Metas funcionales MF-1…MF-7 (MF-5 retirada) → 24 RF vigentes → código y pruebas (tabla siguiente y §c) | `backend/`, `frontend/`, 72 pruebas |
| OE-4 Formular el protocolo de validación | Fuera del alcance de esta entrega técnica; se formula en el paper y se ejecuta en el Trabajo de Grado | Paper del proyecto (metodología) |

**Desglose del OE-3 en metas funcionales y RF:**

```
Necesidad: plataforma única para crear, asignar, ejecutar y seguir servicios de mensajería,
           con evidencia digital, seguimiento en tiempo real, chat directo cliente-motorizado,
           agendamiento de recolecciones por el propio cliente y API abierta.
```

| Problema (§1) | Objetivo específico | RF que lo cumplen |
|---|---|---|
| P1 Asignación informal, sin registro único de estados | MF-1 (configurar la operación), MF-2 (crear y asignar), MF-3 (ejecutar) | RF-01, RF-03, RF-05, RF-07, RF-09, RF-10, RF-12, RF-21 |
| P2 Cliente sin visibilidad | MF-4 (seguimiento en tiempo real y chat) | RF-08, RF-15, RF-16, RF-27, RF-28 |
| P3 Sin evidencia digital | MF-3 | RF-11 (+ RN-02, RN-17) |
| P4 Novedades sin trazabilidad | MF-3, MF-2 | RF-13 (+ RN-05), RF-08 |
| P5 Sin autoservicio de agendamiento ni reglas de cobertura | MF-1 (cobertura), MF-4 (planificar) | RF-02, RF-17 (+ RN-03, RN-15) |
| P6 Sin integración con terceros | MF-6 (API documentada, API Key, webhooks) | RF-06, RF-24, RF-25, RF-29 (+ RNF-03) |
| Transversal: acceso seguro de los 4 roles | MF-7 (seguridad y pruebas) | RF-19, RF-20 (+ RNF-01, RNF-02, RNF-07, RNF-12, RNF-17) |

Asignación de RF a objetivos (sin huecos ni duplicados): MF-1 → RF-01..03 · MF-2 → RF-05..08, RF-21 · MF-3 → RF-09..14 · MF-4 → RF-15..17, RF-27, RF-28 · MF-6 → RF-24, RF-25, RF-29 · MF-7 → RF-19, RF-20 (3 + 5 + 6 + 5 + 3 + 2 = 24). **Los 24 RF vigentes tienen objetivo y las seis metas vigentes tienen al menos un RF.** MF-5 (chatbot y pagos) está retirada y RF-04, RF-18, RF-22, RF-23 y RF-26 ya no se asignan a ninguna meta.

---

## c. Matriz principal (una fila por RF)

### c.1 Administrador (MF-1, MF-6)

| RF | Necesidad / OE | BPMN | C4 N2 | C4 N3 | MER | Código backend | Frontend | Prueba | Estado |
|---|---|---|---|---|---|---|---|---|---|
| **RF-01** Gestionar usuarios | P1 / MF-1 | Fuera del proceso modelado (configuración) | App, API | accounts, Permisos RBAC | USUARIO | `GET/POST/PATCH/DELETE /api/usuarios/` → `accounts/views.py:UsuarioViewSet` (`IsAdmin`); `accounts/serializers.py:UsuarioSerializer` | `features/admin/usuarios-list.page.ts`, `usuario-form.page.ts`; `core/services/usuarios.service.ts` | T-ACC-04, T-ACC-05, T-ACC-06 → `accounts/tests.py::UsuariosRBACTests.test_admin_puede_listar_usuarios`, `test_no_admin_no_puede_listar_usuarios`, `test_anonimo_no_puede_listar_usuarios` | **Parcial** (H-08: el frontend desactiva con `DELETE`; crear sin contraseña usa `make_random_password()`; crear/editar/desactivar sin prueba) |
| **RF-02** Configurar matriz de cobertura | P5 / MF-1 | Fuera del proceso (configuración); sus datos los usa `ST_ValidarAgenda` | App, API | coverage | COBERTURA | `/api/cobertura/` → `coverage/views.py:CoberturaViewSet`; `GET /api/cobertura/agenda-disponible/?zona=` → `AgendaDisponibleView` | `features/admin/cobertura-list.page.ts`, `cobertura-form.page.ts`; `core/services/cobertura.service.ts` | T-COV-01…04 → `coverage/tests.py::CoberturaTests` (4 pruebas) | Implementado |
| **RF-03** Consultar panel de servicios | P1 / MF-1 | Fuera del proceso (consulta) | App, API | services | SERVICIO | `GET /api/servicios/` → `services/views.py:ServicioViewSet.get_queryset` (ADMIN sin filtro) | `features/admin/dashboard.page.ts` (`serviciosService.list()`, contador por `EstadoServicio`) | **Sin prueba automatizada** ni caso manual propio en el plan (T-UI-01 solo cubre el login y la redirección al dashboard); verificación manual en navegador | Implementado |
| **RF-04** ~~Gestionar inventario~~ | — | — | — | — | — | — | — | — | **Retirado del alcance (2026-10-09)**: se eliminó la app `inventory` (01 §2.4) |
| **RF-24** Generar API Keys | P6 / MF-6 | Fuera del proceso (configuración); habilita `ST_AutenticarKey` | App, API | integrations, Autenticación por API Key | API_KEY, USUARIO | `/api/integraciones/api-keys/` → `integrations/views.py:ApiKeyViewSet.create`; `integrations/serializers.py:ApiKeyCreateSerializer.validate_actua_como` | `features/admin/api-keys-list.page.ts`; `core/services/api-keys.service.ts` | T-INT-01, T-INT-02, T-INT-03 → `integrations/tests.py::ApiKeyEndpointTests` (6), `ApiKeyAuthenticationTests` (4) | Implementado |
| **RF-25** Configurar webhooks | P6 / MF-6 | `SND_WebhookCreado`, `SND_WebhookAsignado`, `SND_WebhookEntregado`, `SND_WebhookRecolectado`, `SND_WebhookNovedad`, `SND_WebhookDevuelto` | App, API | integrations, Despachador de webhooks | WEBHOOK_ENDPOINT, WEBHOOK_DELIVERY | `/api/integraciones/webhooks/` → `integrations/views.py:WebhookEndpointViewSet`; envío: `integrations/services.py:disparar_webhook`, `firmar`, `_enviar_a_endpoint`; invocado por `services/views.py:ServicioViewSet._notificar` | `features/admin/webhooks-list.page.ts`; `core/services/webhooks.service.ts` | T-INT-01, T-INT-04, T-INT-05 → `integrations/tests.py::WebhookEndpointTests` (4), `DispararWebhookTests` (5) | Implementado (H-09: `recibir-en-centro` e `iniciar-transito` no emiten evento) |
| **RF-29** Consultar bitácora de webhooks | P6 / MF-6 | Fuera del proceso (consulta de lo registrado por `SND_Webhook*`) | App, API | integrations | WEBHOOK_DELIVERY | `GET /api/integraciones/webhooks/{endpoint_id}/entregas/` → `integrations/views.py:WebhookEntregasView` | `features/admin/webhooks-list.page.ts` (`webhooksService.entregas`) | Sin ID T- (H-05) → `integrations/tests.py::WebhookEndpointTests.test_entregas_endpoint_lista_bitacora_solo_para_admin` | Implementado |

### c.2 Alistador y sistema integrador (MF-2)

| RF | Necesidad / OE | BPMN | C4 N2 | C4 N3 | MER | Código backend | Frontend | Prueba | Estado |
|---|---|---|---|---|---|---|---|---|---|
| **RF-05** Crear servicio manual | P1 / MF-2 | `SE_Alistador`, `UT_Registrar`, `GW_MergeCreacion`, `ST_ValidarDatos`, `GW_DatosValidos`, `EE_Rechazo400`, `GW_MergeValidas`, `ST_RegistrarCreado`, `SND_WebhookCreado` | App, API | services, Permisos RBAC | SERVICIO, USUARIO | `POST /api/servicios/` → `services/views.py:ServicioViewSet.create` / `perform_create`; `services/serializers.py:ServicioCreateSerializer.validate` | `features/alistador/servicio-form.page.ts`; `servicios.service.ts:create` | T-SRV-01…04 → `services/tests.py::CrearServicioTests` (4) | Implementado (H-04: no valida cobertura ni leadtime) |
| **RF-06** Crear servicio vía API externa | P6 / MF-2 | `SE_API`, `ST_AutenticarKey`, `GW_KeyValida`, `EE_Rechazo401`, luego `GW_MergeCreacion` y el mismo camino de RF-05 | API, Documentación API | Autenticación por API Key, services | API_KEY, SERVICIO | `POST /api/servicios/` con `X-API-Key` → `integrations/authentication.py:ApiKeyAuthentication.authenticate` → `ApiKey.autenticar()` → `ServicioViewSet.create`; contrato en `GET /api/schema/`, `/api/docs/` | No aplica (actor externo) | T-INT-03 → `integrations/tests.py::ApiKeyAuthenticationTests` (4) | Implementado (sin prueba de punta a punta de `POST /api/servicios/` con API Key) |
| **RF-07** Crear ruta y asignar servicio | P1 / MF-2 | `UT_AsignarRuta`, `ST_PasarAsignado`, `SND_WebhookAsignado` | App, API | services, Despachador de webhooks | RUTA, SERVICIO | `POST /api/rutas/` → `services/views.py:RutaViewSet`; `POST /api/servicios/{id}/asignar-ruta/` → `ServicioViewSet.asignar_ruta` (`AsignarRutaSerializer`) | `features/alistador/ruta-form.page.ts`, `servicios-list.page.ts`; `rutas.service.ts:create`, `servicios.service.ts:asignarRuta` | T-SRV-05 → `services/tests.py::CicloDeVidaEntregaTests.test_flujo_completo_entrega` | Implementado |
| **RF-08** Consultar estado e historial de novedades | P2, P4 / MF-2 | Fuera del proceso modelado (consulta); la "reasignación" no existe | App, API | services | SERVICIO, NOVEDAD, EVIDENCIA | `GET /api/servicios/{id}/` → `ServicioViewSet.retrieve` con `services/serializers.py:ServicioSerializer` (`novedades[]`, `evidencia`) | Estado en `features/alistador/servicios-list.page.ts`; el historial de novedades solo se muestra en `features/motorizado/servicio-detail.page.ts` | Indirecta: T-SRV-09 (`CicloDeVidaRecoleccionTests.test_cerrar_con_evidencia_completa` verifica `evidencia`); ninguna prueba verifica `novedades[]` | **Parcial** (H-08: reasignar no implementado) |
| **RF-21** Sugerir orden de ruta | P1 / MF-2 | `GW_Optimizar`, `UT_PedirOrden`, `ST_Optimizar` (+ flujos `MF05`/`MF06` con Nominatim) | App, API | optimization, Cliente de geocodificación | RUTA, SERVICIO, PUNTO_GEOCODIFICADO | `POST /api/optimizacion/rutas/{ruta_id}/` → `optimization/views.py:OptimizarRutaView.post`; `optimization/geocoding.py:geocodificar`; `optimization/heuristica.py:ordenar_nearest_neighbor`, `haversine_km` | `features/alistador/optimizar-ruta.page.ts`; `optimizacion.service.ts:optimizar` | T-OPT-01…04 → `optimization/tests.py::OptimizarRutaTests` (8) | Implementado (alcance RES-13) |
| **RF-26** ~~Asociar varios productos a un servicio~~ | — | — | — | — | — | — | — | — | **Retirado del alcance (2026-10-09)**: se eliminaron `ServicioProducto` y `PUT /servicios/{id}/productos/` (01 §2.4) |

### c.3 Motorizado (MF-3)

| RF | Necesidad / OE | BPMN | C4 N2 | C4 N3 | MER | Código backend | Frontend | Prueba | Estado |
|---|---|---|---|---|---|---|---|---|---|
| **RF-09** Ver servicios asignados | P1 / MF-3 | `UT_ConsultarRuta` | App, API | services | SERVICIO, RUTA | `GET /api/servicios/` → `ServicioViewSet.get_queryset` (`ruta__motorizado=user`); `GET /api/rutas/` → `RutaViewSet.get_queryset` | `features/motorizado/servicios-list.page.ts` | T-SRV-06 → `services/tests.py::CicloDeVidaEntregaTests.test_motorizado_no_asignado_no_puede_operar_el_servicio` (la prueba verifica 404, no 403) | Implementado |
| **RF-10** Recibir en centro (Entrega) | P1 / MF-3 | `GW_TipoServicio`, `UT_RecibirCentro`, `ST_PasarRecibido` | App, API | services | SERVICIO | `POST /api/servicios/{id}/recibir-en-centro/` → `ServicioViewSet.recibir_en_centro` (+ `_motorizado_autorizado`) | `features/motorizado/servicio-detail.page.ts` (botón si `ENTREGA` y `ASIGNADO`); `servicios.service.ts:recibirEnCentro` | T-SRV-05, T-SRV-07 → `CicloDeVidaEntregaTests.test_flujo_completo_entrega`, `test_recibir_en_centro_no_aplica_a_recoleccion` | Implementado (H-02: un REINTENTAR permite saltarse el centro) |
| **RF-11** Capturar evidencia (Recolección) | P3 / MF-3 | `UT_Evidencia`, `ST_ValidarEvidencia`, `GW_EvidenciaOK`, `ST_PasarRecolectado`, `SND_WebhookRecolectado`, `EE_Recolectado` | App, API, Almacenamiento de evidencias | services, Despachador de webhooks | EVIDENCIA, SERVICIO | `POST /api/servicios/{id}/cerrar/` (multipart) → `ServicioViewSet.cerrar`; `services/serializers.py:CerrarServicioSerializer.validate`; `services/models.py:Evidencia` | `features/motorizado/servicio-detail.page.ts` (`<input capture="environment">`, `SignaturePad`); `servicios.service.ts:cerrar(id, {foto, firma})` | T-SRV-08, T-SRV-09 → `services/tests.py::CicloDeVidaRecoleccionTests.test_cerrar_sin_evidencia_falla`, `test_cerrar_con_evidencia_completa`; T-UI-02, T-UI-03 (manual) | Implementado |
| **RF-12** Iniciar tránsito y cerrar servicio | P1 / MF-3 | `UT_IniciarTransito`, `ST_PasarTransito`, `GW_MergeTransito`, `UT_ConfirmarEntrega`, `ST_PasarEntregado`, `SND_WebhookEntregado`, `EE_Entregado` | App, API | services, Despachador de webhooks | SERVICIO | `POST /api/servicios/{id}/iniciar-transito/` → `ServicioViewSet.iniciar_transito`; `POST /api/servicios/{id}/cerrar/` → `ServicioViewSet.cerrar` | `features/motorizado/servicio-detail.page.ts` (`puedeIniciarTransito`); `servicios.service.ts:iniciarTransito`, `cerrar` | T-SRV-05, T-SRV-09 → `CicloDeVidaEntregaTests.test_flujo_completo_entrega`, `CicloDeVidaRecoleccionTests.test_cerrar_con_evidencia_completa` | Implementado |
| **RF-13** Registrar novedad | P4 / MF-3 | `GW_Resultado`, `UT_RegistrarNovedad`, `ST_GuardarNovedad`, `GW_AccionNovedad`, `SND_WebhookNovedad`, `SND_WebhookDevuelto`, `EE_Devuelto` | App, API | services, Despachador de webhooks | NOVEDAD, SERVICIO | `POST /api/servicios/{id}/novedad/` → `ServicioViewSet.novedad`; `services/serializers.py:NovedadCreateSerializer`; `services/models.py:Novedad.Accion` | `features/motorizado/servicio-detail.page.ts` (`puedeRegistrarNovedad`); `servicios.service.ts:novedad` | T-SRV-10, T-SRV-11 → `services/tests.py::NovedadTests.test_reintentar_deja_en_novedad_y_permite_reintentar_transito`, `test_devolver_deja_servicio_terminal` | **Parcial** (H-11: tras REINTENTAR la app no permite reanudar) |
| **RF-14** Reportar posición GPS | P2 / MF-3 | `PG_Inicio`, `ST_EnviarGPS`, `IE_Cada8s`, `GW_SigueTransito`, `ST_DifundirGPS`, `PG_Fin` | App, API, Tiempo real, Capa de canales | tracking, TrackingConsumer | POSICION_GPS | `POST /api/tracking/posicion/` → `tracking/views.py:ReportarPosicionView.post` (`IsMotorizado`, `group_send('tracking_<id>')`) | `features/motorizado/servicio-detail.page.ts:startTracking` (`watchPosition` + `setInterval 8000`); `tracking.service.ts:postPosicion` | T-TRK-01, T-TRK-02 → `tracking/tests.py::TrackingTests.test_motorizado_asignado_puede_reportar_posicion`, `test_motorizado_no_asignado_no_puede_reportar_posicion`; T-UI-04 (manual) | Implementado (nota 4: el backend no exige `EN_TRANSITO`) |

### c.4 Cliente (MF-4)

| RF | Necesidad / OE | BPMN | C4 N2 | C4 N3 | MER | Código backend | Frontend | Prueba | Estado |
|---|---|---|---|---|---|---|---|---|---|
| **RF-15** Ver tracking del motorizado | P2 / MF-4 | Fuera de las actividades (anotación `TA_Tracking`, 05-bpmn §7) | App, API | tracking | POSICION_GPS, SERVICIO | `GET /api/tracking/ultima-posicion/?servicio_id=` → `tracking/views.py:UltimaPosicionView.get` | `features/cliente/tracking.page.ts` (Leaflet); `tracking.service.ts:ultimaPosicion` | T-TRK-03, T-TRK-04 → `tracking/tests.py::TrackingTests.test_cliente_dueno_puede_ver_ultima_posicion`, `test_otro_cliente_no_puede_ver_la_posicion` | Implementado |
| **RF-16** Chatear con el motorizado | P2 / MF-4 | Fuera de las actividades (anotación `TA_Tracking`, `ws/chat/{id}/`, 05-bpmn §7) | App, API, Tiempo real | services, ChatConsumer | MENSAJE_CHAT, SERVICIO | `GET/POST /api/servicios/{id}/mensajes/` → `services/views.py:ServicioViewSet.mensajes` (solo el cliente dueño y el motorizado asignado; ADMIN y ALISTADOR reciben 403; otro cliente u otro motorizado, 404); `services/serializers.py:MensajeChatSerializer` (`max_length=1000`) | `shared/chat.page.ts` (rutas `cliente/servicios/:id/chat` y `motorizado/servicios/:id/chat`); `servicios.service.ts:mensajes`, `enviarMensaje` | T-SRV-12…14 → `services/tests.py::MensajesChatTests` (5: `test_cliente_dueno_puede_enviar_y_leer_mensajes`, `test_otro_cliente_no_puede_acceder_al_chat` —verifica 404—, `test_motorizado_asignado_puede_participar`, `test_admin_y_alistador_no_pueden_leer_ni_escribir_en_el_chat` —verifica 403—, `test_motorizado_no_asignado_no_puede_acceder_al_chat` —verifica 404—); `ChatWebSocketTests.test_admin_y_alistador_no_pueden_conectarse_al_chat` | Implementado (criterios (a)–(d) con prueba; el límite de 1000 caracteres solo se valida por REST: §g.2, nuevo) |
| **RF-17** Planificar recolección propia | P5 / MF-4 | `SE_Cliente`, `UT_Planificar`, `ST_ValidarAgenda`, `GW_AgendaValida`, `EE_RechazoAgenda`, `GW_MergeValidas`, `ST_RegistrarCreado`, `SND_WebhookCreado` | App, API | services, coverage | SERVICIO, COBERTURA | `POST /api/servicios/planificar/` → `ServicioViewSet.planificar` (`PlanificarRecoleccionSerializer`, `Cobertura`, `DIAS_ORDEN`); agenda: `GET /api/cobertura/agenda-disponible/` | `features/cliente/planificar.page.ts` + `shared/planificar-form.component.ts`; `servicios.service.ts:planificar`, `cobertura.service.ts:agendaDisponible` | T-SRV-15, T-SRV-16 → `services/tests.py::PlanificarRecoleccionTests.test_planificar_respeta_leadtime`, `test_planificar_fecha_valida_crea_recoleccion` | Implementado (criterios "día no habilitado" y "zona sin cobertura" sin prueba; la API no exige `direccion_origen`: H-13, LIM-39) |
| **RF-18** ~~Usar chatbot guiado con catálogo~~ | — | — | — | — | — | — | — | — | **Retirado del alcance (2026-10-09)**: se eliminaron la app `chatbot` y el catálogo para el chatbot (01 §2.4) |
| **RF-22** ~~Chatbot en lenguaje libre~~ | — | — | — | — | — | — | — | — | **Retirado del alcance (2026-10-09)**: se eliminaron el chatbot y su modelo de lenguaje simulado (01 §2.4) |
| **RF-23** ~~Generar pago al comprar por chatbot~~ | — | — | — | — | — | — | — | — | **Retirado del alcance (2026-10-09)**: se eliminaron la app `payments` y la compra por chatbot (01 §2.4) |
| **RF-27** Tracking y chat en tiempo real | P2 / MF-4 | `ST_DifundirGPS` (+ anotaciones de `ws/tracking` y `ws/chat` en `TA_Tracking`) | App, Tiempo real, Capa de canales | Middleware JWT de WebSocket, TrackingConsumer, ChatConsumer | POSICION_GPS, MENSAJE_CHAT | `ws/tracking/{servicio_id}/` → `tracking/consumers.py:TrackingConsumer`; `ws/chat/{servicio_id}/` → `services/consumers.py:ChatConsumer` (solo cliente dueño y motorizado asignado; `cmedriver/routing.py`); `cmedriver/ws_auth.py:JWTAuthMiddleware` | `tracking.service.ts:conectarTracking` + respaldo `POLL_FALLBACK_MS = 8000` en `features/cliente/tracking.page.ts`; `shared/chat.page.ts` (WebSocket + `POLL_FALLBACK_MS = 5000`) | T-SRV-20, T-SRV-21, T-TRK-05, T-TRK-06 → `services/tests.py::ChatWebSocketTests` (3), `tracking/tests.py::TrackingWebSocketTests` (2) | Implementado (la app recibe el chat por WebSocket pero lo envía por REST; el envío por WebSocket solo lo ejerce T-SRV-20) |
| **RF-28** Ver destino y ETA en el mapa | P2 / MF-4 | Fuera de las actividades (consulta de apoyo al tracking; mencionado en `TA_Tracking`) | App, API | tracking, Cliente de geocodificación | PUNTO_GEOCODIFICADO, SERVICIO | `GET /api/tracking/destino/?servicio_id=` → `tracking/views.py:DestinoView` (usa `optimization/geocoding.py:geocodificar`) | `features/cliente/tracking.page.ts` (`obtenerDestino`, `etaMinutos`); el motorizado no lo consume en su app | Sin ID T- (H-05) → `tracking/tests.py::DestinoTests` (3) | Implementado (en la app solo para el Cliente) |

### c.5 Todos los usuarios (MF-7)

| RF | Necesidad / OE | BPMN | C4 N2 | C4 N3 | MER | Código backend | Frontend | Prueba | Estado |
|---|---|---|---|---|---|---|---|---|---|
| **RF-19** Iniciar sesión con usuario o correo | Transversal / MF-7 | Fuera del proceso modelado (precondición de todos los lanes) | App, API | accounts, Autenticación JWT | USUARIO | `POST /api/auth/login/` → `accounts/views.py:LoginView` (`CMEDriverTokenObtainPairSerializer.validate`); `POST /api/auth/refresh/` → `TokenRefreshView`; `GET /api/auth/me/` → `MeView` | `features/auth/login.page.ts`; `auth.service.ts:login`, `refreshToken`; `core/interceptors/auth.interceptor.ts`; `core/guards/auth.guard.ts`, `role.guard.ts` | T-ACC-01, 02, 03, 07 → `accounts/tests.py::AuthTests` (4) | Implementado |
| **RF-20** Restablecer contraseña por correo | Transversal / MF-7 | Fuera del proceso modelado | App, API (+ Servidor SMTP externo) | accounts | USUARIO | `POST /api/auth/password-reset/` → `PasswordResetRequestView`; `POST /api/auth/password-reset/confirm/` → `PasswordResetConfirmView` | `features/auth/forgot-password.page.ts`, `reset-password.page.ts`; `auth.service.ts:requestPasswordReset`, `confirmPasswordReset` | T-ACC-08…11 → `accounts/tests.py::PasswordResetTests` (4) | Implementado (correo por consola en desarrollo, RES-08) |

---

## d. Matriz de reglas de negocio (RN-01…RN-19; 16 vigentes)

| RN | Gateway / actividad BPMN | Dónde se aplica en código (`backend/`) | Entidad.campo (MER) | Prueba | Estado |
|---|---|---|---|---|---|
| RN-01 Entrega inicia en centro | `GW_TipoServicio`, `ST_PasarRecibido`, `ST_PasarTransito` (anotación `TA_H02`) | `services/views.py:ServicioViewSet.recibir_en_centro`, `iniciar_transito` (`estados_validos_por_tipo`) | SERVICIO.tipo, SERVICIO.estado | T-SRV-05, T-SRV-07 | **Parcial** (H-02) |
| RN-02 Evidencia obligatoria en Recolección | `ST_ValidarEvidencia`, `GW_EvidenciaOK` | `services/serializers.py:CerrarServicioSerializer.validate`; `views.py:ServicioViewSet.cerrar` | EVIDENCIA.foto, EVIDENCIA.firma | T-SRV-08, T-SRV-09 | Implementado |
| RN-03 Leadtime y días hábiles | `ST_ValidarAgenda`, `GW_AgendaValida`, `EE_RechazoAgenda` (anotación `TA_H04`) | `services/views.py:ServicioViewSet.planificar`; `coverage/views.py:AgendaDisponibleView` | COBERTURA.leadtime_dias, COBERTURA.dias_disponibles, SERVICIO.fecha_agenda | T-SRV-15, T-COV-03 (el rechazo por "día no habilitado" de `planificar` no se prueba) | **Parcial** (H-04: no aplica a la creación manual ni a la de API Key) |
| RN-04 ~~Producto visible en chatbot~~ | — | — | — | — | **Retirado del alcance (2026-10-09)** |
| RN-05 Novedad con acción | `GW_AccionNovedad`, `ST_GuardarNovedad` | `services/models.py:Novedad.Accion`; `views.py:ServicioViewSet.novedad`; `serializers.py:NovedadCreateSerializer` | NOVEDAD.accion | T-SRV-10, T-SRV-11 | Implementado |
| RN-06 ~~Producto protegido~~ | — | — | — | — | **Retirado del alcance (2026-10-09)** |
| RN-07 Webhook por suscripción | `SND_Webhook*` (6 tareas) | `integrations/models.py:WebhookEndpoint.suscrito_a`; `integrations/services.py:disparar_webhook` | WEBHOOK_ENDPOINT.activo, WEBHOOK_ENDPOINT.eventos | `integrations/tests.py::DispararWebhookTests.test_evento_no_suscrito_no_genera_entrega`, `test_endpoint_inactivo_no_recibe_webhooks` | Implementado |
| RN-08 API Key actúa como Alistador | `ST_AutenticarKey`, `GW_KeyValida`, `EE_Rechazo401` | `integrations/serializers.py:ApiKeyCreateSerializer.validate_actua_como`; `integrations/authentication.py:ApiKeyAuthentication.authenticate`; `models.py:ApiKey.autenticar` | API_KEY.actua_como, API_KEY.activa | `ApiKeyEndpointTests.test_actua_como_debe_ser_alistador`, T-INT-03 | Implementado |
| RN-09 Ciclo de vida del servicio | `ST_PasarAsignado`, `ST_PasarRecibido`, `ST_PasarTransito`, `ST_PasarEntregado`, `ST_PasarRecolectado`, `ST_GuardarNovedad`, `GW_MergeTransito` | Acciones de `services/views.py:ServicioViewSet`; `serializers.py:ServicioSerializer` (`estado` de solo lectura) | SERVICIO.estado (`EstadoServicio`) | T-SRV-05, T-SRV-09, T-SRV-10, T-SRV-11 | **Parcial** (H-02 en backend; H-11 en la app) |
| RN-10 Asignación solo desde CREADO | `ST_PasarAsignado` | `services/views.py:ServicioViewSet.asignar_ruta` | SERVICIO.estado, SERVICIO.ruta_id | T-SRV-05 (camino feliz; el rechazo 400 no se prueba) | Implementado |
| RN-11 Solo el motorizado asignado opera | `UT_ConsultarRuta`, `ST_PasarRecibido`, `UT_IniciarTransito`, `ST_EnviarGPS` | `services/views.py:ServicioViewSet._motorizado_autorizado`, `get_queryset`; `tracking/views.py:ReportarPosicionView` | RUTA.motorizado_id, SERVICIO.ruta_id | T-SRV-06, T-TRK-02 | Implementado |
| RN-12 Estados terminales | `ST_PasarEntregado`, `ST_GuardarNovedad`, fines `EE_Entregado`/`EE_Recolectado`/`EE_Devuelto` | `services/views.py:ServicioViewSet.novedad`, `cerrar` | SERVICIO.estado | T-SRV-11 (cerrar tras `DEVUELTO`); novedad sobre servicio cerrado sin prueba | Implementado |
| RN-13 Dirección según tipo | `ST_ValidarDatos`, `GW_DatosValidos`, `EE_Rechazo400` (solo el camino Alistador / API Key) | `services/serializers.py:ServicioCreateSerializer.validate`. **`PlanificarRecoleccionSerializer` no la aplica** (omitir `direccion_origen` provoca un 500 y enviarla vacía crea la recolección sin origen) | SERVICIO.direccion_destino, SERVICIO.direccion_origen | T-SRV-02, T-SRV-03 (solo `POST /api/servicios/`) | **Parcial** (`planificar`, H-13) |
| RN-14 Visibilidad por propietario | Fuera del proceso (transversal a todos los lanes) | `services/views.py:ServicioViewSet.get_queryset`, `mensajes`; `services/consumers.py:ChatConsumer._usuario_autorizado`; `tracking/consumers.py:TrackingConsumer`; `tracking/views.py:UltimaPosicionView`, `DestinoView` | SERVICIO.cliente_id, RUTA.motorizado_id | T-SRV-13, T-SRV-21, T-TRK-04, T-TRK-06, `tracking/tests.py::DestinoTests.test_otro_cliente_no_puede_ver_el_destino`, `services/tests.py::MensajesChatTests.test_admin_y_alistador_no_pueden_leer_ni_escribir_en_el_chat` | **Parcial** (H-01; `UltimaPosicionView` no restringe al motorizado, 06-c4 §7, observación 7) |
| RN-15 Zona con cobertura | `ST_ValidarAgenda`, `GW_AgendaValida` | `coverage/models.py:Cobertura.zona` (`unique`); `services/views.py:ServicioViewSet.planificar`; `coverage/views.py:AgendaDisponibleView` | COBERTURA.zona | T-COV-04 (agenda); el 400 de `planificar` sin prueba | Implementado |
| RN-16 ~~Resultado de pago~~ | — | — | — | — | **Retirado del alcance (2026-10-09)** |
| RN-17 Una evidencia por servicio | `ST_PasarRecolectado` | `services/models.py:Evidencia.servicio` (`OneToOneField`); `views.py:ServicioViewSet.cerrar` (`update_or_create`) | EVIDENCIA.servicio_id (UK) | T-SRV-09 (creación); el reemplazo no se prueba | Implementado |
| RN-18 Correo único | Fuera del proceso modelado | `accounts/models.py:Usuario.email` (`unique=True`) | USUARIO.email | **Sin prueba de duplicado** (T-ACC-07 prueba el login por correo, no la unicidad) | Implementado |
| RN-19 Reset sin enumeración | Fuera del proceso modelado | `accounts/views.py:PasswordResetRequestView.post` | USUARIO.email | T-ACC-09 | Implementado |

---

## e. Matriz RNF principales → decisión de stack/arquitectura → evidencia

| RNF | Decisión de stack / arquitectura | Dónde está en el C4 | Evidencia verificable |
|---|---|---|---|
| RNF-01 JWT | SimpleJWT (access 8 h, refresh 1 día); JWT también para WebSocket | N3 Autenticación JWT, Middleware JWT de WebSocket | `cmedriver/settings.py` (`SIMPLE_JWT`, `DEFAULT_AUTHENTICATION_CLASSES`); `cmedriver/ws_auth.py:JWTAuthMiddleware`; T-ACC-01, T-ACC-06 |
| RNF-02 RBAC | Rol en `Usuario.rol` + clases de permiso por vista + filtrado en `get_queryset` | N3 Permisos RBAC | `accounts/permissions.py`; `ServicioViewSet.get_permissions`; T-ACC-05, T-COV-01, T-SRV-01, T-SRV-06, T-SRV-13, T-TRK-02, T-TRK-04, T-OPT-01, T-INT-01 (⚠️ H-01) |
| RNF-03 API documentada | drf-spectacular (OpenAPI 3 + Swagger UI) | N2 Documentación API | `GET /api/schema/`, `GET /api/docs/` en `cmedriver/urls.py`; inspección manual |
| RNF-07 / RNF-12 Credenciales con hash | `set_password()` (PBKDF2); API Key guardada como SHA-256 + prefijo | N3 accounts, Autenticación por API Key | `integrations/models.py:ApiKey.key_hash`, `prefix`; T-ACC-10, T-INT-02 |
| RNF-08 Modularidad | Monolito modular de 6 apps Django (`accounts`, `coverage`, `services`, `tracking`, `optimization`, `integrations`; decisión §8 de 03-arquitectura) | N3: 6 componentes (apps) | Estructura `backend/<app>/{models,serializers,views,urls,tests}.py` (verificada en las 6 apps); `INSTALLED_APPS` en `cmedriver/settings.py` |
| RNF-10 / RNF-16 Tiempo real y resiliencia | Django Channels + Daphne en el mismo proceso ASGI; polling de respaldo en el frontend | N2 Servicio de tiempo real, Capa de canales | `cmedriver/asgi.py`, `cmedriver/routing.py`; `POLL_FALLBACK_MS` 8000/5000 en `tracking.page.ts`/`chat.page.ts`; T-SRV-20, T-TRK-05 |
| RNF-11 Webhooks firmados *best-effort* | HMAC-SHA256 en `X-CMEDriver-Signature`, timeout por endpoint, nunca propaga errores | N3 Despachador de webhooks | `integrations/services.py:firmar`, `_enviar_a_endpoint` (`urlopen(..., timeout=...)`); T-INT-04, T-INT-05 |
| RNF-13 ~~Proveedores intercambiables~~ | — | — | **Retirado del alcance (2026-10-09)**: solo se refería a `MockLLMClient` y `MockPaymentProvider`, eliminados con el chatbot y los pagos |
| RNF-15 Tolerancia a fallos externos | `geocodificar` devuelve `None` ante cualquier falla de Nominatim (caché `PuntoGeocodificado` y salida controlada); webhook caído se registra con `exito=False` | N3 Cliente de geocodificación, Despachador de webhooks | T-OPT-03, T-INT-05, `tracking/tests.py::DestinoTests.test_geocoding_fallido_devuelve_404_no_500` |
| RNF-05 / RNF-14 Usabilidad móvil y portabilidad | Ionic 9 + Angular 22 (tema iOS) y Capacitor 8 | N2 App CMEDriver | T-UI-05 (manual); build Android no verificado (RES-14) |
| RNF-06 Frecuencia GPS | Intervalo fijo de 8 s en la app | N2 App CMEDriver | `features/motorizado/servicio-detail.page.ts:startTracking` (`setInterval(..., 8000)`); BPMN `IE_Cada8s` |
| RNF-17 Suite de pruebas | Django test runner + `APIClient`, BD aislada | — | 72 métodos `test_*` en 6 `tests.py` (accounts 11, coverage 4, integrations 19, optimization 8, services 21, tracking 9); `run_tests.ps1` / `run_tests.sh` (⚠️ H-05: el plan dice 93; eran 96 antes del 2026-10-09) |
| RNF-18 Configuración segura | Variables de entorno; arranque bloqueado sin `DJANGO_SECRET_KEY` en producción | N2 nodo Servidor ASGI Daphne | `cmedriver/settings.py` (`RuntimeError` si `DEBUG=False` sin clave) |
| RNF-20 Privacidad | Filtrado por propietario (RN-14) en servicios, tracking, destino y chat | N3 Permisos RBAC + `get_queryset` | T-SRV-13, T-SRV-21, T-TRK-04, T-TRK-06, `MensajesChatTests.test_admin_y_alistador_no_pueden_leer_ni_escribir_en_el_chat` (⚠️ H-01, H-07, RES-11) |

---

## f. Ejemplo narrado de punta a punta: RF-11 "Capturar evidencia" + RN-02

Este recorrido sirve para la sustentación porque toca todas las capas con un requerimiento de prioridad Alta. Los elementos citados (actividades BPMN, componentes C4, entidades MER y pruebas) siguen vigentes tras el retiro de inventario, pagos y chatbot: se comprobaron de nuevo contra el `.bpmn`, 06-c4.md y los `tests.py`.

1. **Necesidad (P3).** Las recolecciones no dejan prueba verificable, lo que dificulta resolver reclamos. → **Objetivo MF-3**: el Motorizado ejecuta el servicio con flujo diferenciado y *recolectar con foto y firma*.
2. **Requerimiento.** **RF-11**: "El sistema debe exigir una foto del producto y una firma digital del cliente para cerrar un servicio de RECOLECCION, y almacenarlas como `Evidencia` del servicio". Lo refuerzan **RN-02** (sin foto **y** firma no se cierra) y **RN-17** (máximo una evidencia por servicio).
3. **Proceso (BPMN).** En el lane *Motorizado*, después de `MT_Visita` y del `PG_Fin`, el gateway `GW_Resultado` (¿se pudo recolectar?) toma la rama "Sí"; `GW_TipoCierre` deriva por RECOLECCIÓN a **`UT_Evidencia`** (capturar foto y firma y cerrar). En el lane *Sistema*, **`ST_ValidarEvidencia`** aplica RN-02 y **`GW_EvidenciaOK`** decide: "No" (HTTP 400) devuelve a `UT_Evidencia`; "Sí" pasa a **`ST_PasarRecolectado`**, luego **`SND_WebhookRecolectado`** (flujo de mensaje `MF07` al sistema integrador) y termina en **`EE_Recolectado`**.
4. **Arquitectura (C4).**
   - **N1:** la persona *Motorizado* usa la *Plataforma CMEDriver*; el *Receptor de webhooks* recibe `servicio.recolectado`.
   - **N2:** *App CMEDriver* → (HTTPS multipart + JWT) → *API REST CMEDriver* → escribe los archivos en *Almacenamiento de evidencias* (`media/evidencias/fotos|firmas/`) y la fila en *Base de datos*.
   - **N3:** componente **services** (núcleo), con *Autenticación JWT*, *Permisos RBAC* (`IsMotorizado`) y *Despachador de webhooks*.
   - **N4:** `ServicioViewSet.cerrar` → `_motorizado_autorizado` (RN-11) → `CerrarServicioSerializer.validate` (RN-02) → `Evidencia.objects.update_or_create` (RN-17) → `servicio.estado = RECOLECTADO` → `_notificar('servicio.recolectado')` → `disparar_webhook`.
5. **Datos (MER).** Entidad **EVIDENCIA** (`services.Evidencia`): `servicio_id` FK→SERVICIO con UK (relación 1:0..1), `foto`, `firma` (rutas de imagen) y `capturado_en` (auditoría, RNF-04). Cambia **SERVICIO.estado** de `EN_TRANSITO` a `RECOLECTADO` (terminal, RN-09/RN-12). Se registra una fila de **WEBHOOK_DELIVERY** por cada **WEBHOOK_ENDPOINT** activo suscrito (RN-07).
6. **Código.**
   - Endpoint: `POST /api/servicios/{id}/cerrar/` (multipart con `foto` y `firma`), ruta generada por `DefaultRouter` en `backend/services/urls.py` a partir de `@action(detail=True, methods=['post'], url_path='cerrar')`.
   - Backend: `backend/services/views.py:ServicioViewSet.cerrar`; `backend/services/serializers.py:CerrarServicioSerializer.validate` (mensaje "Un servicio de RECOLECCION requiere foto y firma para poder cerrarse."); `backend/services/models.py:Evidencia`.
   - Frontend: `frontend/src/app/features/motorizado/servicio-detail.page.ts` toma la foto con `<input type="file" accept="image/*" capture="environment">`, dibuja la firma con `SignaturePad` y llama a `core/services/servicios.service.ts:cerrar(id, { foto, firma })`, que arma un `FormData`.
7. **Pruebas.**
   - **T-SRV-08** → `backend/services/tests.py::CicloDeVidaRecoleccionTests.test_cerrar_sin_evidencia_falla`: cerrar sin archivos responde **400** (rama "No" de `GW_EvidenciaOK`).
   - **T-SRV-09** → `backend/services/tests.py::CicloDeVidaRecoleccionTests.test_cerrar_con_evidencia_completa`: con foto y firma responde **200**, `estado = RECOLECTADO` y `evidencia` no nula (rama "Sí", `EE_Recolectado`).
   - **T-UI-02 / T-UI-03** (manuales): captura real con cámara y firma en canvas.
   - La firma del webhook resultante la verifica `integrations/tests.py::DispararWebhookTests.test_envio_exitoso_registra_entrega_y_firma_correcta` (T-INT-04).

**Resultado:** RF-11 queda trazado sin huecos desde la necesidad hasta una prueba automatizada que pasa, y cada regla que lo acompaña (RN-02, RN-09, RN-11, RN-17, RN-07) tiene un punto concreto de aplicación en el código.

---

## g. Cobertura y huecos de trazabilidad

### g.1 Métricas

Todas las cifras se calculan sobre los elementos **vigentes** tras el cambio de alcance del 2026-10-09 (RF 24, RN 16, RNF 19). Los retirados (RF-04, 18, 22, 23, 26; RN-04, 06, 16; RNF-13) conservan su fila de una línea y no entran en ninguna métrica.

| Indicador | Valor | Detalle |
|---|---|---|
| RF vigentes | **24 / 29** | Retirados: RF-04, RF-18, RF-22, RF-23, RF-26 |
| RF con objetivo específico (OE) | **24 / 24 (100 %)** | Ver §b (MF-1: 3 · MF-2: 5 · MF-3: 6 · MF-4: 5 · MF-6: 3 · MF-7: 2) |
| RF con al menos una prueba automatizada específica | **22 / 24 (92 %)** | Sin prueba específica: RF-03 (ninguna) y RF-08 (solo indirecta) |
| RF con alguna prueba automatizada (incluida indirecta) | **23 / 24 (96 %)** | Solo RF-03 depende de verificación manual |
| RF que aparecen como actividad en el BPMN | **13 / 24 (54 %)** | RF-05, 06, 07, 09, 10, 11, 12, 13, 14, 17, 21, 25, 27 (coincide con 05-bpmn §1) |
| RF fuera del proceso modelado | **11 / 24** | RF-01, 02, 03, 08, 15, 16, 19, 20, 24, 28, 29 (configuración, autenticación y consultas; RF-15, RF-16 y RF-28 aparecen solo en la anotación `TA_Tracking` y RF-02 como dato de `ST_ValidarAgenda`) |
| RF con componente C4 N3 y entidad MER | **24 / 24** | Toda fila vigente de §c tiene ambos |
| Entidades MER usadas por al menos un RF | **12 / 12** | Ninguna entidad huérfana |
| RF con pantalla en el frontend | **23 / 24 (96 %)** | Sin pantalla: RF-06 (actor externo, no aplica). Parciales en la UI: RF-08 (el Alistador no ve el historial de novedades) y RF-28 (solo para el Cliente) |
| Estado de los RF | **21 Implementado · 3 Parcial · 0 Simulado** | Parcial: RF-01 (H-08), RF-08 (H-08), RF-13 (H-11) |
| RN vigentes | **16 / 19** | Retiradas: RN-04, RN-06, RN-16 |
| RN con prueba automatizada | **15 / 16 (94 %)** | Sin prueba: RN-18. Solo camino feliz o cobertura parcial: RN-03, RN-10, RN-12, RN-13 (solo en `POST /servicios/`), RN-15, RN-17 |
| RN con punto en el BPMN | **13 / 16 (81 %)** | Fuera del proceso: RN-14, RN-18, RN-19 |
| Estado de las RN | **11 Implementado · 5 Parcial · 0 Simulado** | Parcial: RN-01 (H-02), RN-03 (H-04), RN-09 (H-02, H-11), RN-13 (`planificar`, H-13), RN-14 (H-01) |
| RNF vigentes con fila en §e | **16 / 19 (84 %)** | Sin fila (la matriz es de «principales»): RNF-04, RNF-09, RNF-19; su evidencia está en 01 §5 |
| Pruebas automatizadas existentes | **72 métodos `test_*`** | accounts 11, coverage 4, integrations 19, optimization 8, services 21, tracking 9 (6 apps; todas en verde) |
| Casos del plan de pruebas obsoletos | **18** | T-INV-01…03, T-BOT-01…09, T-PAG-01…03, T-SRV-17…19: siguen en `16-plan-pruebas.md`, ninguna fila vigente los cita |

### g.2 Huecos de trazabilidad detectados

Los ítems marcados **(nuevo)** se detectaron en esta revisión; los marcados **(resuelto)** se cerraron después de detectarse y se conservan con su número para no alterar las referencias; el resto se conserva de la versión anterior, depurado de lo que solo existía por las funciones retiradas.

**RF sin prueba o con prueba incompleta**
1. **RF-03** no tiene prueba automatizada ni un caso manual propio en el plan de pruebas (T-UI-01 es "Login visual en los 4 roles" y solo comprueba la redirección al dashboard). *Corregido en la Fase 7:* 01-requerimientos.md ya no atribuye RF-03 a T-UI-01 y describe la verificación manual propuesta.
2. **RF-08**: ninguna prueba verifica que `GET /api/servicios/{id}/` incluya `novedades[]` con fecha; solo se verifica `evidencia` (T-SRV-09).
3. **RF-06**: se prueba la autenticación por API Key, pero no la creación de un servicio de punta a punta con `X-API-Key`.
4. **RF-01**: solo se prueba el listado y el RBAC; crear, editar y desactivar usuarios no tienen prueba (precisamente donde está H-08).
5. **RF-17**: los criterios (b) "día no habilitado" y (c) "zona sin cobertura" de `planificar` no tienen prueba (RN-03 y RN-15 en ese endpoint).
6. **RF-16 (resuelto, 2026-10-09)**: el código dejaba a ADMIN y ALISTADOR leer (200) y escribir (201) en el chat, algo que RF-16 no describe y que ninguna prueba cubría. `ServicioViewSet.mensajes` y `ChatConsumer._usuario_autorizado` ahora solo admiten al cliente dueño y al motorizado asignado: ADMIN y ALISTADOR reciben 403 por REST y no pueden conectarse al WebSocket (cierre 4403). Lo verifican `MensajesChatTests.test_admin_y_alistador_no_pueden_leer_ni_escribir_en_el_chat`, `MensajesChatTests.test_motorizado_no_asignado_no_puede_acceder_al_chat` y `ChatWebSocketTests.test_admin_y_alistador_no_pueden_conectarse_al_chat`. Ya no hay hueco: las rutas `servicios/:id/chat` del frontend existen solo para `cliente` y `motorizado`.
7. **RF-28 y RF-29** tienen pruebas pero **no ID `T-`** en el plan (H-05).

**RN sin prueba o con prueba parcial**
8. **RN-18** (correo único) no tiene prueba: T-ACC-07 prueba el login por correo, no la unicidad.
9. **RN-10, RN-12, RN-17**: solo se prueba el camino feliz; no se prueba asignar desde un estado distinto de `CREADO`, registrar novedad sobre un servicio cerrado ni el reemplazo de la evidencia.

**Validaciones ausentes**
10. **`planificar` no exige `direccion_origen` (nuevo)**: `PlanificarRecoleccionSerializer` es un `ModelSerializer` sobre `Servicio.direccion_origen` (`blank=True`), así que no la exige, y `ServicioViewSet.planificar` luego lee `data['direccion_origen']`. Comprobado con una ejecución puntual: sin el campo la API responde **500** (`KeyError`) y con `""` responde 201 y crea una RECOLECCION sin origen. Contradice RN-13, que solo cumple `ServicioCreateSerializer` (01 §6 ya lo precisa), y por eso RN-13 figura como Parcial en §d. La app lo evita (`shared/planificar-form.component.ts` deshabilita el envío con la dirección vacía); solo se alcanza llamando directamente a la API. Está registrado como **H-13** (01 §8) y **LIM-39** (08), y descrito en 04-mer §4.4.6; sigue sin prueba.
11. **Chat por WebSocket sin validación de longitud (nuevo)**: `MensajeChat.texto` admite 1000 caracteres y la API REST lo valida (`POST .../mensajes/` con 1001 caracteres responde 400), pero `ChatConsumer.receive` / `_guardar_mensaje` guarda el texto sin revisar la longitud (SQLite no impone el límite de `varchar`). La app del chat envía solo por REST (`servicios.service.ts:enviarMensaje`) y usa el WebSocket solo para recibir, así que la brecha solo la alcanza un cliente WebSocket directo; T-SRV-20 prueba únicamente un mensaje corto. Sigue **abierto**: no tiene ID de hallazgo propio y figura como caso sin prueba en LIM-31 (04-mer §4.4.6). 03-arquitectura §6 (flujo 4) ya describe que la app envía por REST y recibe por WebSocket.

**Proceso (BPMN) ↔ requerimientos ↔ código**
12. **Actividad sin RF:** `MT_Visita` (actividad física del motorizado; es correcto que no tenga RF ni código).
13. **RF operativos fuera del BPMN:** RF-08 (consulta del historial) pertenece a la operación del servicio pero no tiene actividad propia en el proceso. RF-15, RF-16 y RF-28 solo figuran en la anotación de comunicación `TA_Tracking` dentro del pool.
14. **H-11:** el BPMN y el backend permiten `NOVEDAD → EN_TRANSITO` (bucle REINTENTAR de `GW_AccionNovedad` a `GW_MergeTransito`), pero la app del motorizado oculta "Iniciar tránsito" y "Novedad" en ese estado (`puedeIniciarTransito`, `puedeRegistrarNovedad`). El proceso modelado no es ejecutable de punta a punta desde la interfaz.
15. **H-02 / H-04 / H-09** siguen abiertos y están anotados en el BPMN (`TA_H02`, `TA_H04`, `TA_H09b`); H-11 en `TA_Reintentar`.
16. **Gateway sin documentar (resuelto):** `GW_MergeOpt` existe en `bpmn-ciclo-servicio.bpmn` (une la salida "No" de `GW_Optimizar` y la de `ST_Optimizar` y entrega a `UT_ConsultarRuta`) y faltaba en la tabla de gateways; ya figura en 05-bpmn.md §5.

**Arquitectura / frontend**
17. **RF-28** declara como actor también al Motorizado, pero solo `features/cliente/tracking.page.ts` consume `GET /api/tracking/destino/`.
18. **RN-14 / RF-15:** `UltimaPosicionView` solo restringe al rol CLIENTE; un motorizado puede consultar la posición de servicios ajenos (06-c4.md §7, observación 7).

**Datos (MER)**
19. **Atributo sin requerimiento que lo mueva:** `RUTA.estado` (`EstadoRuta`) nunca cambia de `PLANEADA`; ningún RF ni actividad BPMN lo actualiza.

**Documentación**
20. **Plan de pruebas desactualizado (nuevo):** `16-plan-pruebas.md` conserva 18 casos de funciones retiradas (T-INV-01…03, T-BOT-01…09, T-PAG-01…03, T-SRV-17…19) y declara «93/93»; hoy hay 72 pruebas (H-05, LIM-33). Los IDs vigentes no se renumeraron, de ahí el salto T-SRV-16 → T-SRV-20.
21. **Códigos de estado del plan (nuevo):** T-SRV-06 y T-SRV-13 del plan declaran 403, pero las pruebas reales (`test_motorizado_no_asignado_no_puede_operar_el_servicio` y `test_otro_cliente_no_puede_acceder_al_chat`) verifican 404, porque el servicio ajeno no entra en el *queryset* (`get_queryset`) y no se revela su existencia. 01 §4 ya lo dice así en RF-09 («404») y en RF-16 («404»).
22. *Corregido en la Fase 7:* la anotación `TA_Reintentar` de `docs/diagrams/src/bpmn-ciclo-servicio.bpmn` usaba el ID provisional "O-01"; ahora dice "Hallazgo H-11" y el PNG/SVG se regeneraron.
