# Core Module API

The `codemode.core` module provides the primary interfaces for code execution. This includes the main `Codemode` class, the `ExecutorClient` for gRPC communication, and the `ComponentRegistry` for managing tools and agents.

## Codemode

The main entry point for the codemode library. Manages configuration, component registry, and executor communication.

```python
from codemode import Codemode
from codemode.config import ClientConfig
```

### Constructor

```python
Codemode(
    config: CodemodeConfig | None = None,
    registry: ComponentRegistry | None = None,
    client_config: ClientConfig | None = None,
    executor_client: ExecutorClient | None = None
)
```

Initialize a Codemode instance.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `config` | `CodemodeConfig \| None` | Legacy CodemodeConfig object (mutually exclusive with `client_config`) |
| `registry` | `ComponentRegistry \| None` | Optional existing registry. Creates new if `None` |
| `client_config` | `ClientConfig \| None` | New-style ClientConfig (recommended) |
| `executor_client` | `ExecutorClient \| None` | Optional pre-configured ExecutorClient |

**Raises:**

- `ValueError`: If neither `config` nor `client_config` is provided

**Example:**

```python
from codemode.config import ClientConfig

client_config = ClientConfig(
    executor_url="http://executor:8001",
    executor_api_key="secret-key"
)
codemode = Codemode(client_config=client_config)
```

---

### Class Methods

#### from_client_config

```python
@classmethod
def from_client_config(
    config: ClientConfig | None = None,
    registry: ComponentRegistry | None = None,
    config_path: str | Path | None = None
) -> Codemode
```

Create a Codemode instance from ClientConfig. This is the recommended initialization method.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `config` | `ClientConfig \| None` | ClientConfig object |
| `registry` | `ComponentRegistry \| None` | Optional existing registry |
| `config_path` | `str \| Path \| None` | Path to `codemode-client.yaml` |

**Returns:** Configured `Codemode` instance

**Raises:**

- `ValueError`: If environment variables are missing when loading from env

**Example:**

```python
# From explicit config
config = ClientConfig(
    executor_url="http://executor:8001",
    executor_api_key="secret-key"
)
codemode = Codemode.from_client_config(config)

# From YAML file
codemode = Codemode.from_client_config(config_path="codemode-client.yaml")

# From environment variables
codemode = Codemode.from_client_config()
```

---

#### from_env

```python
@classmethod
def from_env(registry: ComponentRegistry | None = None) -> Codemode
```

Create a Codemode instance from environment variables.

**Required Environment Variables:**

- `CODEMODE_EXECUTOR_URL`: Executor service URL
- `CODEMODE_EXECUTOR_API_KEY`: API key for authentication

**Returns:** Configured `Codemode` instance

**Example:**

```python
import os
os.environ["CODEMODE_EXECUTOR_URL"] = "http://executor:8001"
os.environ["CODEMODE_EXECUTOR_API_KEY"] = "secret"
codemode = Codemode.from_env()
```

---

#### from_config

```python
@classmethod
def from_config(
    config_path: str | Path,
    registry: ComponentRegistry | None = None
) -> Codemode
```

Create a Codemode instance from a legacy configuration file.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `config_path` | `str \| Path` | Path to `codemode.yaml` |
| `registry` | `ComponentRegistry \| None` | Optional existing registry |

**Returns:** Configured `Codemode` instance

**Raises:**

- `FileNotFoundError`: If config file not found
- `ConfigLoadError`: If config is invalid

**Example:**

```python
codemode = Codemode.from_config("codemode.yaml")
print(codemode.config.project.name)
```

---

### Instance Methods

#### execute

```python
def execute(
    code: str,
    execution_timeout: int | None = None
) -> str
```

Execute Python code synchronously.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `code` | `str` | Python code to execute |
| `execution_timeout` | `int \| None` | Custom timeout in seconds. Uses config default if `None` |

**Returns:** Execution result as string

**Raises:**

- `ExecutorClientError`: If execution fails

**Example:**

