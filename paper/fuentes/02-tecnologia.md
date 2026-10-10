# Pool de fuentes 02: Tecnología

Investigador: paper-investigador. Fecha de consulta de todas las verificaciones: 2026-10-06.

Alcance: Marco Teórico 4.3 a 4.7 y justificación de tecnologías en la Metodología. Supuesto de trabajo (no confirmado en CONVENCIONES): MT 4.3 = diseño de APIs, API-first, webhooks y arquitectura (monolito modular frente a microservicios); MT 4.4 = comunicación en tiempo real y aplicaciones híbridas multiplataforma; MT 4.5 = asistente conversacional y modelos de lenguaje con invocación de herramientas; MT 4.6 = optimización de rutas y geocodificación; MT 4.7 = seguridad (JWT, control de acceso por roles, HMAC, seguridad de APIs). Si el índice real del Marco Teórico difiere, las etiquetas "Uso sugerido" deben reasignarse por subtema (a a g).

Resumen del pool: 37 fuentes verificadas (se pidieron 15; se entregan más para dar margen de elección, con un núcleo recomendado más abajo). 29 son de 2021 a 2026 (78 %; las dos páginas de documentación sin fecha, Stripe y GitHub, y la de Capacitor y la política de Nominatim se cuentan como vigentes en 2026). Las 8 anteriores a 2021 son fundacionales o de estándar y están justificadas en cada entrada: Dantzig y Ramser (1959), Krawczyk et al. (1997), Fielding (2000), Ferraiolo et al. (2001), Fette y Melnikov (2011), Jones et al. (2015), Hougardy y Wilde (2015) y Dunér y Nilsson (2020, único estudio hallado que compara webhooks y polling). Tipos: 19 artículos, 7 ponencias o capítulos de congreso, 2 tesis (una doctoral fundacional y una de pregrado), 3 RFC del IETF y 6 documentos de documentación técnica o guías abiertas (OWASP x2, Stripe, GitHub, Capacitor y la política de uso de Nominatim). Contrapuntos y limitaciones incluidos: Su et al. (2024) y Mendonça et al. (2021) sobre el regreso de microservicios a monolito; Al-Qora'n y Al-Said Ahmad (2025) sobre los vacíos del monolito modular; Gracia Orejuela et al. (2024) sobre datos que no respaldan del todo su propia conclusión; Oliveira et al. (2023) sobre el costo de los marcos multiplataforma; Brynjolfsson et al. (2025) sobre efectos heterogéneos de la IA en atención al cliente; Greshake et al. (2023), Zhan et al. (2024) y Huang et al. (2025) sobre riesgos de los LLM; Hougardy y Wilde (2015) sobre el peor caso del vecino más cercano; Pérez y Aybar (2024) y Kılıç et al. (2023) sobre la calidad de la geocodificación y de OpenStreetMap; Yang et al. (2026) y Shatnawi et al. (2024) sobre vulnerabilidades en implementaciones de JWT.

Notas de uso para los redactores:
- Donde dice "según el resumen", solo se leyó el abstract; donde dice "texto completo", se leyó el documento (todo o las secciones indicadas).
- Ninguna de estas fuentes evalúa a CMEDriver. Respaldan conceptos, riesgos y decisiones de diseño. No debe escribirse que alguna "demuestra" que el prototipo funciona mejor. Recordar la sección 8 de CONVENCIONES: el modelo de lenguaje del chatbot es simulado (`MockLLMClient`), así que la literatura de riesgos de LLM se usa como consideración de diseño de la arquitectura de tool-calling, no como evaluación de un LLM real.
- Las entradas de documentación técnica (Stripe, GitHub, Capacitor, OWASP, Nominatim) no son literatura arbitrada; sirven para describir prácticas de la industria y el contexto de uso de cada tecnología. Citarlas como tales.
- Varias fuentes tienen acceso abierto (por ejemplo Su et al., Bogner et al., Nicolescu y Tudorache, Jazemi et al.). Las de IEEE y ACM pueden exigir acceso institucional.

Núcleo recomendado si el Marco Teórico solo admite unas 16 de este archivo: Fielding (2000), Bogner et al. (2023), Lercher et al. (2024), Su et al. (2024), Al-Qora'n y Al-Said Ahmad (2025), Fette y Melnikov (2011), Oliveira et al. (2023), Brynjolfsson et al. (2025), Greshake et al. (2023), Qu et al. (2025), OWASP GenAI Security Project (2025), Jazemi et al. (2023), Pérez y Aybar (2024), Jones et al. (2015), Yang et al. (2026) y OWASP API Security Project (2023).

---

## a) Diseño de APIs REST, enfoque API-first, webhooks e integración de sistemas

### [fielding2000] Fielding (2000)
- Referencia APA 7: Fielding, R. T. (2000). *Architectural styles and the design of network-based software architectures* [Tesis doctoral, University of California, Irvine]. https://ics.uci.edu/~fielding/pubs/dissertation/top.htm
- Tipo: tesis doctoral (fundacional)
- Verificación: página oficial de la tesis (ics.uci.edu/~fielding/pubs/dissertation/top.htm y abstract.htm), consultadas 2026-10-06 con WebFetch y curl: coinciden título, autor, institución (University of California, Irvine), grado (Doctor of Philosophy in Information and Computer Science) y año 2000. El resumen se leyó directamente en abstract.htm. No tiene DOI.
- Hechos verificados (texto del resumen):
  - Define un estilo arquitectónico como un conjunto nombrado y coordinado de restricciones arquitectónicas, y propone usar estilos para guiar el diseño de software de aplicaciones en red.
  - Introduce el estilo REST (Representational State Transfer) y describe cómo se usó para guiar el diseño y desarrollo de la arquitectura de la Web moderna.
  - Según el resumen, REST enfatiza la escalabilidad de las interacciones entre componentes, la generalidad de las interfaces, el despliegue independiente de componentes y el uso de componentes intermediarios para reducir la latencia, reforzar la seguridad y encapsular sistemas heredados.
  - Justificación como fundacional: es el origen del término y la definición de REST; ninguna fuente posterior lo reemplaza como referencia de origen. Verificado también que el capítulo 5 se titula "Representational State Transfer (REST)" (WebFetch).
- Cita en texto: (Fielding, 2000)
- Uso sugerido: MT 4.3 | Metodología

### [bogner2023] Bogner et al. (2023)
- Referencia APA 7: Bogner, J., Kotstein, S., & Pfaff, T. (2023). Do RESTful API design rules have an impact on the understandability of Web APIs? *Empirical Software Engineering, 28*(6), Article 132. https://doi.org/10.1007/s10664-023-10367-y
- Tipo: artículo (estudio empírico, experimento controlado)
- Verificación: Crossref (api.crossref.org/works/10.1007/s10664-023-10367-y), consultado 2026-10-06: coinciden los tres autores, título, revista, volumen 28, número 6, número de artículo 132 y año (en línea 2023-09-26; número de noviembre de 2023). Resumen leído en el propio registro de Crossref.
- Hechos verificados (según el resumen):
  - Los autores señalan que existen muchas reglas de diseño de APIs, pero que falta evidencia empírica sobre la efectividad de la mayoría de ellas.
  - Realizaron un experimento controlado en la web con 105 participantes (industria y academia) sobre 12 reglas de diseño REST, comparando fragmentos de API que cumplen la regla con fragmentos que la violan.
  - Para 11 de las 12 reglas, las versiones que violaban la regla tuvieron peor desempeño en las preguntas de comprensión, y en 9 de 12 las violaciones se calificaron como más difíciles de entender. La experiencia previa con REST no influyó en el desempeño de comprensión para las violaciones.
  - Los autores presentan sus resultados como una primera evidencia empírica de la importancia de seguir reglas de diseño en APIs REST.
- Cita en texto: (Bogner et al., 2023)
- Uso sugerido: MT 4.3

### [beaulieu2022] Beaulieu et al. (2022)
- Referencia APA 7: Beaulieu, N., Dascalu, S. M., & Hand, E. (2022). API-first design: A survey of the state of academia and industry. En S. Latifi (Ed.), *ITNG 2022 19th International Conference on Information Technology-New Generations* (pp. 73–79). Springer. https://doi.org/10.1007/978-3-030-97652-1_10
- Tipo: ponencia (capítulo de actas de congreso; revisión de literatura académica y gris)
- Verificación: Crossref (capítulo 10.1007/978-3-030-97652-1_10 y volumen 10.1007/978-3-030-97652-1, que registra a Shahram Latifi como editor) y página del editor (link.springer.com/chapter/10.1007/978-3-030-97652-1_10), consultados 2026-10-06: coinciden autores, título, libro (ITNG 2022), páginas 73-79, año 2022 y ISBN 978-3-030-97652-1. El resumen se leyó en la página de Springer.
- Hechos verificados (según el resumen):
  - Plantean que el resultado esperado del diseño de microservicios es una API bien definida, pero que persisten desafíos para definir y exponer APIs limpias.
  - Describen el principio API-first: todas las capacidades de una organización y sus sistemas se exponen mediante una API, y la base del diseño del sistema es la definición de APIs claras y bien definidas.
  - Reconocen como desafío la "infancia" del tema y la necesidad de investigación arbitrada que defina guías de adopción y una línea base; el capítulo explora publicaciones académicas y literatura gris y plantea líneas de investigación futuras.
  - Uso crítico: respalda la definición de API-first y, a la vez, permite señalar que la base académica del enfoque era todavía escasa.
- Cita en texto: (Beaulieu et al., 2022)
- Uso sugerido: Intro | MT 4.3

