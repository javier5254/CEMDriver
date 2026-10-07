# CMEDriver

Plataforma de gestión de servicios de mensajería (entregas y recolecciones) con 3 roles operativos (Administrador, Alistador, Motorizado) + vista de Cliente, tracking GPS, chat, chatbot guiado e inventario.

Toda la documentación del proyecto (charter, requisitos, arquitectura, modelo de datos, diagramas, API, cronograma, pruebas, mockups, manual de herramientas) está indexada en [docs/README.md](docs/README.md).

## Estructura del repo

```
CMEDriver/
  docs/       -> documentación del proyecto (léela primero)
  backend/    -> API REST en Django + Django REST Framework
  frontend/   -> app Ionic + Angular (login + 4 áreas por rol)
```

## Backend (Django) — probado y funcionando

```bash
cd backend
./.venv/Scripts/python.exe manage.py runserver 0.0.0.0:8000
```

- API en `http://localhost:8000/api/`
- Documentación interactiva (Swagger) en `http://localhost:8000/api/docs/`
- Panel de administración Django en `http://localhost:8000/admin/`

### Si necesitas recrear el entorno desde cero
```bash
cd backend
py -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe manage.py migrate
./.venv/Scripts/python.exe manage.py seed_data
```

### Usuarios de prueba (creados por `seed_data`)
| Usuario | Password | Rol |
|---|---|---|
| admin | admin1234 | ADMIN |
| alistador1 | alistador1234 | ALISTADOR |
| motorizado1 | motorizado1234 | MOTORIZADO |
| cliente1 | cliente1234 | CLIENTE |

`seed_data` también crea 2 zonas de cobertura, 3 productos (2 disponibles para el chatbot) y varios servicios de ejemplo en distintos estados (CREADO, ASIGNADO, ENTREGADO, RECOLECTADO) para poder probar la interfaz sin partir de cero.

El flujo completo (login → crear servicio → asignar ruta → recibir en centro/iniciar tránsito → cerrar con evidencia → novedades → tracking → chat → chatbot → planificación de recolección) fue validado end-to-end contra la API real.

## Frontend (Ionic + Angular) — probado y funcionando

```bash
cd frontend
npm install
npm start
```

Se sirve en `http://localhost:4200` y consume la API en `http://localhost:8000/api` (configurable en `frontend/src/environments/environment.ts`). Requiere el backend corriendo. Validado de punta a punta en los 4 roles: login, dashboards, ciclo de vida completo de servicios, tracking con Leaflet, chat, captura de foto/firma y chatbot guiado.

## Pruebas automatizadas

```bash
cd backend
./.venv/Scripts/python.exe manage.py test
```

Ver [docs/16-plan-pruebas.md](docs/16-plan-pruebas.md) para el detalle de casos de prueba y cómo correr subconjuntos.

## Siguientes pasos
Ver [docs/06-cronograma.md](docs/06-cronograma.md) para el plan de trabajo y [docs/07-roadmap-futuro.md](docs/07-roadmap-futuro.md) para lo que queda fuera del MVP.
