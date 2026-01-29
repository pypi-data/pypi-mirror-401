# Environment Variables Reference

This page provides a complete reference of all environment variables supported by Codemode. Environment variables take precedence over YAML configuration files.

## Client Configuration Variables

These variables configure the main application's connection to the executor sidecar.

### Connection Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CODEMODE_EXECUTOR_URL` | string | - | Executor sidecar URL (required) |
| `CODEMODE_EXECUTOR_API_KEY` | string | - | API key for authentication (required) |
| `CODEMODE_EXECUTOR_TIMEOUT` | integer | `35` | Request timeout in seconds |
| `CODEMODE_MAX_CODE_LENGTH` | integer | `10000` | Maximum code length in characters |

### Retry Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CODEMODE_RETRY_ENABLED` | boolean | `true` | Enable automatic retries |
| `CODEMODE_RETRY_MAX_ATTEMPTS` | integer | `3` | Maximum retry attempts |
| `CODEMODE_RETRY_BACKOFF_BASE_MS` | integer | `100` | Base backoff delay in milliseconds |
| `CODEMODE_RETRY_BACKOFF_MAX_MS` | integer | `5000` | Maximum backoff delay in milliseconds |

### Client TLS Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CODEMODE_TLS_ENABLED` | boolean | `false` | Enable TLS for executor connection |
| `CODEMODE_TLS_MODE` | string | `system` | TLS mode: `system` or `custom` |
| `CODEMODE_TLS_CA_FILE` | string | - | Path to CA certificate file |
| `CODEMODE_TLS_CLIENT_CERT_FILE` | string | - | Path to client certificate file |
| `CODEMODE_TLS_CLIENT_KEY_FILE` | string | - | Path to client private key file |

### Observability Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CODEMODE_LOG_LEVEL` | string | `INFO` | Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `CODEMODE_INCLUDE_CORRELATION_ID` | boolean | `true` | Include correlation IDs in requests |
| `CODEMODE_CORRELATION_ID_PREFIX` | string | `codemode` | Prefix for correlation IDs |
| `CODEMODE_TRACEBACK_LIMIT` | integer | `10` | Maximum traceback frames in errors |

## Sidecar Configuration Variables

These variables configure the executor sidecar service.

### Server Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CODEMODE_SIDECAR_PORT` | integer | `8001` | gRPC server port |
| `CODEMODE_SIDECAR_HOST` | string | `0.0.0.0` | Server bind address |
| `CODEMODE_MAIN_APP_GRPC_TARGET` | string | `localhost:50051` | Main app callback target |
| `CODEMODE_API_KEY` | string | - | API key for authentication |
| `CODEMODE_LOG_LEVEL` | string | `INFO` | Log level |

### Execution Limits

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CODEMODE_CODE_TIMEOUT` | integer | `30` | Code execution timeout in seconds |
| `CODEMODE_MAX_CODE_LENGTH` | integer | `10000` | Maximum code length in characters |

### Security Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CODEMODE_ALLOW_DIRECT_EXECUTION` | boolean | `false` | Allow unsandboxed execution |
| `CODEMODE_ALLOWED_COMMANDS` | string | - | Comma-separated list of allowed commands |

### Sidecar TLS Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CODEMODE_TLS_ENABLED` | boolean | `false` | Enable TLS for gRPC server |
| `CODEMODE_TLS_MODE` | string | `system` | TLS mode: `system` or `custom` |
| `CODEMODE_TLS_CERT_FILE` | string | - | Path to server certificate file |
| `CODEMODE_TLS_KEY_FILE` | string | - | Path to server private key file |
| `CODEMODE_TLS_CA_FILE` | string | - | Path to CA certificate file |
| `CODEMODE_TLS_REQUIRE_CLIENT_AUTH` | boolean | `false` | Require client certificates (mTLS) |

### Callback TLS Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CODEMODE_CALLBACK_TLS_ENABLED` | boolean | `false` | Enable TLS for callbacks |
| `CODEMODE_CALLBACK_TLS_CA_FILE` | string | - | Path to callback CA certificate |
| `CODEMODE_CALLBACK_TLS_CLIENT_CERT` | string | - | Path to callback client certificate |
| `CODEMODE_CALLBACK_TLS_CLIENT_KEY` | string | - | Path to callback client key |

## Boolean Value Formats

Boolean environment variables accept the following values:

- **True:** `true`, `1`, `yes`, `on`
- **False:** `false`, `0`, `no`, `off`

Values are case-insensitive.

## List Value Formats

List values (such as `CODEMODE_ALLOWED_COMMANDS`) use comma-separated format:

```bash
export CODEMODE_ALLOWED_COMMANDS="python,pip,ls,cat"
```

## Docker Compose Examples

### Development Configuration

