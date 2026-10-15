# Referencia técnica derivada del código

Este anexo se genera desde los modelos y las rutas de la aplicación. No consulta la base publicada ni exporta datos personales.

Tipos, nulabilidad y relaciones corresponden a los modelos versionados; la coincidencia con el esquema se verifica mediante migraciones y db check.

## Cómo leer el diccionario

PK identifica una fila; FK exige una fila relacionada; NULL indica si un valor puede faltar. Una restricción única impide repetir una combinación. Los campos created_at y updated_at conservan creación y última modificación en UTC.

Los nombres que terminan en _id son referencias, _on son fechas de negocio y _at son instantes. active controla disponibilidad; status representa un estado del proceso. Consulta el manual integral para las reglas de permisos y el significado de cada entidad.

## Tabla announcements

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `author_user_id` | INTEGER | No | FK → users.id |
| `title` | VARCHAR(150) | No | — |
| `body` | TEXT | No | — |
| `status` | VARCHAR(20) | No | — |
| `published_at` | DATETIME | Sí | — |
| `created_at` | DATETIME | No | — |
| `updated_at` | DATETIME | No | — |

Combinaciones únicas:
No adicionales a las claves indicadas.

Restricciones de valores:
- `status IN ('draft', 'published', 'archived')`

Índices declarados:
- `ix_announcements_author_user_id (author_user_id)`
- `ix_announcements_published_at (published_at)`
- `ix_announcements_status (status)`
- `ix_announcements_status_published_at (status, published_at)`

## Tabla audit_events

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `actor_user_id` | INTEGER | Sí | FK → users.id |
| `action` | VARCHAR(80) | No | — |
| `entity_type` | VARCHAR(50) | No | — |
| `entity_id` | VARCHAR(80) | Sí | — |
| `metadata_redacted` | JSON | No | — |
| `created_at` | DATETIME | No | — |

Combinaciones únicas:
No adicionales a las claves indicadas.

Restricciones de valores:
No adicionales a las claves indicadas.

Índices declarados:
- `ix_audit_events_action (action)`
- `ix_audit_events_actor_user_id (actor_user_id)`
- `ix_audit_events_created_at (created_at)`

## Tabla daily_checkins

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `user_id` | INTEGER | No | FK → users.id |
| `checked_on` | DATE | No | — |
| `energy` | INTEGER | No | — |
| `focus` | INTEGER | No | — |
| `created_at` | DATETIME | No | — |
| `updated_at` | DATETIME | No | — |

Combinaciones únicas:
- `user_id, checked_on`

Restricciones de valores:
- `energy BETWEEN 1 AND 5`
- `focus BETWEEN 1 AND 5`

Índices declarados:
No adicionales a las claves indicadas.

## Tabla habit_entries

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `user_id` | INTEGER | No | FK → users.id |
| `habit_id` | INTEGER | No | FK → habits.id |
| `completed_on` | DATE | No | — |
| `created_at` | DATETIME | No | — |

Combinaciones únicas:
- `user_id, habit_id, completed_on`

Restricciones de valores:
No adicionales a las claves indicadas.

Índices declarados:
- `ix_habit_entries_completed_on (completed_on)`
- `ix_habit_entries_habit_id (habit_id)`
- `ix_habit_entries_user_completed_on (user_id, completed_on)`
- `ix_habit_entries_user_id (user_id)`

## Tabla habits

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `code` | VARCHAR(50) | No | — |
| `name` | VARCHAR(100) | No | — |
| `description` | VARCHAR(280) | No | — |
| `category` | VARCHAR(50) | No | — |
| `icon` | VARCHAR(20) | No | — |
| `points` | INTEGER | No | — |
| `active` | BOOLEAN | No | — |
| `sort_order` | INTEGER | No | — |
| `created_at` | DATETIME | No | — |
| `updated_at` | DATETIME | No | — |

Combinaciones únicas:
- `code`

Restricciones de valores:
- `points BETWEEN 1 AND 100`

Índices declarados:
No adicionales a las claves indicadas.

## Tabla health_measurements

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `user_id` | INTEGER | No | FK → users.id |
| `weight_kg` | NUMERIC(5, 2) | No | — |
| `height_cm` | NUMERIC(5, 2) | No | — |
| `bmi_snapshot` | NUMERIC(5, 2) | No | — |
| `age_months` | INTEGER | Sí | — |
| `reference_sex` | VARCHAR(12) | Sí | — |
| `reference_source` | VARCHAR(32) | Sí | — |
| `growth_percentile` | NUMERIC(5, 2) | Sí | — |
| `measured_on` | DATE | No | — |
| `created_at` | DATETIME | No | — |

Combinaciones únicas:
No adicionales a las claves indicadas.

