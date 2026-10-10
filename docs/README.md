# Índice de documentación — CMEDriver

> **Nota (2026-10-09): cambio de alcance.** El autor redujo el alcance del proyecto: se retiraron el **inventario, los pagos y el chatbot** (código incluido), y el chat quedó solo como canal entre el cliente y el motorizado. Los documentos numerados **01 a 17 de esta carpeta** y todo `v1/` son **históricos**: se redactaron antes de ese cambio y **no reflejan el alcance vigente** (todavía describen inventario, pagos, chatbot, 9 apps y 17 entidades). **Prevalece [entrega/](entrega/00-guia-de-entrega.md)**, que se verificó contra el código actual (6 apps, 12 entidades y 72 pruebas). Si un documento histórico contradice a uno de `entrega/`, vale el de `entrega/`. El detalle del cambio está en [entrega/01-requerimientos.md §2.4](entrega/01-requerimientos.md#24-cambios-de-alcance).

## Entrega final (docs/entrega/) — vigente

Documentos consolidados de la entrega final, verificados contra el código y ajustados al alcance vigente. Prevalecen sobre los documentos históricos de la tabla siguiente cuando hay diferencias.

| # | Documento | Contenido |
|---|---|---|
| 00 | [Guía de la entrega](entrega/00-guia-de-entrega.md) | Mapa consigna → documento y sección; recorrido sugerido para la sustentación; pendientes del autor |
| 01 | [Requerimientos](entrega/01-requerimientos.md) | Problema, objetivos, actores, RF, RNF, reglas de negocio (RN), restricciones (RES), hallazgos H-01…H-13 y cambios de alcance (§2.4) |
| 02 | [Stack tecnológico](entrega/02-stack-tecnologico.md) | Tecnologías usadas con su justificación y las alternativas descartadas |
| 03 | [Arquitectura](entrega/03-arquitectura.md) | Estilo arquitectónico, diagrama general, componentes, las 6 apps del backend, seguridad, despliegue actual y propuesto |
| 04 | [Modelo entidad-relación](entrega/04-mer.md) | MER de 12 entidades, diccionario de datos, relaciones, restricciones y cambios de alcance |
| 05 | [BPMN](entrega/05-bpmn.md) | Modelado del proceso de negocio «Ciclo de vida de un servicio de mensajería» |
| 06 | [Modelo C4](entrega/06-c4.md) | Contexto, contenedores, componentes y código |
| 07 | [Matriz de trazabilidad](entrega/07-trazabilidad.md) | Relación entre requerimientos, reglas, componentes y pruebas |
| 08 | [Limitaciones y mejoras](entrega/08-limitaciones-y-mejoras.md) | Limitaciones conocidas LIM-01…LIM-39 (35 vigentes y 4 resueltas por reducción de alcance), servicio simulado (correo) y hoja de ruta |

## Documentos históricos (docs/01 a docs/17) — NO reflejan el alcance vigente

Anteriores a la reducción de alcance del 2026-10-09. Se conservan como registro del proceso del proyecto. Cada uno que menciona inventario, pagos o chatbot lleva al inicio una nota que lo indica. Para el alcance vigente, ver `entrega/`.

| # | Documento | Contenido (histórico) |
|---|---|---|
| 01 | [Project charter](01-project-charter.md) | Problema, objetivos, alcance del MVP, innovación, stakeholders |
| 02 | [Requisitos](02-requisitos.md) | Historias de usuario (RF), requerimientos no funcionales (RNF), reglas de negocio (RN); incluye los retirados (inventario, pagos, chatbot) |
| 03 | [Arquitectura](03-arquitectura.md) | Stack técnico, 9 apps del backend (3 retiradas), seguridad/RBAC, decisiones de diseño (ADR) |
| 04 | [Modelo de datos](04-modelo-datos.md) | Diagrama entidad-relación de 17 entidades (imagen + Mermaid); el vigente tiene 12 |
| 05 | [Diseño de API](05-api.md) | Contrato de endpoints REST por módulo; incluye `/api/productos/`, `/api/pagos/` y `/api/chatbot/`, ya eliminados |
| 06 | [Cronograma](06-cronograma.md) | Fases, hitos y diagrama de Gantt |
| 07 | [Roadmap futuro](07-roadmap-futuro.md) | Qué se completó en v2 vs. trabajo futuro; lista como pendientes el chatbot con LLM real, los pagos y el inventario |
| 08 | [Diagrama de clases](08-diagrama-clases.md) | UML de clases (imagen + Mermaid) con las 9 apps anteriores al cambio |
| 09 | [Formatos de historias/requisitos](09-formatos-historias-requisitos.md) | Plantillas en blanco para nuevas HU / RF / RNF / RN (siguen siendo utilizables) |
| 10 | [Diagrama de casos de uso](10-diagrama-casos-uso.md) | UML de casos de uso (SVG) + tabla de actores/relaciones; incluye inventario, chatbot y compra |
| 11 | [Manual de distribución](11-manual-distribucion.md) | Instalación, despliegue a producción, backups, troubleshooting (contenido operativo ajustado al alcance vigente) |
| 12 | [Mockups](12-mockups.md) | Enlace al canvas de mockups navegable + notas de diseño; incluye la pantalla del chatbot |
| 13 | [RF y RNF completos](13-rf-rnf-completos.md) | Requerimientos diligenciados con criterio de verificación; incluye los retirados |
| 14 | [Diagrama C4](14-diagrama-c4.md) | Contexto (C1) y Contenedores (C2); el vigente está en [entrega/06-c4.md](entrega/06-c4.md) |
| 15 | [Diagrama de flujo](15-diagrama-flujo.md) | Proceso end-to-end de un servicio, con bifurcaciones (no depende de lo retirado) |
| 16 | [Plan de pruebas](16-plan-pruebas.md) | Casos de prueba y cómo ejecutar la suite; cuenta 93 pruebas y conserva casos `T-INV-*`, `T-BOT-*` y `T-PAG-*`. La suite vigente tiene 72 |
| 17 | [Manual de herramientas](17-manual-herramientas.md) | Todo el stack, modelos de arquitectura y herramientas de diseño usados, con justificación |

## Otros archivos de este directorio
- [diagrams/](diagrams/) — fuentes Mermaid/SVG (`src/`) e imágenes renderizadas (`img/`) de todos los diagramas. Los de la entrega (`arquitectura-general`, `mer-entrega`, `bpmn-ciclo-servicio`, `c4-*`) están al día; los demás (`er`, `clases`, casos de uso, `c4-contexto` y `c4-contenedores`) son históricos
- [mockups/](mockups/) — fuentes editables de los mockups (`.dc.html`), históricos
- [v1/](v1/) — snapshot congelado de toda la documentación, diagramas y mockups tal como estaban al cierre del MVP (antes de las funcionalidades v2: auth por correo, tiempo real, chatbot conversacional, optimización de rutas, pagos e integraciones). Histórico
