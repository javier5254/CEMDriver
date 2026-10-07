# Fase 6b — Matriz de trazabilidad

> **Objetivo:** demostrar que cada necesidad del problema se convierte en requerimientos, que esos requerimientos aparecen en el proceso (BPMN), en la arquitectura (C4), en los datos (MER) y en el código, y que el código está verificado por pruebas.
> **Insumos:** [01-requerimientos.md](01-requerimientos.md) (problema, OE-1…OE-7, RF-01…RF-29, RNF, RN-01…RN-19, hallazgos H-01…H-12), [02-stack-tecnologico.md](02-stack-tecnologico.md), [03-arquitectura.md](03-arquitectura.md) (nombres canónicos), [04-mer.md](04-mer.md) (17 entidades), [05-bpmn.md](05-bpmn.md) (IDs de actividades y gateways), [06-c4.md](06-c4.md) (N2 contenedores, N3 componentes, N4 clases de `services`), [16-plan-pruebas.md](../16-plan-pruebas.md) (IDs `T-…`).
> **Verificación:** cada endpoint, archivo, clase, función y prueba citada se comprobó contra el código actual (`backend/*/urls.py`, `views.py`, `serializers.py`, `models.py`, `tests.py`, `cmedriver/routing.py` y `frontend/src/app`). No se modificó código.

---

## a. Cómo leer la matriz

Cada fila sigue la cadena **Necesidad → Requerimiento → Proceso → Arquitectura → Datos → Código → Prueba**:

| Columna | Qué contiene | Fuente |
|---|---|---|
| **RF** | ID estable del requerimiento funcional. | 01-requerimientos.md §4 |
| **Necesidad / OE** | Problema del §1 que atiende (P1…P6) y objetivo específico (OE-1…OE-7). | 01-requerimientos.md §1 y §2.2 |
| **BPMN** | ID de la(s) actividad(es) del proceso "Ciclo de vida de un servicio" que lo ejecutan; *fuera del proceso modelado* si es configuración, autenticación o consulta transversal. | 05-bpmn.md §4–§5 |
| **C4 N2** | Contenedor(es) con nombre canónico. "App" = App CMEDriver, "API" = API REST CMEDriver, "Tiempo real" = Servicio de tiempo real. | 06-c4.md §3 |
| **C4 N3** | Componente(s) (apps Django o componentes transversales). | 06-c4.md §4 |
| **MER** | Entidad(es) que el RF lee o escribe. | 04-mer.md |
| **Código backend** | Método HTTP + ruta real y `archivo:Clase.método` (rutas relativas a `backend/`). | `urls.py`, `views.py` |
| **Frontend** | Página y servicio Angular que lo consumen (rutas relativas a `frontend/src/app/`). | `app.routes.ts`, `core/services` |
| **Prueba** | ID del plan (`T-…`) y prueba automatizada `app/tests.py::Clase.metodo`. | 16-plan-pruebas.md, `tests.py` |
| **Estado** | **Implementado** (cumple el criterio de aceptación), **Parcial** (algún criterio no se cumple; referencia al hallazgo H-xx) o **Simulado** (la arquitectura es real pero el proveedor externo es un *mock*). | Verificación en código |

Problemas del §1 de 01-requerimientos.md: **P1** asignación informal · **P2** cliente sin visibilidad · **P3** sin evidencia digital · **P4** novedades sin trazabilidad · **P5** sin autoservicio ni reglas de cobertura · **P6** sin integración con terceros.

---

## b. Cadena de alto nivel: Problema → Objetivos → RF

```
Necesidad: plataforma única para crear, asignar, ejecutar y seguir servicios de mensajería,
           con evidencia digital, seguimiento en tiempo real, autoservicio y API abierta.
```

| Problema (§1) | Objetivo específico | RF que lo cumplen |
|---|---|---|
| P1 Asignación informal, sin registro único de estados | OE-1 (configurar la operación), OE-2 (crear y asignar), OE-3 (ejecutar) | RF-01, RF-03, RF-05, RF-07, RF-09, RF-10, RF-12, RF-21, RF-26 |
| P2 Cliente sin visibilidad | OE-4 (seguimiento en tiempo real) | RF-08, RF-15, RF-16, RF-27, RF-28 |
| P3 Sin evidencia digital | OE-3 | RF-11 (+ RN-02, RN-17) |
| P4 Novedades sin trazabilidad | OE-3, OE-2 | RF-13 (+ RN-05), RF-08 |
| P5 Sin autoservicio ni reglas de cobertura | OE-1 (cobertura, inventario), OE-4 (planificar), OE-5 (chatbot y pagos) | RF-02, RF-04, RF-17, RF-18, RF-22, RF-23 (+ RN-03, RN-04, RN-15) |
| P6 Sin integración con terceros | OE-6 (API documentada, API Key, webhooks) | RF-06, RF-24, RF-25, RF-29 (+ RNF-03) |
| Transversal: acceso seguro de los 4 roles | OE-7 (seguridad y pruebas) | RF-19, RF-20 (+ RNF-01, RNF-02, RNF-07, RNF-12, RNF-17) |

Asignación de RF a objetivos (sin huecos ni duplicados): OE-1 → RF-01..04 · OE-2 → RF-05..08, RF-21, RF-26 · OE-3 → RF-09..14 · OE-4 → RF-15..17, RF-27, RF-28 · OE-5 → RF-18, RF-22, RF-23 · OE-6 → RF-24, RF-25, RF-29 · OE-7 → RF-19, RF-20. **Los 29 RF tienen objetivo y todos los objetivos tienen al menos un RF.**

---

## c. Matriz principal (una fila por RF)

### c.1 Administrador (OE-1, OE-6)

