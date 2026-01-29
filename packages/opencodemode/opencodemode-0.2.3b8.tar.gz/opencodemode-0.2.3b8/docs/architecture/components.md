# Component Architecture

This document provides a detailed breakdown of Codemode's internal components, their responsibilities, and how they interact.

## Core Module (`codemode/core/`)

The core module contains the primary client-side components.

### Codemode Class

**Location**: `codemode/core/codemode.py`

The `Codemode` class is the main entry point for users. It orchestrates configuration loading, component registration, and code execution.

```python
from codemode import Codemode
from codemode.config import ClientConfig

# Create from configuration
config = ClientConfig(
    executor_url="http://executor:8001",
    executor_api_key="secret-key",
)
codemode = Codemode.from_client_config(config)

# Execute code
result = codemode.execute("result = 2 + 2")
```

**Responsibilities**:

- Configuration loading from YAML, environment variables, or dictionaries
- Managing the `ComponentRegistry` for tool and agent registration
- Providing the `execute()` and `execute_async()` methods for code execution
- Creating framework-specific tools (e.g., `as_crewai_tool()`)
- Health and readiness checks for the executor

**Key Methods**:

| Method | Description |
|--------|-------------|
| `from_client_config()` | Create instance from `ClientConfig` |
| `from_config()` | Create instance from YAML file path |
| `from_env()` | Create instance from environment variables |
| `execute()` | Execute code synchronously |
| `execute_async()` | Execute code asynchronously |
| `with_context()` | Set runtime context variables |
| `health_check()` | Check if executor is healthy |

### ExecutorClient

**Location**: `codemode/core/executor_client.py`

The `ExecutorClient` handles all gRPC communication with the executor sidecar.

```python
from codemode.core.executor_client import ExecutorClient

client = ExecutorClient(
    executor_url="http://executor:8001",
    api_key="secret-key",
    retry_enabled=True,
    retry_max_attempts=3,
)

result = client.execute(
    code="result = tools['weather'].run(location='NYC')",
    available_tools=["weather"],
    config={},
    execution_timeout=30,
)
```

**Responsibilities**:

- Establishing gRPC connections (secure or insecure)
- Sending execution requests with proper authentication
- Automatic retry with exponential backoff on transient failures
- Correlation ID generation and propagation for request tracing
- TLS/mTLS credential management

**Key Features**:

| Feature | Description |
|---------|-------------|
| Retry Logic | Exponential backoff with jitter for UNAVAILABLE, DEADLINE_EXCEEDED, RESOURCE_EXHAUSTED |
| Correlation IDs | Auto-generated request IDs for distributed tracing |
| TLS Support | System certificates or custom CA/client certificates |
| Timeout Handling | Configurable request timeouts with proper cleanup |

### ComponentRegistry

**Location**: `codemode/core/registry.py`

The `ComponentRegistry` is a central repository for all components accessible from executed code.

```python
from codemode.core.registry import ComponentRegistry
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    location: str = Field(..., description="City name")

registry = ComponentRegistry()
registry.register_tool(
    name="weather",
    tool=weather_tool,
    input_schema=WeatherInput,
    description="Get current weather",
)
```

**Responsibilities**:

- Registering and retrieving tools, agents, teams, and flows
- Managing tool schemas (input/output) for validation and documentation
- Storing static configuration (set at startup)
- Managing dynamic runtime context (per-request)

**Component Types**:

| Type | Description |
|------|-------------|
| `tools` | Individual functions/tools with optional schemas |
| `agents` | Individual AI agents |
| `teams` | Groups of agents (Crew, GroupChat, etc.) |
| `flows` | Workflows/graphs (Flow, StateGraph, etc.) |
| `config` | Static configuration key-value pairs |

### RuntimeContext

**Location**: `codemode/core/context.py`

`RuntimeContext` carries per-request variables that are passed to tools during execution.

```python
from codemode.core.context import RuntimeContext

context = RuntimeContext(variables={
    "client_id": "acme-corp",
    "user_id": "user_123",
    "session_id": "sess_456",
})

# Set on codemode instance
codemode.with_context(
    client_id="acme-corp",
    user_id="user_123",
)
```

