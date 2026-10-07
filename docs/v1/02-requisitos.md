# Requisitos — CMEDriver

## 1. Requerimientos funcionales por rol (historias de usuario)

### Administrador
- RF-01: Como administrador, quiero crear/editar/desactivar usuarios y asignarles un rol (Admin, Alistador, Motorizado), para controlar el acceso a la plataforma.
- RF-02: Como administrador, quiero definir la matriz de cobertura (zona, leadtime en días, días/horarios de agenda disponibles), para que el sistema calcule automáticamente las fechas de agenda válidas para cada zona.
- RF-03: Como administrador, quiero ver un panel con el estado general de servicios (creados, en tránsito, entregados, con novedad), para supervisar la operación.
- RF-04: Como administrador, quiero gestionar el catálogo de productos/inventario (alta, edición, stock por centro), para mantenerlo disponible al chatbot.

### Alistador
- RF-05: Como alistador, quiero crear un servicio de mensajería (Entrega o Recolección) manualmente, indicando cliente, dirección, producto(s) y zona.
- RF-06: Como alistador, quiero que un servicio también pueda crearse vía API externa (misma validación que el formulario manual), para permitir integraciones.
- RF-07: Como alistador, quiero asignar uno o varios servicios a una ruta y a un motorizado, para organizar la operación diaria.
- RF-08: Como alistador, quiero ver el estado de cada servicio y reasignarlo si es necesario (ej. tras una novedad).

### Motorizado
- RF-09: Como motorizado, quiero ver la lista de servicios asignados a mi ruta del día, diferenciando visualmente Entrega vs Recolección.
- RF-10: Como motorizado, si el servicio es de Entrega, quiero ver que debo pasar primero por el centro de mensajería a recibir el producto antes de iniciar el tránsito hacia el cliente.
- RF-11: Como motorizado, si el servicio es de Recolección, quiero ver la dirección del cliente, y al llegar poder tomar una foto del producto y capturar la firma del cliente para cerrar el servicio.
- RF-12: Como motorizado, quiero poder marcar un servicio como "en tránsito" y luego como "entregado"/"recolectado".
- RF-13: Como motorizado, quiero poder registrar una novedad en la entrega (cliente ausente, dirección errada, rechazo, etc.) y decidir si el paquete se devuelve al centro de mensajería o se reintenta.
- RF-14: Como motorizado, quiero que mi ubicación GPS se transmita periódicamente mientras tengo un servicio en tránsito, para que el cliente y el administrador puedan verla.

### Cliente
- RF-15: Como cliente, quiero ver en un mapa la ubicación del motorizado y el estado de mi servicio en tiempo (cuasi) real.
- RF-16: Como cliente, quiero poder escribirle un mensaje al motorizado asignado a mi servicio.
- RF-17: Como cliente, quiero poder planificar una recolección yo mismo, eligiendo una fecha dentro de las disponibles según la matriz de cobertura de mi zona.
- RF-18: Como cliente, quiero interactuar con un chatbot guiado (menús) para comprar un producto del catálogo o solicitar que me recojan algo, según lo que esté parametrizado como disponible.

## 2. Requerimientos no funcionales
- RNF-01: Autenticación basada en JWT, con expiración de token y refresh.
- RNF-02: Autorización por rol (RBAC) a nivel de API — un rol no puede invocar endpoints de otro rol.
- RNF-03: La API debe estar documentada (OpenAPI/Swagger) para soportar integraciones externas.
- RNF-04: El sistema debe registrar auditoría mínima de cambios de estado de un servicio (quién, cuándo, qué estado).
- RNF-05: El frontend debe ser responsive / usable desde un navegador móvil (Ionic + Angular).
- RNF-06: El envío de posición GPS no debe requerir más de una petición cada 5-10 segundos (polling), evitando sobrecarga en el MVP.
- RNF-07: Las contraseñas deben almacenarse con hash (nunca en texto plano).
- RNF-08: El sistema debe ser modular (apps/dominios independientes) para facilitar escalar a microservicios en el futuro.

## 3. Reglas de negocio clave
- RN-01: Un servicio de tipo Entrega siempre inicia en el centro de mensajería (el motorizado debe confirmar "recibido en centro" antes de pasar a "en tránsito").
- RN-02: Un servicio de tipo Recolección siempre requiere foto + firma digital del cliente para poder cerrarse como "recolectado".
- RN-03: La fecha de agenda de una recolección solicitada por el cliente debe respetar el leadtime configurado para su zona en la matriz de cobertura.
- RN-04: Un producto solo aparece como opción en el chatbot si está marcado como `disponible_chatbot = true` y tiene stock > 0 en el centro correspondiente.
- RN-05: Una novedad siempre debe resultar en una de dos acciones: `DEVOLVER_A_CENTRO` o `REINTENTAR`; no puede quedar un servicio "colgado" sin acción.
