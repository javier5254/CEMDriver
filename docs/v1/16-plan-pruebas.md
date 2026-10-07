# Plan de pruebas — CMEDriver

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

### `tracking` — GPS
| ID | Caso | Resultado esperado |
|---|---|---|
| T-TRK-01 | Motorizado asignado reporta posición | 201 |
| T-TRK-02 | Motorizado NO asignado reporta posición | 403 |
| T-TRK-03 | Cliente dueño consulta la última posición | 200, coincide con la última reportada |
| T-TRK-04 | Otro cliente consulta la posición | 403 |

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
**32/32 pruebas automatizadas en verde** (`manage.py test`, 0.45s). Las pruebas manuales de UI (`T-UI-*`) quedan pendientes de una pasada de QA sobre el frontend ya funcional.

### Hallazgos de la primera corrida (ya corregidos)
- El endpoint `POST /api/servicios/` devolvía una respuesta sin el campo `estado` (usaba el serializer de creación, más delgado, en vez del serializer completo). Se corrigió `ServicioViewSet.create()` para devolver siempre la representación completa del servicio recien creado.
- Dos pruebas asumían que acceder a un servicio ajeno devolvía `403 Forbidden`. En realidad devuelve `404 Not Found`, porque `get_queryset()` ya filtra los servicios visibles por rol (un cliente/motorizado ajeno al servicio ni siquiera lo ve en su queryset) — esto es intencional y preferible desde el punto de vista de seguridad (no revela la existencia del recurso a quien no tiene acceso a él). Se ajustaron las pruebas para reflejar el comportamiento correcto, documentado inline en `services/tests.py`.
