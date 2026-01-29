# Codemode Production Integration Plan

**Created**: 2026-01-09
**Status**: In Progress
**Branch**: `fix/production-integration-issues`

---

## Executive Summary

This plan addresses critical issues identified during production integration of codemode with CrewAI applications. The work is organized into 5 phases with clear deliverables and success criteria.

---

## Table of Contents

1. [Phase 1: Configuration Separation & Environment Variables](#phase-1-configuration-separation--environment-variables)
2. [Phase 2: Docker Build & Assets Fix](#phase-2-docker-build--assets-fix)
3. [Phase 3: Tool Metadata & Schema Support](#phase-3-tool-metadata--schema-support)
4. [Phase 4: Reliability & Observability](#phase-4-reliability--observability)
5. [Phase 5: Documentation & Migration](#phase-5-documentation--migration)
6. [Implementation Progress](#implementation-progress)
7. [Knowledge Transfer Log](#knowledge-transfer-log)

---

## Phase 1: Configuration Separation & Environment Variables

### Goal
Separate client (main app) and sidecar (executor) configuration with comprehensive environment variable support.

### Rationale
Current state: Single `codemode.yaml` serves both client and sidecar, causing confusion in production deployments where they run independently.

### Deliverables

#### 1.1 Create Client Configuration Model

**File**: `codemode/config/client_config.py`

```python
class ClientConfig(BaseModel):
    """
    Configuration for the main application (client side).

    All fields support environment variable overrides.
    """

    # Executor connection
    executor_url: str                           # ENV: CODEMODE_EXECUTOR_URL
    executor_api_key: str                       # ENV: CODEMODE_EXECUTOR_API_KEY
    executor_timeout: int = 35                  # ENV: CODEMODE_EXECUTOR_TIMEOUT (1-600)

    # Retry configuration
    retry_enabled: bool = True                  # ENV: CODEMODE_RETRY_ENABLED
    retry_max_attempts: int = 3                 # ENV: CODEMODE_RETRY_MAX_ATTEMPTS
    retry_backoff_base_ms: int = 100            # ENV: CODEMODE_RETRY_BACKOFF_BASE_MS
    retry_backoff_max_ms: int = 5000            # ENV: CODEMODE_RETRY_BACKOFF_MAX_MS

    # Code limits (validation before sending)
    max_code_length: int = 10000                # ENV: CODEMODE_MAX_CODE_LENGTH

    # TLS (client connecting to executor)
    tls_enabled: bool = False                   # ENV: CODEMODE_TLS_ENABLED
    tls_mode: Literal["system", "custom"] = "system"  # ENV: CODEMODE_TLS_MODE
    tls_ca_file: str | None = None              # ENV: CODEMODE_TLS_CA_FILE
    tls_client_cert_file: str | None = None     # ENV: CODEMODE_TLS_CLIENT_CERT_FILE
    tls_client_key_file: str | None = None      # ENV: CODEMODE_TLS_CLIENT_KEY_FILE

    # Observability
    log_level: str = "INFO"                     # ENV: CODEMODE_LOG_LEVEL
    include_correlation_id: bool = True         # ENV: CODEMODE_INCLUDE_CORRELATION_ID
    correlation_id_prefix: str = "cm"           # ENV: CODEMODE_CORRELATION_ID_PREFIX

    # Error handling
    traceback_limit: int = 5                    # ENV: CODEMODE_TRACEBACK_LIMIT
```

#### 1.2 Create Sidecar Configuration Model

**File**: `codemode/config/sidecar_config.py`

```python
class SidecarConfig(BaseModel):
    """
    Configuration for the executor sidecar.

    All fields support environment variable overrides.
    """

    # Service binding
    port: int = 8001                            # ENV: CODEMODE_SIDECAR_PORT
    host: str = "0.0.0.0"                       # ENV: CODEMODE_SIDECAR_HOST
    main_app_grpc_target: str = "localhost:50051"  # ENV: CODEMODE_MAIN_APP_TARGET
    api_key: str | None = None                  # ENV: CODEMODE_API_KEY

    # Execution limits
    code_timeout: int = 30                      # ENV: CODEMODE_CODE_TIMEOUT (1-300)
    max_code_length: int = 10000                # ENV: CODEMODE_MAX_CODE_LENGTH

    # Security
    allow_direct_execution: bool = False        # ENV: CODEMODE_ALLOW_DIRECT_EXECUTION
    allowed_commands: list[str] = []            # ENV: CODEMODE_ALLOWED_COMMANDS (comma-sep)

    # TLS (server accepting connections)
    tls_enabled: bool = False                   # ENV: CODEMODE_TLS_ENABLED
    tls_mode: Literal["system", "custom"] = "system"  # ENV: CODEMODE_TLS_MODE
    tls_cert_file: str | None = None            # ENV: CODEMODE_TLS_CERT_FILE
    tls_key_file: str | None = None             # ENV: CODEMODE_TLS_KEY_FILE
    tls_ca_file: str | None = None              # ENV: CODEMODE_TLS_CA_FILE
    tls_require_client_auth: bool = False       # ENV: CODEMODE_TLS_REQUIRE_CLIENT_AUTH

    # Callback TLS (connecting back to main app)
    callback_tls_enabled: bool = False          # ENV: CODEMODE_CALLBACK_TLS_ENABLED
    callback_tls_ca_file: str | None = None     # ENV: CODEMODE_CALLBACK_TLS_CA_FILE
    callback_tls_client_cert: str | None = None # ENV: CODEMODE_CALLBACK_TLS_CLIENT_CERT
    callback_tls_client_key: str | None = None  # ENV: CODEMODE_CALLBACK_TLS_CLIENT_KEY

    # Observability
    log_level: str = "INFO"                     # ENV: CODEMODE_LOG_LEVEL
```

#### 1.3 Update Config Loader

**File**: `codemode/config/loader.py`

Add methods:
- `load_client_config(path: str | None = None) -> ClientConfig`
- `load_sidecar_config(path: str | None = None) -> SidecarConfig`
- `_load_from_env(model: type[BaseModel]) -> BaseModel`

Support loading from:
1. YAML file with env var substitution
2. Pure environment variables (no YAML)
3. Programmatic dict

#### 1.4 Update CLI Commands

**File**: `codemode/cli/main.py`

New commands:
```bash
codemode init client    # Creates codemode-client.yaml
codemode init sidecar   # Creates codemode-sidecar.yaml
codemode init           # Interactive: asks which to create, or creates both
```

#### 1.5 Update Executor Service

**File**: `codemode/executor/service.py`

- Use `SidecarConfig` instead of raw `os.getenv()` calls
- Support loading from YAML or env vars

#### 1.6 Update Codemode Main Class

**File**: `codemode/core/codemode.py`

- Add `Codemode.from_client_config(config: ClientConfig)` factory
- Deprecate old config loading (with warning)

### Success Criteria
- [ ] Client and sidecar have separate config models
- [ ] All config options have env var support
- [ ] CLI can initialize separate config files
- [ ] Existing code continues to work (with deprecation warnings)
- [ ] Unit tests pass

---

## Phase 2: Docker Build & Assets Fix

### Goal
Fix docker build command to work when installed from PyPI, with clear error messages.

### Rationale
Current state: `codemode docker build` fails because Dockerfile requires full repo checkout.

### Deliverables

#### 2.1 Update Dockerfile for PyPI Install

**File**: `docker_sidecar/Dockerfile`

Change from editable install to PyPI install:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install opencodemode from PyPI
ARG CODEMODE_VERSION=latest
RUN pip install --no-cache-dir "opencodemode[grpc]==${CODEMODE_VERSION}" || \
    pip install --no-cache-dir "opencodemode[grpc]"

# Expose gRPC port
EXPOSE 8001

# Run executor service
CMD ["python", "-m", "codemode.executor.service"]
```

#### 2.2 Fix Build Context Detection

**File**: `codemode/docker/manager.py`

Update `build_executor_image()`:
- Better error messages when Dockerfile not found
- Suggest `codemode docker assets` as solution
- Validate build context before attempting build

#### 2.3 Enhance Docker Assets Export

**File**: `codemode/docker_assets.py`

Update `export_bundle()` to include:
- `Dockerfile` (updated for PyPI)
- `docker-compose.yml`
- `sidecar.yaml.template`
- `README.md` with instructions

#### 2.4 Update CLI Docker Commands

**File**: `codemode/cli/main.py`

Improve error messages:
```
✗ Dockerfile not found.

To build the executor image:
  1. Export assets:  codemode docker assets --dest ./sidecar
  2. Build image:    docker build -t codemode-executor ./sidecar

Or pull pre-built image (when available):
  docker pull ghcr.io/mldlwizard/codemode-executor:latest
```

### Success Criteria
- [ ] `codemode docker assets` exports complete buildable bundle
- [ ] Exported Dockerfile builds successfully
- [ ] Clear error messages guide users
- [ ] Docker compose works with exported assets

---

## Phase 3: Tool Metadata & Schema Support

### Goal
Add input/output schema support for tools with Pydantic-based registration.

### Rationale
Current state: `ListTools` only returns name/description/is_async/has_context. Agents cannot see parameter schemas, leading to incorrect tool calls.

### Deliverables

#### 3.1 Fix _struct_to_dict Bug

**File**: `codemode/grpc/server.py`

Change:
```python
# Before (buggy - shallow conversion)
def _struct_to_dict(struct: Struct | None) -> dict[str, Any]:
    if not struct:
        return {}
    return dict(struct)

# After (correct - recursive conversion)
from google.protobuf.json_format import MessageToDict

def _struct_to_dict(struct: Struct | None) -> dict[str, Any]:
    if not struct:
        return {}
    return MessageToDict(struct, preserving_proto_field_name=True)
```

#### 3.2 Update Proto Definition

**File**: `codemode/protos/codemode.proto`

Add:
```protobuf
// Tool schema information
message ToolSchema {
  string json_schema = 1;  // Full JSON Schema as string (supports nested objects)
}

// Updated ToolInfo
message ToolInfo {
  string name = 1;
  bool is_async = 2;
  bool has_context = 3;
  string description = 4;
  ToolSchema input_schema = 5;   // Input parameters schema
  ToolSchema output_schema = 6;  // Return type schema
}

// Request for single tool schema (progressive discovery)
message GetToolSchemaRequest {
  string tool_name = 1;
}

message GetToolSchemaResponse {
  string tool_name = 1;
  ToolSchema input_schema = 2;
  ToolSchema output_schema = 3;
  string description = 4;
}

// Update ToolService
service ToolService {
  rpc CallTool(ToolCallRequest) returns (ToolCallResponse);
  rpc ListTools(google.protobuf.Empty) returns (ListToolsResponse);
  rpc GetToolSchema(GetToolSchemaRequest) returns (GetToolSchemaResponse);  // NEW
}
```

#### 3.3 Create Schema Utilities

**File**: `codemode/tools/schema.py` (NEW)

```python
"""
Tool schema utilities for Pydantic-based schema registration.

This module provides utilities for converting Pydantic models to JSON Schema
for tool registration and discovery.
"""

from typing import Any
from pydantic import BaseModel


def pydantic_to_json_schema(model: type[BaseModel]) -> dict[str, Any]:
    """
    Convert a Pydantic model to JSON Schema.

    Supports nested models, optional fields, defaults, and descriptions.

    Args:
        model: Pydantic BaseModel class

    Returns:
        JSON Schema dictionary

    Example:
        >>> class WeatherInput(BaseModel):
        ...     location: str = Field(..., description="City name")
        ...     units: str = Field("celsius", description="Temperature units")
        ...
        >>> schema = pydantic_to_json_schema(WeatherInput)
        >>> print(schema)
        {
            'type': 'object',
            'properties': {
                'location': {'type': 'string', 'description': 'City name'},
                'units': {'type': 'string', 'default': 'celsius', ...}
            },
            'required': ['location']
        }
    """
    return model.model_json_schema()


def dict_to_json_schema(schema_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Validate and normalize a JSON Schema dictionary.

    Args:
        schema_dict: Raw JSON Schema dictionary

    Returns:
        Normalized JSON Schema dictionary
    """
    # Basic validation
    if not isinstance(schema_dict, dict):
        raise ValueError("Schema must be a dictionary")
    return schema_dict


def schema_to_json_string(schema: dict[str, Any]) -> str:
    """Convert schema dict to JSON string for proto transport."""
    import json
    return json.dumps(schema, separators=(',', ':'))


def json_string_to_schema(json_str: str) -> dict[str, Any]:
    """Parse JSON string back to schema dict."""
    import json
    return json.loads(json_str)
```

#### 3.4 Update Tool Registration

**File**: `codemode/core/registry.py`

Add `ToolRegistration` dataclass and update `register_tool()`:

```python
@dataclass
class ToolRegistration:
    """Container for registered tool with metadata."""
    tool: Any
    input_schema: dict[str, Any] | None = None
    output_schema: dict[str, Any] | None = None
    description: str | None = None


class ComponentRegistry:
    def __init__(self) -> None:
        # Change from dict[str, Any] to dict[str, ToolRegistration]
        self._tool_registrations: dict[str, ToolRegistration] = {}
        # Keep tools property for backward compatibility
        ...

    def register_tool(
        self,
        name: str,
        tool: Any,
        input_schema: type[BaseModel] | dict[str, Any] | None = None,
        output_schema: type[BaseModel] | dict[str, Any] | None = None,
        description: str | None = None,
        overwrite: bool = False,
    ) -> None:
        """
        Register a tool with optional input/output schemas.

        Args:
            name: Unique identifier for the tool
            tool: Tool instance (callable, or object with run/run_with_context)
            input_schema: Pydantic model or JSON Schema dict for input validation
            output_schema: Pydantic model or JSON Schema dict for return type
            description: Optional description override (uses tool.description or __doc__)
            overwrite: If True, overwrite existing tool with same name

        Raises:
            ComponentAlreadyExistsError: If tool exists and overwrite=False
            ValueError: If name or tool is invalid

        Example:
            >>> from pydantic import BaseModel, Field
            >>>
            >>> class WeatherInput(BaseModel):
            ...     location: str = Field(..., description="City name")
            ...     units: str = Field("celsius", description="Temperature units")
            ...
            >>> class WeatherOutput(BaseModel):
            ...     temperature: float = Field(..., description="Temperature value")
            ...     conditions: str = Field(..., description="Weather conditions")
            ...     humidity: float = Field(..., description="Humidity percentage")
            ...
            >>> registry.register_tool(
            ...     name='weather',
            ...     tool=weather_tool,
            ...     input_schema=WeatherInput,
            ...     output_schema=WeatherOutput,
            ...     description="Get current weather for a location"
            ... )
        """
```

#### 3.5 Update ListTools Implementation

**File**: `codemode/grpc/server.py`

Update `ListTools()` to include schemas:
```python
async def ListTools(self, request, context):
    tool_infos = []
    for name, registration in self.registry.get_tool_registrations().items():
        tool = registration.tool

        # Get schemas
        input_schema_json = None
        output_schema_json = None
        if registration.input_schema:
            input_schema_json = schema_to_json_string(registration.input_schema)
        if registration.output_schema:
            output_schema_json = schema_to_json_string(registration.output_schema)

        tool_infos.append(
            codemode_pb2.ToolInfo(
                name=name,
                is_async=self._is_async(tool),
                has_context=hasattr(tool, "run_with_context"),
                description=registration.description or "",
                input_schema=codemode_pb2.ToolSchema(json_schema=input_schema_json or ""),
                output_schema=codemode_pb2.ToolSchema(json_schema=output_schema_json or ""),
            )
        )
    return codemode_pb2.ListToolsResponse(tools=tool_infos)
```

#### 3.6 Add GetToolSchema RPC

**File**: `codemode/grpc/server.py`

Add new RPC handler:
```python
async def GetToolSchema(self, request, context):
    """Get detailed schema for a specific tool."""
    tool_name = request.tool_name
    registration = self.registry.get_tool_registration(tool_name)

    if not registration:
        context.abort(grpc.StatusCode.NOT_FOUND, f"Tool '{tool_name}' not found")

    return codemode_pb2.GetToolSchemaResponse(
        tool_name=tool_name,
        input_schema=codemode_pb2.ToolSchema(
            json_schema=schema_to_json_string(registration.input_schema or {})
        ),
        output_schema=codemode_pb2.ToolSchema(
            json_schema=schema_to_json_string(registration.output_schema or {})
        ),
        description=registration.description or "",
    )
```

#### 3.7 Add Meta-Tools for Discovery

**File**: `codemode/grpc/server.py`

Register built-in `__list__` and `__schema__` tools:
```python
class ListToolsMetaTool:
    """Built-in tool for listing available tools."""
    description = "List all available tools with brief descriptions"

    def run(self) -> dict[str, Any]:
        # Returns list of tool names and descriptions
        ...

    async def run(self) -> dict[str, Any]:
        # Async version
        ...


class GetSchemaMetaTool:
    """Built-in tool for getting tool schema."""
    description = "Get input and output schema for a specific tool"

    def run(self, name: str) -> dict[str, Any]:
        # Returns schema for specified tool
        ...

    async def run(self, name: str) -> dict[str, Any]:
        # Async version
        ...
```

#### 3.8 Update CodemodeTool Description

**File**: `codemode/integrations/crewai.py`

Update description with:
- Discovery examples (sync and async)
- Input/output schema usage
- Tool chaining examples using output schemas
- Complete async pattern with asyncio.run(main())

(See refined plan in conversation for full description text)

#### 3.9 Regenerate Proto Files

**Command**:
```bash
make proto
```

**Add to Makefile**:
```makefile
.PHONY: proto
proto:
	python -m grpc_tools.protoc \
		-I=codemode/protos \
		--python_out=codemode/protos \
		--grpc_python_out=codemode/protos \
		codemode/protos/codemode.proto
	@echo "Proto files regenerated"
```

### Success Criteria
- [ ] `_struct_to_dict` properly converts nested structs
- [ ] Proto files regenerated with new schema fields
- [ ] `register_tool()` accepts input_schema and output_schema
- [ ] `ListTools` returns schemas
- [ ] `GetToolSchema` RPC works
- [ ] Meta-tools work (sync and async)
- [ ] CodemodeTool description is comprehensive
- [ ] Unit tests pass

---

## Phase 4: Reliability & Observability

### Goal
Add retry logic, correlation IDs, and structured error handling.

### Rationale
Current state: No retry on transient failures, no way to correlate logs across services, error details are lost.

### Deliverables

#### 4.1 Add Retry Logic to ExecutorClient

**File**: `codemode/core/executor_client.py`

```python
class ExecutorClient:
    def __init__(
        self,
        target: str,
        api_key: str | None = None,
        timeout: int = 35,
        # Retry configuration
        retry_enabled: bool = True,
        retry_max_attempts: int = 3,
        retry_backoff_base_ms: int = 100,
        retry_backoff_max_ms: int = 5000,
        retry_status_codes: list[grpc.StatusCode] | None = None,
    ):
        """
        Initialize executor client with retry support.

        Args:
            target: gRPC target address (host:port)
            api_key: API key for authentication
            timeout: Request timeout in seconds
            retry_enabled: Enable automatic retry on transient failures
            retry_max_attempts: Maximum number of retry attempts
            retry_backoff_base_ms: Base backoff time in milliseconds
            retry_backoff_max_ms: Maximum backoff time in milliseconds
            retry_status_codes: gRPC status codes to retry on
        """
        self.retry_enabled = retry_enabled
        self.retry_max_attempts = retry_max_attempts
        self.retry_backoff_base_ms = retry_backoff_base_ms
        self.retry_backoff_max_ms = retry_backoff_max_ms
        self.retry_status_codes = retry_status_codes or [
            grpc.StatusCode.UNAVAILABLE,
            grpc.StatusCode.DEADLINE_EXCEEDED,
            grpc.StatusCode.RESOURCE_EXHAUSTED,
        ]

    def _calculate_backoff(self, attempt: int) -> float:
        """Calculate backoff with jitter."""
        import random
        base = self.retry_backoff_base_ms * (2 ** attempt)
        jitter = random.uniform(0.8, 1.2)
        backoff = min(base * jitter, self.retry_backoff_max_ms)
        return backoff / 1000  # Convert to seconds

    def execute(self, ...):
        """Execute code with automatic retry on transient failures."""
        last_error = None
        for attempt in range(self.retry_max_attempts):
            try:
                return self._execute_once(...)
            except grpc.RpcError as e:
                if not self.retry_enabled:
                    raise
                if e.code() not in self.retry_status_codes:
                    raise
                if attempt == self.retry_max_attempts - 1:
                    raise

                backoff = self._calculate_backoff(attempt)
                logger.warning(
                    "Retry attempt %d/%d after %.2fs: %s",
                    attempt + 1, self.retry_max_attempts, backoff, e.code()
                )
                time.sleep(backoff)
                last_error = e

        raise last_error
```

#### 4.2 Add Correlation ID Support

**File**: `codemode/core/correlation.py` (NEW)

```python
"""
Correlation ID generation and management.

Correlation IDs are used to trace requests across the main app and executor.
Format: {prefix}-{base36_timestamp}-{random}
Example: cm-2x5f9k-a7b3 (12 chars total)
"""

import random
import string
import time


def generate_correlation_id(prefix: str = "cm") -> str:
    """
    Generate a unique correlation ID.

    Format: {prefix}-{base36_timestamp}-{random}
    - prefix: configurable, default "cm"
    - timestamp: base36 encoded milliseconds (compact)
    - random: 4 random alphanumeric chars

    Args:
        prefix: ID prefix (default: "cm")

    Returns:
        Correlation ID string (~12 chars)

    Example:
        >>> generate_correlation_id()
        'cm-2x5f9k-a7b3'
    """
    # Base36 encode current time in milliseconds
    timestamp = int(time.time() * 1000)
    ts_b36 = _to_base36(timestamp)[-6:]  # Last 6 chars

    # Random suffix
    chars = string.ascii_lowercase + string.digits
    suffix = ''.join(random.choices(chars, k=4))

    return f"{prefix}-{ts_b36}-{suffix}"


def _to_base36(num: int) -> str:
    """Convert integer to base36 string."""
    chars = string.digits + string.ascii_lowercase
    if num == 0:
        return '0'
    result = []
    while num:
        result.append(chars[num % 36])
        num //= 36
    return ''.join(reversed(result))
```

#### 4.3 Update ExecutionResult with Correlation ID

**File**: `codemode/executor/models.py`

```python
@dataclass
class ExecutionError:
    """Structured error information."""
    error_type: str      # "SecurityViolation", "Timeout", "RuntimeError", etc.
    message: str         # Error message
    traceback: str | None = None  # Limited traceback (configurable frames)


@dataclass
class ExecutionResult:
    """Result of code execution."""
    success: bool
    result: str | None = None
    stdout: str = ""
    stderr: str = ""
    error: str | None = None
    error_details: ExecutionError | None = None  # NEW
    correlation_id: str | None = None            # NEW
    duration_ms: float | None = None             # NEW

    @classmethod
    def success_result(cls, result: str | None, ..., correlation_id: str | None = None):
        ...

    @classmethod
    def error_result(cls, error: str, ..., correlation_id: str | None = None):
        ...
```

#### 4.4 Add Structured Error Parsing

**File**: `codemode/executor/runner.py`

```python
def _parse_traceback(stderr: str, limit: int = 5) -> str | None:
    """
    Extract last N frames from Python traceback in stderr.

    Args:
        stderr: Standard error output
        limit: Maximum number of frames to include (0 to disable)

    Returns:
        Limited traceback string or None
    """
    if limit == 0 or not stderr:
        return None

    # Find traceback section
    lines = stderr.split('\n')
    tb_start = None
    for i, line in enumerate(lines):
        if line.startswith('Traceback (most recent call last):'):
            tb_start = i
            break

    if tb_start is None:
        return None

    # Extract frames (each frame is 2 lines: File... and code)
    tb_lines = lines[tb_start:]
    frames = []
    i = 1
    while i < len(tb_lines) - 1:
        if tb_lines[i].strip().startswith('File '):
            frames.append((tb_lines[i], tb_lines[i + 1] if i + 1 < len(tb_lines) else ''))
            i += 2
        else:
            break

    # Take last N frames
    limited_frames = frames[-limit:] if len(frames) > limit else frames

    # Reconstruct
    result = ['Traceback (most recent call last):']
    for file_line, code_line in limited_frames:
        result.append(file_line)
        if code_line.strip():
            result.append(code_line)

    # Add error line
    if tb_lines:
        result.append(tb_lines[-1])

    return '\n'.join(result)


def _classify_error(stderr: str, return_code: int) -> str:
    """Classify error type from stderr and return code."""
    if "Security violation" in stderr:
        return "SecurityViolation"
    if "timeout" in stderr.lower():
        return "Timeout"
    if "SyntaxError" in stderr:
        return "SyntaxError"
    if "ImportError" in stderr or "ModuleNotFoundError" in stderr:
        return "ImportError"
    if "TypeError" in stderr:
        return "TypeError"
    if "ValueError" in stderr:
        return "ValueError"
    if "KeyError" in stderr:
        return "KeyError"
    if return_code != 0:
        return "RuntimeError"
    return "Unknown"
```

#### 4.5 Update Logging for Correlation

Update all modules to include correlation_id in log messages:
- `codemode/core/executor_client.py`
- `codemode/executor/service.py`
- `codemode/executor/runner.py`
- `codemode/grpc/server.py`

Use `extra` parameter for structured logging:
```python
logger.info(
    "Execution request received",
    extra={
        "correlation_id": correlation_id,
        "code_chars": len(code),
        "tool_count": len(tools),
    }
)
```

#### 4.6 Pass Correlation ID via gRPC Metadata

**File**: `codemode/core/executor_client.py`

```python
def execute(self, ..., correlation_id: str | None = None):
    if correlation_id is None and self.include_correlation_id:
        correlation_id = generate_correlation_id(self.correlation_id_prefix)

    metadata = []
    if self.api_key:
        metadata.append(("authorization", f"Bearer {self.api_key}"))
    if correlation_id:
        metadata.append(("x-correlation-id", correlation_id))

    # ... execute with metadata
```

**File**: `codemode/executor/service.py`

```python
async def Execute(self, request, context):
    metadata = dict(context.invocation_metadata())
    correlation_id = metadata.get("x-correlation-id")

    # Include in all logs and pass to runner
    ...
```

### Success Criteria
- [ ] Retry logic works with exponential backoff
- [ ] Correlation IDs are generated and propagated
- [ ] Structured errors include type, message, traceback
- [ ] Traceback limit is configurable
- [ ] Logs include correlation IDs
- [ ] Unit tests pass

---

## Phase 5: Documentation & Migration

### Goal
Comprehensive documentation and clean migration guide.

### Deliverables

#### 5.1 Configuration Reference

**File**: `docs/configuration.md` (NEW)

Complete reference including:
- All client config options with env vars
- All sidecar config options with env vars
- YAML vs env-only examples
- Migration from old config format

#### 5.2 Tool Schemas Documentation

**File**: `docs/features/tool-schemas.md` (NEW)

- How to define input/output schemas with Pydantic
- Registration examples
- Progressive discovery usage
- Tool chaining with output schemas

#### 5.3 Migration Guide

**File**: `docs/migration/v0.2.0.md` (NEW)

- Breaking changes list
- Step-by-step migration
- Before/after code examples
- Deprecation timeline

#### 5.4 Update Existing Documentation

Files to update:
- `README.md` - Update examples, add schema section
- `docs/features/crewai-integration.md` - Add schema examples
- `docs/SIDECAR_DEPLOYMENT.md` - Update config instructions
- `AGENTS.md` - Update development commands

#### 5.5 Update CHANGELOG

**File**: `CHANGELOG.md`

Add v0.2.0 section with all changes.

### Success Criteria
- [ ] All new features documented
- [ ] Migration guide complete
- [ ] README updated
- [ ] AGENTS.md updated
- [ ] CHANGELOG updated

---

## Implementation Progress

### Phase 1: Configuration Separation
| Task | Status | Agent | Notes |
|------|--------|-------|-------|
| 1.1 Create ClientConfig | Not Started | | |
| 1.2 Create SidecarConfig | Not Started | | |
| 1.3 Update ConfigLoader | Not Started | | |
| 1.4 Update CLI | Not Started | | |
| 1.5 Update executor service | Not Started | | |
| 1.6 Update Codemode class | Not Started | | |
| Tests passing | Not Started | | |

### Phase 2: Docker Build Fix
| Task | Status | Agent | Notes |
|------|--------|-------|-------|
| 2.1 Update Dockerfile | Not Started | | |
| 2.2 Fix build context | Not Started | | |
| 2.3 Enhance assets export | Not Started | | |
| 2.4 Update CLI messages | Not Started | | |
| Tests passing | Not Started | | |

### Phase 3: Tool Metadata & Schema
| Task | Status | Agent | Notes |
|------|--------|-------|-------|
| 3.1 Fix _struct_to_dict | Not Started | | |
| 3.2 Update proto | Not Started | | |
| 3.3 Create schema utils | Not Started | | |
| 3.4 Update registry | Not Started | | |
| 3.5 Update ListTools | Not Started | | |
| 3.6 Add GetToolSchema | Not Started | | |
| 3.7 Add meta-tools | Not Started | | |
| 3.8 Update CodemodeTool | Not Started | | |
| 3.9 Regenerate protos | Not Started | | |
| Tests passing | Not Started | | |

### Phase 4: Reliability & Observability
| Task | Status | Agent | Notes |
|------|--------|-------|-------|
| 4.1 Add retry logic | Not Started | | |
| 4.2 Add correlation IDs | Not Started | | |
| 4.3 Update ExecutionResult | Not Started | | |
| 4.4 Add error parsing | Not Started | | |
| 4.5 Update logging | Not Started | | |
| 4.6 Propagate correlation ID | Not Started | | |
| Tests passing | Not Started | | |

### Phase 5: Documentation
| Task | Status | Agent | Notes |
|------|--------|-------|-------|
| 5.1 Configuration reference | Not Started | | |
| 5.2 Tool schemas doc | Not Started | | |
| 5.3 Migration guide | Not Started | | |
| 5.4 Update existing docs | Not Started | | |
| 5.5 Update CHANGELOG | Not Started | | |

---

## Knowledge Transfer Log

This section is updated by each sub-agent with key decisions and implementation details.

### Session 1: Plan Creation
- **Date**: 2026-01-09
- **Agent**: Main orchestrator
- **Work Done**: Created comprehensive plan document
- **Key Decisions**:
  - Clean break from old config (no backward compat)
  - Pydantic-only schema support (no docstring parsing)
  - Input AND output schema support
  - Correlation ID format: `{prefix}-{base36_ts}-{random}` (~12 chars)
  - Meta-tools support both sync and async
- **Next Steps**: Create fix branch, start Phase 1

---

*Last Updated: 2026-01-09*
