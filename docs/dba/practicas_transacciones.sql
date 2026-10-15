-- Con psql, ejecutar este archivo completo; todo termina en ROLLBACK.
-- DBeaver: ejecutar como script, no activar autocommit entre instrucciones.
\set ON_ERROR_STOP on
BEGIN;
DO $$ BEGIN
  IF current_database() <> 'vitalilab_estudio_ega1026' THEN
    RAISE EXCEPTION 'Solo se permiten practicas en la copia de estudio';
  END IF;
END $$;
SET LOCAL ROLE ega1026_estudio;
-- INSERT, SELECT, UPDATE, DELETE sobre una fila temporal dentro de la transaccion.
INSERT INTO daily_checkins
 (id,user_id,checked_on,energy,focus,created_at,updated_at)
VALUES (900001,5,'2026-10-16',3,4,'2026-10-16','2026-10-16');
SELECT id,user_id,energy,focus FROM daily_checkins WHERE id=900001;
UPDATE daily_checkins SET energy=4 WHERE id=900001 AND user_id=5;
DELETE FROM daily_checkins WHERE id=900001 AND user_id=5;
-- Integridad: excepciones esperadas se capturan para que el script siga.
DO $$ BEGIN
  BEGIN
    INSERT INTO habit_entries(id,user_id,habit_id,completed_on,created_at)
    VALUES(900002,3,1,'2026-10-14','2026-10-14');
    RAISE EXCEPTION 'FALLO: acepto un cumplimiento duplicado';
  EXCEPTION WHEN unique_violation THEN
    RAISE NOTICE 'OK: UNIQUE impide duplicar XP de un habito por dia';
  END;
  BEGIN
    INSERT INTO school_memberships
     (id,user_id,school_id,group_id,requested_role,status,allow_aggregate,
      authorization_confirmed,created_at,updated_at)
    VALUES(900003,5,1,3,'student','pending',false,false,'2026-10-16','2026-10-16');
    RAISE EXCEPTION 'FALLO: acepto un grupo de otro colegio';
  EXCEPTION WHEN foreign_key_violation THEN
    RAISE NOTICE 'OK: FK compuesta impide mezclar colegios';
  END;
  BEGIN
    UPDATE routine_exercises SET sets=0 WHERE id=1;
    RAISE EXCEPTION 'FALLO: acepto cero series';
  EXCEPTION WHEN check_violation THEN
    RAISE NOTICE 'OK: CHECK impide cero series';
  END;
  BEGIN
    DELETE FROM habits WHERE id=1;
    RAISE EXCEPTION 'FALLO: permitio borrar un habito referenciado';
  EXCEPTION WHEN foreign_key_violation THEN
    RAISE NOTICE 'OK: RESTRICT conserva las referencias del habito';
  END;
  BEGIN
    EXECUTE 'ALTER TABLE public.users ADD COLUMN forbidden integer';
    RAISE EXCEPTION 'FALLO: permitio modificar estructura public';
  EXCEPTION WHEN insufficient_privilege THEN
    RAISE NOTICE 'OK: sin permiso para alterar tablas del proyecto';
  END;
  BEGIN
    EXECUTE 'CREATE ROLE forbidden_study_role';
    RAISE EXCEPTION 'FALLO: permitio crear roles';
  EXCEPTION WHEN insufficient_privilege THEN
    RAISE NOTICE 'OK: sin permiso para administrar usuarios PostgreSQL';
  END;
END $$;
-- DDL propio: CREATE TABLE permitido SOLO en su esquema de ejercicios.
CREATE TABLE practica_ega1026.notas_temporales(id integer PRIMARY KEY,nota text NOT NULL);
INSERT INTO practica_ega1026.notas_temporales VALUES(1,'Tabla de demostracion');
SELECT id,nota FROM practica_ega1026.notas_temporales;
-- CASCADE del detalle en la copia, reversible (no ejecutar en el sitio).
DELETE FROM personal_routines WHERE id=1 AND user_id=3;
DO $$ BEGIN
  IF EXISTS(SELECT 1 FROM routine_exercises WHERE routine_id=1) THEN
    RAISE EXCEPTION 'FALLO: detalle no eliminado en cascada';
  END IF;
END $$;
ROLLBACK;
-- Despues debe haber 2 ejercicios y no existir notas_temporales.
SELECT COUNT(*) AS ejercicios_restaurados FROM routine_exercises WHERE routine_id=1;
SELECT to_regclass('practica_ega1026.notas_temporales') AS debe_ser_null;
