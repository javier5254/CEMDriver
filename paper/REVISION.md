# REVISION: Entregas 1 y 2 de CMEDriver

Control contra las rúbricas (CONVENCIONES.md, sección 12). **Actualizado el 2026-10-09** tras el cambio de alcance (el autor retiró el inventario, los pagos y el chatbot; ver el apartado "Cambios 2026-10-09"). Páginas medidas con Word (COM) el 2026-10-09; las páginas "de contenido" excluyen portada y contraportada (2 páginas) y referencias.

Archivos: `paper/Proyecto_CMEDriver_Entrega1.docx` (10 páginas físicas) y `paper/Proyecto_CMEDriver_Entrega2.docx` (21 páginas físicas), regenerados con `node build.js 1` y `node build.js 2` en `paper/build/`.

## Entrega 1: Resumen + Introducción

| Criterio de la rúbrica | Estado | Evidencia |
|---|---|---|
| (a) Resumen 250 a 350 palabras, 4 o 5 palabras clave, con problema, objetivos, metodología y adelanto del desarrollo | Cumple | 329 palabras (350 contando la línea de palabras clave); 5 palabras clave; sin resultados empíricos; adelanto con seis apps y 72 pruebas del backend; declara lo simulado (usuarios y correo de consola en desarrollo) y la asistencia de IA |
| (b) Planteamiento contextualizado con datos o fuentes académicas, cierra con la pregunta | Cumple | 3.1 usa CCCE 2025, MinTIC 2026, DNP 2023 y 2025 y literatura arbitrada; la hipótesis sobre el operador pequeño ahora habla de agendamiento y comunicación directa, sin compras ni chatbot; la pregunta está en 3.2 con el texto vigente |
| (c) Objetivo general y 3 a 5 específicos con verbos verificables | Cumple | 1 general y 4 específicos (identificar, diseñar y documentar, implementar, formular); el OE-3 ya no incluye chatbot |
| (d) Justificación y beneficiarios | Cumple | 3.4: justificación académica (API, tiempo real, control de acceso en el backend) y práctica, beneficiarios, contraargumento |
| (e) 5 a 10 citas académicas únicas | Cumple | 10 fuentes únicas (sin cambios): Mohammad 2023, Janinhoff 2024, CCCE 2025, MinTIC 2026, DNP 2023, DNP 2025, Gutierrez-Franco 2021, Restrepo-Betancur 2026, Seghezzi 2023, Boom-Cárcamo 2024. Tres son informes oficiales, no académicos |
| Referencias sin huérfanas | Cumple | 10 citadas, 10 en la lista |
| Referencias recientes (70 % de 2021 a 2026) | Cumple | 10 de 10 (100 %) |
| Extensión (Introducción 4 a 5 páginas) | Cumple | Introducción 5 páginas (2 075 palabras; p. 4 a 8, la última al 85 %); Resumen 1 página; referencias 2 páginas; total 10 |
| Tercera persona | Cumple | Sin primera persona |
| Citas textuales de 40 o más palabras | Cumple | Ninguna |
| Afirmaciones empíricas inventadas | Cumple | Ningún resultado propio; "72 pruebas" es el conteo de la suite del backend; los usuarios son simulados |
| Declaración de IA | Parcial | Se anuncia en 3.5 y se desarrolla en la Metodología (Entrega 2); la entrada Anthropic va en las referencias de la Entrega 2 |
| Coherencia con el cambio de alcance | Cumple | Título, resumen, pregunta, objetivo general, OE-3, 3.4 y 3.5 sincronizados con `docs/entrega/01-requerimientos.md` (§1, §2, §2.4); 3.3 y 3.5 declaran que inventario, pagos y asistente conversacional se retiraron en octubre de 2026 |

## Entrega 2: Marco Teórico + Metodología

