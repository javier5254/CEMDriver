# Plan de pruebas — CMEDriver (v2)

> **Nota (2026-10-09):** este documento es **histórico**: se redactó antes de la reducción de alcance que retiró el inventario, los pagos y el chatbot (el chat quedó solo como canal entre el cliente y el motorizado) y **no refleja el alcance vigente**. Cuenta 93 pruebas y conserva los casos `T-INV-*`, `T-BOT-*`, `T-PAG-*` y `T-SRV-17…19`, de funciones retiradas; la suite vigente del backend tiene **69 pruebas** y la prueba de cada requerimiento vigente está en [entrega/01-requerimientos.md §4](entrega/01-requerimientos.md#4-requerimientos-funcionales-rf). Prevalece la documentación de [entrega/](entrega/00-guia-de-entrega.md), en particular [entrega/01-requerimientos.md §2.4](entrega/01-requerimientos.md#24-cambios-de-alcance).

## 1. Estrategia
Las pruebas del backend están **automatizadas** (no solo documentadas): cada caso de prueba de este documento tiene su contraparte ejecutable en `backend/*/tests.py`, usando el framework de pruebas de Django + `rest_framework.test.APIClient`. Cada corrida crea y destruye su propia base de datos de prueba — no depende de los datos de `seed_data`.

## 2. Cómo ejecutar las pruebas

```bash
cd backend
./.venv/Scripts/python.exe manage.py test               # todas las apps
./.venv/Scripts/python.exe manage.py test services       # solo un app
./.venv/Scripts/python.exe manage.py test services.tests.NovedadTests   # solo una clase
./.venv/Scripts/python.exe manage.py test -v 2           # salida detallada (verbosity 2)
```

En macOS/Linux, reemplazar `./.venv/Scripts/python.exe` por `python` (con el entorno virtual activado).

### Script de conveniencia
Para no escribir la ruta del entorno virtual cada vez, hay un script wrapper en `backend/`:
```bash
# Windows (PowerShell)
./run_tests.ps1
./run_tests.ps1 services
./run_tests.ps1 services.tests.NovedadTests

# macOS/Linux
./run_tests.sh
./run_tests.sh services
```

## 3. Cobertura de casos de prueba por módulo

### `accounts` — Autenticación y usuarios
| ID | Caso | Resultado esperado |
|---|---|---|
| T-ACC-01 | Login con credenciales válidas | 200, devuelve `access`, `refresh` y `user.rol` |
| T-ACC-02 | Login con password incorrecta | 401 |
| T-ACC-03 | `GET /api/auth/me/` autenticado | 200, devuelve el usuario actual |
| T-ACC-04 | Admin lista usuarios | 200 |
| T-ACC-05 | Alistador/Motorizado/Cliente intentan listar usuarios | 403 para los 3 roles |
| T-ACC-06 | Anónimo intenta listar usuarios | 401 |
| T-ACC-07 | Login usando el correo en vez del username | 200, resuelve al usuario correcto |
| T-ACC-08 | Solicitar reset de contraseña con correo existente | 200, se envía un correo (verificado con `django.core.mail.outbox` en pruebas) |
| T-ACC-09 | Solicitar reset con correo inexistente | 200 igual (nunca revela si el correo existe), no se envía correo |
| T-ACC-10 | Confirmar reset con token válido | 200, la nueva contraseña permite login |
| T-ACC-11 | Confirmar reset con token inválido/alterado | 400 |

### `coverage` — Matriz de cobertura
| ID | Caso | Resultado esperado |
|---|---|---|
| T-COV-01 | No-admin intenta crear cobertura | 403 |
| T-COV-02 | Cualquier autenticado puede leer cobertura | 200 |
| T-COV-03 | Agenda disponible respeta leadtime y días hábiles configurados | Todas las fechas devueltas cumplen ambas condiciones |
| T-COV-04 | Agenda disponible de una zona inexistente | 404 |

### `inventory` — Productos / chatbot
| ID | Caso | Resultado esperado |
|---|---|---|
| T-INV-01 | Motorizado intenta crear producto | 403 |
| T-INV-02 | Alistador crea producto | 201 |
| T-INV-03 | Catálogo del chatbot solo muestra productos con `disponible_chatbot=true` y `stock>0` | Solo aparece el producto que cumple ambas condiciones |

### `services` — Núcleo del dominio
| ID | Caso | Resultado esperado |
|---|---|---|
| T-SRV-01 | No-alistador intenta crear servicio | 403 |
| T-SRV-02 | Crear ENTREGA sin `direccion_destino` | 400 |
| T-SRV-03 | Crear RECOLECCION sin `direccion_origen` | 400 |
| T-SRV-04 | Crear servicio válido | 201, estado `CREADO` |
| T-SRV-05 | Flujo completo ENTREGA: asignar-ruta &rarr; recibir-en-centro &rarr; iniciar-transito &rarr; cerrar | Termina en `ENTREGADO` |
| T-SRV-06 | Motorizado no asignado a la ruta intenta operar el servicio | 403 |
| T-SRV-07 | `recibir-en-centro` sobre una RECOLECCION | 400 (regla RN-01, solo aplica a Entrega) |
| T-SRV-08 | Cerrar RECOLECCION sin foto/firma | 400 |
| T-SRV-09 | Cerrar RECOLECCION con foto y firma | 200, estado `RECOLECTADO`, incluye `evidencia` |
| T-SRV-10 | Novedad con `accion=REINTENTAR` | Estado pasa a `NOVEDAD`, luego permite volver a `iniciar-transito` |
| T-SRV-11 | Novedad con `accion=DEVOLVER_A_CENTRO` | Estado pasa a `DEVUELTO` (terminal); `cerrar` posterior falla con 400 |
| T-SRV-12 | Cliente dueño envía y lee mensajes del chat | 201 al enviar, lista con 1 mensaje al leer |
| T-SRV-13 | Otro cliente (no dueño) intenta leer el chat | 403 |
| T-SRV-14 | Motorizado asignado participa en el chat | 201 |
| T-SRV-15 | Cliente planifica recolección fuera del leadtime | 400 |
| T-SRV-16 | Cliente planifica recolección en fecha válida | 201, tipo `RECOLECCION`, estado `CREADO` |
| T-SRV-17 | Alistador define líneas de producto de un servicio | 200, `productos_detalle` refleja la lista enviada |
| T-SRV-18 | Reemplazar líneas de producto es idempotente | Una segunda llamada reemplaza por completo la lista anterior |
| T-SRV-19 | No-alistador intenta definir líneas de producto | 403 |
| T-SRV-20 (WS) | Mensaje enviado por WebSocket se guarda y se difunde a ambos participantes | Cliente y motorizado conectados reciben el mismo mensaje en <1s; queda 1 `MensajeChat` en BD |
| T-SRV-21 (WS) | Usuario no autorizado intenta conectarse al chat de un servicio ajeno | La conexión WebSocket se rechaza (no se acepta el handshake) |

### `tracking` — GPS
| ID | Caso | Resultado esperado |
|---|---|---|
| T-TRK-01 | Motorizado asignado reporta posición | 201 |
| T-TRK-02 | Motorizado NO asignado reporta posición | 403 |
| T-TRK-03 | Cliente dueño consulta la última posición | 200, coincide con la última reportada |
| T-TRK-04 | Otro cliente consulta la posición | 403 |
| T-TRK-05 (WS) | Cliente dueño conectado recibe por WebSocket la posición reportada por REST | El mensaje recibido coincide con la posición posteada |
| T-TRK-06 (WS) | Usuario no autorizado intenta conectarse al tracking de un servicio ajeno | La conexión WebSocket se rechaza |

### `optimization` — Optimización de rutas
| ID | Caso | Resultado esperado |
|---|---|---|
| T-OPT-01 | No-admin/alistador intenta optimizar una ruta | 403 |
| T-OPT-02 | Orden sugerido correcto para coordenadas conocidas (geocoding *mockeado*, sin red real) | El orden devuelto coincide con el vecino-más-cercano calculado a mano |
| T-OPT-03 | Una dirección que no geocodifica queda fuera del orden sugerido | Aparece en `no_geocodificados`, el resto del orden se calcula igual, 200 (no error) |
| T-OPT-04 | Segunda llamada para el mismo servicio no vuelve a geocodificar | El mock de geocoding se llama la misma cantidad de veces (se usó el caché `PuntoGeocodificado`) |

### `chatbot` — Asistente conversacional
| ID | Caso | Resultado esperado |
|---|---|---|
| T-BOT-01 | Saludo / mensaje vacío | Devuelve el menú de opciones (comprar / recolección) |
| T-BOT-02 | Mensaje no reconocido | Respuesta de fallback amigable, nunca un 500 |
| T-BOT-03 | Compra completa en un solo mensaje ("quiero comprar Termo") | Salta el listado, va directo a pedir zona/dirección |
| T-BOT-04 | Compra completa eligiendo el producto en un turno separado del listado | Crea el servicio y el pago correctamente (regresión de un bug real encontrado y corregido, ver más abajo) |
| T-BOT-05 | Recolección con fecha que viola el leadtime | Respuesta de rechazo (no 500), reutilizando la misma validación que `/servicios/planificar/` |
| T-BOT-06 | Recolección: reintentar con otra fecha tras un rechazo | No hay que repetir zona/dirección, solo la fecha |
| T-BOT-07 | Cliente dueño lee su historial de conversación | 200 |
| T-BOT-08 | Otro cliente intenta leer una conversación ajena | 403 |
| T-BOT-09 | Rol distinto de CLIENTE intenta usar el chatbot | 403 |

### `payments` — Pagos simulados
| ID | Caso | Resultado esperado |
|---|---|---|
| T-PAG-01 | Procesar un pago simulado | Termina en `APROBADO` o `RECHAZADO`, nunca se queda en `PENDIENTE` |
| T-PAG-02 | Referencia del pago es única | Sin colisiones entre pagos distintos |
| T-PAG-03 | Cliente ajeno consulta un pago que no es suyo | 403 |

### `integrations` — API keys y webhooks
| ID | Caso | Resultado esperado |
|---|---|---|
| T-INT-01 | No-admin intenta gestionar API keys / webhooks | 403 |
| T-INT-02 | Crear una API key devuelve la clave cruda | Solo en la respuesta de creación; un `GET` posterior de la lista nunca la incluye |
| T-INT-03 | `ApiKeyAuthentication` acepta una clave válida y rechaza una inválida/inactiva | Autenticación exitosa solo con la clave correcta y activa |
| T-INT-04 | `disparar_webhook` firma correctamente y registra la entrega (HTTP mockeado, sin red real) | `WebhookDelivery.exito=True`, firma HMAC verificable |
| T-INT-05 | `disparar_webhook` ante un endpoint inalcanzable | Nunca lanza excepción; `WebhookDelivery.exito=False` con el error registrado |

## 4. Pruebas manuales pendientes (fuera del alcance de la suite automatizada)
Estas requieren interacción real de navegador/dispositivo y se validan manualmente antes de cada entrega:

| ID | Caso | Cómo probarlo |
|---|---|---|
| T-UI-01 | Login visual en los 4 roles redirige a su área correspondiente | Navegar a `/login`, probar cada credencial demo |
| T-UI-02 | Captura de foto en el cierre de una Recolección | Desde el frontend, en un servicio RECOLECCION `EN_TRANSITO`, adjuntar una imagen |
| T-UI-03 | Captura de firma en canvas | Firmar sobre el canvas de `signature_pad` antes de cerrar |
| T-UI-04 | Tracking GPS real desde el navegador móvil | Aceptar permiso de geolocalización, verificar que el marcador se mueve en el mapa del cliente |
| T-UI-05 | Responsive en viewport de celular | Redimensionar/emular un viewport de 390px de ancho en las 4 áreas |

## 5. Estado actual
**93/93 pruebas automatizadas en verde** (`manage.py test`, ~3s). Las pruebas manuales de UI (`T-UI-*`) quedan pendientes de una pasada de QA formal, aunque todas las features de v2 (auth por correo, reset de contraseña, WebSockets de tracking/chat, chatbot, pagos, API keys/webhooks, optimización de ruta) ya se verificaron manualmente en vivo contra el frontend real además de la suite automatizada.

### Hallazgos de la primera corrida — MVP (ya corregidos)
- El endpoint `POST /api/servicios/` devolvía una respuesta sin el campo `estado` (usaba el serializer de creación, más delgado, en vez del serializer completo). Se corrigió `ServicioViewSet.create()` para devolver siempre la representación completa del servicio recien creado.
- Dos pruebas asumían que acceder a un servicio ajeno devolvía `403 Forbidden`. En realidad devuelve `404 Not Found`, porque `get_queryset()` ya filtra los servicios visibles por rol (un cliente/motorizado ajeno al servicio ni siquiera lo ve en su queryset) — esto es intencional y preferible desde el punto de vista de seguridad (no revela la existencia del recurso a quien no tiene acceso a él). Se ajustaron las pruebas para reflejar el comportamiento correcto, documentado inline en `services/tests.py`.

### Hallazgos de la ronda v2 (ya corregidos)
- **Migraciones de `chatbot`/`payments` no aplicadas a la base de datos real** (`db.sqlite3`): la suite de pruebas pasaba porque usa una base de datos aislada que se migra desde cero en cada corrida, pero `manage.py migrate` nunca se había ejecutado contra la base de datos de desarrollo real. Se detectó al intentar borrar datos de prueba manualmente (`OperationalError: no such table: payments_pago`) y se corrigió aplicando las migraciones pendientes. **Lección**: pasar la suite de pruebas no garantiza que las migraciones estén aplicadas en el entorno real — conviene verificar `manage.py showmigrations` como parte del checklist de integración, no solo correr los tests.
- **Bug real en el chatbot** (`chatbot/llm.py`): si el cliente escribía "quiero comprar" (sin nombrar el producto) y luego elegía el producto en un mensaje *separado* del listado, el sistema perdía el producto elegido y el turno de la fecha terminaba en `KeyError: 'producto_id'` (error 500). Causa: el enrutador de la conversación asumía que, una vez con `intencion=comprar` en curso, el siguiente mensaje siempre era zona/dirección — nunca contemplaba que aún faltara capturar el producto. Se corrigió haciendo que `_continuar_compra` revise primero si falta el producto, y se agregó una prueba de regresión (`test_elegir_producto_en_un_turno_separado_completa_la_compra`) que reproduce exactamente esta secuencia de turnos.
