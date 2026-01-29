# Codemode Executor Sidecar Dockerfile
#
# This Dockerfile builds the codemode executor sidecar that runs code in isolation.
# It installs codemode from PyPI, making it usable without the full repo checkout.
#
# Build:
#   docker build -t codemode-executor .
#   docker build -t codemode-executor --build-arg CODEMODE_VERSION=0.2.0 .
#
# Run:
#   docker run -p 8001:8001 -e CODEMODE_API_KEY=your-key codemode-executor
#
# Documentation: https://github.com/mldlwizard/codemode

FROM python:3.11-slim

# Build arguments
ARG CODEMODE_VERSION=latest

# Labels for container metadata
LABEL org.opencontainers.image.title="Codemode Executor"
LABEL org.opencontainers.image.description="Secure code execution sidecar for multi-agent AI systems"
LABEL org.opencontainers.image.source="https://github.com/mldlwizard/codemode"
LABEL org.opencontainers.image.version="${CODEMODE_VERSION}"

# Install minimal system tools for optional direct execution
RUN apt-get update && apt-get install -y --no-install-recommends \
    grep \
    findutils \
    coreutils \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# Install opencodemode from PyPI
# If CODEMODE_VERSION is 'latest', install without version pin
# Otherwise, install the specified version
RUN if [ "${CODEMODE_VERSION}" = "latest" ]; then \
        pip install --no-cache-dir "opencodemode[grpc]"; \
    else \
        pip install --no-cache-dir "opencodemode[grpc]==${CODEMODE_VERSION}"; \
    fi

# Create necessary directories for execution
RUN mkdir -p /workspace /sandbox /outputs /tmp

# Create non-root user for security
RUN useradd -m -u 1000 executor && \
    chown -R executor:executor /app /sandbox /outputs /tmp /workspace

# Switch to non-root user
USER executor

# Expose gRPC port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.settimeout(5); s.connect(('localhost', 8001)); s.close()" || exit 1

# Run the executor service
# Configuration is loaded from:
#   1. /app/codemode-sidecar.yaml or /app/sidecar.yaml (if present)
#   2. Environment variables (CODEMODE_* prefix)
CMD ["python", "-m", "codemode.executor.service"]
