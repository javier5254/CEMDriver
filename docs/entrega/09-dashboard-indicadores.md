# 9. Dashboard de indicadores operativos (RF-30) y datos de demostración

**Proyecto:** CMEDriver — plataforma de gestión de mensajería (entregas y recolecciones).
**Autor:** Javier Esteban Mora Osorio (único integrante). UNINPAHU, Ingeniería de Software.
**Relacionado:** [01-requerimientos.md](01-requerimientos.md) (RF y reglas de negocio) · [03-arquitectura.md](03-arquitectura.md) · [08-limitaciones-y-mejoras.md](08-limitaciones-y-mejoras.md)

Este documento describe el módulo de indicadores agregado para la entrega final: un endpoint que calcula métricas operativas **directamente sobre la base de datos del proyecto**, un comando que carga datos de demostración reproducibles y un comando que exporta los indicadores a JSON. Todo el código está en `backend/`; la pantalla del dashboard vive en `frontend/` (`src/app/features/indicadores/`) y consume este mismo endpoint.

> **Aviso sobre los datos.** Las cifras que se muestran en la demostración salen de datos **sintéticos** generados por `seed_demo`. No son operaciones reales de Logytech Mobile ni de ninguna empresa, y no sirven como evidencia del desempeño de una operación real. Demuestran que el sistema calcula, a partir de sus propias tablas, indicadores coherentes con su modelo de datos.

---

## 9.1 Propósito y requerimiento

| Campo | Valor |
|---|---|
| ID | **RF-30** |
| Nombre | Consultar indicadores operativos |
| Actores | Administrador, Alistador |
| Descripción | El sistema debe permitir al Administrador y al Alistador consultar, para un periodo de 1 a 365 días y opcionalmente para una zona, indicadores operativos calculados desde la base de datos: volumen y estados de los servicios, tasa de éxito, novedades, completitud de la evidencia, productividad por motorizado, actividad de la operación (rutas, GPS, chat) y estado de las integraciones. |
| Criterio de aceptación | `GET /api/indicadores/` responde 200 a ADMIN y ALISTADOR, 403 a CLIENTE y MOTORIZADO y 401 sin autenticación; las cifras coinciden con un conjunto de datos conocido (verificado por pruebas automatizadas, §9.8) y los totales son coherentes entre secciones (la suma de `por_estado`, de `por_zona` y de `serie_diaria` es igual a `resumen.servicios_total`). |
| Evidencia | `backend/services/indicadores.py` → `calcular_indicadores`; `backend/services/views_indicadores.py` → `IndicadoresView`; `backend/services/tests_indicadores.py` |

**Integración con los demás documentos.** RF-30 se declara aquí y está incorporado en [01-requerimientos.md](01-requerimientos.md) (§4.1, nota 8 y §9), en [07-trazabilidad.md](07-trazabilidad.md) (§c.1 y §g), en [03-arquitectura.md](03-arquitectura.md) (§4 y §6), en [06-c4.md](06-c4.md) (§4.1 y §5.1) y en [08-limitaciones-y-mejoras.md](08-limitaciones-y-mejoras.md) (LIM-40, LIM-41 y §8.5). Con él, los RF vigentes son 25 de 30.

---

## 9.2 Endpoint `GET /api/indicadores/`

### Autenticación y permisos

| Quién llama | Resultado |
|---|---|
| ADMIN | 200 |
| ALISTADOR (JWT o API Key de un alistador, cabecera `X-API-Key`) | 200 |
| CLIENTE | 403 |
| MOTORIZADO | 403 |
| Sin token | 401 |

El permiso es la clase `IsAdminOAlistador` (`backend/accounts/permissions.py`), construida con el mismo ayudante que `IsAdmin`, `IsAlistador`, etc. El endpoint está documentado en OpenAPI (`/api/docs/`, etiqueta `indicadores`) con los dos parámetros y el esquema de la respuesta.

### Parámetros de consulta

