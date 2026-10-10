# Mockups — CMEDriver (v2)

> **Nota (2026-10-09):** este documento es **histórico**: se redactó antes de la reducción de alcance que retiró el inventario, los pagos y el chatbot (el chat quedó solo como canal entre el cliente y el motorizado) y **no refleja el alcance vigente**. Incluye la pantalla «Chatbot conversacional» (compra y pago), retirada; el frontend vigente no la tiene. Prevalece la documentación de [entrega/](entrega/00-guia-de-entrega.md), en particular [entrega/01-requerimientos.md §2.4](entrega/01-requerimientos.md#24-cambios-de-alcance).

> La versión v1 de estos mockups (7 pantallas, estilo Material) quedó congelada en [`v1/12-mockups.md`](v1/12-mockups.md) y [`v1/mockups/`](v1/mockups/).

Canvas navegable con las 11 pantallas clave del producto (MVP + funcionalidades v2): **https://claude.ai/code/artifact/9fcedc09-e71f-49e7-accb-16ca8795d8bb**

Archivos fuente editables en [mockups/src/](mockups/src/) (formato `.dc.html`, uno por pantalla) y layout en [mockups/src/canvas.json](mockups/src/canvas.json).

## Pantallas incluidas
| Pantalla | Rol | Qué muestra |
|---|---|---|
| Login | Todos | Ingreso único con usuario/contraseña (o correo), hint de credenciales demo |
| Recuperar contraseña | Todos | Solicitud de enlace de restablecimiento por correo, con aviso de modo desarrollo (enlace impreso en consola, sin envío real) |
| Dashboard | Administrador | Conteo de servicios por estado (8 KPIs) + navegación a Usuarios/Cobertura/API Keys/Webhooks |
| API Keys | Administrador | Alta de credenciales para integraciones externas, aviso de llave de un solo vistazo, listado con prefijo/estado/último uso |
| Webhooks | Administrador | Listado de endpoints suscritos a eventos, con bitácora de últimas entregas (éxito/fallo, código HTTP) expandida en línea |
| Crear servicio | Alistador | Formulario de creación (tipo Entrega/Recolección) + lista de servicios recientes con badges de estado |
| Optimizar ruta | Alistador | Sugerencia de orden de visita para una ruta ya asignada (heurística de vecino más cercano sobre direcciones geocodificadas), con distancia total estimada y paradas no geocodificables |
| Mis servicios | Motorizado | Lista del día, diferenciando visualmente Entrega vs Recolección por color/ícono |
| Cerrar recolección | Motorizado | Detalle de un servicio EN_TRANSITO con el flujo de evidencia (foto + firma) antes de poder cerrar |
| Tracking y chat | Cliente | Mapa en vivo (WebSocket) con la posición del motorizado, marcador de destino y ETA estimado, más acceso al chat del servicio |
| Chatbot conversacional | Cliente | Hilo de texto libre contra un LLM simulado (con "tool calling"): compra de productos y solicitud de recolección conversacional, con tarjetas de confirmación (servicio creado, pago) |

## Notas de diseño
- Estilo v2: paleta inspirada en iOS/Apple (`#007AFF` azul de sistema, `#34C759` verde, `#FF9500` ámbar, `#FF3B30` rojo, fondo `#F2F2F7`), tipografía del sistema (`-apple-system`/San Francisco con fallback a Segoe UI), tarjetas con esquinas redondeadas ~9-14px y badges de color por estado — reemplaza la paleta Material más plana de v1.
- El frontend real (Ionic + Angular) usa `mode: 'ios'` y estos mismos tokens de color (`frontend/src/theme/variables.scss`), pero **no replica pantalla por pantalla** el tratamiento de tarjetas/sombras de estos mockups — las pantallas del build funcional usan los componentes Ionic por defecto (listas planas, formularios estándar) sobre esa paleta de color. Los mockups son el objetivo visual a futuro, no un espejo 1:1 del estado actual del código.
- Son **mockups estáticos** (no clicables) — representan el diseño visual objetivo del producto.
- Llevar el tratamiento visual completo de estos mockups (tarjetas, sombras, estados vacíos) a cada pantalla del frontend es trabajo pendiente — ver [07-roadmap-futuro.md](07-roadmap-futuro.md).