```yaml
version: "3.8"

services:
  main-app:
    build: .
    environment:
      - CODEMODE_EXECUTOR_URL=executor:8001
      - CODEMODE_EXECUTOR_API_KEY=dev-key
      - CODEMODE_EXECUTOR_TIMEOUT=30
      - CODEMODE_LOG_LEVEL=DEBUG
      - CODEMODE_RETRY_ENABLED=true
    depends_on:
      - executor

  executor:
    image: codemode/executor:latest
    environment:
      - CODEMODE_SIDECAR_PORT=8001
      - CODEMODE_API_KEY=dev-key
      - CODEMODE_MAIN_APP_GRPC_TARGET=main-app:50051
      - CODEMODE_CODE_TIMEOUT=30
      - CODEMODE_LOG_LEVEL=DEBUG
      - CODEMODE_ALLOW_DIRECT_EXECUTION=false
    ports:
      - "8001:8001"
```

### Production Configuration with TLS

```yaml
version: "3.8"

services:
  main-app:
    build: .
    environment:
      - CODEMODE_EXECUTOR_URL=executor:8001
      - CODEMODE_EXECUTOR_API_KEY=${CODEMODE_API_KEY}
      - CODEMODE_EXECUTOR_TIMEOUT=35
      - CODEMODE_LOG_LEVEL=INFO
      - CODEMODE_TLS_ENABLED=true
      - CODEMODE_TLS_MODE=custom
      - CODEMODE_TLS_CA_FILE=/certs/ca.crt
      - CODEMODE_TLS_CLIENT_CERT_FILE=/certs/client.crt
      - CODEMODE_TLS_CLIENT_KEY_FILE=/certs/client.key
    volumes:
      - ./certs:/certs:ro
    depends_on:
      - executor

  executor:
    image: codemode/executor:latest
    environment:
      - CODEMODE_SIDECAR_PORT=8001
      - CODEMODE_SIDECAR_HOST=0.0.0.0
      - CODEMODE_API_KEY=${CODEMODE_API_KEY}
      - CODEMODE_MAIN_APP_GRPC_TARGET=main-app:50051
      - CODEMODE_CODE_TIMEOUT=30
      - CODEMODE_MAX_CODE_LENGTH=10000
      - CODEMODE_LOG_LEVEL=INFO
      - CODEMODE_ALLOW_DIRECT_EXECUTION=false
      - CODEMODE_ALLOWED_COMMANDS=python,pip
      - CODEMODE_TLS_ENABLED=true
      - CODEMODE_TLS_MODE=custom
      - CODEMODE_TLS_CERT_FILE=/certs/server.crt
      - CODEMODE_TLS_KEY_FILE=/certs/server.key
      - CODEMODE_TLS_CA_FILE=/certs/ca.crt
      - CODEMODE_TLS_REQUIRE_CLIENT_AUTH=true
      - CODEMODE_CALLBACK_TLS_ENABLED=true
      - CODEMODE_CALLBACK_TLS_CA_FILE=/certs/ca.crt
      - CODEMODE_CALLBACK_TLS_CLIENT_CERT=/certs/callback-client.crt
      - CODEMODE_CALLBACK_TLS_CLIENT_KEY=/certs/callback-client.key
    volumes:
      - ./certs:/certs:ro
    ports:
      - "8001:8001"
```

### Minimal Configuration

For quick testing with minimal configuration:

```yaml
version: "3.8"

services:
  main-app:
    build: .
    environment:
      - CODEMODE_EXECUTOR_URL=executor:8001
      - CODEMODE_EXECUTOR_API_KEY=test-key
    depends_on:
      - executor

  executor:
    image: codemode/executor:latest
    environment:
      - CODEMODE_API_KEY=test-key
```

## Shell Script Examples

### Exporting Variables

```bash
#!/bin/bash

# Client configuration
export CODEMODE_EXECUTOR_URL="localhost:8001"
export CODEMODE_EXECUTOR_API_KEY="your-api-key"
export CODEMODE_EXECUTOR_TIMEOUT=30
export CODEMODE_LOG_LEVEL="DEBUG"

# TLS configuration
export CODEMODE_TLS_ENABLED="true"
export CODEMODE_TLS_MODE="custom"
export CODEMODE_TLS_CA_FILE="/path/to/ca.crt"
```

### Using .env Files

Create a `.env` file:

```bash
# .env
CODEMODE_EXECUTOR_URL=localhost:8001
CODEMODE_EXECUTOR_API_KEY=your-api-key
CODEMODE_EXECUTOR_TIMEOUT=30
CODEMODE_TLS_ENABLED=false
CODEMODE_LOG_LEVEL=INFO
```

Load with:

```bash
source .env
# or with Docker Compose
docker-compose --env-file .env up
```

## See Also

- [Configuration Overview](index.md)
- [Client Configuration Reference](client-config.md)
- [Sidecar Configuration Reference](sidecar-config.md)