| RF | Necesidad / OE | BPMN | C4 N2 | C4 N3 | MER | Código backend | Frontend | Prueba | Estado |
|---|---|---|---|---|---|---|---|---|---|
| **RF-01** Gestionar usuarios | P1 / OE-1 | Fuera del proceso modelado (configuración) | App, API | accounts, Permisos RBAC | USUARIO | `GET/POST/PATCH/DELETE /api/usuarios/` → `accounts/views.py:UsuarioViewSet` (`IsAdmin`); `accounts/serializers.py:UsuarioSerializer` | `features/admin/usuarios-list.page.ts`, `usuario-form.page.ts`; `core/services/usuarios.service.ts` | T-ACC-04, T-ACC-05, T-ACC-06 → `accounts/tests.py::UsuariosRBACTests.test_admin_puede_listar_usuarios`, `test_no_admin_no_puede_listar_usuarios`, `test_anonimo_no_puede_listar_usuarios` | **Parcial** (H-08: el frontend desactiva con `DELETE`; crear sin contraseña usa `make_random_password()`; crear/editar/desactivar sin prueba) |
| **RF-02** Configurar matriz de cobertura | P5 / OE-1 | Fuera del proceso (configuración); sus datos los usa `ST_ValidarAgenda` | App, API | coverage | COBERTURA | `/api/cobertura/` → `coverage/views.py:CoberturaViewSet`; `GET /api/cobertura/agenda-disponible/?zona=` → `AgendaDisponibleView` | `features/admin/cobertura-list.page.ts`, `cobertura-form.page.ts`; `core/services/cobertura.service.ts` | T-COV-01…04 → `coverage/tests.py::CoberturaTests` (4 pruebas) | Implementado |
| **RF-03** Consultar panel de servicios | P1 / OE-1 | Fuera del proceso (consulta) | App, API | services | SERVICIO | `GET /api/servicios/` → `services/views.py:ServicioViewSet.get_queryset` (ADMIN sin filtro) | `features/admin/dashboard.page.ts` (`serviciosService.list()`, contador por `EstadoServicio`) | **Sin prueba automatizada**; solo verificación manual en navegador | Implementado |
| **RF-04** Gestionar inventario | P5 / OE-1 | Fuera del proceso (configuración) | API (Panel de administración Django como apoyo) | inventory | PRODUCTO | `/api/productos/` → `inventory/views.py:ProductoViewSet.get_permissions` (escritura `IsAdmin`) | **Sin pantalla de gestión**; solo lectura en `features/alistador/servicio-form.page.ts` vía `core/services/productos.service.ts` | T-INV-01, T-INV-02 → `inventory/tests.py::InventarioTests.test_solo_admin_puede_crear_producto`, `test_alistador_puede_leer_catalogo_para_asociar_a_servicios` | **Parcial** (H-08 sin pantalla; H-03 el plan dice que el Alistador crea) |
| **RF-24** Generar API Keys | P6 / OE-6 | Fuera del proceso (configuración); habilita `ST_AutenticarKey` | App, API | integrations, Autenticación por API Key | API_KEY, USUARIO | `/api/integraciones/api-keys/` → `integrations/views.py:ApiKeyViewSet.create`; `integrations/serializers.py:ApiKeyCreateSerializer.validate_actua_como` | `features/admin/api-keys-list.page.ts`; `core/services/api-keys.service.ts` | T-INT-01, T-INT-02, T-INT-03 → `integrations/tests.py::ApiKeyEndpointTests` (6), `ApiKeyAuthenticationTests` (4) | Implementado |
| **RF-25** Configurar webhooks | P6 / OE-6 | `SND_WebhookCreado`, `SND_WebhookAsignado`, `SND_WebhookEntregado`, `SND_WebhookRecolectado`, `SND_WebhookNovedad`, `SND_WebhookDevuelto` | App, API | integrations, Despachador de webhooks | WEBHOOK_ENDPOINT, WEBHOOK_DELIVERY | `/api/integraciones/webhooks/` → `integrations/views.py:WebhookEndpointViewSet`; envío: `integrations/services.py:disparar_webhook`, `firmar`, `_enviar_a_endpoint`; invocado por `services/views.py:ServicioViewSet._notificar` | `features/admin/webhooks-list.page.ts`; `core/services/webhooks.service.ts` | T-INT-01, T-INT-04, T-INT-05 → `integrations/tests.py::WebhookEndpointTests`, `DispararWebhookTests` (5) | Implementado (H-09: `recibir-en-centro`, `iniciar-transito` y la compra por chatbot no emiten evento) |
| **RF-29** Consultar bitácora de webhooks | P6 / OE-6 | Fuera del proceso (consulta de lo registrado por `SND_Webhook*`) | App, API | integrations | WEBHOOK_DELIVERY | `GET /api/integraciones/webhooks/{endpoint_id}/entregas/` → `integrations/views.py:WebhookEntregasView` | `features/admin/webhooks-list.page.ts` (`webhooksService.entregas`) | Sin ID T- (H-05) → `integrations/tests.py::WebhookEndpointTests.test_entregas_endpoint_lista_bitacora_solo_para_admin` | Implementado |

### c.2 Alistador y sistema integrador (OE-2)

