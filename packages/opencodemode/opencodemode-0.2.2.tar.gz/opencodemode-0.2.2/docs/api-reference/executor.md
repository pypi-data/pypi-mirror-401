# Executor Module API

The `codemode.executor` module provides the executor sidecar implementation. This includes execution models, the code runner, security validation, and the gRPC service.

## ExecutionResult

Result model returned by the executor after code execution.

```python
from codemode.executor.models import ExecutionResult
```

### Attributes

| Name | Type | Description |
|------|------|-------------|
| `success` | `bool` | Whether execution succeeded |
| `result` | `str \| None` | Execution result (if successful) |
| `stdout` | `str` | Standard output from execution |
| `stderr` | `str` | Standard error from execution |
| `error` | `str \| None` | Error message (if failed) |
| `error_details` | `ExecutionError \| None` | Structured error information |
| `correlation_id` | `str \| None` | Request correlation ID for tracing |
| `duration_ms` | `float \| None` | Execution duration in milliseconds |

### Example

```python
result = ExecutionResult(
    success=True,
    result="{'weather': '72F'}",
    stdout="Execution completed\n",
    stderr="",
    correlation_id="cm-2x5f9k-a7b3",
    duration_ms=150.5
)
```

### Class Methods

#### success_result

```python
@classmethod
def success_result(
    result: str | None,
    stdout: str = "",
    stderr: str = "",
    correlation_id: str | None = None,
    duration_ms: float | None = None
) -> ExecutionResult
```

Create a successful execution result.

**Example:**

```python
result = ExecutionResult.success_result(
    result="Done",
    stdout="OK\n",
    correlation_id="cm-2x5f9k-a7b3",
    duration_ms=50.2
)
```

---

#### error_result

```python
@classmethod
def error_result(
    error: str,
    stdout: str = "",
    stderr: str = "",
    error_details: ExecutionError | None = None,
    correlation_id: str | None = None,
    duration_ms: float | None = None
) -> ExecutionResult
```

Create an error execution result.

**Example:**

```python
error_info = ExecutionError(
    error_type="Timeout",
    message="Execution timeout after 30 seconds"
)
result = ExecutionResult.error_result(
    error="Timeout",
    stderr="...",
    error_details=error_info,
    correlation_id="cm-2x5f9k-a7b3",
    duration_ms=30000.0
)
```

---

## ExecutionError

Structured error information from code execution.

```python
from codemode.executor.models import ExecutionError
```

### Attributes

| Name | Type | Description |
|------|------|-------------|
| `error_type` | `str` | Classification of the error |
| `message` | `str` | Human-readable error message |
| `traceback` | `str \| None` | Limited traceback information |

### Error Types

| Type | Description |
|------|-------------|
| `SecurityViolation` | Security policy was violated |
| `Timeout` | Execution timed out |
| `SyntaxError` | Python syntax error |
| `ImportError` | Module import failed |
| `TypeError` | Type mismatch error |
| `ValueError` | Invalid value error |
| `KeyError` | Dictionary key not found |
| `RuntimeError` | General runtime error |
| `Unknown` | Could not classify the error |

### Example

```python
error = ExecutionError(
    error_type="TypeError",
    message="unsupported operand type(s) for +: 'int' and 'str'",
    traceback="File '<string>', line 5, in <module>\n    result = x + y"
)
```

---

## CodeRunner

Executes Python code with gRPC tool proxies in a sandboxed environment.

```python
from codemode.executor.runner import CodeRunner
```

### Constructor

```python
CodeRunner(
    main_app_target: str | None = None,
    api_key: str | None = None,
    security_validator: SecurityValidator | None = None,
    allow_direct_execution: bool = False
)
```

**Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `main_app_target` | `str \| None` | `"localhost:50051"` | Main app gRPC target |
| `api_key` | `str \| None` | `None` | API key for authentication |
| `security_validator` | `SecurityValidator \| None` | `None` | Custom security validator |
| `allow_direct_execution` | `bool` | `False` | Allow direct system commands |

---

### Methods

#### run

```python
async def run(
    code: str,
    available_tools: list[str],
    config: dict[str, Any],
    timeout: int = 30,
    context: dict[str, Any] | None = None,
    tool_metadata: dict[str, dict] | None = None,
    correlation_id: str | None = None
) -> ExecutionResult
```

Execute Python code with tool proxies in a sandboxed environment.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `code` | `str` | Python code to execute |
| `available_tools` | `list[str]` | List of tool names to make available |
| `config` | `dict[str, Any]` | Configuration dictionary |
| `timeout` | `int` | Execution timeout in seconds |
| `context` | `dict[str, Any] \| None` | Optional runtime context for tools |
| `tool_metadata` | `dict[str, dict] \| None` | Metadata about tools (async, has_context) |
| `correlation_id` | `str \| None` | Optional correlation ID for request tracing |

**Returns:** `ExecutionResult` with success status and output

**Raises:**

- `ValueError`: If `tool_metadata` is not provided

**Example:**

```python
runner = CodeRunner(
    main_app_target="app:50051",
    api_key="secret"
)

result = await runner.run(
    code="result = tools['weather'].run(location='NYC')",
    available_tools=["weather"],
    config={},
    tool_metadata={"weather": {"is_async": False, "has_context": False}},
    timeout=30
)
```

---

## SecurityValidator

Validates code for security issues before execution.

```python
from codemode.executor.security import SecurityValidator
```

### Constructor

