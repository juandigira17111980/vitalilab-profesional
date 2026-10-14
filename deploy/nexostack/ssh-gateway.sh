#!/bin/sh
set -eu
# No eval, shell arguments, interactive terminal, file transfer or Docker access.
case "${SSH_ORIGINAL_COMMAND:-status}" in
  status|health|restart|backup|events)
    exec /usr/bin/sudo -n /usr/local/sbin/vitalilab-ops "${SSH_ORIGINAL_COMMAND:-status}"
    ;;
  *) echo 'This key is restricted to VitaliLab operations.' >&2; exit 2 ;;
esac