| RF | Necesidad / OE | BPMN | C4 N2 | C4 N3 | MER | Código backend | Frontend | Prueba | Estado |
|---|---|---|---|---|---|---|---|---|---|
| **RF-05** Crear servicio manual | P1 / OE-2 | `UT_Registrar`, `ST_ValidarDatos`, `GW_DatosValidos`, `ST_RegistrarCreado`, `SND_WebhookCreado` | App, API | services, Permisos RBAC | SERVICIO, USUARIO, PRODUCTO | `POST /api/servicios/` → `services/views.py:ServicioViewSet.create` / `perform_create`; `services/serializers.py:ServicioCreateSerializer.validate` | `features/alistador/servicio-form.page.ts`; `servicios.service.ts:create` | T-SRV-01…04 → `services/tests.py::CrearServicioTests` (4) | Implementado (H-04: no valida cobertura ni leadtime) |
| **RF-06** Crear servicio vía API externa | P6 / OE-2 | `SE_API`, `ST_AutenticarKey`, `GW_KeyValida`, `EE_Rechazo401`, luego el mismo camino de RF-05 | API, Documentación API | Autenticación por API Key, services | API_KEY, SERVICIO | `POST /api/servicios/` con `X-API-Key` → `integrations/authentication.py:ApiKeyAuthentication.authenticate` → `ApiKey.autenticar()` → `ServicioViewSet.create`; contrato en `GET /api/schema/`, `/api/docs/` | No aplica (actor externo) | T-INT-03 → `integrations/tests.py::ApiKeyAuthenticationTests` (4) | Implementado (sin prueba de punta a punta de `POST /api/servicios/` con API Key) |
| **RF-07** Crear ruta y asignar servicio | P1 / OE-2 | `UT_AsignarRuta`, `ST_PasarAsignado`, `SND_WebhookAsignado` | App, API | services, Despachador de webhooks | RUTA, SERVICIO | `POST /api/rutas/` → `services/views.py:RutaViewSet`; `POST /api/servicios/{id}/asignar-ruta/` → `ServicioViewSet.asignar_ruta` (`AsignarRutaSerializer`) | `features/alistador/ruta-form.page.ts`, `servicios-list.page.ts`; `rutas.service.ts:create`, `servicios.service.ts:asignarRuta` | T-SRV-05 → `services/tests.py::CicloDeVidaEntregaTests.test_flujo_completo_entrega` | Implementado |
| **RF-08** Consultar estado e historial de novedades | P2, P4 / OE-2 | Fuera del proceso modelado (consulta); la "reasignación" no existe | App, API | services | SERVICIO, NOVEDAD, EVIDENCIA | `GET /api/servicios/{id}/` → `ServicioViewSet.retrieve` con `services/serializers.py:ServicioSerializer` (`novedades[]`, `evidencia`) | Estado en `features/alistador/servicios-list.page.ts`; el historial de novedades solo se muestra en `features/motorizado/servicio-detail.page.ts` | Indirecta: T-SRV-09 (`CicloDeVidaRecoleccionTests.test_cerrar_con_evidencia_completa` verifica `evidencia`); ninguna prueba verifica `novedades[]` | **Parcial** (H-08: reasignar no implementado) |
| **RF-21** Sugerir orden de ruta | P1 / OE-2 | `GW_Optimizar`, `UT_PedirOrden`, `ST_Optimizar` (+ flujos `MF05`/`MF06` con Nominatim) | App, API | optimization, Cliente de geocodificación | RUTA, SERVICIO, PUNTO_GEOCODIFICADO | `POST /api/optimizacion/rutas/{ruta_id}/` → `optimization/views.py:OptimizarRutaView.post`; `optimization/geocoding.py:geocodificar`; `optimization/heuristica.py:ordenar_nearest_neighbor`, `haversine_km` | `features/alistador/optimizar-ruta.page.ts`; `optimizacion.service.ts:optimizar` | T-OPT-01…04 → `optimization/tests.py::OptimizarRutaTests` (8) | Implementado (alcance RES-13) |
| **RF-26** Asociar varios productos a un servicio | P1 / OE-2 | Fuera del proceso modelado | API | services | SERVICIO_PRODUCTO, PRODUCTO | `PUT /api/servicios/{id}/productos/` → `ServicioViewSet.productos` (`ServicioProductoItemSerializer`) | **Sin pantalla ni método en `servicios.service.ts`** (solo API) | T-SRV-17…19 → `services/tests.py::ServicioProductoTests` (3) | Implementado (solo por API) |

### c.3 Motorizado (OE-3)

| RF | Necesidad / OE | BPMN | C4 N2 | C4 N3 | MER | Código backend | Frontend | Prueba | Estado |
|---|---|---|---|---|---|---|---|---|---|
| **RF-09** Ver servicios asignados | P1 / OE-3 | `UT_ConsultarRuta` | App, API | services | SERVICIO, RUTA | `GET /api/servicios/` → `ServicioViewSet.get_queryset` (`ruta__motorizado=user`); `GET /api/rutas/` → `RutaViewSet.get_queryset` | `features/motorizado/servicios-list.page.ts` | T-SRV-06 → `services/tests.py::CicloDeVidaEntregaTests.test_motorizado_no_asignado_no_puede_operar_el_servicio` | Implementado |
| **RF-10** Recibir en centro (Entrega) | P1 / OE-3 | `GW_TipoServicio`, `UT_RecibirCentro`, `ST_PasarRecibido` | App, API | services | SERVICIO | `POST /api/servicios/{id}/recibir-en-centro/` → `ServicioViewSet.recibir_en_centro` (+ `_motorizado_autorizado`) | `features/motorizado/servicio-detail.page.ts` (botón si `ENTREGA` y `ASIGNADO`); `servicios.service.ts:recibirEnCentro` | T-SRV-05, T-SRV-07 → `CicloDeVidaEntregaTests.test_flujo_completo_entrega`, `test_recibir_en_centro_no_aplica_a_recoleccion` | Implementado (H-02: un REINTENTAR permite saltarse el centro) |
| **RF-11** Capturar evidencia (Recolección) | P3 / OE-3 | `UT_Evidencia`, `ST_ValidarEvidencia`, `GW_EvidenciaOK`, `ST_PasarRecolectado`, `SND_WebhookRecolectado`, `EE_Recolectado` | App, API, Almacenamiento de evidencias | services, Despachador de webhooks | EVIDENCIA, SERVICIO | `POST /api/servicios/{id}/cerrar/` (multipart) → `ServicioViewSet.cerrar`; `services/serializers.py:CerrarServicioSerializer.validate`; `services/models.py:Evidencia` | `features/motorizado/servicio-detail.page.ts` (`<input capture="environment">`, `SignaturePad`); `servicios.service.ts:cerrar(id, {foto, firma})` | T-SRV-08, T-SRV-09 → `services/tests.py::CicloDeVidaRecoleccionTests.test_cerrar_sin_evidencia_falla`, `test_cerrar_con_evidencia_completa`; T-UI-02, T-UI-03 (manual) | Implementado |
| **RF-12** Iniciar tránsito y cerrar servicio | P1 / OE-3 | `UT_IniciarTransito`, `ST_PasarTransito`, `GW_MergeTransito`, `UT_ConfirmarEntrega`, `ST_PasarEntregado`, `SND_WebhookEntregado`, `EE_Entregado` | App, API | services, Despachador de webhooks | SERVICIO | `POST /api/servicios/{id}/iniciar-transito/` → `ServicioViewSet.iniciar_transito`; `POST /api/servicios/{id}/cerrar/` → `ServicioViewSet.cerrar` | `features/motorizado/servicio-detail.page.ts` (`puedeIniciarTransito`); `servicios.service.ts:iniciarTransito`, `cerrar` | T-SRV-05, T-SRV-09 → `CicloDeVidaEntregaTests.test_flujo_completo_entrega`, `CicloDeVidaRecoleccionTests.test_cerrar_con_evidencia_completa` | Implementado |
| **RF-13** Registrar novedad | P4 / OE-3 | `GW_Resultado`, `UT_RegistrarNovedad`, `ST_GuardarNovedad`, `GW_AccionNovedad`, `SND_WebhookNovedad`, `SND_WebhookDevuelto`, `EE_Devuelto` | App, API | services, Despachador de webhooks | NOVEDAD, SERVICIO | `POST /api/servicios/{id}/novedad/` → `ServicioViewSet.novedad`; `services/serializers.py:NovedadCreateSerializer`; `services/models.py:Novedad.Accion` | `features/motorizado/servicio-detail.page.ts` (`puedeRegistrarNovedad`); `servicios.service.ts:novedad` | T-SRV-10, T-SRV-11 → `services/tests.py::NovedadTests.test_reintentar_deja_en_novedad_y_permite_reintentar_transito`, `test_devolver_deja_servicio_terminal` | **Parcial** (H-11: tras REINTENTAR la app no permite reanudar) |
| **RF-14** Reportar posición GPS | P2 / OE-3 | `PG_Inicio`, `ST_EnviarGPS`, `IE_Cada8s`, `GW_SigueTransito`, `ST_DifundirGPS`, `PG_Fin` | App, API, Tiempo real, Capa de canales | tracking, TrackingConsumer | POSICION_GPS | `POST /api/tracking/posicion/` → `tracking/views.py:ReportarPosicionView.post` (`IsMotorizado`, `group_send('tracking_<id>')`) | `features/motorizado/servicio-detail.page.ts:startTracking` (`watchPosition` + `setInterval 8000`); `tracking.service.ts:postPosicion` | T-TRK-01, T-TRK-02 → `tracking/tests.py::TrackingTests.test_motorizado_asignado_puede_reportar_posicion`, `test_motorizado_no_asignado_no_puede_reportar_posicion`; T-UI-04 (manual) | Implementado (nota 4: el backend no exige `EN_TRANSITO`) |

