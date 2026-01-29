# Config Module API

The `codemode.config` module provides configuration models and loaders for both client applications and the executor sidecar. All configuration supports YAML files and environment variable overrides.

## ClientConfig

Configuration for main applications that connect to the codemode executor sidecar.

```python
from codemode.config import ClientConfig
```

### Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `executor_url` | `str` | Required | Executor service URL |
| `executor_api_key` | `str` | Required | API key for authentication |
| `executor_timeout` | `int` | `35` | Request timeout in seconds (1-600) |
| `max_code_length` | `int` | `10000` | Maximum code length in characters (100-100000) |
| `retry` | `RetryConfig` | See below | Retry configuration |
| `tls` | `TlsClientConfig` | See below | TLS configuration |
| `observability` | `ObservabilityConfig` | See below | Logging and tracing configuration |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CODEMODE_EXECUTOR_URL` | Executor service URL |
| `CODEMODE_EXECUTOR_API_KEY` | API key for authentication |
| `CODEMODE_EXECUTOR_TIMEOUT` | Request timeout in seconds |
| `CODEMODE_MAX_CODE_LENGTH` | Maximum code length |

### Example

```python
from codemode.config import ClientConfig

config = ClientConfig(
    executor_url="http://executor:8001",
    executor_api_key="secret-key",
    executor_timeout=30,
    retry=RetryConfig(enabled=True, max_attempts=3)
)
```

### Class Methods

#### from_env

```python
@classmethod
def from_env() -> ClientConfig
```

Create ClientConfig from environment variables only.

**Returns:** `ClientConfig` instance populated from environment variables

**Raises:**

- `ValueError`: If required environment variables are missing

**Example:**

```python
import os
os.environ["CODEMODE_EXECUTOR_URL"] = "http://executor:8001"
os.environ["CODEMODE_EXECUTOR_API_KEY"] = "secret"
config = ClientConfig.from_env()
```

---

## RetryConfig

Retry configuration for transient failures.

```python
from codemode.config.client_config import RetryConfig
```

### Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `enabled` | `bool` | `True` | Enable automatic retry |
| `max_attempts` | `int` | `3` | Maximum retry attempts (1-10) |
| `backoff_base_ms` | `int` | `100` | Base backoff time in milliseconds (10-10000) |
| `backoff_max_ms` | `int` | `5000` | Maximum backoff time in milliseconds (100-60000) |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CODEMODE_RETRY_ENABLED` | Enable retry (`true`/`false`) |
| `CODEMODE_RETRY_MAX_ATTEMPTS` | Maximum retry attempts |
| `CODEMODE_RETRY_BACKOFF_BASE_MS` | Base backoff time in ms |
| `CODEMODE_RETRY_BACKOFF_MAX_MS` | Maximum backoff time in ms |

---

## TlsClientConfig

TLS configuration for client connections to the executor.

```python
from codemode.config.client_config import TlsClientConfig
```

### Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `enabled` | `bool` | `False` | Enable TLS encryption |
| `mode` | `Literal["system", "custom"]` | `"system"` | Certificate mode |
| `ca_file` | `str \| None` | `None` | CA certificate for server verification |
| `client_cert_file` | `str \| None` | `None` | Client certificate for mTLS |
| `client_key_file` | `str \| None` | `None` | Client private key for mTLS |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CODEMODE_TLS_ENABLED` | Enable TLS (`true`/`false`) |
| `CODEMODE_TLS_MODE` | `system` or `custom` |
| `CODEMODE_TLS_CA_FILE` | CA certificate path |
| `CODEMODE_TLS_CLIENT_CERT_FILE` | Client certificate path |
| `CODEMODE_TLS_CLIENT_KEY_FILE` | Client key path |

---

## ObservabilityConfig

Observability and logging configuration.

```python
from codemode.config.client_config import ObservabilityConfig
```

### Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `log_level` | `str` | `"INFO"` | Logging level |
| `include_correlation_id` | `bool` | `True` | Include correlation IDs in requests |
| `correlation_id_prefix` | `str` | `"cm"` | Prefix for generated correlation IDs (1-8 chars) |
| `traceback_limit` | `int` | `5` | Max traceback frames in errors (0-50) |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CODEMODE_LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `CODEMODE_INCLUDE_CORRELATION_ID` | Include correlation IDs (`true`/`false`) |
| `CODEMODE_CORRELATION_ID_PREFIX` | Correlation ID prefix |
| `CODEMODE_TRACEBACK_LIMIT` | Max traceback frames |

---

## SidecarConfig

Configuration for the executor sidecar service.

```python
from codemode.config import SidecarConfig
```

### Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `port` | `int` | `8001` | gRPC server port (1-65535) |
| `host` | `str` | `"0.0.0.0"` | gRPC server host binding |
| `main_app_grpc_target` | `str` | `"localhost:50051"` | Main app gRPC target for callbacks |
| `api_key` | `str \| None` | `None` | API key for authentication |
| `limits` | `ExecutionLimitsConfig` | See below | Execution limits |
| `security` | `SecurityConfig` | See below | Security settings |
| `tls` | `TlsServerConfig` | See below | TLS configuration for gRPC server |
| `callback_tls` | `CallbackTlsConfig` | See below | TLS for callbacks to main app |
| `log_level` | `str` | `"INFO"` | Logging level |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CODEMODE_SIDECAR_PORT` | gRPC server port |
| `CODEMODE_SIDECAR_HOST` | gRPC server host |
| `CODEMODE_MAIN_APP_TARGET` | Main app gRPC target |
| `CODEMODE_API_KEY` | API key |
| `CODEMODE_LOG_LEVEL` | Logging level |

### Class Methods

#### from_env