| Parámetro | Tipo | Por defecto | Descripción |
|---|---|---|---|
| `dias` | entero 1–365 | 30 | Tamaño del periodo. El día actual cuenta como el último: `desde = hoy − (dias − 1)`, `hasta = hoy`. |
| `zona` | texto | (sin filtro) | Texto **exacto** de `Servicio.zona` (por ejemplo `Bogota - Chapinero`). Vacío equivale a sin filtro. |

Un `dias` fuera de rango o no numérico (`0`, `366`, `-3`, `abc`, `7.5`) responde **400**:

```json
{"dias": ["dias debe ser un número entero entre 1 y 365."]}
```

### Convenciones de la respuesta

- **Contrato fijo:** los nombres y la estructura no cambian; lo consumen el dashboard del frontend, la presentación y el comando de exportación.
- **Tasas:** son **proporciones entre 0 y 1** (no porcentajes), redondeadas a 4 decimales. Incluye `evidencia.porcentaje`: aunque se llama «porcentaje», por contrato es una proporción 0–1, igual que las demás tasas.
- **Datos que no se pueden calcular** (denominador cero o sin registros) se devuelven como `null`, nunca como un valor inventado.
- **Periodo:** se mide por `Servicio.creado_en` en la **fecha local del servidor** (`TIME_ZONE = America/Bogota`, `USE_TZ = True`). Un servicio creado a las 22:30 hora de Bogotá cuenta en ese día aunque en UTC ya sea el siguiente.

### Ejemplo real

Respuesta de `GET /api/indicadores/?dias=14` sobre la base de datos demo, obtenida el 2026-11-17 llamando a la vista con `demo_admin` (los valores cambian con la fecha en que se siembran los datos):

