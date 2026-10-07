# Modelo de datos — CMEDriver

![Modelo entidad-relación](diagrams/img/er.png)

Fuente editable (Mermaid): [diagrams/src/er.mmd](diagrams/src/er.mmd)

<details>
<summary>Ver código Mermaid</summary>

```mermaid
erDiagram
    USUARIO {
        int id PK
        string username
        string password_hash
        string nombre
        string rol "ADMIN | ALISTADOR | MOTORIZADO | CLIENTE"
        string telefono
        boolean activo
    }

    COBERTURA {
        int id PK
        string zona
        int leadtime_dias
        string dias_disponibles "ej: LUN,MAR,MIE"
        time hora_inicio
        time hora_fin
    }

    PRODUCTO {
        int id PK
        string sku
        string nombre
        string descripcion
        decimal precio
        int stock
        string centro_mensajeria
        boolean disponible_chatbot
    }

    RUTA {
        int id PK
        int motorizado_id FK
        date fecha
        string estado "PLANEADA | EN_CURSO | FINALIZADA"
    }

    SERVICIO {
        int id PK
        string tipo "ENTREGA | RECOLECCION"
        int cliente_id FK
        int producto_id FK
        string zona
        string direccion_origen
        string direccion_destino
        date fecha_agenda
        string estado "CREADO | ASIGNADO | RECIBIDO_CENTRO | EN_TRANSITO | ENTREGADO | RECOLECTADO | NOVEDAD | DEVUELTO"
        int ruta_id FK
        datetime creado_en
    }

    NOVEDAD {
        int id PK
        int servicio_id FK
        string tipo
        string detalle
        string accion "DEVOLVER_A_CENTRO | REINTENTAR"
        datetime creado_en
    }

    EVIDENCIA {
        int id PK
        int servicio_id FK
        string foto_url
        string firma_url
        datetime capturado_en
    }

    POSICION_GPS {
        int id PK
        int servicio_id FK
        int motorizado_id FK
        decimal lat
        decimal lng
        datetime timestamp
    }

    MENSAJE_CHAT {
        int id PK
        int servicio_id FK
        int autor_id FK
        string texto
        datetime enviado_en
    }

    USUARIO ||--o{ RUTA : "conduce (motorizado)"
    USUARIO ||--o{ SERVICIO : "solicita (cliente)"
    RUTA ||--o{ SERVICIO : "agrupa"
    SERVICIO ||--o| NOVEDAD : "puede tener"
    SERVICIO ||--o| EVIDENCIA : "genera"
    SERVICIO ||--o{ POSICION_GPS : "trackea"
    SERVICIO ||--o{ MENSAJE_CHAT : "conversa"
    PRODUCTO ||--o{ SERVICIO : "referencia"
    COBERTURA ||--o{ SERVICIO : "valida zona/leadtime"
```
</details>

## Notas
- `SERVICIO.producto_id` se modela 1-a-1 simplificado para el MVP; una evolución natural es una tabla intermedia `SERVICIO_PRODUCTO` para soportar múltiples productos por servicio (documentado en el roadmap).
- `EVIDENCIA` solo es obligatoria cuando `SERVICIO.tipo = RECOLECCION`.
- `COBERTURA` se usa tanto para validar la fecha de agenda que asigna el administrador como para calcular las fechas disponibles que ve el cliente al planificar su propia recolección.
