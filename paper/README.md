# Paper — Proyecto (Ingeniería de Software), CMEDriver

Reglas y núcleo fijo (pregunta, objetivos): [CONVENCIONES.md](CONVENCIONES.md). Control contra las rúbricas: [REVISION.md](REVISION.md). Agentes por fase: [../.claude/agents/](../.claude/agents/).

**Meta:** Entrega 2, domingo 11 de octubre de 2026 (portada, marco teórico, metodología, referencias; la Entrega 1 aporta resumen e introducción). Entrega 3 antes del 27 de noviembre.

**Última actualización: 2026-10-09 (cambio de alcance).** El autor retiró del proyecto el inventario, los pagos y el chatbot (y con ellos el LLM simulado y la pasarela simulada). El chat solo comunica al cliente con el motorizado (solo el cliente dueño del servicio y el motorizado asignado). El paper se sincronizó con `docs/entrega/` (6 apps Django, 12 entidades, 72 pruebas automatizadas del backend). El resumen del estado de cada fase está abajo y el detalle en REVISION.md.

## Fases y estado

| Fase | Agente | Salida | Estado (2026-10-09) |
|---|---|---|---|
| Investigación | `paper-investigador` | `fuentes/01..04-*.md` (pool verificado; no se modifica con el cambio de alcance) | hecha |
| 0. Introducción (Entrega 1) | `paper-redactor-introduccion` | `secciones/03-introduccion.md`, `secciones/resumen.md` | sincronizada con el nuevo alcance |
| 1. Marco Teórico | `paper-redactor-marco-teorico` | `secciones/04-marco-teorico.md` | sincronizada (25 citas únicas; 4.5 reescrita sobre agendamiento y chat) |
| 2. Metodología | `paper-redactor-metodologia` | `secciones/05-metodologia.md`, `figuras/c4-contenedores.png` | sincronizada (figura copiada de `docs/diagrams/img/c4-2-contenedores.png`) |
| Consolidación | `paper-ensamblador` | `Proyecto_CMEDriver_Entrega1.docx` y `Entrega2.docx`, `REVISION.md` | regenerados |
| 3. Avance de Resultados | `paper-redactor-avance-resultados` | `secciones/06-avance-resultados.md` | no iniciada (Entrega 3) |

## Reconstruir los .docx

```
cd paper/build
node build.js 1     # Proyecto_CMEDriver_Entrega1.docx (resumen, introducción, referencias)
node build.js 2     # Proyecto_CMEDriver_Entrega2.docx (marco teórico, metodología, referencias)
```

El script lee `secciones/*.md`, el pool `fuentes/*.md` y genera las listas `secciones/referencias-entrega1.md` y `referencias-entrega2.md` a partir de la lista `KEYS` de `build/build.js` (si se agrega o quita una cita, hay que editar `KEYS`). Si cambia el título, editar también `TITLE` en `build.js` y `secciones/00-portada.md`.

## Lo que debe hacer el estudiante (los agentes entregan borradores)

La guía de UNINPAHU prohíbe entregar un trabajo escrito totalmente por IA y exige declarar el uso. Antes de entregar:

1. Leer todo, editar y reescribir con su propia voz; entender cada afirmación (la sustentación es en la semana 15).
2. Completar los marcadores `[COMPLETAR: ...]` (resaltados en amarillo en los .docx): nombre del estudiante, ciudad, entregas fallidas en Colombia, registro del software y titularidad, alcance exacto del uso de IA, participantes de la validación, definiciones con página de Sommerville (2005) y Bass et al. (2003).
3. Abrir al azar varias referencias (DOI/URL) y confirmar que dicen lo que el texto afirma.
4. Abrir el `.docx` en Word, actualizar la paginación y confirmar la extensión (REVISION.md trae las páginas medidas con Word el 2026-10-09).
5. Confirmar con la docente asesora el título provisional (cambió: ya no dice "autogestión conversacional"), la pregunta de investigación y los objetivos; si la Entrega 1 ya se entregó con el alcance anterior, informarle del ajuste.