```python
result = codemode.execute("result = 2 + 2")
print(result)  # '4'

# With tools
code = """
weather = tools['weather'].run(location='NYC')
result = {'weather': weather}
"""
result = codemode.execute(code)
```

---

#### execute_async

```python
async def execute_async(
    code: str,
    execution_timeout: int | None = None
) -> str
```

Execute Python code asynchronously.

**Parameters:** Same as `execute()`

**Returns:** Execution result as string

**Example:**

```python
result = await codemode.execute_async("result = 2 + 2")
```

---

#### as_crewai_tool

```python
def as_crewai_tool() -> CodemodeTool
```

Get Codemode as a CrewAI tool for use with CrewAI agents.

**Returns:** `CodemodeTool` instance

**Raises:**

- `ImportError`: If CrewAI is not installed

**Example:**

```python
tool = codemode.as_crewai_tool()

from crewai import Agent
agent = Agent(
    role="Orchestrator",
    tools=[tool],
    backstory="You write Python code"
)
```

---

#### with_context

```python
def with_context(**variables) -> Codemode
```

Set runtime context with variables. Supports fluent API chaining.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `**variables` | `Any` | Dynamic variables (client_id, user_id, etc.) |

**Returns:** Self for method chaining

**Example:**

```python
codemode.with_context(
    client_id="acme",
    user_id="user_123",
    session_id="sess_456"
)
```

---

#### health_check

```python
def health_check() -> bool
```

Check if the executor service is healthy.

**Returns:** `True` if executor is healthy, `False` otherwise

**Example:**

```python
if codemode.health_check():
    print("Executor is healthy")
```

---

#### ready_check

```python
def ready_check() -> bool
```

Check if the executor is ready and can reach the main application.

**Returns:** `True` if executor is ready, `False` otherwise

**Example:**

```python
if codemode.ready_check():
    print("Executor is ready")
```

---

#### close

```python
def close() -> None
```

Close resources and the executor client's connection.

**Example:**

```python
codemode.close()

# Or use as context manager
with Codemode.from_client_config(config) as codemode:
    result = codemode.execute("result = 42")
```

---

## ExecutorClient

Client for communicating with the executor sidecar via gRPC. Provides automatic retry with exponential backoff and correlation ID support.

```python
from codemode.core import ExecutorClient
```

### Constructor

```python
ExecutorClient(
    executor_url: str,
    api_key: str,
    timeout: int = 35,
    tls_config: GrpcTlsConfig | None = None,
    retry_enabled: bool = True,
    retry_max_attempts: int = 3,
    retry_backoff_base_ms: int = 100,
    retry_backoff_max_ms: int = 5000,
    retry_status_codes: list[grpc.StatusCode] | None = None,
    include_correlation_id: bool = True,
    correlation_id_prefix: str = "cm"
)
```

**Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `executor_url` | `str` | - | URL of the executor service |
| `api_key` | `str` | - | API key for authentication |
| `timeout` | `int` | `35` | Request timeout in seconds |
| `tls_config` | `GrpcTlsConfig \| None` | `None` | TLS configuration |
| `retry_enabled` | `bool` | `True` | Enable automatic retry |
| `retry_max_attempts` | `int` | `3` | Maximum retry attempts |
| `retry_backoff_base_ms` | `int` | `100` | Base backoff time in milliseconds |
| `retry_backoff_max_ms` | `int` | `5000` | Maximum backoff time in milliseconds |
| `retry_status_codes` | `list[grpc.StatusCode] \| None` | `None` | gRPC status codes to retry on |
| `include_correlation_id` | `bool` | `True` | Auto-generate correlation IDs |
| `correlation_id_prefix` | `str` | `"cm"` | Prefix for correlation IDs |

**Example:**

```python
client = ExecutorClient(
    executor_url="http://executor:8001",
    api_key="secret-key",
    retry_max_attempts=5,
    correlation_id_prefix="myapp"
)
```

---

### Methods

#### execute

```python
def execute(
    code: str,
    available_tools: list[str],
    config: dict[str, Any],
    execution_timeout: int = 30,
    context: RuntimeContext | None = None,
    correlation_id: str | None = None
) -> ExecutionResult
```

