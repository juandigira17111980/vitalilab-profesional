\set ON_ERROR_STOP on
BEGIN;
DO $$ BEGIN
  IF current_database() <> 'vitalilab_estudio_ega1026' THEN
    RAISE EXCEPTION 'Este archivo es exclusivo de la instancia de estudio';
  END IF;
END $$;
CREATE ROLE ega1026_estudio NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE
  NOREPLICATION NOBYPASSRLS CONNECTION LIMIT 4;
REVOKE ALL ON DATABASE vitalilab_estudio_ega1026 FROM PUBLIC;
REVOKE CONNECT ON DATABASE postgres, template1 FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT CONNECT ON DATABASE vitalilab_estudio_ega1026 TO ega1026_estudio;
GRANT USAGE ON SCHEMA public TO ega1026_estudio;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ega1026_estudio;
GRANT INSERT, UPDATE, DELETE ON
  users,user_profiles,health_measurements,habits,habit_entries,user_goals,daily_checkins,
  schools,school_groups,school_memberships,teacher_group_assignments,
  school_enrollment_requests,personal_routines,routine_exercises,routine_completions,
  announcements,audit_events TO ega1026_estudio;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ega1026_estudio;
CREATE SCHEMA practica_ega1026 AUTHORIZATION ega1026_estudio;
ALTER ROLE ega1026_estudio SET search_path = public, practica_ega1026;
ALTER ROLE ega1026_estudio SET statement_timeout = '5s';
ALTER ROLE ega1026_estudio SET lock_timeout = '2s';
ALTER ROLE ega1026_estudio SET idle_in_transaction_session_timeout = '60s';
ALTER ROLE ega1026_estudio SET timezone = 'UTC';
COMMIT;
-- NOLOGIN deliberado. Activacion individual solo tras validar su llave publica,
-- asignar password SCRAM por canal privado y configurar tunel restringido.
