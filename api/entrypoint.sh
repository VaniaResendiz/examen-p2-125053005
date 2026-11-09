#!/bin/sh
set -e
mkdir -p /root/.ssh
# Genera la llave solo si no existe todavía (sin contraseña)
if [ ! -f /keys/id_ed25519 ]; then
  ssh-keygen -t ed25519 -N "" -f /keys/id_ed25519 -C "api@datamart"
fi
chmod 600 /keys/id_ed25519
chmod 644 /keys/id_ed25519.pub
printf "Host hadoop\n  User hadoop\n  IdentityFile /keys/id_ed25519\n  StrictHostKeyChecking no\n  UserKnownHostsFile /dev/null\n" > /root/.ssh/config
chmod 600 /root/.ssh/config
# Ejecuta el comando del contenedor (python app.py)
exec "$@"
