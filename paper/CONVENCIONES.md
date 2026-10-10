# Convenciones del paper — Proyecto (Ingeniería de Software), CMEDriver

Este archivo es la fuente única de reglas para todos los agentes que trabajan en el paper. Léelo completo antes de empezar.

## 1. Qué se entrega y cuándo

- Asignatura: **Proyecto (Ingeniería de Software)**, programa profesional, UNINPAHU, semestre 2026-II. Es la primera mitad del trabajo de grado.
- Entregable final: **paper de investigación de 19 a 25 páginas de contenido** (sin portada, contraportada, referencias ni anexos).
- **Entrega 2 (30 %): domingo 11 de octubre de 2026.** Alcance: Portada y contraportada, Resumen, Introducción (incluye planteamiento del problema, pregunta, objetivos y justificación, que corresponden a la Entrega 1 vencida), Marco Teórico, Metodología y Referencias.
- Entrega 3 (40 %, antes del 27 de noviembre): documento final, suma Avance de Resultados y Anexos. Sustentación en la semana 15.
- El software terminado, las pruebas y los resultados definitivos NO se piden en esta asignatura (corresponden a Trabajo de Grado). Se pide un avance: diseño inicial y prototipo temprano.

## 2. Núcleo fijo del paper (actualizado el 2026-10-09 por el cambio de alcance; el estudiante puede ajustarlo después)

El 2026-10-09 el autor retiró del proyecto el inventario, los pagos y el chatbot (y con ellos el LLM simulado y la pasarela de pagos simulada). El chat solo sirve para que el cliente y el motorizado se comuniquen. Las secciones 13 y 14 detallan lo vigente; la fuente de verdad sobre el sistema es `docs/entrega/` (en especial `01-requerimientos.md` §1, §2 y §2.4, `03-arquitectura.md` y `06-c4.md`).

**Título provisional:** CMEDriver: plataforma orientada a API para la gestión, trazabilidad en tiempo real y comunicación directa cliente-mensajero en servicios de mensajería en Colombia

**Pregunta de investigación:** ¿Cómo puede una plataforma orientada a API integrar la gestión de servicios de mensajería (entregas y recolecciones), la trazabilidad en tiempo real, la evidencia digital de entrega y la comunicación directa entre cliente y mensajero en las operaciones de Logytech Mobile en Colombia durante el segundo semestre de 2026?

**Objetivo general:** Diseñar y desarrollar un prototipo funcional temprano de una plataforma orientada a API que integre la gestión de servicios de mensajería (entregas y recolecciones), la trazabilidad en tiempo real, la evidencia digital de entrega y el chat directo entre el cliente y el mensajero en las operaciones de Logytech Mobile en Colombia durante el segundo semestre de 2026.

**Objetivos específicos (los 4 vigentes, tal como están en `secciones/03-introduccion.md`, sección 3.3):**
1. Identificar, a partir de la literatura y del análisis del dominio, los problemas de coordinación, trazabilidad y atención al cliente en los servicios de mensajería de última milla, y derivar de ellos un conjunto priorizado de requerimientos funcionales y no funcionales.
2. Diseñar y documentar una arquitectura modular orientada a API (REST, comunicación en tiempo real y webhooks) que soporte los roles de administración, alistamiento, mensajería en campo y cliente, y modelarla mediante casos de uso, diagramas de clases, modelo entidad-relación, modelo C4 y mockups.
3. Implementar un prototipo funcional temprano que cubra los flujos centrales: ciclo de vida del servicio, seguimiento GPS en tiempo real, chat cliente-motorizado y evidencia digital de recolección.
4. Formular un protocolo de validación para Trabajo de Grado que especifique los criterios de evaluación, los instrumentos y los usuarios participantes.

**Palabras clave (5):** logística de última milla; trazabilidad en tiempo real; arquitectura orientada a API; evidencia digital de entrega; ingeniería de software.

## 3. Estructura y extensión

Con Arial 11, interlineado 1.5 y márgenes de 2,54 cm se rinden aproximadamente 380 a 420 palabras por página. Los objetivos de palabras ya descuentan espacio de tablas y figuras.