Execute code in the executor service with automatic retry.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `code` | `str` | Python code to execute |
| `available_tools` | `list[str]` | List of tool names available for use |
| `config` | `dict[str, Any]` | Configuration dictionary |
| `execution_timeout` | `int` | Timeout for code execution |
| `context` | `RuntimeContext \| None` | Optional runtime context to inject |
| `correlation_id` | `str \| None` | Optional correlation ID (auto-generated if not provided) |

**Returns:** `ExecutionResult` with execution outcome

**Raises:**

- `ExecutorTimeoutError`: If request times out after all retries
- `ExecutorConnectionError`: If connection fails after all retries
- `ExecutorClientError`: For other gRPC errors

**Example:**

```python
result = client.execute(
    code="result = tools['weather'].run(location='NYC')",
    available_tools=["weather"],
    config={},
    correlation_id="req-abc123"
)
print(result.correlation_id)  # 'req-abc123'
```

---

#### health_check

```python
def health_check() -> bool
```

Check if the executor service is healthy.

**Returns:** `True` if healthy, `False` otherwise

---

#### ready_check

```python
def ready_check() -> bool
```

Check if the executor can reach the main application.

**Returns:** `True` if ready, `False` otherwise

---

#### close

```python
def close() -> None
```

Close the gRPC channel. This method is idempotent and thread-safe.

---

#### execute_async

```python
async def execute_async(
    code: str,
    available_tools: list[str],
    config: dict[str, Any],
    execution_timeout: int = 30,
    context: RuntimeContext | None = None,
    correlation_id: str | None = None
) -> ExecutionResult
```

Execute code asynchronously with non-blocking retry logic.

This is the primary async execution method. It uses `asyncio.sleep()` for retries, ensuring the event loop is not blocked during backoff periods.

**Parameters:** Same as `execute()`

**Returns:** `ExecutionResult` with execution outcome

**Raises:**

- `ExecutorTimeoutError`: If request times out after all retries
- `ExecutorConnectionError`: If connection fails after all retries
- `ExecutorClientError`: For other gRPC errors or if client is closed

**Example:**

```python
async with ExecutorClient(
    executor_url="http://localhost:8001",
    api_key="secret-key",
) as client:
    result = await client.execute_async(
        code="result = 42",
        available_tools=[],
        config={},
    )
    print(result.result)  # "42"
```

**Thread Safety:** This method is safe to call concurrently from multiple async tasks.

---

#### close_async

```python
async def close_async() -> None
```

Close the gRPC channel asynchronously. This method is idempotent and thread-safe.

**Example:**

```python
client = ExecutorClient(...)
try:
    result = await client.execute_async(...)
finally:
    await client.close_async()
```

---

### Context Managers

ExecutorClient supports both sync and async context managers for automatic resource cleanup:

```python
# Sync context manager
with ExecutorClient(...) as client:
    result = client.execute(...)

# Async context manager (recommended for async code)
async with ExecutorClient(...) as client:
    result = await client.execute_async(...)
```

---

## ComponentRegistry

Central registry for managing AI components. Framework-agnostic design supporting tools, agents, teams, and flows.

```python
from codemode.core import ComponentRegistry
```

### Constructor

```python
ComponentRegistry()
```

Initialize an empty registry.

---

### Tool Registration

#### register_tool

```python
def register_tool(
    name: str,
    tool: Any,
    description: str | None = None,
    input_schema: type[BaseModel] | dict[str, Any] | None = None,
    output_schema: type[BaseModel] | dict[str, Any] | None = None,
    overwrite: bool = False
) -> None
```

Register a tool with optional schema information.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `name` | `str` | Unique identifier for the tool |
| `tool` | `Any` | Tool instance to register |
| `description` | `str \| None` | Description override |
| `input_schema` | `type[BaseModel] \| dict \| None` | Pydantic model or JSON Schema for input |
| `output_schema` | `type[BaseModel] \| dict \| None` | Pydantic model or JSON Schema for output |
| `overwrite` | `bool` | Overwrite existing tool if `True` |