```json
{
  "generado_en": "2026-11-17T19:30:21.593194-05:00",
  "periodo": {"dias": 14, "desde": "2026-11-04", "hasta": "2026-11-17", "zona": null},
  "resumen": {"servicios_total": 67, "entregas": 41, "recolecciones": 26, "en_curso": 16, "cerrados_exitosos": 49, "devueltos": 2, "tasa_exito": 0.9608, "servicios_con_novedad": 4, "tasa_novedad": 0.0597},
  "por_estado": [
    {"estado": "CREADO", "etiqueta": "Creado", "total": 3},
    {"estado": "ASIGNADO", "etiqueta": "Asignado a ruta", "total": 6},
    {"estado": "RECIBIDO_CENTRO", "etiqueta": "Recibido en centro", "total": 2},
    {"estado": "EN_TRANSITO", "etiqueta": "En tránsito", "total": 4},
    {"estado": "NOVEDAD", "etiqueta": "Con novedad", "total": 1},
    {"estado": "ENTREGADO", "etiqueta": "Entregado", "total": 31},
    {"estado": "RECOLECTADO", "etiqueta": "Recolectado", "total": 18},
    {"estado": "DEVUELTO", "etiqueta": "Devuelto al centro", "total": 2}
  ],
  "serie_diaria": [
    {"fecha": "2026-11-04", "entregas": 2, "recolecciones": 5},
    {"fecha": "2026-11-05", "entregas": 4, "recolecciones": 2},
    {"fecha": "2026-11-06", "entregas": 4, "recolecciones": 2},
    {"fecha": "2026-11-07", "entregas": 2, "recolecciones": 0},
    {"fecha": "2026-11-08", "entregas": 1, "recolecciones": 0},
    {"fecha": "2026-11-09", "entregas": 3, "recolecciones": 2},
    {"fecha": "2026-11-10", "entregas": 4, "recolecciones": 1},
    {"fecha": "2026-11-11", "entregas": 5, "recolecciones": 2},
    {"fecha": "2026-11-12", "entregas": 2, "recolecciones": 4},
    {"fecha": "2026-11-13", "entregas": 4, "recolecciones": 2},
    {"fecha": "2026-11-14", "entregas": 2, "recolecciones": 1},
    {"fecha": "2026-11-15", "entregas": 1, "recolecciones": 0},
    {"fecha": "2026-11-16", "entregas": 4, "recolecciones": 2},
    {"fecha": "2026-11-17", "entregas": 3, "recolecciones": 3}
  ],
  "por_zona": [
    {"zona": "Bogota - Usaquen", "total": 16, "exitosos": 14, "con_novedad": 2},
    {"zona": "Bogota - Chapinero", "total": 13, "exitosos": 7, "con_novedad": 1},
    {"zona": "Bogota - Suba", "total": 12, "exitosos": 9, "con_novedad": 0},
    {"zona": "Bogota - Kennedy", "total": 11, "exitosos": 8, "con_novedad": 1},
    {"zona": "Bogota - Teusaquillo", "total": 9, "exitosos": 6, "con_novedad": 0},
    {"zona": "Bogota - Fontibon", "total": 6, "exitosos": 5, "con_novedad": 0}
  ],
  "novedades": {
    "total": 5,
    "por_tipo": [
      {"tipo": "Dirección errada", "total": 2},
      {"tipo": "Cliente ausente", "total": 1},
      {"tipo": "Paquete dañado", "total": 1},
      {"tipo": "Rechazo del destinatario", "total": 1}
    ],
    "por_accion": [
      {"accion": "REINTENTAR", "etiqueta": "Reintentar", "total": 3},
      {"accion": "DEVOLVER_A_CENTRO", "etiqueta": "Devolver a centro", "total": 2}
    ]
  },
  "evidencia": {"recolecciones_cerradas": 18, "con_evidencia_completa": 17, "porcentaje": 0.9444, "horas_promedio_a_cierre": 45.78},
  "motorizados": [
    {"id": 63, "nombre": "Andrés Felipe Rojas", "servicios": 28, "cerrados_exitosos": 21, "con_novedad": 3},
    {"id": 64, "nombre": "Jhon Alexander Gómez", "servicios": 24, "cerrados_exitosos": 20, "con_novedad": 1},
    {"id": 65, "nombre": "Wilmer Eduardo Cárdenas", "servicios": 8, "cerrados_exitosos": 7, "con_novedad": 0},
    {"id": 66, "nombre": "Diego Armando Parra", "servicios": 4, "cerrados_exitosos": 1, "con_novedad": 0}
  ],
  "operacion": {"rutas": 24, "sin_asignar": 3, "posiciones_gps": 199, "mensajes_chat": 47},
  "integraciones": {
    "api_keys_activas": 1,
    "webhooks_activos": 1,
    "envios_webhook": {"total": 193, "exitosos": 180, "fallidos": 13, "tasa_exito": 0.9326}
  }
}
```

---

## 9.3 Definición exacta de cada indicador

Todas las cifras se calculan con agregaciones del ORM de Django (`values().annotate(Count(...))`, `Exists`, `Avg`), sin recorrer objetos en Python ni consultas por fila. Sea **S** el conjunto de servicios con `creado_en` dentro del periodo y, si se indicó `zona`, con `Servicio.zona` igual a ese texto.

### `periodo`

| Campo | Definición |
|---|---|
| `dias` | Valor del parámetro (30 por defecto). |
| `desde`, `hasta` | `hasta` = fecha local de hoy; `desde` = `hasta − (dias − 1)`. |
| `zona` | Texto recibido o `null`. |
| `generado_en` (raíz) | Instante del cálculo, ISO 8601 con zona horaria. |

### `resumen`

| Campo | Fórmula | Origen |
|---|---|---|
| `servicios_total` | \|S\| | `Servicio` |
| `entregas`, `recolecciones` | servicios de S con `tipo = ENTREGA` / `RECOLECCION` | `Servicio.tipo` |
| `en_curso` | servicios de S con estado en {CREADO, ASIGNADO, RECIBIDO_CENTRO, EN_TRANSITO, NOVEDAD} | `Servicio.estado` |
| `cerrados_exitosos` | servicios de S con estado ENTREGADO o RECOLECTADO | `Servicio.estado` |
| `devueltos` | servicios de S con estado DEVUELTO | `Servicio.estado` |
| `tasa_exito` | `cerrados_exitosos / (cerrados_exitosos + devueltos)`; `null` si el denominador es 0. Los servicios en curso no entran. | derivado |
| `servicios_con_novedad` | servicios **distintos** de S con al menos una `Novedad` (aunque hoy ya estén cerrados) | `Novedad.servicio` (`Exists`) |
| `tasa_novedad` | `servicios_con_novedad / servicios_total`; `null` si no hay servicios | derivado |

