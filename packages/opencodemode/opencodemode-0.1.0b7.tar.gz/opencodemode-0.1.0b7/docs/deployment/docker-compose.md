# Docker Compose Setup

This guide covers deploying codemode with Docker Compose, including the main application and executor sidecar services.

## Basic Configuration

A minimal Docker Compose setup with a main application and executor sidecar:

```yaml
version: "3.8"

services:
  # Main application (your AI agent orchestrator)
  main-app:
    build: .
    ports:
      - "8000:8000"
      - "50051:50051"
    environment:
      - CODEMODE_API_KEY=${CODEMODE_API_KEY:-dev-secret-key}
      - EXECUTOR_URL=http://executor:8001
    depends_on:
      executor:
        condition: service_healthy
    networks:
      - codemode

  # Executor sidecar (isolated code execution)
  executor:
    build:
      context: ./docker_sidecar
      dockerfile: Dockerfile
    ports:
      - "8001:8001"
    environment:
      - CODEMODE_API_KEY=${CODEMODE_API_KEY:-dev-secret-key}
      - CODEMODE_MAIN_APP_TARGET=main-app:50051
      - CODEMODE_CODE_TIMEOUT=30
      - CODEMODE_LOG_LEVEL=INFO
    networks:
      - codemode
    healthcheck:
      test: ["CMD", "python", "-c", "import socket; s=socket.socket(); s.settimeout(5); s.connect(('localhost', 8001)); s.close()"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

networks:
  codemode:
    driver: bridge
```

## Production Configuration

A production-ready configuration with security hardening and resource limits:

```yaml
version: "3.8"

services:
  main-app:
    build: .
    ports:
      - "8000:8000"
      - "50051:50051"
    environment:
      - CODEMODE_API_KEY=${CODEMODE_API_KEY}
      - EXECUTOR_URL=http://executor:8001
    depends_on:
      executor:
        condition: service_healthy
    networks:
      - codemode
    restart: unless-stopped

  executor:
    build:
      context: ./docker_sidecar
      dockerfile: Dockerfile
      args:
        CODEMODE_VERSION: ${CODEMODE_VERSION:-latest}
    image: codemode-executor:${CODEMODE_VERSION:-latest}
    container_name: codemode-executor

    environment:
      # Authentication
      - CODEMODE_API_KEY=${CODEMODE_API_KEY}

      # Callback configuration
      - CODEMODE_MAIN_APP_TARGET=main-app:50051

      # Execution limits
      - CODEMODE_CODE_TIMEOUT=${CODEMODE_CODE_TIMEOUT:-30}
      - CODEMODE_MAX_CODE_LENGTH=${CODEMODE_MAX_CODE_LENGTH:-10000}

      # Security
      - CODEMODE_ALLOW_DIRECT_EXECUTION=false

      # Logging
      - CODEMODE_LOG_LEVEL=${CODEMODE_LOG_LEVEL:-INFO}

    ports:
      - "8001:8001"

    # Security hardening
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    read_only: false
    tmpfs:
      - /tmp:size=100M,mode=1777

    # Resource limits
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 128M

    # Health check
    healthcheck:
      test: ["CMD", "python", "-c", "import socket; s=socket.socket(); s.settimeout(5); s.connect(('localhost', 8001)); s.close()"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

    networks:
      - codemode
    restart: unless-stopped

networks:
  codemode:
    driver: bridge
```

## TLS-Enabled Configuration

For production environments requiring encrypted communication:

