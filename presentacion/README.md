# Presentación de CMEDriver

Presentación HTML de la sustentación final. Es un solo archivo que abre sin internet (las fuentes de Google se usan si hay conexión y, si no, entran las del sistema), con 16 láminas que son las paradas de una ruta de entrega. Los indicadores salen de la base de datos del sistema y las capturas son de la aplicación en ejecución.

## Regenerar

Desde la raíz del repositorio, con cualquier Python 3 (solo se usa la biblioteca estándar; si Pillow está disponible, por ejemplo en `backend/.venv`, reduce las capturas):

```
python presentacion/construir.py
backend/.venv/Scripts/python.exe presentacion/construir.py     # en Windows, con el entorno del backend
```

Genera dentro de `presentacion/`:

| Archivo | Uso |
|---|---|
| `index.html` | Documento completo. Abrir con doble clic. |
| `index.artifact.html` | Fragmento (`<title>`, `<meta>`, `<style>`, contenido y `<script>`) para publicar como Artifact. Debe mostrarse en un contenedor con la altura de la ventana. |

El script imprime el tamaño de cada archivo. El fragmento debe quedar por debajo de 14 MB (hoy ocupa cerca de 1 MB).

Opciones: `--datos ruta.json` (otro JSON de indicadores, por ejemplo `datos/ejemplo-indicadores.json`), `--proyecto ruta.json`, `--capturas carpeta`, `--sin-reducir` (no usar Pillow) y `--webp` (recodificar capturas a WebP).

## De dónde salen los datos

| Fuente | Qué alimenta | Cómo actualizarla |
|---|---|---|
| `datos/indicadores.json` | Láminas 8, 9 y 10 (KPIs, gráficos, lectura, evidencia, novedades, integraciones). Todo se dibuja con SVG propio desde este JSON. | `python backend/manage.py exportar_indicadores --salida presentacion/datos/indicadores.json` (opciones `--dias` y `--zona`) y volver a construir. Para una demo con datos poblados, ejecutar antes `python backend/manage.py seed_demo`. |
| `datos/proyecto.json` | Láminas 11, 12 y 16: pruebas, aplicaciones, entidades, requisitos vigentes y totales, limitaciones y enlace del repositorio. | Editar el archivo con los valores medidos y volver a construir. |
| `capturas/*.png` | Láminas 7 y 10, mediante los marcadores `{{captura:nombre.png}}` de la plantilla. | Reemplazar el PNG y volver a construir. |
| `plantilla.html` | Textos, cronograma (SVG de la lámina 13) y presupuesto (constante `PRESUPUESTO` en el `<script>`, con total calculado por el script). | Editar y volver a construir. |
| `datos/ejemplo-indicadores.json` | Datos ficticios con el mismo contrato, solo para probar la construcción. | No se usa por defecto. |

Si falta `datos/indicadores.json`, el script avisa y las láminas de indicadores muestran un recuadro "sin datos" con la instrucción para generarlo; la presentación sigue funcionando. Si falta una captura, su lámina muestra un recuadro "captura pendiente" y el script avisa por consola.

### Cambiar cifras

- Indicadores: no se escriben a mano; se regenera el JSON.
- Cifras del proyecto: editar `datos/proyecto.json`. Las claves usadas son `pruebas`, `apps`, `entidades`, `requisitos_vigentes`, `requisitos_total`, `limitaciones_vigentes`, `limitaciones_altas` y `repositorio`.
- Presupuesto: editar `PRESUPUESTO` e `IMPREVISTOS` en `plantilla.html`. El subtotal, los imprevistos, el total de la tabla y el total del título se recalculan solos.
- Cronograma: las barras de la lámina 13 son SVG dentro de `plantilla.html` (columnas M1 a M6; cada fila ocupa 64 unidades).

### Capturas

| Archivo | Lámina | Proporción esperada |
|---|---|---|
| `indicadores-admin.png` | 7 | escritorio, 1440 x 900 |
| `motorizado-servicio.png` | 7 | móvil, 390 x 844 |
| `cliente-tracking.png` | 7 | móvil |
| `cliente-chat.png` | 7 | móvil |
| `swagger.png` | 10 | escritorio |

`servicios-alistador.png` y `admin-dashboard.png` están disponibles en la carpeta pero la plantilla actual no las usa. Para incluir una, agregar `<img src="{{captura:nombre.png}}" alt="...">` en un marco `.pantalla` (escritorio) o `.pantalla-m` (móvil). Las capturas más anchas de 1600 px se reducen y las que superan 350 KB se recodifican a WebP si ahorran al menos un 30 %.

## Atajos de teclado

| Tecla | Acción |
|---|---|
| `→`, `Espacio`, `AvPág` | Parada siguiente |
| `←`, `RePág` | Parada anterior |
| `Inicio`, `Fin` | Primera y última parada |
| `1` a `9` | Ir a esa parada (dos dígitos seguidos, por ejemplo `1` `2`, para las paradas 10 a 16) |
| `F` | Pantalla completa (si el navegador la rechaza, muestra un aviso) |
| `T` | Tema claro u oscuro (se recuerda en `localStorage` cuando está disponible) |
| `?` | Ayuda de atajos; `Esc` la cierra |
| `#p5` en la URL | Abre directamente la parada 5 |
| Deslizar (táctil) | Anterior y siguiente |
| `Ctrl` + `P` | Imprime una lámina por página (formato 1920 x 1080) |

También hay botones visibles de anterior y siguiente, tema, pantalla completa y ayuda en la barra de ruta, y cada nodo de la ruta lleva a su parada.

## Comportamiento

- Escenario fijo de 1920 x 1080 escalado a la ventana con franjas laterales o superiores si la proporción difiere de 16:9.
- Con menos de 720 px de ancho las láminas se apilan en una columna con desplazamiento vertical normal. Los diagramas anchos (ciclo de vida, arquitectura, cronograma, tabla del presupuesto) se desplazan horizontalmente dentro de su propio recuadro.
- Respeta `prefers-reduced-motion` (sin transiciones ni pulso) y `prefers-color-scheme`.

## Láminas

1. Portada
2. El problema
3. Operación actual (hipótesis P1 a P6)
4. La propuesta
5. Ciclo de vida
6. Los cuatro roles
7. El producto en acción
8. Indicadores del sistema
9. Evidencia y novedades
10. API para integradores
11. Arquitectura
12. Calidad y verificación
13. Cronograma
14. Presupuesto
15. Producto entregable
16. Siguiente parada

## Honestidad de los datos

Los indicadores de las láminas 8, 9 y 10 se generaron con `seed_demo` sobre la base de datos del sistema; no son operaciones reales de la empresa de referencia, y las láminas lo dicen en su pie. Los usuarios del prototipo son de prueba, el sistema no está desplegado y no se ha validado con operadores reales.
