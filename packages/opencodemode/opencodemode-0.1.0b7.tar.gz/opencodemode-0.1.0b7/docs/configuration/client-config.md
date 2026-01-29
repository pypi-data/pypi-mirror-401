# Client Configuration Reference

The `ClientConfig` model defines how the main application connects to and communicates with the executor sidecar. This page documents all available configuration options.

## Configuration Fields

### Connection Settings

#### executor_url

- **Type:** `str`
- **Required:** Yes
- **Description:** The URL of the executor sidecar service. This should include the host and port but not the protocol scheme (gRPC handles this internally).

```yaml
executor_url: "localhost:8001"
```

#### executor_api_key

- **Type:** `str`
- **Required:** Yes
- **Description:** The API key used for authenticating requests to the executor sidecar. This must match the `api_key` configured on the sidecar.

```yaml
executor_api_key: "your-secure-api-key"
```

#### executor_timeout

- **Type:** `int`
- **Default:** `35`
- **Description:** The maximum time in seconds to wait for a response from the executor. This should be set higher than the sidecar's `code_timeout` to account for network latency and overhead.

```yaml
executor_timeout: 35
```

#### max_code_length

- **Type:** `int`
- **Default:** `10000`
- **Description:** The maximum number of characters allowed in code submissions. Requests exceeding this limit will be rejected before being sent to the executor.

```yaml
max_code_length: 10000
```

### Retry Configuration

The `retry` section controls automatic retry behavior for failed requests.

#### retry.enabled

- **Type:** `bool`
- **Default:** `true`
- **Description:** Whether to automatically retry failed requests. When enabled, transient failures will be retried according to the configured policy.

#### retry.max_attempts

- **Type:** `int`
- **Default:** `3`
- **Description:** The maximum number of retry attempts before giving up. The total number of requests will be `max_attempts + 1` (initial request plus retries).

#### retry.backoff_base_ms

- **Type:** `int`
- **Default:** `100`
- **Description:** The base delay in milliseconds between retry attempts. Actual delay uses exponential backoff: `base * 2^attempt`.

#### retry.backoff_max_ms

- **Type:** `int`
- **Default:** `5000`
- **Description:** The maximum delay in milliseconds between retry attempts. Backoff delay is capped at this value.

```yaml
retry:
  enabled: true
  max_attempts: 3
  backoff_base_ms: 100
  backoff_max_ms: 5000
```

### TLS Configuration

The `tls` section controls TLS/SSL settings for secure communication with the executor.

#### tls.enabled

- **Type:** `bool`
- **Default:** `false`
- **Description:** Whether to use TLS for the connection to the executor. When enabled, all communication is encrypted.

#### tls.mode

- **Type:** `str`
- **Values:** `"system"` | `"custom"`
- **Default:** `"system"`
- **Description:** The TLS certificate verification mode.
  - `system`: Use system-installed CA certificates
  - `custom`: Use custom certificates specified in the configuration

#### tls.ca_file

- **Type:** `str`
- **Required:** When `mode` is `"custom"`
- **Description:** Path to the CA certificate file for verifying the server's certificate.

#### tls.client_cert_file

- **Type:** `str`
- **Optional**
- **Description:** Path to the client certificate file for mutual TLS authentication. Required if the sidecar has `require_client_auth` enabled.

#### tls.client_key_file

- **Type:** `str`
- **Optional**
- **Description:** Path to the client private key file for mutual TLS authentication.

```yaml
tls:
  enabled: true
  mode: custom
  ca_file: /certs/ca.crt
  client_cert_file: /certs/client.crt
  client_key_file: /certs/client.key
```

### Observability Configuration

The `observability` section controls logging and debugging behavior.

#### observability.log_level

- **Type:** `str`
- **Values:** `"DEBUG"` | `"INFO"` | `"WARNING"` | `"ERROR"` | `"CRITICAL"`
- **Default:** `"INFO"`
- **Description:** The minimum log level for codemode client logs.

