# VitaliLab Profesional

VitaliLab es una aplicación web educativa para registrar hábitos saludables, consultar progreso y presentar indicadores de bienestar con contexto. Esta reconstrucción transforma el prototipo original en un monolito modular Flask, con seguridad, migraciones, pruebas, experiencia responsive y despliegue reproducible.

## Estado verificable

| Componente | Resultado |
|---|---|
| Aplicación y backend | Implementados en `feat/reconstruccion-profesional` |
| Modelo de datos | 7 tablas, 2 migraciones Alembic, integridad e índices |
| Seguridad | Hash scrypt, CSRF, autorización, bloqueo temporal, rate limits y cabeceras |
| Frontend | Responsive, navegación móvil, formularios accesibles y estados controlados |
| Calidad local | 24 pruebas aprobadas, 90,41 % de cobertura, Ruff sin hallazgos |
| Base vacía | `flask db upgrade` y `flask db check` aprobados |
| Staging | Configuración declarativa lista; despliegue remoto pendiente de ejecutar/aprobar |
| Production | Congelada; no se ha modificado |

La calificación final no se declara como 100/100 hasta validar CI, PostgreSQL, Staging, backup/restauración y aceptación del propietario. Consulte [Informe QA y readiness](docs/13_INFORME_QA_Y_READINESS.md).

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
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
flask --app wsgi:app db upgrade
flask --app wsgi:app seed-habits
flask --app wsgi:app run
```

Antes de iniciar, ajuste `.env` para una base local. El archivo está ignorado por Git y nunca debe contener valores que se copien a documentación o capturas.

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

El CI repite estas comprobaciones, ejecuta las migraciones contra PostgreSQL 18 y construye la imagen de producción.

## Ambientes y ramas

```text
feature/fix/docs -> PR -> staging -> Render Staging -> aprobación -> main -> Production
```

- `staging`: integración y demostración con datos ficticios.
- `main`: candidato autorizado a Production.
- Production no recibe cambios automáticos desde esta rama de trabajo.

## Documentación

La fuente de verdad está en [docs/README.md](docs/README.md). Incluye arquitectura, diccionario DBA, backend, UX, seguridad, Git, Render, QA, operación, bitácora y guía de sustentación.

## Alcance sanitario y privacidad

VitaliLab es una herramienta educativa y no sustituye orientación médica. Las medidas son opcionales y no se incluyen en logs ni auditoría. Antes de Production, la institución debe aprobar la política de tratamiento, especialmente si participarán menores de edad.
