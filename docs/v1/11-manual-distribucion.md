# Manual de instalación y distribución — CMEDriver

## 1. Requisitos del sistema

| Componente | Requisito |
|---|---|
| Sistema operativo | Windows, macOS o Linux (probado en Windows 11) |
| Backend | Python 3.11+ (probado con 3.12) |
| Frontend | Node.js 18+ y npm 9+ (probado con Node 24 / npm 11) |
| Base de datos (MVP) | SQLite (incluida, sin instalación adicional) |
| Base de datos (producción sugerida) | PostgreSQL 14+ |
| Navegador | Cualquier navegador moderno (Chrome, Edge, Firefox) — la app corre en el navegador, no requiere instalación en el celular |

No se requieren licencias de pago ni API keys (los mapas usan Leaflet + OpenStreetMap).

## 2. Instalación del backend (Django)

```bash
cd backend
py -m venv .venv                       # Windows
# o: python3 -m venv .venv             # macOS/Linux

# Windows
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe manage.py migrate
./.venv/Scripts/python.exe manage.py seed_data
./.venv/Scripts/python.exe manage.py runserver 0.0.0.0:8000

# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver 0.0.0.0:8000
```

Verificación: abrir `http://localhost:8000/api/docs/` debe mostrar la documentación Swagger de la API.

### Variables de configuración relevantes (`backend/cmedriver/settings.py`)
| Variable | Uso | Valor MVP |
|---|---|---|
| `DEBUG` | Activa mensajes de error detallados y sirve `media/` directamente | `True` (cambiar a `False` en producción) |
| `SECRET_KEY` | Firma de sesiones/tokens | Clave de desarrollo incluida — **regenerar antes de producción** |
| `DATABASES` | Motor de base de datos | SQLite (cambiar a PostgreSQL en producción) |
| `CORS_ALLOWED_ORIGINS` | Orígenes permitidos para el frontend | `localhost:8100` / `localhost:4200` — agregar el dominio real en producción |
| `SIMPLE_JWT` | Duración de tokens de acceso/refresco | 8h / 1 día |

## 3. Instalación del frontend (Ionic + Angular)

```bash
cd frontend
npm install
npm start        # o: npx ionic serve
```

La app queda disponible en `http://localhost:4200` (o `:8100` según el comando usado) y espera al backend en `http://localhost:8000/api` (configurable en `frontend/src/environments/environment.ts`).

Para generar un build de producción (archivos estáticos listos para servir desde cualquier servidor web):
```bash
npm run build
```
Esto genera una carpeta `www/` (o `dist/`) que puede desplegarse en cualquier servidor de archivos estáticos (Nginx, Apache, Netlify, Vercel, un bucket S3 con hosting estático, etc.).

## 4. Datos iniciales (usuarios de prueba)
Ver tabla completa en el [README.md](../README.md) principal. Resumen: `admin/admin1234`, `alistador1/alistador1234`, `motorizado1/motorizado1234`, `cliente1/cliente1234`.

**Importante:** estos usuarios y contraseñas son solo para demo/desarrollo. Antes de cualquier despliegue real, se deben crear usuarios nuevos con contraseñas seguras y desactivar o eliminar los usuarios de demo.

## 5. Despliegue en producción (recomendaciones)

Este MVP corre en modo desarrollo (`runserver` de Django + servidor de desarrollo de Angular). Para un despliegue real:

1. **Backend**: servir con un servidor WSGI de producción (ej. `gunicorn` o `waitress`) detrás de un proxy (Nginx). Cambiar `DEBUG=False`, definir `ALLOWED_HOSTS`, migrar a PostgreSQL, y servir `media/` desde almacenamiento persistente (o un bucket tipo S3).
2. **Frontend**: generar el build (`npm run build`) y servir los archivos estáticos resultantes desde el mismo Nginx o un CDN.
3. **Variables sensibles**: mover `SECRET_KEY` y credenciales de base de datos a variables de entorno (no versionarlas en el repositorio).
4. **HTTPS**: obligatorio en producción, tanto para la API como para el frontend (los navegadores restringen geolocalización y cámara en sitios sin HTTPS).
5. **Contenedores (opcional, recomendado a futuro)**: empaquetar backend y frontend en imágenes Docker separadas + un `docker-compose.yml` con PostgreSQL, para reproducibilidad del entorno. No incluido en el MVP por tiempo, pero es el siguiente paso natural (ver [07-roadmap-futuro.md](07-roadmap-futuro.md)).

## 6. Respaldo y mantenimiento
- **Backup de base de datos**: en SQLite, respaldar el archivo `backend/db.sqlite3` periódicamente. En PostgreSQL, usar `pg_dump` programado.
- **Backup de evidencias**: la carpeta `backend/media/evidencias/` contiene las fotos y firmas — debe respaldarse junto con la base de datos (o migrarse a almacenamiento en la nube en producción).
- **Migraciones**: cualquier cambio a los modelos requiere `python manage.py makemigrations` seguido de `python manage.py migrate` en el entorno destino.

## 7. Problemas comunes (troubleshooting)
| Síntoma | Causa probable | Solución |
|---|---|---|
| Frontend no puede llamar a la API (error CORS) | El origen del frontend no está en `CORS_ALLOWED_ORIGINS` | Agregar el origen real en `settings.py` |
| Login funciona pero las peticiones siguientes devuelven 401 | Token expirado o no se está enviando el header `Authorization` | Verificar el interceptor HTTP del frontend y la duración configurada en `SIMPLE_JWT` |
| La cámara o el GPS no funcionan en el celular | El sitio no está en HTTPS (ni es `localhost`) | Los navegadores móviles exigen HTTPS para geolocalización/cámara fuera de `localhost` |
| `python` no se reconoce en Windows | Alias de Microsoft Store interceptando el comando | Usar el launcher `py` en su lugar (`py -m venv .venv`, etc.) |