| Sección | Extensión según la guía | Meta en palabras | Citas exigidas |
|---|---|---|---|
| Portada y Contraportada | — | — | — |
| Resumen | 250 a 350 palabras + 4 a 5 palabras clave | 250 a 350 | — |
| 3. Introducción | 4 a 5 páginas | 1.600 a 2.000 | 5 a 10 |
| 4. Marco Teórico | 8 a 10 páginas | 3.200 a 3.900 | 15 a 25 fuentes únicas |
| 5. Metodología | 3 a 4 páginas | 1.200 a 1.600 | 3 a 5 |
| 6. Avance de Resultados (Entrega 3) | 3 a 5 páginas | 1.200 a 1.900 | las que apliquen |
| 7. Referencias | mínimo 20 a 25 fuentes únicas | — | — |
| 8. Anexos (Entrega 3) | documentos separados | — | — |

Cada cita del texto debe tener su referencia y cada referencia debe estar citada al menos una vez. No puede haber referencias huérfanas.

## 4. Formato (lo aplica el ensamblador, los redactores solo escriben markdown)

Arial 11, texto justificado, interlineado 1.5, márgenes de 2,54 cm en todos los lados, páginas en números arábigos en el margen superior derecho. Tablas y figuras numeradas, con título en cursiva y fuente en nota al pie. Referencias con sangría francesa de 1,27 cm y orden alfabético por apellido del primer autor.

## 5. Estilo de redacción

- Español de Colombia, **tercera persona impersonal** ("se diseñó", "el estudiante", "la plataforma"). Nunca primera persona ("creamos", "desarrollé", "nuestro").
- Claridad y precisión. Sin relleno ni frases grandilocuentes.
- **Analítico y crítico, no una lista de definiciones.** Compara fuentes, contrasta posturas, señala limitaciones y vacíos. Cada subtítulo cierra con una frase que conecta con el siguiente (hilo argumental).
- Párrafos de 5 a 8 líneas. Las listas con viñetas se usan poco y solo cuando aportan.
- Mayúsculas y cursivas según APA 7 y el manual institucional.

## 6. Citación (APA 7, adaptación UNINPAHU)

- Cita corta (menos de 40 palabras): entre comillas dobles dentro del párrafo, con autor, año y página o párrafo: Según Pérez (2020), "texto" (p. 15).
- **Las citas de 40 palabras o más están prohibidas.** Prefiere siempre la paráfrasis: (Autor, año), sin comillas.
- Dos autores: (López & Martínez, 2021). Tres o más: (Ramírez et al., 2022). Organizaciones: nombre completo la primera vez con sigla entre corchetes y luego la sigla.
- No uses citas secundarias. Cita solo lo que tengas verificado en la fuente.
- Solo pones número de página en citas textuales y únicamente si lo verificaste en el texto. Con paráfrasis no hace falta.

## 7. Regla de oro anti-fabricación (la más importante de este proyecto)

Este es un trabajo evaluado que declara su origen. Una referencia inventada es fraude académico y se sanciona con 0.0.

1. **Una fuente solo existe si la verificaste.** Verificar significa confirmar autores, año, título y medio contra una fuente de datos real: la API de Crossref (`https://api.crossref.org/works/<doi>` o `...works?query.bibliographic=<título>&rows=3`), OpenAlex (`https://api.openalex.org/works?search=<título>`), el sitio de la editorial, el repositorio institucional o la página oficial de la norma. Hazlo con `curl` desde Bash. Un DOI que no resuelve, o metadatos que no coinciden con lo que recordabas, descartan la fuente.
2. **Nada de memoria.** No escribas una referencia "porque la conoces". Si no la verificaste en esta sesión, no entra.
3. **Los hechos que se atribuyen a una fuente deben provenir de lo que leíste** (resumen/abstract o texto). No inventes cifras, porcentajes ni conclusiones. Si solo leíste el resumen, atribuye únicamente lo que el resumen dice.
4. Si dudas, descarta la fuente o márcala `[SIN VERIFICAR]` y no la uses en el texto.
5. Prioriza: artículos arbitrados, ponencias de congresos (IEEE, ACM, Springer, Elsevier, MDPI, Scielo, Redalyc), libros de editoriales académicas, informes de entidades oficiales (DNP, DANE, MinTIC, Cámara Colombiana de Comercio Electrónico), normas y documentación oficial. **La mayoría (al menos 70 %) debe ser de 2021 a 2026.** Se admiten trabajos fundacionales anteriores (por ejemplo Fielding 2000, Hevner et al. 2004) en minoría y justificados.
6. Prefiere fuentes en acceso abierto o con DOI para que el estudiante y el docente puedan abrirlas.

## 8. Honestidad sobre CMEDriver

CMEDriver es un **prototipo académico**. Describe lo que existe y no lo que sería deseable:

- Implementado y verificado con pruebas automatizadas del backend (72 pruebas en verde; antes del cambio de alcance eran 96): autenticación JWT con roles (RBAC), ciclo de vida del servicio (entregas y recolecciones), cobertura y leadtime, planificación de recolecciones por el cliente, evidencia (foto y firma), novedades, tracking GPS, chat por WebSockets y REST **solo entre el cliente dueño del servicio y el motorizado asignado** (ADMIN y ALISTADOR no participan), API Keys y webhooks firmados con HMAC, geocodificación con Nominatim y heurística de vecino más cercano. Arquitectura: 6 apps Django (accounts, coverage, services, tracking, optimization, integrations) y 12 entidades.
- **Simulado:** los usuarios (administrador, alistador, motorizado, cliente) son de prueba, sin validación con operadores ni clientes reales, y el correo de restablecimiento de contraseña usa el backend de consola en desarrollo. **Ya no hay LLM simulado ni pasarela de pagos simulada: se retiraron junto con el chatbot, el inventario y los pagos.** No los describas como parte del producto; solo pueden mencionarse como alcance excluido y mejora futura opcional.
- No verificado: build nativo de Android (falló por una limitación del entorno de desarrollo).
- **No existen** encuestas, entrevistas, métricas de mejora ni datos de usuarios reales. No los inventes, no afirmes que el sistema "redujo" o "mejoró" nada. La validación empírica es trabajo de Trabajo de Grado.
- El desarrollo del prototipo y la documentación contaron con asistencia de IA (Claude, de Anthropic). Debe declararse (ver sección 9).

## 9. Declaración de uso de inteligencia artificial (obligatoria según la Guía APA/IA de UNINPAHU)

La guía exige declarar explícitamente el uso de IA en el texto y en las referencias, y prohíbe entregar un trabajo escrito totalmente por IA. Por eso:

- El paper incluye la subsección "Consideraciones éticas y declaración de uso de inteligencia artificial" dentro de la Metodología. Debe decir con precisión qué se hizo con IA (asistencia en generación de código, documentación técnica y borradores de redacción), que el estudiante supervisó, editó y reinterpretó el contenido, y que las fuentes fueron verificadas.
- En el texto se cita así: (Anthropic, 2026). En referencias: `Anthropic. (2026). *Claude* [Modelo de lenguaje grande]. https://claude.ai/`
- Las citas textuales tomadas de la IA, si las hubiera, solo pueden ser cortas.
- La declaración se refiere al uso de IA por el autor como asistente de desarrollo y redacción. El prototipo ya no incorpora ningún modelo de lenguaje en su ejecución (el LLM simulado del chatbot se retiró el 2026-10-09).
- Todos los borradores son **borradores para que el estudiante los revise, edite y haga suyos**. No presentes nada como definitivo.

## 10. Archivos, carpetas y formato

```
paper/
  CONVENCIONES.md            este archivo
  README.md                  tablero de estado
  fuentes/                   pool de fuentes verificadas (lo escriben los investigadores)
    01-contexto.md
    02-tecnologia.md
    03-metodologia-normativa.md
  secciones/                 una sección por archivo markdown (lo escriben los redactores)
    00-portada.md   03-introduccion.md   04-marco-teorico.md   05-metodologia.md
    06-avance-resultados.md (Entrega 3)   resumen.md   referencias.md
  figuras/                   imágenes PNG usadas en el paper
  build/                     scripts de ensamblado a .docx
  Proyecto_CMEDriver_Entrega2.docx   (lo genera el ensamblador)
  REVISION.md                informe de control contra la lista de verificación de la guía
```

**Formato de las entradas del pool de fuentes** (`paper/fuentes/*.md`), una por fuente:

```
### [clave] Apellido (año)
- Referencia APA 7: <referencia completa, con DOI o URL, lista para pegar>
- Tipo: artículo | ponencia | libro | informe oficial | norma | documentación técnica
- Verificación: <API o URL consultada, fecha de consulta (2026-10-xx), qué metadatos coincidieron>
- Hechos verificados: <2 a 4 viñetas parafraseadas con lo que la fuente realmente dice; indica si salió del resumen o del texto completo>
- Cita en texto: (Apellido, año) | (Apellido & Apellido, año) | (Apellido et al., año)
- Uso sugerido: Intro | MT 4.x | Metodología
```