### `por_estado`

Siempre los 8 estados, aunque tengan 0, en el orden CREADO, ASIGNADO, RECIBIDO_CENTRO, EN_TRANSITO, NOVEDAD, ENTREGADO, RECOLECTADO, DEVUELTO. `total` = servicios de S en ese estado. Etiquetas: Creado, Asignado a ruta, Recibido en centro, En tránsito, Con novedad, Entregado, Recolectado, Devuelto al centro.

### `serie_diaria`

Un elemento por **cada día** del periodo (incluye días con 0), en orden ascendente. `entregas` y `recolecciones` = servicios de S creados ese día local (`TruncDate(creado_en)` en la zona horaria actual), por `tipo`, sin importar su estado.

### `por_zona`

Agrupa S por `Servicio.zona` (texto exacto). `total` = servicios; `exitosos` = ENTREGADO o RECOLECTADO; `con_novedad` = servicios con al menos una novedad. Orden: `total` descendente y, en empate, zona alfabética.

### `novedades`

Sobre las novedades de los servicios de S (se asocian por la fecha de creación del **servicio**, no por `Novedad.creado_en`).

| Campo | Definición | Origen |
|---|---|---|
| `total` | cantidad de `Novedad` | `Novedad` |
| `por_tipo` | conteo por `Novedad.tipo`, orden descendente. Los códigos que guarda la app del motorizado se devuelven con etiqueta legible: `CLIENTE_AUSENTE` → «Cliente ausente», `DIRECCION_ERRADA` → «Dirección errada», `RECHAZO` → «Rechazo del destinatario», `ACCESO_RESTRINGIDO` → «Acceso restringido», `PAQUETE_DANADO` → «Paquete dañado», `OTRO` → «Otro». Un tipo desconocido (el campo es texto libre) se devuelve tal cual. | `Novedad.tipo` |
| `por_accion` | siempre `REINTENTAR` («Reintentar») y `DEVOLVER_A_CENTRO` («Devolver a centro»), con su conteo (0 si no hay) | `Novedad.accion` |

### `evidencia`

Se calcula sobre las recolecciones de S en estado RECOLECTADO.

| Campo | Fórmula | Origen |
|---|---|---|
| `recolecciones_cerradas` | cantidad de servicios de S en estado RECOLECTADO | `Servicio.estado` |
| `con_evidencia_completa` | de ellas, las que tienen `Evidencia` con `foto` **y** `firma` no vacías (RF-12) | `Evidencia.foto`, `Evidencia.firma` |
| `porcentaje` | `con_evidencia_completa / recolecciones_cerradas` (proporción 0–1); `null` si no hay recolecciones cerradas | derivado |
| `horas_promedio_a_cierre` | promedio de `Evidencia.capturado_en − Servicio.creado_en`, en horas con 2 decimales; `null` si no hay evidencias | `Evidencia.capturado_en`, `Servicio.creado_en` |

### `motorizados`

Servicios de S que tienen ruta, agrupados por `ruta__motorizado`. Cada elemento: `id` y `nombre` (o `username` si el nombre está vacío), `servicios` (los de S en sus rutas), `cerrados_exitosos` (ENTREGADO o RECOLECTADO) y `con_novedad` (con al menos una novedad). Orden: `servicios` descendente. Los servicios sin ruta no aparecen aquí.

### `operacion`

