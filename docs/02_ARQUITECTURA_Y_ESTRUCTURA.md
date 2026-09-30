# Arquitectura y estructura

## 1. Patrón elegido

VitaliLab usa un **monolito modular con separación por dominio**. Las rutas coordinan HTTP, los formularios validan entradas, los servicios concentran reglas reutilizables, SQLAlchemy protege la persistencia y Jinja presenta datos preparados.

No se implementaron microservicios: aumentarían despliegues, fallos distribuidos, observabilidad y costos sin una necesidad proporcional.

## 2. Estructura real

```text
app/
├── __init__.py          fábrica, extensiones, blueprints y cabeceras
├── config.py            configuración y validación por ambiente
├── extensions.py        DB, Migrate, Login, CSRF y Limiter
├── models.py            entidades y restricciones del dominio
├── forms.py             validación del servidor
├── errors.py            respuestas 400/403/404/429/500
├── commands.py          seeds y alta administrativa
├── auth/routes.py       identidad y sesiones
├── profile/routes.py    perfil y medidas propias
├── habits/routes.py     catálogo y cumplimiento
├── admin/routes.py      comunicados y auditoría
├── main/routes.py       contenido, panel, health y readiness
├── services/            audit.py, email.py y progress.py
├── templates/           layout, macro y pantallas
└── static/              CSS, JS y marca SVG
migrations/versions/         historial de esquema
tests/                       auth, operación, progreso y rutas
```

## 3. Flujo: completar un hábito

```mermaid
sequenceDiagram
    actor U as Usuario
    participant V as Vista Jinja
    participant R as Ruta Flask
    participant S as Progress Service
    participant D as Base de datos
    U->>V: Marcar como cumplido
    V->>R: POST con sesión y CSRF
    R->>S: complete_habit(usuario, hábito)
    S->>D: Buscar/inserción con unicidad diaria
    alt Ya existe o carrera concurrente
        D-->>S: Existente/IntegrityError
        S-->>R: false; no suma
    else Nuevo
        S->>D: Evento de auditoría + commit
        S-->>R: true
    end
    R-->>V: Mensaje y estado recalculado
```

Puntos, racha y nivel no se almacenan como saldos mutables: se derivan de eventos verificables, reduciendo inconsistencias.

## 4. Fronteras

| Componente | Responsabilidad | Prohibido |
|---|---|---|
| Blueprint/ruta | Autenticación, coordinación y respuesta | SQL concatenado o reglas sensibles del cliente |
| Formulario | Tipo, formato, longitud y rango | Autorizar roles |
| Servicio | Regla de progreso, auditoría o correo | Renderizar HTML |
| Modelo/ORM | Relación, constraint y persistencia | Confiar en valores calculados por el navegador |
| Plantilla | Presentación semántica | Consultar DB |
| Configuración | Diferencias por ambiente | Secretos versionados |

## 5. Contratos de arranque

- `create_app(test_config=None)` no crea ni elimina tablas.
- `wsgi:app` es el punto de entrada para Gunicorn.
- `flask db upgrade` aplica el esquema.
- `flask seed-habits` sincroniza cuatro hábitos idempotentes.
- `GET /health` prueba el proceso.
- `GET /ready` ejecuta `SELECT 1` y devuelve 503 si la DB no responde.

## 6. Configuración

`APP_ENV=staging|production` impide arrancar con el secreto de desarrollo o SQLite. Las cookies seguras y HSTS se activan en ambientes HTTPS. `DATABASE_URL` antiguo con `postgres://` se normaliza al driver Psycopg 3.

## 7. Escalabilidad deliberada

El catálogo y los comunicados son pequeños. Los historiales se filtran e indexan por usuario/fecha. Staging usa un worker y cuatro threads para mantener coherente el rate limit en memoria. Si se escala a varios procesos/instancias, `RATELIMIT_STORAGE_URI` debe apuntar a Redis compartido.

## 8. Estado

La arquitectura está ✅ implementada y validada localmente. La topología de Staging está 🟡 declarada y pendiente de evidencia remota.
