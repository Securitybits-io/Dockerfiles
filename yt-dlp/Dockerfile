FROM ghcr.io/securitybits-io/alpine:3.21.3

ARG DUMB_INIT_VERSION=1.2.5
ARG BUILD_VERSION

RUN set -x \
 && apk update \
 && apk upgrade -a \
 && apk add --no-cache \
        ca-certificates \
        curl \
        dumb-init \
        ffmpeg \
        python3 \
        py3-pip \
        py3-mutagen \
        libstdc++ \
 && python3 -m pip install \
        --break-system-packages \
        --no-cache-dir \
        "curl_cffi>=0.10,<0.16" \
 && curl -Lo /usr/local/bin/yt-dlp \
        "https://github.com/yt-dlp/yt-dlp/releases/download/${BUILD_VERSION}/yt-dlp" \
 && chmod a+rx /usr/local/bin/yt-dlp \
 && apk del curl

ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

RUN dumb-init yt-dlp --version
RUN yt-dlp --list-impersonate-targets

ENTRYPOINT ["dumb-init", "yt-dlp"]
CMD ["--help"]