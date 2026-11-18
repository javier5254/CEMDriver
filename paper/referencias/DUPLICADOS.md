# Depuración de referencias duplicadas (Entrega 3)

La docente observó que Al-Qora'n y Al-Said Ahmad 2025a y 2025b eran el mismo artículo. La auditoría de `Proyecto_CMEDriver_Final.docx` (84 citas, bibliografía de Mendeley Cite) encontró que no era el único caso: el documento tenía **46 ids de Mendeley para 35 fuentes reales**. Respaldo previo: `paper/_respaldo/Final_antes_de_duplicados.docx`.

## Grupos fusionados en el documento (9)

| Fuente (DOI o título) | Ids que había | Citas por id | Queda |
|---|---|---|---|
| Al-Qora'n y Al-Said Ahmad (2025), 10.3390/fi17110496 | 2025a, 2025b | 1 / 2 | Al-Qora'n y Al-Said Ahmad, 2025 |
| Beaulieu et al. (2022), 10.1007/978-3-030-97652-1_10 | 2022a, 2022b | 1 / 2 | Beaulieu et al., 2022 |
| Ley 1581 de 2012 | 2012a, 2012b | 1 / 6 | Ley 1581 de 2012, 2012 |
| Mohammad et al. (2023), 10.1080/16258312.2023.2173488 | 2023a, b, c | 1 / 2 / 1 | Mohammad et al., 2023 |
| Pérez y Aybar (2024), 10.3390/ijgi13060170 | 2024a, 2024b | 1 / 2 | Pérez y Aybar, 2024 |
| Randerath y Friedrich (2025), 10.1177/20501579241270785 | 2025a, 2025b | 2 / 1 | Randerath y Friedrich, 2025 |
| Restrepo-Betancur et al. (2026), 10.1016/j.trip.2026.102181 | 2026a, b, c | 2 / 1 / 1 | Restrepo-Betancur et al., 2026 |
| DNP (2023), comunicado del costo logístico | dos registros (autor mal analizado "Planeación, D. N. de") | 2 / 1 | Departamento Nacional de Planeación (2023) |
| DNP (2025), ENL 2024 | dos registros (ídem) | 1 / 1 | Departamento Nacional de Planeación (2025) |

Resultado: **35 referencias únicas**, 30 citas modificadas (JSON de Mendeley, `citeprocText` y texto visible sin sufijos a/b/c), 11 entradas sobrantes eliminadas de la bibliografía, sin huérfanas en ningún sentido y sin sufijos restantes.

## Otros archivos

`referencias/*.bib`, `*.ris` (incluido `referencias-unificado.*`), `secciones/referencias-entrega1.md` y `referencias-entrega2.md` y la lista KEYS de `build/build.js` **ya no tenían duplicados** (una entrada por fuente, 36 en el unificado); no se modificaron. El duplicado vivía solo en la biblioteca de Mendeley y en los campos del Word.

## Pasos manuales del estudiante en Mendeley

1. Mendeley Reference Manager > **Library** > menú **Duplicates** (o "Check for Duplicates").
2. Revisar cada grupo de la tabla y pulsar **Merge** para dejar un solo registro (conservar el de autores con nombres completos).
3. En Word: pestaña **Mendeley Cite** > **Refresh**. Como el documento ya apunta a un solo id por fuente, la bibliografía quedará igual, sin sufijos a/b/c.

El documento ya no depende de los registros duplicados: si se borran o fusionan en la biblioteca, las citas siguen resolviendo al id conservado.