Restricciones de valores:
- `bmi_snapshot BETWEEN 5 AND 100`
- `growth_percentile IS NULL OR growth_percentile BETWEEN 0 AND 100`
- `height_cm BETWEEN 50 AND 250`
- `reference_sex IS NULL OR reference_sex IN ('male', 'female')`
- `weight_kg BETWEEN 10 AND 500`

Índices declarados:
- `ix_health_measurements_measured_on (measured_on)`
- `ix_health_measurements_user_id (user_id)`
- `ix_health_measurements_user_measured_on (user_id, measured_on)`

## Tabla personal_routines

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `user_id` | INTEGER | No | FK → users.id |
| `name` | VARCHAR(80) | No | — |
| `description` | VARCHAR(500) | No | — |
| `goal` | VARCHAR(12) | No | — |
| `active` | BOOLEAN | No | — |
| `revision` | INTEGER | No | — |
| `created_at` | DATETIME | No | — |
| `updated_at` | DATETIME | No | — |

Combinaciones únicas:
No adicionales a las claves indicadas.

Restricciones de valores:
- `goal IN ('center', 'energy', 'strength')`
- `revision >= 1`

Índices declarados:
- `ix_personal_routines_user_active (user_id, active)`

## Tabla routine_completions

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `user_id` | INTEGER | No | FK → users.id |
| `routine_slug` | VARCHAR(60) | No | — |
| `habit_id` | INTEGER | No | FK → habits.id |
| `completed_on` | DATE | No | — |
| `created_at` | DATETIME | No | — |

Combinaciones únicas:
- `user_id, routine_slug, completed_on`

Restricciones de valores:
No adicionales a las claves indicadas.

Índices declarados:
- `ix_routine_completions_habit_id (habit_id)`
- `ix_routine_completions_user_id (user_id)`

## Tabla routine_exercises

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `routine_id` | INTEGER | No | FK → personal_routines.id |
| `position` | INTEGER | No | — |
| `name` | VARCHAR(80) | No | — |
| `sets` | INTEGER | No | — |
| `repetitions` | INTEGER | Sí | — |
| `duration_seconds` | INTEGER | Sí | — |
| `rest_seconds` | INTEGER | No | — |
| `instructions` | VARCHAR(280) | No | — |
| `visual` | VARCHAR(12) | No | — |

Combinaciones únicas:
- `routine_id, position`

Restricciones de valores:
- `duration_seconds IS NULL OR duration_seconds BETWEEN 5 AND 3600`
- `position BETWEEN 0 AND 11`
- `repetitions IS NOT NULL OR duration_seconds IS NOT NULL`
- `repetitions IS NULL OR repetitions BETWEEN 1 AND 200`
- `rest_seconds BETWEEN 0 AND 600`
- `sets BETWEEN 1 AND 20`
- `visual IN ('posture', 'march', 'palms', 'shoulders', 'wall', 'walk', 'breathing', 'custom')`

Índices declarados:
No adicionales a las claves indicadas.

## Tabla school_enrollment_requests

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `user_id` | INTEGER | No | FK → users.id |
| `school_name` | VARCHAR(160) | No | — |
| `group_name` | VARCHAR(80) | No | — |
| `requested_role` | VARCHAR(12) | No | — |
| `status` | VARCHAR(12) | No | — |
| `reviewed_at` | DATETIME | Sí | — |
| `reviewed_by_user_id` | INTEGER | Sí | FK → users.id |
| `created_at` | DATETIME | No | — |
| `updated_at` | DATETIME | No | — |

Combinaciones únicas:
- `user_id`

Restricciones de valores:
- `requested_role IN ('student', 'teacher')`
- `status IN ('pending', 'resolved', 'rejected', 'cancelled')`

Índices declarados:
- `ix_enrollment_status_created (status, created_at)`
- `ix_school_enrollment_requests_reviewed_by_user_id (reviewed_by_user_id)`

## Tabla school_groups

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `school_id` | INTEGER | No | FK → schools.id |
| `name` | VARCHAR(80) | No | — |
| `academic_year` | INTEGER | No | — |
| `active` | BOOLEAN | No | — |
| `created_at` | DATETIME | No | — |
| `updated_at` | DATETIME | No | — |

Combinaciones únicas:
- `id, school_id`
- `school_id, academic_year, name`

Restricciones de valores:
- `academic_year BETWEEN 2020 AND 2100`

Índices declarados:
- `ix_school_groups_school_id (school_id)`

## Tabla school_memberships

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `user_id` | INTEGER | No | FK → users.id |
| `school_id` | INTEGER | No | FK → schools.id, school_groups.school_id |
| `group_id` | INTEGER | Sí | FK → school_groups.id |
| `requested_role` | VARCHAR(12) | No | — |
| `status` | VARCHAR(12) | No | — |
| `allow_aggregate` | BOOLEAN | No | — |
| `aggregate_since` | DATETIME | Sí | — |
| `reviewed_at` | DATETIME | Sí | — |
| `reviewed_by_user_id` | INTEGER | Sí | FK → users.id |
| `authorization_confirmed` | BOOLEAN | No | — |
| `created_at` | DATETIME | No | — |
| `updated_at` | DATETIME | No | — |