### c.4 Cliente (OE-4, OE-5)

| RF | Necesidad / OE | BPMN | C4 N2 | C4 N3 | MER | Código backend | Frontend | Prueba | Estado |
|---|---|---|---|---|---|---|---|---|---|
| **RF-15** Ver tracking del motorizado | P2 / OE-4 | Fuera de las actividades (anotación de comunicación dentro del pool, 05-bpmn §7) | App, API | tracking | POSICION_GPS, SERVICIO | `GET /api/tracking/ultima-posicion/?servicio_id=` → `tracking/views.py:UltimaPosicionView.get` | `features/cliente/tracking.page.ts` (Leaflet); `tracking.service.ts:ultimaPosicion` | T-TRK-03, T-TRK-04 → `tracking/tests.py::TrackingTests.test_cliente_dueno_puede_ver_ultima_posicion`, `test_otro_cliente_no_puede_ver_la_posicion` | Implementado |
| **RF-16** Chatear con el motorizado | P2 / OE-4 | Fuera de las actividades (anotación `ws/chat/{id}/`, 05-bpmn §7) | App, API, Tiempo real | services, ChatConsumer | MENSAJE_CHAT, SERVICIO | `GET/POST /api/servicios/{id}/mensajes/` → `ServicioViewSet.mensajes`; `services/serializers.py:MensajeChatSerializer` | `shared/chat.page.ts` (rutas `cliente/servicios/:id/chat` y `motorizado/servicios/:id/chat`); `servicios.service.ts:mensajes`, `enviarMensaje` | T-SRV-12…14 → `services/tests.py::MensajesChatTests` (3) | Implementado |
| **RF-17** Planificar recolección propia | P5 / OE-4 | `SE_Cliente`, `GW_QueSolicita`, `UT_Planificar`, `ST_ValidarAgenda`, `GW_AgendaValida`, `EE_RechazoAgenda`, `ST_RegistrarCreado`, `SND_WebhookCreado` | App, API | services, coverage | SERVICIO, COBERTURA | `POST /api/servicios/planificar/` → `ServicioViewSet.planificar` (`PlanificarRecoleccionSerializer`, `Cobertura`, `DIAS_ORDEN`); agenda: `GET /api/cobertura/agenda-disponible/` | `features/cliente/planificar.page.ts` + `shared/planificar-form.component.ts`; `servicios.service.ts:planificar`, `cobertura.service.ts:agendaDisponible` | T-SRV-15, T-SRV-16 → `services/tests.py::PlanificarRecoleccionTests.test_planificar_respeta_leadtime`, `test_planificar_fecha_valida_crea_recoleccion` | Implementado (criterios "día no habilitado" y "zona sin cobertura" sin prueba) |
| **RF-18** Usar chatbot guiado con catálogo | P5 / OE-5 | `UT_Comprar` (menú y catálogo) | App, API | chatbot, inventory | PRODUCTO, CONVERSACION, MENSAJE_BOT | `POST /api/chatbot/mensaje/` → `chatbot/views.py:MensajeChatbotView`; `chatbot/llm.py:tool_listar_productos`; `GET /api/productos/disponibles-chatbot/` → `inventory/views.py:ProductosDisponiblesChatbotView` | `features/cliente/chatbot.page.ts`; `chatbot.service.ts:enviarMensaje` (`productos.service.ts:disponiblesChatbot` existe pero ninguna página lo usa) | T-BOT-01, T-INV-03 → `chatbot/tests.py::ChatbotSaludoYFallbackTests.test_saludo_ofrece_el_menu_de_opciones`, `inventory/tests.py::InventarioTests.test_productos_disponibles_chatbot_filtra_por_stock_y_flag` | Implementado |
| **RF-22** Chatbot en lenguaje libre | P5 / OE-5 | `UT_Comprar`, `UT_Planificar` (vía chatbot) | App, API | chatbot (→ services, coverage) | CONVERSACION, MENSAJE_BOT, SERVICIO, COBERTURA | `POST /api/chatbot/mensaje/` → `MensajeChatbotView.post` → `chatbot/llm.py:MockLLMClient.responder`, `tool_consultar_agenda`, `tool_crear_recoleccion`; `GET /api/chatbot/conversaciones/{id}/mensajes/` → `ConversacionMensajesView` | `features/cliente/chatbot.page.ts`; `chatbot.service.ts:enviarMensaje`, `historial` | T-BOT-01…09 → `chatbot/tests.py::ChatbotSaludoYFallbackTests` (3), `ChatbotRecoleccionTests` (3), `ChatbotComprarTests` (3), `ChatbotPermisosTests` (3) | **Simulado** (`MockLLMClient`, RES-06; H-04) |
| **RF-23** Generar pago al comprar por chatbot | P5 / OE-5 | `UT_Comprar`, `ST_CrearCompra` | App, API | chatbot, payments | PAGO, SERVICIO, PRODUCTO | `chatbot/llm.py:tool_crear_compra` → `payments/provider.py:obtener_proveedor_pago().procesar` (`MockPaymentProvider`); `GET /api/pagos/{pk}/` → `payments/views.py:PagoDetailView` | `features/cliente/chatbot.page.ts` (insignia `Pago APROBADO/RECHAZADO`); **sin pantalla que consulte `/api/pagos/{id}/`** | T-BOT-04, T-PAG-01…03 → `chatbot/tests.py::ChatbotComprarTests.test_flujo_completo_de_compra_crea_servicio_y_pago`, `payments/tests.py::MockPaymentProviderTests` (4), `PagoDetailViewTests` (5) | **Simulado** (`MockPaymentProvider`, RES-07; H-09, H-12) |
| **RF-27** Tracking y chat en tiempo real | P2 / OE-4 | `ST_DifundirGPS` (+ anotaciones de `ws/tracking` y `ws/chat`) | App, Tiempo real, Capa de canales | Middleware JWT de WebSocket, TrackingConsumer, ChatConsumer | POSICION_GPS, MENSAJE_CHAT | `ws/tracking/{servicio_id}/` → `tracking/consumers.py:TrackingConsumer`; `ws/chat/{servicio_id}/` → `services/consumers.py:ChatConsumer` (`cmedriver/routing.py`); `cmedriver/ws_auth.py:JWTAuthMiddleware` | `tracking.service.ts:conectarTracking` + respaldo `POLL_FALLBACK_MS = 8000` en `features/cliente/tracking.page.ts`; `shared/chat.page.ts` (WebSocket + `POLL_FALLBACK_MS = 5000`) | T-SRV-20, T-SRV-21, T-TRK-05, T-TRK-06 → `services/tests.py::ChatWebSocketTests` (2), `tracking/tests.py::TrackingWebSocketTests` (2) | Implementado |
| **RF-28** Ver destino y ETA en el mapa | P2 / OE-4 | Fuera de las actividades (consulta de apoyo al tracking) | App, API | tracking, Cliente de geocodificación | PUNTO_GEOCODIFICADO, SERVICIO | `GET /api/tracking/destino/?servicio_id=` → `tracking/views.py:DestinoView` (usa `optimization/geocoding.py:geocodificar`) | `features/cliente/tracking.page.ts` (`obtenerDestino`, `etaMinutos`); el motorizado no lo consume en su app | Sin ID T- (H-05) → `tracking/tests.py::DestinoTests` (3) | Implementado (en la app solo para el Cliente) |

