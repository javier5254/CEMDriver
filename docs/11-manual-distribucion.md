# Manual de instalación y distribución — CMEDriver (v2)

## 1. Requisitos del sistema

| Componente | Requisito |
|---|---|
| Sistema operativo | Windows, macOS o Linux (probado en Windows 11) |
| Backend | Python 3.11+ (probado con 3.12) |
| Frontend | Node.js 18+ y npm 9+ (probado con Node 24 / npm 11) |
| Base de datos (MVP) | SQLite (incluida, sin instalación adicional) |
| Base de datos (producción sugerida) | PostgreSQL 14+ |
| Navegador | Cualquier navegador moderno (Chrome, Edge, Firefox) — la app corre en el navegador, no requiere instalación en el celular |

No se requieren licencias de pago ni API keys para correr el MVP: los mapas y el geocoding usan OpenStreetMap/Nominatim (gratuitos), el correo sale por consola en desarrollo, y el chatbot/pagos usan implementaciones simuladas (ver [03-arquitectura.md](03-arquitectura.md)).

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

**Nota v2**: con `channels` y `daphne` instalados (ya incluidos en `requirements.txt`) y `daphne` como primera app en `INSTALLED_APPS`, el mismo comando `runserver` sirve automáticamente tanto HTTP como WebSockets (`ws://localhost:8000/ws/...`) — no hace falta levantar un proceso aparte para los sockets en desarrollo.

### Variables de configuración relevantes (`backend/cmedriver/settings.py`)
| Variable | Uso | Valor MVP |
|---|---|---|
| `DEBUG` | Activa mensajes de error detallados y sirve `media/` directamente | `True` (cambiar a `False` en producción) |
| `SECRET_KEY` | Firma de sesiones/tokens | Clave de desarrollo incluida — **regenerar antes de producción** |
| `DATABASES` | Motor de base de datos | SQLite (cambiar a PostgreSQL en producción) |
| `CORS_ALLOWED_ORIGINS` | Orígenes permitidos para el frontend | `localhost:8100` / `localhost:4200` — agregar el dominio real en producción |
| `SIMPLE_JWT` | Duración de tokens de acceso/refresco | 8h / 1 día |
| `CHANNEL_LAYERS` | Backend de la capa de canales (WebSockets) | En memoria (un solo proceso) — cambiar a `channels_redis.core.RedisChannelLayer` si se despliega con varios workers/procesos |
| `MAILERS` / `DEFAULT_FROM_EMAIL` | Envío de correo (reset de contraseña) | Backend de consola (imprime el correo en el log) — cambiar el `BACKEND` a un SMTP real en producción |
| `FRONTEND_URL` | Para construir el enlace de reset de contraseña en el correo | `http://localhost:4200` — cambiar al dominio real en producción |

### Conectar proveedores reales (opcional, más allá del MVP)
| Módulo | Archivo a modificar | Qué cambiar |
|---|---|---|
| Correo real | `settings.py` → `MAILERS` | Backend SMTP real (Gmail con contraseña de aplicación, SendGrid, Mailgun, AWS SES, Resend, etc.) |
| Chatbot con LLM real | `chatbot/llm.py` | Reemplazar `MockLLMClient` por una llamada real a la API de un proveedor (ej. Anthropic), manteniendo la misma firma `responder(historial, mensaje_nuevo)` y las mismas funciones "tool" ya construidas |
| Pagos reales | `payments/provider.py` | Reemplazar `MockPaymentProvider` por un cliente real de Wompi/PayU/Stripe, manteniendo la misma firma `procesar(pago)` |

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

## 4. Empaquetado nativo (Capacitor)

