# Fase 2 — Stack tecnológico y justificación

**Proyecto:** CMEDriver — plataforma de gestión de mensajería (entregas y recolecciones) con cuatro roles: Administrador, Alistador, Motorizado y Cliente.
**Repositorio:** <https://github.com/javier5254/CEMDriver>

Este documento recoge **lo que el proyecto usa realmente**, con las versiones tomadas de `backend/requirements.txt` y `frontend/package.json`. Para cada tecnología se explica la necesidad concreta del proyecto que resuelve (con el requisito RF/RNF/RN que la motiva, según [13-rf-rnf-completos.md](../13-rf-rnf-completos.md)) y qué alternativa se consideró y por qué se descartó.

Convenciones de estado usadas en las tablas:

- **En uso**: está instalado y funcionando en el código del repositorio.
- **Simulado**: la arquitectura de integración es real, pero el proveedor externo está reemplazado por una implementación local (`MockLLMClient`, `MockPaymentProvider`).
- **Propuesta**: no existe todavía en el repositorio; es la recomendación concreta para un despliegue real. Hoy el sistema **no está desplegado** en ningún servidor público: corre en local en modo desarrollo.

---

## 1. Resumen del stack

| Capa | Elección |
|---|---|
| Frontend | Ionic 9 + Angular 22 (SPA, tema iOS), empaquetable como app nativa con Capacitor 8 |
| Backend | Python 3.12 + Django 6.1 + Django REST Framework 3.18 (monolito modular, 9 apps) |
| Tiempo real | Django Channels 4.3 sobre el servidor ASGI Daphne 4.2 (WebSocket) |
| Base de datos | SQLite (desarrollo) → PostgreSQL (propuesta para producción) |
| Autenticación | JWT (SimpleJWT) para personas + API Key propia para sistemas integradores |
| Servicios externos | Nominatim/OpenStreetMap (real), teselas OSM (real), SMTP (consola en dev), pagos y LLM (simulados) |
| Despliegue | Local en desarrollo; propuesta Docker Compose + Nginx + Daphne + PostgreSQL + Redis en una VM Linux |
| Control de versiones | Git + GitHub |

---

## 2. Frontend