### c.5 Todos los usuarios (OE-7)

| RF | Necesidad / OE | BPMN | C4 N2 | C4 N3 | MER | Código backend | Frontend | Prueba | Estado |
|---|---|---|---|---|---|---|---|---|---|
| **RF-19** Iniciar sesión con usuario o correo | Transversal / OE-7 | Fuera del proceso modelado (precondición de todos los lanes) | App, API | accounts, Autenticación JWT | USUARIO | `POST /api/auth/login/` → `accounts/views.py:LoginView` (`CMEDriverTokenObtainPairSerializer.validate`); `POST /api/auth/refresh/` → `TokenRefreshView`; `GET /api/auth/me/` → `MeView` | `features/auth/login.page.ts`; `auth.service.ts:login`, `refreshToken`; `core/interceptors/auth.interceptor.ts`; `core/guards/auth.guard.ts`, `role.guard.ts` | T-ACC-01, 02, 03, 07 → `accounts/tests.py::AuthTests` (4) | Implementado |
| **RF-20** Restablecer contraseña por correo | Transversal / OE-7 | Fuera del proceso modelado | App, API (+ Servidor SMTP externo) | accounts | USUARIO | `POST /api/auth/password-reset/` → `PasswordResetRequestView`; `POST /api/auth/password-reset/confirm/` → `PasswordResetConfirmView` | `features/auth/forgot-password.page.ts`, `reset-password.page.ts`; `auth.service.ts:requestPasswordReset`, `confirmPasswordReset` | T-ACC-08…11 → `accounts/tests.py::PasswordResetTests` (4) | Implementado (correo por consola en desarrollo, RES-08) |

---

## d. Matriz de reglas de negocio (RN-01…RN-19)

