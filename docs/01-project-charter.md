# Project Charter — CMEDriver (v2)

> Este documento describe el proyecto en su versión v2 (expandida). La versión original del MVP queda congelada en [docs/v1/](v1/) tal como se entregó primero.

> **Nota (octubre de 2026):** la problemática, la pregunta y los objetivos vigentes son los del paper del proyecto y están en [entrega/01-requerimientos.md §1–§2](entrega/01-requerimientos.md#1-problema-o-necesidad-identificada). Las secciones 2 a 4 de este charter se conservan como registro histórico.

## 1. Nombre del proyecto
**CMEDriver** — Plataforma de gestión de servicios de mensajería (entregas y recolecciones) con tracking en tiempo real, chatbot de autogestión para clientes e inventario integrado.

## 2. Problema
Los centros de mensajería/courier operan hoy con procesos manuales o herramientas desconectadas entre sí: asignación de rutas por teléfono/WhatsApp, sin visibilidad del cliente sobre dónde está su pedido, sin evidencia digital de entrega/recolección, y sin un canal de autoservicio para que el cliente compre o solicite una recolección sin llamar.

## 3. Objetivo general
Construir una plataforma web/móvil que permita administrar, alistar, transportar y hacer seguimiento en tiempo real de servicios de mensajería (entrega y recolección), con un canal de autogestión (chatbot) e inventario de productos para el cliente final.

## 4. Objetivos específicos
1. Permitir a un administrador crear usuarios y parametrizar la matriz de cobertura (zonas, leadtime, fechas de agenda disponibles).
2. Permitir a un alistador crear servicios (manual o vía API) y asignarlos a rutas/motorizados.
3. Permitir a un motorizado ejecutar el servicio (recibir en centro o recoger en dirección del cliente, con foto y firma) y reportar novedades.
4. Dar al cliente una vista de tracking en tiempo real, un canal de chat con el motorizado, y la posibilidad de planificar sus propias recolecciones.
5. Ofrecer un chatbot guiado para que el cliente compre productos o solicite una recolección según el catálogo parametrizado.
6. Diseñar la plataforma con una API pública clara, pensada para integraciones externas y escalabilidad futura.

## 5. Alcance del MVP (Fase 1 + parte de Fase 2)
**Incluye:**
- Login con 3 roles (Administrador, Alistador, Motorizado) + vista de Cliente.
- CRUD de usuarios y matriz de cobertura (zona → leadtime → fechas de agenda disponibles).
- Creación de servicios (tipo Entrega / Recolección), asignación a ruta y motorizado.
- Flujo diferenciado en la app del motorizado según tipo de servicio.
- Captura de evidencia (foto + firma digital) en recolecciones.
- Registro de novedades (reintento / devolución al centro).
- Tracking GPS por polling (no websockets en el MVP) visible para cliente y administrador.
- Chat cliente–motorizado por mensajería simple (polling).
- Chatbot guiado por menús (sin LLM) conectado al inventario, para comprar o solicitar recolección.
- Inventario básico de productos parametrizable por centro de mensajería.
- Planificación de recolecciones por el propio cliente, respetando la matriz de cobertura/leadtime.

## 5.1 Alcance de v2 (adicional al MVP)
- Autenticación con correo electrónico + restablecimiento de contraseña por correo.
- Tracking y chat en **tiempo real de verdad** (WebSockets, Django Channels), con respaldo automático a polling.
- **Chatbot conversacional** (texto libre, no solo menús) con arquitectura real de tool-calling — modelo de lenguaje simulado por falta de API key real.
- **Pagos** generados automáticamente al comprar por el chatbot — proveedor de pago simulado por falta de credenciales reales.
- **Optimización de rutas**: geocoding real (Nominatim/OpenStreetMap) + sugerencia de orden de visita (vecino más cercano).
- **API Keys y Webhooks**: integración real para sistemas externos, sin necesidad de un usuario humano.
- **Inventario avanzado**: un servicio puede tener varias líneas de producto con cantidad.
- **Rediseño visual** inspirado en el lenguaje de diseño de Apple (iOS/macOS) en vez del Material Design por defecto.
- **Empaquetado nativo** (Capacitor) configurado para Android — ver limitación real de build en [11-manual-distribucion.md](11-manual-distribucion.md).

Lo que queda genuinamente fuera de alcance incluso en v2 está en [07-roadmap-futuro.md](07-roadmap-futuro.md) (ej. LLM real, pasarela de pago real, ruteo multi-vehículo, build nativo verificado).

## 6. Justificación de la innovación
El diferenciador del proyecto no es "otro sistema de mensajería", sino:
- Una **API-first platform**: todo lo que hacen las interfaces web pasa por una API REST documentada, y en v2 esto se volvió real — sistemas externos pueden autenticarse con una API Key propia y recibir webhooks firmados sobre cambios de estado, sin necesitar un usuario humano.
- Un **chatbot conversacional** conectado al inventario, la cobertura y los pagos, que reduce la fricción del cliente para comprar o pedir una recolección — con una arquitectura de tool-calling real, lista para un modelo de lenguaje real cuando haya credenciales.
- Una **optimización de rutas** basada en geocoding real, no solo agrupación por zona — un componente genuinamente algorítmico, no solo CRUD.
- Una arquitectura modular por dominio (9 apps Django independientes) pensada para escalar a microservicios desde el día 1.

## 7. Stakeholders
| Rol | Interés |
|---|---|
| Estudiante(s) / equipo de desarrollo | Entregar el proyecto de grado/curso |
| Docente / evaluador | Validar cumplimiento de requisitos académicos y calidad técnica |
| Administrador del centro de mensajería (usuario simulado) | Controlar operación y cobertura |
| Alistador (usuario simulado) | Operar la creación/asignación de servicios |
| Motorizado (usuario simulado) | Ejecutar servicios en campo |
| Cliente final (usuario simulado) | Recibir/solicitar servicios con visibilidad total |