| Tecnología y versión | Para qué se usa en CMEDriver | Justificación (necesidad concreta) | Alternativa considerada y por qué se descartó |
|---|---|---|---|
| **Angular 22.0.1** (`@angular/core`, `router`, `forms`) | Framework de la SPA: componentes, enrutamiento por rol, servicios HTTP, interceptores para adjuntar el JWT | La app tiene 4 áreas separadas por rol (RF-01 a RF-27) que comparten servicios (autenticación, API, tracking). La inyección de dependencias y el router con guards de Angular permiten aislar cada área y redirigir según el rol del token (RNF-02) | **React**: exige elegir y ensamblar router, manejo de formularios y cliente HTTP por separado; Angular los trae integrados y con TypeScript estricto por defecto, lo que reduce decisiones en un equipo pequeño |
| **Ionic Framework 9** (`@ionic/angular`, `mode: 'ios'`) | Biblioteca de componentes táctiles (listas, tarjetas, modales, toasts, tabs) | El motorizado y el cliente usan la app desde el celular (RNF-05: usable en viewport móvil). Ionic da componentes móviles listos y la misma base de código sirve para web y para app nativa | **Angular Material**: pensado para escritorio/web; no ofrece la experiencia de app móvil ni la integración con Capacitor que sí tiene Ionic |
| **TypeScript ~6.0** | Lenguaje del frontend | Tipar los contratos de la API (servicios, estados, roles) evita errores al consumir los endpoints REST | **JavaScript puro**: sin tipos, los errores de contrato aparecen en tiempo de ejecución |
| **RxJS ~7.8** | Flujos asíncronos (peticiones HTTP, intervalos de polling de respaldo) | El tracking y el chat combinan WebSocket con un fallback a polling si el socket falla (RNF-10); RxJS modela bien esos flujos | Promesas/`async-await` puras: menos expresivas para reintentos e intervalos; además RxJS ya es dependencia obligatoria de Angular |
| **Leaflet 1.9.4** + teselas **OpenStreetMap** | Mapa del tracking del motorizado para el cliente | RF-15 / RF-27: mostrar en vivo la posición del motorizado. Leaflet no necesita API key ni cuenta de facturación | **Google Maps JavaScript API**: requiere API key, tarjeta de facturación y tiene cuotas; innecesario para un MVP académico |
| **signature_pad 5.1.4** | Captura de la firma del cliente sobre un `<canvas>` táctil | RF-11 / RN-02: una recolección no se puede cerrar sin foto **y firma** | Plugins nativos de firma: obligarían a compilar la app nativa; signature_pad funciona en el navegador sin dependencias |
| **`<input type="file" capture="environment">`** (API del navegador) | Toma de la foto de evidencia con la cámara trasera | RF-11 / RN-02 (foto obligatoria en recolección) | **`@capacitor/camera`**: solo aporta valor en la app nativa; el input HTML funciona igual en navegador móvil |
| **WebSocket nativo del navegador** | Cliente de los canales `/ws/tracking/{id}/` y `/ws/chat/{id}/` | RF-27: tracking y chat en vivo sin recargar | **Socket.IO**: requiere un servidor compatible con su protocolo propio; Django Channels habla WebSocket estándar |
| **Capacitor 8** (`@capacitor/core` 8.5.2, `android`, `ios`, `app`, `haptics`, `keyboard`, `status-bar`) | Empaquetar la misma SPA como app Android/iOS (`appId com.cmedriver.app`) | El motorizado trabaja en la calle; tener la opción de app instalable sin reescribir el frontend | **React Native / Flutter**: exigen otra base de código distinta de la web. **Cordova**: en desuso frente a Capacitor. Estado real: proyecto `android/` generado y sincronizado; el build de Gradle falló en la máquina de desarrollo por un problema de JDK/Windows (ver [11-manual-distribucion.md](../11-manual-distribucion.md) §4) |
| **Ionicons 8** | Iconografía de la interfaz | Consistencia visual con los componentes Ionic | Font Awesome: dependencia extra sin beneficio frente a la incluida en Ionic |

---

## 3. Backend

