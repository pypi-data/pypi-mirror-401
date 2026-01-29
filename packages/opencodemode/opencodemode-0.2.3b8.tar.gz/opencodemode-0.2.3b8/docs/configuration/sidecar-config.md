# Sidecar Configuration Reference

The `SidecarConfig` model defines how the executor sidecar operates, including server settings, security policies, execution limits, and callback configuration. This page documents all available configuration options.

## Configuration Fields

### Server Settings

#### port

- **Type:** `int`
- **Default:** `8001`
- **Description:** The port on which the gRPC server listens for incoming execution requests.

```yaml
port: 8001
```

#### host

- **Type:** `str`
- **Default:** `"0.0.0.0"`
- **Description:** The network interface to bind the server to. Use `0.0.0.0` to accept connections from any interface, or `127.0.0.1` for localhost only.

```yaml
host: "0.0.0.0"
```

#### main_app_grpc_target

- **Type:** `str`
- **Default:** `"localhost:50051"`
- **Description:** The gRPC target address for callbacks to the main application. Used when executed code needs to invoke tools or functions in the main app.

```yaml
main_app_grpc_target: "main-app:50051"
```

#### api_key

- **Type:** `str`
- **Optional**
- **Description:** The API key required for authenticating incoming requests. When set, all requests must include this key in the metadata. Leave unset to disable authentication (not recommended for production).

```yaml
api_key: "your-secure-api-key"
```

#### log_level

- **Type:** `str`
- **Values:** `"DEBUG"` | `"INFO"` | `"WARNING"` | `"ERROR"` | `"CRITICAL"`
- **Default:** `"INFO"`
- **Description:** The minimum log level for sidecar logs.

```yaml
log_level: INFO
```

### Execution Limits

The `limits` section controls resource limits for code execution.

#### limits.code_timeout

- **Type:** `int`
- **Default:** `30`
- **Description:** Maximum execution time in seconds for a single code execution. Executions exceeding this limit are terminated.

#### limits.max_code_length

- **Type:** `int`
- **Default:** `10000`
- **Description:** Maximum number of characters allowed in submitted code. Requests exceeding this limit are rejected.

```yaml
limits:
  code_timeout: 30
  max_code_length: 10000
```

### Security Configuration

The `security` section controls security policies for code execution.

#### security.allow_direct_execution

- **Type:** `bool`
- **Default:** `false`
- **Description:** Whether to allow direct code execution without sandboxing. When `false`, code is executed in a restricted environment. Enable with caution.

#### security.allowed_commands

- **Type:** `list[str]`
- **Default:** `[]`
- **Description:** List of shell commands that executed code is allowed to invoke. An empty list disables command execution entirely.

```yaml
security:
  allow_direct_execution: false
  allowed_commands:
    - python
    - pip
    - ls
```

### Server TLS Configuration

The `tls` section controls TLS/SSL settings for the gRPC server.

#### tls.enabled

- **Type:** `bool`
- **Default:** `false`
- **Description:** Whether to enable TLS for the gRPC server. When enabled, clients must connect using TLS.

#### tls.mode

- **Type:** `str`
- **Values:** `"system"` | `"custom"`
- **Default:** `"system"`
- **Description:** The TLS certificate mode.
  - `system`: Use system-provided certificates (typically for development)
  - `custom`: Use custom certificates specified in the configuration

#### tls.cert_file

- **Type:** `str`
- **Required:** When `enabled` is `true`
- **Description:** Path to the server certificate file (PEM format).

#### tls.key_file

- **Type:** `str`
- **Required:** When `enabled` is `true`
- **Description:** Path to the server private key file (PEM format).

#### tls.ca_file

- **Type:** `str`
- **Optional**
- **Description:** Path to the CA certificate file for client certificate verification. Required when `require_client_auth` is enabled.

#### tls.require_client_auth

- **Type:** `bool`
- **Default:** `false`
- **Description:** Whether to require clients to present a valid certificate (mutual TLS). When enabled, clients must provide a certificate signed by the CA specified in `ca_file`.

```yaml
tls:
  enabled: true
  mode: custom
  cert_file: /certs/server.crt
  key_file: /certs/server.key
  ca_file: /certs/ca.crt
  require_client_auth: true
```

### Callback TLS Configuration

The `callback_tls` section controls TLS settings for connections from the sidecar back to the main application.

#### callback_tls.enabled

