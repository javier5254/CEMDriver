# Manual de herramientas, arquitecturas y modelos usados — CMEDriver

Referencia de todo lo que compone el proyecto: lenguajes, frameworks, librerías, modelos de arquitectura y herramientas de diseño/documentación, con el motivo de cada elección.

## 1. Backend

| Herramienta | Versión usada | Rol en el proyecto | Por qué se eligió |
|---|---|---|---|
| **Python** | 3.12 | Lenguaje del backend | Estándar de la industria para APIs rápidas de construir, gran ecosistema |
| **Django** | 6.1 | Framework web / ORM | Incluye ORM, sistema de migraciones, panel de administración y autenticación listos para usar — acelera muchísimo un MVP |
| **Django REST Framework (DRF)** | 3.18 | Construcción de la API REST | Serializers, ViewSets, permisos y routers estándar para exponer el dominio como API |
| **djangorestframework-simplejwt** | 5.5 | Autenticación JWT | Login basado en tokens (access/refresh), estándar para SPAs y apps móviles |
| **django-cors-headers** | 4.9 | CORS | Permite que el frontend (otro origen/puerto) consuma la API desde el navegador |
| **drf-spectacular** | 0.30 | Documentación OpenAPI/Swagger | Genera la documentación interactiva de la API (`/api/docs/`) automáticamente desde el código |
| **Pillow** | 12.3 | Manejo de imágenes | Requerido por los `ImageField` de Django (evidencia: foto y firma) |
| **SQLite** | incluido en Python | Base de datos (desarrollo) | Cero configuración, arranca de inmediato — pensado para el MVP en horas |
| **PostgreSQL** | (sugerido, producción) | Base de datos (producción) | Motor recomendado para producción real, mismo ORM sin cambios de código |

## 2. Frontend

| Herramienta | Rol en el proyecto | Por qué se eligió |
|---|---|---|
| **Angular** | Framework SPA | Estructura robusta (componentes, routing, servicios, inyección de dependencias) para una app con 4 áreas por rol |
| **Ionic** | Librería de componentes UI | Componentes táctiles listos (listas, tarjetas, tabs) pensados para verse bien tanto en navegador de escritorio como en celular, sin escribir CSS desde cero |
| **Leaflet + OpenStreetMap** | Mapas para el tracking | Sin necesidad de API key ni cuenta de facturación (a diferencia de Google Maps), suficiente para el MVP |
| **signature_pad** | Captura de firma digital | Librería ligera basada en `<canvas>` para firmar sobre pantalla táctil |
| **Vite** (vía Angular CLI) | Servidor de desarrollo / bundler | Es el motor de build que usa el Angular CLI moderno (`ng serve`) — recarga en caliente rápida durante desarrollo |

## 3. Modelos y estilos de arquitectura aplicados

| Modelo/patrón | Dónde se aplica | Propósito |
|---|---|---|
| **API REST** | Toda la comunicación frontend-backend | Contrato claro, reutilizable también por integraciones externas (ver [05-api.md](05-api.md)) |
| **Arquitectura por capas (MVC-like de Django)** | Backend: `models.py` / `serializers.py` / `views.py` | Separación entre datos, transformación/validación y lógica de exposición HTTP |
| **Diseño modular por dominio ("apps" Django)** | `accounts`, `coverage`, `inventory`, `services`, `tracking` | Cada dominio de negocio aislado, facilita evolucionar a microservicios (RNF-08) |
| **RBAC (Role-Based Access Control)** | Permisos DRF por endpoint (`accounts/permissions.py`) | Control de acceso alineado a los 4 roles del negocio |
| **Máquina de estados finita** | Ciclo de vida de `Servicio` (`EstadoServicio`) | Modela formalmente las transiciones válidas de un servicio (ver [15-diagrama-flujo.md](15-diagrama-flujo.md)) |
| **C4 Model** | Documentación de arquitectura ([14-diagrama-c4.md](14-diagrama-c4.md)) | Estándar para documentar arquitectura de software en 4 niveles de zoom (contexto, contenedores, componentes, código) |
| **SPA (Single Page Application)** | Frontend Ionic + Angular | Una sola carga de página, navegación por rutas del lado del cliente |

## 4. Documentación, diagramación y diseño

| Herramienta | Rol | Por qué se eligió |
|---|---|---|
| **Mermaid** | Diagramas de clases, ER, flujo | Se escribe como texto plano versionable junto al código, se renderiza automáticamente en GitHub/VS Code y se puede exportar a imagen |
| **@mermaid-js/mermaid-cli (mmdc)** | Render de los `.mmd` a imagen PNG | Permite generar las imágenes de los diagramas sin depender de un visor externo, para incrustarlas en Word/PDF |
| **SVG a mano** | Casos de uso ([diagrams/casos-uso.svg](diagrams/casos-uso.svg)) y C4 ([diagrams/c4-contexto.svg](diagrams/c4-contexto.svg), [diagrams/c4-contenedores.svg](diagrams/c4-contenedores.svg)) | Mermaid no tiene soporte maduro para casos de uso UML, y su auto-layout para C4 dejaba texto solapado; SVG a mano da control total del layout para un resultado limpio |
| **Claude Design (canvas de mockups)** | Mockups de las pantallas ([12-mockups.md](12-mockups.md)) | Prototipado visual rápido de las pantallas clave sin necesidad de una herramienta de diseño externa |
| **Markdown** | Toda la documentación (`docs/`) | Texto plano, versionable en el mismo repositorio que el código, se lee bien en cualquier editor o en GitHub |

## 5. Pruebas

| Herramienta | Rol | Por qué se eligió |
|---|---|---|
| **Django test framework (`manage.py test`) + `rest_framework.test.APITestCase`** | Pruebas automatizadas del backend | Viene incluido con Django/DRF, no requiere dependencias nuevas, corre contra una base de datos de prueba aislada (se crea y destruye sola en cada corrida) |
| **`APIClient` / `force_authenticate`** | Simular peticiones autenticadas por rol en las pruebas | Evita tener que hacer login real (HTTP) en cada prueba, más rápido y aislado |

Ver [16-plan-pruebas.md](16-plan-pruebas.md) para el detalle de casos de prueba y cómo ejecutarlos.

## 6. Resumen de decisiones "por qué no X"
| Se usó | En vez de | Motivo principal |
|---|---|---|
| SQLite (dev) | PostgreSQL desde el día 1 | Cero instalación, arranca al instante |
| Polling HTTP | WebSockets (Django Channels) | Menos infraestructura para un MVP de pocas horas |
| Leaflet + OSM | Google Maps Platform | Sin API key ni facturación |
| Chatbot por menús (frontend) | Backend de chatbot con NLU/LLM | El chatbot del MVP es determinístico; se documenta como evolución en [07-roadmap-futuro.md](07-roadmap-futuro.md) |
| Django REST Framework | FastAPI | Django trae ORM + admin + auth integrados, ideal para ir rápido en el MVP mantendo todo en un solo framework |