| Tecnología y versión | Para qué se usa en CMEDriver | Justificación (necesidad concreta) | Alternativa considerada y por qué se descartó |
|---|---|---|---|
| **Django 6.1.1** | Framework web: ORM, migraciones, autenticación, panel `/admin/`, envío de correo | El dominio es relacional y con muchas reglas (estados del servicio, cobertura, inventario). El ORM y las migraciones permiten evolucionar el modelo (v1 → v2 añadió 4 apps) sin SQL manual; el usuario personalizado `accounts.Usuario` con rol cubre RF-01 | **FastAPI**: más ligero, pero obliga a elegir e integrar ORM, migraciones, admin y autenticación por separado |
| **Django REST Framework 3.18.1** | Serializers, ViewSets, routers, permisos por rol, acciones de transición (`asignar-ruta`, `cerrar`, `novedad`...) | Toda la funcionalidad se expone como API REST consumida por la app y por integradores externos con el mismo contrato (RF-06). Las clases de permiso de DRF implementan el RBAC (RNF-02) | **Vistas Django + JsonResponse a mano**: repetiría validación, paginación y control de permisos en cada endpoint |
| **djangorestframework-simplejwt 5.5.1** (+ PyJWT 2.14) | Emisión y validación de JWT (access 8 h, refresh 1 día); login por usuario **o** correo | RNF-01: autenticación con expiración y renovación; RF-19: login con correo. Un token sin estado sirve igual para REST y para el WebSocket | **Sesiones con cookie de Django**: incómodas para una SPA en otro origen, para la app nativa y para autenticar el WebSocket |
| **API Key propia** (`integrations.authentication.ApiKeyAuthentication`) | Autenticar sistemas integradores (ERP/e-commerce) con el header `X-API-Key` | RF-06 / RF-24: un sistema externo crea servicios sin login humano. La clave se guarda solo como hash SHA-256 (RNF-12) y actúa como un usuario ALISTADOR (RN-08), así reutiliza los permisos existentes | **OAuth2 client-credentials** (p. ej. django-oauth-toolkit): más estándar, pero mucho más complejo de implementar y explicar en el alcance del MVP; queda como evolución |
| **Django Channels 4.3.2** | Consumers WebSocket `TrackingConsumer` y `ChatConsumer`, grupos `tracking_<id>` y `chat_<id>` | RF-27: posición GPS y mensajes en vivo (< 1 s). El patrón publicar/suscribir por grupos encaja con "varias personas mirando el mismo servicio" | **Polling REST** (lo que usaba v1): más carga y latencia; se mantiene solo como respaldo (RNF-10). **Node.js + Socket.IO**: obligaría a un segundo backend y a duplicar la autorización |
| **Daphne 4.2.3** | Servidor ASGI que atiende HTTP y WebSocket en el mismo proceso (`runserver` lo usa al estar primero en `INSTALLED_APPS`) | Un único proceso sirve la API y los sockets en desarrollo, sin infraestructura extra | **Gunicorn/WSGI**: no soporta WebSocket. **Uvicorn**: válido, pero Daphne es el servidor de referencia de Channels y se integra con `runserver` |
| **django-cors-headers 4.9.0** | Permitir que la SPA (`localhost:4200`/`8100`) consuma la API (`localhost:8000`) | Frontend y backend se sirven en orígenes distintos; los orígenes permitidos se leen de `CORS_ALLOWED_ORIGINS` | Servir el frontend desde Django: acopla los despliegues y complica el flujo de desarrollo con `ng serve` |
| **Pillow 12.3.0** | Soporte de `ImageField` para la foto y la firma de evidencia | RF-11 / RN-02: guardar y validar imágenes de evidencia | Guardar como `FileField` sin validación: se perdería la verificación de que el archivo es una imagen |
| **`django.core.mail`** (backend de consola en dev) | Correo de restablecimiento de contraseña | RF-20 / RNF-09: enlace de un solo uso. En dev el correo se imprime en consola, sin cuenta SMTP real | Integrar un proveedor transaccional (SendGrid, SES) desde el inicio: requiere cuenta y credenciales; con Django es cambiar `EMAIL_BACKEND` |
| **`urllib` (biblioteca estándar)** | Llamadas HTTP salientes a Nominatim y a los webhooks | Evitar dependencias nuevas para dos clientes HTTP simples | **requests / httpx**: mejores APIs, pero añadían dependencia sin necesidad real |

---

## 4. Base de datos

| Tecnología y versión | Para qué se usa en CMEDriver | Justificación (necesidad concreta) | Alternativa considerada y por qué se descartó |
|---|---|---|---|
| **SQLite 3** (incluida en Python) — **en uso, desarrollo** | Persistencia de todo el dominio (`backend/db.sqlite3`): usuarios, servicios, rutas, novedades, cobertura, inventario, posiciones GPS, chat, pagos, API keys, webhooks | Cero instalación: cualquier integrante o evaluador clona el repo, corre `migrate` + `seed_data` y tiene datos de prueba en minutos. Es suficiente para un solo usuario concurrente de demo y para la suite de 96 pruebas | **PostgreSQL desde el día 1**: obliga a instalar y configurar un servidor de BD en cada máquina de desarrollo, sin beneficio funcional para el MVP |
| **PostgreSQL 16** — **propuesta, producción** | Misma persistencia en un despliegue real | SQLite bloquea la base completa en cada escritura: con varios motorizados reportando GPS cada 5-10 s (RNF-06) y transiciones concurrentes se vuelve el cuello de botella. PostgreSQL ofrece concurrencia real (MVCC), copias de seguridad con `pg_dump`, roles de acceso y alta disponibilidad. El cambio **no requiere tocar modelos ni vistas**: el ORM de Django abstrae el motor; basta con cambiar `DATABASES` e instalar el driver `psycopg` | **MySQL/MariaDB**: igual de válido con Django, pero PostgreSQL tiene mejor soporte de `JSONField` (usado en `Conversacion.contexto` y `MensajeBot.function_call`) y es el motor recomendado por la comunidad Django. **MongoDB**: el dominio es fuertemente relacional (servicio → ruta → motorizado → evidencias); un documental complicaría la integridad referencial (p. ej. `on_delete=PROTECT`, RN-06) |

