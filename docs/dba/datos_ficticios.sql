-- DATOS INVENTADOS. No se copiaron usuarios ni mediciones del sitio.
-- Solo un administrador inicializa esta base VACIA, nunca produccion.
\set ON_ERROR_STOP on
BEGIN;
DO $$ BEGIN
  IF current_database() <> 'vitalilab_estudio_ega1026' THEN
    RAISE EXCEPTION 'Destino incorrecto: solo vitalilab_estudio_ega1026';
  END IF;
  IF EXISTS (SELECT 1 FROM public.users) OR EXISTS (SELECT 1 FROM public.habits) THEN
    RAISE EXCEPTION 'La base debe estar vacia; no se sobreescriben datos';
  END IF;
END $$;

INSERT INTO users (id,email,password_hash,role,status,failed_login_count,created_at,updated_at) VALUES
 (1,'admin@example.invalid','not-a-real-login-hash','admin','active',0,'2026-01-15 12:00','2026-01-15 12:00'),
 (2,'docente@example.invalid','not-a-real-login-hash','user','active',0,'2026-01-15 12:00','2026-01-15 12:00'),
 (3,'alumna@example.invalid','not-a-real-login-hash','user','active',0,'2026-01-15 12:00','2026-01-15 12:00'),
 (4,'alumno@example.invalid','not-a-real-login-hash','user','active',0,'2026-01-15 12:00','2026-01-15 12:00'),
 (5,'personal@example.invalid','not-a-real-login-hash','user','active',0,'2026-01-15 12:00','2026-01-15 12:00');
INSERT INTO user_profiles
 (user_id,display_name,birth_date,grade,timezone,privacy_version,privacy_accepted_at,
 created_at,updated_at,usage_mode,institution_name,personalization_completed_at) VALUES
 (1,'Administracion ficticia','1990-01-01',NULL,'America/Bogota','study-1','2026-01-15','2026-01-15','2026-01-15','personal',NULL,'2026-01-15'),
 (2,'Docente ficticio','1990-02-01','10 A','America/Bogota','study-1','2026-01-15','2026-01-15','2026-01-15','institutional','Colegio Ficticio Aurora','2026-01-15'),
 (3,'Estudiante ficticia A','2010-01-15','10 A','America/Bogota','study-1','2026-01-15','2026-01-15','2026-01-15','institutional','Colegio Ficticio Aurora','2026-01-15'),
 (4,'Estudiante ficticio B','2010-01-15','10 A','America/Bogota','study-1','2026-01-15','2026-01-15','2026-01-15','institutional','Colegio Ficticio Aurora','2026-01-15'),
 (5,'Persona ficticia','2000-01-01',NULL,'America/Bogota','study-1','2026-01-15','2026-01-15','2026-01-15','personal',NULL,'2026-01-15');
INSERT INTO habits
 (id,code,name,description,category,icon,points,active,sort_order,created_at,updated_at) VALUES
 (1,'study-water','Hidratacion','Ejemplo de catalogo','wellbeing','water',10,true,1,'2026-01-15','2026-01-15'),
 (2,'study-movement','Movimiento','Ejemplo de catalogo','movement','move',15,true,2,'2026-01-15','2026-01-15'),
 (3,'study-rest','Descanso','Ejemplo de catalogo','rest','moon',10,true,3,'2026-01-15','2026-01-15');
INSERT INTO health_measurements
 (id,user_id,weight_kg,height_cm,bmi_snapshot,measured_on,created_at,age_months,reference_sex,reference_source,growth_percentile) VALUES
 (1,3,50,160,19.53,'2026-02-15','2026-02-15 12:00',193,'female',NULL,NULL),
 (2,3,51,161,19.68,'2026-04-15','2026-04-15 12:00',195,'female',NULL,NULL),
 (3,4,55,165,20.20,'2026-02-15','2026-02-15 12:00',193,'male',NULL,NULL);
-- Percentiles NULL deliberadamente: no se inventa una interpretacion clinica.
INSERT INTO habit_entries (id,user_id,habit_id,completed_on,created_at) VALUES
 (1,3,1,'2026-10-14','2026-10-14 12:00'),
 (2,3,2,'2026-10-14','2026-10-14 12:01'),
 (3,3,1,'2026-10-15','2026-10-15 12:00'),
 (4,4,1,'2026-10-15','2026-10-15 12:00');