**Responsibilities**:

- Storing request-specific variables (user ID, session, tenant, etc.)
- Serialization for transport across gRPC
- Providing a clean interface for context-aware tools

---

## Executor Module (`codemode/executor/`)

The executor module contains components that run inside the sidecar container.

### CodeRunner

**Location**: `codemode/executor/runner.py`

The `CodeRunner` executes Python code in a sandboxed subprocess environment.

```python
from codemode.executor.runner import CodeRunner

runner = CodeRunner(
    main_app_target="main-app:50051",
    api_key="secret-key",
)

result = await runner.run(
    code="result = tools['weather'].run(location='NYC')",
    available_tools=["weather"],
    config={},
    timeout=30,
    tool_metadata={"weather": {"is_async": False}},
)
```

**Responsibilities**:

- Security validation before execution
- Wrapping user code with tool proxy infrastructure
- Spawning isolated Python subprocesses
- Capturing stdout, stderr, and result variables
- Timeout enforcement with process termination
- Error classification and traceback parsing

**Execution Flow**:

1. Validate code with `SecurityValidator`
2. Generate tool proxy classes (sync/async based on metadata)
3. Wrap user code with imports, helpers, and proxy initialization
4. Execute in subprocess with `asyncio.create_subprocess_exec()`
5. Parse output for `__CODEMODE_RESULT__` marker
6. Return structured `ExecutionResult`

### ExecutorGrpcService

**Location**: `codemode/executor/service.py`

The gRPC service that handles execution requests from the main application.

**Responsibilities**:

- Receiving and validating `ExecuteRequest` messages
- Authenticating requests via API key
- Fetching tool metadata from the main app via `ListTools`
- Delegating to `CodeRunner` for actual execution
- Returning `ExecuteResponse` with results or errors

**gRPC Methods**:

| Method | Description |
|--------|-------------|
| `Execute` | Execute code and return results |
| `Health` | Health check endpoint |
| `Ready` | Readiness check (can reach main app) |

### SecurityValidator

**Location**: `codemode/executor/security.py`

Validates code for security issues before execution.

```python
from codemode.executor.security import SecurityValidator

validator = SecurityValidator(
    max_code_length=10000,
    allow_direct_execution=False,
)

result = validator.validate(code)
if not result.is_safe:
    print(f"Blocked: {result.reason}")
```

**Responsibilities**:

- Checking code length limits
- Detecting blocked patterns (`eval`, `exec`, `__import__`, etc.)
- Detecting blocked imports (`subprocess`, `os.system`, `socket`, etc.)
- Detecting suspicious patterns (infinite loops, unicode tricks)
- Optional command and path whitelisting for direct execution mode

**Blocked Categories**:

| Category | Examples |
|----------|----------|
| Dangerous Builtins | `eval()`, `exec()`, `compile()`, `open()` |
| Reflection | `__import__`, `__builtins__`, `getattr()`, `setattr()` |
| System Access | `subprocess`, `os.system`, `os.popen` |
| Networking | `socket`, `urllib`, `http.client` |
| Low-Level | `ctypes`, `multiprocessing`, `signal` |

### ExecutionResult / ExecutionError

**Location**: `codemode/executor/models.py`

Structured models for execution outcomes.

```python
from codemode.executor.models import ExecutionResult, ExecutionError

# Success result
result = ExecutionResult(
    success=True,
    result="42",
    stdout="Calculating...\n",
    stderr="",
    correlation_id="cm-abc123",
    duration_ms=150.5,
)

# Error result with details
result = ExecutionResult(
    success=False,
    error="Execution failed with return code 1",
    error_details=ExecutionError(
        error_type="ValueError",
        message="invalid literal for int()",
        traceback="...",
    ),
)
```

---

## Config Module (`codemode/config/`)

The config module handles configuration loading and validation.

### ClientConfig

**Location**: `codemode/config/client_config.py`

Simplified configuration for client applications.

