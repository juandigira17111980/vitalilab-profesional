# Changelog

Los cambios relevantes de VitaliLab se documentan siguiendo una adaptación de Keep a Changelog.

## [Unreleased]

### Added

- Fábrica Flask y módulos de autenticación, perfil, hábitos, contenido y administración.
- Modelo SQLAlchemy normalizado y migraciones Alembic.
- Recuperación de acceso por SMTP configurable.
- Panel personal, panel administrativo, contenidos y sistema visual responsive.
- Health/readiness endpoints, contenedor no privilegiado, Compose y Render Blueprint.
- CI de calidad, PostgreSQL y construcción de contenedor.
- Suite automatizada y documentación académica/operativa.

### Security

- Contraseñas con hash scrypt.
- Protección CSRF, cookies endurecidas, CSP, HSTS condicional, anti-clickjacking y `nosniff`.
- Rate limits, bloqueo temporal y mensajes que no enumeran cuentas.
- Roles en servidor y auditoría con metadatos redactados.
- Secretos externos a Git y base PostgreSQL privada en Staging.

### Changed

- Sustitución del prototipo monolítico SQLite por un monolito modular preparado para PostgreSQL.
- Cálculo de puntos y rachas derivado de eventos diarios idempotentes.

### Fixed

- Duplicación de puntos por reenvío.
- Inconsistencias entre rutas, plantillas y modelo.
- Incompatibilidad CSRF detectada en prueba de navegador.
- Alta administrativa sin validación equivalente a la interfaz.
