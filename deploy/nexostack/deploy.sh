#!/bin/bash
set -euo pipefail
umask 077
[[ ${EUID} == 0 ]] || { echo 'Run with the trusted infrastructure account.' >&2; exit 1; }
sha=${1:-}
[[ $sha =~ ^[0-9a-f]{40}$ ]] || { echo 'Expected a full verified commit.' >&2; exit 2; }
base=/opt/labs/vitalilab
release=$base/releases/$sha
[[ -f $release/wsgi.py && -f $base/secrets/runtime.env ]] || exit 3
exec 9>"$base/deploy.lock"
flock -n 9 || { echo 'Another VitaliLab deployment is active.' >&2; exit 4; }
export RELEASE_SHA=$sha
dc=(docker compose --env-file "$base/secrets/runtime.env" -f "$release/deploy/nexostack/compose.yaml")
"${dc[@]}" config --quiet
nice -n 15 ionice -c 2 -n 7 "${dc[@]}" build web
"${dc[@]}" up -d --wait --wait-timeout 90 db
if [[ -L $base/current ]]; then
  "$base/current/deploy/nexostack/backup.sh"
fi
"${dc[@]}" run --no-deps --rm migrate
"${dc[@]}" exec -T db psql -U vitalilab_owner -d vitalilab_staging -v ON_ERROR_STOP=1 <<'SQL'
REVOKE ALL ON DATABASE vitalilab_staging FROM PUBLIC;
GRANT CONNECT ON DATABASE vitalilab_staging TO vitalilab_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON users, user_profiles, health_measurements,
  habits, habit_entries, announcements, audit_events TO vitalilab_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO vitalilab_app;
GRANT SELECT ON alembic_version TO vitalilab_app;
SQL
"${dc[@]}" up -d --no-deps --wait --wait-timeout 90 web
ln -sfn "$release" "$base/current"
echo "VitaliLab release active: $sha"
