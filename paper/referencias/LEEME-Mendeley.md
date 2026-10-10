# Referencias de CMEDriver en Mendeley

> **Actualización 2026-10-09 (cambio de alcance).** Las listas de referencias cambiaron: en la Entrega 2 se retiraron Su et al. (2024) y OWASP GenAI Security Project (2025) y se agregaron Madhwal et al. (2022) y Souza et al. (2022); la Entrega 1 no cambió. Cada lista sigue con 10 y 28 fuentes. **Los archivos `.bib` y `.ris` no están en esta carpeta** (solo este LEEME); hay que regenerarlos a partir de `secciones/referencias-entrega1.md` y `referencias-entrega2.md`, que son la versión vigente, o importar las fuentes con DOI directamente en Mendeley.

Archivos previstos: `entrega1.bib` y `entrega1.ris` (10 fuentes), `entrega2.bib` y `entrega2.ris` (28 fuentes). Son exactamente las listas de `secciones/referencias-entrega1.md` y `referencias-entrega2.md`. Las fuentes con DOI traían metadatos de Crossref (títulos y años ajustados a la lista del pool); las demás se escribieron a mano desde el pool, sin campos añadidos.

## 1. Importar en Mendeley Reference Manager

1. Entrar a Mendeley Reference Manager con la cuenta del estudiante.
2. Crear una colección (por ejemplo "CMEDriver Entrega 1").
3. Menú **Add new > File(s) from computer** y elegir `entrega1.ris` (o `.bib`). Repetir con la Entrega 2 en otra colección.
4. Revisar cada registro importado (ver sección 5) y completar los campos faltantes.

## 2. Estilo APA 7

En Mendeley Cite (Word), **Citation style > American Psychological Association 7th edition**.

## 3. Mendeley Cite en Word

1. En Word: **Insertar > Obtener complementos**, buscar "Mendeley Cite" e instalarlo (requiere iniciar sesión).
2. En la pestaña **Referencias > Mendeley Cite**, iniciar sesión.
3. Poner el cursor donde va la cita, **Insert citation**, buscar y marcar la fuente, y confirmar. Para citas con página, editar la cita y añadir "Page".
4. Al terminar el texto: **Insert bibliography**. Se actualiza con **Refresh** cuando se agreguen o quiten citas.
5. Las citas del texto actual (escritas a mano en los .docx) deben sustituirse por citas de Mendeley Cite, o dejarse como texto y pegar la bibliografía generada solo si el docente lo acepta.

## 4. Adaptación UNINPAHU (verificar contra la guía)

Mendeley genera APA 7 estándar en inglés. Verificar contra la guía y corregir en Word:

- Sangría francesa de 1,27 cm y orden alfabético por apellido del primer autor.
- Sin citas textuales de 40 palabras o más (usar paráfrasis).
- Uso de IA declarado en el texto y en las referencias (entrada Anthropic, 2026, ya incluida en `entrega2`).
- Idioma: Mendeley puede escribir "&", "In", "Article", "n.d." y "et al." en inglés; la lista de CMEDriver usa "&" y "En", "Artículo/Article", "s. f.". Ajustar a mano si la docente lo exige.
- Solo se listan las fuentes citadas en el texto.

## 5. Referencias que Mendeley no importa bien (completar a mano)

- **Normas y leyes** (Ley 1581 de 2012, Ley 23 de 1982, Decisión Andina 351 de 1993): Mendeley no tiene tipo "legislación" en .bib. Se importaron como documento genérico con el nombre de la norma como autor. El estilo APA las mostrará como "Ley 1581 de 2012 (2012). Título…"; editar para obtener "Ley 1581 de 2012. (2012, 17 de octubre). Por la cual… Diario Oficial No. 48.587. URL" (el diario oficial y la fecha completa están en el campo de nota/howpublished).
- **ISO/IEC/IEEE 29148:2018**: importada como documento genérico; el número de norma queda en una nota.
- **Páginas web sin fecha** (Brown, C4 model; Dirección Nacional de Derecho de Autor, Registro de software): sin año; Mendeley mostrará "n.d."; cambiar a "s. f." en el texto. Poner el nombre del sitio si la guía lo exige.
- **Comunicados de prensa del DNP** (2023, 2025): la etiqueta "Comunicado de prensa" va entre corchetes tras el título; Mendeley no la coloca así.
- **Informes** (CCCE, MinTIC): MinTIC lleva "Colombia TIC" como editorial; verificar.
- **Anthropic (2026), Claude [Modelo de lenguaje grande]**: la nota entre corchetes se añade a mano.
- **Beck et al. (2001)** y **Schwaber y Sutherland (2020)**: documentos web; revisar que salgan sin editorial duplicada.
- **Kuhrmann et al. (2022)**: Crossref entrega los 19+ autores sin diacríticos (Münch, Tüzün, López, Küpper); APA 7 muestra 19 y puntos suspensivos; corregir apellidos si se desea.
- **Randerath y Friedrich**: la lista usa 2025 (número 1 del vol. 13); Crossref indica 2024 de publicación en línea. Se dejó 2025.
- **Artículos con número de artículo** (Al-Qora'n, Pérez, Jazemi, Restrepo-Betancur, Gutierrez-Franco, Janinhoff, Bogner, Parizi): el .bib lo pone como `pages`; APA 7 pide "Article N". Editar en Mendeley si el estilo muestra solo el número.
- **Beaulieu et al. (2022)**: capítulo de actas; el editor (Latifi, S.) y la editorial "Springer" vienen de la lista. Mendeley puede mostrarlo como capítulo; verificar "En S. Latifi (Ed.)".
- **Libros** (Bass, Sommerville, Hernández-Sampieri): importan bien, pero la edición ("2.ª", "7.ª") se escribe "2nd ed." en APA en inglés; ajustar. Hernández-Sampieri: pendiente confirmar el tercer autor.

## 6. Diferencias entre el pool y el formato exigido por la guía APA UNINPAHU

Comparadas con "Guía trabajos escritos IA: Normas APA":

1. **Documentos web**: la guía pide "Organización. (Año, día mes). *Título*. Sitio web. URL". Las entradas de Brown (s. f.), DNDA (s. f.), Manifiesto Ágil, Scrum Guide, CCCE y los comunicados del DNP no traen el nombre del sitio (sí lo traen OWASP y MinTIC). Añadirlo solo si se verifica; no se inventó.
2. **Legislación**: la guía usa "Ley 23 de 1982. (1982, 19 de febrero). Sobre derechos de autor. Diario Oficial No. 35.949. URL"; el pool la sigue. La Decisión 351 del pool no pone el título en cursiva ni indica órgano emisor igual a la guía; es consistente con ese patrón, sin cursiva.
3. **Artículos**: la guía muestra "volumen(número), pp-pp" y el pool usa cursiva en revista y volumen, "Article N" y rango con raya (–). La guía usa guion corto y no menciona número de artículo; es una diferencia menor y APA 7 estándar la respalda.
4. **Idioma de la lista**: el pool mezcla "Article" (inglés) y "Artículo" (Parizi) y "En" para actas; unificar a español o inglés según el docente.
5. **Idioma de los títulos**: la guía no pide traducir; se dejaron en el idioma original.
6. **IA**: la entrada Anthropic (2026) sigue la estructura de la guía (modelo de lenguaje grande entre corchetes); la guía presenta la URL del ejemplo ChatGPT/Gemini igual.
