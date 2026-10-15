-- Catalogs and migration revision only. Never exports application rows.
SELECT jsonb_build_object(
  'postgres_version', current_setting('server_version'),
  'migration_revision', (SELECT version_num FROM public.alembic_version),
  'tables', (
    SELECT jsonb_agg(jsonb_build_object(
      'name', t.relname,
      'columns', (
        SELECT jsonb_agg(jsonb_build_object(
          'name', a.attname,
          'type', format_type(a.atttypid, a.atttypmod),
          'nullable', NOT a.attnotnull,
          'default', pg_get_expr(d.adbin, d.adrelid),
          'primary_key', EXISTS (
            SELECT 1 FROM pg_constraint k
            WHERE k.conrelid=t.oid AND k.contype='p' AND a.attnum=ANY(k.conkey)
          )
        ) ORDER BY a.attnum)
        FROM pg_attribute a
        LEFT JOIN pg_attrdef d ON d.adrelid=a.attrelid AND d.adnum=a.attnum
        WHERE a.attrelid=t.oid AND a.attnum>0 AND NOT a.attisdropped
      ),
      'constraints', (
        SELECT COALESCE(jsonb_agg(jsonb_build_object(
          'name', k.conname, 'kind', k.contype,
          'definition', pg_get_constraintdef(k.oid),
          'columns', (
            SELECT jsonb_agg(a.attname ORDER BY u.position)
            FROM unnest(k.conkey) WITH ORDINALITY AS u(attnum,position)
            JOIN pg_attribute a ON a.attrelid=k.conrelid AND a.attnum=u.attnum
          ),
          'target_table', (SELECT relname FROM pg_class WHERE oid=k.confrelid),
          'target_columns', (
            SELECT jsonb_agg(a.attname ORDER BY u.position)
            FROM unnest(k.confkey) WITH ORDINALITY AS u(attnum,position)
            JOIN pg_attribute a ON a.attrelid=k.confrelid AND a.attnum=u.attnum
          )
        ) ORDER BY k.conname), '[]'::jsonb)
        FROM pg_constraint k WHERE k.conrelid=t.oid
      ),
      'indexes', (
        SELECT COALESCE(jsonb_agg(jsonb_build_object(
          'name', x.relname, 'unique', i.indisunique, 'primary', i.indisprimary,
          'definition', pg_get_indexdef(i.indexrelid)
        ) ORDER BY x.relname), '[]'::jsonb)
        FROM pg_index i JOIN pg_class x ON x.oid=i.indexrelid
        WHERE i.indrelid=t.oid
      )
    ) ORDER BY t.relname)
    FROM pg_class t JOIN pg_namespace n ON n.oid=t.relnamespace
    WHERE n.nspname='public' AND t.relkind='r' AND t.relname<>'alembic_version'
  )
);