Combinaciones únicas:
- `id, school_id`
- `user_id`

Restricciones de valores:
- `requested_role IN ('student', 'teacher')`
- `status IN ('pending', 'approved', 'rejected', 'revoked')`

Índices declarados:
- `ix_membership_group_status (group_id, status)`
- `ix_school_memberships_reviewed_by_user_id (reviewed_by_user_id)`
- `ix_school_memberships_school_id (school_id)`

## Tabla schools

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `code` | VARCHAR(60) | No | — |
| `name` | VARCHAR(160) | No | — |
| `active` | BOOLEAN | No | — |
| `created_at` | DATETIME | No | — |
| `updated_at` | DATETIME | No | — |

Combinaciones únicas:
- `code`

Restricciones de valores:
No adicionales a las claves indicadas.

Índices declarados:
No adicionales a las claves indicadas.

## Tabla teacher_group_assignments

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `membership_id` | INTEGER | No | FK → school_memberships.id |
| `school_id` | INTEGER | No | FK → school_groups.school_id, school_memberships.school_id |
| `group_id` | INTEGER | No | FK → school_groups.id |
| `created_at` | DATETIME | No | — |
| `updated_at` | DATETIME | No | — |

Combinaciones únicas:
- `membership_id, group_id`

Restricciones de valores:
No adicionales a las claves indicadas.

Índices declarados:
- `ix_assignment_group (group_id)`

## Tabla user_goals

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `user_id` | INTEGER | No | FK → users.id |
| `habit_id` | INTEGER | No | FK → habits.id |
| `target_days` | INTEGER | No | — |
| `created_at` | DATETIME | No | — |
| `updated_at` | DATETIME | No | — |

Combinaciones únicas:
- `user_id, habit_id`

Restricciones de valores:
- `target_days BETWEEN 1 AND 7`

Índices declarados:
No adicionales a las claves indicadas.

## Tabla user_profiles

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `user_id` | INTEGER | No | PK; FK → users.id |
| `display_name` | VARCHAR(80) | No | — |
| `birth_date` | DATE | Sí | — |
| `usage_mode` | VARCHAR(20) | No | — |
| `institution_name` | VARCHAR(160) | Sí | — |
| `reference_sex` | VARCHAR(12) | No | — |
| `movement_goal` | VARCHAR(12) | No | — |
| `movement_preference` | VARCHAR(12) | No | — |
| `personalization_completed_at` | DATETIME | Sí | — |
| `measurement_consent_at` | DATETIME | Sí | — |
| `grade` | VARCHAR(80) | Sí | — |
| `timezone` | VARCHAR(50) | No | — |
| `privacy_version` | VARCHAR(20) | No | — |
| `privacy_accepted_at` | DATETIME | No | — |
| `created_at` | DATETIME | No | — |
| `updated_at` | DATETIME | No | — |

Combinaciones únicas:
No adicionales a las claves indicadas.

Restricciones de valores:
- `movement_goal IN ('center', 'energy', 'strength')`
- `movement_preference IN ('adaptable', 'seated', 'supported', 'standing')`
- `reference_sex IN ('unspecified', 'female', 'male')`
- `usage_mode IN ('personal', 'institutional')`

Índices declarados:
No adicionales a las claves indicadas.

## Tabla users

| Campo | Tipo | Permite NULL | Clave y relación |
|---|---|---|---|
| `id` | INTEGER | No | PK |
| `email` | VARCHAR(254) | No | — |
| `password_hash` | VARCHAR(255) | No | — |
| `role` | VARCHAR(20) | No | — |
| `status` | VARCHAR(20) | No | — |
| `last_login_at` | DATETIME | Sí | — |
| `failed_login_count` | INTEGER | No | — |
| `locked_until` | DATETIME | Sí | — |
| `created_at` | DATETIME | No | — |
| `updated_at` | DATETIME | No | — |

Combinaciones únicas:
No adicionales a las claves indicadas.

Restricciones de valores:
- `role IN ('user', 'admin')`
- `status IN ('active', 'inactive')`

Índices declarados:
- `ix_users_email (email)`

## Mapa de rutas

Este mapa muestra direcciones y funciones reales. No representa una API pública contractual ni concede acceso: los decoradores y servicios comprueban sesión, rol, propietario y colegio según el caso. Toda acción POST requiere CSRF.