| Criterio de la rúbrica | Estado | Evidencia |
|---|---|---|
| (a) Marco por subtítulos, analítico, con conceptos, enfoques de software y normativa | Cumple | 4.1 a 4.10; análisis crítico y límites de cada fuente; normativa en 4.8; enfoques en 4.9; Tablas 1 a 3 (términos, datos personales, enfoques). La antigua 4.5 (asistentes conversacionales) se sustituyó por "Agendamiento por el cliente y comunicación directa con el mensajero" |
| (b) 15 a 25 citas únicas en el marco, mayoría de los últimos 5 años | Cumple | **25 fuentes únicas** en el marco (conteo con script sobre cada cita). **15 de 25 (60 %)** son de 2021 a 2026: Mohammad 2023, Restrepo-Betancur 2026, Mogire 2023, Randerath 2025, Madhwal 2022, Souza 2022, Beaulieu 2022, Bogner 2023, Al-Qora'n 2025, Gracia Orejuela 2024, Jazemi 2023, Pérez 2024, OWASP API 2023, Kuhrmann 2022 y Parizi 2022. Las 10 restantes son normas colombianas y andina (Ley 1581, Ley 23, Decisión 351), DNDA (s. f.), ISO 29148 (2018) y fuentes pedidas por la guía (Sommerville 2005, Bass 2003, Beck 2001, Schwaber 2020, Brown s. f.) |
| (c) Enfoque, tipo, naturaleza y diseño coherentes | Cumple | 5.1: aplicada, DSR, cualitativo-descriptivo, mixta después; la pregunta se reformuló en 5.1 con el texto vigente ("cómo puede una plataforma orientada a API integrar…") |
| (d) Herramientas, proceso de selección, arquitectura, etapas | Cumple | 5.3 (proceso en 4 pasos, Tabla 2 sin la fila de chatbot y pagos y con la fila de correo simulado; arquitectura con seis apps y 12 entidades; Figura 1 actualizada; párrafo "Lo que se simula"), 5.1 (fases DSR), 5.4 (etapas) y Actividad 3 en Tabla 4 |
| (e) Coherencia con la Entrega 1 | Cumple | 5.6, Tabla 5, con los 4 objetivos específicos de la sección 3.3 (seis apps, 72 pruebas, usuarios simulados) |
| Actividades 1, 2 y 3 de la Guía 2 | Cumple | Tabla 1 del marco (6 términos; se cambió "agencia excesiva" por "rastreo basado en aplicaciones"), Tabla 2 (datos personales; la fila de chat indica que solo los dos participantes acceden), Tabla 4 de la Metodología; instrumentos en Tabla 1 de la Metodología, planificados |
| Citas en Metodología (3 a 5) | Cumple | 5 fuentes únicas (Peffers, Hernández-Sampieri, Schwaber, Brown, Anthropic) |
| Referencias (mínimo 20 a 25, sin huérfanas) | Cumple | 28 únicas (25 del marco más Peffers, Hernández-Sampieri y Anthropic), generadas desde KEYS en build.js; ninguna cita sin entrada y ninguna entrada sin cita |
| 70 % de 2021 a 2026 en la lista | Parcial | 16 de 28 (57 %): las 15 del marco más Anthropic. Sin contar normas colombianas y andina y Brown s. f. (5), 16 de 23 (70 %). Quedan fuera de rango Sommerville, Bass, Beck, Schwaber, ISO 29148, Peffers y Hernández-Sampieri, exigidas por la guía o metodológicas |
| Extensión (Marco 8 a 10 páginas; Metodología 3 a 4) | Parcial | Medido con Word (COM): Marco 10 páginas (p. 3 a 12; 3 842 palabras de prosa y 408 en tablas); Metodología 6 páginas (p. 13 a 18; 1 269 palabras de prosa y 551 en tablas), por encima de lo sugerido por las tablas obligatorias. Total de contenido 16 páginas; el documento tiene 21 páginas físicas (referencias p. 19 a 21) |
| Tercera persona | Cumple | Sin primera persona |
| Citas textuales de 40 o más palabras | Cumple | Ninguna; el marco y la metodología parafrasean y no incluyen citas entre comillas |
| Afirmaciones empíricas inventadas | Cumple | No hay resultados de CMEDriver; lo atribuido a Madhwal y Souza viene del resumen leído en el pool y se declara su límite; la restricción del chat y las pruebas se verificaron contra `backend/services/views.py`, `consumers.py` y `tests.py` |
| Declaración de IA en texto y referencias | Cumple | 5.7 cita (Anthropic, 2026); aclara que el prototipo no incorpora ningún modelo de lenguaje; entrada en referencias |

## Hallazgos sobre fuentes

- Sin citas huérfanas en ninguna de las dos entregas. Ninguna referencia inventada. Todas las fuentes nuevas (Madhwal et al., 2022; Souza et al., 2022) están verificadas en `fuentes/01-contexto.md` (Crossref y resumen leído).
- La entrada **Anthropic (2026)** no existe en el pool; se tomó literal de CONVENCIONES.md, sección 9.
- Hernández-Sampieri y Mendoza Torres (2018): el pool la verifica con dos autores; pendiente confirmar en la portada del ejemplar si hay un tercero.
- Kuhrmann et al. (2022): referencia tomada del pool (19 autores, sin diacríticos en Münch, Tüzün, López, Küpper).
- Sommerville (2005) y Bass et al. (2003): textos no consultados; el marco lo declara y deja `[COMPLETAR]`.
- Fuentes de normativa y de la docente citadas sin DOI: enlaces según el pool, no revalidados hoy.
- Madhwal et al. (2022) trata una cadena de bloques que CMEDriver no usa, y Souza et al. (2022) es un estudio brasileño de entregas, no de recolecciones: ambos se citan con esa salvedad en 4.2, 4.5 y 4.10.

## Pendientes para el estudiante

