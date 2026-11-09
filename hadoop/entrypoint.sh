#!/bin/bash
# Espera la llave pública de la API y la autoriza (en segundo plano)
AUTH=/home/hadoop/.ssh/authorized_keys
(
  for i in $(seq 1 60); do
    if [ -f /keys/id_ed25519.pub ]; then
      grep -qF "$(cat /keys/id_ed25519.pub)" "$AUTH" || cat /keys/id_ed25519.pub >> "$AUTH"
      chown hadoop:hadoop "$AUTH"
      chmod 600 "$AUTH"
      break
    fi
    sleep 2
  done
) &
# sshd en primer plano mantiene vivo el contenedor
exec /usr/sbin/sshd -D -e
