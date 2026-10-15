#!/bin/bash
# Roll back compatible application code only. Keep the additive schema and all records.
set -euo pipefail
umask 077
[[ $EUID == 0 && $# == 1 ]] || exit 1
sha=$1
[[ $sha =~ ^[0-9a-f]{40}$ ]] || exit 2
base=/opt/labs/vitalilab
release=$base/releases/$sha
[[ $(realpath -e "$base/releases") == /opt/labs/vitalilab/releases ]] || exit 3
[[ $(realpath -e "$release") == "$release" && -f $release/wsgi.py ]] || exit 4
[[ -L $base/current && -f $base/secrets/runtime.env ]] || exit 5
exec 9>"$base/deploy.lock"
flock -n 9 || exit 6
# This is not a general downgrade mechanism. The administrator must verify code/schema
# compatibility against the current schema before selecting a previous image.
docker image inspect "vitalilab-lab:$sha" >/dev/null
[[ $(docker inspect -f '{{index .Config.Labels "com.docker.compose.project"}}' vitalilab-db-lab) == vitalilab-lab ]] || exit 7
[[ $(docker inspect -f '{{.State.Health.Status}}' vitalilab-db-lab) == healthy ]] || exit 8
domain_options=()
if python3 "$release/scripts/check_domain_dns.py"; then
  domain_options=(-f "$release/deploy/nexostack/domain-https.yaml")
elif [[ $(docker inspect -f '{{index .Config.Labels "traefik.http.routers.vitalilab-main-https.tls.certresolver"}}' vitalilab-web-lab) == letsencrypt ]]; then
  echo 'DNS check failed; refusing to remove active principal HTTPS.' >&2
  exit 9
fi
export RELEASE_SHA=$sha
dc=(docker compose --env-file "$base/secrets/runtime.env" -f "$release/deploy/nexostack/compose.yaml" "${domain_options[@]}")
"${dc[@]}" config --quiet
"$base/current/deploy/nexostack/backup.sh"
"${dc[@]}" up -d --no-build --no-deps --wait --wait-timeout 90 web
ln -sfn "$release" "$base/current"
echo "Compatible web code restored: $sha; database and additive schema preserved."
