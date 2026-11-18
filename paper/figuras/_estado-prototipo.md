# Estado verificado del prototipo (2026-11-17)

- `manage.py test` (backend): **72 pruebas, todas OK** (Ran 72 tests; system check sin problemas).
- INSTALLED_APPS propias: accounts, coverage, services, tracking, optimization, integrations (6 apps; el resto es framework: daphne, channels, DRF, simplejwt, corsheaders, drf_spectacular).
- Rutas: 6 ViewSets con router (usuarios, cobertura, servicios, rutas, integraciones/api-keys, integraciones/webhooks) + 9 rutas `path()` explícitas (accounts 5, optimization 1, tracking 3: posicion, ultima-posicion, destino) + `api/schema/` y `api/docs/`. Conteo por inspección de urls.py, no por listado exhaustivo de acciones.
- Base db.sqlite3 usada: 3 servicios de prueba (2 entregas, 1 recolección), 1 ruta, usuarios demo. Se añadió 1 posición GPS ficticia (servicio 2) para el mapa.

## Figuras (en paper/figuras/)
- fig-casos-uso.png (2000 px): 2x2 de los 4 diagramas de casos de uso. Se corrigieron los SVG de Administrador (sin "Gestionar inventario") y Cliente (sin "Usar chatbot" ni "Comprar producto"; subtítulo ajustado).
- fig-mer.png (docs/diagrams/img/mer-entrega.png): MER de 12 entidades (USUARIO, COBERTURA, RUTA, SERVICIO, EVIDENCIA, NOVEDAD, MENSAJE_CHAT, POSICION_GPS, PUNTO_GEOCODIFICADO, API_KEY, WEBHOOK_ENDPOINT, WEBHOOK_DELIVERY).
- fig-mockups.png (2400 px): mockups (no son capturas reales) AlistadorCrearServicio (1200x800, se quitó "Producto (opcional)"), MotorizadoDetalle y ClienteTracking (390x844).
- fig-prototipo.png (2000 px): capturas REALES: lista de servicios del alistador (1000x700), detalle de servicio #2 del motorizado (390x844), tracking del cliente con mapa Leaflet/OSM, destino y ETA (390x844).

## Notas
- Los mockups muestran datos de ejemplo y un chat (cliente–motorizado) coherente con el alcance; el detalle del prototipo no muestra aún evidencia porque el servicio #2 está ASIGNADO.
- docs/10-diagrama-casos-uso.md ya está marcado como histórico (no modificado).
