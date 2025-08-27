#!/usr/bin/env bash
set -euo pipefail

USERNAME="${USERNAME:-tunnel}"

# 1) Generate host keys if missing
if ! ls /etc/ssh/ssh_host_*key >/dev/null 2>&1; then
  echo "[init] Generating SSH host keys…"
  ssh-keygen -A
fi

# 2) Ensure authorized_keys for login user
mkdir -p "/home/${USERNAME}/.ssh"
chmod 700 "/home/${USERNAME}/.ssh"

if [ -s /run/secrets/authorized_keys ]; then
  cp /run/secrets/authorized_keys "/home/${USERNAME}/.ssh/authorized_keys"
elif [ -s /authorized_keys ]; then
  cp /authorized_keys "/home/${USERNAME}/.ssh/authorized_keys"
elif [ -n "${AUTHORIZED_KEYS:-}" ]; then
  printf "%s\n" "${AUTHORIZED_KEYS}" > "/home/${USERNAME}/.ssh/authorized_keys"
fi

if [ -f "/home/${USERNAME}/.ssh/authorized_keys" ]; then
  chown -R "${USERNAME}:${USERNAME}" "/home/${USERNAME}/.ssh"
  chmod 600 "/home/${USERNAME}/.ssh/authorized_keys"
else
  echo "[warn] No authorized_keys provided. You won't be able to SSH into the container."
fi

# 3) Start sshd (daemonizes by default on Alpine)
echo "[init] Starting sshd…"
mkdir -p /var/run/sshd
/usr/sbin/sshd

# 4) Build AutoSSH command
if [ -z "${REMOTE_SSH:-}" ] || [ -z "${REMOTE_PORT:-}" ]; then
  echo "[error] REMOTE_SSH and REMOTE_PORT must be set. Example:"
  echo "        docker run -e REMOTE_SSH='user@bastion.example.com' -e REMOTE_PORT='22222' IMAGE"
  exit 2
fi

SSH_CMD_OPTS=()
if [ -n "${AUTOSSH_KEY_PATH:-}" ]; then
  if [ -f "${AUTOSSH_KEY_PATH}" ]; then
    chmod 600 "${AUTOSSH_KEY_PATH}"
    SSH_CMD_OPTS+=("-i" "${AUTOSSH_KEY_PATH}")
  else
    echo "[warn] AUTOSSH_KEY_PATH set but file not found: ${AUTOSSH_KEY_PATH}"
  fi
fi

# Ensure localhost resolves inside container for the reverse target
TARGET="localhost:22"

echo "[init] Launching AutoSSH reverse tunnel:"
echo "       ${REMOTE_SSH}:${REMOTE_PORT}  <=  ${TARGET}"
echo "       (bastion port ${REMOTE_SSH_PORT})"

# 5) Run autossh in foreground (keeps container alive)
exec autossh -M 0 -N \
  -p "${REMOTE_SSH_PORT}" \
  -R "${REMOTE_PORT}:${TARGET}" \
  ${SSH_OPTS} \
  "${SSH_CMD_OPTS[@]}" \
  "${REMOTE_SSH}"