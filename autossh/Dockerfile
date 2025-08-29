FROM ghcr.io/securitybits-io/alpine:3.21.3

# Install OpenSSH server + AutoSSH
RUN apk add --no-cache \
              openssh \
              autossh bash \
              shadow \
              ca-certificates \
              sudo \
              curl \
              nmap \
              nano \
              && update-ca-certificates

# Create unprivileged user for SSH login
ARG USERNAME=tunnel
ARG UID=1000
RUN useradd -u ${UID} -m -s /bin/bash ${USERNAME}
RUN echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > "/etc/sudoers.d/${USERNAME}"
RUN usermod -U ${USERNAME}
RUN passwd -d ${USERNAME}

# Harden sshd a bit and ensure it runs
RUN mkdir -p /var/run/sshd /etc/ssh/keys && \
    sed -i \
      -e 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' \
      -e 's/^#\?PermitRootLogin.*/PermitRootLogin yes/' \
      -e 's/^#\?ChallengeResponseAuthentication.*/ChallengeResponseAuthentication no/' \
      -e 's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/' \
      -e 's/^#\?X11Forwarding.*/X11Forwarding no/' \
      /etc/ssh/sshd_config && \
    echo "GatewayPorts yes" >> /etc/ssh/sshd_config

# Defaults for AutoSSH behavior (can be overridden at runtime)
ENV AUTOSSH_GATETIME=0 \
    AUTOSSH_POLL=30 \
    AUTOSSH_FIRST_POLL=30 \
    AUTOSSH_LOGLEVEL=7

ENV REMOTE_SSH="" \
    REMOTE_PORT="" \
    REMOTE_SSH_PORT="22" \
    AUTOSSH_KEY_PATH="" \
    AUTHORIZED_KEYS="" \
    SSH_OPTS="-o StrictHostKeyChecking=accept-new -o ServerAliveInterval=30 -o ServerAliveCountMax=3"

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the container's SSH daemon (the reverse tunnel targets this)
EXPOSE 22

# Small healthcheck: is sshd running and socket present?
HEALTHCHECK --interval=30s --timeout=5s --retries=5 CMD pgrep -x sshd >/dev/null || exit 1

ENTRYPOINT ["/entrypoint.sh"]