INSERT INTO user_goals (id,user_id,habit_id,target_days,created_at,updated_at) VALUES
 (1,3,1,5,'2026-01-15','2026-01-15'),(2,4,2,3,'2026-01-15','2026-01-15');
INSERT INTO daily_checkins (id,user_id,checked_on,energy,focus,created_at,updated_at) VALUES
 (1,3,'2026-10-14',3,4,'2026-10-14','2026-10-14'),
 (2,3,'2026-10-15',4,4,'2026-10-15','2026-10-15');
INSERT INTO schools (id,code,name,active,created_at,updated_at) VALUES
 (1,'STUDY-AURORA','Colegio Ficticio Aurora',true,'2026-01-15','2026-01-15'),
 (2,'STUDY-BOSQUE','Colegio Ficticio Bosque',true,'2026-01-15','2026-01-15');
INSERT INTO school_groups (id,school_id,name,academic_year,active,created_at,updated_at) VALUES
 (1,1,'10 A',2026,true,'2026-01-15','2026-01-15'),
 (2,1,'10 B',2026,true,'2026-01-15','2026-01-15'),
 (3,2,'10 A',2026,true,'2026-01-15','2026-01-15');
INSERT INTO school_memberships
 (id,user_id,school_id,group_id,requested_role,status,allow_aggregate,authorization_confirmed,
 reviewed_at,reviewed_by_user_id,created_at,updated_at) VALUES
 (1,2,1,NULL,'teacher','approved',false,true,'2026-01-15',1,'2026-01-15','2026-01-15'),
 (2,3,1,1,'student','approved',false,true,'2026-01-15',1,'2026-01-15','2026-01-15'),
 (3,4,1,1,'student','approved',false,true,'2026-01-15',1,'2026-01-15','2026-01-15');
INSERT INTO teacher_group_assignments
 (id,membership_id,school_id,group_id,created_at,updated_at) VALUES
 (1,1,1,1,'2026-01-15','2026-01-15');
INSERT INTO school_enrollment_requests
 (id,user_id,school_name,group_name,requested_role,status,created_at,updated_at) VALUES
 (1,5,'Colegio Ficticio Horizonte','Grupo inventado','student','pending','2026-10-15','2026-10-15');
INSERT INTO personal_routines (id,user_id,name,description,goal,active,revision,created_at,updated_at) VALUES
 (1,3,'Mi pausa ficticia','Ejemplo para explicar cabecera y detalle','energy',true,1,'2026-10-14','2026-10-14');
INSERT INTO routine_exercises
 (id,routine_id,position,name,sets,repetitions,duration_seconds,rest_seconds,instructions,visual) VALUES
 (1,1,0,'Movilidad de hombros',2,8,NULL,30,'Ejemplo de instrucciones para estudiar','shoulders'),
 (2,1,1,'Respiracion tranquila',1,NULL,30,15,'Ejemplo de duracion para estudiar','breathing');
INSERT INTO routine_completions (id,user_id,routine_slug,habit_id,completed_on,created_at) VALUES
 (1,3,'personal-1',2,'2026-10-14','2026-10-14 12:01');
INSERT INTO announcements (id,author_user_id,title,body,status,published_at,created_at,updated_at) VALUES
 (1,1,'Comunicado inventado','Texto ficticio para demostrar relaciones','published','2026-01-15','2026-01-15','2026-01-15');
INSERT INTO audit_events (id,actor_user_id,action,entity_type,entity_id,metadata_redacted,created_at) VALUES
 (1,1,'study.seed','study','1','{"synthetic":true}','2026-10-15');
INSERT INTO alembic_version (version_num) VALUES ('c842d6e190ab');
-- Sincroniza secuencias tras ids explicitos. Solo tablas del esquema de estudio.
DO $$ DECLARE t record; seq text; last_id bigint;
BEGIN
  FOR t IN SELECT table_name FROM information_schema.columns
           WHERE table_schema='public' AND column_name='id' LOOP
    seq := pg_get_serial_sequence(format('public.%I',t.table_name),'id');
    IF seq IS NOT NULL THEN
      EXECUTE format('SELECT COALESCE(MAX(id),1) FROM public.%I',t.table_name) INTO last_id;
      PERFORM setval(seq,last_id,true);
    END IF;
  END LOOP;
END $$;
COMMIT;