| RN | Gateway / actividad BPMN | Dónde se aplica en código (`backend/`) | Entidad.campo (MER) | Prueba | Estado |
|---|---|---|---|---|---|
| RN-01 Entrega inicia en centro | `GW_TipoServicio`, `ST_PasarRecibido`, `ST_PasarTransito` | `services/views.py:ServicioViewSet.recibir_en_centro`, `iniciar_transito` (`estados_validos_por_tipo`) | SERVICIO.tipo, SERVICIO.estado | T-SRV-05, T-SRV-07 | **Parcial** (H-02) |
| RN-02 Evidencia obligatoria en Recolección | `ST_ValidarEvidencia`, `GW_EvidenciaOK` | `services/serializers.py:CerrarServicioSerializer.validate`; `views.py:ServicioViewSet.cerrar` | EVIDENCIA.foto, EVIDENCIA.firma | T-SRV-08, T-SRV-09 | Implementado |
| RN-03 Leadtime y días hábiles | `ST_ValidarAgenda`, `GW_AgendaValida`, `EE_RechazoAgenda` | `services/views.py:ServicioViewSet.planificar`; `coverage/views.py:AgendaDisponibleView`; `chatbot/llm.py:tool_consultar_agenda`, `tool_crear_recoleccion` | COBERTURA.leadtime_dias, COBERTURA.dias_disponibles, SERVICIO.fecha_agenda | T-SRV-15, T-COV-03, T-BOT-05 | **Parcial** (H-04: no aplica a creación manual, API Key ni compra) |
| RN-04 Producto visible en chatbot | `UT_Comprar`, `ST_CrearCompra` | `inventory/views.py:ProductosDisponiblesChatbotView.get`; `chatbot/llm.py:tool_listar_productos`, `tool_crear_compra` | PRODUCTO.disponible_chatbot, PRODUCTO.stock | T-INV-03 | Implementado |
| RN-05 Novedad con acción | `GW_AccionNovedad`, `ST_GuardarNovedad` | `services/models.py:Novedad.Accion`; `views.py:ServicioViewSet.novedad`; `serializers.py:NovedadCreateSerializer` | NOVEDAD.accion | T-SRV-10, T-SRV-11 | Implementado |
| RN-06 Producto protegido | Fuera del proceso modelado | `services/models.py:ServicioProducto.producto` (`on_delete=PROTECT`) | SERVICIO_PRODUCTO.producto_id | **Sin prueba** | Implementado |
| RN-07 Webhook por suscripción | `SND_Webhook*` (6 tareas) | `integrations/models.py:WebhookEndpoint.suscrito_a`; `integrations/services.py:disparar_webhook` | WEBHOOK_ENDPOINT.activo, WEBHOOK_ENDPOINT.eventos | `integrations/tests.py::DispararWebhookTests.test_evento_no_suscrito_no_genera_entrega`, `test_endpoint_inactivo_no_recibe_webhooks` | Implementado |
| RN-08 API Key actúa como Alistador | `ST_AutenticarKey`, `GW_KeyValida`, `EE_Rechazo401` | `integrations/serializers.py:ApiKeyCreateSerializer.validate_actua_como`; `integrations/authentication.py:ApiKeyAuthentication.authenticate`; `models.py:ApiKey.autenticar` | API_KEY.actua_como, API_KEY.activa | `ApiKeyEndpointTests.test_actua_como_debe_ser_alistador`, T-INT-03 | Implementado |
| RN-09 Ciclo de vida del servicio | `ST_PasarAsignado`, `ST_PasarRecibido`, `ST_PasarTransito`, `ST_PasarEntregado`, `ST_PasarRecolectado`, `ST_GuardarNovedad`, `GW_MergeTransito` | Acciones de `services/views.py:ServicioViewSet`; `serializers.py:ServicioSerializer` (`estado` de solo lectura) | SERVICIO.estado (`EstadoServicio`) | T-SRV-05, T-SRV-09, T-SRV-10, T-SRV-11 | **Parcial** (H-02 en backend; H-11 en la app) |
| RN-10 Asignación solo desde CREADO | `ST_PasarAsignado` | `services/views.py:ServicioViewSet.asignar_ruta` | SERVICIO.estado, SERVICIO.ruta_id | T-SRV-05 (camino feliz; el rechazo 400 no se prueba) | Implementado |
| RN-11 Solo el motorizado asignado opera | `UT_ConsultarRuta`, `ST_PasarRecibido`, `UT_IniciarTransito`, `ST_EnviarGPS` | `services/views.py:ServicioViewSet._motorizado_autorizado`, `get_queryset`; `tracking/views.py:ReportarPosicionView` | RUTA.motorizado_id, SERVICIO.ruta_id | T-SRV-06, T-TRK-02 | Implementado |
| RN-12 Estados terminales | `ST_PasarEntregado`, `ST_GuardarNovedad`, fines `EE_Entregado`/`EE_Recolectado`/`EE_Devuelto` | `services/views.py:ServicioViewSet.novedad`, `cerrar` | SERVICIO.estado | T-SRV-11 (cerrar tras `DEVUELTO`); novedad sobre servicio cerrado sin prueba | Implementado |
| RN-13 Dirección según tipo | `ST_ValidarDatos`, `GW_DatosValidos`, `EE_Rechazo400` | `services/serializers.py:ServicioCreateSerializer.validate`; `PlanificarRecoleccionSerializer` | SERVICIO.direccion_destino, SERVICIO.direccion_origen | T-SRV-02, T-SRV-03 | Implementado |
| RN-14 Visibilidad por propietario | Fuera del proceso (transversal a todos los lanes) | `services/views.py:ServicioViewSet.get_queryset`, `mensajes`; `services/consumers.py:ChatConsumer`; `tracking/consumers.py:TrackingConsumer`; `tracking/views.py`; `chatbot/views.py:ConversacionMensajesView`; `payments/views.py:PagoDetailView` | SERVICIO.cliente_id, RUTA.motorizado_id, CONVERSACION.cliente_id, PAGO.cliente_id | T-SRV-13, T-SRV-21, T-TRK-04, T-TRK-06, T-BOT-08, T-PAG-03 | **Parcial** (H-01; `UltimaPosicionView` no restringe al motorizado, 06-c4 §7.7) |
| RN-15 Zona con cobertura | `ST_ValidarAgenda`, `GW_AgendaValida` | `coverage/models.py:Cobertura.zona` (`unique`); `services/views.py:ServicioViewSet.planificar`; `coverage/views.py:AgendaDisponibleView` | COBERTURA.zona | T-COV-04 (agenda); el 400 de `planificar` sin prueba | Implementado |
| RN-16 Resultado de pago | `ST_CrearCompra` | `payments/provider.py:MockPaymentProvider.procesar`; `payments/models.py:Pago.referencia` (`unique`) | PAGO.estado, PAGO.referencia | T-PAG-01, T-PAG-02 | **Simulado** (H-12: el servicio no depende del resultado) |
| RN-17 Una evidencia por servicio | `ST_PasarRecolectado` | `services/models.py:Evidencia.servicio` (`OneToOneField`); `views.py:ServicioViewSet.cerrar` (`update_or_create`) | EVIDENCIA.servicio_id (UK) | T-SRV-09 (creación); el reemplazo no se prueba | Implementado |
| RN-18 Correo único | Fuera del proceso modelado | `accounts/models.py:Usuario.email` (`unique=True`) | USUARIO.email | **Sin prueba de duplicado** (T-ACC-07 prueba el login por correo, no la unicidad) | Implementado |
| RN-19 Reset sin enumeración | Fuera del proceso modelado | `accounts/views.py:PasswordResetRequestView.post` | USUARIO.email | T-ACC-09 | Implementado |

