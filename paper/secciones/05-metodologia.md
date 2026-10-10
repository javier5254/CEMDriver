# 5. Metodología

Este capítulo retoma el problema, la pregunta y los cuatro objetivos específicos de la Introducción (sección 3.3) sin replantearlos, y explica cómo se estudió y construyó el prototipo CMEDriver. Se distingue siempre entre lo implementado, lo simulado y lo planificado para la asignatura Trabajo de Grado, donde Logytech Mobile, empresa multinacional de logística, es la organización de aplicación en Colombia (segundo semestre de 2026), sujeto a su autorización.

## 5.1 Enfoque, tipo y diseño de la investigación

La pregunta de investigación indaga cómo una plataforma orientada a API puede integrar la gestión de servicios de mensajería, la trazabilidad en tiempo real, la evidencia digital y el chat directo entre cliente y mensajero: es una pregunta de diseño y no de medición de un fenómeno existente. Por eso el estudio es **investigación aplicada de desarrollo tecnológico**, guiada por Design Science Research (DSR), en la que el conocimiento se genera al construir y aplicar un artefacto (Peffers et al., 2007). Sus seis actividades se asocian así con el proyecto: la identificación del problema y los objetivos de la solución corresponden a la revisión de literatura y a los requisitos (Objetivo 1); el diseño y desarrollo, a los modelos y al prototipo (Objetivos 2 y 3); la demostración, a pruebas automatizadas del backend y recorridos con roles simulados, que no constituyen evaluación empírica; la evaluación, solo al protocolo (Objetivo 4), cuya ejecución es pendiente; y la comunicación, a este documento.

Frente a las rutas cuantitativa, cualitativa y mixta, el enfoque es **predominantemente cualitativo-descriptivo en esta etapa**. Hernández-Sampieri y Mendoza Torres (2018) recogen la postura pragmática, según la cual el planteamiento del problema determina el método y la combinación de rutas solo se justifica si permite responder mejor la pregunta. Aquí no hay hipótesis causales ni variables que medir, porque no existen datos de usuarios reales; la ruta cuantitativa se descarta por ahora, pues afirmar mejoras sería infundado. Lo que se produce son requisitos, modelos y un prototipo descritos de forma sistemática. La ruta se vuelve **mixta** en Trabajo de Grado, con datos cualitativos (entrevistas y observación) y cuantitativos (listas de chequeo, tiempos y escalas de percepción). La **naturaleza** del estudio es descriptiva y de desarrollo; el **diseño** es de ciclos iterativos de construcción con evaluación diferida, sin alcance para comprobar causalidad ni generalizar.

## 5.2 Población, usuarios, técnicas e instrumentos

En esta etapa no hay población ni muestra. La unidad de análisis es el **proceso de un servicio de mensajería** (creación, asignación, ejecución, evidencia y cierre), las fuentes son la literatura y el análisis del dominio, y los roles de administrador, alistador, motorizado y cliente fueron **simulados**; ningún dato proviene de personas reales. Para Trabajo de Grado se **diseña y planifica** una población de personal administrativo y de alistamiento, motorizados y clientes de Logytech Mobile, sujeta a la autorización de la empresa, con muestreo por conveniencia y, por tanto, resultados no generalizables; la unidad de análisis pasa a ser el servicio de mensajería de esa organización: `[COMPLETAR: número de participantes y criterio de selección]`. La Tabla 1 separa los instrumentos usados de los planificados; **ninguno de los segundos se ha aplicado.**

**Tabla 1**

*Técnicas e instrumentos: usados y planificados*

| Técnica | Instrumento | Para qué sirve | Aplicado a | Estado |
|---|---|---|---|---|
| Revisión documental y análisis de requisitos | Matriz de fuentes; fichas RF/RNF e historias de usuario | Caracterizar el problema y derivar requisitos | Literatura y dominio | Usado |
| Modelado y prototipado | Casos de uso, clases, ER, C4; mockups y prototipo | Documentar el diseño y hacer tangibles los requisitos | Artefacto | Usado |
| Pruebas automatizadas | Suites de Django/DRF y de WebSockets (72 pruebas) | Verificar el comportamiento del backend | Código | Usado |
| Entrevista semiestructurada | Guion de preguntas | Validar requisitos y flujos con quienes operan | Personal administrativo y de alistamiento de Logytech Mobile | Planificado |
| Observación | Pauta de observación en campo | Contrastar el flujo con la práctica real | Motorizados de Logytech Mobile | Planificado |
| Encuesta | Cuestionario con escala de usabilidad | Medir percepción del seguimiento y del chat con el mensajero | Clientes de Logytech Mobile | Planificado |
| Prueba piloto | Lista de chequeo de flujos centrales | Verificar que cada flujo se completa con usuarios reales | Los cuatro roles, en Logytech Mobile | Planificado |