```yaml
version: "3.8"

services:
  main-app:
    build: .
    ports:
      - "8000:8000"
      - "50051:50051"
    environment:
      - CODEMODE_API_KEY=${CODEMODE_API_KEY}
      - CODEMODE_TLS_ENABLED=true
      - CODEMODE_TLS_CERT_FILE=/certs/server.crt
      - CODEMODE_TLS_KEY_FILE=/certs/server.key
      - CODEMODE_TLS_CA_FILE=/certs/ca.crt
    volumes:
      - ./certs:/certs:ro
    depends_on:
      executor:
        condition: service_healthy
    networks:
      - executor-network
    restart: unless-stopped

  executor:
    build:
      context: ./docker_sidecar
      dockerfile: Dockerfile
    environment:
      - CODEMODE_API_KEY=${CODEMODE_API_KEY}
      - CODEMODE_MAIN_APP_TARGET=main-app:50051

      # Server TLS configuration
      - CODEMODE_TLS_ENABLED=true
      - CODEMODE_TLS_MODE=custom
      - CODEMODE_TLS_CERT_FILE=/certs/executor.crt
      - CODEMODE_TLS_KEY_FILE=/certs/executor.key
      - CODEMODE_TLS_CA_FILE=/certs/ca.crt

      # mTLS (optional - enable for mutual authentication)
      # - CODEMODE_TLS_REQUIRE_CLIENT_AUTH=true

      # Callback TLS for connecting to main app
      - CODEMODE_CALLBACK_TLS_ENABLED=true
      - CODEMODE_CALLBACK_TLS_CA_FILE=/certs/ca.crt
      # - CODEMODE_CALLBACK_TLS_CLIENT_CERT=/certs/client.crt
      # - CODEMODE_CALLBACK_TLS_CLIENT_KEY=/certs/client.key

    volumes:
      - ./certs:/certs:ro

    # Security hardening
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=100m

    # Resource limits
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M

    networks:
      - executor-network
    restart: unless-stopped

    healthcheck:
      test: ["CMD", "python", "-c", "import socket; s=socket.socket(); s.settimeout(5); s.connect(('localhost', 8001)); s.close()"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

networks:
  # Isolated network with no external access
  executor-network:
    driver: bridge
    internal: true
```

## Network Isolation

For maximum security, use an internal network that prevents the executor from accessing external resources:

```yaml
networks:
  # Isolated network - no external internet access
  executor-network:
    driver: bridge
    internal: true

  # Public network for main app (if needed)
  public:
    driver: bridge
```

Then attach services appropriately:

```yaml
services:
  main-app:
    networks:
      - public
      - executor-network

  executor:
    networks:
      - executor-network  # No access to public network
```

## Secrets Management with Docker Secrets

For production deployments, use Docker secrets instead of environment variables for sensitive data:

```yaml
version: "3.8"

services:
  main-app:
    build: .
    secrets:
      - codemode_api_key
    environment:
      - CODEMODE_API_KEY_FILE=/run/secrets/codemode_api_key
    networks:
      - codemode

  executor:
    build:
      context: ./docker_sidecar
      dockerfile: Dockerfile
    secrets:
      - codemode_api_key
    environment:
      - CODEMODE_API_KEY_FILE=/run/secrets/codemode_api_key
      - CODEMODE_MAIN_APP_TARGET=main-app:50051
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    networks:
      - codemode

secrets:
  codemode_api_key:
    file: ./secrets/api_key.txt

networks:
  codemode:
    driver: bridge
```

### Creating Secrets Files

```bash
# Create secrets directory
mkdir -p secrets

# Generate a secure API key
openssl rand -base64 32 > secrets/api_key.txt

# Set restrictive permissions
chmod 600 secrets/api_key.txt
```

## Volume Mounts for Data Sharing

Configure volumes for workspace access and output storage:

```yaml
services:
  executor:
    volumes:
      # Configuration (read-only)
      - ./codemode-sidecar.yaml:/app/codemode-sidecar.yaml:ro

      # Project files for code execution (read-only)
      - ./project_files:/workspace:ro

      # Output directory for results (read-write)
      - ./outputs:/outputs:rw

      # TLS certificates (read-only)
      - ./certs:/certs:ro

volumes:
  # Sandbox volume with size limit
  executor-sandbox:
    driver: local
    driver_opts:
      type: tmpfs
      device: tmpfs
      o: size=1024m
```

## Running the Stack

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service health
docker-compose ps

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

## Environment File

Create a `.env` file for configuration:

```bash
# .env
CODEMODE_API_KEY=your-secure-api-key-here
CODEMODE_VERSION=latest
CODEMODE_CODE_TIMEOUT=30
CODEMODE_MAX_CODE_LENGTH=10000
CODEMODE_LOG_LEVEL=INFO
```

Ensure the `.env` file is not committed to version control:

```bash
echo ".env" >> .gitignore
```

## Next Steps

- [Production Checklist](production.md) - Security and reliability best practices
- [Docker Deployment](docker.md) - Single container deployment
- [TLS Encryption](../features/tls-encryption.md) - Certificate configuration details
