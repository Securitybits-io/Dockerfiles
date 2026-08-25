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
        libgcc


RUN apk add --no-cache --virtual .build-deps \
    build-base \
    python3-dev \
    libffi-dev

RUN python3 -m pip install \
        --break-system-packages \
        --no-cache-dir \
        curl_cffi==0.15.0

RUN curl -Lo /usr/local/bin/yt-dlp \
 "https://github.com/yt-dlp/yt-dlp/releases/download/${BUILD_VERSION}/yt-dlp" \
 && chmod a+rx /usr/local/bin/yt-dlp \
 && apk del curl

RUN apk del .build-deps

ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

RUN dumb-init yt-dlp --version

RUN python3 -c "import curl_cffi; print('curl_cffi:', curl_cffi.__version__)"
RUN python3 -c "import curl_cffi.requests; print('curl_cffi requests OK')"

RUN yt-dlp -v --list-impersonate-targets

ENTRYPOINT ["dumb-init", "yt-dlp"]
CMD ["--help"]