*Nota.* Fuente: Elaboración propia.

## 5.3 Herramientas, proceso de selección y arquitectura

La selección siguió cuatro pasos: listar las capacidades que exigen los objetivos (API, tiempo real, aplicación multirol, mapas, evidencia, integraciones), identificar alternativas, puntuarlas con criterios explícitos y registrar la decisión y la alternativa descartada. Los criterios fueron costo cero y ausencia de credenciales (restricción de un proyecto académico individual), rapidez de desarrollo, soporte de los requisitos, posibilidad de evolución a producción y madurez del ecosistema. Las decisiones provienen de la documentación técnica del proyecto (Anexo A) y no de un estudio comparativo formal, lo que se reconoce como limitación. La Tabla 2 presenta el resultado.

**Tabla 2**

*Selección de herramientas y tecnologías*

| Capa | Seleccionada | Alternativa considerada | Criterio decisivo |
|---|---|---|---|
| Backend y autenticación | Django y Django REST Framework; JWT y API Key propia | FastAPI; OAuth2 completo | ORM, administración y autenticación integrados; OAuth2 queda como evolución |
| Tiempo real | Django Channels y Daphne, con respaldo a sondeo | Solo sondeo | Difusión push de GPS y chat; el respaldo da resiliencia |
| Base de datos | SQLite (desarrollo), PostgreSQL (propuesta) | PostgreSQL desde el inicio | Cero configuración ahora, mismo ORM después |
| Frontend y empaquetado | Angular e Ionic; Capacitor | Aplicaciones separadas por rol; desarrollo nativo | Un código para cuatro roles; build de Android no verificado |
| Mapas y geocodificación | Leaflet, OpenStreetMap y Nominatim | Google Maps Platform | Sin llave ni facturación; una solicitud por segundo |
| Correo | `django.core.mail` con backend de consola (**simulado** en desarrollo) | Proveedor transaccional | Sin cuenta ni credenciales; se cambia por configuración |
| Documentación | Markdown, Mermaid y C4 | Herramientas de diseño externas | Texto versionable junto al código |

*Nota.* Fuente: Elaboración propia a partir de la documentación técnica del proyecto (Anexo A).

La arquitectura es **modular, orientada a API**, con seis aplicaciones de dominio (cuentas, cobertura, servicios, seguimiento, optimización e integraciones) en un backend único que persiste 12 entidades, separadas para poder extraerlas después. Se documenta con el modelo C4 (Brown, s. f.); la Figura 1 muestra el nivel de contenedores. La aplicación Ionic y Angular consume la API REST con JWT y recibe posiciones y mensajes por WebSocket; el chat de cada servicio admite solo al cliente propietario y al motorizado asignado, lo que comprueban pruebas automatizadas (REST y WebSocket). Los sistemas externos usan API Key y reciben webhooks firmados con HMAC; el geocodificador, las teselas del mapa y el servidor de correo son servicios externos.

**Figura 1**

*Diagrama C4, nivel de contenedores de CMEDriver*

![Diagrama C4 de contenedores de CMEDriver: aplicación Ionic y Angular, API REST Django, servicio de tiempo real con Channels, base de datos, almacenamiento de evidencias y sistemas externos](../figuras/c4-contenedores.png)

*Nota.* Fuente: Elaboración propia. Los niveles de contexto, componentes y código están en la documentación técnica del proyecto (Anexo A).

**Lo que se simula.** Es poco y se declara: los usuarios (administrador, alistador, motorizado y cliente) son de prueba y, en desarrollo, el correo de restablecimiento de contraseña se imprime en la consola del servidor. El resto (autenticación, ciclo de vida, GPS, chat, webhooks y geocodificación con Nominatim) se ejecuta de verdad, pero en un entorno de desarrollo: el sistema no está desplegado.

## 5.4 Metodología de desarrollo

La guía de la asignatura contrasta tres familias de procesos, que la Tabla 3 compara con las condiciones del proyecto.

**Tabla 3**

*Metodologías de desarrollo frente a las condiciones del proyecto*

