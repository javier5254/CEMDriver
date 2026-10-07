# Diagrama de clases — CMEDriver (v2)

> Derivado directamente de los modelos Django implementados en `backend/` (accounts, coverage, inventory, services, tracking, optimization, chatbot, payments, integrations), para que el diagrama quede consistente con el código real.

![Diagrama de clases](diagrams/img/clases.png)

Fuente editable (Mermaid): [diagrams/src/clases.mmd](diagrams/src/clases.mmd)

<details>
<summary>Ver código Mermaid</summary>

```mermaid
classDiagram
    class Usuario {
        +int id
        +string username
        +string password_hash
        +string nombre
        +string rol
        +string telefono
        +string email
        +bool is_active
        +set_password(password)
        +check_password(password)
    }

    class Cobertura {
        +int id
        +string zona
        +int leadtime_dias
        +string dias_disponibles
        +time hora_inicio
        +time hora_fin
        +dias_codigos() List~string~
    }

    class Producto {
        +int id
        +string sku
        +string nombre
        +string descripcion
        +decimal precio
        +int stock
        +string centro_mensajeria
        +bool disponible_chatbot
    }

    class Ruta {
        +int id
        +date fecha
        +string estado
    }

    class Servicio {
        +int id
        +string tipo
        +string zona
        +string direccion_origen
        +string direccion_destino
        +date fecha_agenda
        +string estado
        +datetime creado_en
        +asignarRuta(ruta)
        +recibirEnCentro()
        +iniciarTransito()
        +cerrar(foto, firma)
        +registrarNovedad(tipo, detalle, accion)
    }

    class Evidencia {
        +int id
        +file foto
        +file firma
        +datetime capturado_en
    }

    class Novedad {
        +int id
        +string tipo
        +string detalle
        +string accion
        +datetime creado_en
    }

    class MensajeChat {
        +int id
        +string texto
        +datetime enviado_en
    }

    class PosicionGPS {
        +int id
        +decimal lat
        +decimal lng
        +datetime timestamp
    }

    class ServicioProducto {
        +int id
        +int cantidad
    }

    class PuntoGeocodificado {
        +int id
        +decimal lat
        +decimal lng
        +string direccion_geocodificada
        +datetime creado_en
    }

    class Conversacion {
        +int id
        +json contexto
        +datetime creado_en
    }

    class MensajeBot {
        +int id
        +string autor
        +string texto
        +json function_call
        +datetime creado_en
    }

    class MockLLMClient {
        <<simulado>>
        +responder(historial, mensaje_nuevo) dict
    }

    class Pago {
        +int id
        +decimal monto
        +string estado
        +string proveedor
        +string referencia
        +datetime creado_en
    }

    class MockPaymentProvider {
        <<simulado>>
        +procesar(pago) Pago
    }

    class ApiKey {
        +int id
        +string nombre
        +string key_hash
        +string prefix
        +bool activa
        +datetime ultimo_uso
        +generar(nombre, actua_como)$ tuple
    }

    class WebhookEndpoint {
        +int id
        +string nombre
        +string url
        +string secret
        +string eventos
        +bool activo
        +suscrito_a(evento) bool
    }

    class WebhookDelivery {
        +int id
        +string evento
        +json payload
        +int status_code
        +bool exito
        +string error
    }

    class EstadoPago {
        <<enumeration>>
        PENDIENTE
        APROBADO
        RECHAZADO
    }

    class Rol {
        <<enumeration>>
        ADMIN
        ALISTADOR
        MOTORIZADO
        CLIENTE
    }

    class TipoServicio {
        <<enumeration>>
        ENTREGA
        RECOLECCION
    }

    class EstadoServicio {
        <<enumeration>>
        CREADO
        ASIGNADO
        RECIBIDO_CENTRO
        EN_TRANSITO
        ENTREGADO
        RECOLECTADO
        NOVEDAD
        DEVUELTO
    }

    Usuario "1" --> "1" Rol : tiene
    Usuario "1" --> "0..*" Ruta : conduce (motorizado)
    Usuario "1" --> "0..*" Servicio : solicita (cliente)
    Usuario "1" --> "0..*" MensajeChat : autor
    Usuario "1" --> "0..*" PosicionGPS : reporta (motorizado)

    Ruta "1" --> "0..*" Servicio : agrupa
    Servicio "1" --> "1" TipoServicio : tiene
    Servicio "1" --> "1" EstadoServicio : tiene
    Servicio "1" --> "0..1" Evidencia : genera
    Servicio "1" --> "0..*" Novedad : registra
    Servicio "1" --> "0..*" MensajeChat : contiene
    Servicio "1" --> "0..*" PosicionGPS : trackea
    Servicio "0..*" --> "0..1" Producto : referencia
    Servicio "0..*" --> "1" Cobertura : valida contra (zona/leadtime)
    Servicio "1" --> "0..*" ServicioProducto : tiene lineas
    Producto "1" --> "0..*" ServicioProducto : aparece en
    Servicio "1" --> "0..1" PuntoGeocodificado : cache geocoding
    Usuario "1" --> "0..*" Conversacion : conversa (cliente)
    Conversacion "1" --> "0..*" MensajeBot : contiene
    Conversacion "1" --> "1" MockLLMClient : usa
    Usuario "1" --> "0..*" Pago : paga (cliente)
    Servicio "1" --> "0..1" Pago : genera
    Pago "1" --> "1" EstadoPago : tiene
    Pago "1" --> "1" MockPaymentProvider : procesado por
    Usuario "1" --> "0..*" ApiKey : actua_como (alistador)
    WebhookEndpoint "1" --> "0..*" WebhookDelivery : registra
```
</details>

## Notas de diseño
- `Rol`, `TipoServicio`, `EstadoServicio` y `EstadoPago` están modelados como enumeraciones (`TextChoices` en Django) más que como clases independientes — se muestran aquí para documentar los valores válidos de cada campo.
- Los métodos de `Servicio` (`asignarRuta`, `recibirEnCentro`, `iniciarTransito`, `cerrar`, `registrarNovedad`) están implementados como *actions* del `ServicioViewSet` en `backend/services/views.py`, no como métodos de instancia del modelo — se documentan a nivel de clase porque representan el comportamiento/ciclo de vida del servicio, que es lo relevante para el diagrama UML.
- La relación `Servicio -> Cobertura` es una validación de negocio (zona + leadtime), no una foreign key física en la base de datos — se modela como asociación porque es una regla de negocio central (RN-03).
- `MockLLMClient` y `MockPaymentProvider` llevan el estereotipo `<<simulado>>`: son implementaciones intercambiables (RNF-13) sin credenciales externas — el diagrama documenta honestamente que no son integraciones reales todavía.
- `ApiKey.actua_como` es una asociación a `Usuario` (rol ALISTADOR), no una clase de "usuario de sistema" separada — así los permisos existentes de ALISTADOR aplican sin duplicar lógica de autorización.
