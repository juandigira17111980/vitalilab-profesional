#!/bin/bash
set -euo pipefail
umask 077
base=/opt/labs/vitalilab
[[ ${EUID} == 0 && -d $base/backups ]] || exit 1
[[ $(realpath -e "$base/backups") == /opt/labs/vitalilab/backups ]] || exit 2
exec 8>"$base/backup.lock"
flock -n 8 || { echo 'Another VitaliLab backup is active.' >&2; exit 3; }
stamp=$(date -u +%Y%m%dT%H%M%S%NZ)
target=$base/backups/vitalilab-$stamp.dump
docker exec vitalilab-db-lab pg_dump -U vitalilab_owner -d vitalilab_staging \
  --format=custom > "$target.part"
test -s "$target.part"
mv "$target.part" "$target"
sha256sum "$target" > "$target.sha256"
echo "Backup created: $(basename "$target")"
# Retention only touches this project's validated, explicit backup directory.
find /opt/labs/vitalilab/backups -maxdepth 1 -type f \
  -name 'vitalilab-*.dump*' -mtime +14 -delete