```python
SecurityValidator(
    max_code_length: int = 10000,
    additional_blocked_patterns: list[str] | None = None,
    additional_blocked_imports: list[str] | None = None,
    allow_direct_execution: bool = False,
    allowed_commands: list[str] | None = None,
    allowed_paths: dict[str, str] | None = None
)
```

**Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `max_code_length` | `int` | `10000` | Maximum code length in characters |
| `additional_blocked_patterns` | `list[str] \| None` | `None` | Additional patterns to block |
| `additional_blocked_imports` | `list[str] \| None` | `None` | Additional imports to block |
| `allow_direct_execution` | `bool` | `False` | Allow direct system commands |
| `allowed_commands` | `list[str] \| None` | `None` | Allowed system commands |
| `allowed_paths` | `dict[str, str] \| None` | `None` | Allowed path access mapping |

**Example:**

```python
validator = SecurityValidator(
    max_code_length=5000,
    additional_blocked_patterns=["dangerous_func"],
    allow_direct_execution=True,
    allowed_commands=["grep", "cat", "ls"],
    allowed_paths={"/workspace": "r", "/sandbox": "rw"}
)
```

---

### Class Attributes

#### BLOCKED_PATTERNS

Default patterns that are blocked:

```python
{
    "__import__", "eval(", "exec(", "compile(",
    "open(", "file(", "input(", "raw_input(",
    "execfile(", "__builtins__", "reload(",
    "vars(", "dir(", "globals(", "locals(",
    "delattr(", "setattr(", "getattr("
}
```

#### BLOCKED_IMPORTS

Default imports that are blocked:

```python
{
    "subprocess", "os.system", "os.popen", "os.spawn", "os.exec",
    "socket", "urllib", "urllib2", "urllib3",
    "httplib", "http.client", "ftplib", "telnetlib", "smtplib",
    "ssl", "ctypes", "multiprocessing", "threading",
    "asyncio.subprocess", "pty", "pwd", "grp",
    "resource", "signal", "sys.exit"
}
```

---

### Methods

#### validate

```python
def validate(code: str) -> SecurityValidationResult
```

Validate code for security issues.

**Checks performed:**

1. Code length check
2. Blocked pattern check
3. Blocked import check
4. Suspicious pattern check
5. Command usage check (if direct execution enabled)
6. Path access check (if direct execution enabled)

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `code` | `str` | Python code to validate |

**Returns:** `SecurityValidationResult` indicating if code is safe

**Example:**

```python
validator = SecurityValidator()

result = validator.validate("result = 2 + 2")
print(result.is_safe)  # True

result = validator.validate("import subprocess")
print(result.is_safe)  # False
print(result.reason)   # "Blocked import(s) detected: subprocess"
```

---

## SecurityValidationResult

Result of security validation.

```python
from codemode.executor.security import SecurityValidationResult
```

### Attributes

| Name | Type | Description |
|------|------|-------------|
| `is_safe` | `bool` | Whether the code is safe to execute |
| `violations` | `list[str]` | List of security violations found |
| `reason` | `str` | Human-readable reason if unsafe |

### Class Methods

#### safe

```python
@classmethod
def safe() -> SecurityValidationResult
```

Create a result indicating code is safe.

#### unsafe

```python
@classmethod
def unsafe(
    violations: list[str],
    reason: str
) -> SecurityValidationResult
```

Create a result indicating code is unsafe.

**Example:**

```python
result = SecurityValidationResult.unsafe(
    violations=["eval"],
    reason="Blocked pattern: eval"
)
```

---

## ExecutorGrpcService

gRPC service handling execution requests from the main application.

```python
from codemode.executor.service import ExecutorGrpcService
```

### Constructor

```python
ExecutorGrpcService(
    code_runner: CodeRunner,
    config: SidecarConfig | None = None,
    main_app_target: str | None = None,
    api_key: str | None = None
)
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `code_runner` | `CodeRunner` | CodeRunner instance for executing code |
| `config` | `SidecarConfig \| None` | SidecarConfig for configuration (recommended) |
| `main_app_target` | `str \| None` | Main app gRPC target (legacy) |
| `api_key` | `str \| None` | API key for authentication (legacy) |

---

### Class Methods

#### from_config

```python
@classmethod
def from_config(
    config: SidecarConfig,
    security_validator: SecurityValidator | None = None
) -> ExecutorGrpcService
```

Create an ExecutorGrpcService from a SidecarConfig.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `config` | `SidecarConfig` | SidecarConfig instance |
| `security_validator` | `SecurityValidator \| None` | Optional SecurityValidator |

**Returns:** Configured `ExecutorGrpcService` instance

**Example:**

```python
from codemode.config import SidecarConfig

config = SidecarConfig.from_env()
service = ExecutorGrpcService.from_config(config)
```

---

### gRPC Methods

#### Execute

```python
async def Execute(request, context) -> ExecutionResponse
```

Execute code with tool access.

Reads correlation ID from both request field and `x-correlation-id` metadata header.

---

#### Health

```python
async def Health(request, context) -> HealthResponse
```

Return health status of the executor.

---

#### Ready

```python
async def Ready(request, context) -> HealthResponse
```

Check readiness by pinging main app ToolService.

---

## Server Functions

### serve

```python
async def serve(config: SidecarConfig | None = None) -> None
```

Start the executor gRPC server.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `config` | `SidecarConfig \| None` | Optional SidecarConfig. Auto-loads from file or env if not provided |

**Example:**

```python
import asyncio
from codemode.executor.service import serve

asyncio.run(serve())
```

---

### main

```python
def main() -> None
```

Entry point for the executor service.

```bash
python -m codemode.executor.service
```