### [lercher2024] Lercher et al. (2024)
- Referencia APA 7: Lercher, A., Glock, J., Macho, C., & Pinzger, M. (2024). Microservice API evolution in practice: A study on strategies and challenges. *Journal of Systems and Software, 215*, Article 112110. https://doi.org/10.1016/j.jss.2024.112110
- Tipo: artículo (estudio empírico cualitativo, entrevistas)
- Verificación: Crossref (api.crossref.org/works/10.1016/j.jss.2024.112110), consultado 2026-10-06: coinciden los cuatro autores, título, revista, volumen 215, número de artículo 112110 y año 2024 (septiembre). Resumen leído vía OpenAlex. Un pasaje adicional (sección 4.5.2) se consultó en la versión preprint de arXiv (2311.08175) mediante ar5iv y WebFetch, es decir, con resumen automático de la herramienta y no con lectura directa del PDF; conviene que el estudiante confirme el pasaje en el artículo publicado.
- Hechos verificados:
  - Según el resumen: 17 entrevistas semiestructuradas con desarrolladores, arquitectos y gerentes de 11 empresas, analizadas con codificación abierta (teoría fundamentada), sobre APIs REST y comunicación orientada a eventos mediante brokers.
  - Según el resumen: identificaron seis estrategias (centradas en compatibilidad hacia atrás, versionado y colaboración entre equipos) y seis desafíos (análisis del impacto de los cambios, comunicación ineficaz de los cambios y consumidores que dependen de versiones desactualizadas), y los resumen en dos problemas: acoplamiento organizacional estrecho y dependencia forzada del consumidor.
  - Según el preprint (sección 4.5.2, "Follow the API-first approach"): 11 de los 17 participantes siguen el enfoque API-first, es decir, acuerdan la definición de la API con los consumidores antes de implementar.
- Cita en texto: (Lercher et al., 2024)
- Uso sugerido: MT 4.3

### [duner2020] Dunér y Nilsson (2020)
- Referencia APA 7: Dunér, D., & Nilsson, M. (2020). *Scalability of push and pull based event notification: A comparison between webhooks and polling* [Trabajo de grado de pregrado, KTH Royal Institute of Technology]. DiVA. http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-279546
- Tipo: tesis de pregrado (no arbitrada; fundacional por falta de alternativa)
- Verificación: OpenAlex (works/W3082018009), consultado 2026-10-06: coinciden título, autores, año 2020, tipo "bachelorThesis" cosechado del repositorio DiVA de KTH con el URN indicado. Resumen leído vía OpenAlex. Advertencia: la página del repositorio (kth.diva-portal.org) no respondió desde este entorno (conexión rechazada con WebFetch y curl), por lo que la verificación es solo contra OpenAlex. El estudiante debe abrir el enlace y confirmar los datos antes de usarla.
- Hechos verificados (según el resumen):
  - Compara webhooks (método basado en push) y polling (basado en pull) como métodos de notificación de eventos cuando aumenta el tráfico, con el fin de dar una base a los desarrolladores para elegir método.
  - Mide uso de CPU, uso de memoria y tiempo de respuesta.
  - Las pruebas indicaron que los webhooks rinden mejor en la mayoría de las circunstancias, pero los autores advierten que hace falta probar en un entorno mejor definido para llegar a una conclusión confiable.
  - Uso crítico: es la única evidencia comparativa hallada sobre webhooks frente a polling. Por ser trabajo de pregrado y con conclusión explícitamente provisional, citarla solo como indicio y con cautela. Es anterior a 2021 (excepción justificada).
- Cita en texto: (Dunér & Nilsson, 2020)
- Uso sugerido: MT 4.3

### [stripe-webhooks] Stripe (s. f.)
- Referencia APA 7: Stripe. (s. f.). *Receive Stripe events in your webhook endpoint*. Stripe Documentation. Recuperado el 6 de octubre de 2026, de https://docs.stripe.com/webhooks
- Tipo: documentación técnica
- Verificación: WebFetch de https://docs.stripe.com/webhooks, 2026-10-06; se leyó la página completa (título confirmado: "Receive Stripe events in your webhook endpoint"). Sin fecha de publicación en la página.
- Hechos verificados (texto completo):
  - Stripe firma cada evento incluyendo una firma en el encabezado `Stripe-Signature` y recomienda verificarla; sin verificación, un atacante podría enviar eventos falsos para disparar acciones como cumplir pedidos, conceder acceso o modificar registros.
  - La firma se genera con HMAC y SHA-256, usando el secreto de firma del endpoint como clave y la cadena "marca de tiempo, punto y cuerpo de la solicitud" como mensaje; la verificación debe usar comparación de cadenas en tiempo constante para evitar ataques de temporización.
  - Contra los ataques de repetición, la marca de tiempo forma parte de lo firmado y las bibliotecas aplican por defecto una tolerancia de 5 minutos; recomienda rotar periódicamente los secretos de firma.
  - Buenas prácticas: responder rápido con un 2xx y procesar de forma asíncrona, guardar los identificadores de evento para evitar duplicados, no depender del orden de entrega (no está garantizado) y tener en cuenta los reintentos automáticos de la plataforma.
  - Uso crítico: es práctica de un proveedor comercial, no evidencia académica. Sirve para mostrar que la firma HMAC con marca de tiempo es un patrón corriente en la industria.
- Cita en texto: (Stripe, s. f.)
- Uso sugerido: MT 4.3 | MT 4.7 | Metodología

### [github-webhooks] GitHub (s. f.)
- Referencia APA 7: GitHub. (s. f.). *Validating webhook deliveries*. GitHub Docs. Recuperado el 6 de octubre de 2026, de https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
- Tipo: documentación técnica
- Verificación: WebFetch de https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries, 2026-10-06 (título confirmado: "Validating webhook deliveries"). El contenido llegó como resumen automático de la herramienta, no como texto completo.
- Hechos verificados (según el resumen de la herramienta sobre la página):
  - Recomienda crear un secreto aleatorio de alta entropía y guardarlo fuera del código.
  - La firma se calcula con HMAC-SHA256 sobre el contenido (payload) usando ese secreto y llega en el encabezado `X-Hub-Signature-256`, con prefijo "sha256=".
  - Aconseja comparar con funciones de tiempo constante (por ejemplo `secure_compare` o `crypto.timingSafeEqual`) en lugar de operadores de igualdad comunes, para evitar ataques de temporización.
- Cita en texto: (GitHub, s. f.)
- Uso sugerido: MT 4.7 | Metodología (usar junto con Stripe como segundo ejemplo; si hay límite de referencias, basta una de las dos)

---

## b) Monolito modular frente a microservicios

### [su2024] Su et al. (2024)
- Referencia APA 7: Su, R., Li, X., & Taibi, D. (2024). From microservice to monolith: A multivocal literature review. *Electronics, 13*(8), Article 1452. https://doi.org/10.3390/electronics13081452
- Tipo: artículo (revisión de literatura multivocal)
- Verificación: Crossref (api.crossref.org/works/10.3390/electronics13081452), consultado 2026-10-06: coinciden los tres autores, título, revista, volumen 13(8), número de artículo 1452 y año 2024 (en línea 2024-04-11). Resumen leído en Crossref (licencia CC BY 4.0).
- Hechos verificados (según el resumen):
  - Los autores afirman que el fenómeno de volver de microservicios a monolito ha aumentado en frecuencia y genera un debate intenso en la industria; la revisión investiga los motivos y los aspectos a cuidar al hacerlo.
  - Identifican cuatro casos de regreso (el plano de control de Istio, el servicio de monitoreo de Amazon Prime Video, Segment e InVision) y cinco razones principales: costo, complejidad, escalabilidad, rendimiento y organización.
  - Durante el regreso señalan seis aspectos clave, entre ellos unificar el almacenamiento de datos, abandonar técnicas diversas y aprender a usar principios de diseño modular.
  - Las opiniones de los practicantes fueron mixtas, y la mayoría consideró que el regreso exige analizar la situación real del sistema y sus principios.
- Cita en texto: (Su et al., 2024)
- Uso sugerido: MT 4.3 | Metodología (justificación del monolito modular)

### [mendonca2021] Mendonça et al. (2021)
- Referencia APA 7: Mendonça, N. C., Box, C., Manolache, C., & Ryan, L. (2021). The monolith strikes back: Why Istio migrated from microservices to a monolithic architecture. *IEEE Software, 38*(5), 17–22. https://doi.org/10.1109/MS.2021.3080335
- Tipo: artículo (informe de experiencia industrial)
- Verificación: Crossref (api.crossref.org/works/10.1109/ms.2021.3080335) y OpenAlex, consultados 2026-10-06: coinciden los cuatro autores, título, revista, volumen 38(5), páginas 17-22 y año 2021 (septiembre). El resumen se leyó en la página de Google Research (research.google/pubs/the-monolith-strikes-back-why-istio-migrated-from-microservices-to-a-monolithic-architecture/). Crossref escribe "Mendonca" sin cedilla; OpenAlex y Google Research usan "Mendonça". El PDF de IEEE no se pudo abrir desde este entorno, así que no se leyó el texto completo.
- Hechos verificados (según el resumen):
  - Señala que existen relativamente pocos informes industriales de proyectos de microservicios en los que los inconvenientes superan los beneficios.
  - Reporta las decisiones de diseño, los compromisos y las lecciones aprendidas del proyecto Istio (service mesh de código abierto), que adoptó microservicios desde temprano y luego migró a una arquitectura monolítica.
  - Uso crítico: sirve como caso de contrapunto a la adopción por defecto de microservicios; al ser un solo caso de un proyecto de infraestructura de gran escala, no se generaliza a una plataforma pequeña como CMEDriver.
- Cita en texto: (Mendonça et al., 2021)
- Uso sugerido: MT 4.3

