#!/bin/sh
set -eu
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
  --set=app_password="$VITALILAB_APP_PASSWORD" <<'SQL'
CREATE ROLE vitalilab_app LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE PASSWORD :'app_password';
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON DATABASE vitalilab_staging FROM PUBLIC;
GRANT CONNECT ON DATABASE vitalilab_staging TO vitalilab_app;
GRANT USAGE ON SCHEMA public TO vitalilab_app;
SQL
