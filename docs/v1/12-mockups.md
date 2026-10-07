# Mockups — CMEDriver

Canvas navegable con las 7 pantallas clave del MVP: **https://claude.ai/code/artifact/9fcedc09-e71f-49e7-accb-16ca8795d8bb**

Archivos fuente editables en [mockups/src/](mockups/src/) (formato `.dc.html`, uno por pantalla) y layout en [mockups/src/canvas.json](mockups/src/canvas.json).

## Pantallas incluidas
| Pantalla | Rol | Qué muestra |
|---|---|---|
| Login | Todos | Ingreso único con usuario/contraseña, hint de credenciales demo |
| Dashboard | Administrador | Conteo de servicios por estado (8 KPIs) + navegación a Usuarios/Cobertura |
| Crear servicio | Alistador | Formulario de creación (tipo Entrega/Recolección) + lista de servicios recientes con badges de estado |
| Mis servicios | Motorizado | Lista del día, diferenciando visualmente Entrega vs Recolección por color/ícono |
| Cerrar recolección | Motorizado | Detalle de un servicio EN_TRANSITO con el flujo de evidencia (foto + firma) antes de poder cerrar |
| Tracking y chat | Cliente | Mapa con la posición del motorizado + chat del mismo servicio |
| Chatbot guiado | Cliente | Flujo por botones/menús: comprar producto o solicitar recolección |

## Notas de diseño
- Estilo: paleta neutra con azul corporativo como acento (`#1D4ED8`), tipografía del sistema (coherente con cómo se ve una app Ionic real), tarjetas con esquinas redondeadas y badges de color por estado.
- Son **mockups estáticos** (no clicables) — representan el diseño visual objetivo del producto, no necesariamente el estilo del build de desarrollo actual del frontend (que todavía usa los componentes por defecto de Ionic sin personalizar).
- Sirven como referencia visual para implementar el theming/estilos definitivos sobre el frontend Ionic + Angular ya funcional.
