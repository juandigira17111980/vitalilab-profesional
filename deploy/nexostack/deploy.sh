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
domain_options=()
if python3 "$release/scripts/check_domain_dns.py"; then
  domain_options=(-f "$release/deploy/nexostack/domain-https.yaml")
elif [[ $(docker inspect -f '{{index .Config.Labels "traefik.http.routers.vitalilab-main-https.tls.certresolver"}}' vitalilab-web-lab 2>/dev/null || true) == letsencrypt ]]; then
  echo 'Principal HTTPS is already active; refusing to drop its resolver because DNS failed.' >&2
  exit 5
fi
dc=(docker compose --env-file "$base/secrets/runtime.env" -f "$release/deploy/nexostack/compose.yaml" "${domain_options[@]}")
"${dc[@]}" config --quiet
nice -n 15 ionice -c 2 -n 7 "${dc[@]}" build web
if docker container inspect vitalilab-db-lab >/dev/null 2>&1; then
  # Its init-script bind mount refers to the original release. A normal Compose up would
  # recreate PostgreSQL solely because the new release has a different host path.
  # Database configuration changes require a separate planned operation, not a UI release.
  [[ $(docker inspect -f '{{index .Config.Labels "com.docker.compose.project"}}' vitalilab-db-lab) == vitalilab-lab ]] || exit 6
  [[ $(docker inspect -f '{{.State.Health.Status}}' vitalilab-db-lab) == healthy ]] || exit 7
  [[ $(docker inspect -f '{{.Config.Image}}' vitalilab-db-lab) == postgres:18-alpine ]] || exit 8
else
  "${dc[@]}" up -d --wait --wait-timeout 90 db
fi
if [[ -L $base/current ]]; then
  "$base/current/deploy/nexostack/backup.sh"
fi
"${dc[@]}" run --no-deps --rm migrate
"${dc[@]}" exec -T db psql -U vitalilab_owner -d vitalilab_staging -v ON_ERROR_STOP=1 <<'SQL'
REVOKE ALL ON DATABASE vitalilab_staging FROM PUBLIC;
GRANT CONNECT ON DATABASE vitalilab_staging TO vitalilab_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON users, user_profiles, health_measurements,
  habits, habit_entries, announcements, audit_events, user_goals, daily_checkins,
  schools, school_groups, school_memberships, teacher_group_assignments, routine_completions,
  school_enrollment_requests, personal_routines, routine_exercises
  TO vitalilab_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO vitalilab_app;
GRANT SELECT ON alembic_version TO vitalilab_app;
SQL
"${dc[@]}" up -d --no-deps --wait --wait-timeout 90 web
ln -sfn "$release" "$base/current"
echo "VitaliLab release active: $sha"
