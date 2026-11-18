# Paper — Proyecto (Ingeniería de Software), CMEDriver

Reglas y núcleo fijo (pregunta, objetivos): [CONVENCIONES.md](CONVENCIONES.md). Control contra las rúbricas: [REVISION.md](REVISION.md). Agentes por fase: [../.claude/agents/](../.claude/agents/).

**Meta:** Entrega 2, domingo 11 de octubre de 2026 (portada, marco teórico, metodología, referencias; la Entrega 1 aporta resumen e introducción). Entrega 3 antes del 27 de noviembre.

**Última actualización: 2026-10-09 (cambio de alcance).** El autor retiró del proyecto el inventario, los pagos y el chatbot (y con ellos el LLM simulado y la pasarela simulada). El chat solo comunica al cliente con el motorizado (solo el cliente dueño del servicio y el motorizado asignado). El paper se sincronizó con `docs/entrega/` (6 apps Django, 12 entidades, 110 pruebas automatizadas del backend, 25 requisitos funcionales vigentes). El resumen del estado de cada fase está abajo y el detalle en REVISION.md.

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

### Documento unificado (Entregas 1 y 2)

```
cd paper/build
python unir_entregas.py     # genera Proyecto_CMEDriver_Unificado.docx
```

Une los dos Word **sin regenerar nada**: toma `Proyecto_CMEDriver_Entrega1.docx` completo (portada, contraportada, resumen e introducción, **con las citas de Mendeley Cite que se le hayan insertado**), le agrega el cuerpo de `Proyecto_CMEDriver_Entrega2.docx` desde "4. Marco Teórico" hasta antes de las referencias (con sus 8 tablas y la figura) y escribe una sola lista de referencias, sin duplicados y en orden alfabético. Solo cambia el rótulo de la portada y la contraportada ("Entrega 1" pasa a "Entregas 1 y 2"). No modifica los archivos de origen y solo usa la librería estándar de Python. Las citas de la parte de la Entrega 2 siguen siendo texto, no campos de Mendeley. **No ejecutar `node build.js 1` después de insertar citas de Mendeley**: sobrescribiría el archivo de la Entrega 1.


## Lo que debe hacer el estudiante (los agentes entregan borradores)

La guía de UNINPAHU prohíbe entregar un trabajo escrito totalmente por IA y exige declarar el uso. Antes de entregar:

1. Leer todo, editar y reescribir con su propia voz; entender cada afirmación (la sustentación es en la semana 15).
2. Completar el único marcador `[COMPLETAR: ...]` que queda (resaltado en amarillo en el .docx de la Entrega 2): definiciones con página de Sommerville (2005) y Bass et al. (2003), previa consulta de los libros. El resto se completó el 2026-10-13.
3. Abrir al azar varias referencias (DOI/URL) y confirmar que dicen lo que el texto afirma.
4. Abrir el `.docx` en Word, actualizar la paginación y confirmar la extensión (REVISION.md trae las páginas medidas con Word el 2026-10-09).
5. Confirmar con la docente asesora el título provisional (cambió: ya no dice "autogestión conversacional"), la pregunta de investigación y los objetivos; si la Entrega 1 ya se entregó con el alcance anterior, informarle del ajuste.


## Entrega 3 (2026-11-17): documento final con Mendeley

Estado: `Proyecto_CMEDriver_Final.docx` tiene portada, resumen, secciones 3 a 6, referencias y los campos de Mendeley Cite (87 citas y bibliografía). Copia de revisión en PDF: `Proyecto_CMEDriver_Final.pdf`. Los anexos van aparte (`Anexos_CMEDriver.docx`, `build/build_anexos.js`). La organización de referencia no se nombra en ningún archivo.

**Nunca regenerar el Final desde markdown ni con `node build.js`**: se perderían los campos de Mendeley. Para rehacer solo la sección 6 (parte de `_respaldo/Final_antes_de_avance.docx`, el Final previo a la sección 6, y reescribe el Final):

```
cd paper/build
node build_seccion6.js        # secciones/06-avance-resultados.md -> build/_tmp/seccion6.docx
py injertar_seccion6.py       # injerta la sección 6 antes de "7. Referencias", clona los campos de Mendeley y aplica ajustes de coherencia y anonimización (anonimizar.py)
```

Si se edita el Final en Word, el script ya no sirve (partiría del respaldo y perdería esos cambios): editar el Word directamente. Medir páginas: `build/medir_paginas.ps1`.

## Versión vigente (2026-11-18)

La versión de entrega es `Proyecto_CMEDriver_Final_v7.docx`, copiada a `ENTREGA/Proyecto_CMEDriver_Final.docx` (con su `.pdf`), junto con `ENTREGA/Anexos_CMEDriver.docx` y `ENTREGA/Anexo_B_Cronograma_Presupuesto_Producto.docx`. El cronograma (sección 7, Tabla 9) usa fechas reales del semestre 2026-II, del 20 de agosto al 17 de noviembre de 2026, más los seis meses relativos (M1 a M6) del Trabajo de Grado. Para reemplazar el cuerpo de la sección 7 en una copia del Final: `node build/build_seccion7.js` y `python build/injertar_cronograma.py ENTRADA.docx SALIDA.docx`.
