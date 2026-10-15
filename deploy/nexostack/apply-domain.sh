#!/bin/bash
# Routing-only release: no DB recreation, migrations, shared proxy restart or DNS writes.
set -euo pipefail
umask 077
[[ $EUID == 0 && $# -ge 1 && $# -le 2 ]] || exit 1
sha=$1
[[ $sha =~ ^[0-9a-f]{40}$ ]] || exit 2
[[ ${2:-} == '' || ${2:-} == --require-dns ]] || exit 3
base=/opt/labs/vitalilab
release=$base/releases/$sha
[[ $(realpath -e "$base/releases") == /opt/labs/vitalilab/releases ]] || exit 4
[[ $(realpath -e "$release") == "$release" && -f $release/wsgi.py ]] || exit 5
[[ -L $base/current && -f $base/secrets/runtime.env ]] || exit 6
exec 9>"$base/deploy.lock"
flock -n 9 || { echo 'Another VitaliLab deployment is active.' >&2; exit 8; }
previous=$(readlink -f "$base/current")
[[ $previous == /opt/labs/vitalilab/releases/* ]] || exit 7
# A routing-only release must not smuggle application/dependency/schema changes.
diff -qr "$previous/app" "$release/app" >/dev/null
diff -qr "$previous/migrations" "$release/migrations" >/dev/null
cmp "$previous/requirements.txt" "$release/requirements.txt"
cmp "$previous/wsgi.py" "$release/wsgi.py"
domain_options=()
if python3 "$release/scripts/check_domain_dns.py"; then
  domain_options=(-f "$release/deploy/nexostack/domain-https.yaml")
elif [[ ${2:-} == --require-dns ]]; then
  echo 'DNS is not ready. No service was modified.' >&2
  exit 9
fi
export RELEASE_SHA=$sha
dc=(docker compose --env-file "$base/secrets/runtime.env" -f "$release/deploy/nexostack/compose.yaml" "${domain_options[@]}")
"${dc[@]}" config --quiet
nice -n 15 ionice -c 2 -n 7 "${dc[@]}" build web
"$previous/deploy/nexostack/backup.sh"
"${dc[@]}" up -d --no-deps --wait --wait-timeout 90 web
ln -sfn "$release" "$base/current"
echo "VitaliLab domain routing prepared: $sha"
if [[ ${#domain_options[@]} == 0 ]]; then
  echo 'Main-domain HTTPS is pending DNS and a subsequent --require-dns activation.'
fi
