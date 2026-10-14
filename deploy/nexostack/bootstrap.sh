#!/bin/bash
set -euo pipefail
umask 077
[[ ${EUID} == 0 ]] || exit 1
base=/opt/labs/vitalilab
install -d -m 0700 "$base" "$base/secrets" "$base/backups" "$base/releases"
if [[ ! -e $base/secrets/runtime.env ]]; then
  printf 'POSTGRES_ADMIN_PASSWORD=%s\nPOSTGRES_APP_PASSWORD=%s\nSECRET_KEY=%s\n' \
    "$(openssl rand -hex 32)" "$(openssl rand -hex 32)" "$(openssl rand -hex 32)" \
    > "$base/secrets/runtime.env"
fi
if [[ ! -e $base/secrets/postgres-server.key ]]; then
  openssl req -x509 -newkey rsa:3072 -sha256 -days 365 -nodes \
    -keyout "$base/secrets/postgres-server.key" \
    -out "$base/secrets/postgres-server.crt" \
    -subj '/CN=db' -addext 'subjectAltName=DNS:db' 2>/dev/null
  cp "$base/secrets/postgres-server.crt" "$base/secrets/postgres-ca.crt"
  # The postgres user in the official Alpine image is uid/gid 70.
  chown 70:70 "$base/secrets/postgres-server.key"
  chmod 0600 "$base/secrets/postgres-server.key" "$base/secrets/runtime.env"
  chmod 0644 "$base/secrets/postgres-server.crt" "$base/secrets/postgres-ca.crt"
fi
echo 'Private VitaliLab configuration prepared; secrets were not printed.'
