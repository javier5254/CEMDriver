# Pool de fuentes 03: Metodología y normativa

Investigador: paper-investigador. Fecha de consulta de todas las verificaciones: 2026-10-06.
Alcance: Metodología (sección 5) y Marco Teórico 4.8. Subtemas: a) Design Science Research; b) manual de metodología de la investigación; c) desarrollo ágil e iterativo con prototipado; d) calidad de software (ISO/IEC 25010 y calidad en desarrollo ágil); e) normativa colombiana (protección de datos y firma electrónica); f) desarrollo asistido por IA generativa.

Resumen del pool: 22 fuentes verificadas. Tipos: 10 artículos arbitrados, 3 ponencias, 1 libro, 1 documentación técnica oficial (Scrum Guide), 1 norma técnica (ISO/IEC 25010:2023), 5 normas legales colombianas y 1 preprint (Becker et al., 2025, marcado como tal). Frescura: de las 17 fuentes que no son normas legales, 13 son de 2021 a 2026 (76 %); las 4 anteriores a 2021 son fundacionales y se justifican en cada entrada (Hevner et al. 2004, Peffers et al. 2007, Hernández-Sampieri y Mendoza Torres 2018, Schwaber y Sutherland 2020). Contando también las 5 normas legales (por naturaleza fijadas en su fecha de expedición, 1999 a 2015), la proporción 2021-2026 es 13 de 22 (59 %). Contrapuntos incluidos: Kuhrmann et al. (2022, los métodos ágiles "puros" son minoría), López et al. (2022, falta de consenso en medir calidad en desarrollo ágil), Londoño et al. (2023, propuesta sin validación empírica), Becker et al. (2025, el único estudio con efecto negativo en productividad), Borg et al. (2026, sin efecto detectable en mantenibilidad) y Pearce et al. (2022, riesgo de seguridad).

Notas de uso para los redactores:
- Donde dice "según el resumen", solo se leyó el abstract; donde dice "texto completo", se leyó el documento (todo o las secciones indicadas). Hevner et al. y Peffers et al. son de acceso cerrado: solo se leyó el resumen; no atribuirles nada más (por ejemplo, el detalle de sus directrices).
- CMEDriver es un prototipo académico. Las normas colombianas se presentan como requisitos de diseño y trabajo de validación pendiente; no afirmar que el prototipo "cumple" la Ley 1581 ni que su captura de firma constituye una firma electrónica con efectos legales. Ese análisis jurídico no fue verificado (ver "Vacíos").
- La documentación técnica del proyecto (docs/06-cronograma.md) describe fases iterativas con evolución de versiones, pero no declara Scrum. Si el paper menciona Scrum, debe ser como marco de referencia y con la salvedad de que la guía describe un equipo de varias personas (ver Scrum Guide y Ramadhan et al.).
- Los estudios del subtema f) miden desarrolladores profesionales con asistentes de código (Copilot, Cursor); ninguno evalúa a Claude como agente de código ni a CMEDriver. No extrapolar sus cifras al prototipo. La declaración de uso de IA del paper se cita con Anthropic (2026), según CONVENCIONES sección 9.
- Cómo citar normas con el formato de la guía UNINPAHU: la referencia inicia con el título de la norma ("Ley 1581 de 2012. (2012, 17 de octubre). ...") y, por tanto, en el texto se cita (Ley 1581 de 2012) o con artículo: (Ley 1581 de 2012, art. 4). La fecha entre paréntesis es la de expedición, como en los ejemplos de la guía.

---

## a) Design Science Research en sistemas de información e ingeniería de software