> **Decisión SQLite (dev) → PostgreSQL (prod):** se prioriza la velocidad de arranque en desarrollo y se difiere el motor robusto al despliegue, apoyándose en que el ORM hace el cambio transparente. Pendientes técnicos para concretarlo: añadir `psycopg` a `requirements.txt` y leer `DATABASES` desde variables de entorno (hoy está fijo a SQLite en `settings.py`).

---

## 5. Frameworks (resumen)

| Tecnología y versión | Para qué se usa en CMEDriver | Justificación | Alternativa descartada |
|---|---|---|---|
| **Django 6.1 + DRF 3.18** | Backend y API REST | Ver §3: ORM, migraciones, admin, auth y permisos integrados para un dominio relacional con RBAC | FastAPI (ensamblado manual de piezas) |
| **Django Channels 4.3** | Tiempo real | Ver §3: WebSocket en el mismo proyecto Django, reutilizando modelos y autorización | Servidor Node/Socket.IO aparte |
| **Angular 22** | SPA | Ver §2: estructura por rol, DI, router con guards | React (más piezas por elegir) |
| **Ionic 9** | UI móvil | Ver §2: componentes táctiles, misma base para web y nativa | Angular Material |
| **Capacitor 8** | Puente a nativo | Ver §2: app Android/iOS desde la misma SPA | React Native / Flutter |

---

## 6. Lenguajes

| Lenguaje y versión | Para qué se usa en CMEDriver | Justificación | Alternativa descartada |
|---|---|---|---|
| **Python 3.12** (probado 3.12.10) | Backend completo, comando `seed_data`, pruebas | Ecosistema Django; sintaxis clara para un equipo académico; type hints usados en módulos clave (`geocodificar() -> tuple[float, float] \| None`) | Java/Spring Boot: más verboso y ciclos de desarrollo más lentos para un MVP |
| **TypeScript ~6.0** | Frontend | Tipado de los contratos de la API; lenguaje nativo de Angular | JavaScript sin tipos |
| **HTML5 / SCSS** | Plantillas y estilos de las páginas Ionic (tema iOS) | Estándar de Angular/Ionic; variables CSS de Ionic para el tema | — |
| **SQL** (generado por el ORM) | Consultas a la BD | No se escribe SQL a mano: el ORM genera SQL compatible con SQLite y PostgreSQL, lo que habilita la migración de motor | SQL a mano: ataría el código a un motor |
| **Markdown + Mermaid** | Documentación y diagramas en `docs/` | Texto plano versionado junto al código | Documentos Word sueltos fuera del repositorio |

---

## 7. Servicios externos / APIs