---

## e. Matriz RNF principales → decisión de stack/arquitectura → evidencia

| RNF | Decisión de stack / arquitectura | Dónde está en el C4 | Evidencia verificable |
|---|---|---|---|
| RNF-01 JWT | SimpleJWT (access 8 h, refresh 1 día); JWT también para WebSocket | N3 Autenticación JWT, Middleware JWT de WebSocket | `cmedriver/settings.py` (`SIMPLE_JWT`, `DEFAULT_AUTHENTICATION_CLASSES`); `cmedriver/ws_auth.py:JWTAuthMiddleware`; T-ACC-01, T-ACC-06 |
| RNF-02 RBAC | Rol en `Usuario.rol` + clases de permiso por vista + filtrado en `get_queryset` | N3 Permisos RBAC | `accounts/permissions.py`; `ServicioViewSet.get_permissions`; T-ACC-05, T-SRV-01, T-SRV-19, T-OPT-01, T-BOT-09, T-INT-01 (⚠️ H-01) |
| RNF-03 API documentada | drf-spectacular (OpenAPI 3 + Swagger UI) | N2 Documentación API | `GET /api/schema/`, `GET /api/docs/` en `cmedriver/urls.py`; inspección manual |
| RNF-07 / RNF-12 Credenciales con hash | `set_password()` (PBKDF2); API Key guardada como SHA-256 + prefijo | N3 accounts, Autenticación por API Key | `integrations/models.py:ApiKey.key_hash`, `prefix`; T-ACC-10, T-INT-02 |
| RNF-08 Modularidad | Monolito modular de 9 apps Django (decisión §8 de 03-arquitectura) | N3: 9 componentes | Estructura `backend/<app>/{models,serializers,views,urls,tests}.py` |
| RNF-10 / RNF-16 Tiempo real y resiliencia | Django Channels + Daphne en el mismo proceso ASGI; polling de respaldo en el frontend | N2 Servicio de tiempo real, Capa de canales | `cmedriver/asgi.py`, `cmedriver/routing.py`; `POLL_FALLBACK_MS` 8000/5000 en `tracking.page.ts`/`chat.page.ts`; T-SRV-20, T-TRK-05 |
| RNF-11 Webhooks firmados *best-effort* | HMAC-SHA256 en `X-CMEDriver-Signature`, timeout por endpoint, nunca propaga errores | N3 Despachador de webhooks | `integrations/services.py:firmar`, `_enviar_a_endpoint` (`urlopen(..., timeout=...)`); T-INT-04, T-INT-05 |
| RNF-13 Proveedores intercambiables | Patrón Strategy: `PaymentProvider` / `MockPaymentProvider`, `MockLLMClient` | N1/N2 Proveedor de pagos y Proveedor LLM (simulados); N3 payments, chatbot | `payments/provider.py:obtener_proveedor_pago`; `chatbot/llm.py:MockLLMClient`; T-PAG-01, T-BOT-* |
| RNF-15 Tolerancia a fallos externos | Geocodificación con caché y salida controlada; *fallback* del chatbot | N3 Cliente de geocodificación, chatbot | T-OPT-03, T-BOT-02, T-INT-05, `tracking/tests.py::DestinoTests.test_geocoding_fallido_devuelve_404_no_500` |
| RNF-05 / RNF-14 Usabilidad móvil y portabilidad | Ionic 9 + Angular 22 (tema iOS) y Capacitor 8 | N2 App CMEDriver | T-UI-05 (manual); build Android no verificado (RES-14) |
| RNF-06 Frecuencia GPS | Intervalo fijo de 8 s en la app | N2 App CMEDriver | `features/motorizado/servicio-detail.page.ts:startTracking` (`setInterval(..., 8000)`); BPMN `IE_Cada8s` |
| RNF-17 Suite de pruebas | Django test runner + `APIClient`, BD aislada | — | 96 métodos `test_*` en 9 `tests.py`; `run_tests.ps1` / `run_tests.sh` (⚠️ H-05: el plan dice 93) |
| RNF-18 Configuración segura | Variables de entorno; arranque bloqueado sin `DJANGO_SECRET_KEY` en producción | N2 nodo Servidor ASGI Daphne | `cmedriver/settings.py` (`RuntimeError` si `DEBUG=False` sin clave) |
| RNF-20 Privacidad | Filtrado por propietario (RN-14) | N3 Permisos RBAC + `get_queryset` | T-SRV-13, T-TRK-04, T-BOT-08, T-PAG-03 (⚠️ H-01, H-07, RES-11) |

---

## f. Ejemplo narrado de punta a punta: RF-11 "Capturar evidencia" + RN-02

Este recorrido sirve para la sustentación porque toca todas las capas con un requerimiento de prioridad Alta.

1. **Necesidad (P3).** Las recolecciones no dejan prueba verificable, lo que dificulta resolver reclamos. → **Objetivo OE-3**: el Motorizado ejecuta el servicio con flujo diferenciado y *recolectar con foto y firma*.
2. **Requerimiento.** **RF-11**: "El sistema debe exigir una foto del producto y una firma digital del cliente para cerrar un servicio de RECOLECCION y almacenarlas como `Evidencia`". Lo refuerzan **RN-02** (sin foto **y** firma no se cierra) y **RN-17** (máximo una evidencia por servicio).
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