| Campo | Definición | Origen |
|---|---|---|
| `rutas` | rutas con `fecha` entre `desde` y `hasta`. Con `zona`, solo las que llevan al menos un servicio de esa zona (la ruta no tiene zona propia). | `Ruta.fecha` |
| `sin_asignar` | servicios de S en estado CREADO | `Servicio.estado` |
| `posiciones_gps` | `PosicionGPS` con `timestamp` dentro del periodo (con `zona`, de servicios de esa zona) | `PosicionGPS.timestamp` |
| `mensajes_chat` | `MensajeChat` con `enviado_en` dentro del periodo (con `zona`, de servicios de esa zona) | `MensajeChat.enviado_en` |

### `integraciones`

Las cifras de integraciones son **globales**: no se filtran por `zona`.

| Campo | Definición | Origen |
|---|---|---|
| `api_keys_activas` | `ApiKey` con `activa = True` | `ApiKey.activa` |
| `webhooks_activos` | `WebhookEndpoint` con `activo = True` | `WebhookEndpoint.activo` |
| `envios_webhook.total` | `WebhookDelivery` con `creado_en` dentro del periodo | `WebhookDelivery` |
| `envios_webhook.exitosos` / `fallidos` | los de `exito = True` / el resto | `WebhookDelivery.exito` |
| `envios_webhook.tasa_exito` | `exitosos / total`; `null` si no hubo envíos | derivado |

---

## 9.4 Comando `seed_demo` (datos de demostración)

Archivo: `backend/accounts/management/commands/seed_demo.py`. Se ejecuta **después** de `seed_data` (que crea los 4 usuarios base y las zonas Chapinero y Suba); no lo modifica ni duplica: si faltan las dos zonas base las crea con los mismos valores.

```powershell
cd backend
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_data          # opcional: usuarios base
.\.venv\Scripts\python.exe manage.py seed_demo          # 240 servicios en 60 días
.\.venv\Scripts\python.exe manage.py seed_demo --reset  # borra lo demo y lo recrea
```

| Opción | Por defecto | Efecto |
|---|---|---|
| `--dias` | 60 | Días de operación a simular (1–365). |
| `--servicios` | 240 | Cantidad de servicios. |
| `--semilla` | 2026 | Semilla del generador (`random.Random`): con la misma semilla y el mismo día se obtienen las mismas entidades. Cada componente (servicios, rutas, evidencias, GPS, chat, webhooks) usa su propio generador derivado de la semilla. |
| `--reset` | no | Borra **solo** lo creado por `seed_demo` y lo recrea. |

**Idempotencia.** Ejecutarlo dos veces sin `--reset` no duplica nada: detecta los usuarios `demo_*`, avisa y termina. Con `--reset` elimina primero lo demo (servicios de los clientes `demo_*` y, en cascada, sus evidencias, novedades, chat y posiciones; los archivos de foto y firma; rutas de los motorizados demo; API keys y webhooks `[DEMO]`; usuarios `demo_*`) y vuelve a crearlo. No toca ningún dato que no lleve la marca demo. Las coberturas (zonas) se conservan porque no llevan marca y son configuración inofensiva.

**Qué crea.**

