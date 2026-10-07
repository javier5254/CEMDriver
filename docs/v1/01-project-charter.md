# Project Charter — CMEDriver

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

**Fuera de alcance del MVP** (ver [07-roadmap-futuro.md](07-roadmap-futuro.md)):
- Tracking en tiempo real por WebSockets/streaming continuo.
- Chatbot con LLM/IA generativa.
- Óptimización automática de rutas (ruteo inteligente).
- App móvil nativa compilada (Capacitor/App Store/Play Store) — el MVP corre como app Ionic/Angular en navegador.
- Pasarela de pagos real.

## 6. Justificación de la innovación
El diferenciador del proyecto no es "otro sistema de mensajería", sino:
- Una **API-first platform**: todo lo que hacen las interfaces web pasa por una API REST documentada, pensada para que terceros (e-commerce, ERPs) puedan crear e integrar servicios.
- Un **chatbot de autogestión** conectado al inventario, que reduce la fricción del cliente para comprar o pedir una recolección.
- Una arquitectura pensada para escalar por módulos (cobertura, inventario, tracking, chatbot como servicios independientes desde el día 1, aunque el MVP los corra en un solo backend).

## 7. Stakeholders
| Rol | Interés |
|---|---|
| Estudiante(s) / equipo de desarrollo | Entregar el proyecto de grado/curso |
| Docente / evaluador | Validar cumplimiento de requisitos académicos y calidad técnica |
| Administrador del centro de mensajería (usuario simulado) | Controlar operación y cobertura |
| Alistador (usuario simulado) | Operar la creación/asignación de servicios |
| Motorizado (usuario simulado) | Ejecutar servicios en campo |
| Cliente final (usuario simulado) | Recibir/solicitar servicios con visibilidad total |
