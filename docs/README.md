# Índice de documentación — CMEDriver

| # | Documento | Contenido |
|---|---|---|
| 01 | [Project charter](01-project-charter.md) | Problema, objetivos, alcance del MVP, innovación, stakeholders |
| 02 | [Requisitos](02-requisitos.md) | Historias de usuario (RF), requerimientos no funcionales (RNF), reglas de negocio (RN) |
| 03 | [Arquitectura](03-arquitectura.md) | Stack técnico, apps del backend, seguridad/RBAC, decisiones de diseño (ADR) |
| 04 | [Modelo de datos](04-modelo-datos.md) | Diagrama entidad-relación (imagen + Mermaid) |
| 05 | [Diseño de API](05-api.md) | Contrato de endpoints REST por módulo |
| 06 | [Cronograma](06-cronograma.md) | Fases, hitos y diagrama de Gantt |
| 07 | [Roadmap futuro](07-roadmap-futuro.md) | Qué se completó en v2 vs. trabajo futuro genuino que queda fuera de alcance |
| 08 | [Diagrama de clases](08-diagrama-clases.md) | UML de clases (imagen + Mermaid), derivado del código real |
| 09 | [Formatos de historias/requisitos](09-formatos-historias-requisitos.md) | Plantillas en blanco para nuevas HU / RF / RNF / RN |
| 10 | [Diagrama de casos de uso](10-diagrama-casos-uso.md) | UML de casos de uso (SVG) + tabla de actores/relaciones |
| 11 | [Manual de distribución](11-manual-distribucion.md) | Instalación, despliegue a producción, backups, troubleshooting |
| 12 | [Mockups](12-mockups.md) | Enlace al canvas de mockups navegable + notas de diseño |
| 13 | [RF y RNF completos](13-rf-rnf-completos.md) | Todos los requerimientos diligenciados con criterio de verificación |
| 14 | [Diagrama C4](14-diagrama-c4.md) | Contexto (C1) y Contenedores (C2) |
| 15 | [Diagrama de flujo](15-diagrama-flujo.md) | Proceso end-to-end de un servicio, con bifurcaciones |
| 16 | [Plan de pruebas](16-plan-pruebas.md) | Casos de prueba y cómo ejecutar la suite automatizada |
| 17 | [Manual de herramientas](17-manual-herramientas.md) | Todo el stack, modelos de arquitectura y herramientas de diseño usados, con justificación |

## Entrega final (docs/entrega/)

Documentos consolidados de la entrega final, verificados contra el código. Prevalecen sobre los documentos históricos de la tabla anterior cuando hay diferencias.

| # | Documento | Contenido |
|---|---|---|
| 01 | [Requerimientos](entrega/01-requerimientos.md) | Problema, objetivos, actores, RF, RNF, reglas de negocio (RN), restricciones (RES) y hallazgos H-01…H-12 |
| 02 | [Stack tecnológico](entrega/02-stack-tecnologico.md) | Tecnologías usadas con su justificación y las alternativas descartadas |
| 03 | [Arquitectura](entrega/03-arquitectura.md) | Estilo arquitectónico, diagrama general, componentes, seguridad, despliegue actual y propuesto |
| 04 | [Modelo entidad-relación](entrega/04-mer.md) | MER, diccionario de datos, relaciones y restricciones |
| 05 | [BPMN](entrega/05-bpmn.md) | Modelado de los procesos de negocio |
| 06 | [Modelo C4](entrega/06-c4.md) | Contexto, contenedores, componentes y código |
| 07 | [Matriz de trazabilidad](entrega/07-trazabilidad.md) | Relación entre requerimientos, reglas, componentes y pruebas |
| 08 | [Limitaciones y mejoras](entrega/08-limitaciones-y-mejoras.md) | Limitaciones conocidas LIM-01…LIM-38, servicios simulados y hoja de ruta |

## Otros archivos de este directorio
- [diagrams/](diagrams/) — fuentes Mermaid/SVG (`src/`) e imágenes renderizadas (`img/`) de todos los diagramas
- [mockups/](mockups/) — fuentes editables de los mockups (`.dc.html`)
- [v1/](v1/) — snapshot congelado de toda la documentación, diagramas y mockups tal como estaban al cierre del MVP (antes de las funcionalidades v2: auth por correo, tiempo real, chatbot conversacional, optimización de rutas, pagos e integraciones)