**Formato markdown de las secciones:** títulos con `#` (`# 3. Introducción`, `## 3.1 ...`), párrafos normales, cursiva con `*texto*`, negrita con `**texto**`, listas con `-` o `1.`, tablas con sintaxis markdown. Para figuras y tablas usa este bloque exacto:

```
**Figura 1**

*Título de la figura en cursiva*

![Texto alternativo](../figuras/archivo.png)

*Nota.* Fuente: Elaboración propia.
```

(Para tablas: `**Tabla 1**`, `*Título*`, la tabla markdown y `*Nota.* Fuente: ...`.) Cada figura o tabla debe mencionarse en el texto ("como muestra la Figura 1").

Los marcadores que el estudiante debe completar se escriben `[COMPLETAR: descripción]` y se resaltan en el .docx.

## 11. Material interno del proyecto (fuente primaria sobre CMEDriver)

**Desde el 2026-10-09 la fuente de verdad es `docs/entrega/` (`01-requerimientos.md` a `08-limitaciones-y-mejoras.md`); los documentos de `docs/` anteriores a esa fecha pueden describir inventario, pagos y chatbot, que ya no existen: en caso de discrepancia prevalece `docs/entrega/`.** Todo en `C:\GitLogytech\CMEDriver\docs\`: `01-project-charter.md`, `02-requisitos.md`, `03-arquitectura.md`, `04-modelo-datos.md`, `05-api.md`, `06-cronograma.md`, `07-roadmap-futuro.md`, `08-diagrama-clases.md`, `10-diagrama-casos-uso.md`, `12-mockups.md`, `13-rf-rnf-completos.md`, `14-diagrama-c4.md`, `15-diagrama-flujo.md`, `16-plan-pruebas.md`, `17-manual-herramientas.md`, y las imágenes en `docs/diagrams/img/*.png`. El código está en `backend/` y `frontend/`. Estos documentos describen el sistema construido; **no son referencias académicas**. En el paper se mencionan como "documentación técnica del proyecto (Anexo A)" y nunca se listan en Referencias.

Las guías originales del curso están en `C:\Users\javier.mora\Downloads\`: `Guia_Proyecto_Software_Profesional.docx`, `Cronograma_Asesorias_Profesional_Software.xlsx` y `Guía trabajos escritos IA_ Normas APA.pdf`.

## 12. Requisitos de la docente (rúbricas y Guía 2) — prevalecen sobre lo anterior si hay conflicto

Archivos: `Rubricas_Proyecto_Profesional_Software.xlsx` y `Guia2_MarcoTeorico_Metodologia_Arquitectura_Software.docx` (en Downloads). **Hoy se completan la Entrega 1 y la Entrega 2, como dos documentos separados:**

- **Entrega 1 (30 %): Resumen + Introducción.** Rúbrica: (a) Resumen 250 a 350 palabras con 4 o 5 palabras clave: problema, objetivos, metodología propuesta y adelanto del desarrollo inicial; (b) planteamiento del problema contextualizado **con datos o fuentes académicas** que cierra con la pregunta de investigación específica al contexto; (c) objetivo general coherente y **3 a 5 objetivos específicos con verbos verificables, sin actividades de cronograma disfrazadas**; (d) justificación académica, tecnológica y/o práctica y **a quién beneficia**; (e) 5 a 10 citas académicas únicas en APA UNINPAHU.
- **Entrega 2 (30 %): Marco Teórico + Metodología.** No replantear el problema, retomar el de la Entrega 1. Rúbrica: (a) marco por subtítulos temáticos, analítico, que integre **conceptos, enfoques de ingeniería de software y normativa colombiana**; (b) 15 a 25 citas únicas **en el marco teórico**, en su mayoría de los últimos 5 años; (c) enfoque (cualitativo, cuantitativo o mixto), tipo, naturaleza y diseño coherentes con los objetivos; (d) herramientas, tecnologías, **proceso de selección**, arquitectura y etapas de desarrollo; (e) coherencia explícita con problema y objetivos de la Entrega 1.

**Contenido obligatorio de la Guía 2:**
1. Marco teórico: cada subtítulo cierra explicando cómo el concepto se relaciona con el problema. Prohibido copiar biografías de autores o listas de definiciones.
2. **Actividad 1:** tabla de 4 a 6 términos técnicos centrales (Término | Definición con autor | Fuente), definidos con literatura especializada, no con diccionario.
3. **Enfoques de ingeniería de software** de la guía, a evaluar críticamente según su pertinencia: Ingeniería de Software (Sommerville, 2005), Arquitectura de Software (Bass, Clements y Kazman, 2003), metodologías ágiles (Manifiesto Ágil, 2001; Guía de Scrum 2020), Design Thinking (Stanford d.school), modelo C4, especificación de requisitos ISO/IEC/IEEE 29148. Son fuentes de la docente; verifícalas y úsalas, y complétalas con literatura reciente.
4. **Normativa:** Ley 1581 de 2012 (datos personales); Ley 23 de 1982 y Decisión Andina 351 de 1993 (derechos de autor sobre el software); registro de software ante la Dirección Nacional de Derecho de Autor.
5. **Actividad 2:** responder para CMEDriver: ¿maneja datos personales?, ¿de quién? (nombre, teléfono, direcciones, ubicación GPS, firma y foto de evidencia, mensajes de chat de clientes y motorizados), ¿planea registrar el software? (el estudiante decide: marca `[COMPLETAR: confirmar si se registrará el software]`).
6. Metodología: explicar el enfoque con una justificación frente a la tabla de enfoques de la guía; **definir población/usuarios e instrumentos** (técnica, instrumento, para qué sirve: entrevista semiestructurada, observación, encuesta, prueba piloto con lista de chequeo). Aclara con honestidad que en esta etapa los roles fueron simulados y que los instrumentos con usuarios reales están **diseñados y planificados** para Trabajo de Grado; presenta qué instrumento se aplicará a quién. No digas que ya se aplicaron.
7. **Actividad 3:** tabla final (Tipo de investigación | Metodología de desarrollo | Herramientas/tecnologías | Arquitectura propuesta). Metodología de desarrollo: justifica con la tabla de la guía (ágil, por prototipos, cascada). La realidad fue incremental por prototipos con iteraciones tipo ágil; no afirmes Scrum completo con roles que no existieron.
8. Sección **"Coherencia con la Entrega 1"**: responde si metodología y arquitectura permiten lograr cada objetivo específico (tabla objetivo → decisión metodológica/arquitectónica).
9. Cuando se mencione el diagrama de arquitectura, usa el **modelo C4** (ya existen `docs/diagrams/c4-contexto.svg` y `c4-contenedores.svg`).

**Ensamblado:** produce dos .docx: `Proyecto_CMEDriver_Entrega1.docx` (portada, resumen, introducción, referencias de esa entrega) y `Proyecto_CMEDriver_Entrega2.docx` (portada, marco teórico, metodología, referencias de esa entrega), y `REVISION.md` evalúa cada una contra su rúbrica.

## 13. Objetivos vigentes (sustituyen a cualquier versión anterior)

La Introducción (`secciones/03-introduccion.md`, sección 3.3) fija **4 objetivos específicos** con verbos verificables: (1) identificar problemas y derivar requerimientos; (2) diseñar y documentar la arquitectura modular orientada a API y modelarla (casos de uso, clases, ER, C4, mockups); (3) implementar el prototipo funcional temprano (ciclo de vida del servicio, seguimiento GPS en tiempo real, chat cliente-motorizado y evidencia digital de recolección; **sin chatbot**); (4) formular el protocolo de validación para Trabajo de Grado. Marco Teórico, Metodología y la tabla de coherencia con la Entrega 1 deben usar estos 4, leídos directamente de esa sección. El objetivo 3 se acotó el 2026-10-09 (cambio de alcance); los demás no cambiaron.

## 14. Pregunta y objetivo general vigentes (sustituyen a cualquier versión anterior)

Organización de aplicación: **Logytech Mobile**, empresa multinacional de logística (dato dado por el estudiante; no se afirma nada más sobre la empresa). Lugar: Colombia. Tiempo: segundo semestre de 2026. Pregunta y objetivo general comparten contenido y difieren solo en el verbo; léelos de `secciones/03-introduccion.md` secciones 3.2 y 3.3 (transcritos en la sección 2 de este archivo). Integran la gestión de servicios de mensajería (entregas y recolecciones), la trazabilidad en tiempo real, la evidencia digital de entrega y **la comunicación directa (chat) entre cliente y mensajero**; ya no hay autogestión conversacional ni asistente. No se afirman datos, métricas ni validación con la operación de Logytech Mobile: no existen.

Honestidad sobre el cambio de alcance: la Introducción (3.3 y 3.5) y la Metodología (5.4) declaran que en octubre de 2026 se retiraron el inventario, los pagos y el asistente conversacional. Si la Entrega 1 ya se entregó con la versión anterior, conviene informar a la docente del ajuste.