### [goncalves2021] Gonçalves et al. (2021)
- Referencia APA 7: Gonçalves, N. M., Faustino, D., Silva, A. R., & Portela, M. (2021). Monolith modularization towards microservices: Refactoring and performance trade-offs. En *2021 IEEE 18th International Conference on Software Architecture Companion (ICSA-C)* (pp. 1–8). IEEE. https://doi.org/10.1109/ICSA-C52384.2021.00015
- Tipo: ponencia (estudio empírico de un caso)
- Verificación: Crossref (api.crossref.org/works/10.1109/icsa-c52384.2021.00015) y OpenAlex, consultados 2026-10-06: coinciden los cuatro autores, título, congreso ICSA-C 2021, páginas 1-8 y año 2021 (marzo). Crossref escribe los apellidos sin tilde; OpenAlex usa "Gonçalves" y "Nuno M." (iniciales tomadas de OpenAlex). Resumen leído vía OpenAlex.
- Hechos verificados (según el resumen):
  - Analizan el impacto de migrar un objeto de dominio "rico" (con entidades de dominio fuertemente conectadas, que favorecen la reutilización) hacia una arquitectura modular, tanto en el costo de desarrollo del refactor como en el costo de rendimiento en la ejecución.
  - Sostienen que dividir la lógica de negocio en módulos con interfaces bien definidas introduce un costo de rendimiento.
  - Observan que el esfuerzo de migración y los problemas de rendimiento ya son relevantes al migrar hacia un monolito modular, y no solo al migrar hacia microservicios, que es lo que analiza el estado del arte.
- Cita en texto: (Gonçalves et al., 2021)
- Uso sugerido: MT 4.3

### [alqoran2025] Al-Qora'n y Al-Said Ahmad (2025)
- Referencia APA 7: Al-Qora’n, L. F., & Al-Said Ahmad, A. (2025). Modular monolith architecture in cloud environments: A systematic literature review. *Future Internet, 17*(11), Article 496. https://doi.org/10.3390/fi17110496
- Tipo: artículo (revisión sistemática de literatura)
- Verificación: Crossref (api.crossref.org/works/10.3390/fi17110496), consultado 2026-10-06: coinciden los dos autores, título, revista, volumen 17(11), número de artículo 496 y año 2025 (en línea 2025-10-29). Resumen leído en Crossref y en OpenAlex (idénticos).
- Hechos verificados (según el resumen):
  - Presentan lo que describen como la primera revisión sistemática sobre arquitectura monolítica modular en entornos de nube: guía de Kitchenham, seis bibliotecas digitales, estudios de 2020 a mayo de 2025, 369 registros y 15 estudios primarios incluidos.
  - Describen la arquitectura monolítica modular como un híbrido entre el monolito tradicional y los microservicios, que combina simplicidad operativa con modularidad y mantenibilidad; encuentran terminología inconsistente en la literatura.
  - Los factores de adopción identificados son el despliegue simplificado, la mantenibilidad y la menor sobrecarga de orquestación; reportan evidencia comparativa de que conviene cuando los microservicios introducen complejidad o costos excesivos.
  - Vacíos señalados por los autores: ausencia de una definición consensuada, evidencia empírica de rendimiento (benchmarking) limitada y soporte de herramientas insuficiente.