1. Completar todos los `[COMPLETAR]` (resaltados en amarillo en los .docx): nombre del estudiante (portada y contraportada), ciudad (Bogotá, por confirmar), registro del software y titularidad de derechos (marco y metodología), definiciones con página de Sommerville (2005) y Bass et al. (2003), número de participantes y criterio de selección, y alcance exacto del uso de IA.
2. Docente asesora en portada: Luisa Fernanda Loza Muñetón, según la guía; verificar ortografía del nombre.
3. Confirmar el nuevo **título provisional** (ya no dice "autogestión conversacional") y, si la Entrega 1 ya se entregó con el chatbot en el objetivo, informar a la docente del ajuste de alcance.
4. Confirmar el tercer autor de Hernández-Sampieri y restituir los diacríticos de Kuhrmann et al.
5. Fuentes verificadas del pool que quedaron fuera del marco por el tope de 25 y que pueden sustituir a otras si se prefiere otro balance: Heinbach et al. (2022; visibilidad, notificaciones y prueba de entrega digital), Fette y Melnikov (2011; protocolo WebSocket), Su et al. (2024; regreso de microservicios a monolito), Stripe (s. f.) y GitHub (s. f.) sobre firma HMAC de webhooks, Krawczyk et al. (1997; HMAC), Ferraiolo et al. (2001; RBAC), Ley 527 de 1999 (mensajes de datos y firma electrónica) y Engelhardt et al. (2026). Para cambiar la lista, editar el texto y `KEYS` en `build/build.js`.
6. La Metodología (6 páginas) excede lo sugerido por las tablas y la figura; podría pasar la Tabla 3 a texto.
7. Verificar los enlaces de las referencias y revisar y reescribir el texto con voz propia (el contenido contó con asistencia de IA).
8. Abrir los .docx en Word, actualizar paginación y revisar el aspecto de las tablas y la Figura 1.
9. Decidir si la Entrega 1 debe incluir la declaración de IA con su referencia (hoy vive en la Entrega 2).
10. Los archivos `.bib` y `.ris` que menciona `referencias/LEEME-Mendeley.md` no están en la carpeta; regenerarlos desde las listas vigentes si se usa Mendeley.

## Cambios 2026-10-09 (sincronización con el cambio de alcance)

Alcance vigente: ciclo de vida del servicio (entregas y recolecciones), tracking GPS y chat en tiempo real (solo cliente dueño y motorizado asignado; ADMIN y ALISTADOR no participan), evidencia digital, planificación de recolección por el cliente con cobertura y leadtime, optimización de ruta con Nominatim, API REST con API Key y webhooks firmados, roles y RBAC; 6 apps Django, 12 entidades y 72 pruebas del backend. Retirados: inventario, pagos y chatbot (con el LLM y la pasarela simulados).

- **Portada y `build.js`:** el título pasó de "…y autogestión conversacional de servicios…" a "…y comunicación directa cliente-mensajero en servicios de mensajería en Colombia".
- **Resumen:** reescrito (problema, pregunta, objetivo, adelanto con seis apps y 72 pruebas, lo simulado: usuarios y correo de consola); palabra clave "asistente conversacional" sustituida por "evidencia digital de entrega".
- **Introducción:** hipótesis del planteamiento (agendamiento y comunicación directa), pregunta y objetivo general con el texto vigente, OE-3 sin chatbot, nota de acotación del Objetivo 3, justificación (control de acceso en el backend en lugar del asistente), alcance y delimitaciones (lo excluido, lo simulado, 72 pruebas) y organización; texto recortado de nuevo a 2 075 palabras.
- **Marco teórico:** se retiró la 4.5 de asistentes y modelos de lenguaje y el término "agencia excesiva"; nueva 4.5 (agendamiento y chat directo: Souza et al., 2022; Ley 1581; OWASP API1); 4.2 incorpora la prueba de entrega (Madhwal et al., 2022); 4.3 sin Su et al. y con seis apps; 4.7 sin la parte de LLM y con autorización por objeto y firma de webhooks; 4.10 sin tool-calling. Se quitaron de la lista OWASP GenAI (2025) y Su et al. (2024) y se agregaron Madhwal et al. (2022) y Souza et al. (2022): 25 citas únicas, 60 % recientes, igual que antes.
- **Metodología:** pregunta reformulada en 5.1; Tabla 1 (pruebas y encuesta sin chatbot); Tabla 2 (sin chatbot y pagos, con la fila de correo simulado); arquitectura con 6 apps y 12 entidades; párrafo "Lo que se simula"; Figura 1 reemplazada por `docs/diagrams/img/c4-2-contenedores.png` (misma figura actualizada, sin pagos ni LLM); 5.4 sin chatbot e inventario y con la nota del ajuste de alcance; Tabla 5 (seis apps, 72 pruebas); 5.7 aclara que el prototipo no incorpora ningún modelo de lenguaje y que la IA fue herramienta del autor.
- **CONVENCIONES.md** (secciones 2, 8, 9, 11, 13 y 14), **README.md**, `referencias/LEEME-Mendeley.md` y esta REVISION.md actualizados.
- Se conservaron los marcadores `[COMPLETAR]`. El pool `fuentes/*.md` no se modificó (sus notas sobre chatbots y LLM son material de investigación, no texto del paper).
