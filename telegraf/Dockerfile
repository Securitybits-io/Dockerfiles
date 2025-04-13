FROM telegraf:latest

ARG DUMB_INIT_VERSION=1.2.5

ARG BUILD_VERSION

RUN apt-get update && \
    apt-get install -y --no-install-recommends ipmitool snmp libsnmp-base && \
	rm -rf /var/lib/apt/lists/*