| Tecnología y estado | Para qué se usa en CMEDriver | Justificación (necesidad concreta) | Alternativa considerada y por qué se descartó |
|---|---|---|---|
| **Nominatim (OpenStreetMap)** — **real** | Geocodificar las direcciones de una ruta (`optimization/geocoding.py`) con caché en `PuntoGeocodificado`, para la heurística de vecino más cercano | RF-21: sugerir el orden de visita de la ruta a partir de direcciones reales. Gratuito, sin API key; se respeta la política de 1 req/s (`RATE_LIMIT_SEGUNDOS = 1.1`) y el User-Agent propio | **Google Geocoding API**: más precisa pero de pago y con API key. Mitigación del límite de Nominatim: caché de puntos ya geocodificados |
| **Teselas de OpenStreetMap** — **real** | Mapa base del tracking (Leaflet carga `tile.openstreetmap.org` desde el navegador) | RF-15 / RF-27 | Google Maps / Mapbox (API key y cuota) |
| **Proveedor de pagos** — **simulado** (`payments/provider.py`, `MockPaymentProvider`) | Procesar el pago de una compra hecha por el chatbot (aprueba ~90 %, rechaza ~10 % para variedad en la demo) | RF-23 / RNF-13: el flujo de compra necesita un pago; no hay credenciales de comercio. La interfaz `PaymentProvider.procesar(pago)` y la fábrica `obtener_proveedor_pago()` dejan el punto exacto de reemplazo | **Integrar Wompi/PayU real**: requiere cuenta de comercio verificada; fuera del alcance académico. Se eligió el patrón Strategy para no bloquear el flujo |
| **Proveedor LLM** — **simulado** (`chatbot/llm.py`, `MockLLMClient`) | Responder al cliente en lenguaje libre y decidir qué "tool" invocar (listar productos, consultar agenda, crear recolección, crear compra) | RF-22: chatbot en texto libre. No hay API key de un LLM; se construyó la arquitectura real de tool-calling (historial, `function_call` persistido, slot-filling) con reglas de palabras clave como "cerebro" | **Chatbot solo con botones/máquina de estados** (v1): no demuestra el patrón de integración con un LLM. **LLM real desde el inicio**: sin presupuesto ni key |
| **Servidor SMTP** — **consola en dev** | Envío del enlace de restablecimiento de contraseña | RF-20. En dev el correo se imprime en el log; en producción se cambia `EMAIL_BACKEND` por variable de entorno a SMTP real | Cuenta SMTP real en desarrollo: credenciales en máquinas de desarrollo sin necesidad |
| **API REST de CMEDriver para integradores** (entrada) | ERP/e-commerce crean y consultan servicios con `X-API-Key` | RF-06 / RF-24 | OAuth2 (ver §3) |
| **Webhooks salientes firmados** (salida) | Notificar eventos `servicio.*` (`creado`, `asignado`, `entregado`, `recolectado`, `novedad`, `devuelto`) a URLs registradas, con firma `X-CMEDriver-Signature` (HMAC-SHA256) | RF-25 / RN-07 / RNF-11: el integrador se entera de los cambios sin hacer polling; la entrega es *best-effort* y nunca rompe la petición original | **Que el integrador haga polling a la API**: más carga y latencia. **Cola de mensajes (Celery/RabbitMQ)** para reintentos: infraestructura extra, queda como evolución |

---

## 8. Servicios en la nube

> **Estado real:** CMEDriver **no está desplegado en ninguna nube**. Todo corre en local (`runserver` + `ng serve`). Lo siguiente es la **propuesta** concreta para un despliegue de producción.

| Tecnología (propuesta) | Para qué se usaría | Justificación | Alternativa considerada y por qué se descartó |
|---|---|---|---|
| **Máquina virtual Linux (Ubuntu 24.04 LTS) en un proveedor IaaS** — p. ej. AWS EC2 `t3.small` o un Droplet de DigitalOcean de 2 GB — **propuesta** | Alojar todos los contenedores Docker del sistema (ver §9) | Volumen de una empresa de mensajería pequeña/mediana: una sola VM basta. Control total para ejecutar Daphne (WebSocket de larga duración), Redis y PostgreSQL juntos con costo mensual bajo y predecible | **PaaS (Heroku, Render, Railway)**: más simples, pero el disco es efímero (las evidencias se perderían sin un bucket aparte), los planes gratuitos duermen el proceso (cortan los WebSocket) y el costo crece al añadir BD + Redis. **Kubernetes**: sobredimensionado para este volumen |
| **PostgreSQL gestionado** (p. ej. AWS RDS) — **propuesta, opcional** | BD de producción con backups automáticos | Elimina la administración de backups y parches; alternativa a correr PostgreSQL en contenedor en la misma VM | PostgreSQL en contenedor: más barato; aceptable al inicio si se programa `pg_dump` |
| **Almacenamiento de objetos compatible con S3** (AWS S3 / DigitalOcean Spaces) con `django-storages` — **propuesta, opcional** | Guardar fotos y firmas de evidencia fuera del disco de la VM | Las evidencias son prueba de entrega (RN-02): deben sobrevivir a la recreación de la VM y respaldarse | Volumen Docker local: suficiente al inicio, pero ligado a la VM |
| **Let's Encrypt (Certbot)** — **propuesta** | Certificados TLS para HTTPS/WSS | Los navegadores móviles exigen HTTPS para geolocalización y cámara fuera de `localhost` (necesario para RF-11, RF-14) | Certificado comercial: costo innecesario |
| **Proveedor SMTP transaccional** (p. ej. SendGrid, Amazon SES) — **propuesta** | Envío real del correo de restablecimiento | RF-20 en producción; solo cambia `EMAIL_BACKEND` y credenciales por variables de entorno | Gmail con contraseña de aplicación: límites diarios bajos y mala reputación de envío |