```python
from codemode.config import ClientConfig

# From explicit values
config = ClientConfig(
    executor_url="http://executor:8001",
    executor_api_key="secret-key",
    executor_timeout=35,
)

# From environment variables
config = ClientConfig.from_env()
# Reads: CODEMODE_EXECUTOR_URL, CODEMODE_EXECUTOR_API_KEY
```

### SidecarConfig

**Location**: `codemode/config/sidecar_config.py`

Configuration for the executor sidecar.

```python
from codemode.config import SidecarConfig

config = SidecarConfig(
    grpc_port=8001,
    main_app_url="http://main-app:50051",
    api_key="secret-key",
    code_timeout=30,
    max_code_length=10000,
)
```

### ConfigLoader

**Location**: `codemode/config/loader.py`

Loads configuration from various sources.

```python
from codemode.config.loader import ConfigLoader

# Load from YAML file
config = ConfigLoader.load("codemode.yaml")

# Load client config from YAML
client_config = ConfigLoader.load_client_config("codemode-client.yaml")

# Load from dictionary
config = ConfigLoader.load_dict({
    "project": {"name": "my-app"},
    "framework": {"type": "crewai"},
    "executor": {"url": "...", "api_key": "..."},
})
```

---

## Tools Module (`codemode/tools/`)

The tools module provides infrastructure for tool registration and schema management.

### ToolRegistration

**Location**: `codemode/tools/schema.py`

Holds tool instance with associated metadata.

```python
from codemode.tools.schema import ToolRegistration

registration = ToolRegistration(
    tool=weather_tool,
    input_schema={"type": "object", "properties": {...}},
    output_schema={"type": "object", "properties": {...}},
    description="Get current weather for a location",
)
```

**Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `tool` | Any | The tool instance (callable or object with `run()`) |
| `input_schema` | dict | JSON Schema for input validation |
| `output_schema` | dict | JSON Schema for return type |
| `description` | str | Human-readable description |

### Meta-Tools

The system provides built-in meta-tools accessible via gRPC:

| Tool | Description |
|------|-------------|
| `ListTools` | Returns all registered tools with metadata |
| `GetToolSchema` | Returns detailed schema for a specific tool |

These are implemented in `ToolService` and allow the executor to discover available tools.

---

## gRPC Module (`codemode/grpc/`)

The gRPC module provides the server infrastructure for tool callbacks.

### ToolService

**Location**: `codemode/grpc/server.py`

The gRPC server that handles tool invocation requests from the executor.

```python
from codemode.grpc.server import start_tool_service

# Start synchronously (blocks forever)
start_tool_service(
    registry=registry,
    host="0.0.0.0",
    port=50051,
    api_key="secret-key",
)

# Start asynchronously (returns server)
server = await start_tool_service_async(
    registry=registry,
    port=50051,
)
```

**gRPC Methods**:

| Method | Description |
|--------|-------------|
| `CallTool` | Invoke a registered tool with arguments |
| `ListTools` | List all tools with metadata and schemas |
| `GetToolSchema` | Get detailed schema for a specific tool |

**Features**:

- API key authentication via gRPC metadata
- Automatic async/sync tool detection
- Context injection for context-aware tools
- Optional thread pool for concurrent sync tool execution
- TLS/mTLS support for secure communication

---

## Component Interaction Diagram

```
+------------------+     +-------------------+     +------------------+
|    Codemode      |---->| ExecutorClient    |---->| ExecutorService  |
|    (API)         |     | (gRPC Client)     |     | (gRPC Server)    |
+------------------+     +-------------------+     +--------+---------+
        |                                                   |
        v                                                   v
+------------------+                              +------------------+
|ComponentRegistry |                              |   CodeRunner     |
|  - tools         |                              |   (Subprocess)   |
|  - agents        |                              +--------+---------+
|  - config        |                                       |
+--------+---------+                                       v
         |                                        +------------------+
         v                                        |  Tool Proxies    |
+------------------+     +-------------------+    |  (gRPC Clients)  |
|   ToolService    |<----| ToolCallRequest   |<---+------------------+
|   (gRPC Server)  |     +-------------------+
+------------------+
```
