# Configuration Overview

Codemode uses a flexible configuration system that supports multiple sources and provides sensible defaults for rapid development while allowing fine-grained control for production deployments.

## Configuration Models

Codemode provides two distinct configuration models, each tailored to its deployment context:

### ClientConfig

Used by the main application to configure how it communicates with the executor sidecar. This includes connection settings, retry behavior, TLS options, and observability preferences.

See [Client Configuration Reference](client-config.md) for complete documentation.

### SidecarConfig

Used by the executor sidecar to configure the gRPC server, security policies, execution limits, and callback settings to the main application.

See [Sidecar Configuration Reference](sidecar-config.md) for complete documentation.

## Configuration Sources

Configuration can be provided through three mechanisms, listed in order of precedence (highest to lowest):

### 1. Environment Variables

Environment variables take the highest precedence and override all other configuration sources. This is the recommended approach for containerized deployments and CI/CD pipelines.

```bash
export CODEMODE_EXECUTOR_URL="executor:8001"
export CODEMODE_EXECUTOR_API_KEY="your-api-key"
```

See [Environment Variables Reference](environment-variables.md) for the complete list.

### 2. YAML Configuration Files

YAML files provide a structured way to define configuration. By default, Codemode looks for `codemode.yaml` in the current working directory.

```yaml
executor_url: "localhost:8001"
executor_api_key: "dev-key"
executor_timeout: 30

retry:
  enabled: true
  max_attempts: 3
```

### 3. Programmatic Configuration

Configuration can be set directly in code, which is useful for testing or dynamic configuration scenarios.

```python
from codemode.config import ClientConfig

config = ClientConfig(
    executor_url="localhost:8001",
    executor_api_key="dev-key",
    executor_timeout=30,
)
```

## Configuration Loading Priority

When Codemode loads configuration, it merges values from all sources using the following priority order:

1. **Environment variables** (highest priority)
2. **YAML configuration file**
3. **Programmatic defaults** (lowest priority)

This means environment variables will override YAML settings, and YAML settings will override programmatic defaults.

### Example

Given the following configuration sources:

**codemode.yaml:**
```yaml
executor_url: "yaml-host:8001"
executor_timeout: 30
```

**Environment:**
```bash
export CODEMODE_EXECUTOR_URL="env-host:8001"
```

**Result:**
```python
# executor_url = "env-host:8001"  (from environment)
# executor_timeout = 30           (from YAML)
```

## Loading Configuration

Use the `ConfigLoader` class to load and merge configuration from all sources:

```python
from codemode.config import ConfigLoader

# Load client configuration
client_config = ConfigLoader.load_client_config()

# Load sidecar configuration
sidecar_config = ConfigLoader.load_sidecar_config()

# Load from a specific file
client_config = ConfigLoader.load_client_config(config_path="/path/to/config.yaml")
```

## Validation

All configuration models use Pydantic for validation. Invalid configuration values will raise a `ValidationError` with detailed information about the issue:

```python
from codemode.config import ClientConfig
from pydantic import ValidationError

try:
    config = ClientConfig(
        executor_url="localhost:8001",
        executor_api_key="key",
        executor_timeout=-1,  # Invalid: must be positive
    )
except ValidationError as e:
    print(e)
```

## Next Steps

- [Client Configuration Reference](client-config.md) - Complete ClientConfig documentation
- [Sidecar Configuration Reference](sidecar-config.md) - Complete SidecarConfig documentation
- [Environment Variables Reference](environment-variables.md) - All environment variables