- **Usuarios** (contraseña de desarrollo, ver §9.6): 4 motorizados `demo_moto1…4`, 8 clientes `demo_cliente1…8` con nombres colombianos plausibles, un alistador `demo_alistador1` y un administrador `demo_admin` (este sin permisos de Django admin).
- **Cobertura:** además de Chapinero y Suba, las zonas `Bogota - Usaquen`, `Bogota - Teusaquillo`, `Bogota - Fontibon` y `Bogota - Kennedy`, con *leadtime* y días válidos (se mantiene la escritura sin tildes de los nombres de zona existentes).
- **Servicios** repartidos en los últimos `--dias` días: más volumen entre semana (el domingo casi no hay), ligero crecimiento hacia el presente, ≈ 65 % entregas y ≈ 35 % recolecciones, direcciones de Bogotá con nomenclatura plausible por zona. Las recolecciones respetan *leadtime* y días válidos de su zona (mismo criterio que `POST /api/servicios/planificar/`).
- **Estados coherentes con la máquina de estados real** (`services/views.py`): una entrega pasa por CREADO → ASIGNADO → RECIBIDO_CENTRO → EN_TRANSITO → ENTREGADO; una recolección va de ASIGNADO a EN_TRANSITO y a RECOLECTADO (nunca pasa por RECIBIDO_CENTRO). DEVUELTO exige una novedad con acción `DEVOLVER_A_CENTRO`; NOVEDAD, una novedad `REINTENTAR` abierta. Los de los últimos 1–2 días quedan en estados abiertos, y hay unos pocos rezagados sin completar. Las proporciones de los servicios ya resueltos se fijan por cuotas (≈ 6,5 % devueltos, ≈ 4 % con novedad abierta, ≈ 7 % rezagados; el resto cerrado con éxito), no por sorteo individual, para que no dependan del azar de la semilla.
- **Rutas** por motorizado y fecha de agenda, con los servicios asignados (los CREADO no tienen ruta).
- **Novedades** con los tipos de la operación (cliente ausente, dirección errada, rechazo, acceso restringido, paquete dañado), guardados con los códigos que usa la app del motorizado, y acciones coherentes con el estado final.
- **Evidencias** con foto y firma generadas con Pillow (una caja con etiqueta «DEMO» y un trazo de firma) guardadas en `media/evidencias/` como lo hace el sistema; ≈ 95 % completas y unas pocas con solo foto o solo firma, para que el indicador no sea 100 %.
- **Posiciones GPS** (trayectorias suaves alrededor de Bogotá) para los servicios en tránsito y algunos cerrados recientes; **mensajes de chat** cliente↔motorizado.
- **Integraciones:** una API key `[DEMO]` y un webhook `[DEMO]` activo con ≈ 700 envíos registrados en `WebhookDelivery` (≈ 93–95 % exitosos, el resto con 5xx, tiempo agotado o conexión rechazada). Su URL (`http://127.0.0.1:9/...`) rechaza la conexión al instante: si se opera la app con el webhook demo activo, el envío fallará rápido en lugar de esperar el *timeout*.
- **Fechas retroactivas:** `creado_en`, `capturado_en`, `timestamp` y `enviado_en` son `auto_now_add`, así que se corrigen con `QuerySet.update()` tras crear cada registro. Ningún instante queda en el futuro, a cualquier hora del día (lo verifica una prueba).

Composición con la semilla por defecto, sembrada el 2026-11-17 (varía con la fecha, porque los estados dependen de cuántos días atrás se agendó cada servicio): 240 servicios (155 entregas, 85 recolecciones); 124 ENTREGADO, 64 RECOLECTADO (78 % cerrados con éxito), 15 DEVUELTO, 9 NOVEDAD, 9 CREADO, 13 ASIGNADO, 2 RECIBIDO_CENTRO y 4 EN_TRANSITO; 44 novedades; 64 evidencias (61 completas); ≈ 210 posiciones GPS, 84 mensajes y 718 envíos de webhook (679 exitosos).

Al terminar imprime un resumen (usuarios, servicios por estado, rutas, novedades, evidencias, GPS, chat, webhooks) y las credenciales demo. La API key se muestra **una sola vez** (después solo existe su hash, como en cualquier API key del sistema).

## 9.5 Comando `exportar_indicadores`

Archivo: `backend/services/management/commands/exportar_indicadores.py`. Llama a **la misma** función `calcular_indicadores` que el endpoint, por lo que ambos entregan el mismo JSON.

```powershell
cd backend
# a un archivo (crea las carpetas necesarias):
.\.venv\Scripts\python.exe manage.py exportar_indicadores --dias 30 --salida ..\presentacion\datos\indicadores.json
# por la salida estándar, filtrando una zona:
.\.venv\Scripts\python.exe manage.py exportar_indicadores --dias 7 --zona "Bogota - Suba"
```

| Opción | Por defecto | Efecto |
|---|---|---|
| `--dias` | 30 | Periodo (1–365; fuera de rango termina con error). |
| `--zona` | (sin filtro) | Zona exacta. |
| `--salida` | (stdout) | Ruta del archivo JSON (UTF-8, `indent=2`, acentos sin escapar). Si se omite, imprime el JSON. |