```python
@classmethod
def from_env() -> SidecarConfig
```

Create SidecarConfig from environment variables only.

**Returns:** `SidecarConfig` instance

**Example:**

```python
import os
os.environ["CODEMODE_API_KEY"] = "secret"
config = SidecarConfig.from_env()
```

#### get_grpc_address

```python
def get_grpc_address() -> str
```

Get the full gRPC address for server binding.

**Returns:** Address string in format `host:port`

---

## ExecutionLimitsConfig

Execution limits for code safety.

```python
from codemode.config.sidecar_config import ExecutionLimitsConfig
```

### Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `code_timeout` | `int` | `30` | Maximum execution time in seconds (1-300) |
| `max_code_length` | `int` | `10000` | Maximum code length in characters (100-100000) |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CODEMODE_CODE_TIMEOUT` | Max execution time in seconds |
| `CODEMODE_MAX_CODE_LENGTH` | Max code length in characters |

---

## SecurityConfig

Security settings for code execution.

```python
from codemode.config.sidecar_config import SecurityConfig
```

### Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `allow_direct_execution` | `bool` | `False` | Allow direct system commands |
| `allowed_commands` | `list[str]` | `[]` | Allowed system commands |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CODEMODE_ALLOW_DIRECT_EXECUTION` | Allow direct execution (`true`/`false`) |
| `CODEMODE_ALLOWED_COMMANDS` | Comma-separated list of allowed commands |

---

## TlsServerConfig

TLS configuration for the sidecar gRPC server.

```python
from codemode.config.sidecar_config import TlsServerConfig
```

### Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `enabled` | `bool` | `False` | Enable TLS encryption |
| `mode` | `Literal["system", "custom"]` | `"system"` | Certificate mode |
| `cert_file` | `str \| None` | `None` | Server certificate path |
| `key_file` | `str \| None` | `None` | Server private key path |
| `ca_file` | `str \| None` | `None` | CA certificate for client verification |
| `require_client_auth` | `bool` | `False` | Require mTLS client authentication |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CODEMODE_TLS_ENABLED` | Enable TLS |
| `CODEMODE_TLS_MODE` | `system` or `custom` |
| `CODEMODE_TLS_CERT_FILE` | Server certificate path |
| `CODEMODE_TLS_KEY_FILE` | Server private key path |
| `CODEMODE_TLS_CA_FILE` | CA certificate path |
| `CODEMODE_TLS_REQUIRE_CLIENT_AUTH` | Require mTLS |

---

## ConfigLoader

Loads and parses Codemode configuration files with environment variable substitution.

```python
from codemode.config import ConfigLoader
```

### Class Methods

#### load

```python
@classmethod
def load(config_path: str | Path) -> CodemodeConfig
```

Load legacy configuration from a YAML file.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `config_path` | `str \| Path` | Path to configuration file |

**Returns:** Validated `CodemodeConfig` instance

**Raises:**

- `FileNotFoundError`: If config file doesn't exist
- `ConfigLoadError`: If file is invalid

**Example:**

```python
config = ConfigLoader.load("codemode.yaml")
```

---

#### load_client_config

```python
@classmethod
def load_client_config(config_path: str | Path) -> ClientConfig
```

Load client configuration from a YAML file.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `config_path` | `str \| Path` | Path to `codemode-client.yaml` |

**Returns:** Validated `ClientConfig` instance

**Raises:**

- `FileNotFoundError`: If config file doesn't exist
- `ConfigLoadError`: If file is invalid

**Example:**

```python
config = ConfigLoader.load_client_config("codemode-client.yaml")
print(config.executor_url)
```

---

#### load_sidecar_config

```python
@classmethod
def load_sidecar_config(config_path: str | Path) -> SidecarConfig
```

Load sidecar configuration from a YAML file.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `config_path` | `str \| Path` | Path to `codemode-sidecar.yaml` |

**Returns:** Validated `SidecarConfig` instance

**Raises:**

- `FileNotFoundError`: If config file doesn't exist
- `ConfigLoadError`: If file is invalid

**Example:**

```python
config = ConfigLoader.load_sidecar_config("codemode-sidecar.yaml")
print(config.port)
```

---

## Environment Variable Substitution

Configuration files support environment variable substitution using the `${VAR_NAME}` syntax.

### Basic Substitution

```yaml
executor:
  api_key: ${CODEMODE_API_KEY}
```

### Default Values

```yaml
executor:
  timeout: ${CODEMODE_TIMEOUT:-30}
```

If `CODEMODE_TIMEOUT` is not set, the value `30` is used.

### Example Configuration Files

#### codemode-client.yaml

```yaml
executor_url: ${CODEMODE_EXECUTOR_URL:-http://localhost:8001}
executor_api_key: ${CODEMODE_EXECUTOR_API_KEY}
executor_timeout: 35

retry:
  enabled: true
  max_attempts: 3
  backoff_base_ms: 100
  backoff_max_ms: 5000

tls:
  enabled: false
  mode: system

observability:
  log_level: INFO
  include_correlation_id: true
  correlation_id_prefix: cm
  traceback_limit: 5
```

#### codemode-sidecar.yaml

```yaml
port: 8001
host: 0.0.0.0
main_app_grpc_target: ${MAIN_APP_TARGET:-localhost:50051}
api_key: ${CODEMODE_API_KEY}

limits:
  code_timeout: 30
  max_code_length: 10000

security:
  allow_direct_execution: false
  allowed_commands: []

tls:
  enabled: false
  mode: system

callback_tls:
  enabled: false

log_level: INFO
```

---

## Exceptions

### ConfigLoadError

Raised when configuration loading fails.

```python
from codemode.config.loader import ConfigLoadError
```