| Ruta | Método | Función | Archivo |
|---|---|---|---|
| `/` | GET | `main.home` | `app/main/routes.py` |
| `/acceso/ingresar` | GET, POST | `auth.login` | `app/auth/routes.py` |
| `/acceso/recuperar` | GET, POST | `auth.forgot_password` | `app/auth/routes.py` |
| `/acceso/registro` | GET, POST | `auth.register` | `app/auth/routes.py` |
| `/acceso/restablecer/<token>` | GET, POST | `auth.reset_password` | `app/auth/routes.py` |
| `/acceso/salir` | POST | `auth.logout` | `app/auth/routes.py` |
| `/admin/` | GET | `admin.dashboard` | `app/admin/routes.py` |
| `/admin/anuncios` | POST | `admin.create_announcement` | `app/admin/routes.py` |
| `/admin/anuncios/<int:announcement_id>/archivar` | POST | `admin.archive_announcement` | `app/admin/routes.py` |
| `/admin/anuncios/<int:announcement_id>/publicar` | POST | `admin.publish_announcement` | `app/admin/routes.py` |
| `/admin/colegios/` | GET | `school.admin_index` | `app/school/routes.py` |
| `/admin/colegios/<kind>/<int:item_id>/estado` | POST | `school.toggle_status` | `app/school/routes.py` |
| `/admin/colegios/altas/<int:request_id>` | GET, POST | `school.review_enrollment` | `app/school/routes.py` |
| `/admin/colegios/asignaciones` | POST | `school.assign` | `app/school/routes.py` |
| `/admin/colegios/asignaciones/<int:assignment_id>/retirar` | POST | `school.remove_assignment` | `app/school/routes.py` |
| `/admin/colegios/crear` | POST | `school.create_school` | `app/school/routes.py` |
| `/admin/colegios/grupos` | POST | `school.create_group` | `app/school/routes.py` |
| `/admin/colegios/solicitudes/<int:membership_id>` | GET, POST | `school.review` | `app/school/routes.py` |
| `/bitacora/` | GET, POST | `wellness.checkin` | `app/wellness/routes.py` |
| `/colegios/` | GET, POST | `school.account` | `app/school/routes.py` |
| `/colegios/estadisticas` | POST | `school.consent` | `app/school/routes.py` |
| `/colegios/retirar` | POST | `school.withdraw` | `app/school/routes.py` |
| `/contenido/<slug>` | GET | `main.content` | `app/main/routes.py` |
| `/docentes/` | GET | `school.teacher` | `app/school/routes.py` |
| `/docentes/grupos/<int:group_id>` | GET | `school.group_report` | `app/school/routes.py` |
| `/docentes/rutinas/<slug>/proyectar` | GET | `school.project_routine` | `app/school/routes.py` |
| `/habitos/` | GET | `habits.index` | `app/habits/routes.py` |
| `/habitos/<int:habit_id>/completar` | POST | `habits.complete` | `app/habits/routes.py` |
| `/health` | GET | `main.health` | `app/main/routes.py` |
| `/metas/` | GET, POST | `wellness.goals` | `app/wellness/routes.py` |
| `/metas/<int:goal_id>/eliminar` | POST | `wellness.delete_goal` | `app/wellness/routes.py` |
| `/mis-rutinas/<int:routine_id>/` | GET | `wellness.personal_routine` | `app/wellness/routes.py` |
| `/mis-rutinas/<int:routine_id>/archivar` | POST | `wellness.archive_routine` | `app/wellness/routes.py` |
| `/mis-rutinas/<int:routine_id>/editar` | GET, POST | `wellness.edit_personal_routine` | `app/wellness/routes.py` |
| `/mis-rutinas/<int:routine_id>/registrar` | POST | `wellness.complete_personal_routine` | `app/wellness/routes.py` |
| `/mis-rutinas/nueva` | GET, POST | `wellness.edit_personal_routine` | `app/wellness/routes.py` |
| `/panel` | GET | `main.dashboard` | `app/main/routes.py` |
| `/perfil/` | GET, POST | `profile.edit` | `app/profile/routes.py` |
| `/perfil/inicio/medicion` | GET, POST | `profile.setup_measurement` | `app/profile/routes.py` |
| `/perfil/inicio/objetivo` | GET, POST | `profile.setup_goal` | `app/profile/routes.py` |
| `/perfil/seguimiento` | GET | `profile.tracking` | `app/profile/routes.py` |
| `/privacidad` | GET | `main.privacy` | `app/main/routes.py` |
| `/progreso/` | GET | `wellness.progress` | `app/wellness/routes.py` |
| `/ready` | GET | `main.ready` | `app/main/routes.py` |
| `/rutinas/` | GET | `wellness.library` | `app/wellness/routes.py` |
| `/rutinas/<slug>/` | GET | `wellness.routine` | `app/wellness/routes.py` |
| `/rutinas/<slug>/registrar` | POST | `wellness.complete_routine` | `app/wellness/routes.py` |
