-- Ejecutar sobre la copia ficticia, no sobre datos personales del sitio.
-- Cada SELECT es una demostracion independiente, sin escribir datos.
-- 1. Identidad y motor: current_user no es una cuenta de la pagina web.
SELECT current_database() AS base, current_user AS usuario, version() AS motor;
-- 2. Diecisiete tablas de negocio y una tabla tecnica Alembic.
SELECT table_name FROM information_schema.tables
WHERE table_schema='public' AND table_type='BASE TABLE' ORDER BY table_name;
-- 3. Todos los campos y tipos fisicos, sin consultar datos personales.
SELECT table_name,ordinal_position,column_name,data_type,is_nullable,column_default
FROM information_schema.columns WHERE table_schema='public'
ORDER BY table_name,ordinal_position;
-- 4. Claves primarias, foraneas, unicidades y limites CHECK.
SELECT c.relname AS tabla,k.conname AS restriccion,k.contype AS tipo,
       pg_get_constraintdef(k.oid) AS definicion
FROM pg_constraint k JOIN pg_class c ON c.oid=k.conrelid
JOIN pg_namespace n ON n.oid=c.relnamespace
WHERE n.nspname='public' ORDER BY c.relname,k.contype,k.conname;
-- 5. Uno a uno: no duplicamos correo ni contrasena en el perfil.
SELECT u.id,u.email,p.display_name,p.usage_mode
FROM users u JOIN user_profiles p ON p.user_id=u.id ORDER BY u.id;
-- 6. Uno a muchos: dos mediciones de la misma estudiante ficticia.
SELECT p.display_name,m.measured_on,m.weight_kg,m.height_cm,m.bmi_snapshot
FROM user_profiles p JOIN health_measurements m ON m.user_id=p.user_id
WHERE p.user_id=3 ORDER BY m.measured_on;
-- 7. Puntos: se suman entradas de habitos; NO se suma otra vez routine_completions.
-- Esperado antes de ejercicios: estudiante 3 = 35 XP, estudiante 4 = 10 XP.
SELECT p.user_id,p.display_name,COALESCE(SUM(h.points),0) AS xp
FROM user_profiles p LEFT JOIN habit_entries e ON e.user_id=p.user_id
LEFT JOIN habits h ON h.id=e.habit_id
GROUP BY p.user_id,p.display_name ORDER BY p.user_id;
-- 8. Cabecera/detalle: dos ejercicios, no columnas ejercicio_1/ejercicio_2.
SELECT r.id,r.name AS rutina,x.position,x.name AS ejercicio,
       x.sets,x.repetitions,x.duration_seconds,x.rest_seconds
FROM personal_routines r JOIN routine_exercises x ON x.routine_id=r.id
WHERE r.user_id=3 ORDER BY r.id,x.position;
-- 9. Colegio + grupo + vinculo. Las dos columnas preservan el mismo colegio.
SELECT s.name AS colegio,g.name AS grupo,m.requested_role,m.status,p.display_name
FROM school_memberships m JOIN schools s ON s.id=m.school_id
LEFT JOIN school_groups g ON (g.id,g.school_id)=(m.group_id,m.school_id)
JOIN user_profiles p ON p.user_id=m.user_id ORDER BY m.id;
-- 10. Alcance docente. Esto demuestra la relacion; NO es el panel anonimizado.
SELECT t.membership_id,t.school_id,g.name,g.academic_year
FROM teacher_group_assignments t
JOIN school_groups g ON (g.id,g.school_id)=(t.group_id,t.school_id);
-- 11. Una solicitud de texto NO es una membresia aprobada.
SELECT q.user_id,q.school_name,q.group_name,q.status,m.id AS membership_id
FROM school_enrollment_requests q LEFT JOIN school_memberships m ON m.user_id=q.user_id;
-- 12. Restricciones de acceso y propiedad; no devuelve contrasenas.
SELECT current_user,
 has_schema_privilege(current_user,'public','CREATE') AS crear_en_public,
 has_schema_privilege(current_user,'practica_ega1026','CREATE') AS crear_en_practica,
 has_table_privilege(current_user,'public.users','SELECT') AS leer_usuarios_ficticios,
 has_database_privilege(current_user,'postgres','CONNECT') AS conectar_db_tecnica;
-- 13. Indices: un Seq Scan con cinco filas no demuestra lentitud.
EXPLAIN SELECT id,measured_on,bmi_snapshot FROM health_measurements
WHERE user_id=3 ORDER BY measured_on;
