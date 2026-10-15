# Diccionario fisico completo de PostgreSQL

Extraido de catalogos PostgreSQL 18.6; revision Alembic `c842d6e190ab`. No se exportaron filas.

Los tipos y DEFAULT de este documento son los del motor, no tipos genericos del ORM. Sin DEFAULT SQL no significa sin valor en la aplicacion: Flask/SQLAlchemy aplica varios valores al insertar. SQL manual debe suministrarlos. Las fechas timestamp son sin zona horaria y el codigo usa la convencion UTC.

## announcements

Comunicados, autor y estado de publicación.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `author_user_id` | integer | No | Cuenta autora del comunicado; no se borra si hay referencias RESTRICT. |
| `title` | character varying(150) | No | Título del comunicado. |
| `body` | text | No | Contenido del comunicado, escapado al presentarlo en HTML. |
| `status` | character varying(20) | No | Estado permitido por el CHECK de esta tabla; no siempre comparte vocabulario. |
| `published_at` | timestamp without time zone | Si | Instante de publicación, si existe. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |
| `updated_at` | timestamp without time zone | No | Última modificación registrada por la aplicación, con convención UTC. |

### Defaults del motor

- `id`: `nextval('announcements_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `ck_announcements_valid_status`: `CHECK (((status)::text = ANY ((ARRAY['draft'::character varying, 'published'::character varying, 'archived'::character varying])::text[])))`
- `fk_announcements_author_user_id_users`: `FOREIGN KEY (author_user_id) REFERENCES users(id) ON DELETE RESTRICT`
- `pk_announcements`: `PRIMARY KEY (id)`

### Indices fisicos

- `CREATE INDEX ix_announcements_author_user_id ON public.announcements USING btree (author_user_id)`
- `CREATE INDEX ix_announcements_published_at ON public.announcements USING btree (published_at)`
- `CREATE INDEX ix_announcements_status ON public.announcements USING btree (status)`
- `CREATE INDEX ix_announcements_status_published_at ON public.announcements USING btree (status, published_at)`
- `CREATE UNIQUE INDEX pk_announcements ON public.announcements USING btree (id)`

## audit_events

Eventos técnicos con metadatos redactados, no un historial médico.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `actor_user_id` | integer | Si | Cuenta que originó el evento; puede quedar NULL al retirarse. |
| `action` | character varying(80) | No | Tipo de acción auditada, sin contraseñas o medidas personales. |
| `entity_type` | character varying(50) | No | Tipo lógico del objeto afectado. |
| `entity_id` | character varying(80) | Si | Identificador lógico como texto; no hay una FK polimórfica. |
| `metadata_redacted` | json | No | JSON técnico redactado; no es JSONB ni texto libre médico. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |

### Defaults del motor

- `id`: `nextval('audit_events_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `fk_audit_events_actor_user_id_users`: `FOREIGN KEY (actor_user_id) REFERENCES users(id) ON DELETE SET NULL`
- `pk_audit_events`: `PRIMARY KEY (id)`

### Indices fisicos

- `CREATE INDEX ix_audit_events_action ON public.audit_events USING btree (action)`
- `CREATE INDEX ix_audit_events_actor_user_id ON public.audit_events USING btree (actor_user_id)`
- `CREATE INDEX ix_audit_events_created_at ON public.audit_events USING btree (created_at)`
- `CREATE UNIQUE INDEX pk_audit_events ON public.audit_events USING btree (id)`

## daily_checkins

Bitácora de energía y enfoque por fecha.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `user_id` | integer | No | Cuenta propietaria o vinculada; véase la clave foránea. |
| `checked_on` | date | No | Día de la entrada de bitácora; único por usuario y fecha. |
| `energy` | integer | No | Energía declarada en escala de uno a cinco. |
| `focus` | integer | No | Enfoque declarado en escala de uno a cinco. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |
| `updated_at` | timestamp without time zone | No | Última modificación registrada por la aplicación, con convención UTC. |

### Defaults del motor

- `id`: `nextval('daily_checkins_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `ck_daily_checkins_valid_energy`: `CHECK (((energy >= 1) AND (energy <= 5)))`
- `ck_daily_checkins_valid_focus`: `CHECK (((focus >= 1) AND (focus <= 5)))`
- `fk_daily_checkins_user_id_users`: `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`
- `pk_daily_checkins`: `PRIMARY KEY (id)`
- `uq_user_daily_checkin`: `UNIQUE (user_id, checked_on)`

### Indices fisicos

- `CREATE UNIQUE INDEX pk_daily_checkins ON public.daily_checkins USING btree (id)`
- `CREATE UNIQUE INDEX uq_user_daily_checkin ON public.daily_checkins USING btree (user_id, checked_on)`

## habit_entries

Cumplimiento diario de cada hábito por usuario.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `user_id` | integer | No | Cuenta propietaria o vinculada; véase la clave foránea. |
| `habit_id` | integer | No | Hábito relacionado del catálogo. |
| `completed_on` | date | No | Día local al que corresponde un cumplimiento. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |

### Defaults del motor

- `id`: `nextval('habit_entries_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `fk_habit_entries_habit_id_habits`: `FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE RESTRICT`
- `fk_habit_entries_user_id_users`: `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`
- `pk_habit_entries`: `PRIMARY KEY (id)`
- `uq_habit_daily`: `UNIQUE (user_id, habit_id, completed_on)`

### Indices fisicos

- `CREATE INDEX ix_habit_entries_completed_on ON public.habit_entries USING btree (completed_on)`
- `CREATE INDEX ix_habit_entries_habit_id ON public.habit_entries USING btree (habit_id)`
- `CREATE INDEX ix_habit_entries_user_completed_on ON public.habit_entries USING btree (user_id, completed_on)`
- `CREATE INDEX ix_habit_entries_user_id ON public.habit_entries USING btree (user_id)`
- `CREATE UNIQUE INDEX pk_habit_entries ON public.habit_entries USING btree (id)`
- `CREATE UNIQUE INDEX uq_habit_daily ON public.habit_entries USING btree (user_id, habit_id, completed_on)`

## habits

Catálogo de hábitos y puntos por cumplimiento.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `code` | character varying(50) | No | Código estable y único del catálogo correspondiente. |
| `name` | character varying(100) | No | Nombre legible del elemento representado por esta tabla. |
| `description` | character varying(280) | No | Descripción visible del hábito o rutina. |
| `category` | character varying(50) | No | Agrupación del hábito para su presentación. |
| `icon` | character varying(20) | No | Identificador del icono utilizado en la interfaz. |
| `points` | integer | No | Puntos del hábito; no una columna de puntos acumulados por usuario. |
| `active` | boolean | No | Disponibilidad lógica del elemento, sin borrarlo físicamente. |
| `sort_order` | integer | No | Posición de presentación del hábito. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |
| `updated_at` | timestamp without time zone | No | Última modificación registrada por la aplicación, con convención UTC. |

### Defaults del motor

- `id`: `nextval('habits_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `ck_habits_valid_points`: `CHECK (((points >= 1) AND (points <= 100)))`
- `pk_habits`: `PRIMARY KEY (id)`
- `uq_habits_code`: `UNIQUE (code)`

### Indices fisicos

- `CREATE UNIQUE INDEX pk_habits ON public.habits USING btree (id)`
- `CREATE UNIQUE INDEX uq_habits_code ON public.habits USING btree (code)`

## health_measurements

Historial de mediciones con el contexto del momento registrado.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `user_id` | integer | No | Cuenta propietaria o vinculada; véase la clave foránea. |
| `weight_kg` | numeric(5,2) | No | Peso registrado en kilogramos, validado por límites técnicos. |
| `height_cm` | numeric(5,2) | No | Altura registrada en centímetros; se convierte a metros al calcular IMC. |
| `bmi_snapshot` | numeric(5,2) | No | IMC guardado en esa medición; no se recalcula al cambiar el perfil. |
| `measured_on` | date | No | Fecha de negocio de la medición; no equivale al instante created_at. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |
| `age_months` | integer | Si | Edad en meses cumplidos en la fecha de la medición. |
| `reference_sex` | character varying(12) | Si | Referencia de crecimiento registrada, no identidad de género. |
| `reference_source` | character varying(32) | Si | Identificador de la referencia utilizada, cuando procede. |
| `growth_percentile` | numeric(5,2) | Si | Percentil descriptivo cuando el cálculo tiene contexto suficiente. |

### Defaults del motor

- `id`: `nextval('health_measurements_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `ck_health_measurements_valid_bmi`: `CHECK (((bmi_snapshot >= (5)::numeric) AND (bmi_snapshot <= (100)::numeric)))`
- `ck_health_measurements_valid_growth_percentile`: `CHECK (((growth_percentile IS NULL) OR ((growth_percentile >= (0)::numeric) AND (growth_percentile <= (100)::numeric))))`
- `ck_health_measurements_valid_height`: `CHECK (((height_cm >= (50)::numeric) AND (height_cm <= (250)::numeric)))`
- `ck_health_measurements_valid_measurement_reference_sex`: `CHECK (((reference_sex IS NULL) OR ((reference_sex)::text = ANY ((ARRAY['male'::character varying, 'female'::character varying])::text[]))))`
- `ck_health_measurements_valid_weight`: `CHECK (((weight_kg >= (10)::numeric) AND (weight_kg <= (500)::numeric)))`
- `fk_health_measurements_user_id_users`: `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`
- `pk_health_measurements`: `PRIMARY KEY (id)`

### Indices fisicos

- `CREATE INDEX ix_health_measurements_measured_on ON public.health_measurements USING btree (measured_on)`
- `CREATE INDEX ix_health_measurements_user_id ON public.health_measurements USING btree (user_id)`
- `CREATE INDEX ix_health_measurements_user_measured_on ON public.health_measurements USING btree (user_id, measured_on)`
- `CREATE UNIQUE INDEX pk_health_measurements ON public.health_measurements USING btree (id)`

## personal_routines

Cabecera privada de una rutina y control de su revisión.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `user_id` | integer | No | Cuenta propietaria o vinculada; véase la clave foránea. |
| `name` | character varying(80) | No | Nombre legible del elemento representado por esta tabla. |
| `description` | character varying(500) | No | Descripción visible del hábito o rutina. |
| `goal` | character varying(12) | No | Objetivo funcional de la rutina propia. |
| `active` | boolean | No | Disponibilidad lógica del elemento, sin borrarlo físicamente. |
| `revision` | integer | No | Versión optimista de edición; evita sobrescribir cambios de otra ventana. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |
| `updated_at` | timestamp without time zone | No | Última modificación registrada por la aplicación, con convención UTC. |

### Defaults del motor

- `id`: `nextval('personal_routines_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `ck_personal_routines_valid_routine_goal`: `CHECK (((goal)::text = ANY ((ARRAY['center'::character varying, 'energy'::character varying, 'strength'::character varying])::text[])))`
- `ck_personal_routines_valid_routine_revision`: `CHECK ((revision >= 1))`
- `fk_personal_routines_user_id_users`: `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`
- `pk_personal_routines`: `PRIMARY KEY (id)`

### Indices fisicos

- `CREATE INDEX ix_personal_routines_user_active ON public.personal_routines USING btree (user_id, active)`
- `CREATE UNIQUE INDEX pk_personal_routines ON public.personal_routines USING btree (id)`

## routine_completions

Actividad declarada por usuario, identificador de rutina y día.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `user_id` | integer | No | Cuenta propietaria o vinculada; véase la clave foránea. |
| `routine_slug` | character varying(60) | No | Identificador textual del catálogo o personal-ID; no es una FK física. |
| `habit_id` | integer | No | Hábito relacionado del catálogo. |
| `completed_on` | date | No | Día local al que corresponde un cumplimiento. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |

### Defaults del motor

- `id`: `nextval('routine_completions_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `fk_routine_completions_habit_id_habits`: `FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE RESTRICT`
- `fk_routine_completions_user_id_users`: `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`
- `pk_routine_completions`: `PRIMARY KEY (id)`
- `uq_routine_daily`: `UNIQUE (user_id, routine_slug, completed_on)`

### Indices fisicos

- `CREATE INDEX ix_routine_completions_habit_id ON public.routine_completions USING btree (habit_id)`
- `CREATE INDEX ix_routine_completions_user_id ON public.routine_completions USING btree (user_id)`
- `CREATE UNIQUE INDEX pk_routine_completions ON public.routine_completions USING btree (id)`
- `CREATE UNIQUE INDEX uq_routine_daily ON public.routine_completions USING btree (user_id, routine_slug, completed_on)`

## routine_exercises

Ejercicios ordenados de una rutina, con dosis y descansos.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `routine_id` | integer | No | Rutina personal a la que pertenece el ejercicio. |
| `position` | integer | No | Posición de cero a once; única dentro de su rutina. |
| `name` | character varying(80) | No | Nombre legible del elemento representado por esta tabla. |
| `sets` | integer | No | Series entre uno y veinte; límite técnico, no prescripción individual. |
| `repetitions` | integer | Si | Repeticiones opcionales; debe existir repetición o duración. |
| `duration_seconds` | integer | Si | Duración opcional en segundos. |
| `rest_seconds` | integer | No | Descanso en segundos según los límites técnicos. |
| `instructions` | character varying(280) | No | Instrucciones escritas del ejercicio. |
| `visual` | character varying(12) | No | Referencia de demostración SVG o custom; no contiene un archivo de imagen. |

### Defaults del motor

- `id`: `nextval('routine_exercises_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `ck_routine_exercises_exercise_has_dose`: `CHECK (((repetitions IS NOT NULL) OR (duration_seconds IS NOT NULL)))`
- `ck_routine_exercises_valid_exercise_duration`: `CHECK (((duration_seconds IS NULL) OR ((duration_seconds >= 5) AND (duration_seconds <= 3600))))`
- `ck_routine_exercises_valid_exercise_position`: `CHECK ((("position" >= 0) AND ("position" <= 11)))`
- `ck_routine_exercises_valid_exercise_reps`: `CHECK (((repetitions IS NULL) OR ((repetitions >= 1) AND (repetitions <= 200))))`
- `ck_routine_exercises_valid_exercise_rest`: `CHECK (((rest_seconds >= 0) AND (rest_seconds <= 600)))`
- `ck_routine_exercises_valid_exercise_sets`: `CHECK (((sets >= 1) AND (sets <= 20)))`
- `ck_routine_exercises_valid_exercise_visual`: `CHECK (((visual)::text = ANY ((ARRAY['posture'::character varying, 'march'::character varying, 'palms'::character varying, 'shoulders'::character varying, 'wall'::character varying, 'walk'::character varying, 'breathing'::character varying, 'custom'::character varying])::text[])))`
- `fk_routine_exercises_routine_id_personal_routines`: `FOREIGN KEY (routine_id) REFERENCES personal_routines(id) ON DELETE CASCADE`
- `pk_routine_exercises`: `PRIMARY KEY (id)`
- `uq_routine_exercise_position`: `UNIQUE (routine_id, "position")`

### Indices fisicos

- `CREATE UNIQUE INDEX pk_routine_exercises ON public.routine_exercises USING btree (id)`
- `CREATE UNIQUE INDEX uq_routine_exercise_position ON public.routine_exercises USING btree (routine_id, "position")`

## school_enrollment_requests

Solicitud escrita que no concede permisos institucionales.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `user_id` | integer | No | Cuenta propietaria o vinculada; véase la clave foránea. |
| `school_name` | character varying(160) | No | Nombre escrito por la persona solicitante, aún sin validación institucional. |
| `group_name` | character varying(80) | No | Grupo escrito en la solicitud, no una FK al catálogo de grupos. |
| `requested_role` | character varying(12) | No | Rol escolar solicitado student/teacher; requiere revisión de la aplicación. |
| `status` | character varying(12) | No | Estado permitido por el CHECK de esta tabla; no siempre comparte vocabulario. |
| `reviewed_at` | timestamp without time zone | Si | Instante de revisión administrativa. |
| `reviewed_by_user_id` | integer | Si | Cuenta revisora opcional; SET NULL conserva el evento sin ella. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |
| `updated_at` | timestamp without time zone | No | Última modificación registrada por la aplicación, con convención UTC. |

### Defaults del motor

- `id`: `nextval('school_enrollment_requests_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `ck_school_enrollment_requests_valid_enrollment_status`: `CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'resolved'::character varying, 'rejected'::character varying, 'cancelled'::character varying])::text[])))`
- `ck_school_enrollment_requests_valid_requested_role`: `CHECK (((requested_role)::text = ANY ((ARRAY['student'::character varying, 'teacher'::character varying])::text[])))`
- `fk_school_enrollment_requests_reviewed_by_user_id_users`: `FOREIGN KEY (reviewed_by_user_id) REFERENCES users(id) ON DELETE SET NULL`
- `fk_school_enrollment_requests_user_id_users`: `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`
- `pk_school_enrollment_requests`: `PRIMARY KEY (id)`
- `uq_school_enrollment_requests_user_id`: `UNIQUE (user_id)`

### Indices fisicos

- `CREATE INDEX ix_enrollment_status_created ON public.school_enrollment_requests USING btree (status, created_at)`
- `CREATE INDEX ix_school_enrollment_requests_reviewed_by_user_id ON public.school_enrollment_requests USING btree (reviewed_by_user_id)`
- `CREATE UNIQUE INDEX pk_school_enrollment_requests ON public.school_enrollment_requests USING btree (id)`
- `CREATE UNIQUE INDEX uq_school_enrollment_requests_user_id ON public.school_enrollment_requests USING btree (user_id)`

## school_groups

Grupos de un colegio y un año académico.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `school_id` | integer | No | Colegio asociado; también participa en claves foráneas compuestas. |
| `name` | character varying(80) | No | Nombre legible del elemento representado por esta tabla. |
| `academic_year` | integer | No | Año del grupo, independiente del año actual del servidor. |
| `active` | boolean | No | Disponibilidad lógica del elemento, sin borrarlo físicamente. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |
| `updated_at` | timestamp without time zone | No | Última modificación registrada por la aplicación, con convención UTC. |

### Defaults del motor

- `id`: `nextval('school_groups_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `ck_school_groups_valid_academic_year`: `CHECK (((academic_year >= 2020) AND (academic_year <= 2100)))`
- `fk_school_groups_school_id_schools`: `FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE RESTRICT`
- `pk_school_groups`: `PRIMARY KEY (id)`
- `uq_school_group_id_school`: `UNIQUE (id, school_id)`
- `uq_school_group_year_name`: `UNIQUE (school_id, academic_year, name)`

### Indices fisicos

- `CREATE INDEX ix_school_groups_school_id ON public.school_groups USING btree (school_id)`
- `CREATE UNIQUE INDEX pk_school_groups ON public.school_groups USING btree (id)`
- `CREATE UNIQUE INDEX uq_school_group_id_school ON public.school_groups USING btree (id, school_id)`
- `CREATE UNIQUE INDEX uq_school_group_year_name ON public.school_groups USING btree (school_id, academic_year, name)`

## school_memberships

Vinculación revisada de una cuenta con una institución.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `user_id` | integer | No | Cuenta propietaria o vinculada; véase la clave foránea. |
| `school_id` | integer | No | Colegio asociado; también participa en claves foráneas compuestas. |
| `group_id` | integer | Si | Grupo asociado; puede ser opcional en una membresía. |
| `requested_role` | character varying(12) | No | Rol escolar solicitado student/teacher; requiere revisión de la aplicación. |
| `status` | character varying(12) | No | Estado permitido por el CHECK de esta tabla; no siempre comparte vocabulario. |
| `allow_aggregate` | boolean | No | Preferencia voluntaria de inclusión en agregados. |
| `aggregate_since` | timestamp without time zone | Si | Inicio de la preferencia vigente de agregación. |
| `reviewed_at` | timestamp without time zone | Si | Instante de revisión administrativa. |
| `reviewed_by_user_id` | integer | Si | Cuenta revisora opcional; SET NULL conserva el evento sin ella. |
| `authorization_confirmed` | boolean | No | Confirmación administrativa necesaria para la vinculación. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |
| `updated_at` | timestamp without time zone | No | Última modificación registrada por la aplicación, con convención UTC. |

### Defaults del motor

- `id`: `nextval('school_memberships_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `ck_school_memberships_valid_membership_status`: `CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'approved'::character varying, 'rejected'::character varying, 'revoked'::character varying])::text[])))`
- `ck_school_memberships_valid_school_role`: `CHECK (((requested_role)::text = ANY ((ARRAY['student'::character varying, 'teacher'::character varying])::text[])))`
- `fk_school_membership_group_school`: `FOREIGN KEY (group_id, school_id) REFERENCES school_groups(id, school_id) ON DELETE RESTRICT`
- `fk_school_memberships_reviewed_by_user_id_users`: `FOREIGN KEY (reviewed_by_user_id) REFERENCES users(id) ON DELETE SET NULL`
- `fk_school_memberships_school_id_schools`: `FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE RESTRICT`
- `fk_school_memberships_user_id_users`: `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`
- `pk_school_memberships`: `PRIMARY KEY (id)`
- `uq_school_membership_id_school`: `UNIQUE (id, school_id)`
- `uq_school_memberships_user_id`: `UNIQUE (user_id)`

### Indices fisicos

- `CREATE INDEX ix_membership_group_status ON public.school_memberships USING btree (group_id, status)`
- `CREATE INDEX ix_school_memberships_reviewed_by_user_id ON public.school_memberships USING btree (reviewed_by_user_id)`
- `CREATE INDEX ix_school_memberships_school_id ON public.school_memberships USING btree (school_id)`
- `CREATE UNIQUE INDEX pk_school_memberships ON public.school_memberships USING btree (id)`
- `CREATE UNIQUE INDEX uq_school_membership_id_school ON public.school_memberships USING btree (id, school_id)`
- `CREATE UNIQUE INDEX uq_school_memberships_user_id ON public.school_memberships USING btree (user_id)`

## schools

Catálogo institucional gestionado por administración.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `code` | character varying(60) | No | Código estable y único del catálogo correspondiente. |
| `name` | character varying(160) | No | Nombre legible del elemento representado por esta tabla. |
| `active` | boolean | No | Disponibilidad lógica del elemento, sin borrarlo físicamente. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |
| `updated_at` | timestamp without time zone | No | Última modificación registrada por la aplicación, con convención UTC. |

### Defaults del motor

- `id`: `nextval('schools_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `pk_schools`: `PRIMARY KEY (id)`
- `uq_schools_code`: `UNIQUE (code)`

### Indices fisicos

- `CREATE UNIQUE INDEX pk_schools ON public.schools USING btree (id)`
- `CREATE UNIQUE INDEX uq_schools_code ON public.schools USING btree (code)`

## teacher_group_assignments

Asignación docente a grupos del mismo colegio.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `membership_id` | integer | No | Vinculación del docente, comprobada junto con school_id. |
| `school_id` | integer | No | Colegio asociado; también participa en claves foráneas compuestas. |
| `group_id` | integer | No | Grupo asociado; puede ser opcional en una membresía. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |
| `updated_at` | timestamp without time zone | No | Última modificación registrada por la aplicación, con convención UTC. |

### Defaults del motor

- `id`: `nextval('teacher_group_assignments_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `fk_assignment_group_school`: `FOREIGN KEY (group_id, school_id) REFERENCES school_groups(id, school_id) ON DELETE RESTRICT`
- `fk_assignment_membership_school`: `FOREIGN KEY (membership_id, school_id) REFERENCES school_memberships(id, school_id) ON DELETE CASCADE`
- `pk_teacher_group_assignments`: `PRIMARY KEY (id)`
- `uq_teacher_group`: `UNIQUE (membership_id, group_id)`

### Indices fisicos

- `CREATE INDEX ix_assignment_group ON public.teacher_group_assignments USING btree (group_id)`
- `CREATE UNIQUE INDEX pk_teacher_group_assignments ON public.teacher_group_assignments USING btree (id)`
- `CREATE UNIQUE INDEX uq_teacher_group ON public.teacher_group_assignments USING btree (membership_id, group_id)`

## user_goals

Meta semanal del usuario para un hábito concreto.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `user_id` | integer | No | Cuenta propietaria o vinculada; véase la clave foránea. |
| `habit_id` | integer | No | Hábito relacionado del catálogo. |
| `target_days` | integer | No | Meta entre uno y siete días para un hábito. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |
| `updated_at` | timestamp without time zone | No | Última modificación registrada por la aplicación, con convención UTC. |

### Defaults del motor

- `id`: `nextval('user_goals_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `ck_user_goals_valid_target_days`: `CHECK (((target_days >= 1) AND (target_days <= 7)))`
- `fk_user_goals_habit_id_habits`: `FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE RESTRICT`
- `fk_user_goals_user_id_users`: `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`
- `pk_user_goals`: `PRIMARY KEY (id)`
- `uq_user_goal_habit`: `UNIQUE (user_id, habit_id)`

### Indices fisicos

- `CREATE UNIQUE INDEX pk_user_goals ON public.user_goals USING btree (id)`
- `CREATE UNIQUE INDEX uq_user_goal_habit ON public.user_goals USING btree (user_id, habit_id)`

## user_profiles

Perfil, preferencias, contexto y confirmaciones de privacidad.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `user_id` [PK] | integer | No | Cuenta propietaria o vinculada; véase la clave foránea. |
| `display_name` | character varying(80) | No | Nombre o apodo mostrado en el perfil. |
| `birth_date` | date | Si | Fecha de nacimiento opcional; permite obtener edad al medir. |
| `grade` | character varying(80) | Si | Texto de grado, grupo o área conservado en el perfil. |
| `timezone` | character varying(50) | No | Zona IANA utilizada para determinar el día local del usuario. |
| `privacy_version` | character varying(20) | No | Versión de la política aceptada. |
| `privacy_accepted_at` | timestamp without time zone | No | Instante de aceptación de la política. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |
| `updated_at` | timestamp without time zone | No | Última modificación registrada por la aplicación, con convención UTC. |
| `usage_mode` | character varying(20) | No | Experiencia personal o institucional; no concede permisos por sí sola. |
| `institution_name` | character varying(160) | Si | Texto de contexto del perfil; no sustituye una vinculación verificada. |
| `reference_sex` | character varying(12) | No | Referencia de crecimiento registrada, no identidad de género. |
| `movement_goal` | character varying(12) | No | Objetivo funcional center, energy o strength; no categoría de IMC. |
| `movement_preference` | character varying(12) | No | Preferencia adaptable, seated, supported o standing. |
| `personalization_completed_at` | timestamp without time zone | Si | Final del recorrido inicial; evita repetirlo en cada ingreso. |
| `measurement_consent_at` | timestamp without time zone | Si | Instante de la confirmación para guardar mediciones. |

### Defaults del motor

- `usage_mode`: `'personal'::character varying`
- `reference_sex`: `'unspecified'::character varying`
- `movement_goal`: `'energy'::character varying`
- `movement_preference`: `'adaptable'::character varying`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `ck_user_profiles_valid_movement_goal`: `CHECK (((movement_goal)::text = ANY ((ARRAY['center'::character varying, 'energy'::character varying, 'strength'::character varying])::text[])))`
- `ck_user_profiles_valid_movement_preference`: `CHECK (((movement_preference)::text = ANY ((ARRAY['adaptable'::character varying, 'seated'::character varying, 'supported'::character varying, 'standing'::character varying])::text[])))`
- `ck_user_profiles_valid_reference_sex`: `CHECK (((reference_sex)::text = ANY ((ARRAY['unspecified'::character varying, 'female'::character varying, 'male'::character varying])::text[])))`
- `ck_user_profiles_valid_usage_mode`: `CHECK (((usage_mode)::text = ANY ((ARRAY['personal'::character varying, 'institutional'::character varying])::text[])))`
- `fk_user_profiles_user_id_users`: `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`
- `pk_user_profiles`: `PRIMARY KEY (user_id)`

### Indices fisicos

- `CREATE UNIQUE INDEX pk_user_profiles ON public.user_profiles USING btree (user_id)`

## users

Identidad de la cuenta, autenticación y estado de acceso.

| Campo | Tipo PostgreSQL | Nulo | Explicacion |
|---|---|---|---|
| `id` [PK] | integer | No | Identificador de la fila; no representa una medida ni un código externo. |
| `email` | character varying(254) | No | Correo único para acceso; no debe exponerse con datos reales en una sustentación. |
| `password_hash` | character varying(255) | No | Hash scrypt de acceso, nunca contraseña en texto. El ejemplo no es válido. |
| `role` | character varying(20) | No | Rol de aplicación user/admin; distinto de un rol PostgreSQL y del rol escolar. |
| `status` | character varying(20) | No | Estado permitido por el CHECK de esta tabla; no siempre comparte vocabulario. |
| `last_login_at` | timestamp without time zone | Si | Instante del último ingreso correcto. |
| `failed_login_count` | integer | No | Intentos fallidos usados por el bloqueo temporal de la aplicación. |
| `locked_until` | timestamp without time zone | Si | Fin del bloqueo temporal; NULL significa que no hay fecha registrada. |
| `created_at` | timestamp without time zone | No | Instante de creación. Convención UTC sin zona incorporada al tipo SQL. |
| `updated_at` | timestamp without time zone | No | Última modificación registrada por la aplicación, con convención UTC. |

### Defaults del motor

- `id`: `nextval('users_id_seq'::regclass)`

### Claves, relaciones y restricciones

NOT NULL se representa campo por campo en la columna Nulo. Sus nombres físicos también están en el catálogo JSON y el DDL completos.

- `ck_users_valid_role`: `CHECK (((role)::text = ANY ((ARRAY['user'::character varying, 'admin'::character varying])::text[])))`
- `ck_users_valid_status`: `CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying])::text[])))`
- `pk_users`: `PRIMARY KEY (id)`

### Indices fisicos

- `CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email)`
- `CREATE UNIQUE INDEX pk_users ON public.users USING btree (id)`