**Raises:**

- `ComponentAlreadyExistsError`: If tool exists and `overwrite=False`
- `ValueError`: If name or tool is invalid

**Example:**

```python
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    location: str = Field(..., description="City name")
    units: str = Field("celsius", description="Temperature units")

class WeatherOutput(BaseModel):
    temperature: float = Field(..., description="Temperature value")
    conditions: str = Field(..., description="Weather conditions")

registry.register_tool(
    name="weather",
    tool=weather_tool,
    input_schema=WeatherInput,
    output_schema=WeatherOutput,
    description="Get current weather for a location"
)
```

---

#### get_tool

```python
def get_tool(name: str) -> Any
```

Get a registered tool by name.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `name` | `str` | Tool name |

**Returns:** Tool instance

**Raises:**

- `ComponentNotFoundError`: If tool not found

---

#### list_tools

```python
@property
def tools(self) -> dict[str, Any]
```

Get dictionary of all registered tools.

**Returns:** Dictionary mapping tool names to tool instances

**Example:**

```python
for name, tool in registry.tools.items():
    print(f"Tool: {name}")
```

---

### Context Management

The registry provides thread-safe context management using Python's `ContextVar`. Context is automatically isolated per async task.

#### set_context

```python
def set_context(self, context: RuntimeContext) -> None
```

Set runtime context for the current async task.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `context` | `RuntimeContext` | Context to set |

**Thread Safety:** This method is thread-safe. Context is isolated per async task using `ContextVar`.

**Example:**

```python
from codemode.core.registry import RuntimeContext

context = RuntimeContext(variables={"client_id": "acme", "user_id": "user_123"})
registry.set_context(context)
```

---

#### get_context

```python
def get_context(self) -> RuntimeContext | None
```

Get runtime context for the current async task.

**Returns:** `RuntimeContext` if set, `None` otherwise

**Thread Safety:** This method is thread-safe. Returns the context for the current task only.

**Example:**

```python
context = registry.get_context()
if context:
    client_id = context.get("client_id")
```

---

#### clear_context

```python
def clear_context(self) -> None
```

Clear runtime context for the current async task.

**Thread Safety:** This method is thread-safe. Only clears context for the current task.

---

### Module-Level Context Functions

For direct access outside the registry:

```python
from codemode.core.registry import get_current_context, reset_context

# Get current context (same as registry.get_context())
context = get_current_context()

# Reset context (useful in testing)
reset_context()
```

---

## correlation Module

Utilities for generating correlation IDs for request tracing.

```python
from codemode.core.correlation import generate_correlation_id
```

### generate_correlation_id

```python
def generate_correlation_id(prefix: str = "cm") -> str
```

Generate a unique correlation ID for request tracing.

**Format:** `{prefix}-{base36_timestamp}-{random}`

**Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `prefix` | `str` | `"cm"` | ID prefix string |

**Returns:** Correlation ID string (approximately 15 characters with default prefix)

**Example:**

```python
from codemode.core.correlation import generate_correlation_id

# Default prefix
id1 = generate_correlation_id()  # 'cm-2x5f9k-a7b3'

# Custom prefix
id2 = generate_correlation_id(prefix="req")  # 'req-2x5f9k-c8d2'
```

---

## Exceptions

### ExecutorClientError

Base exception for executor client errors.

```python
from codemode.core.executor_client import ExecutorClientError
```

### ExecutorConnectionError

Raised when connection to the executor fails.

```python
from codemode.core.executor_client import ExecutorConnectionError
```

### ExecutorTimeoutError

Raised when the executor request times out.

```python
from codemode.core.executor_client import ExecutorTimeoutError
```

### ComponentNotFoundError

Raised when a component is not found in the registry.

```python
from codemode.core.registry import ComponentNotFoundError
```

### ComponentAlreadyExistsError

Raised when attempting to register a component that already exists.

```python
from codemode.core.registry import ComponentAlreadyExistsError
```
