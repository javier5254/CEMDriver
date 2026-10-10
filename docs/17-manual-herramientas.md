# Manual de herramientas, arquitecturas y modelos usados — CMEDriver (v2)

> **Nota (2026-10-09):** este documento es **histórico**: se redactó antes de la reducción de alcance que retiró el inventario, los pagos y el chatbot (el chat quedó solo como canal entre el cliente y el motorizado) y **no refleja el alcance vigente**. Lista como parte del stack el chatbot con modelo de lenguaje simulado y la pasarela de pagos simulada, y 9 apps Django; la lista vigente está en [entrega/02-stack-tecnologico.md](entrega/02-stack-tecnologico.md). Prevalece la documentación de [entrega/](entrega/00-guia-de-entrega.md), en particular [entrega/01-requerimientos.md §2.4](entrega/01-requerimientos.md#24-cambios-de-alcance).

Referencia de todo lo que compone el proyecto: lenguajes, frameworks, librerías, modelos de arquitectura y herramientas de diseño/documentación, con el motivo de cada elección.

## 1. Backend

| Herramienta | Versión usada | Rol en el proyecto | Por qué se eligió |
|---|---|---|---|
| **Python** | 3.12 | Lenguaje del backend | Estándar de la industria para APIs rápidas de construir, gran ecosistema |
| **Django** | 6.1 | Framework web / ORM | Incluye ORM, sistema de migraciones, panel de administración y autenticación listos para usar |
| **Django REST Framework (DRF)** | 3.18 | Construcción de la API REST | Serializers, ViewSets, permisos y routers estándar para exponer el dominio como API |
| **djangorestframework-simplejwt** | 5.5 | Autenticación JWT | Login basado en tokens (access/refresh), acepta usuario o correo |
| **Django Channels + Daphne** | 4.3 / 4.2 | WebSockets (tracking y chat en tiempo real) | Reemplaza el polling del MVP inicial por push real; capa de canales en memoria, sin depender de Redis en desarrollo |
| **django-cors-headers** | 4.9 | CORS | Permite que el frontend (otro origen/puerto) consuma la API desde el navegador |
| **drf-spectacular** | 0.30 | Documentación OpenAPI/Swagger | Genera la documentación interactiva de la API (`/api/docs/`) automáticamente desde el código |
| **Pillow** | 12.3 | Manejo de imágenes | Requerido por los `ImageField` de Django (evidencia: foto y firma) |
| **`django.core.mail`** (backend de consola en dev) | incluido en Django | Envío de correos (reset de contraseña) | Sin necesidad de una cuenta SMTP real para desarrollar/demostrar; cambiar a un proveedor real es una sola configuración |
| **Nominatim (OpenStreetMap)** | API pública HTTP | Geocoding de direcciones para la optimización de rutas | Gratuito, sin API key; se respeta su límite de 1 req/seg |
| **SQLite** | incluido en Python | Base de datos (desarrollo) | Cero configuración, arranca de inmediato |
| **PostgreSQL** | (sugerido, producción) | Base de datos (producción) | Motor recomendado para producción real, mismo ORM sin cambios de código |

## 2. Frontend

| Herramienta | Rol en el proyecto | Por qué se eligió |
|---|---|---|
| **Angular** | Framework SPA | Estructura robusta (componentes, routing, servicios, inyección de dependencias) para una app con 4 áreas por rol |
| **Ionic** (`mode: 'ios'`) | Librería de componentes UI | Componentes táctiles listos; en v2 se fuerza el modo iOS (en vez del Material por defecto) como parte del rediseño visual |
| **Leaflet + OpenStreetMap** | Mapas para el tracking | Sin necesidad de API key ni cuenta de facturación |
| **signature_pad** | Captura de firma digital | Librería ligera basada en `<canvas>` para firmar sobre pantalla táctil |
| **WebSocket nativo del navegador** | Cliente de tiempo real (tracking, chat) | Sin librería adicional; con fallback automático a polling si la conexión falla (RNF-10) |
| **Capacitor** (`@capacitor/android`, `@capacitor/ios`) | Empaquetado nativo | Permite compilar la misma app Ionic/Angular como proyecto Android/iOS nativo — ver estado real en [11-manual-distribucion.md](11-manual-distribucion.md) |
| **Vite** (vía Angular CLI) | Servidor de desarrollo / bundler | Motor de build del Angular CLI moderno (`ng serve`), recarga en caliente rápida |

## 3. Modelos y estilos de arquitectura aplicados

| Modelo/patrón | Dónde se aplica | Propósito |
|---|---|---|
| **API REST** | Toda la comunicación frontend-backend | Contrato claro, reutilizable también por integraciones externas (ver [05-api.md](05-api.md)) |
| **Arquitectura por capas (MVC-like de Django)** | Backend: `models.py` / `serializers.py` / `views.py` | Separación entre datos, transformación/validación y lógica de exposición HTTP |
| **Diseño modular por dominio ("apps" Django)** | `accounts`, `coverage`, `inventory`, `services`, `tracking`, `optimization`, `chatbot`, `payments`, `integrations` | Cada dominio de negocio aislado, facilita evolucionar a microservicios (RNF-08); las 4 apps nuevas de v2 se construyeron sin modificar los modelos existentes |
| **RBAC (Role-Based Access Control)** + **API Key** | Permisos DRF (`accounts/permissions.py`) + `integrations.authentication.ApiKeyAuthentication` | Control de acceso alineado a los 4 roles humanos, más un mecanismo de autenticación para sistemas externos sin usuario humano |
| **Máquina de estados finita** | Ciclo de vida de `Servicio` (`EstadoServicio`) | Modela formalmente las transiciones válidas de un servicio (ver [15-diagrama-flujo.md](15-diagrama-flujo.md)) |
| **Publish/Subscribe (WebSockets, Channel Layers)** | Tracking GPS y chat en tiempo real | Un evento (posición nueva, mensaje nuevo) se difunde a todos los suscritos a un grupo (`tracking_<id>`, `chat_<id>`) sin que ellos pregunten (push, no polling) |
| **Webhooks salientes firmados (HMAC)** | `integrations.services.disparar_webhook` | Patrón estándar de notificación a sistemas externos sobre cambios de estado, con verificación de autenticidad por firma |
| **Strategy / adaptador intercambiable** | `MockLLMClient` (chatbot), `MockPaymentProvider` (pagos) | Aísla la lógica de negocio detrás de una interfaz para poder sustituir la implementación simulada por una real (LLM, pasarela de pago) sin tocar el resto del código (RNF-13) |
| **C4 Model** | Documentación de arquitectura ([14-diagrama-c4.md](14-diagrama-c4.md)) | Estándar para documentar arquitectura de software en niveles de zoom (contexto, contenedores) |
| **SPA (Single Page Application)** | Frontend Ionic + Angular | Una sola carga de página, navegación por rutas del lado del cliente |

## 4. Documentación, diagramación y diseño

| Herramienta | Rol | Por qué se eligió |
|---|---|---|
| **Mermaid** | Diagramas de clases, ER, flujo | Se escribe como texto plano versionable junto al código, se renderiza automáticamente en GitHub/VS Code y se puede exportar a imagen |
| **@mermaid-js/mermaid-cli (mmdc)** | Render de los `.mmd` a imagen PNG, con tema personalizado ([diagrams/src/mermaid-theme.json](diagrams/src/mermaid-theme.json)) para que la paleta iOS coincida con mockups y SVGs a mano | Permite generar las imágenes de los diagramas sin depender de un visor externo, para incrustarlas en Word/PDF |
| **SVG a mano** | Casos de uso, uno por actor ([diagrams/casos-uso-administrador.svg](diagrams/casos-uso-administrador.svg), [-alistador](diagrams/casos-uso-alistador.svg), [-motorizado](diagrams/casos-uso-motorizado.svg), [-cliente](diagrams/casos-uso-cliente.svg)) y C4 ([diagrams/c4-contexto.svg](diagrams/c4-contexto.svg), [diagrams/c4-contenedores.svg](diagrams/c4-contenedores.svg)) | Mermaid no tiene soporte maduro para casos de uso UML, y su auto-layout para C4 dejaba texto solapado; SVG a mano da control total del layout y de la paleta visual (tema iOS, sombras suaves) |
| **Claude Design (canvas de mockups)** | Mockups de las pantallas ([12-mockups.md](12-mockups.md)) | Prototipado visual rápido de las pantallas clave sin necesidad de una herramienta de diseño externa |
| **Markdown** | Toda la documentación (`docs/`) | Texto plano, versionable en el mismo repositorio que el código, se lee bien en cualquier editor o en GitHub |

## 5. Pruebas

| Herramienta | Rol | Por qué se eligió |
|---|---|---|
| **Django test framework (`manage.py test`) + `rest_framework.test.APITestCase`** | Pruebas automatizadas del backend (REST) | Viene incluido con Django/DRF, corre contra una base de datos de prueba aislada |
| **`channels.testing.WebsocketCommunicator`** | Pruebas automatizadas de los consumers de WebSocket | Permite probar conexión, autorización y mensajes en tiempo real sin un navegador real, con métodos de test `async def` |
| **`APIClient` / `force_authenticate`** | Simular peticiones autenticadas por rol en las pruebas | Evita tener que hacer login real (HTTP) en cada prueba, más rápido y aislado |
| **`unittest.mock.patch`** | Aislar llamadas de red en pruebas (geocoding, webhooks) | Las pruebas nunca dependen de servicios externos reales (Nominatim, un receptor HTTP) — deterministas y sin acceso a internet |

Ver [16-plan-pruebas.md](16-plan-pruebas.md) para el detalle de casos de prueba y cómo ejecutarlos.

## 6. Resumen de decisiones "por qué no X"
| Se usó | En vez de | Motivo principal |
|---|---|---|
| SQLite (dev) | PostgreSQL desde el día 1 | Cero instalación, arranca al instante |
| WebSockets (Channels) con fallback a polling | Solo WebSockets, o solo polling | Tiempo real real, pero resiliente: si el socket falla, la app sigue funcionando por polling (RNF-10) |
| Leaflet + OSM (tiles) + Nominatim (geocoding) | Google Maps Platform | Sin API key ni facturación, aceptando el límite de tasa de Nominatim |
| Chatbot con arquitectura real de tool-calling + modelo **simulado** | LLM real desde el inicio | No había API key de un proveedor de LLM disponible; se prefirió construir el patrón de integración real (reutilizable) en vez de posponerlo |
| Pasarela de pago **simulada** | Integrar Wompi/PayU real | No había credenciales de comercio disponibles; mismo patrón de intercambiabilidad que el chatbot |
| API Key propia | OAuth2 client-credentials | Mucho más simple de implementar y explicar en un MVP académico |
| Django REST Framework | FastAPI | Django trae ORM + admin + auth integrados, ideal para ir rápido manteniendo todo en un solo framework |