| Metodología | Limitación aquí | Decisión |
|---|---|---|
| Cascada | Requisitos cambiantes y sin cliente real que los fije; retroalimentación tardía | Descartada |
| Ágil (Scrum) | Scrum define Scrum Master, Product Owner y equipo (Schwaber & Sutherland, 2020); trabajó una persona con asesoría docente | Prácticas adoptadas, marco no |
| Por prototipos | Riesgo de documentación escasa | **Elegida**, con documentación en paralelo |

*Nota.* Fuente: Elaboración propia.

El desarrollo fue **incremental por prototipos, con iteraciones de inspiración ágil**: se entregó software funcionando por fases (núcleo con roles, servicios y evidencia; tiempo real y planificación de recolecciones; y una segunda versión con optimización de rutas, claves de API y webhooks) y se aceptaron cambios entre fases, como la migración del sondeo a WebSockets y, en octubre de 2026, el ajuste del alcance (sección 3.5). **No se aplicó Scrum completo**: no hubo roles diferenciados, sprints formales ni retrospectivas con un equipo. Se mantuvieron la entrega temprana, la reflexión entre fases y una documentación paralela. Las etapas son MVP y versión 2 (realizadas), Entrega 3 con avance de resultados y, en Trabajo de Grado, validación con usuarios, pruebas definitivas y despliegue.

## 5.5 Actividad 3: síntesis metodológica

**Tabla 4**

*Tipo de investigación, metodología, herramientas y arquitectura*

| Tipo de investigación | Metodología de desarrollo | Herramientas y tecnologías | Arquitectura propuesta |
|---|---|---|---|
| Aplicada, de desarrollo tecnológico (DSR), enfoque cualitativo-descriptivo, mixto en Trabajo de Grado | Incremental por prototipos con iteraciones de inspiración ágil | Django y DRF, Channels, Angular e Ionic, Capacitor, SQLite y PostgreSQL, Leaflet y Nominatim, Mermaid | Modular orientada a API (REST, WebSocket y webhooks), documentada con C4 |

*Nota.* Fuente: Elaboración propia.

## 5.6 Coherencia con la Entrega 1

La Tabla 5 verifica si las decisiones anteriores permiten lograr cada objetivo específico.

**Tabla 5**

*Objetivos específicos y decisiones que los respaldan*

| Objetivo específico (sección 3.3) | Decisión metodológica o arquitectónica | ¿Se logra? |
|---|---|---|
| 1. Identificar problemas y derivar requerimientos | Enfoque cualitativo; revisión documental, análisis del dominio y fichas RF/RNF | Sí, con fuentes secundarias; contraste con personal y clientes de Logytech Mobile en Trabajo de Grado, sujeto a su autorización |
| 2. Diseñar y documentar la arquitectura modular orientada a API y modelarla | Seis aplicaciones de dominio y 12 entidades, REST, WebSocket y webhooks; modelos UML, ER, C4 y mockups | Sí |
| 3. Implementar el prototipo funcional temprano | Desarrollo incremental por prototipos; herramientas de la Tabla 2; pruebas automatizadas | Sí, con 72 pruebas automatizadas del backend, usuarios simulados y Android sin verificar |
| 4. Formular el protocolo de validación | Instrumentos y usuarios de la Tabla 1 (personal y clientes de Logytech Mobile); ruta mixta | Se formula; su ejecución en Logytech Mobile es de Trabajo de Grado, sujeta a autorización |

*Nota.* Fuente: Elaboración propia.

## 5.7 Consideraciones éticas y declaración de uso de inteligencia artificial

CMEDriver trata datos personales en su diseño (nombres, teléfonos, direcciones, ubicación GPS, fotos y firmas de evidencia y mensajes de chat) que entran en el ámbito de la Ley 1581 de 2012. En esta etapa son datos de prueba; antes de trabajar con personas reales se requerirán autorización informada, finalidad definida y medidas de seguridad, cuyo cumplimiento no se ha verificado ni se afirma. `[COMPLETAR: confirmar si se registrará el software]`.

**Declaración de uso de IA.** En el desarrollo del prototipo, la documentación técnica y los borradores de este documento se empleó Claude, un modelo de lenguaje de Anthropic (Anthropic, 2026), como asistente para generar código, documentación y borradores de redacción. El estudiante supervisó el trabajo, editó y reinterpretó el contenido, y las fuentes fueron verificadas contra sus registros originales antes de incluirlas. El asistente no sustituye la autoría ni la responsabilidad del estudiante. La IA fue una herramienta del autor en el desarrollo y la redacción; el prototipo no incorpora ningún modelo de lenguaje en su ejecución. `[COMPLETAR: el estudiante debe confirmar el alcance exacto del uso de IA]`.