| Indicador | Valor | Detalle |
|---|---|---|
| RF con objetivo específico (OE) | **29 / 29 (100 %)** | Ver §b |
| RF con al menos una prueba automatizada específica | **27 / 29 (93 %)** | Sin prueba específica: RF-03 (ninguna) y RF-08 (solo indirecta) |
| RF con alguna prueba automatizada (incluida indirecta) | **28 / 29 (97 %)** | Solo RF-03 depende de verificación manual |
| RF que aparecen como actividad en el BPMN | **16 / 29 (55 %)** | RF-05, 06, 07, 09, 10, 11, 12, 13, 14, 17, 18, 21, 22, 23, 25, 27 |
| RF fuera del proceso modelado | **13 / 29** | RF-01, 02, 03, 04, 08, 15, 16, 19, 20, 24, 26, 28, 29 (configuración, autenticación y consultas; RF-15 y RF-16 aparecen solo como anotaciones y RF-02 como dato de `ST_ValidarAgenda`) |
| RF con componente C4 N3 y entidad MER | **29 / 29** | Toda fila de §c tiene ambos |
| Entidades MER usadas por al menos un RF | **17 / 17** | Ninguna entidad huérfana |
| RF con pantalla en el frontend | **26 / 29** | Sin pantalla: RF-04 (la gestión del catálogo; solo hay lectura), RF-06 (actor externo, no aplica) y RF-26. Parciales en la UI: RF-23 (no hay consulta del pago) y RF-28 (solo para el Cliente) |
| Estado de los RF | **23 Implementado · 4 Parcial · 2 Simulado** | Parcial: RF-01 (H-08), RF-04 (H-08, H-03), RF-08 (H-08), RF-13 (H-11). Simulado: RF-22, RF-23 (H-12) |
| RN con prueba automatizada | **17 / 19** | Sin prueba: RN-06, RN-18 |
| RN con punto en el BPMN | **15 / 19** | Fuera del proceso: RN-06, RN-14, RN-18, RN-19 |
| Estado de las RN | **14 Implementado · 4 Parcial · 1 Simulado** | Parcial: RN-01 (H-02), RN-03 (H-04), RN-09 (H-02, H-11), RN-14 (H-01). Simulado: RN-16 |
| Pruebas automatizadas existentes | **96 métodos `test_*`** | accounts 11, chatbot 12, coverage 4, integrations 19, inventory 3, optimization 8, payments 9, services 21, tracking 9 |

### g.2 Huecos de trazabilidad detectados

**RF sin prueba o con prueba incompleta**
1. **RF-03** no tiene prueba automatizada. Además, 01-requerimientos.md la vincula a T-UI-01, pero en el plan T-UI-01 es "Login visual en los 4 roles": la referencia no corresponde.
2. **RF-08**: ninguna prueba verifica que `GET /api/servicios/{id}/` incluya `novedades[]` con fecha; solo se verifica `evidencia` (T-SRV-09).
3. **RF-06**: se prueba la autenticación por API Key, pero no la creación de un servicio de punta a punta con `X-API-Key`.
4. **RF-01**: solo se prueba el listado y el RBAC; crear, editar y desactivar usuarios no tienen prueba (precisamente donde está H-08).
5. **RF-17**: los criterios (b) "día no habilitado" y (c) "zona sin cobertura" de `planificar` no tienen prueba (RN-03 y RN-15 en ese endpoint).
6. **RF-28 y RF-29** tienen pruebas pero **no ID `T-`** en el plan (H-05).

**RN sin prueba o con prueba parcial**
7. **RN-06** (producto protegido) y **RN-18** (correo único) no tienen prueba.
8. **RN-10, RN-12, RN-17**: solo se prueba el camino feliz; no se prueba asignar desde un estado distinto de `CREADO`, registrar novedad sobre un servicio cerrado ni el reemplazo de la evidencia.

**Proceso (BPMN) ↔ requerimientos ↔ código**
9. **Actividad sin RF:** `MT_Visita` (actividad física del motorizado; es correcto que no tenga RF ni código).
10. **RF operativos fuera del BPMN:** RF-08 (consulta del historial) y RF-26 (líneas de producto) pertenecen a la operación del servicio pero no tienen actividad propia en el proceso. RF-15, RF-16 y RF-28 solo figuran como anotaciones de comunicación dentro del pool.
11. **H-11 (nuevo):** el BPMN y el backend permiten `NOVEDAD → EN_TRANSITO` (bucle REINTENTAR de `GW_AccionNovedad` a `GW_MergeTransito`), pero la app del motorizado oculta "Iniciar tránsito" y "Novedad" en ese estado (`puedeIniciarTransito`, `puedeRegistrarNovedad`). El proceso modelado no es ejecutable de punta a punta desde la interfaz.
12. **H-12 (nuevo):** `ST_CrearCompra` crea la ENTREGA en `CREADO` antes de cobrar y no la revierte si el pago es `RECHAZADO`: el BPMN no tiene gateway sobre el resultado del pago.
13. **H-02 / H-04 / H-09** siguen abiertos y están anotados en el BPMN (`TA_H02`, `TA_H04`, `TA_Compra`, `TA_H09b`).

**Arquitectura / frontend**
14. **Endpoints sin pantalla:** `PUT /api/servicios/{id}/productos/` (RF-26), `GET /api/pagos/{pk}/` (RF-23), escritura de `/api/productos/` (RF-04). El método `productos.service.ts:disponiblesChatbot` existe pero ninguna página lo usa (el chatbot obtiene el catálogo por `tool_listar_productos`).
15. **RF-28** declara como actor también al Motorizado, pero solo `features/cliente/tracking.page.ts` consume `GET /api/tracking/destino/`.
16. **RN-14 / RF-15:** `UltimaPosicionView` solo restringe al rol CLIENTE; un motorizado puede consultar la posición de servicios ajenos (06-c4.md §7.7).

**Datos (MER)**
17. **Atributo sin requerimiento que lo mueva:** `RUTA.estado` (`EstadoRuta`) nunca cambia de `PLANEADA`; ningún RF ni actividad BPMN lo actualiza.

**Documentación**
18. **H-03:** T-INV-02 del plan ("Alistador crea producto → 201") contradice la prueba real (Alistador → 403).
19. El archivo fuente `docs/diagrams/src/bpmn-ciclo-servicio.bpmn` (anotación `TA_Reintentar`) aún dice "Observación O-01"; el documento 05-bpmn.md ya usa los IDs H-11 y H-12.