La presentación usa esa exportación (`presentacion/datos/indicadores.json`): los números de las diapositivas salen de la base de datos, no están escritos a mano.

---

## 9.6 Credenciales de demostración (solo desarrollo)

> **Solo para desarrollo local.** Son cuentas de demostración con una contraseña conocida y publicada en este documento; no deben existir en ningún entorno real. Se eliminan con `seed_demo --reset` o borrando los usuarios `demo_*`.

| Usuario | Rol | Contraseña |
|---|---|---|
| `demo_admin` | ADMIN | `demo1234` |
| `demo_alistador1` | ALISTADOR | `demo1234` |
| `demo_moto1` … `demo_moto4` | MOTORIZADO | `demo1234` |
| `demo_cliente1` … `demo_cliente8` | CLIENTE | `demo1234` |

Para ver el dashboard: iniciar sesión como `demo_admin` o `demo_alistador1`. Con `demo_cliente*` o `demo_moto*` el endpoint responde 403.

---

## 9.7 Limitaciones

Se registran sin maquillar; varias provienen del modelo de datos actual, no del cálculo.

1. **No hay historial de transiciones de estado.** `Servicio.estado` guarda solo el estado actual; no existe una tabla de eventos ni marcas de tiempo por transición. Por eso no se puede calcular el tiempo en cada estado, un embudo histórico ni cuántos servicios estaban «en curso» un día pasado.
2. **No hay marca de cierre en las entregas.** Cerrar una ENTREGA solo cambia el estado. No existe `cerrado_en`, así que **no hay «tiempo de entrega»** para servicios de ENTREGA. Solo las recolecciones dejan una marca de cierre (`Evidencia.capturado_en`), y por eso `horas_promedio_a_cierre` existe solo para ellas.
3. **El «tiempo a cierre» de las recolecciones incluye la espera agendada.** Mide desde la creación del servicio hasta la captura de la evidencia; como el cliente agenda con *leadtime* de 1–2 días según la zona, el valor típico es de decenas de horas y **no** mide la rapidez del motorizado en el trayecto.
4. **El periodo se mide por fecha de creación.** Un servicio creado hace 3 días y cerrado hoy cuenta en el día en que se creó. En periodos cortos y recientes, la proporción de servicios «en curso» es alta simplemente porque aún no han tenido tiempo de cerrarse.
5. **`tasa_exito` ignora lo que sigue abierto.** Se calcula solo sobre servicios resueltos (exitosos + devueltos): un servicio con NOVEDAD abierta no cuenta ni como éxito ni como fallo.
6. **`servicios_con_novedad` es histórico, no el estado actual.** Cuenta también servicios que tuvieron una novedad con acción `REINTENTAR` y luego se cerraron con éxito; no equivale a `por_estado.NOVEDAD`.
7. **«Evidencia completa» mide presencia, no calidad.** Verifica que existan foto y firma, no que la imagen sirva ni que la firma corresponda al destinatario.
8. **`Novedad.tipo` y `Servicio.zona` son texto libre.** Escrituras distintas del mismo concepto se cuentan por separado (salvo los códigos conocidos de novedad, que se normalizan a su etiqueta). `por_zona` y el filtro `zona` comparan por texto exacto.
9. **Las rutas no tienen zona.** Con el filtro `zona`, `operacion.rutas` cuenta las rutas que llevan al menos un servicio de esa zona (una aproximación). Las cifras de integraciones no se filtran por zona.
10. **Cálculo en vivo y sin caché.** Cada consulta recalcula con agregaciones sobre SQLite. Es adecuado para el volumen del prototipo (cientos o pocos miles de servicios); no se probó con volúmenes grandes ni se agregaron índices.
11. **Los datos de demostración no son operaciones reales de Logytech Mobile.** Son sintéticos, generados con una semilla y reglas simples (cuotas de estados, mezcla de zonas y tipos). Las cifras muestran el funcionamiento del cálculo y la coherencia de los datos; **no** son evidencia empírica del desempeño de ninguna operación ni validan una hipótesis del proyecto.
12. **Los envíos de webhook demo son registros sintéticos.** No se hizo ninguna petición HTTP real: se insertaron filas en `WebhookDelivery` con resultados simulados.
13. **Un solo punto de partida ficticio para el GPS.** Las trayectorias parten de un depósito inventado (Puente Aranda) y avanzan en línea suave hacia la zona de destino; no siguen calles.

