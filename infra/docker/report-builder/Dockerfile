# Reproducible LaTeX build environment for the report — no host install
# required. Pulls the official static tectonic binary from GitHub
# Releases, checksum-verified, rather than a random third-party image.
FROM debian:bookworm-slim

ARG TECTONIC_VERSION=0.17.0
ARG TARGETARCH

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

# sha256 of the official release tarballs (tectonic-typesetting/tectonic),
# recomputed locally at pin time — verified against no official checksums
# file being published, so this is the checksum of what was downloaded and
# pinned into this Dockerfile.
RUN set -eux; \
    case "${TARGETARCH}" in \
      amd64) ARCH="x86_64-unknown-linux-musl"; SHA256="8533d07f9ccbd7a65824b9e0459041bca34af1eb33daba48f59215593753a3b7" ;; \
      arm64) ARCH="aarch64-unknown-linux-musl"; SHA256="b10954a95404f3ab2328d2fa59a5ebab8e657f893fab096f98be8db7c0c979b8" ;; \
      *) echo "unsupported TARGETARCH: ${TARGETARCH}" >&2; exit 1 ;; \
    esac; \
    URL="https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%40${TECTONIC_VERSION}/tectonic-${TECTONIC_VERSION}-${ARCH}.tar.gz"; \
    curl -fsSL -o /tmp/tectonic.tar.gz "${URL}"; \
    echo "${SHA256}  /tmp/tectonic.tar.gz" | sha256sum -c -; \
    tar -xzf /tmp/tectonic.tar.gz -C /usr/local/bin; \
    rm /tmp/tectonic.tar.gz

WORKDIR /workspace
ENTRYPOINT ["tectonic"]
