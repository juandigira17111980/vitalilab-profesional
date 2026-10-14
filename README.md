# VitaliLab Profesional

VitaliLab es una aplicación web educativa para registrar hábitos saludables, consultar progreso y presentar indicadores de bienestar con contexto. Esta reconstrucción transforma el prototipo original en un monolito modular Flask, con seguridad, migraciones, pruebas, experiencia responsive y despliegue reproducible.

## Estado verificable

| Componente | Resultado |
|---|---|
| Aplicación y backend | Integrados en `staging` mediante PR #2 |
| Modelo de datos | 7 tablas, 2 migraciones Alembic, integridad e índices |
| Seguridad | Hash scrypt, CSRF, autorización, bloqueo temporal, rate limits y cabeceras |
| Frontend | Responsive, navegación móvil, formularios accesibles y estados controlados |
| Calidad | 28 pruebas y 90,67 % local; CI PostgreSQL, seguridad y Docker aprobado |
| Base de datos | Migración, deriva, backup y restauración aislada aprobados en PostgreSQL 18 CI |
| Staging | Copia académica en NexoStack; evidencia en docs/18 |
| Production | Congelada; no se ha modificado |

La copia es un laboratorio, no un reemplazo productivo de Render. SMTP real, accesibilidad formal, alertas personales, operación offsite y privacidad institucional siguen requiriendo validación. No se declara una calificación 100/100 por publicar contenedores. Consulte [Informe QA y readiness](docs/13_INFORME_QA_Y_READINESS.md) y [evidencia NexoStack](docs/18_NEXOSTACK_OPERACION_Y_ACCESOS.md).

## Funciones

- Registro, login, logout, bloqueo temporal y recuperación de contraseña.
- Perfil propio y medidas opcionales con IMC educativo.
- Catálogo de hábitos, cumplimiento diario idempotente, puntos, nivel y racha.
- Dashboard personal de siete días.
- Contenidos educativos y política de privacidad.
- Panel administrativo para comunicados y auditoría sin datos sensibles.
- Health check de proceso (`/health`) y readiness de base de datos (`/ready`).

## Arquitectura

```text
app/
├── auth/       registro, acceso, cierre y recuperación
├── profile/    perfil propio y medidas
├── habits/     cumplimiento de hábitos
├── admin/      comunicados y eventos de auditoría
├── main/       inicio, contenidos, panel y health checks
├── services/   progreso, correo y auditoría
├── templates/  interfaz Jinja reutilizable
└── static/     sistema visual y JavaScript progresivo
migrations/       historial Alembic
tests/            pruebas unitarias e integración
docs/             documentación técnica y académica
```

PostgreSQL es obligatorio en Staging y Production. SQLite se admite únicamente para desarrollo y pruebas locales.

## Inicio local con Python

Requiere Python 3.13.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
$env:APP_ENV = "development"
$env:DATABASE_URL = "sqlite:///vitalilab-aprendizaje.db"
$env:SECRET_KEY = (.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))")
$env:SESSION_COOKIE_SECURE = "false"
.\.venv\Scripts\python.exe -m flask --app wsgi:app db upgrade
.\.venv\Scripts\python.exe -m flask --app wsgi:app seed-habits
.\.venv\Scripts\python.exe -m flask --app wsgi:app run
```

Estas variables deben establecerse en la misma terminal del arranque. `.env.example` es una referencia: copiarla no instala PostgreSQL ni garantiza cargar `.env`, porque `python-dotenv` no está declarado. Para la práctica inicial se usa SQLite exclusivo; en ambientes compartidos se exige PostgreSQL.

## Aprender y sustentar

Si estás empezando, lee primero [VitaliLab explicado desde cero](docs/15_MANUAL_DE_APRENDIZAJE_Y_SUSTENTACION.md). Incluye fundamentos, montaje Windows, las razones del modelo de datos, recorridos del código, ocho laboratorios y preguntas de sustentación. Después consulta los capítulos técnicos por área.

## Copia de práctica en NexoStack

[Abrir VitaliLab de práctica](https://vitalilab.lab.nexostack.app). Usa web no root, PostgreSQL 18 propia con TLS, volumen persistente y recursos limitados. El montaje está en `deploy/nexostack`, separado de Mercanta, Murano, Krono 57 y el Render histórico.

Juan y Emanuel tienen cuentas individuales de aplicación y llaves distintas para cinco operaciones de gestión: estado, salud, reinicio de esta web, backup y eventos. No se entrega acceso administrativo general al VPS o a Coolify. Consulta [publicación](docs/16_PUBLICACION_DE_LA_COPIA_DE_PRACTICA.md) y [operación y accesos](docs/18_NEXOSTACK_OPERACION_Y_ACCESOS.md). Los secretos no se incluyen en el repositorio ni en el material para estudiantes.

La adaptación `vercel.json` se conserva como opción, no como proveedor activo. `render.yaml` sigue describiendo una alternativa de prueba; no se modifica la producción actual.

## Inicio local con Docker

```text
docker compose up --build
```

La web queda disponible solo en `http://127.0.0.1:5000`; PostgreSQL no publica su puerto al host. Docker no estaba instalado en el equipo de auditoría, por lo que la construcción del contenedor se valida en GitHub Actions.

## Administración y migraciones

```powershell
flask --app wsgi:app create-admin
flask --app wsgi:app db upgrade
flask --app wsgi:app db check
flask --app wsgi:app seed-habits
```

El alta administrativa valida correo y aplica la misma política fuerte de contraseña. El seed es idempotente.

## Calidad

```powershell
ruff check app tests wsgi.py migrations/versions
ruff format --check app tests wsgi.py migrations/versions
pytest
```

El CI repite estas comprobaciones, ejecuta análisis estático de seguridad, migra PostgreSQL 18, prueba un backup/restore aislado y construye la imagen de producción.

## Ambientes y ramas

```text
feature/fix/docs -> PR -> staging -> NexoStack laboratorio -> aprobación -> main -> Production
```

- `staging`: integración y demostración con datos ficticios.
- `main`: candidato autorizado a Production.
- Production no recibe cambios automáticos desde esta rama de trabajo.

## Documentación

La fuente de verdad está en [docs/README.md](docs/README.md). Incluye arquitectura, diccionario DBA, backend, UX, seguridad, Git, Render, QA, operación, bitácora y guía de sustentación.

## Alcance sanitario y privacidad

VitaliLab es una herramienta educativa y no sustituye orientación médica. Las medidas son opcionales y no se incluyen en logs ni auditoría. Antes de Production, la institución debe aprobar la política de tratamiento, especialmente si participarán menores de edad.
