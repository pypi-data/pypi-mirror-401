# Docker Deployment

This guide covers deploying the codemode executor as a Docker container for isolated code execution in multi-agent AI systems.

## Building the Executor Image

The executor image is built from the `docker_sidecar/` directory:

```bash
# Build with latest codemode version
docker build -t codemode-executor docker_sidecar/

# Build with a specific version
docker build -t codemode-executor:0.2.0 \
  --build-arg CODEMODE_VERSION=0.2.0 \
  docker_sidecar/
```

The Dockerfile uses Python 3.11-slim as the base image and installs codemode from PyPI with gRPC support.

## Running the Executor Container

### Basic Usage

```bash
docker run -d \
  --name codemode-executor \
  -p 8001:8001 \
  -e CODEMODE_API_KEY=your-secure-api-key \
  codemode-executor
```

### Production Configuration

```bash
docker run -d \
  --name codemode-executor \
  -p 8001:8001 \
  -e CODEMODE_API_KEY=your-secure-api-key \
  -e CODEMODE_MAIN_APP_TARGET=host.docker.internal:50051 \
  -e CODEMODE_CODE_TIMEOUT=30 \
  -e CODEMODE_LOG_LEVEL=INFO \
  --security-opt no-new-privileges:true \
  --cap-drop ALL \
  --memory 512m \
  --cpus 1.0 \
  --read-only \
  --tmpfs /tmp:size=100M,mode=1777 \
  codemode-executor
```

## Environment Variables

The executor supports configuration through environment variables with the `CODEMODE_` prefix.

### Core Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `CODEMODE_API_KEY` | None | API key for authentication (required for production) |
| `CODEMODE_SIDECAR_PORT` | `8001` | gRPC server port |
| `CODEMODE_SIDECAR_HOST` | `0.0.0.0` | gRPC server host binding |
| `CODEMODE_MAIN_APP_TARGET` | `localhost:50051` | Main app gRPC target for tool callbacks |
| `CODEMODE_LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |

### Execution Limits

| Variable | Default | Description |
|----------|---------|-------------|
| `CODEMODE_CODE_TIMEOUT` | `30` | Maximum execution time in seconds (1-300) |
| `CODEMODE_MAX_CODE_LENGTH` | `10000` | Maximum code length in characters (100-100000) |

### Security Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `CODEMODE_ALLOW_DIRECT_EXECUTION` | `false` | Allow direct system commands |
| `CODEMODE_ALLOWED_COMMANDS` | Empty | Comma-separated list of allowed commands |

### TLS Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `CODEMODE_TLS_ENABLED` | `false` | Enable TLS encryption |
| `CODEMODE_TLS_MODE` | `system` | Certificate mode: `system` or `custom` |
| `CODEMODE_TLS_CERT_FILE` | None | Path to server certificate (PEM) |
| `CODEMODE_TLS_KEY_FILE` | None | Path to server private key (PEM) |
| `CODEMODE_TLS_CA_FILE` | None | Path to CA certificate for client verification |
| `CODEMODE_TLS_REQUIRE_CLIENT_AUTH` | `false` | Require mTLS client authentication |

### Callback TLS Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `CODEMODE_CALLBACK_TLS_ENABLED` | `false` | Enable TLS for callbacks to main app |
| `CODEMODE_CALLBACK_TLS_CA_FILE` | None | CA certificate for main app verification |
| `CODEMODE_CALLBACK_TLS_CLIENT_CERT` | None | Client certificate for mTLS callbacks |
| `CODEMODE_CALLBACK_TLS_CLIENT_KEY` | None | Client private key for mTLS callbacks |

## Volume Mounts

The executor container supports optional volume mounts for configuration and data:

```bash
docker run -d \
  --name codemode-executor \
  -p 8001:8001 \
  -e CODEMODE_API_KEY=your-secure-api-key \
  -v ./codemode-sidecar.yaml:/app/codemode-sidecar.yaml:ro \
  -v ./project_files:/workspace:ro \
  -v ./outputs:/outputs:rw \
  -v ./certs:/certs:ro \
  codemode-executor
```

| Mount Path | Purpose | Access |
|------------|---------|--------|
| `/app/codemode-sidecar.yaml` | Configuration file | Read-only |
| `/workspace` | Project files for code execution | Read-only |
| `/outputs` | Output directory for results | Read-write |
| `/certs` | TLS certificates | Read-only |
| `/sandbox` | Scratch space for execution | Read-write |

## Health Checks

The executor container includes a built-in health check that verifies the gRPC server is accepting connections on port 8001.

### Docker Health Check

The Dockerfile defines a health check that runs every 30 seconds:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.settimeout(5); s.connect(('localhost', 8001)); s.close()" || exit 1
```

### Checking Container Health

```bash
# View health status
docker inspect --format='{{.State.Health.Status}}' codemode-executor

# View health check logs
docker inspect --format='{{json .State.Health}}' codemode-executor | jq
```

### Health Status Values

- `starting`: Container is starting and health checks have not yet run
- `healthy`: Health check is passing
- `unhealthy`: Health check is failing

## Complete Example

The following example runs the executor with security hardening and resource limits:

```bash
docker run -d \
  --name codemode-executor \
  --restart unless-stopped \
  -p 8001:8001 \
  \
  # Authentication
  -e CODEMODE_API_KEY=your-secure-api-key \
  \
  # Callback configuration
  -e CODEMODE_MAIN_APP_TARGET=host.docker.internal:50051 \
  \
  # Execution limits
  -e CODEMODE_CODE_TIMEOUT=30 \
  -e CODEMODE_MAX_CODE_LENGTH=10000 \
  \
  # TLS (optional)
  -e CODEMODE_TLS_ENABLED=true \
  -e CODEMODE_TLS_MODE=custom \
  -e CODEMODE_TLS_CERT_FILE=/certs/server.crt \
  -e CODEMODE_TLS_KEY_FILE=/certs/server.key \
  -v ./certs:/certs:ro \
  \
  # Security hardening
  --security-opt no-new-privileges:true \
  --cap-drop ALL \
  --read-only \
  --tmpfs /tmp:size=100M,mode=1777 \
  \
  # Resource limits
  --memory 512m \
  --cpus 1.0 \
  \
  codemode-executor
```

## Next Steps

- [Docker Compose Setup](docker-compose.md) - Multi-service deployment with Docker Compose
- [Production Checklist](production.md) - Production deployment best practices
- [TLS Encryption](../features/tls-encryption.md) - Detailed TLS configuration guide
