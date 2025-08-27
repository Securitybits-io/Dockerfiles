# AutoSSH-Proxy

Dockerfile to build a simple AutoSSH-Proxy
```
docker run --rm \
  -p 2222:22 \
  -e REMOTE_SSH="tunnel@<IPADRESS TO BASTION>" \
  -e REMOTE_PORT="25022" \
  -e REMOTE_SSH_PORT="22" \
  -e AUTOSSH_KEY_PATH="/run/secrets/id_rsa" \
  -e AUTHORIZED_KEYS="<THE PUBLIC SSH KEY FOR AUTHING TO TUNNEL>" \
  -v $(pwd)/tunnel.id_rsa:/run/secrets/id_rsa \
  ghcr.io/securitybits-io/autossh:latest
```