- Cita en texto: (Al-Qora'n & Al-Said Ahmad, 2025)
- Uso sugerido: MT 4.3 | Metodología

### [bjorndal2021] Bjørndal et al. (2021)
- Referencia APA 7: Bjørndal, N., Mazzara, M., Bucchiarone, A., Dragoni, N., & Dustdar, S. (2021). Migration from monolith to microservices: Benchmarking a case study. *The Journal of Object Technology, 20*(2), 3:1. https://doi.org/10.5381/jot.2021.20.2.a3
- Tipo: artículo (estudio de caso con experimentos)
- Verificación: Crossref (api.crossref.org/works/10.5381/jot.2021.20.2.a3) y OpenAlex, consultados 2026-10-06: coinciden los cinco autores, título (Crossref añade un punto final), revista, volumen 20(2), identificador de página "3:1" y año 2021. Resumen leído vía OpenAlex.
- Hechos verificados (según el resumen):
  - Señalan que las ventajas de migrar de monolito a microservicios no han sido investigadas extensamente y proponen una metodología e indicadores de rendimiento para evaluar si la migración es beneficiosa.
  - Obtienen las métricas mediante una revisión sistemática validada con una encuesta a profesionales de la industria: latencia, rendimiento (throughput), escalabilidad, CPU, memoria y utilización de red.
  - Aplican esas métricas en dos experimentos con versiones monolítica y de microservicios del mismo sistema. El resumen no reporta cuál arquitectura resultó mejor, así que no atribuirle un resultado comparativo.
- Cita en texto: (Bjørndal et al., 2021)
- Uso sugerido: MT 4.3 | Metodología (indicadores para la estrategia de validación de Trabajo de Grado)

---

## c) Comunicación en tiempo real: WebSockets frente a polling y SSE

### [fette2011] Fette y Melnikov (2011)
- Referencia APA 7: Fette, I., & Melnikov, A. (2011). *The WebSocket protocol* (RFC 6455). Internet Engineering Task Force. https://doi.org/10.17487/RFC6455
- Tipo: norma (RFC, Standards Track del IETF; fundacional)
- Verificación: Crossref (api.crossref.org/works/10.17487/RFC6455) y texto oficial en rfc-editor.org/rfc/rfc6455.txt, consultados 2026-10-06: coinciden autores (I. Fette, A. Melnikov), título, número de RFC, categoría Standards Track y fecha diciembre de 2011. Se leyó el resumen y la sección 1.1 (no normativa). El DOI resuelve en doi.org.
- Hechos verificados (texto completo, resumen y sección 1.1):
  - El protocolo WebSocket habilita la comunicación bidireccional entre un cliente que ejecuta código no confiable en un entorno controlado y un servidor que aceptó esa comunicación; usa el modelo de seguridad basado en origen de los navegadores y consiste en un apretón de manos (handshake) de apertura seguido de un entramado básico de mensajes sobre TCP.
  - La sección 1.1 explica que, históricamente, las aplicaciones web con comunicación bidireccional abusaban de HTTP haciendo polling al servidor mientras enviaban las notificaciones hacia arriba como llamadas HTTP independientes, con tres problemas: múltiples conexiones TCP por cliente, sobrecarga de cabeceras HTTP en cada mensaje y la necesidad de mapear conexiones de salida y de entrada.
  - Propone una única conexión TCP para el tráfico en ambos sentidos como alternativa al polling HTTP, útil para juegos, multiusuario con edición simultánea e interfaces que exponen servicios del servidor en tiempo real.
  - Justificación como fundacional: es el estándar vigente del protocolo (documentación oficial del IETF); no existe una versión posterior que lo sustituya.
- Cita en texto: (Fette & Melnikov, 2011)
- Uso sugerido: MT 4.4 | Metodología (justificación de Django Channels)

### [gracia2024] Gracia Orejuela et al. (2024)
- Referencia APA 7: Gracia Orejuela, K. J., Gorozabel Bazurto, M. B., & Chango Sailema, W. G. (2024). Long polling, websockets y server-sent events: Comunicación para el envío de datos en tiempo real. *Mikarimin. Revista Científica Multidisciplinaria, 10*(3), 101–120. https://doi.org/10.61154/mrcm.v10i3.3272
- Tipo: artículo (estudio de caso experimental, en español)
- Verificación: Crossref (api.crossref.org/works/10.61154/mrcm.v10i3.3272) y OpenAlex, consultados 2026-10-06: coinciden los tres autores, título, revista (Universidad Regional Autónoma de los Andes, Ecuador), volumen 10(3), páginas 101-120 y año 2024. Se descargó el PDF de acceso abierto (revista.uniandes.edu.ec) y se extrajo su texto localmente; se leyeron resumen, metodología, resultados y conclusiones. El DOI redirige correctamente (HTTP 302).
- Hechos verificados (texto completo):
  - Estudio realizado en el departamento de TI de la Pontificia Universidad Católica del Ecuador (sede Esmeraldas) para evaluar Long polling, WebSockets y Server-Sent Events con un chat en línea; el resumen concluye que WebSockets es el protocolo más adecuado para una arquitectura de backend escalable porque ofrece una conexión bidireccional entre cliente y servidor.
  - En la sección de conclusiones se reportan pruebas de 2.000 solicitudes por protocolo: WebSocket sin fallos, con tiempo medio de respuesta de unos 2,78 s y 284 transacciones por segundo; Long polling con 138 fallos (6,90 %); Server-Sent Events sin fallos, con tiempo medio de 1.889,92 ms y 399,68 transacciones por segundo.
  - Los autores declaran como limitación que las pruebas se hicieron en un entorno controlado y sin factores externos propios de producción (las tablas muestran una URL local, `localhost`).
  - Uso crítico (observación del investigador): en esas pruebas SSE obtuvo menor tiempo medio y mayor rendimiento que WebSocket, de modo que la conclusión del resumen a favor de WebSocket descansa sobre todo en su bidireccionalidad y no en las cifras. Citar el estudio con cautela y como respaldo de que Long polling mostró la mayor tasa de fallos; la elección de WebSocket para el chat y el seguimiento de CMEDriver se justifica mejor por la necesidad de comunicación bidireccional (RFC 6455).
- Cita en texto: (Gracia Orejuela et al., 2024)
- Uso sugerido: MT 4.4

---

## d) Aplicaciones híbridas, PWA y marcos multiplataforma (Ionic y Capacitor)

### [capacitor-docs] Capacitor (s. f.)
- Referencia APA 7: Capacitor. (s. f.). *Capacitor: Cross-platform native runtime for web apps*. Capacitor Documentation. Recuperado el 6 de octubre de 2026, de https://capacitorjs.com/docs
- Tipo: documentación técnica
- Verificación: WebFetch de https://capacitorjs.com/docs, 2026-10-06 (título de la página: "Capacitor - Cross-platform Native Runtime for Web Apps | Capacitor Documentation"); el pie de la página indica que el sitio pertenece a "An OutSystems Company", por lo que se usa el nombre del proyecto como autor. El contenido llegó como resumen automático de la herramienta.
- Hechos verificados (según el resumen de la herramienta sobre la página):
  - La documentación define a Capacitor como un entorno de ejecución nativo multiplataforma para construir aplicaciones móviles con herramientas web modernas que se ejecutan de forma nativa en iOS, Android y más; sus destinos son iOS, Android y la web (PWA).
  - Lo presenta como sucesor de Cordova y PhoneGap (con guía de migración) y señala que puede integrarse con Ionic Framework pero funciona de forma independiente.
  - Trata los proyectos nativos como artefactos de código fuente y no como salida de compilación, y ofrece una API de plugins (Swift en iOS, Java en Android y JavaScript en la web) para añadir funcionalidad nativa cuando se necesita.
- Cita en texto: (Capacitor, s. f.)
- Uso sugerido: MT 4.4 | Metodología

### [oliveira2023] Oliveira et al. (2023)
- Referencia APA 7: Oliveira, W., Moraes, B., Castor, F., & Fernandes, J. P. (2023). Analyzing the resource usage overhead of mobile app development frameworks. En *Proceedings of the 27th International Conference on Evaluation and Assessment in Software Engineering* (pp. 152–161). ACM. https://doi.org/10.1145/3593434.3593487
- Tipo: ponencia (estudio empírico)
- Verificación: Crossref (api.crossref.org/works/10.1145/3593434.3593487) y OpenAlex, consultados 2026-10-06: coinciden los cuatro autores, título, congreso EASE 2023, páginas 152-161 y año 2023 (junio). Resumen completo leído vía OpenAlex. El DOI da HTTP 403 al acceso automático (bloqueo del editor), pero los metadatos de Crossref y OpenAlex coinciden.
- Hechos verificados (según el resumen):
  - Analizan consumo de energía, tiempo de ejecución y uso de memoria de benchmarks y aplicaciones Android hechas con Flutter, React Native e Ionic, frente a variantes nativas equivalentes en Java; describen a Ionic como un enfoque basado en aplicaciones web que no depende de detalles de cada plataforma.
  - Usaron diez benchmarks intensivos en CPU y dos aplicaciones. Concluyen que los marcos multiplataforma e híbridos pueden ser competitivos en aplicaciones intensivas en CPU: en cinco de los diez benchmarks, al menos una versión basada en marco superó a la nativa en energía y tiempo (reducciones de hasta 81 % y 83 %), y en otros tres los resultados fueron similares.
  - En general Flutter impuso la menor sobrecarga y React Native la mayor; sin embargo, en una app que anima continuamente varias imágenes, la versión de React Native usó menos CPU y energía. Los autores destacan la importancia de analizar el comportamiento esperado de la aplicación antes de elegir un marco.
  - Uso crítico: el resumen no reporta resultados específicos de Ionic y los benchmarks son intensivos en CPU, no un caso típico de una app de logística con mapas y red. Es un contrapunto al supuesto de que lo híbrido siempre rinde peor, no una validación de Ionic para CMEDriver.
- Cita en texto: (Oliveira et al., 2023)
- Uso sugerido: MT 4.4 | Metodología

### [kaczmarczyk2022] Kaczmarczyk et al. (2022)
- Referencia APA 7: Kaczmarczyk, A., Zając, P., & Zabierowski, W. (2022). Performance comparison of native and hybrid Android mobile applications based on sensor data-driven applications based on Bluetooth Low Energy (BLE) and Wi-Fi communication architecture. *Energies, 15*(13), Article 4574. https://doi.org/10.3390/en15134574
- Tipo: artículo (comparación experimental)
- Verificación: Crossref (api.crossref.org/works/10.3390/en15134574), consultado 2026-10-06: coinciden los tres autores, título, revista, volumen 15(13), número de artículo 4574 y año 2022 (en línea 2022-06-23). Solo se pudo leer el resumen (Crossref); el texto completo en mdpi.com respondió HTTP 403 a WebFetch y curl.
- Hechos verificados (según el resumen):
  - El objetivo es comparar aplicaciones móviles nativas e híbridas para Android considerando las necesidades de sistemas con comunicación BLE y Wi-Fi, a partir de aplicaciones implementadas en Java 8 y en el framework Ionic.
  - Comparan la eficiencia del procesamiento de datos en ambas tecnologías para indicar dependencias que ayuden a elegir tecnología en proyectos basados en BLE, Wi-Fi y redes de sensores.
  - Limitación de lo leído: el resumen no reporta resultados, por lo que no se puede atribuir a los autores ninguna conclusión sobre cuál tecnología fue más eficiente. Usarla solo para sostener que existen comparaciones directas entre Ionic y Java nativo; si se necesita el resultado, el estudiante debe leer el texto completo.
- Cita en texto: (Kaczmarczyk et al., 2022)
- Uso sugerido: MT 4.4

### [zou2024] Zou y Darus (2024)
- Referencia APA 7: Zou, D., & Darus, M. Y. (2024). A comparative analysis of cross-platform mobile development frameworks. En *2024 IEEE 6th Symposium on Computers & Informatics (ISCI)* (pp. 84–90). IEEE. https://doi.org/10.1109/ISCI62787.2024.10667693
- Tipo: ponencia (análisis comparativo descriptivo)
- Verificación: Crossref (api.crossref.org/works/10.1109/isci62787.2024.10667693) y OpenAlex, consultados 2026-10-06: coinciden los dos autores, título, congreso ISCI 2024, páginas 84-90 y año 2024 (agosto). Resumen leído vía OpenAlex.
- Hechos verificados (según el resumen):
  - Describen las categorías de enfoques de desarrollo móvil (aplicaciones nativas, web móviles, basadas en widgets, con puente de JavaScript, entre otras) y comparan cinco marcos populares: Corona SDK (Solar2D), Ionic, Flutter, React Native y Xamarin.
  - La evaluación cubre ventajas y desventajas en lenguaje de desarrollo, tecnología base, rendimiento, apoyo de la comunidad, capacidades multiplataforma y curva de aprendizaje.
  - Los autores reconocen que se trata de un campo cambiante y piden estudios futuros con casos de aplicación más diversos y muestras mayores, lo que limita el alcance de sus conclusiones.
- Cita en texto: (Zou & Darus, 2024)
- Uso sugerido: MT 4.4

---

## e) Chatbots y modelos de lenguaje en atención al cliente; invocación de herramientas; riesgos

### [nicolescu2022] Nicolescu y Tudorache (2022)
- Referencia APA 7: Nicolescu, L., & Tudorache, M. T. (2022). Human-computer interaction in customer service: The experience with AI chatbots—A systematic literature review. *Electronics, 11*(10), Article 1579. https://doi.org/10.3390/electronics11101579
- Tipo: artículo (revisión sistemática)
- Verificación: Crossref (api.crossref.org/works/10.3390/electronics11101579) y OpenAlex, consultados 2026-10-06: coinciden los dos autores, título, revista, volumen 11(10), número de artículo 1579 y año 2022 (en línea 2022-05-15). Resumen completo leído en Crossref.
- Hechos verificados (según el resumen):
  - Revisión sistemática de 40 publicaciones con estudios empíricos sobre la experiencia del cliente con chatbots de servicio al cliente.
  - Los factores que influyen se agrupan en tres categorías: relacionados con el chatbot (funcionales, de sistema y antropomórficos), con el cliente y con el contexto; el conjunto de factores produce percepciones y actitudes tanto positivas como negativas.
  - Según los estudios empíricos revisados, los factores más influyentes son la relevancia de la respuesta y la resolución del problema, que suelen asociarse con satisfacción, continuidad de uso del chatbot, compras y recomendaciones.
- Cita en texto: (Nicolescu & Tudorache, 2022)
- Uso sugerido: Intro | MT 4.5

### [brynjolfsson2025] Brynjolfsson et al. (2025)
- Referencia APA 7: Brynjolfsson, E., Li, D., & Raymond, L. (2025). Generative AI at work. *The Quarterly Journal of Economics, 140*(2), 889–942. https://doi.org/10.1093/qje/qjae044
- Tipo: artículo (estudio empírico)
- Verificación: Crossref (api.crossref.org/works/10.1093/qje/qjae044), consultado 2026-10-06: coinciden los tres autores, título, revista, volumen 140(2), páginas 889-942 y año 2025 (en línea 2025-02-04; número impreso de abril de 2025). Resumen leído en Crossref y OpenAlex (idénticos). Existe una versión previa como documento de trabajo del NBER (DOI 10.3386/w31161); se cita la versión publicada.
- Hechos verificados (según el resumen):
  - Estudian la introducción escalonada de un asistente conversacional basado en IA generativa con datos de 5.172 agentes de soporte al cliente.
  - El acceso a la asistencia aumenta en promedio un 15 % la productividad, medida en problemas resueltos por hora, con gran heterogeneidad: los agentes menos experimentados mejoran en velocidad y calidad, mientras que los más experimentados obtienen ganancias pequeñas en velocidad y pequeñas caídas en calidad.
  - También reportan que los clientes son más corteses y menos propensos a pedir hablar con un gerente.
  - Uso crítico: el asistente apoya a agentes humanos; no es un chatbot autónomo de cara al cliente. No presentarlo como evidencia de que un chatbot reemplaza la atención humana ni de resultados de CMEDriver.
- Cita en texto: (Brynjolfsson et al., 2025)
- Uso sugerido: Intro | MT 4.5

### [qu2025] Qu et al. (2025)
- Referencia APA 7: Qu, C., Dai, S., Wei, X., Cai, H., Wang, S., Yin, D., Xu, J., & Wen, J.-R. (2025). Tool learning with large language models: A survey. *Frontiers of Computer Science, 19*(8), Article 198343. https://doi.org/10.1007/s11704-024-40678-2
- Tipo: artículo (revisión)
- Verificación: Crossref (api.crossref.org/works/10.1007/s11704-024-40678-2), consultado 2026-10-06: coinciden los ocho autores, título, revista, volumen 19(8), número de artículo 198343 y año 2025 (en línea 2025-01-13). Crossref no trae resumen; se leyó en la página del preprint (arxiv.org/abs/2405.17935, WebFetch), que indica la aceptación en *Frontiers of Computer Science* con ese mismo DOI.
- Hechos verificados (según el resumen del preprint):
  - Estudia cómo se pueden potenciar los LLM integrando herramientas para resolver problemas complejos, organizando la revisión en torno a dos preguntas: por qué el aprendizaje de herramientas ofrece ventajas (seis dimensiones) y cómo se implementa.
  - Sistematiza la implementación en cuatro etapas del flujo de trabajo: planificación de la tarea, selección de herramientas, llamada a herramientas y generación de la respuesta.
  - Resume benchmarks y métodos de evaluación para las distintas etapas y discute desafíos actuales y direcciones futuras.
- Cita en texto: (Qu et al., 2025)
- Uso sugerido: MT 4.5 | Metodología (justificación de la arquitectura de tool-calling)

### [greshake2023] Greshake et al. (2023)
- Referencia APA 7: Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. En *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security* (pp. 79–90). ACM. https://doi.org/10.1145/3605764.3623985
- Tipo: ponencia (estudio de seguridad)
- Verificación: Crossref (api.crossref.org/works/10.1145/3605764.3623985) y OpenAlex, consultados 2026-10-06: coinciden los seis autores, título, congreso AISec 2023 (16th ACM Workshop on Artificial Intelligence and Security), páginas 79-90 y año 2023 (noviembre). Resumen leído vía OpenAlex.
- Hechos verificados (según el resumen):
  - Sostienen que las aplicaciones integradas con LLM desdibujan la frontera entre datos e instrucciones y abren nuevos vectores de ataque mediante inyección indirecta de instrucciones: se inyectan prompts en datos que la aplicación recupera en el momento de la inferencia.
  - Derivan una taxonomía desde la perspectiva de seguridad informática que incluye robo de datos, gusanos y contaminación del ecosistema de información, y demuestran la viabilidad de los ataques contra sistemas reales (como Bing Chat y motores de completado de código) y aplicaciones sintéticas con GPT-4.
  - Muestran que procesar prompts recuperados puede equivaler a ejecución arbitraria de código, manipular la funcionalidad de la aplicación y controlar si se llama a otras APIs y cómo; indican que, al momento del estudio, faltaban mitigaciones efectivas.
- Cita en texto: (Greshake et al., 2023)
- Uso sugerido: MT 4.5 | MT 4.7

### [zhan2024] Zhan et al. (2024)
- Referencia APA 7: Zhan, Q., Liang, Z., Ying, Z., & Kang, D. (2024). InjecAgent: Benchmarking indirect prompt injections in tool-integrated large language model agents. En *Findings of the Association for Computational Linguistics: ACL 2024* (pp. 10471–10506). Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.findings-acl.624
- Tipo: ponencia (benchmark)
- Verificación: Crossref (api.crossref.org/works/10.18653/v1/2024.findings-acl.624), ACL Anthology (aclanthology.org/2024.findings-acl.624/) y arXiv (arxiv.org/abs/2403.02691), consultados 2026-10-06: coinciden los cuatro autores, título, actas (Findings of ACL 2024), páginas 10471-10506 y año 2024. Resumen leído en ACL Anthology y arXiv (con la herramienta WebFetch).
- Hechos verificados (según el resumen):
  - Los agentes basados en LLM que acceden a herramientas e interactúan con contenido externo (por ejemplo correos o sitios web) quedan expuestos a inyecciones indirectas de instrucciones que buscan manipularlos para ejecutar acciones dañinas contra los usuarios.
  - El benchmark InjecAgent reúne 1.054 casos de prueba con 17 herramientas de usuario y 62 herramientas de atacante, con dos tipos de intención del ataque: daño directo al usuario y robo de datos privados.
  - Evaluaron 30 agentes: según el resumen, un agente GPT-4 con prompt ReAct resultó vulnerable en un 24 % de los casos, y las tasas de éxito aumentaron cuando el atacante reforzó la instrucción con un "prompt de hackeo".
- Cita en texto: (Zhan et al., 2024)
- Uso sugerido: MT 4.5 | MT 4.7

### [huang2025] Huang et al. (2025)
- Referencia APA 7: Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., Chen, Q., Peng, W., Feng, X., Qin, B., & Liu, T. (2025). A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions. *ACM Transactions on Information Systems, 43*(2), 1–55. https://doi.org/10.1145/3703155
- Tipo: artículo (revisión)
- Verificación: Crossref (api.crossref.org/works/10.1145/3703155), consultado 2026-10-06: coinciden los once autores, título, revista, volumen 43(2), páginas 1-55 y año 2025 (en línea 2025-01-24; impreso 2025-03-31). Resumen leído en Crossref y en OpenAlex. OpenAlex fecha la versión anticipada en 2024; se usa 2025, año del volumen.
- Hechos verificados (según el resumen):
  - Los LLM son propensos a la alucinación, es decir, a generar contenido plausible pero no factual, lo que genera preocupación por su fiabilidad en sistemas reales de recuperación de información.
  - La revisión propone una taxonomía de la alucinación en la era de los LLM, analiza los factores que la causan, y presenta métodos y benchmarks de detección y metodologías de mitigación.
  - Discuten las limitaciones actuales de los LLM aumentados con recuperación (retrieval-augmented) para combatir las alucinaciones.
- Cita en texto: (Huang et al., 2025)
- Uso sugerido: MT 4.5

### [owasp-llm2025] OWASP GenAI Security Project (2025)
- Referencia APA 7: OWASP GenAI Security Project. (2025). *OWASP top 10 for LLM applications 2025*. OWASP Foundation. https://genai.owasp.org/llm-top-10/
- Tipo: documentación técnica (guía abierta de seguridad)
- Verificación: sitio oficial genai.owasp.org, consultado 2026-10-06 con curl y WebFetch: la página "llm-top-10" lista los diez riesgos con el sufijo 2025 y atribuye el proyecto al OWASP GenAI Security Project; se leyeron además las páginas de LLM01:2025 (llm01-prompt-injection) y LLM06:2025 (llm062025-excessive-agency). La página no muestra una fecha de publicación; se usa 2025 por la edición. En el texto, la primera cita debe llevar el nombre completo con sigla: (OWASP GenAI Security Project [OWASP], 2025), y luego (OWASP, 2025).
- Hechos verificados (texto de las páginas oficiales):
  - La lista 2025 incluye: LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Supply Chain, LLM04 Data and Model Poisoning, LLM05 Improper Output Handling, LLM06 Excessive Agency, LLM07 System Prompt Leakage, LLM08 Vector and Embedding Weaknesses, LLM09 Misinformation y LLM10 Unbounded Consumption.
  - LLM01: ocurre cuando los prompts alteran el comportamiento o la salida del LLM de formas no previstas, ya sea por inyección directa o indirecta (contenido externo); entre las mitigaciones listadas figuran restringir el comportamiento del modelo, validar formatos de salida, filtrar entradas y salidas, aplicar mínimo privilegio, exigir aprobación humana para acciones de alto riesgo y segregar el contenido externo.
  - LLM06: un sistema basado en LLM suele recibir cierta capacidad de acción (llamar funciones o interactuar con otros sistemas mediante extensiones); la vulnerabilidad aparece cuando salidas inesperadas o manipuladas causan acciones dañinas. Las causas son funcionalidad, permisos y autonomía excesivos; entre las prevenciones se cuentan minimizar las extensiones, aplicar mínimo privilegio, ejecutar en el contexto del usuario, exigir aprobación humana y validar la autorización en los sistemas posteriores en lugar de confiar en el LLM.
- Cita en texto: (OWASP GenAI Security Project [OWASP], 2025) la primera vez; (OWASP, 2025) después.
- Uso sugerido: MT 4.5 | MT 4.7 | Metodología (principio de que la autorización debe aplicarse en el backend y no en el modelo)

---

## f) Optimización de rutas, vecino más cercano, geocodificación y calidad de OpenStreetMap

### [dantzig1959] Dantzig y Ramser (1959)
- Referencia APA 7: Dantzig, G. B., & Ramser, J. H. (1959). The truck dispatching problem. *Management Science, 6*(1), 80–91. https://doi.org/10.1287/mnsc.6.1.80
- Tipo: artículo (fundacional)
- Verificación: Crossref (api.crossref.org/works/10.1287/mnsc.6.1.80), consultado 2026-10-06: coinciden los dos autores, título, revista, volumen 6(1), páginas 80-91 y año 1959 (octubre). Resumen leído en Crossref y OpenAlex (idénticos). El DOI da HTTP 403 al acceso automático (bloqueo del editor).
- Hechos verificados (según el resumen):
  - Trata el ruteo óptimo de una flota de camiones de reparto de gasolina entre una terminal y muchas estaciones de servicio, con demandas especificadas y rutas más cortas conocidas entre puntos.
  - Busca asignar estaciones a camiones de modo que se satisfagan las demandas y se minimice el recorrido total de la flota.
  - Ofrece un procedimiento basado en programación lineal para obtener una solución casi óptima, y los autores indican que aún no se habían hecho aplicaciones prácticas del método.
  - Justificación como fundacional: es el trabajo de origen del problema de ruteo de vehículos; se cita una sola vez para situar el origen del problema.
- Cita en texto: (Dantzig & Ramser, 1959)
- Uso sugerido: MT 4.6

### [jazemi2023] Jazemi et al. (2023)
- Referencia APA 7: Jazemi, R., Alidadiani, E., Ahn, K., & Jang, J. (2023). A review of literature on vehicle routing problems of last-mile delivery in urban areas. *Applied Sciences, 13*(24), Article 13015. https://doi.org/10.3390/app132413015
- Tipo: artículo (revisión de literatura)
- Verificación: Crossref (api.crossref.org/works/10.3390/app132413015) y OpenAlex, consultados 2026-10-06: coinciden los cuatro autores, título, revista, volumen 13(24), número de artículo 13015 y año 2023 (en línea 2023-12-06). Resumen leído vía OpenAlex.
- Hechos verificados (según el resumen):
  - Plantean que la entrega de paquetes a zonas residenciales urbanas aumenta el reto por el volumen, los horarios ajustados y las condiciones cambiantes, y revisan la literatura reciente sobre ruteo de vehículos para última milla.
  - Identifican cuatro categorías (crowdshipping, casilleros de paquetes, entrega con "sidekicks" y entrega a puntos opcionales) y discuten la naturaleza de los problemas en cinco aspectos: capacidad de la flota, ventanas de tiempo, opción de flota, dinamismo de los datos de entrada y parámetros estocásticos.
  - Señalan los logros y limitaciones de la investigación y proponen una agenda futura.
  - Uso crítico: el resumen no menciona el vecino más cercano ni heurísticas simples; sirve para situar el VRP de última milla y sus dimensiones (ventanas de tiempo, dinamismo) que la heurística del prototipo no modela.
- Cita en texto: (Jazemi et al., 2023)
- Uso sugerido: Intro | MT 4.6

### [hougardy2015] Hougardy y Wilde (2015)
- Referencia APA 7: Hougardy, S., & Wilde, M. (2015). On the nearest neighbor rule for the metric traveling salesman problem. *Discrete Applied Mathematics, 195*, 101–103. https://doi.org/10.1016/j.dam.2014.03.012
- Tipo: artículo (resultado teórico)
- Verificación: Crossref (api.crossref.org/works/10.1016/j.dam.2014.03.012), consultado 2026-10-06: coinciden los dos autores, título, revista, volumen 195, páginas 101-103 y año (número de noviembre de 2015). El resumen se leyó en arXiv (arxiv.org/abs/1401.2071, WebFetch) y en la API de Semantic Scholar, que coinciden entre sí; Crossref y OpenAlex no lo traen.
- Hechos verificados (según el resumen):
  - Presentan una familia simple de instancias del problema del agente viajero con n ciudades en las que la regla del vecino más cercano puede producir un recorrido Θ(log n) veces más largo que el óptimo.
  - La familia sirve a la vez para las variantes gráfica, euclidiana y rectilínea; mejora la mejor cota inferior conocida en el caso euclidiano y prueba por primera vez una cota inferior en el caso rectilíneo.
  - Uso crítico: es un resultado de peor caso; muestra que la heurística del vecino más cercano no ofrece garantía de calidad. Anterior a 2021, justificado por ser el análisis teórico de la heurística sin equivalente reciente hallado.
- Cita en texto: (Hougardy & Wilde, 2015)
- Uso sugerido: MT 4.6 | Metodología (limitación declarada de la heurística)

### [perez2024] Pérez y Aybar (2024)
- Referencia APA 7: Pérez, V., & Aybar, C. (2024). Challenges in geocoding: An analysis of R packages and web scraping approaches. *ISPRS International Journal of Geo-Information, 13*(6), Article 170. https://doi.org/10.3390/ijgi13060170
- Tipo: artículo (estudio comparativo)
- Verificación: Crossref (api.crossref.org/works/10.3390/ijgi13060170) y OpenAlex, consultados 2026-10-06: coinciden los dos autores, título, revista, volumen 13(6), número de artículo 170 y año 2024 (en línea 2024-05-23). Resumen leído vía OpenAlex.
- Hechos verificados (según el resumen):
  - Evalúan 15 métodos o paquetes de R y su integración con APIs externas para convertir direcciones postales en coordenadas, y miden la precisión por cercanía a las coordenadas originales del callejero de Madrid con una muestra de 15.000 direcciones.
  - Encuentran una variabilidad importante: MapQuest fue el más rápido, ArcGIS el más preciso y Nominatim el que más valores faltantes dejó.
  - Proponen una alternativa basada en web scraping que reduce errores y valores faltantes, pero advierten posibles problemas legales.
  - Uso crítico: la evidencia proviene de una sola ciudad europea (Madrid) y de paquetes de R; no mide direcciones colombianas. Sirve para sostener que Nominatim puede dejar direcciones sin resolver y que conviene validar la geocodificación.
- Cita en texto: (Pérez & Aybar, 2024)
- Uso sugerido: MT 4.6 | Metodología

### [kilic2023] Kılıç et al. (2023)
- Referencia APA 7: Kılıç, B., Hacar, M., & Gülgen, F. (2023). Effects of reverse geocoding on OpenStreetMap tag quality assessment. *Transactions in GIS, 27*(5), 1599–1613. https://doi.org/10.1111/tgis.13089
- Tipo: artículo (estudio empírico)
- Verificación: Crossref (api.crossref.org/works/10.1111/tgis.13089) y OpenAlex, consultados 2026-10-06: coinciden los tres autores, título, revista, volumen 27(5), páginas 1599-1613 y año 2023 (en línea 2023-07-02). Crossref escribe "Kilic" y las iniciales "Müslüm" para Hacar; OpenAlex escribe "Kılıç" y "M A Hacar" (se usa la grafía con diacríticos y la inicial de Crossref). Resumen leído vía OpenAlex.
- Hechos verificados (según el resumen):
  - Señalan que OpenStreetMap ofrece un conjunto de datos geográficos muy grande, con información geométrica y semántica (etiquetas) aportada de forma voluntaria, y que se reconoce que la cantidad de información de etiquetas es grande pero su calidad suele ser deficiente.
  - Evalúan la validez de las etiquetas de objetos en áreas metropolitanas usando puntos de interés municipales como referencia y geocodificación inversa.
  - Las etiquetas coincidieron con los puntos de interés con una exactitud del 88 %, y concluyen que en entornos metropolitanos donde los centros de interés están muy cercanos la exactitud de las etiquetas y de las direcciones tiende a disminuir.
  - Uso crítico: no se identifica el país del caso en el resumen; sirve como evidencia general de heterogeneidad en la calidad de los datos de OpenStreetMap, no de su calidad en Colombia.
- Cita en texto: (Kılıç et al., 2023)
- Uso sugerido: MT 4.6

### [osmf-nominatim] OpenStreetMap Foundation Operations Working Group (s. f.)
- Referencia APA 7: OpenStreetMap Foundation Operations Working Group. (s. f.). *Nominatim usage policy (aka geocoding policy)*. Recuperado el 6 de octubre de 2026, de https://operations.osmfoundation.org/policies/nominatim/
- Tipo: documentación técnica (política oficial)
- Verificación: WebFetch de https://operations.osmfoundation.org/policies/nominatim/, 2026-10-06 (título: "Nominatim Usage Policy (aka Geocoding Policy)"; publicada por el OSMF Operations Working Group; la página no muestra fecha). El contenido llegó como resumen automático de la herramienta.
- Hechos verificados (según el resumen de la herramienta sobre la página):
  - La política fija para el servicio público nominatim.openstreetmap.org un máximo absoluto de una solicitud por segundo, exige cabeceras HTTP Referer o User-Agent válidas (no bastan las genéricas de las bibliotecas) y exige almacenar en caché los resultados.
  - Desaconseja la geocodificación masiva y la restringe a tareas pequeñas y puntuales con solicitudes de un solo hilo a un máximo de cuatro por minuto.
  - Los datos requieren atribución bajo la licencia ODbL; para necesidades mayores recomienda proveedores comerciales o alojar una instancia propia de Nominatim, y advierte que la política puede cambiar sin aviso.
- Cita en texto: (OpenStreetMap Foundation Operations Working Group, s. f.) la primera vez y luego una sigla definida por el redactor, por ejemplo [OSMF OWG].
- Uso sugerido: MT 4.6 | Metodología (restricciones de uso del geocodificador y por qué el prototipo debe cachear resultados)

---

## g) Seguridad: JWT, RBAC, HMAC y seguridad de APIs

### [jones2015] Jones et al. (2015)
- Referencia APA 7: Jones, M., Bradley, J., & Sakimura, N. (2015). *JSON Web Token (JWT)* (RFC 7519). Internet Engineering Task Force. https://doi.org/10.17487/RFC7519
- Tipo: norma (RFC, Standards Track del IETF; fundacional)
- Verificación: Crossref (api.crossref.org/works/10.17487/RFC7519) y texto oficial en rfc-editor.org/rfc/rfc7519.txt, consultados 2026-10-06: coinciden autores (M. Jones, J. Bradley, N. Sakimura), título, número de RFC, categoría Standards Track y fecha de mayo de 2015. Se leyó el resumen y las secciones 4.1.4, 6 y 8.
- Hechos verificados (texto completo, secciones indicadas):
  - JWT es un medio compacto y apto para URL de representar claims entre dos partes; los claims se codifican como objeto JSON que sirve de carga de una estructura JWS o de texto plano de una JWE, de modo que pueden firmarse o protegerse en integridad con un código de autenticación de mensaje (MAC) o cifrarse.
  - El claim `exp` (tiempo de expiración) identifica el momento desde el cual el JWT no debe aceptarse para su procesamiento (sección 4.1.4).
  - La sección 6 define los JWT sin protección (algoritmo `none`, firma vacía) y la sección 8 establece que, entre los algoritmos de firma y MAC, solo HMAC SHA-256 (HS256) y `none` son de implementación obligatoria para las implementaciones conformes.
  - Justificación como fundacional: es el estándar que define el formato; la literatura posterior (Yang et al., 2026) lo asume como base.
- Cita en texto: (Jones et al., 2015)
- Uso sugerido: MT 4.7 | Metodología

### [yang2026] Yang et al. (2026)
- Referencia APA 7: Yang, J., Wang, E., Chen, J., Wang, Q., Zhang, Y., Duan, H., Xie, W., & Wang, B. (2026). Token time bomb: Evaluating JWT implementations for vulnerability discovery. En *Proceedings 2026 Network and Distributed System Security Symposium (NDSS)*. Internet Society. https://doi.org/10.14722/ndss.2026.240697
- Tipo: ponencia (estudio de seguridad)
- Verificación: Crossref (api.crossref.org/works/10.14722/ndss.2026.240697), OpenAlex y página oficial de NDSS (ndss-symposium.org/ndss-paper/token-time-bomb-evaluating-jwt-implementations-for-vulnerability-discovery/), consultados 2026-10-06: coinciden los ocho autores, título, congreso (NDSS 2026) y año. El DOI resuelve (HTTP 200). Resumen leído vía OpenAlex.
- Hechos verificados (según el resumen):
  - Reportan que, pese a la amplia adopción de JWT, sus implementaciones han introducido vulnerabilidades como la evasión de la verificación de firma, la suplantación de tokens y la denegación de servicio, y que faltaba un estudio sistemático de las implementaciones.
  - Proponen JWTeemo, una metodología de pruebas, y la aplicaron a 43 implementaciones de JWT en 10 lenguajes: descubrieron 31 vulnerabilidades desconocidas, 20 con número CVE asignado, entre ellas una evasión de autenticación en Kubernetes y una denegación de servicio contra Apache James.
  - Clasificaron las vulnerabilidades en cinco tipos y propusieron estrategias de mitigación; informan que discutieron sus hallazgos con el IETF, que los reconoció.
- Cita en texto: (Yang et al., 2026)
- Uso sugerido: MT 4.7

### [shatnawi2024] Shatnawi et al. (2024)
- Referencia APA 7: Shatnawi, A. S., Al-Duwairi, B., & Samarneh, A. A. (2024). Comprehensive empirical study of Python JWT libraries. *Procedia Computer Science, 238*, 827–832. https://doi.org/10.1016/j.procs.2024.06.099
- Tipo: artículo (estudio empírico)
- Verificación: Crossref (api.crossref.org/works/10.1016/j.procs.2024.06.099) y OpenAlex, consultados 2026-10-06: coinciden los tres autores, título, publicación (Procedia Computer Science), volumen 238, páginas 827-832 y año 2024. El DOI resuelve (HTTP 200). Resumen completo leído vía OpenAlex. OpenAlex da el segundo autor como "Basheer Nayef Al-Duwairi"; se usa la forma de Crossref para las iniciales.
- Hechos verificados (según el resumen):
  - Afirman que, aunque el estándar JWT es seguro, algunas implementaciones aún presentan problemas, y analizan las bibliotecas de Python más utilizadas para autenticación con JWT.
  - Enumeran los algoritmos de firma que soporta cada biblioteca y aplican herramientas de pruebas estáticas de seguridad de aplicaciones (SAST) para revisar tanto la adhesión a PEP8 como vulnerabilidades y errores comunes, analizando las advertencias más relevantes para el riesgo de seguridad.
  - Miden además la popularidad y adopción de cada biblioteca con estadísticas de GitHub y la herramienta Sourcegraph.
  - Limitación de lo leído: el resumen no reporta qué bibliotecas fallaron ni cuántas vulnerabilidades hallaron; no atribuirles cifras.
- Cita en texto: (Shatnawi et al., 2024)
- Uso sugerido: MT 4.7

### [ferraiolo2001] Ferraiolo et al. (2001)
- Referencia APA 7: Ferraiolo, D. F., Sandhu, R., Gavrila, S., Kuhn, D. R., & Chandramouli, R. (2001). Proposed NIST standard for role-based access control. *ACM Transactions on Information and System Security, 4*(3), 224–274. https://doi.org/10.1145/501978.501980
- Tipo: artículo (propuesta de estándar; fundacional)
- Verificación: Crossref (api.crossref.org/works/10.1145/501978.501980), consultado 2026-10-06: coinciden los cinco autores, título, revista, volumen 4(3), páginas 224-274 y año 2001 (agosto). Resumen leído en Crossref. El DOI da HTTP 403 al acceso automático (bloqueo del editor).
- Hechos verificados (según el resumen):
  - Proponen un estándar para el control de acceso basado en roles (RBAC), señalando que, aunque los modelos RBAC tenían amplio respaldo y ventajas para la gestión de autorización a gran escala, no existía una definición autorizada única, lo que generaba incertidumbre sobre su utilidad y significado.
  - El estándar unifica ideas de modelos de referencia frecuentes, productos comerciales y prototipos de investigación, y se organiza en el Modelo de Referencia RBAC y la Especificación Funcional del Sistema y de Administración.
  - Se concibe como base para el desarrollo, la evaluación y la contratación de productos, y se limita a las características que ya habían logrado aceptación comercial y en la comunidad de investigación.
  - Justificación como fundacional: es la definición del modelo RBAC de NIST; la fuente más citable para describir roles, permisos y asignación de roles. Anterior a 2021 (excepción justificada).
- Cita en texto: (Ferraiolo et al., 2001)
- Uso sugerido: MT 4.7

### [krawczyk1997] Krawczyk et al. (1997)
- Referencia APA 7: Krawczyk, H., Bellare, M., & Canetti, R. (1997). *HMAC: Keyed-hashing for message authentication* (RFC 2104). Internet Engineering Task Force. https://doi.org/10.17487/RFC2104
- Tipo: norma (RFC de categoría Informational, del IETF; fundacional)
- Verificación: Crossref (api.crossref.org/works/10.17487/RFC2104) y texto oficial en rfc-editor.org/rfc/rfc2104.txt, consultados 2026-10-06: coinciden autores (H. Krawczyk, M. Bellare, R. Canetti), título, número de RFC y fecha de febrero de 1997. El documento indica que es "Informational" y que no especifica un estándar de Internet; la encabeza el Network Working Group. Se leyeron el resumen y las secciones 1 a 3. El DOI resuelve (HTTP 200).
- Hechos verificados (texto completo, secciones 1 a 3):
  - Describe HMAC como un mecanismo de autenticación de mensajes basado en funciones hash criptográficas, que puede usarse con cualquier función hash iterativa (ejemplos: MD5 y SHA-1) combinada con una clave secreta compartida; su fortaleza criptográfica depende de las propiedades de la función hash subyacente.
  - Sus objetivos de diseño incluyen usar sin modificaciones las funciones hash disponibles, conservar el rendimiento original de la función hash, manejar las claves de forma sencilla y permitir reemplazar la función hash si aparecen alternativas más rápidas o seguras.
  - La sección 3 indica que las claves deben elegirse al azar (o con un generador pseudoaleatorio criptográficamente fuerte) y renovarse periódicamente; desaconseja claves de menos de L bytes por reducir la seguridad de la función.
  - Justificación como fundacional: es el documento de referencia del IETF para HMAC, citado por las especificaciones posteriores. No menciona SHA-256 (es de 1997); las prácticas actuales con SHA-256 se documentan en Stripe y GitHub.
- Cita en texto: (Krawczyk et al., 1997)
- Uso sugerido: MT 4.7 | Metodología

### [owasp-api2023] OWASP API Security Project (2023)
- Referencia APA 7: OWASP API Security Project. (2023). *OWASP API security top 10 – 2023*. OWASP Foundation. https://api-security.owasp.org/editions/2023/en/0x11-t10/
- Tipo: documentación técnica (guía abierta de seguridad)
- Verificación: WebFetch de https://owasp.org/API-Security/editions/2023/en/0x11-t10/ (redirige de forma permanente a api-security.owasp.org, que es la URL registrada) y de la página de API2:2023 (api-security.owasp.org/editions/2023/en/0xa2-broken-authentication/), 2026-10-06: confirman la edición 2023 y el proyecto OWASP API Security. El contenido llegó como resumen automático de la herramienta.
- Hechos verificados (según el resumen de la herramienta sobre las páginas):
  - La edición 2023 lista diez riesgos: API1 Broken Object Level Authorization, API2 Broken Authentication, API3 Broken Object Property Level Authorization, API4 Unrestricted Resource Consumption, API5 Broken Function Level Authorization, API6 Unrestricted Access to Sensitive Business Flows, API7 Server Side Request Forgery, API8 Security Misconfiguration, API9 Improper Inventory Management y API10 Unsafe Consumption of APIs.
  - API2:2023 describe la autenticación rota, entre otros casos, la aceptación de tokens JWT sin firma o con firma débil (algoritmo `none`) o sin validar su vencimiento, y recomienda adoptar estándares de autenticación establecidos en lugar de implementaciones propias.
  - API5:2023 relaciona los fallos de autorización a nivel de función con políticas de control de acceso complejas (jerarquías, grupos y roles) y una separación poco clara entre funciones administrativas y regulares.
- Cita en texto: (OWASP API Security Project [OWASP], 2023) la primera vez; (OWASP, 2023) después.
- Uso sugerido: MT 4.7 | Metodología

---

## Fuentes descartadas

- NIST SP 800-224, *Keyed-Hash Message Authentication Code (HMAC): Specification of HMAC and Recommendations for Message Authentication* (M. Sönmez Turan, 2025), DOI 10.6028/NIST.SP.800-224. El DOI figura en Crossref con fecha 2025, pero el enlace del DOI (nvlpubs.nist.gov, PDF final) y la página csrc.nist.gov/pubs/sp/800/224/final respondieron HTTP 404; solo se pudo abrir el borrador inicial (ipd, 2024). No se usa un borrador ni se atribuye contenido a una versión final no verificada. RFC 2104 cubre la definición de HMAC.
- Effendi, J. R. J. R., Prawiro, N. L., Putra, M. F. Z., & Yulianto, B. (2026), "Comparing the performance of polling and websocket approaches for small-scale real-time web applications", IncoSST 2026, DOI 10.1109/incosst69426.2026.11709522. Metadatos verificados en Crossref y OpenAlex, pero no se pudo leer el resumen ni el texto (el registro de Zenodo que enlaza OpenAlex solo contiene un archivo CSV de datos); no se pueden atribuir hechos.
- Serbout, S., & Pautasso, C. (2024), "OAS2Tree: Visual API-first design", LNCS, DOI 10.1007/978-3-031-71246-3_2. Metadatos verificados en Crossref y OpenAlex; el editor omite el resumen (Semantic Scholar lo indica) y el texto es de acceso cerrado. Se descarta hasta poder leerlo.
- Tiwari, K. V., & Sharma, S. (2023), "An optimization model for vehicle routing problem in last-mile delivery", *Expert Systems with Applications* 222, DOI 10.1016/j.eswa.2023.119789. Metadatos coinciden en OpenAlex, pero no se obtuvo el resumen.
- Muriyatmoko, D., Djunaidy, A., & Muklason, A. (2024), "Heuristics and metaheuristics for solving capacitated vehicle routing problem: An algorithm comparison", *Procedia Computer Science* 234, DOI 10.1016/j.procs.2024.03.032. Verificado en Crossref y con resumen leído (compara cuatro heurísticas y cuatro metaheurísticas con OR-Tools y concluye que las metaheurísticas superan a las heurísticas en el caso complejo de cuatro vehículos), pero no incluye el vecino más cercano, por lo que se descarta por relevancia marginal. Queda de reserva si se necesita una comparación heurísticas frente a metaheurísticas.
- Suhaili, S. M., Salim, N., & Jambli, M. N. (2021), "Service chatbots: A systematic review", *Expert Systems with Applications* 184, DOI 10.1016/j.eswa.2021.115461. Metadatos verificados en Crossref, pero Crossref y OpenAlex no traen resumen y el texto es de acceso cerrado; no se pueden atribuir hechos. Se prefirió Nicolescu y Tudorache (2022).
- Su, R., & Li, X. (2024), "Modular monolith: Is this the trend in software architecture?", ACM, DOI 10.1145/3643657.3643911, y Tsechelidis, M., et al. (2023), "Modular monoliths the way to standardization", ACM, DOI 10.1145/3624486.3624506. Ambos verificados en Crossref con resumen leído vía OpenAlex (revisión de literatura gris con tres marcos y cuatro casos; estudio con 12 arquitectos con comentarios positivos pero dudas sobre proyectos grandes), pero se omitieron para no inflar el pool, ya que Al-Qora'n y Al-Said Ahmad (2025) y Su et al. (2024) cubren el tema con mayor solidez. Quedan de reserva.
- Venčkauskas, A., et al. (2023), "Enhancing microservices security with token-based access control method", *Sensors* 23(6), DOI 10.3390/s23063363, y Aldea, C. L., & Bocu, R. (2025), *Applied Sciences* 15(22), DOI 10.3390/app152212088. Metadatos verificados en Crossref y OpenAlex con resumen leído, pero el resumen no habla de JWT ni de RBAC específicamente (el primero propone un método de control de acceso para microservicios; el segundo, controles de seguridad de Zero Trust con Spring Boot y Docker). Relevancia indirecta; descartadas.
- Farooq, M. S., Riaz, S., & Alvi, A. (2022), "Cross-platform mobile development approaches and frameworks", *VFAST Transactions on Software Engineering* 10(2), DOI 10.21015/vtse.v10i2.978. Resumen leído vía OpenAlex (revisión sistemática de 22 estudios de 2012 a 2022), pero no se completó la verificación en Crossref y el resumen no menciona Ionic ni Capacitor. Queda de reserva.
- Artículos de revistas de dudosa revisión por pares o repositorios generalistas encontrados en las búsquedas, entre ellos "API First Development: A Modern Approach to Building Integrated Software Systems" (IJSR, 2021), "Leveraging Server-Sent Events for Enterprise-Scale Real-Time Notifications" (IJSR, 2023), varios preprints de SSRN sobre monolito modular y servicios REST (2026), entradas de Zenodo sobre webhooks ("Production Webhooks in Node.js", "Webhooks: GitHub's Knock on Your Door", esta última con coautoría de modelos de IA) y numerosos artículos de IJSREM, IJRASET e IJFMR sobre PWA y JWT. No se pudo establecer su arbitraje; se prefirieron fuentes con editorial reconocida.
- Publicaciones de blog y de la industria sobre el regreso a monolito (por ejemplo, el caso de Amazon Prime Video): no se consultó la fuente primaria; el caso aparece nombrado en Su et al. (2024), que es la fuente verificada que lo recoge.
- Malavolta, I., Chinnappan, K., & Jasmontas, L. (2020), "Evaluating the impact of caching on the energy consumption and performance of progressive web apps", MOBILESoft 2020, DOI 10.1145/3387905.3388593. Aparece en OpenAlex y es relevante para PWA, pero no se verificó en Crossref ni se leyó su resumen en esta sesión, y es anterior a 2021; queda como pista para el estudiante.

## Vacíos

- **PWA:** no se encontró una fuente verificada y de buena calidad sobre aplicaciones web progresivas (comparación PWA frente a nativas o híbridas). Los resultados de OpenAlex y Crossref fueron de revistas poco confiables o sin resumen accesible; la única pista seria (Malavolta et al., 2020) quedó sin verificar. Si el Marco Teórico necesita desarrollar PWA, debe limitarse a lo que dice la documentación de Capacitor (que lista la web/PWA como plataforma de destino) o marcarse `[COMPLETAR: fuente sobre PWA]`.
- **Capacitor e Ionic específicamente:** no hay estudios académicos sobre Capacitor. Las evidencias de rendimiento sobre Ionic son indirectas y limitadas (Oliveira et al., 2023, con benchmarks intensivos en CPU; Kaczmarczyk et al., 2022, solo con resumen sin resultados; Zou y Darus, 2024, descriptivo). Tampoco se halló evidencia sobre mantenimiento a largo plazo de aplicaciones híbridas frente a nativas.
- **Webhooks:** la evidencia académica es mínima (Dunér y Nilsson, 2020, trabajo de pregrado con repositorio no accesible). El respaldo de la firma HMAC en webhooks descansa en documentación de proveedores (Stripe y GitHub) y en el RFC 2104; no hay estudios arbitrados sobre seguridad de webhooks verificados.
- **API Keys como mecanismo de autenticación máquina a máquina:** no se encontró una fuente académica específica. Solo se cubre de forma indirecta con OWASP API2:2023 (autenticación rota). Si se quiere justificar el diseño de las claves de integración, conviene documentación oficial de Django REST Framework o de un proveedor; no se verificó en esta pasada.
- **Documentación oficial de Django, Django REST Framework, Django Channels, Angular y Ionic Framework:** no se incluyó porque el pedido priorizaba literatura y normas; podría añadirse como documentación técnica verificable si el estudiante la quiere en la Metodología.
- **Comparación empírica de rendimiento monolito frente a microservicios para sistemas pequeños:** Bjørndal et al. (2021) aportan la metodología pero su resumen no reporta resultados; Gonçalves et al. (2021) trata la modularización. No se encontró una comparación directa con cifras que se haya podido leer en esta sesión.
- **Geocodificación en Colombia o Latinoamérica:** no se encontró un estudio sobre la calidad de Nominatim u OpenStreetMap para direcciones colombianas; Pérez y Aybar (2024) es de Madrid y Kılıç et al. (2023) no identifica el país en el resumen. Esa brecha es una limitación a declarar del prototipo, no una afirmación a sostener.
- **Heurísticas para ruteo de mensajería con pocos vehículos:** no se halló una fuente verificada que evalúe el vecino más cercano en entornos reales de última milla; el soporte es teórico (Hougardy y Wilde, 2015) y de contexto (Jazemi et al., 2023; Dantzig y Ramser, 1959). Cualquier afirmación sobre la calidad práctica de la heurística del prototipo debe quedar como trabajo futuro.
- **Chatbots con tool calling en atención al cliente de logística:** no se encontró evidencia específica del sector de mensajería. Brynjolfsson et al. (2025) y Nicolescu y Tudorache (2022) son de atención al cliente en general; Qu et al. (2025) y las fuentes de riesgo (Greshake et al., 2023; Zhan et al., 2024; OWASP) cubren la herramienta y sus amenazas.
- **Accesos bloqueados:** el texto completo de Mendonça et al. (2021, IEEE) y de Kaczmarczyk et al. (2022, MDPI) no se pudo abrir desde este entorno; los datos de esas entradas se limitan al resumen. La página del repositorio de Dunér y Nilsson (2020) tampoco respondió.