- **Type:** `bool`
- **Default:** `false`
- **Description:** Whether to use TLS when connecting to the main application for callbacks.

#### callback_tls.ca_file

- **Type:** `str`
- **Optional**
- **Description:** Path to the CA certificate file for verifying the main application's server certificate.

#### callback_tls.client_cert

- **Type:** `str`
- **Optional**
- **Description:** Path to the client certificate file for mutual TLS with the main application.

#### callback_tls.client_key

- **Type:** `str`
- **Optional**
- **Description:** Path to the client private key file for mutual TLS with the main application.

```yaml
callback_tls:
  enabled: true
  ca_file: /certs/ca.crt
  client_cert: /certs/callback-client.crt
  client_key: /certs/callback-client.key
```

## Complete YAML Example

```yaml
# Server settings
port: 8001
host: "0.0.0.0"
main_app_grpc_target: "main-app:50051"
api_key: "production-api-key-here"
log_level: INFO

# Execution limits
limits:
  code_timeout: 30
  max_code_length: 10000

# Security policies
security:
  allow_direct_execution: false
  allowed_commands:
    - python
    - pip

# Server TLS (incoming connections)
tls:
  enabled: true
  mode: custom
  cert_file: /certs/server.crt
  key_file: /certs/server.key
  ca_file: /certs/ca.crt
  require_client_auth: true

# Callback TLS (outgoing connections to main app)
callback_tls:
  enabled: true
  ca_file: /certs/ca.crt
  client_cert: /certs/callback-client.crt
  client_key: /certs/callback-client.key
```

## Environment Variable Mapping

All sidecar configuration options can be set via environment variables. See the [Environment Variables Reference](environment-variables.md) for the complete mapping.

| Configuration Key | Environment Variable |
|-------------------|---------------------|
| `port` | `CODEMODE_SIDECAR_PORT` |
| `host` | `CODEMODE_SIDECAR_HOST` |
| `main_app_grpc_target` | `CODEMODE_MAIN_APP_GRPC_TARGET` |
| `api_key` | `CODEMODE_API_KEY` |
| `log_level` | `CODEMODE_LOG_LEVEL` |
| `limits.code_timeout` | `CODEMODE_CODE_TIMEOUT` |
| `limits.max_code_length` | `CODEMODE_MAX_CODE_LENGTH` |
| `security.allow_direct_execution` | `CODEMODE_ALLOW_DIRECT_EXECUTION` |
| `security.allowed_commands` | `CODEMODE_ALLOWED_COMMANDS` |
| `tls.enabled` | `CODEMODE_TLS_ENABLED` |
| `tls.mode` | `CODEMODE_TLS_MODE` |
| `tls.cert_file` | `CODEMODE_TLS_CERT_FILE` |
| `tls.key_file` | `CODEMODE_TLS_KEY_FILE` |
| `tls.ca_file` | `CODEMODE_TLS_CA_FILE` |
| `tls.require_client_auth` | `CODEMODE_TLS_REQUIRE_CLIENT_AUTH` |
| `callback_tls.enabled` | `CODEMODE_CALLBACK_TLS_ENABLED` |
| `callback_tls.ca_file` | `CODEMODE_CALLBACK_TLS_CA_FILE` |
| `callback_tls.client_cert` | `CODEMODE_CALLBACK_TLS_CLIENT_CERT` |
| `callback_tls.client_key` | `CODEMODE_CALLBACK_TLS_CLIENT_KEY` |

## Programmatic Usage

```python
from codemode.config import (
    SidecarConfig,
    LimitsConfig,
    SecurityConfig,
    SidecarTLSConfig,
    CallbackTLSConfig,
)

config = SidecarConfig(
    port=8001,
    host="0.0.0.0",
    main_app_grpc_target="main-app:50051",
    api_key="dev-key",
    log_level="DEBUG",
    limits=LimitsConfig(
        code_timeout=30,
        max_code_length=10000,
    ),
    security=SecurityConfig(
        allow_direct_execution=False,
        allowed_commands=["python", "pip"],
    ),
    tls=SidecarTLSConfig(
        enabled=False,
    ),
    callback_tls=CallbackTLSConfig(
        enabled=False,
    ),
)
```

## See Also

- [Configuration Overview](index.md)
- [Client Configuration Reference](client-config.md)
- [Environment Variables Reference](environment-variables.md)