El frontend ya está configurado para empaquetarse como app nativa con [Capacitor](https://capacitorjs.com):

```bash
cd frontend
npm run build              # genera www/
npx cap sync android        # copia www/ al proyecto nativo y sincroniza plugins
cd android
./gradlew assembleDebug     # requiere Android SDK + JDK instalados
```

El proyecto `frontend/android/` ya existe (generado con `npx cap add android`), con `appId com.cmedriver.app` y los plugins `@capacitor/app`, `@capacitor/haptics`, `@capacitor/keyboard`, `@capacitor/status-bar`.

**Estado real de esto en el entorno de desarrollo usado para este proyecto**: `npx cap add android` y la sincronización funcionaron correctamente (SDK de Android y JDK 21 están instalados), pero el build de Gradle (`assembleDebug`) falló en esta máquina específica con `java.io.IOException: Unable to establish loopback connection` — un problema conocido de compatibilidad entre el NIO de JDK 21 y sockets de dominio Unix en ciertas configuraciones de Windows, no relacionado con el código del proyecto. En un computador sin esa restricción (o abriendo `frontend/android/` directamente en Android Studio, que maneja el daemon de Gradle de otra forma) el mismo comando debería generar un APK instalable sin cambios adicionales. iOS requiere además una máquina macOS con Xcode — no evaluado en este entorno (Windows).

## 5. Datos iniciales (usuarios de prueba)
Ver tabla completa en el [README.md](../README.md) principal. Resumen: `admin/admin1234`, `alistador1/alistador1234`, `motorizado1/motorizado1234`, `cliente1/cliente1234`.

**Importante:** estos usuarios y contraseñas son solo para demo/desarrollo. Antes de cualquier despliegue real, se deben crear usuarios nuevos con contraseñas seguras y desactivar o eliminar los usuarios de demo.

## 6. Despliegue en producción (recomendaciones)

Este MVP corre en modo desarrollo (`runserver` de Django + servidor de desarrollo de Angular). Para un despliegue real:

1. **Backend**: servir con un servidor WSGI de producción (ej. `gunicorn` o `waitress`) detrás de un proxy (Nginx). Cambiar `DEBUG=False`, definir `ALLOWED_HOSTS`, migrar a PostgreSQL, y servir `media/` desde almacenamiento persistente (o un bucket tipo S3).
2. **Frontend**: generar el build (`npm run build`) y servir los archivos estáticos resultantes desde el mismo Nginx o un CDN.
3. **Variables sensibles**: mover `SECRET_KEY` y credenciales de base de datos a variables de entorno (no versionarlas en el repositorio).
4. **HTTPS**: obligatorio en producción, tanto para la API como para el frontend (los navegadores restringen geolocalización y cámara en sitios sin HTTPS).
5. **Contenedores (opcional, recomendado a futuro)**: empaquetar backend y frontend en imágenes Docker separadas + un `docker-compose.yml` con PostgreSQL, para reproducibilidad del entorno. No incluido en el MVP por tiempo, pero es el siguiente paso natural (ver [07-roadmap-futuro.md](07-roadmap-futuro.md)).

## 7. Respaldo y mantenimiento
- **Backup de base de datos**: en SQLite, respaldar el archivo `backend/db.sqlite3` periódicamente. En PostgreSQL, usar `pg_dump` programado.
- **Backup de evidencias**: la carpeta `backend/media/evidencias/` contiene las fotos y firmas — debe respaldarse junto con la base de datos (o migrarse a almacenamiento en la nube en producción).
- **Migraciones**: cualquier cambio a los modelos requiere `python manage.py makemigrations` seguido de `python manage.py migrate` en el entorno destino.

## 8. Problemas comunes (troubleshooting)
| Síntoma | Causa probable | Solución |
|---|---|---|
| Frontend no puede llamar a la API (error CORS) | El origen del frontend no está en `CORS_ALLOWED_ORIGINS` | Agregar el origen real en `settings.py` |
| Login funciona pero las peticiones siguientes devuelven 401 | Token expirado o no se está enviando el header `Authorization` | Verificar el interceptor HTTP del frontend y la duración configurada en `SIMPLE_JWT` |
| La cámara o el GPS no funcionan en el celular | El sitio no está en HTTPS (ni es `localhost`) | Los navegadores móviles exigen HTTPS para geolocalización/cámara fuera de `localhost` |
| `python` no se reconoce en Windows | Alias de Microsoft Store interceptando el comando | Usar el launcher `py` en su lugar (`py -m venv .venv`, etc.) |
| El WebSocket no conecta (`ws://...` falla) | Token vencido/ausente en la query string, o el servidor no cargó Channels | Verificar `?token=` en la URL del socket y que `channels`/`daphne` estén en `INSTALLED_APPS`; el frontend cae a polling automáticamente si esto pasa (RNF-10) |
| El correo de reset de contraseña "no llega" | Backend de consola en desarrollo: el correo se imprime en el log del servidor, no se envía de verdad | Revisar la consola donde corre `runserver`; para correo real, configurar `MAILERS` con un proveedor SMTP |
| `assembleDebug` de Gradle falla con `Unable to establish loopback connection` | Incompatibilidad JDK 21 / sockets en esa máquina Windows (ver sección 4) | Probar en Android Studio, otra máquina, o una versión de JDK distinta (ej. JDK 17) |