---

## 9.8 Pruebas que lo verifican

Archivo: `backend/services/tests_indicadores.py` (38 pruebas; con las 72 existentes, la suite completa suma **110**, todas en verde con `python manage.py test`). Las pruebas que siembran datos usan una carpeta temporal para `MEDIA_ROOT` (no ensucian `backend/media`) y congelan el reloj donde comparan dos ejecuciones.

| Clase (pruebas) | Qué verifica |
|---|---|
| `IndicadoresPermisosTests` (5) | ADMIN y ALISTADOR → 200; CLIENTE y MOTORIZADO → 403; sin token → 401; `dias` inválido (`0`, `366`, `-3`, `abc`, `7.5`) → 400 con mensaje; los extremos 1 y 365 son válidos. |
| `IndicadoresCifrasTests` (10) | Sobre un conjunto de 12 servicios armado en la prueba (entregas y recolecciones, todos los estados, novedades, evidencias completa e incompleta, tres motorizados, GPS, chat, API keys y webhooks con envíos): estructura y claves en orden; `resumen` (incluidas `tasa_exito = 0.6667` y `tasa_novedad = 0.3636`); `por_estado` con los 8 estados en orden; `serie_diaria` (longitud = `dias`, total por día); `por_zona`; `novedades` (etiquetas y tipo libre); `evidencia` (50 % y 36 h); `motorizados`; `operacion`; `integraciones` (`tasa_exito = 0.8`). |
| `IndicadoresConsultasTests` (1) | El número de consultas SQL no crece al agregar servicios, zonas, novedades y motorizados (sin N+1) y se mantiene por debajo de 20. |
| `IndicadoresFiltrosTests` (6) | `dias` excluye los servicios y registros fuera del periodo (retrocediendo `creado_en` con `update()`); `dias=1`; periodo largo que sí incluye el servicio antiguo; `zona` filtra todas las secciones y no afecta integraciones; zona sin servicios → ceros, listas vacías y tasas `null`; `zona` vacía = sin filtro. |
| `IndicadoresPeriodoLocalTests` (1) | El periodo usa la fecha local de Bogotá: con `ahora` fijo, servicios creados a las 22:30 y 23:30 locales cuentan en su día, y los de 00:30 del día siguiente y de antes del periodo quedan fuera. |
| `SeedDemoTests` (11) | `seed_demo` crea usuarios y servicios y el endpoint los refleja; valores por defecto (240 servicios, proporciones razonables, 6 zonas, 4 motorizados, evidencia < 100 %); sin `--reset` no duplica; `--reset` deja el mismo estado (dos veces); misma semilla reproducible y otra semilla distinta; no toca datos que no son demo; elimina los archivos de evidencia demo; parámetros inválidos; coherencia con la máquina de estados (estado ↔ ruta, novedades y evidencia) y sin fechas futuras; funciona a cualquier hora del día (00:05, 06:30, 08:00, 12:00, 23:50); las imágenes generadas son válidas y hay evidencias incompletas. |
| `ExportarIndicadoresTests` (4) | Escribe un JSON válido (creando carpetas) igual al resultado de `calcular_indicadores`; conserva los acentos; sin `--salida` imprime JSON por stdout (con `--zona`); `--dias` fuera de rango falla. |

Ejecución:

```powershell
cd backend
.\.venv\Scripts\python.exe manage.py test                     # 110 pruebas
.\.venv\Scripts\python.exe manage.py test services.tests_indicadores   # solo las de RF-30
```
