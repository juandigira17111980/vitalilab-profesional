# VitaliLab Profesional

VitaliLab reúne hábitos, metas, bitácora, seguimiento y rutinas para bienestar personal y escolar. Está construido como un monolito modular Flask, con PostgreSQL, permisos, migraciones, pruebas y despliegue reproducible. El IMC es descriptivo: no diagnostica ni prescribe ejercicios.

El [manual integral del sistema](docs/26_MANUAL_INTEGRAL_DEL_SISTEMA.md) es el punto de entrada para estudiar arquitectura, datos, backend, frontend, Git e infraestructura. La [especificación de personalización](docs/25_PERSONALIZACION_Y_RUTINAS.md) documenta esta ampliación y sus criterios de aceptación.

## Estado verificable

| Componente | Resultado |
|---|---|
| Aplicación y backend | Monolito modular con bienestar personal y módulo escolar; consultar CI y guía 23 para estado de publicación |
| Modelo de datos | 17 tablas de negocio, 6 migraciones Alembic, integridad e índices |
| Seguridad | Hash scrypt, CSRF, autorización, bloqueo temporal, rate limits y cabeceras |
| Frontend | Responsive, navegación móvil, formularios accesibles y estados controlados |
| Calidad | Suite ampliada para permisos escolares, crecimiento y XP; evidencia de este cambio en guía 23 y CI del PR |
| Base de datos | Migración, deriva, backup y restauración aislada aprobados en PostgreSQL 18 CI |
| NexoStack | Servicio aislado accesible por vitalilab.space, www y el nombre de NexoStack; comprobar SHA publicado en /health |
| Render original | Servicio separado y sin modificar por esta entrega |

La presentación profesional no certifica preparación legal, clínica ni operativa. SMTP real, evaluación formal de accesibilidad, alertas externas, recuperación fuera del VPS y condiciones institucionales requieren evidencia propia. No se declara una calificación 100/100 por publicar contenedores. Las guías históricas conservan sus resultados con fecha; esta edición se describe en el manual 26 y el informe de su entrega.

## Funciones

- Ocho hábitos, metas personales, bitácora diaria, actividad de 28 días y quince rutinas públicas con temporizador.
- Rutinas propias privadas con ejercicios, series, repeticiones, segundos, descansos y guías visuales; edición versionada y archivo sin pérdida de puntos.
- Personalización una vez: medición y resultado → objetivo y preferencia → rutinas. No se exige pesarse en cada inicio de sesión.
- Enfoque personal/institucional, colegio y grupo escritos manualmente, revisión contra catálogo verificado y asignaciones docentes del mismo colegio.
- Panel docente con reportes agregados, supresión de grupos pequeños y rutinas para proyectar sin datos individuales.
- Seguimiento anual propio, referencia de crecimiento OMS cuando procede y «Tu próximo paso» por objetivo funcional; nunca por categoría corporal.
- Registro de rutinas y hábito asociado sin duplicar XP diario, incluso con solicitudes simultáneas comprobadas en CI PostgreSQL.
- Logo SVG propio, portada de producto, navegación compacta y móvil con accesos rápidos.
- La calculadora IMC, privacidad y consentimiento permanecen activos. Guardar mediciones escolares exige una vinculación verificada y autorizada.
- [Diseño y auditoría UX](docs/19_EVOLUCION_DE_PRODUCTO_Y_AUDITORIA_UX.md) y [guía de funciones, datos y QA](docs/20_GUIA_DE_FUNCIONES_Y_QA_PREMIUM.md).
- [Guía escolar histórica](docs/23_GUIA_ESCOLAR_Y_VALIDACION.md) y [manual actual](docs/26_MANUAL_INTEGRAL_DEL_SISTEMA.md). El uso con menores necesita verificación institucional real, no solo una casilla.

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
├── school/     vinculaciones, permisos, grupos y panel docente
├── habits/     cumplimiento de hábitos
├── admin/      comunicados y eventos de auditoría
├── main/       inicio, contenidos, panel y health checks
├── services/   progreso, correo, auditoría, movimiento y reglas escolares
├── data/       parámetros oficiales OMS 2007 y procedencia
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
.\.venv\Scripts\python.exe -m flask --app wsgi:app seed-schools
.\.venv\Scripts\python.exe -m flask --app wsgi:app run
```

Estas variables deben establecerse en la misma terminal del arranque. `.env.example` es una referencia: copiarla no instala PostgreSQL ni garantiza cargar `.env`, porque `python-dotenv` no está declarado. Para la práctica inicial se usa SQLite exclusivo; en ambientes compartidos se exige PostgreSQL.

## Aprender y sustentar

Si estás empezando, lee primero [VitaliLab explicado desde cero](docs/15_MANUAL_DE_APRENDIZAJE_Y_SUSTENTACION.md). Incluye fundamentos, montaje Windows, las razones del modelo de datos, recorridos del código, ocho laboratorios y preguntas de sustentación. Después consulta los capítulos técnicos por área.

## Copia de práctica en NexoStack

[Abrir VitaliLab de práctica](https://vitalilab.lab.nexostack.app). Usa web no root, PostgreSQL 18 propia con TLS, volumen persistente y recursos limitados. El montaje está en `deploy/nexostack`, separado de Mercanta, Murano, Krono 57 y el Render histórico.

Juan y Emanuel tienen cuentas individuales de aplicación y llaves distintas para cinco operaciones de gestión: estado, salud, reinicio de esta web, backup y eventos. No se entrega acceso administrativo general al VPS o a Coolify. Consulta [publicación](docs/16_PUBLICACION_DE_LA_COPIA_DE_PRACTICA.md) y [operación y accesos](docs/18_NEXOSTACK_OPERACION_Y_ACCESOS.md). Los secretos no se incluyen en el repositorio ni en el material para estudiantes.

`deploy/nexostack/` describe el montaje actual. `render.yaml` conserva una alternativa de prueba independiente del servicio original. Se retiraron los adaptadores de alojamiento que no se utilizan; no se modifica el sitio histórico ni la infraestructura activa con esta limpieza.

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
flask --app wsgi:app seed-schools
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
