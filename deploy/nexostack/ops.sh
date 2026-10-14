#!/bin/bash
set -euo pipefail
PATH=/usr/sbin:/usr/bin:/sbin:/bin
export PATH
unset DOCKER_HOST DOCKER_CONTEXT DOCKER_CONFIG
[[ ${EUID} == 0 && $# == 1 ]] || exit 2
case "$1" in
  status)
    docker inspect vitalilab-web-lab vitalilab-db-lab \
      --format '{{.Name}} status={{.State.Status}} health={{.State.Health.Status}} restarts={{.RestartCount}}'
    ;;
  health)
    curl --fail --silent --show-error --max-time 15 https://vitalilab.lab.nexostack.app/health
    printf '\n'
    curl --fail --silent --show-error --max-time 15 https://vitalilab.lab.nexostack.app/ready
    printf '\n'
    ;;
  restart)
    docker restart --time 30 vitalilab-web-lab >/dev/null
    echo 'Only the VitaliLab web container was restarted.'
    ;;
  backup)
    /opt/labs/vitalilab/current/deploy/nexostack/backup.sh
    ;;
  events)
    journalctl -u vitalilab-check.service -n 15 --no-pager
    ;;
  *) echo 'Allowed operations: status, health, restart, backup, events.' >&2; exit 2 ;;
esac