---

## 9. Herramientas de despliegue

| Tecnología | Estado | Para qué se usa / usaría | Justificación | Alternativa considerada y por qué se descartó |
|---|---|---|---|---|
| **pip + `requirements.txt` + venv** | En uso | Instalar dependencias exactas del backend (versiones fijadas con `==`) | Reproducibilidad del entorno Python | Poetry/uv: mejores herramientas, pero `requirements.txt` es lo más simple de explicar y usar |
| **npm + `package-lock.json`** | En uso | Dependencias del frontend; `npm run build` genera `www/` estático | Estándar del ecosistema Angular | Yarn/pnpm: sin ventaja relevante aquí |
| **Angular CLI 22 (`@angular/build`, motor esbuild/Vite)** | En uso | Servidor de desarrollo y build de producción optimizado | Herramienta oficial de Angular | Webpack manual: más configuración |
| **Capacitor CLI 8 + Gradle / Android Studio** | En uso (build nativo parcial) | `npx cap sync android` y `assembleDebug` para generar el APK | Ver §2 | — |
| **Variables de entorno** (`backend/.env.example`) | En uso | `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `FRONTEND_URL`, `EMAIL_BACKEND`, `DEFAULT_FROM_EMAIL` | Separar configuración sensible del código (12-factor); `settings.py` falla si falta la clave secreta con `DEBUG=False` | Claves fijas en `settings.py`: riesgo de filtrarlas al repositorio público |
| **Docker + Docker Compose** | Propuesta | Imágenes `backend` (Daphne) y `frontend` (Nginx con el build), más `postgres` y `redis`, en un solo `docker-compose.yml` | Entorno idéntico en cualquier VM; un comando para levantar todo | Instalación manual en la VM: difícil de reproducir |
| **Nginx** | Propuesta | Proxy inverso con TLS: sirve el frontend estático y `/media/`, y reenvía `/api/`, `/admin/` y `/ws/` (con cabeceras `Upgrade`) a Daphne | Un solo punto de entrada HTTPS/WSS; Django con `DEBUG=False` no sirve `/media/` | Exponer Daphne directamente: sin TLS ni archivos estáticos eficientes |
| **Daphne en producción** (o Uvicorn con workers) | Propuesta | Servidor ASGI de la API y los WebSocket | WebSocket requiere ASGI. *Nota:* [11-manual-distribucion.md](../11-manual-distribucion.md) §6 sugiere gunicorn/waitress (WSGI), que **no** sirven WebSocket; la propuesta correcta es ASGI | Gunicorn WSGI (descartado por lo anterior) |
| **channels-redis + Redis 7** | Propuesta | Capa de canales compartida entre varios procesos Daphne | La capa en memoria actual solo funciona con un proceso; con 2+ workers un mensaje publicado en un proceso no llegaría a sockets abiertos en otro | Seguir con `InMemoryChannelLayer`: válido solo con un único proceso |
| **GitHub Actions** | Propuesta | CI: ejecutar `manage.py test` y `ng build` en cada push / pull request | Detectar regresiones automáticamente; integrado con el repositorio en GitHub | Jenkins/GitLab CI: requiere servidor o migrar el repositorio |

---

## 10. Control de versiones

| Tecnología | Para qué se usa en CMEDriver | Justificación | Alternativa descartada |
|---|---|---|---|
| **Git** | Historial del código y de la documentación (`docs/` vive en el mismo repo) | Trazabilidad de cada cambio; documentación versionada junto al código que describe | SVN: centralizado, sin ramas ligeras |
| **GitHub** (<https://github.com/javier5254/CEMDriver>) | Repositorio remoto, entrega del proyecto, renderizado de Markdown y Mermaid | Visualización directa de docs y diagramas Mermaid; base para la propuesta de CI con GitHub Actions | GitLab/Bitbucket: equivalentes; GitHub es el estándar académico y renderiza Mermaid nativamente |
| **`.gitignore`** | Excluye `.venv/`, `db.sqlite3`, `media/`, `.env`, `node_modules/`, `www/` | Evita subir datos locales, evidencias y secretos al repositorio público | — |

---

## 11. Otras herramientas (pruebas, documentación, diagramas)

| Tecnología y versión | Para qué se usa en CMEDriver | Justificación (necesidad concreta) | Alternativa considerada y por qué se descartó |
|---|---|---|---|
| **drf-spectacular 0.30.0** (OpenAPI 3 + Swagger UI) | Esquema `/api/schema/` y documentación interactiva `/api/docs/` generados desde el código | RNF-03: la API debe estar documentada para soportar integraciones externas (RF-06); se mantiene sincronizada automáticamente | **drf-yasg**: solo genera OpenAPI 2 (Swagger 2.0) y tiene menos mantenimiento. Documentación manual: se desactualiza |
| **Django test framework + DRF `APITestCase` / `APIClient`** | 96 pruebas automatizadas del backend (`manage.py test`, scripts `run_tests.sh` / `run_tests.ps1`) | Verificar reglas de negocio (RN-01 a RN-08) y permisos por rol (RNF-02) | **pytest-django**: más cómodo, pero dependencia extra; el runner de Django ya cubre la necesidad |
| **`channels.testing.WebsocketCommunicator`** | Pruebas de conexión, autorización y mensajes de los consumers | RF-27 y la autorización por servicio del WebSocket | Pruebas manuales en navegador únicamente |
| **`unittest.mock.patch`** | Aislar Nominatim y los receptores de webhooks en las pruebas | Pruebas deterministas sin acceso a internet | Llamar a los servicios reales: pruebas lentas e inestables |
| **Vitest 4 + jsdom** (configurado) | Runner de pruebas unitarias del frontend (`npm test`) | Viene con la plantilla de Angular moderna. **Estado real: no hay archivos `*.spec.ts` escritos**; las pruebas del frontend fueron manuales en navegador | Karma/Jasmine: ya deprecado en Angular reciente |
| **ESLint 9 + angular-eslint 22 + typescript-eslint** | Análisis estático del frontend (`npm run lint`) | Calidad y estilo uniforme del código TypeScript | TSLint: deprecado |
| **Mermaid** + **@mermaid-js/mermaid-cli** | Diagramas como texto (`docs/diagrams/src/*.mmd`) renderizados a PNG con tema propio (`mermaid-theme.json`) | Diagramas versionables y regenerables; GitHub los muestra en línea | Draw.io/Visio: binarios difíciles de versionar y revisar |
| **SVG a mano** | Diagramas de casos de uso y C4 | Mermaid no tiene casos de uso UML maduros y su auto-layout del C4 solapaba texto | PlantUML: requiere Java/servidor de render |
| **Panel de administración de Django** (`/admin/`) | Inspección y corrección de datos durante desarrollo y demo | Gratis con Django; acelera pruebas manuales | Construir pantallas de administración propias para todo |