#### observability.include_correlation_id

- **Type:** `bool`
- **Default:** `true`
- **Description:** Whether to include correlation IDs in requests for distributed tracing. Correlation IDs help track requests across service boundaries.

#### observability.correlation_id_prefix

- **Type:** `str`
- **Default:** `"codemode"`
- **Description:** Prefix for generated correlation IDs. Useful for filtering logs in multi-service environments.

#### observability.traceback_limit

- **Type:** `int`
- **Default:** `10`
- **Description:** Maximum number of stack frames to include in error tracebacks.

```yaml
observability:
  log_level: DEBUG
  include_correlation_id: true
  correlation_id_prefix: my-app
  traceback_limit: 10
```

## Complete YAML Example

```yaml
# Connection settings
executor_url: "executor:8001"
executor_api_key: "production-api-key-here"
executor_timeout: 35
max_code_length: 10000

# Retry configuration
retry:
  enabled: true
  max_attempts: 3
  backoff_base_ms: 100
  backoff_max_ms: 5000

# TLS configuration
tls:
  enabled: true
  mode: custom
  ca_file: /certs/ca.crt
  client_cert_file: /certs/client.crt
  client_key_file: /certs/client.key

# Observability
observability:
  log_level: INFO
  include_correlation_id: true
  correlation_id_prefix: codemode
  traceback_limit: 10
```

## Environment Variable Mapping

All client configuration options can be set via environment variables. See the [Environment Variables Reference](environment-variables.md) for the complete mapping.

| Configuration Key | Environment Variable |
|-------------------|---------------------|
| `executor_url` | `CODEMODE_EXECUTOR_URL` |
| `executor_api_key` | `CODEMODE_EXECUTOR_API_KEY` |
| `executor_timeout` | `CODEMODE_EXECUTOR_TIMEOUT` |
| `max_code_length` | `CODEMODE_MAX_CODE_LENGTH` |
| `retry.enabled` | `CODEMODE_RETRY_ENABLED` |
| `retry.max_attempts` | `CODEMODE_RETRY_MAX_ATTEMPTS` |
| `retry.backoff_base_ms` | `CODEMODE_RETRY_BACKOFF_BASE_MS` |
| `retry.backoff_max_ms` | `CODEMODE_RETRY_BACKOFF_MAX_MS` |
| `tls.enabled` | `CODEMODE_TLS_ENABLED` |
| `tls.mode` | `CODEMODE_TLS_MODE` |
| `tls.ca_file` | `CODEMODE_TLS_CA_FILE` |
| `tls.client_cert_file` | `CODEMODE_TLS_CLIENT_CERT_FILE` |
| `tls.client_key_file` | `CODEMODE_TLS_CLIENT_KEY_FILE` |
| `observability.log_level` | `CODEMODE_LOG_LEVEL` |
| `observability.include_correlation_id` | `CODEMODE_INCLUDE_CORRELATION_ID` |
| `observability.correlation_id_prefix` | `CODEMODE_CORRELATION_ID_PREFIX` |
| `observability.traceback_limit` | `CODEMODE_TRACEBACK_LIMIT` |

## Programmatic Usage

```python
from codemode.config import ClientConfig, RetryConfig, TLSConfig, ObservabilityConfig

config = ClientConfig(
    executor_url="localhost:8001",
    executor_api_key="dev-key",
    executor_timeout=30,
    max_code_length=10000,
    retry=RetryConfig(
        enabled=True,
        max_attempts=3,
        backoff_base_ms=100,
        backoff_max_ms=5000,
    ),
    tls=TLSConfig(
        enabled=False,
    ),
    observability=ObservabilityConfig(
        log_level="DEBUG",
        include_correlation_id=True,
    ),
)
```

## See Also

- [Configuration Overview](index.md)
- [Sidecar Configuration Reference](sidecar-config.md)
- [Environment Variables Reference](environment-variables.md)
