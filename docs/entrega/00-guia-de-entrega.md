# 0. Guía de la entrega — dónde se cumple cada punto de la consigna

**Proyecto:** CMEDriver, una plataforma de gestión de mensajería (entregas y recolecciones).
**Autor:** Javier Esteban Mora Osorio (único integrante). UNINPAHU, Ingeniería de Software.
**Repositorio:** <https://github.com/javier5254/CEMDriver> (el repositorio se llama *CEMDriver* y el producto, *CMEDriver*).

Esta guía permite al docente ubicar cada sub-ítem de la consigna en el documento y la sección exacta. Los documentos de `docs/entrega/` se verificaron contra el código y **prevalecen** sobre los documentos históricos de `docs/` cuando hay diferencias.

> **Alcance vigente (cambio del 2026-10-09).** El autor retiró del proyecto el **inventario, los pagos y el chatbot**. El chat queda solo como canal entre el cliente y el motorizado. Cifras vigentes, verificadas contra el código: **6 apps** Django, **12 entidades**, **24 de 29 RF** (los 5 retirados conservan su ID, marcados «Retirado del alcance»), **69 pruebas** del backend en verde (eran 96) y **34 limitaciones vigentes** de 38 (4 resueltas por reducción de alcance). El cambio está explicado en [01 §2.4](01-requerimientos.md#24-cambios-de-alcance), [04 §4.5](04-mer.md#45-cambios-de-alcance), [05 §10](05-bpmn.md#10-cambios-de-alcance) y [08 §8.1](08-limitaciones-y-mejoras.md#81-alcance-de-este-documento), y en la nota inicial de [02](02-stack-tecnologico.md), [03](03-arquitectura.md) y [06 §1](06-c4.md#1-introducción-al-modelo-c4). Los documentos numerados 01 a 17 de `docs/` y `docs/v1/` son **históricos** (anteriores al cambio) y no lo reflejan.

---

## 1. Mapa consigna → evidencia

### 1. Documento de requerimientos

| Sub-ítem exigido | Dónde se cumple |
|---|---|
| Problema o necesidad | [01 §1](01-requerimientos.md#1-problema-o-necesidad-identificada) (problemas P1…P6) |
| Objetivo general (y específicos) | [01 §2.1](01-requerimientos.md#21-objetivo-general) y [§2.2](01-requerimientos.md#22-objetivos-específicos) (OE-1…OE-4; desglose del OE-3 en metas funcionales MF-1…MF-7 en [§2.3](01-requerimientos.md#23-metas-funcionales-del-prototipo-desglose-del-oe-3), con MF-5 retirada) |
| Actores / tipos de usuario | [01 §3.1](01-requerimientos.md#31-actores-humanos-roles-del-sistema) (4 roles con permisos verificados) y [§3.2](01-requerimientos.md#32-actores-externos-sistemas) (5 actores externos: 4 reales y el correo, configurable y en consola en desarrollo) |
| Requerimientos funcionales claros y comprobables | [01 §4](01-requerimientos.md#4-requerimientos-funcionales-rf): RF-01…RF-29 (24 vigentes; RF-04, RF-18, RF-22, RF-23 y RF-26 retirados) con descripción "El sistema debe…", prioridad, criterio de aceptación verificable y prueba que lo verifica |
| Requerimientos no funcionales | [01 §5](01-requerimientos.md#5-requerimientos-no-funcionales-rnf): RNF-01…RNF-20 (19 vigentes; RNF-13 retirado) con métrica y evidencia |
| Reglas de negocio | [01 §6](01-requerimientos.md#6-reglas-de-negocio-rn): RN-01…RN-19 (16 vigentes; RN-04, RN-06 y RN-16 retirados) con el archivo y la función que hacen cumplir cada regla |
| Restricciones | [01 §7](01-requerimientos.md#7-restricciones-del-sistema-res): RES-01…RES-15 (13 vigentes; RES-06 y RES-07 retiradas; técnicas, externas, legales y académicas) |
| Inconsistencias detectadas | [01 §8](01-requerimientos.md#8-hallazgos-inconsistencias-entre-documentación-y-código): hallazgos H-01…H-12 (10 abiertos; H-03 y H-12 resueltos por reducción de alcance y H-09 parcial) |
| Cambios de alcance | [01 §2.4](01-requerimientos.md#24-cambios-de-alcance) (qué se retiró, qué IDs y qué se conserva) y [§9](01-requerimientos.md#9-índice-de-ids) (vigencia de cada serie de IDs) |

### 2. Stack tecnológico (cada tecnología justificada)

| Sub-ítem exigido | Dónde se cumple |
|---|---|
| Resumen | [02 §1](02-stack-tecnologico.md#1-resumen-del-stack) |
| Frontend | [02 §2](02-stack-tecnologico.md#2-frontend) |
| Backend | [02 §3](02-stack-tecnologico.md#3-backend) |
| Base de datos | [02 §4](02-stack-tecnologico.md#4-base-de-datos) (SQLite en desarrollo y PostgreSQL propuesto, con la decisión explicada) |
| Frameworks | [02 §5](02-stack-tecnologico.md#5-frameworks-resumen) |
| Lenguajes | [02 §6](02-stack-tecnologico.md#6-lenguajes) |
| Servicios externos / APIs | [02 §7](02-stack-tecnologico.md#7-servicios-externos--apis) (Nominatim y teselas OSM reales; el correo sale por consola en desarrollo, que es el único servicio simulado) |
| Servicios en la nube | [02 §8](02-stack-tecnologico.md#8-servicios-en-la-nube) (propuesta: hoy no hay despliegue en la nube) |
| Herramientas de despliegue | [02 §9](02-stack-tecnologico.md#9-herramientas-de-despliegue) |
| Control de versiones | [02 §10](02-stack-tecnologico.md#10-control-de-versiones) |
| Otras herramientas | [02 §11](02-stack-tecnologico.md#11-otras-herramientas-pruebas-documentación-diagramas) (pruebas, documentación de la API, diagramas) |
| Justificación y alternativas descartadas | En cada tabla de 02: columnas "Justificación (necesidad concreta)" y "Alternativa considerada y por qué se descartó", vinculadas a RF/RNF/RN |

### 3. Arquitectura propuesta

| Sub-ítem exigido | Dónde se cumple |
|---|---|
| Estilo arquitectónico | [03 §1](03-arquitectura.md#1-estilo-arquitectónico) |
| Diagrama general | [03 §2](03-arquitectura.md#2-diagrama-general) ([imagen](../diagrams/img/arquitectura-general.png)) |
| Usuarios / actores | [03 §2](03-arquitectura.md#2-diagrama-general) (subgrafo "Actores") y [§9](03-arquitectura.md#9-nombres-canónicos-de-contenedores-y-componentes) |
| Aplicaciones y frontend | [03 §3](03-arquitectura.md#3-componentes-del-sistema) (App CMEDriver) |
| Backend y servicios | [03 §3](03-arquitectura.md#3-componentes-del-sistema) (API REST CMEDriver, Servicio de tiempo real, Capa de canales) y [§4](03-arquitectura.md#4-apps-del-backend-módulos-de-la-api-rest-cmedriver) (6 apps de dominio) |
| Base de datos | [03 §3](03-arquitectura.md#3-componentes-del-sistema) (Base de datos y Almacenamiento de evidencias) |
| APIs | [03 §4](03-arquitectura.md#4-apps-del-backend-módulos-de-la-api-rest-cmedriver) (rutas por app) y [§5](03-arquitectura.md#5-seguridad) (JWT y API Key) |
| Sistemas externos | [03 §3](03-arquitectura.md#3-componentes-del-sistema) (Nominatim, teselas OSM, SMTP, integrador, receptor de webhooks) |
| Comunicación entre componentes | [03 §2](03-arquitectura.md#2-diagrama-general) (flechas con protocolo), [§3](03-arquitectura.md#3-componentes-del-sistema) (columna "Se comunica con") y [§6](03-arquitectura.md#6-flujos-representativos) (flujos) |
| Responsabilidades | [03 §3](03-arquitectura.md#3-componentes-del-sistema) (columna "Responsabilidad") y [§4](03-arquitectura.md#4-apps-del-backend-módulos-de-la-api-rest-cmedriver) |
| Justificación | [03 §1.1](03-arquitectura.md#11-por-qué-este-estilo-responde-al-problema) y [§8](03-arquitectura.md#8-decisiones-de-arquitectura-resumen) |
| Despliegue | [03 §7.1](03-arquitectura.md#71-despliegue-actual-desarrollo) (actual) y [§7.2](03-arquitectura.md#72-despliegue-propuesto-producción--propuesta) (propuesta) |

### 4. Modelo entidad-relación (MER)

| Sub-ítem exigido | Dónde se cumple |
|---|---|
| Diagrama | [04 §4.1](04-mer.md#41-diagrama) ([imagen](../diagrams/img/mer-entrega.png)) |
| Entidades | [04 §4.1, "Entidades por módulo"](04-mer.md#entidades-por-módulo) (12 entidades en 6 apps; las 5 retiradas están en [§4.5](04-mer.md#45-cambios-de-alcance)) |
| Atributos (tipo, nulidad, descripción) | [04 §4.2](04-mer.md#42-diccionario-de-datos) (diccionario de datos) |
| Claves primarias | [04 §4.2](04-mer.md#42-diccionario-de-datos) (`id` PK en todas) y en el diagrama (`PK`) |
| Claves foráneas | [04 §4.3](04-mer.md#43-relaciones) (columna "FK" y `on_delete`) |
| Relaciones y cardinalidades | [04 §4.3](04-mer.md#43-relaciones) (columna "Cardinalidad (A : B)") y notación del diagrama |
| Restricciones | [04 §4.4](04-mer.md#44-restricciones-del-modelo): unicidad, estados y transiciones, dominios, integridad por rol, validaciones y observaciones |
| Sin entidades sin función | Cada entidad de [04 §4.2](04-mer.md#42-diccionario-de-datos) tiene el "Requerimiento que la justifica"; [07 §g.1](07-trazabilidad.md#g1-métricas): 12 de 12 entidades las usa al menos un RF |

### 5. BPMN de un proceso real

| Sub-ítem exigido | Dónde se cumple |
|---|---|
| Proceso elegido y por qué | [05 §1](05-bpmn.md#1-propósito-del-proceso-y-por-qué-es-el-principal) ("Ciclo de vida de un servicio de mensajería") |
| Diagrama | [05 §2](05-bpmn.md#2-diagrama), con la fuente [`.bpmn`](../diagrams/src/bpmn-ciclo-servicio.bpmn) y las imágenes [PNG](../diagrams/img/bpmn-ciclo-servicio.png) y [SVG](../diagrams/img/bpmn-ciclo-servicio.svg) |
| Actores, pools y lanes | [05 §3](05-bpmn.md#3-participantes-y-lanes) (un pool con 4 lanes y 2 pools colapsados) |
| Actividades | [05 §4](05-bpmn.md#4-actividades) (con RF/RN y el endpoint que las implementa) |
| Decisiones / gateways | [05 §5](05-bpmn.md#5-gateways) (exclusivos y paralelos) |
| Eventos de inicio, intermedios y de fin | [05 §6](05-bpmn.md#6-eventos) (3 inicios, temporizador, 6 fines) |
| Flujo e interacciones entre participantes | [05 §7](05-bpmn.md#7-interacciones-entre-participantes-flujos-de-mensaje) (flujos de mensaje MF01…MF10) |
| Diferencias entre el proceso ideal y el implementado | [05 §8](05-bpmn.md#8-diferencias-proceso-ideal-vs-implementado) |

### 6. Modelo C4

| Sub-ítem exigido | Dónde se cumple |
|---|---|
| Nivel 1, contexto | [06 §2](06-c4.md#2-nivel-1--diagrama-de-contexto) |
| Nivel 2, contenedores | [06 §3](06-c4.md#3-nivel-2--diagrama-de-contenedores) |
| Nivel 3, componentes | [06 §4](06-c4.md#4-nivel-3--diagrama-de-componentes-api-rest-cmedriver-y-servicio-de-tiempo-real) |
| Nivel 4, código | [06 §5](06-c4.md#5-nivel-4--diagrama-de-código-componente-services) (componente `services`) |
| Coherencia entre niveles | [06 §6.1](06-c4.md#61-descomposición-sistema--contenedores--componentes--clases) (descomposición y entidades del MER), [§6.2](06-c4.md#62-correspondencia-con-la-arquitectura-03-arquitecturamd) (correspondencia con 03) y [§6.3](06-c4.md#63-trazabilidad-de-requisitos-por-nivel) (RF por nivel) |
| Mismos nombres que la arquitectura | Nombres canónicos de [03 §9](03-arquitectura.md#9-nombres-canónicos-de-contenedores-y-componentes) reutilizados en 06 |

### 7. Repositorio y README

| Sub-ítem exigido | Dónde se cumple |
|---|---|
| Nombre y descripción | [README](../../README.md#cmedriver) (título y primer párrafo) |
| Integrantes | [README](../../README.md#cmedriver) (tabla inicial: único integrante) |
| Tecnologías | [README, "Tecnologías utilizadas"](../../README.md#tecnologías-utilizadas) |
| Arquitectura | [README, "Arquitectura general"](../../README.md#arquitectura-general) |
| Instalación y ejecución | [README, "Instalación y ejecución"](../../README.md#instalación-y-ejecución-entorno-local-de-desarrollo) (Windows y Linux/macOS, más las pruebas) |
| Variables de entorno sin secretos | [README, "Variables de entorno"](../../README.md#variables-de-entorno) y [`backend/.env.example`](../../backend/.env.example) (sin valores secretos) |
| Despliegue | [README, "Despliegue"](../../README.md#despliegue) (hoy solo local; la propuesta se marca como tal) |
| Control de versiones | Git + GitHub ([02 §10](02-stack-tecnologico.md#10-control-de-versiones)); `.gitignore` excluye `.env`, `db.sqlite3` y `media/` |

### Transversal: coherencia y trazabilidad

| Cadena | Dónde se cumple |
|---|---|
| Necesidad → objetivos → RF | [07 §b](07-trazabilidad.md#b-cadena-de-alto-nivel-problema--objetivos--rf) |
| RF → BPMN → C4 → MER → código → prueba | [07 §c](07-trazabilidad.md#c-matriz-principal-una-fila-por-rf) (una fila por RF) |
| RN → BPMN → código → MER → prueba | [07 §d](07-trazabilidad.md#d-matriz-de-reglas-de-negocio-rn-01rn-19) |
| RNF → decisión de stack o arquitectura | [07 §e](07-trazabilidad.md#e-matriz-rnf-principales--decisión-de-stackarquitectura--evidencia) |
| Ejemplo narrado de punta a punta | [07 §f](07-trazabilidad.md#f-ejemplo-narrado-de-punta-a-punta-rf-11-capturar-evidencia--rn-02) |
| Métricas y huecos | [07 §g](07-trazabilidad.md#g-cobertura-y-huecos-de-trazabilidad) |
| Limitaciones conocidas y mejoras | [08](08-limitaciones-y-mejoras.md): LIM-01…LIM-38 (34 vigentes y 4 resueltas por reducción de alcance), SIM-01…SIM-03 (solo SIM-03, el correo, sigue vigente) y hoja de ruta |

**Identificadores compartidos entre documentos:** RF-01…RF-29, RNF-01…RNF-20, RN-01…RN-19, RES-01…RES-15 y H-01…H-12 se definen en 01. Los usan 04, 05, 06 y 07, y 08 los referencia en su columna "Origen". Los IDs retirados el 2026-10-09 no se renumeran ni se reutilizan: permanecen marcados «Retirado del alcance». Los nombres de contenedores y componentes se definen en 03 §9 y se reutilizan sin cambios en 06 y 07. Las 12 entidades se definen en 04 y son las mismas de 06 §6.1 y de 07 §c.

---

## 2. Recorrido sugerido para la sustentación

1. **Problema y alcance (2 min).** [01 §1–§3](01-requerimientos.md#1-problema-o-necesidad-identificada): los seis problemas, el objetivo general y los cuatro roles. Aclarar desde el inicio el alcance vigente (inventario, pagos y chatbot retirados el 2026-10-09, [01 §2.4](01-requerimientos.md#24-cambios-de-alcance); el chat es solo cliente-motorizado) y qué es real y qué está simulado: solo el correo, que sale por consola en desarrollo ([08 §8.3](08-limitaciones-y-mejoras.md#83-servicios-simulados-limitación-de-alcance)).
2. **Un requerimiento concreto.** RF-11 "Capturar evidencia" en [01 §4.3](01-requerimientos.md#43-motorizado), con su criterio de aceptación verificable y las reglas RN-02 y RN-17.
3. **Proceso.** Mostrar el [BPMN](05-bpmn.md#2-diagrama) y seguir el camino del lane *Motorizado*: `GW_Resultado` → `UT_Evidencia` → `ST_ValidarEvidencia` → `GW_EvidenciaOK` → `ST_PasarRecolectado` → `SND_WebhookRecolectado` → `EE_Recolectado`.
4. **Arquitectura y C4.** Del [diagrama general](03-arquitectura.md#2-diagrama-general) bajar por el C4: [N1](06-c4.md#2-nivel-1--diagrama-de-contexto) → [N2](06-c4.md#3-nivel-2--diagrama-de-contenedores) (App CMEDriver → API REST CMEDriver → Almacenamiento de evidencias) → [N3](06-c4.md#4-nivel-3--diagrama-de-componentes-api-rest-cmedriver-y-servicio-de-tiempo-real) (`services`, Permisos RBAC, Despachador de webhooks) → [N4](06-c4.md#5-nivel-4--diagrama-de-código-componente-services) (`ServicioViewSet.cerrar`).
5. **Datos.** En el [MER](04-mer.md#41-diagrama), la relación SERVICIO 1 : 0..1 EVIDENCIA (FK única) y el cambio de `SERVICIO.estado` según la [tabla de transiciones](04-mer.md#442-estados-del-servicio-y-transiciones-válidas).
6. **Código y pruebas en vivo.** Abrir `backend/services/views.py` (`cerrar`) y `serializers.py` (`CerrarServicioSerializer.validate`). Ejecutar `./run_tests.ps1 services` y señalar T-SRV-08 (400 sin evidencia) y T-SRV-09 (200 con foto y firma). Si hay tiempo, demostrar el flujo en la app con `motorizado1`.
7. **Trazabilidad.** Mostrar la fila de RF-11 en la [matriz](07-trazabilidad.md#c3-motorizado-mf-3) y el [ejemplo narrado](07-trazabilidad.md#f-ejemplo-narrado-de-punta-a-punta-rf-11-capturar-evidencia--rn-02).
8. **Honestidad técnica.** Cerrar con los [huecos de trazabilidad](07-trazabilidad.md#g2-huecos-de-trazabilidad-detectados) y las limitaciones de prioridad alta de [08](08-limitaciones-y-mejoras.md#82-tabla-consolidada-de-limitaciones) (p. ej. LIM-01 RBAC y LIM-35 servicio detenido en `NOVEDAD`), con la [hoja de ruta](08-limitaciones-y-mejoras.md#84-hoja-de-ruta-de-mejoras-priorizada).

---

## 3. Pendientes del autor antes de entregar

Estas tareas no se pueden resolver desde la documentación. Debe hacerlas el autor:

- [ ] **Declaración de uso de IA:** revisar y ajustar la sección "Declaración de uso de inteligencia artificial" del [README](../../README.md#declaración-de-uso-de-inteligencia-artificial) según la guía de UNINPAHU y retirar el comentario HTML de recordatorio.
- [ ] **Acceso del docente:** si el repositorio es privado, dar acceso al docente en GitHub (*Settings → Collaborators*); si es público, comprobar que se vea sin iniciar sesión.
- [ ] **Nombre del curso:** confirmar el nombre exacto del curso o asignatura, el grupo y el docente, y completarlos en la tabla inicial del README (hoy dice "UNINPAHU — Ingeniería de Software").
- [ ] **Nombre del repositorio:** decidir entre renombrar el repositorio a `CMEDriver` (GitHub redirige la URL antigua) o mantener `CEMDriver` con la aclaración actual (LIM-34). Si se renombra, actualizar las URL en el README, en [02](02-stack-tecnologico.md) y en esta guía.
- [ ] **Revisar borradores:** leer los ocho entregables y esta guía de punta a punta, en especial las partes redactadas con apoyo de IA, y confirmar que se pueden defender en la sustentación.
- [ ] **Sincronizar el paper con el cambio de alcance:** el paper (`paper/secciones/` y los `.docx` de `paper/`) se redactó con el alcance anterior y debe ajustarse a lo vigente. Mínimo: la **pregunta de investigación y el objetivo general** sin «autogestión conversacional»; el **OE-3** sin chatbot; la **justificación y el alcance** sin inventario, LLM ni pagos (el chat solo comunica al cliente con el motorizado); y la **metodología, el marco teórico, el resumen y la portada** si mencionan el chatbot, el inventario, los pagos o el modelo de lenguaje. Los textos vigentes están en [01 §1–§2](01-requerimientos.md#1-problema-o-necesidad-identificada) y las cifras en [01 §2.4](01-requerimientos.md#24-cambios-de-alcance). Después hay que regenerar los `.docx`. Hoy el paper y esta documentación **no** describen el mismo sistema.
- [ ] **Decidir si se restringe el chat a cliente-motorizado en el código:** la documentación vigente dice que el chat solo conecta al cliente con el motorizado (RF-16), pero el código también deja leer y escribir a ADMIN y ALISTADOR (`ServicioViewSet.mensajes` en `backend/services/views.py` y `ChatConsumer` en `backend/services/consumers.py`; ver [01 §4.4](01-requerimientos.md#44-cliente), RF-16, y [04 §4.4.6](04-mer.md#446-observaciones-de-integridad-detectadas)). Hay que elegir: restringir el código a los dos participantes, o conservar el acceso de supervisión del ADMIN y el ALISTADOR y dejarlo escrito como tal en 01, 03 y el paper.
- [ ] **Verificación final:** ejecutar las pruebas (`run_tests.ps1`, 69 en verde), levantar backend y frontend con `seed_data` y comprobar que las imágenes de `docs/diagrams/img/` se vean en GitHub.