### [hevner2004] Hevner et al. (2004)
- Referencia APA 7: Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly, 28*(1), 75–106. https://doi.org/10.2307/25148625
- Tipo: artículo (fundacional)
- Verificación: Crossref (api.crossref.org/works/10.2307/25148625), consultado 2026-10-06: coinciden los cuatro autores y su orden, fecha (2004-03), revista MIS Quarterly, volumen 28(1) y páginas 75-106 (OpenAlex repite 75-106; otras fuentes citan 75-105, por lo que conviene que el estudiante confirme la última página en el PDF). Crossref añade un "1" al final del título (nota al pie del original) que se omite. Resumen leído vía OpenAlex (works/https://doi.org/10.2307/25148625). Texto completo cerrado; el sitio de la revista (misq.umn.edu) bloqueó el acceso automatizado, por lo que no se consultó.
- Hechos verificados (según el resumen):
  - Distingue dos paradigmas en la investigación en sistemas de información: la ciencia del comportamiento, que desarrolla y verifica teorías que explican o predicen el comportamiento humano u organizacional, y la ciencia del diseño, que busca ampliar las capacidades humanas y organizacionales mediante la creación de artefactos nuevos e innovadores.
  - En el paradigma de diseño, el conocimiento sobre el dominio del problema y su solución se obtiene al construir y aplicar el artefacto diseñado.
  - Ofrece un marco conceptual conciso y directrices para comprender, ejecutar y evaluar la investigación de ciencia del diseño, ilustradas con tres ejemplos de la literatura, y analiza los retos de hacer investigación de alta calidad en este paradigma.
- Cita en texto: (Hevner et al., 2004)
- Uso sugerido: Metodología | MT 4.8. Fundacional justificada: es la referencia canónica del enfoque DSR (OpenAlex registra más de 10.000 citas al 2026-10-06). Úsese para justificar que el artefacto (CMEDriver) es el vehículo de generación de conocimiento; combinar con Knauss (2021) para la versión aplicada a trabajos de grado.

### [peffers2007] Peffers et al. (2007)
- Referencia APA 7: Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems, 24*(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302
- Tipo: artículo (fundacional)
- Verificación: Crossref (api.crossref.org/works/10.2753/MIS0742-1222240302), consultado 2026-10-06: coinciden los cuatro autores y su orden, fecha (2007-12; publicado en línea por Taylor & Francis en 2014), revista, volumen 24(3) y páginas 45-77. Resumen leído vía OpenAlex. Texto completo cerrado.
- Hechos verificados (según el resumen):
  - Presenta, demuestra y evalúa una metodología (DSRM) para realizar investigación de ciencia del diseño en sistemas de información; sus autores atribuyen la lenta adopción del enfoque en parte a la falta de una metodología comúnmente aceptada.
  - El proceso tiene seis pasos: identificación y motivación del problema, definición de los objetivos de la solución, diseño y desarrollo, demostración, evaluación y comunicación.
  - La metodología se demuestra y evalúa con cuatro estudios de caso, entre ellos una aplicación de videotelefonía por Internet y una medida de reutilización de software.
- Cita en texto: (Peffers et al., 2007)
- Uso sugerido: Metodología (mapear las fases del proyecto a los seis pasos; el paso de evaluación queda para Trabajo de Grado) | MT 4.8. Fundacional justificada: es el proceso de referencia más usado de DSR (OpenAlex registra más de 7.000 citas al 2026-10-06).

### [knauss2021] Knauss (2021)
- Referencia APA 7: Knauss, E. (2021). Constructive master's thesis work in industry: Guidelines for applying design science research. En *2021 IEEE/ACM 43rd International Conference on Software Engineering: Software Engineering Education and Training (ICSE-SEET)* (pp. 110–121). IEEE. https://doi.org/10.1109/ICSE-SEET52601.2021.00021
- Tipo: ponencia
- Verificación: Crossref (api.crossref.org/works/10.1109/icse-seet52601.2021.00021) y OpenAlex, consultados 2026-10-06: coinciden autor único, año (2021-05), título, actas de ICSE-SEET y páginas 110-121. Texto completo leído en la versión de acceso abierto de arXiv (arXiv:2012.04966v2, 13 feb 2021).
- Hechos verificados (texto completo):
  - Propone siete guías para tesis de maestría basadas en ciencia del diseño, derivadas de 12 tesis analizadas durante siete años: definir el artefacto desde temprano (G1), trabajar en iteraciones que mejoren artefacto y conocimiento (G2), formular las preguntas de investigación según el ciclo regulativo (G3), mantener reuniones periódicas (G4), cambiar el énfasis entre ciclos (G5) y dos guías sobre cómo reportar (G6 y G7).
  - Para G3 sugiere tres preguntas: qué problema tiene la forma actual de hacer algo (RQ1), qué soluciones potenciales lo mitigan (RQ2) y en qué medida el problema se resuelve con ellas (RQ3). Señala que una tesis típica puede completar tres ciclos de aproximadamente un mes cada uno, con énfasis en el problema en el primero, en las soluciones en el segundo y en la evaluación en el tercero.
  - Al comentar las directrices de Hevner et al., el autor indica que existen pocos métodos para construir el artefacto más allá de descripciones generales de enfoques ágiles o iterativos, que interpreta la guía de "proceso de búsqueda" como motivo para trabajar de forma incremental e iterativa, y que los examinadores suelen valorar poco el conocimiento sobre un artefacto concreto (sobre todo si es una herramienta de software) si no se acompaña de preguntas de conocimiento.
  - Limitaciones declaradas: la experiencia del autor se concentra en ingeniería de requisitos y procesos de desarrollo, no es un estudio orientado a la generalización y la evidencia proviene en buena parte de notas y discusiones personales trianguladas con las tesis y publicaciones.
- Cita en texto: (Knauss, 2021)
- Uso sugerido: Metodología (justificar un diseño en ciclos y una pregunta de investigación sobre el problema; reconocer como limitación que la fase de evaluación se hará en Trabajo de Grado) | MT 4.8.

### [goecks2021] Goecks et al. (2021)
- Referencia APA 7: Goecks, L. S., Souza, M. de, Librelato, T. P., & Trento, L. R. (2021). Design science research in practice: Review of applications in industrial engineering. *Gestão & Produção, 28*(4), Artículo e5811. https://doi.org/10.1590/1806-9649-2021v28e5811
- Tipo: artículo (revisión sistemática)
- Verificación: Crossref (api.crossref.org/works/10.1590/1806-9649-2021v28e5811) y OpenAlex, consultados 2026-10-06: coinciden los cuatro autores y su orden, año 2021, revista Gestão & Produção (SciELO), volumen 28(4) y número de artículo e5811; acceso abierto (OpenAlex: gold). Resumen leído vía OpenAlex.
- Hechos verificados (según el resumen):
  - Analiza la aplicación de Design Science Research en las áreas y subáreas de la ingeniería industrial, e identifica clases de problemas, contribuciones y limitaciones de su implementación.
  - Usa revisión sistemática de literatura apoyada en Atlas.ti 8 y análisis de redes para clasificar por área y agrupar por similitudes.
  - Propone una agenda de investigación para replicar el método en áreas emergentes.
- Cita en texto: (Goecks et al., 2021)
- Uso sugerido: MT 4.8 (evidencia de la difusión de DSR fuera de sistemas de información y de sus limitaciones). Pertinencia media: el dominio es ingeniería industrial, no software; solo se leyó el resumen. Uso opcional.

---

## b) Metodología de la investigación (manual de uso en Colombia)

### [hernandez2018] Hernández-Sampieri y Mendoza Torres (2018)
- Referencia APA 7: Hernández-Sampieri, R., & Mendoza Torres, C. P. (2018). *Metodología de la investigación: Las rutas cuantitativa, cualitativa y mixta*. McGraw-Hill Interamericana.
- Tipo: libro (ISBN 978-1-4562-6096-5)
- Verificación: tres registros de catálogo y la editorial, consultados 2026-10-06. (1) Catálogo de la Biblioteca de la ESAP, Colombia (biblioteca.esap.edu.co/bib/31602): autores Roberto Hernández Sampieri y Christian Paulina Mendoza Torres, McGraw-Hill Interamericana, México, 2018, ISBN 9781456260965. (2) Open Library (openlibrary.org/api/books?bibkeys=ISBN:9781456260965): mismo ISBN-13, McGraw Hill Education, 2018 (el dígito de control del ISBN-13 se comprobó y es válido). (3) Repositorio de la UASB (repositorio.uasb.edu.bo/items/70dca925-d1b4-49f0-ae97-26eb71787891): primera edición, 2018. Página de la editorial (highered.mheducation.com/sites/1456260960/information_center_view0/index.html): obra de 2018, ISBN-10 1456260960. Discrepancia a tener en cuenta: la página de la editorial lista además a Sergio Méndez Valencia como tercer autor y titula la obra "Las rutas de la investigación cuantitativa, cualitativa y mixta", mientras que los tres catálogos y la reseña citada abajo registran dos autores y el título sin "de la investigación". Se adopta la forma de los catálogos; el estudiante debe confirmar autores y título en la portada del ejemplar que use. La edición de 2014 (6.ª, ISBN 1456223968) es la anterior y fue reemplazada por esta, por lo que no se usa.
- Hechos verificados (página de la editorial, reseña y un capítulo en línea de la editorial leído en texto completo):
  - Según la editorial, es una obra nueva (primera edición, 2018) que sustituye al texto "Metodología de la investigación", publicado en seis ediciones durante casi 28 años; trata la investigación científica y la investigación aplicada al desarrollo profesional.
  - Según una reseña (Cruz Picón, 2025, *Estudios sobre las Culturas Contemporáneas*, 2(4), 195-199, Redalyc), el libro tiene seis partes y diecisiete capítulos: rutas de investigación en los capítulos 1 y 2, ruta cuantitativa en los capítulos 3 a 10 (incluye planteamiento del problema, marco teórico, alcance, hipótesis, diseño, muestreo y análisis), ruta cualitativa en los capítulos 11 a 14, reporte de resultados en el 15, ruta mixta en el 16 y protocolo de investigación en el 17. La reseña no se incluye en Referencias; solo respalda la estructura.
  - El capítulo 11 en línea de la editorial (ampliación de los métodos mixtos, cap11sampieri.pdf) recoge cuatro posturas ante la combinación de los enfoques cuantitativo y cualitativo (fundamentalistas, separatistas, integradores y pragmáticos) y señala que, para los pragmáticos, el planteamiento del problema y las circunstancias son los que determinan el método, de modo que la combinación solo conviene si es la que mejor permite responder las preguntas de investigación.
- Cita en texto: (Hernández-Sampieri & Mendoza Torres, 2018)
- Uso sugerido: Metodología (definir enfoque, alcance y diseño del estudio). No se leyó el texto de los capítulos sobre alcance y diseño; para afirmar definiciones concretas (por ejemplo, alcance exploratorio o descriptivo) el redactor o el estudiante debe consultar el libro. Fundacional vigente justificado: es el manual de metodología de mayor uso en la educación superior colombiana y en la guía del curso.

---

## c) Desarrollo ágil e iterativo, equipos pequeños y prototipado

### [schwaber2020] Schwaber y Sutherland (2020)
- Referencia APA 7: Schwaber, K., & Sutherland, J. (2020). *The Scrum Guide: The definitive guide to Scrum: The rules of the game*. Scrum Guides. https://scrumguides.org/scrum-guide.html
- Tipo: documentación técnica (guía oficial del marco)
- Verificación: sitio oficial scrumguides.org (versión HTML, que indica ser una copia directa de la versión de noviembre de 2020) y su PDF oficial (scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-US.pdf), consultados 2026-10-06: la portada del PDF dice "Ken Schwaber & Jeff Sutherland, The Scrum Guide, The Definitive Guide to Scrum: The Rules of the Game, November 2020"; licencia Creative Commons Attribution Share-Alike 4.0. Texto leído en el PDF.
- Hechos verificados (texto completo):
  - Define Scrum como un marco ligero que ayuda a generar valor mediante soluciones adaptativas a problemas complejos; se funda en el empirismo y el pensamiento lean, con un enfoque iterativo e incremental, y sus pilares son transparencia, inspección y adaptación.
  - El equipo Scrum consta de un Scrum Master, un Product Owner y Developers; es una unidad pequeña, típicamente de 10 personas o menos, sin subequipos ni jerarquías. Los Sprints son eventos de duración fija de un mes o menos.
  - Los tres artefactos son el Product Backlog (compromiso: Product Goal), el Sprint Backlog (Sprint Goal) y el Incremento (Definition of Done).
  - La propia guía advierte que cambiar el núcleo de Scrum o dejar elementos por fuera "oculta problemas" y limita sus beneficios; esto da una base para discutir con cautela cualquier adaptación a un equipo de una sola persona.
- Cita en texto: (Schwaber & Sutherland, 2020)
- Uso sugerido: Metodología | MT 4.8. Fundacional justificada: es la definición oficial vigente del marco. Si el paper afirma que el desarrollo fue iterativo por fases, citar la guía solo como referencia conceptual y contrastarla con Ramadhan et al. (2025) y Kuhrmann et al. (2022).

### [ramadhan2025] Ramadhan et al. (2025)
- Referencia APA 7: Ramadhan, A. R. P., Waspada, I., Bahtiar, N., & Pramayoga, A. S. (2025). Applying the Scrum method in software development for undergraduate thesis project implementation. *Jurnal Masyarakat Informatika, 16*(1), 119–133. https://doi.org/10.14710/jmasif.16.1.73187
- Tipo: artículo (estudio de caso)
- Verificación: Crossref (api.crossref.org/works/10.14710/jmasif.16.1.73187) y OpenAlex, consultados 2026-10-06: coinciden los cuatro autores (OpenAlex lista tres; el PDF y Crossref listan cuatro), año 2025 (2025-05-30), revista, volumen 16(1) y páginas 119-133; acceso abierto (diamante). Texto completo leído (PDF de ejournal.undip.ac.id). Se observó una discrepancia interna: el resumen de Crossref/OpenAlex dice 13 elementos de backlog y el PDF dice 64; por eso no se cita esa cifra.
- Hechos verificados (texto completo):
  - Plantean que no existe una guía específica para aplicar Scrum en proyectos de grado individuales (un estudiante con dos asesores) y proponen un modelo de adaptación: el primer asesor actúa como Product Owner y tester, el segundo como Scrum Master y tester, y el estudiante como Developer y asistente de ambos roles.
  - Reportan cuatro sprints de 10 días hábiles cada uno, con revisiones integradas a las reuniones de avance de la tesis, y concluyen que el esquema adaptado favoreció la comunicación estructurada con los asesores, la flexibilidad ante cambios de requisitos y la finalización a tiempo, con valores reales de puntos de historia cercanos a los planificados salvo en un sprint retrasado por el aprendizaje de nuevas tecnologías.
  - Limitación: es un único caso, en una sola universidad, y los asesores asumen roles (incluido el de tester) que la guía de Scrum no prevé; los propios autores sugieren explorar el modelo en otros contextos académicos.
- Cita en texto: (Ramadhan et al., 2025)
- Uso sugerido: Metodología (precedente de adaptación de Scrum a un proyecto de grado de un solo desarrollador con asesor; úsese para justificar o matizar la forma de trabajo, sin afirmar que CMEDriver siguió este modelo) | MT 4.8.

### [kuhrmann2022] Kuhrmann et al. (2022)
- Referencia APA 7: Kuhrmann, M., Tell, P., Hebig, R., Klunder, J., Munch, J., Linssen, O., Pfahl, D., Felderer, M., Prause, C. R., MacDonell, S. G., Nakatumba-Nabende, J., Raffo, D., Beecham, S., Tuzun, E., Lopez, G., Paez, N., Fontdevila, D., Licorish, S. A., Kupper, S., . . . Richardson, I. (2022). What makes agile software development agile? *IEEE Transactions on Software Engineering, 48*(9), 3523–3539. https://doi.org/10.1109/TSE.2021.3099532
- Tipo: artículo (estudio empírico, encuesta internacional)
- Verificación: Crossref (api.crossref.org/works/10.1109/tse.2021.3099532), consultado 2026-10-06: 47 autores (se listan los 19 primeros, puntos suspensivos y el último, según APA 7), Kuhrmann primero y Richardson último; volumen 48(9), septiembre de 2022, páginas 3523-3539 (publicado en línea en 2021, por eso OpenAlex indica 2021; se cita 2022, año del volumen). Los apellidos se transcriben como los devuelve Crossref, sin diacríticos (p. ej., Munch, Tuzun, Lopez, Kupper); el estudiante puede restituir las tildes (Münch, Tüzün, López, Küpper). Resumen leído vía OpenAlex; acceso abierto verde (hdl.handle.net/10923/20122).
- Hechos verificados (según el resumen):
  - Parte de que, por evolución o por factores del contexto, los procesos de software en la práctica se vuelven híbridos respecto de los métodos ágiles tal como los prescriben sus creadores, y pregunta qué hace ágil a un método de desarrollo.
  - Con una encuesta internacional de 556 datos, halla que menos del 15 % de los participantes opera sus proyectos de forma puramente tradicional o puramente ágil, y que la elección de prácticas pesa más en el grado de agilidad que la del método.
  - Concluye que ningún método ni práctica garantiza o impide explícitamente la agilidad, y que esta no puede definirse solo en el nivel del proceso.
- Cita en texto: (Kuhrmann et al., 2022)
- Uso sugerido: Metodología | MT 4.8 (contrapunto: justifica describir el proceso por sus prácticas concretas y no por la etiqueta "Scrum" o "ágil").

### [londono2023] Londoño et al. (2023)
- Referencia APA 7: Londoño, I., Agredo-Delgado, V., & Ruiz Melenje, P. H. (2023). Agile prototyping strategy for building shared understanding in requirements engineering. *I+T+C Investigación, Tecnología y Ciencia, 1*(17). https://doi.org/10.57173/ritc.v1n17a6
- Tipo: artículo (propuesta metodológica; autores colombianos)
- Verificación: Crossref (api.crossref.org/works/10.57173/ritc.v1n17a6), OpenAlex y la página de la revista (doi.org/10.57173/ritc.v1n17a6, Unicomfacauca), consultados 2026-10-06: coinciden título, año 2023 (2023-11-15), volumen 1, número 17 y DOI, y el orden de autores Londoño, Agredo-Delgado, Ruiz Melenje (la página de la revista y Crossref coinciden). El PDF imprime el orden Londoño, Ruiz, Agredo-Delgado y una abreviatura distinta del nombre de la revista; se adoptó el orden de Crossref y de la página de la revista. No hay rango de páginas ni número de artículo. Acceso abierto (diamante). Texto leído: resumen y secciones 3 y 5 a 7.
- Hechos verificados (texto completo parcial):
  - Construyen, con Ingeniería de Métodos Situacionales y a partir de dos mapeos sistemáticos de literatura (el primero con 354 artículos identificados y 27 estudios primarios), una estrategia de prototipado ágil para lograr entendimiento compartido de los requisitos entre las partes interesadas.
  - La estrategia tiene fases de planificación, identificación y análisis de requisitos, prototipos no funcionales, gestión de requisitos, prototipos funcionales y socialización, y sostiene que los prototipos dan una representación visual y tangible de los requisitos que facilita la comunicación y la retroalimentación.
  - Limitación: en las secciones leídas no se reporta una validación empírica de la estrategia; las conclusiones sobre ahorro de tiempo, menos errores o mejores requisitos se presentan como propósito o expectativa, no como resultado medido. Debe citarse como propuesta, no como evidencia de efectividad.
- Cita en texto: (Londoño et al., 2023)
- Uso sugerido: MT 4.8 (prototipado en ingeniería de requisitos, justificación de los mockups y del prototipo temprano), siempre con la salvedad de que es una propuesta conceptual sin validación.

---

## d) Calidad de software

### [iso25010-2023] ISO/IEC (2023)
- Referencia APA 7: International Organization for Standardization & International Electrotechnical Commission. (2023). *Systems and software engineering — Systems and software quality requirements and evaluation (SQuaRE) — Product quality model* (ISO/IEC 25010:2023). https://www.iso.org/standard/78176.html
- Tipo: norma (técnica)
- Verificación: la página de iso.org bloqueó el acceso automatizado (HTTP 403 y desafío de Cloudflare), por lo que no se leyó. El título, la fecha y el estado se contrastaron en tres organismos nacionales de normalización, consultados 2026-10-06: EVS de Estonia (evs.ee/en/iso-iec-25010-2023), SIS de Suecia (sis.se, ficha de ISO/IEC 25010:2023) y AFNOR de Francia (boutique.afnor.org), que coinciden en el título exacto, la fecha de noviembre de 2023 (15 de noviembre de 2023), la vigencia y el reemplazo de la edición de 2011; SIS y AFNOR indican 22 páginas. El identificador de iso.org (78176) aparece en un resultado de búsqueda de iso.org y en la ficha de Genorma (iso:proj:78176). La lista de las nueve características se tomó del texto HTML del portal iso25000.com (no oficial de ISO). Texto de la norma (de pago) no leído.
- Hechos verificados (fichas de organismos de normalización y portal iso25000.com):
  - La edición 2023 (segunda edición) define un modelo de calidad del producto aplicable a productos TIC y de software, compuesto por nueve características subdivididas en subcaracterísticas, que sirve de modelo de referencia para especificar, medir y evaluar la calidad a lo largo del ciclo de vida, para desarrolladores, adquirentes, personal de aseguramiento de calidad y evaluadores independientes.
  - Las nueve características son: adecuación funcional, eficiencia de desempeño, compatibilidad, capacidad de interacción, fiabilidad, seguridad, mantenibilidad, flexibilidad y seguridad operacional o "safety" (en inglés: functional suitability, performance efficiency, compatibility, interaction capability, reliability, security, maintainability, flexibility, safety).
  - Frente a la versión de 2011, según una descripción que cita al sitio de ISO (quality.arc42.org/articles/iso-25010-update-2023): se añadió "safety", "usability" pasó a llamarse "interaction capability" y "portability" pasó a "flexibility", con nuevas subcaracterísticas (inclusividad, autodescriptividad, resistencia y escalabilidad). La versión de 2011 se titulaba "Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models", tenía ocho características de calidad del producto y fue retirada (EVS: retirada desde 2024-03-04); el título de 2023 se limita al modelo de calidad del producto.
- Cita en texto: (International Organization for Standardization & International Electrotechnical Commission [ISO/IEC], 2023) la primera vez y (ISO/IEC, 2023) después
- Uso sugerido: Metodología (criterios de validación que se ejecutarán en Trabajo de Grado) | MT 4.8. Los requisitos no funcionales del proyecto (docs/13) se agrupan en seguridad, mantenibilidad, usabilidad y rendimiento, que corresponden a características del modelo (usabilidad figura como capacidad de interacción en la edición 2023). Si se prefiere citar la edición de 2011 por su uso en la literatura, la referencia equivalente sería: International Organization for Standardization & International Electrotechnical Commission. (2011). *Systems and software engineering — Systems and software quality requirements and evaluation (SQuaRE) — System and software quality models* (ISO/IEC 25010:2011), pero está retirada; se recomienda la de 2023 y declarar la diferencia.

### [plevnik2027] Plevnik y Jereb (2027)
- Referencia APA 7: Plevnik, M., & Jereb, B. (2027). Evaluating logistics software quality: A systematic review and research agenda for ISO/IEC 25010 across supply chain digitalization research. *Computer Standards & Interfaces, 99*, Artículo 104187. https://doi.org/10.1016/j.csi.2026.104187
- Tipo: artículo (revisión sistemática)
- Verificación: Crossref (api.crossref.org/works/10.1016/j.csi.2026.104187) y OpenAlex, consultados 2026-10-06: coinciden los dos autores, título, revista, volumen 99 y número de artículo 104187. Fechas: registrado en Crossref el 2026-07-07 y asignado al volumen 99 de enero de 2027, por lo que la referencia lleva 2027 (año del volumen); si el docente prefiere el año de disponibilidad en línea, sería 2026. Acceso abierto híbrido. Resumen leído vía OpenAlex.
- Hechos verificados (según el resumen):
  - Sostienen que la calidad del software logístico rara vez se evalúa con marcos normalizados y que ISO/IEC 25010:2023 no se había aplicado de forma integral al software logístico.
  - Revisión sistemática bajo PRISMA 2020 con 224 artículos (de 554 registros, seis bases de datos): solo 11 citan ISO/IEC 25010 y solo cinco la aplican directamente a software logístico.
  - Las características más frecuentes en los artículos son compatibilidad y adecuación funcional (60 % cada una), fiabilidad (46 %), mantenibilidad (45 %) y capacidad de interacción (36 %); seguridad aparece solo en 21 %. Proponen un perfil preliminar de calidad para software logístico.
- Cita en texto: (Plevnik & Jereb, 2027)
- Uso sugerido: MT 4.8 y Metodología (respaldo para usar ISO/IEC 25010 como marco de evaluación en el dominio logístico y para justificar que la seguridad no puede quedar relegada). Solo se leyó el resumen.

### [lopez2022] López et al. (2022)
- Referencia APA 7: López, L., Burgués, X., Martínez-Fernández, S., Vollmer, A. M., Behutiye, W., Karhapää, P., Franch, X., Rodríguez, P., & Oivo, M. (2022). Quality measurement in agile and rapid software development: A systematic mapping. *Journal of Systems and Software, 186*, Artículo 111187. https://doi.org/10.1016/j.jss.2021.111187
- Tipo: artículo (mapeo sistemático)
- Verificación: Crossref (api.crossref.org/works/10.1016/j.jss.2021.111187) y OpenAlex, consultados 2026-10-06: coinciden los nueve autores y su orden, año 2022 (volumen 186, abril de 2022; publicado en línea en 2021), revista y número de artículo 111187. Resumen leído vía OpenAlex.
- Hechos verificados (según el resumen):
  - Mapea la literatura sobre gestión de requisitos de calidad mediante métricas en desarrollo ágil y rápido; selecciona 61 estudios primarios (2001 a 2019).
  - Halla que, pese a la abundancia de conocimiento y normas, no hay consenso sobre cómo medir los requisitos de calidad: la terminología y los modelos de medición varían, aunque tienen similitudes.
  - Señala que atributos como seguridad y usabilidad cuentan sorprendentemente con pocas métricas reportadas.
- Cita en texto: (López et al., 2022)
- Uso sugerido: MT 4.8 (contrapunto: en desarrollo ágil la medición de calidad no está estandarizada, lo que justifica definir criterios explícitos de validación con ISO/IEC 25010).

---

## e) Normativa colombiana

Qué decreto aplica (confirmado): el texto reglamentario vigente de la Ley 1581 de 2012 está en el Decreto 1074 de 2015, Capítulo 25 (artículos 2.2.2.25.1.1 a 2.2.2.25.7.8). Ese capítulo compila el Decreto 1377 de 2013 (cada artículo del capítulo remite a "Decreto 1377 de 2013, art. N"); el Registro Nacional de Bases de Datos (Decreto 886 de 2014) está en el Capítulo 26. La SIC lo confirma en su política de tratamiento de datos (sedeelectronica.sic.gov.co/politica-de-tratamiento-de-datos-personales): "Decretos 1377 de 2013 y 886 de 2014 (hoy incorporados en el Decreto Único 1074 de 2015)". En consecuencia, citar el Decreto 1074 de 2015 como norma aplicable y mencionar el Decreto 1377 de 2013 solo como origen. Matiz: el Gestor Normativo de Función Pública marca el Decreto 1377 de 2013 como "Derogado parcialmente por el Decreto 1081 de 2015" y no precisa en la página qué disposiciones; no se profundizó. De igual modo, la firma electrónica (Decreto 2364 de 2012) está compilada en el Decreto 1074 de 2015, Capítulo 47 (artículos 2.2.2.47.1 a 2.2.2.47.8, más el 2.2.2.47.9 sobre transformación digital, agregado después).

### [ley1581-2012] Ley 1581 de 2012
- Referencia APA 7: Ley 1581 de 2012. (2012, 17 de octubre). Por la cual se dictan disposiciones generales para la protección de datos personales. Diario Oficial No. 48.587. http://www.secretariasenado.gov.co/senado/basedoc/ley_1581_2012.html
- Tipo: norma (ley estatutaria)
- Verificación: Secretaría del Senado (URL de la referencia; el sitio solo respondió por http) y Gestor Normativo de Función Pública (funcionpublica.gov.co/eva/gestornormativo/norma.php?i=49981), consultados 2026-10-06: coinciden título, fecha de expedición (17 de octubre de 2012) y publicación en el Diario Oficial No. 48.587 de 18 de octubre de 2012. El Senado la encabeza como "Ley Estatutaria 1581 de 2012" y su texto estaba actualizado al 30 de septiembre de 2026. Función Pública la registra como reglamentada por los Decretos 1377 de 2013, 886 de 2014 y 1081 de 2015. Texto de los artículos citados leído en el sitio del Senado.
- Hechos verificados (texto leído):
  - Desarrolla el derecho constitucional a conocer, actualizar y rectificar la información recogida en bases de datos (art. 1) y se aplica al tratamiento de datos personales registrados en cualquier base de datos por entidades públicas o privadas, en territorio colombiano (art. 2).
  - Define autorización como consentimiento previo, expreso e informado del Titular, y dato personal como cualquier información vinculada o asociable a una o varias personas naturales determinadas o determinables; el tratamiento incluye recolección, almacenamiento, uso, circulación o supresión (art. 3).
  - Establece los principios de legalidad, finalidad, libertad, veracidad o calidad, transparencia, acceso y circulación restringida, seguridad y confidencialidad (art. 4); los datos sensibles incluyen los biométricos (art. 5) y su tratamiento está prohibido salvo excepciones como la autorización explícita (art. 6).
  - Reconoce derechos al Titular, entre ellos conocer, actualizar y rectificar sus datos, solicitar prueba de la autorización y presentar quejas ante la Superintendencia de Industria y Comercio (art. 8); exige autorización previa e informada, obtenida por un medio que permita su consulta posterior (art. 9); y asigna la vigilancia a la Superintendencia de Industria y Comercio (art. 19).
- Cita en texto: (Ley 1581 de 2012) o (Ley 1581 de 2012, art. 4)
- Uso sugerido: MT 4.8 (marco legal de datos personales de clientes, direcciones, ubicación GPS de los motorizados y evidencias de entrega). Cuidado: la ubicación y la foto de evidencia pueden constituir datos personales y, si se usan para identificar a una persona, datos biométricos sensibles; el paper debe tratarlo como un requisito por analizar, no como cumplimiento ya verificado. Varios literales fueron declarados condicionalmente exequibles (el sitio del Senado lo marca; Función Pública remite a la sentencia C-748 de 2011, no revisada).

### [decreto1074-2015] Decreto 1074 de 2015
- Referencia APA 7: Decreto 1074 de 2015. (2015, 26 de mayo). Por medio del cual se expide el Decreto Único Reglamentario del Sector Comercio, Industria y Turismo. Diario Oficial No. 49.523. https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=76608
- Tipo: norma (decreto único reglamentario)
- Verificación: Gestor Normativo de Función Pública (URL de la referencia), consultado 2026-10-06: título, fecha de expedición (26 de mayo de 2015), versión integrada con última actualización del 18 de septiembre de 2025, y texto de los capítulos 25 y 47 leído. El número del Diario Oficial (49.523 del 26 de mayo de 2015) se tomó del Régimen Legal de Bogotá D.C. de la Secretaría Jurídica Distrital (alcaldiabogota.gov.co/sisjur/normas/Norma1.jsp?i=62508, registro del Decreto Único Reglamentario 1074 de 2015), porque la página de Función Pública deja vacío ese campo. Fuente complementaria: MinCIT (mincit.gov.co/normatividad/decretos/2015/decreto-1074-de-2015-por-medio-del-cual-se-expide) y su PDF original, que confirman título y fecha.
- Hechos verificados (texto leído):
  - Capítulo 25 ("Reglamenta parcialmente la Ley 1581 de 2012") compila el Decreto 1377 de 2013: limita la recolección a datos pertinentes y adecuados a la finalidad, prohíbe medios engañosos o fraudulentos (art. 2.2.2.25.2.1) y exige que el responsable adopte procedimientos para solicitar la autorización a más tardar al recolectar los datos, informando los datos y las finalidades específicas (art. 2.2.2.25.2.2).
  - Exige políticas de tratamiento en lenguaje claro con contenido mínimo (identificación del responsable, finalidad, derechos, canal de consultas y reclamos, vigencia) y, cuando no sea posible ponerlas a disposición, un aviso de privacidad (arts. 2.2.2.25.3.1 y 2.2.2.25.3.2).
  - Regula la responsabilidad demostrada: el responsable debe poder demostrar a la SIC medidas apropiadas y efectivas, proporcionales a su naturaleza y tamaño, a la naturaleza de los datos, al tipo de tratamiento y a los riesgos (arts. 2.2.2.25.6.1 y 2.2.2.25.6.2). La Sección 7 (normas corporativas vinculantes) fue adicionada por el Decreto 255 de 2022.
  - Capítulo 47 ("Firma electrónica") compila el Decreto 2364 de 2012 (ver entrada correspondiente).
- Cita en texto: (Decreto 1074 de 2015, art. 2.2.2.25.2.2)
- Uso sugerido: MT 4.8 (marco reglamentario de datos personales y firma electrónica; es la forma vigente de citar el Decreto 1377 de 2013 y el Decreto 2364 de 2012).

### [decreto1377-2013] Decreto 1377 de 2013
- Referencia APA 7: Decreto 1377 de 2013. (2013, 27 de junio). Por el cual se reglamenta parcialmente la Ley 1581 de 2012. Diario Oficial No. 48.834. https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=53646
- Tipo: norma (decreto reglamentario; compilado en el Decreto 1074 de 2015)
- Verificación: Gestor Normativo de Función Pública, consultado 2026-10-06: título, fecha de expedición y entrada en vigencia (27 de junio de 2013), publicación en el Diario Oficial 48834 del 27 de junio de 2013, 28 artículos; encabezado "Derogado parcialmente por el Decreto 1081 de 2015". Su incorporación al Decreto 1074 de 2015 (Capítulo 25, cada artículo con la nota "Decreto 1377 de 2013, art. N") se verificó en el texto del Decreto 1074 y en la política de la SIC.
- Hechos verificados (texto leído):
  - Reglamenta parcialmente la Ley 1581 de 2012; según la ficha de Función Pública, trata el ámbito personal o doméstico, las definiciones, la autorización, las políticas de tratamiento, el ejercicio de los derechos de los titulares, las transferencias y transmisiones internacionales y la responsabilidad demostrada.
  - Sus 27 artículos sustantivos hoy figuran como los artículos 2.2.2.25.1.1 a 2.2.2.25.6.2 del Decreto 1074 de 2015; el artículo 28 es de vigencia.
- Cita en texto: (Decreto 1377 de 2013), solo cuando se mencione el origen; para la norma aplicable citar el Decreto 1074 de 2015.
- Uso sugerido: MT 4.8 (nota breve que explique que el Decreto 1377 de 2013 hoy está compilado en el Decreto 1074 de 2015). Opcional como referencia independiente: puede omitirse de Referencias si el texto cita solo el Decreto 1074.

### [ley527-1999] Ley 527 de 1999
- Referencia APA 7: Ley 527 de 1999. (1999, 18 de agosto). Por medio de la cual se define y reglamenta el acceso y uso de los mensajes de datos, del comercio electrónico y de las firmas digitales, y se establecen las entidades de certificación y se dictan otras disposiciones. Diario Oficial No. 43.673. http://www.secretariasenado.gov.co/senado/basedoc/ley_0527_1999.html
- Tipo: norma (ley)
- Verificación: Secretaría del Senado (URL de la referencia, solo por http) y Gestor Normativo de Función Pública (funcionpublica.gov.co/eva/gestornormativo/norma.php?i=4276), consultados 2026-10-06: coinciden título, fecha de expedición (18 de agosto de 1999) y Diario Oficial No. 43.673 de 21 de agosto de 1999. Texto de los artículos citados leído en el Senado.
- Hechos verificados (texto leído):
  - Se aplica a todo tipo de información en forma de mensaje de datos, con las excepciones del art. 1; define mensaje de datos como la información generada, enviada, recibida, almacenada o comunicada por medios electrónicos, ópticos o similares, y firma digital como un valor numérico asociado al mensaje y a la clave del iniciador que permite verificar origen e integridad (art. 2).
  - No se niegan efectos jurídicos, validez o fuerza obligatoria a la información por estar en forma de mensaje de datos (art. 5); el requisito de firma se satisface con un método que identifique al iniciador, indique que el contenido cuenta con su aprobación y sea confiable y apropiado para el propósito del mensaje (art. 7).
  - Los mensajes de datos son admisibles como medio de prueba (art. 10) y su fuerza probatoria se valora con las reglas de la sana crítica, atendiendo la confiabilidad de la generación, archivo y comunicación, la conservación de la integridad y la identificación del iniciador (art. 11).
- Cita en texto: (Ley 527 de 1999) o (Ley 527 de 1999, art. 7)
- Uso sugerido: MT 4.8 (base jurídica de la evidencia digital de entrega y de la firma capturada). El art. 10 remite al Código de Procedimiento Civil; el redactor no debe afirmar qué estatuto procesal aplica hoy sin verificarlo (ver "Vacíos"). No presentar la firma dibujada en pantalla como equivalente a la firma digital definida en el art. 2.

### [decreto2364-2012] Decreto 2364 de 2012
- Referencia APA 7: Decreto 2364 de 2012. (2012, 22 de noviembre). Por medio del cual se reglamenta el artículo 7° de la Ley 527 de 1999, sobre la firma electrónica y se dictan otras disposiciones. Diario Oficial No. 48.622. https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=50583
- Tipo: norma (decreto reglamentario; compilado en el Decreto 1074 de 2015, Capítulo 47)
- Verificación: Gestor Normativo de Función Pública, consultado 2026-10-06: título, fecha de expedición y entrada en vigencia (22 de noviembre de 2012) y publicación en el Diario Oficial 48622 del 22 de noviembre de 2012; texto completo leído. Su compilación en el Decreto 1074 de 2015, Capítulo 47 (artículos 2.2.2.47.1 a 2.2.2.47.8, cada uno con la nota "Decreto 2364 de 2012, art. N"), se verificó en el texto del Decreto 1074.
- Hechos verificados (texto leído):
  - Define firma electrónica como métodos tales como códigos, contraseñas, datos biométricos o claves criptográficas privadas que permiten identificar a una persona en relación con un mensaje de datos, siempre que el método sea confiable y apropiado para los fines de la firma, según las circunstancias y los acuerdos pertinentes (art. 1; hoy art. 2.2.2.47.1).
  - Considera confiable la firma electrónica si los datos de creación corresponden exclusivamente al firmante y si es posible detectar cualquier alteración posterior del mensaje (art. 4), y le reconoce la misma validez y efectos jurídicos que la firma, si cumple los requisitos del art. 3 (art. 5).
  - Presume, salvo prueba en contrario, que los mecanismos de identificación o autenticación acordados entre las partes cumplen los requisitos de firma electrónica; quien provee el método debe asegurar que sea técnicamente seguro y confiable y probarlo si es necesario (art. 7), y la seguridad puede apreciarse con factores como un concepto técnico de perito o una auditoría independiente (art. 8).
- Cita en texto: (Decreto 2364 de 2012) o, para la versión vigente, (Decreto 1074 de 2015, art. 2.2.2.47.3)
- Uso sugerido: MT 4.8 (marco de la firma electrónica de la evidencia de recolección). Como la definición dice "métodos tales como", no se sigue de ella, sin análisis jurídico, que una firma manuscrita capturada en la pantalla del celular califique; el paper debe plantearlo como criterio de diseño (confiabilidad, integridad, custodia de datos de creación) y como asunto por validar.

---

## f) Desarrollo de software asistido por IA generativa: productividad, calidad y riesgos

### [cui2026] Cui et al. (2026)
- Referencia APA 7: Cui, K. Z., Demirer, M., Jaffe, S., Musolff, L., Peng, S., & Salz, T. (2026). The effects of generative AI on high-skilled work: Evidence from three field experiments with software developers. *Management Science*. Publicación anticipada en línea. https://doi.org/10.1287/mnsc.2025.00535
- Tipo: artículo (experimentos de campo)
- Verificación: Crossref (api.crossref.org/works/10.1287/mnsc.2025.00535) y OpenAlex, consultados 2026-10-06: coinciden los seis autores y su orden, título, revista Management Science (INFORMS) y publicación en línea el 2026-02-27; Crossref aún no registra volumen ni número. Resumen leído vía OpenAlex; texto completo cerrado.
- Hechos verificados (según el resumen):
  - Evalúa el efecto de un asistente de código basado en IA generativa mediante ensayos controlados aleatorizados en Microsoft, Accenture y una empresa anónima de Fortune 100, con 4.867 desarrolladores.
  - Al combinar los tres experimentos halla un aumento de 26,08 % (error estándar 10,3 %) en las tareas completadas, aunque cada experimento es ruidoso y los resultados varían entre ellos.
  - Los desarrolladores con menos experiencia mostraron mayor adopción y mayores ganancias de productividad.
- Cita en texto: (Cui et al., 2026)
- Uso sugerido: Metodología (consideraciones éticas y declaración de uso de IA) | MT 4.8. Matiz: mide tareas completadas por profesionales con completado de código; no mide calidad, seguridad ni agentes de código, y no puede extrapolarse a un prototipo académico.

### [borg2026] Borg et al. (2026)
- Referencia APA 7: Borg, M., Hewett, D., Hagatulah, N., Couderc, N., Söderberg, E., Graham, D., Kini, U., & Farley, D. (2026). Echoes of AI: Investigating the downstream effects of AI assistants on software maintainability. *Empirical Software Engineering, 31*(6), Artículo 161. https://doi.org/10.1007/s10664-026-10889-1
- Tipo: artículo (experimento controlado preregistrado)
- Verificación: Crossref (api.crossref.org/works/10.1007/s10664-026-10889-1) y OpenAlex, consultados 2026-10-06: coinciden los ocho autores y su orden, título, revista, volumen 31(6), número de artículo 161 y publicación en línea el 2026-06-09. Acceso abierto híbrido. Resumen leído vía OpenAlex; la página de Springer redirigió a un inicio de sesión y no se leyó el texto completo.
- Hechos verificados (según el resumen):
  - Experimento controlado en dos fases, preregistrado, con 151 participantes (95 % desarrolladores profesionales): en la fase 1 se añadió una funcionalidad a una aplicación web en Java con o sin asistente de IA; en la fase 2, un ensayo aleatorizado, otros participantes evolucionaron esas soluciones sin IA.
  - La fase 2 no halló diferencias significativas en tiempo de finalización ni en calidad de código; el análisis bayesiano sugiere que cualquier mejora en velocidad o calidad por el uso de IA fue, como máximo, pequeña y muy incierta. Los resultados observacionales de la fase 1 mostraron una reducción mediana de 30,7 % en el tiempo con asistente.
  - Los autores concluyen que, dentro del alcance de sus tareas y medidas, no detectaron ventajas ni desventajas sistemáticas de mantenibilidad, y señalan como riesgos por estudiar el exceso de código generado y la "deuda cognitiva".
- Cita en texto: (Borg et al., 2026)
- Uso sugerido: MT 4.8 (calidad, mantenibilidad y matiz crítico frente a Cui et al.; conecta con la característica de mantenibilidad de ISO/IEC 25010) | Metodología (declaración de uso de IA).

### [pearce2022] Pearce et al. (2022)
- Referencia APA 7: Pearce, H., Ahmad, B., Tan, B., Dolan-Gavitt, B., & Karri, R. (2022). Asleep at the keyboard? Assessing the security of GitHub Copilot's code contributions. En *2022 IEEE Symposium on Security and Privacy (SP)* (pp. 754–768). IEEE. https://doi.org/10.1109/SP46214.2022.9833571
- Tipo: ponencia
- Verificación: Crossref (api.crossref.org/works/10.1109/sp46214.2022.9833571) y OpenAlex, consultados 2026-10-06: coinciden los cinco autores y su orden, año (2022-05), actas de IEEE S&P y páginas 754-768. Existe una versión posterior en *Communications of the ACM* 68(2), 96-105 (https://doi.org/10.1145/3610721, 2025), con el mismo resumen y autores, verificada también en Crossref; se cita la ponencia original. Resumen leído vía OpenAlex; texto completo cerrado.
- Hechos verificados (según el resumen):
  - Investiga sistemáticamente con qué frecuencia y en qué condiciones GitHub Copilot recomienda código inseguro, usando 89 escenarios relacionados con debilidades de la lista "Top 25" de CWE de MITRE, que producen 1.689 programas.
  - Examina tres ejes: diversidad de debilidades, de instrucciones (prompts) y de dominios.
  - Encuentra que aproximadamente 40 % de los programas generados eran vulnerables.
- Cita en texto: (Pearce et al., 2022)
- Uso sugerido: Metodología (riesgos del código asistido por IA y necesidad de revisión humana y pruebas) | MT 4.8. Limitación: evalúa el Copilot de la época del estudio (2021-2022); sus cifras no se extrapolan a herramientas actuales ni a Claude.

### [becker2025] Becker et al. (2025)
- Referencia APA 7: Becker, J., Rush, N., Barnes, E., & Rein, D. (2025). *Measuring the impact of early-2025 AI on experienced open-source developer productivity* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2507.09089
- Tipo: preprint (no arbitrado según lo verificado)
- Verificación: DataCite (api.datacite.org/dois/10.48550/arxiv.2507.09089) y OpenAlex, consultados 2026-10-06: coinciden los cuatro autores (DataCite: Becker, Joel; Rush, Nate; Barnes, Elizabeth; Rein, David), año 2025, título y tipo preprint en arXiv (arxiv.org/abs/2507.09089). OpenAlex no registra versión publicada en revista. Resumen leído vía DataCite.
- Hechos verificados (según el resumen):
  - Ensayo controlado aleatorizado con 16 desarrolladores de código abierto con experiencia moderada en IA, que completan 246 tareas en proyectos maduros que conocen desde hace unos cinco años en promedio; cada tarea permite o prohíbe herramientas de IA de principios de 2025 (principalmente Cursor Pro y Claude 3.5/3.7 Sonnet).
  - Los desarrolladores pronosticaban que la IA reduciría el tiempo en 24 % y luego estimaron una reducción de 20 %, pero el resultado medido fue que permitir IA aumentó el tiempo de finalización en 19 %.
  - Los autores advierten que no se puede descartar por completo la influencia de artefactos del experimento, aunque la robustez del efecto sugiere que probablemente no sea su causa principal.
- Cita en texto: (Becker et al., 2025)
- Uso sugerido: MT 4.8 (contrapunto crítico: el efecto sobre la productividad depende del contexto y de la experiencia). Presentarlo explícitamente como preprint y con muestra pequeña (16 desarrolladores).

### [sallou2024] Sallou et al. (2024)
- Referencia APA 7: Sallou, J., Durieux, T., & Panichella, A. (2024). Breaking the silence: The threats of using LLMs in software engineering. En *Proceedings of the 2024 ACM/IEEE 44th International Conference on Software Engineering: New Ideas and Emerging Results* (pp. 102–106). ACM. https://doi.org/10.1145/3639476.3639764
- Tipo: ponencia (ICSE-NIER)
- Verificación: Crossref (api.crossref.org/works/10.1145/3639476.3639764) y OpenAlex, consultados 2026-10-06: coinciden los tres autores y su orden, año 2024 (2024-04-14), actas de ICSE-NIER 2024 y páginas 102-106; acceso abierto (oro). Resumen leído vía OpenAlex.
- Hechos verificados (según el resumen):
  - Plantea que numerosos factores pueden influir en los resultados de experimentos con modelos de lenguaje grandes (LLM) en ingeniería de software y abre la discusión sobre amenazas a la validez de la investigación basada en LLM, entre ellas los modelos de código cerrado, la posible fuga de datos entre el entrenamiento del modelo y la evaluación, y la reproducibilidad de los hallazgos.
  - Propone un conjunto de directrices para investigadores de ingeniería de software y para proveedores de modelos de lenguaje, ilustrado con buenas prácticas existentes y un ejemplo de generación de casos de prueba.
- Cita en texto: (Sallou et al., 2024)
- Uso sugerido: Metodología (consideraciones éticas y declaración de uso de IA: justifica registrar qué modelo se usó, para qué y con qué límites de reproducibilidad) | MT 4.8.

---

## Fuentes descartadas

- Barletta et al. (2023), "Clinical-chatbot AHP evaluation based on 'quality in use' of ISO/IEC 25010", *International Journal of Medical Informatics, 170*, 104951, DOI 10.1016/j.ijmedinf.2022.104951. Los metadatos se verificaron en Crossref (cinco autores, volumen y número de artículo coinciden), pero no se pudo leer ningún resumen: OpenAlex no lo trae, PubMed y Semantic Scholar no lo registran y el PDF del repositorio institucional devolvió HTTP 403. Sin lectura no se pueden atribuir hechos. Sería útil para evaluar el chatbot con ISO/IEC 25010 si el estudiante lo lee.
- Obaid (2024), "Using Prototypes in Agile Software Development", *International Journal of Computers and Informatics, 3*(2), 23-38, DOI 10.59992/ijci.2024.v3n2p2. Verificada en Crossref y con resumen leído, pero descartada: es un texto descriptivo de un solo autor cuyo resumen no declara método ni datos, en una revista de baja visibilidad. Se reemplazó por Londoño et al. (2023).
- Peng et al. (2023), "The Impact of AI on Developer Productivity: Evidence from GitHub Copilot" (arXiv:2302.06590, tarea de implementar un servidor HTTP, 55,8 % más rápido). Solo se consultó en OpenAlex y es un preprint; el hallazgo de productividad lo cubre Cui et al. (2026), arbitrado, del que Peng es coautora.
- Hernández Sampieri, Méndez Valencia y Mendoza Torres (2014), *Metodología de la investigación* (6.ª ed., ISBN 1456223968). Verificada en la página de la editorial, pero es la edición anterior, reemplazada por la de 2018.
- Dato descartado dentro de una fuente consultada: la descripción de quality.arc42.org/articles/iso-25010-update-2023, tal como la devolvió la herramienta de lectura, listaba "Operability" y "Sustainability" entre las nueve características. Al leer el HTML crudo, la página no contiene esa lista (solo menciona los cambios) y el portal iso25000.com lista otras nueve (adecuación funcional, eficiencia de desempeño, compatibilidad, capacidad de interacción, fiabilidad, seguridad, mantenibilidad, flexibilidad y safety). Se usó esta última; la lista de arc42 no debe usarse.
- Páginas que no se pudieron leer y no se usaron como fuente: iso.org (HTTP 403 y desafío de Cloudflare) y misq.umn.edu (desafío de Cloudflare); no se intentó eludir el control de acceso.

## Vacíos

- Manual de metodología: solo hay un manual (Hernández-Sampieri y Mendoza Torres, 2018), de cuyo texto no se leyeron los capítulos sobre alcance y diseño; no se verificó un segundo manual de uso en Colombia. Las definiciones de enfoque, alcance y diseño deben tomarse del libro físico o de biblioteca.
- Design Science Research: Hevner et al. y Peffers et al. son de acceso cerrado y solo se leyó el resumen (no se pueden describir sus siete directrices ni el detalle de cada paso). No se encontró, además de Knauss (2021), una guía reciente de DSR específica para ingeniería de software con acceso verificable; Goecks et al. (2021) es de ingeniería industrial.
- Prototipado e iteración: la única fuente sobre prototipado ágil (Londoño et al., 2023) es una propuesta sin validación empírica; no hay un estudio empírico verificado 2021-2026 sobre desarrollo incremental con prototipos en proyectos de grado. La única fuente sobre Scrum con un solo desarrollador (Ramadhan et al., 2025) es un caso único.
- ISO/IEC 25010: no se leyó el texto de la norma (de pago, y iso.org bloqueó el acceso). Los nombres de las nueve características provienen de un portal no oficial (iso25000.com) contrastado con el conteo de nueve de EVS, SIS y AFNOR; las subcaracterísticas no se verificaron en la norma. Conviene que el estudiante consulte la norma en la biblioteca de UNINPAHU o en ICONTEC (no se verificó si existe una NTC equivalente).
- Normativa: (1) no se verificó el valor probatorio vigente de los mensajes de datos frente al Código General del Proceso (Ley 1564 de 2012), dado que el art. 10 de la Ley 527 remite al Código de Procedimiento Civil; (2) no hay análisis jurídico verificado sobre si la firma dibujada en la pantalla califica como firma electrónica según el Decreto 2364 de 2012; (3) no se revisó el Decreto 886 de 2014 (Registro Nacional de Bases de Datos, Capítulo 26 del Decreto 1074) ni si CMEDriver tendría que inscribirse; (4) no se revisaron circulares ni guías de la SIC, ni la sentencia C-748 de 2011 de control de constitucionalidad de la Ley 1581; (5) no se verificó el significado exacto de la marca "derogado parcialmente por el Decreto 1081 de 2015" en el Decreto 1377 de 2013; (6) no se cubrió la normativa colombiana de comercio electrónico o de protección al consumidor.
- IA generativa en desarrollo: los estudios verificados evalúan asistentes de código (Copilot, Cursor) con profesionales; no se encontró un estudio verificado que evalúe agentes tipo Claude Code ni proyectos académicos con asistencia de IA. El estudio con efecto negativo (Becker et al., 2025) es un preprint con 16 participantes. Tampoco se cubrió literatura sobre buenas prácticas de declaración de uso de IA en investigación; para el paper rige la guía de UNINPAHU (CONVENCIONES sección 9).
