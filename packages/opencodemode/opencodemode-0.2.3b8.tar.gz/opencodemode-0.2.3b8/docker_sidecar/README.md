# Codemode Executor Sidecar (Docker)

This bundle provides the hardened executor container used as the Codemode sidecar for secure code execution. The executor runs code in isolation, protecting your main application from untrusted code.

## Contents

```
docker_sidecar/
├── Dockerfile              # Builds the executor image from PyPI
├── docker-compose.yml      # Docker Compose configuration with security hardening
└── README.md               # This guide
```

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Set your API key
export CODEMODE_API_KEY=your-secret-key

# Start the executor
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f executor
```

### Option 2: Docker Build & Run

```bash
# Build the image (installs codemode from PyPI)
docker build -t codemode-executor .

# Or build with specific version
docker build -t codemode-executor --build-arg CODEMODE_VERSION=0.2.0 .

# Run the container
docker run -d \
  --name codemode-executor \
  --add-host=host.docker.internal:host-gateway \
  -p 8001:8001 \
  -e CODEMODE_API_KEY=your-secret-key \
  -e MAIN_APP_GRPC_TARGET=host.docker.internal:50051 \
  codemode-executor
```

### Option 3: Docker Compose with Config Bridge

```bash
# Generate .env from your codemode.yaml
codemode docker env --config codemode.yaml --output .env

# Start with docker-compose
docker-compose --env-file .env -f docker_sidecar/docker-compose.yml up -d
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CODEMODE_API_KEY` | Yes | - | API key for authentication |
| `MAIN_APP_GRPC_TARGET` | No | `localhost:50051` | ToolService gRPC URL |
| `CODEMODE_SIDECAR_PORT` | No | `8001` | Port for gRPC service |
| `CODEMODE_SIDECAR_HOST` | No | `0.0.0.0` | Host to bind to |
| `CODEMODE_CODE_TIMEOUT` | No | `30` | Max execution time in seconds |
| `CODEMODE_MAX_CODE_LENGTH` | No | `10000` | Max code length in characters |
| `CODEMODE_ALLOW_DIRECT_EXECUTION` | No | `false` | Allow direct command execution |
| `CODEMODE_LOG_LEVEL` | No | `INFO` | Log level (DEBUG, INFO, WARNING, ERROR) |
| `EXECUTOR_NETWORK_MODE` | No | `none` | Code execution network mode |

## TLS Configuration

For TLS/mTLS, set these environment variables:

```bash
# Enable TLS
CODEMODE_TLS_ENABLED=true
CODEMODE_TLS_MODE=custom
CODEMODE_TLS_CERT_FILE=/certs/server.crt
CODEMODE_TLS_KEY_FILE=/certs/server.key
CODEMODE_TLS_CA_FILE=/certs/ca.crt

# For mTLS (require client certificates)
CODEMODE_TLS_REQUIRE_CLIENT_AUTH=true
```

Mount your certificates:
```yaml
volumes:
  - ./certs:/certs:ro
```

## Configuration File

Instead of environment variables, you can use a YAML configuration file:

```bash
# Create config
codemode init sidecar

# Mount in container
docker run -v ./codemode-sidecar.yaml:/app/codemode-sidecar.yaml:ro ...
```

## Generating Config from codemode.yaml

Use the CLI to generate a `.env` file that bridges your `codemode.yaml` to Docker:

```bash
codemode docker env --config codemode.yaml --output .env
```

This creates a `.env` file with all required environment variables, automatically converting `localhost` to `host.docker.internal` for Docker networking.

## Exporting This Bundle

If codemode is installed via PyPI, export the sidecar bundle:

```bash
# Using CLI
codemode docker assets --dest ./executor-sidecar

# Or using Python module
python -m codemode.docker_assets export --dest ./executor-sidecar
```

Then build from the exported directory:

```bash
cd executor-sidecar
docker build -t codemode-executor .
```

## Security Features

- **Non-root user**: Runs as UID 1000 (`executor` user)
- **Minimal base image**: Python 3.11 slim with only essential tools
- **Dropped capabilities**: All capabilities dropped (`--cap-drop ALL`)
- **No privilege escalation**: `--security-opt=no-new-privileges:true`
- **Resource limits**: CPU and memory limits enforced
- **Network isolation**: Can run with `--network=none` for full isolation

## Connecting from Main App

Your main application connects to the executor using the `ClientConfig`:

```python
from codemode import Codemode
from codemode.config import ClientConfig

# From environment variables
codemode = Codemode.from_env()

# Or from config file
config = ClientConfig.from_yaml("codemode-client.yaml")
codemode = Codemode.from_client_config(config)

# Execute code
result = codemode.execute("print('Hello from executor!')")
```

## Troubleshooting

### Check if container is running
```bash
docker ps | grep codemode-executor
```

### View logs
```bash
docker logs codemode-executor
docker logs -f codemode-executor  # Follow logs
```

### Test connectivity
```bash
# From host (if using default port)
grpcurl -plaintext localhost:8001 list

# Or use Python
python -c "import socket; s=socket.socket(); s.connect(('localhost', 8001)); print('Connected!'); s.close()"
```

### Common issues

1. **"Connection refused"**: Ensure container is running and port mapping is correct
2. **"API key invalid"**: Ensure `CODEMODE_API_KEY` matches between client and sidecar
3. **"TLS handshake failed"**: Check certificate paths and permissions

## Notes

- Runs as non-root (UID 1000) with minimal tools (`grep`, `findutils`, `coreutils`)
- `--add-host` is required for Docker to resolve `host.docker.internal` on Linux

## Documentation

- [Configuration Guide](https://github.com/mldlwizard/codemode/blob/main/docs/configuration/index.md)
- [TLS Setup](https://github.com/mldlwizard/codemode/blob/main/docs/features/tls-encryption.md)
- [Deployment Guide](https://github.com/mldlwizard/codemode/blob/main/docs/deployment/docker.md)
