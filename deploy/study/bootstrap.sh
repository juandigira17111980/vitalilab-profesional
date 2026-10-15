#!/usr/bin/env bash
# Operator only: creates ONE separate study instance, never touches the web stack.
set -euo pipefail
umask 077
ROOT=/opt/labs/vitalilab-study-ega1026
DB=vitalilab_estudio_ega1026
CONTAINER=vitalilab-study-db-ega1026
test "$(id -u)" = 0
test "$(realpath "$(dirname "$0")")" = "$ROOT"
cd "$ROOT"
test ! -e initialized
if docker container inspect "$CONTAINER" >/dev/null 2>&1; then
  echo 'STOP: study container already exists; operator review required' >&2
  exit 1
fi
if ss -lntH | awk '{print $4}' | grep -Eq '(^|:)55432$'; then
  echo 'STOP: local port 55432 is occupied' >&2
  exit 1
fi
docker ps -q --no-trunc | sort > baseline.ids
mkdir -m 700 secrets
mkdir -m 755 tls
openssl rand -hex 32 > secrets/owner_password
openssl req -x509 -newkey rsa:2048 -sha256 -nodes -days 365 \
  -keyout tls/server.key -out tls/server.crt \
  -subj '/CN=localhost' -addext 'subjectAltName=DNS:localhost,IP:127.0.0.1' \
  >/dev/null 2>&1
PG_UID=$(docker run --rm --network none --entrypoint id postgres:18-alpine -u postgres)
PG_GID=$(docker run --rm --network none --entrypoint id postgres:18-alpine -g postgres)
chown "$PG_UID:$PG_GID" tls/server.key
chmod 600 tls/server.key
chmod 644 tls/server.crt
docker compose -f compose.yaml config --quiet
docker compose -f compose.yaml up -d --no-deps db
for attempt in $(seq 1 30); do
  if docker exec "$CONTAINER" pg_isready -U study_owner -d "$DB" >/dev/null 2>&1; then
    break
  fi
  sleep 2
done
docker exec "$CONTAINER" pg_isready -U study_owner -d "$DB"
for file in estructura_postgresql.sql datos_ficticios.sql roles.sql; do
  docker exec -i "$CONTAINER" psql -X -U study_owner -d "$DB" \
    -v ON_ERROR_STOP=1 -f - < "$file" > "$file.log"
done
while IFS= read -r existing_id; do
  test "$(docker inspect -f '{{.State.Running}}' "$existing_id")" = true
done < baseline.ids
date -u +%FT%TZ > initialized
echo 'Study instance initialized. Learner role remains NOLOGIN. Existing containers still running.'
