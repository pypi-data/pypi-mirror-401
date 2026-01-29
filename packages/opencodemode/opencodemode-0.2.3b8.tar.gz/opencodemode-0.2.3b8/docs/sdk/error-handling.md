# Error Handling

This guide covers error handling patterns in the Codemode SDK.

## Exception Hierarchy

The SDK provides a hierarchy of exceptions for different error types:

```
ExecutorClientError (base)
├── ExecutorConnectionError
│   └── Connection to executor failed
├── ExecutorTimeoutError
│   └── Request timed out
└── (other gRPC errors)

ComponentNotFoundError
└── Component not in registry

ComponentAlreadyExistsError
└── Component already registered
```

## Importing Exceptions

```python
from codemode.core.executor_client import (
    ExecutorClientError,
    ExecutorConnectionError,
    ExecutorTimeoutError,
)

from codemode.core.registry import (
    ComponentNotFoundError,
    ComponentAlreadyExistsError,
)
```

## Basic Error Handling

### Execution Errors

```python
from codemode import Codemode
from codemode.core.executor_client import (
    ExecutorClientError,
    ExecutorConnectionError,
    ExecutorTimeoutError,
)

async def safe_execute(codemode: Codemode, code: str) -> str | None:
    try:
        return await codemode.execute_async(code)
    except ExecutorTimeoutError:
        logger.error("Execution timed out")
        return None
    except ExecutorConnectionError:
        logger.error("Could not connect to executor")
        return None
    except ExecutorClientError as e:
        logger.error(f"Execution failed: {e}")
        return None
```

### Registry Errors

```python
from codemode.core.registry import ComponentNotFoundError, ComponentAlreadyExistsError

# Handle missing component
try:
    tool = registry.get_tool("nonexistent")
except ComponentNotFoundError:
    logger.warning("Tool not found, using default")
    tool = DefaultTool()

# Handle duplicate registration
try:
    registry.register_tool("weather", weather_tool)
except ComponentAlreadyExistsError:
    logger.warning("Tool already registered, skipping")
```

## Error Types

### ExecutorConnectionError

Raised when the client cannot connect to the executor:

```python
try:
    result = await codemode.execute_async(code)
except ExecutorConnectionError as e:
    # Possible causes:
    # - Executor not running
    # - Network issues
    # - Wrong URL
    # - TLS configuration issues

    logger.error(f"Connection failed: {e}")

    # Retry or fall back
    if codemode.health_check():
        # Executor is up, retry
        result = await codemode.execute_async(code)
    else:
        # Executor is down
        raise ServiceUnavailableError("Executor not available")
```

### ExecutorTimeoutError

Raised when a request times out:

```python
try:
    result = await codemode.execute_async(
        code,
        execution_timeout=60,  # 60 seconds
    )
except ExecutorTimeoutError:
    # Possible causes:
    # - Code takes too long to execute
    # - Network latency
    # - Executor overloaded

    logger.warning("Execution timed out, code may still be running")

    # Don't retry immediately - wait and check
    await asyncio.sleep(5)
    if codemode.ready_check():
        # Executor recovered
        pass
```

### ExecutorClientError

Base exception for all executor errors:

```python
try:
    result = await codemode.execute_async(code)
except ExecutorClientError as e:
    # Includes connection and timeout errors
    # Also includes:
    # - Authentication failures
    # - Invalid requests
    # - Server errors

    logger.error(f"Executor error: {e}")
```

## Retry Patterns

### Automatic Retries

The ExecutorClient has built-in retry with exponential backoff:

```python
client = ExecutorClient(
    executor_url="http://localhost:8001",
    api_key="secret",
    retry_enabled=True,
    retry_max_attempts=3,
    retry_backoff_base_ms=100,
    retry_backoff_max_ms=5000,
    retry_status_codes=[
        grpc.StatusCode.UNAVAILABLE,
        grpc.StatusCode.DEADLINE_EXCEEDED,
        grpc.StatusCode.RESOURCE_EXHAUSTED,
    ],
)
```

### Manual Retry

```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
async def execute_with_retry(codemode: Codemode, code: str) -> str:
    return await codemode.execute_async(code)

# Usage
try:
    result = await execute_with_retry(codemode, code)
except Exception as e:
    logger.error(f"All retries failed: {e}")
```

## Error Recovery

### Circuit Breaker Pattern

```python
import time

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = 0
        self.state = "closed"  # closed, open, half-open

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "open"

    def record_success(self):
        self.failures = 0
        self.state = "closed"

    def can_execute(self) -> bool:
        if self.state == "closed":
            return True

        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
                return True
            return False

        return True  # half-open

# Usage
circuit = CircuitBreaker()

async def protected_execute(codemode: Codemode, code: str) -> str:
    if not circuit.can_execute():
        raise ServiceUnavailableError("Circuit breaker open")

    try:
        result = await codemode.execute_async(code)
        circuit.record_success()
        return result
    except ExecutorClientError as e:
        circuit.record_failure()
        raise
```

### Fallback Pattern

```python
async def execute_with_fallback(codemode: Codemode, code: str) -> str:
    try:
        return await codemode.execute_async(code)
    except ExecutorConnectionError:
        # Fallback to local execution (if safe)
        logger.warning("Executor unavailable, using local fallback")
        return execute_locally(code)
    except ExecutorTimeoutError:
        # Return cached result
        logger.warning("Execution timed out, using cached result")
        return get_cached_result(code)
```

## Error Context

### Correlation IDs

Use correlation IDs to trace errors across services:

```python
import uuid

async def execute_with_tracing(codemode: Codemode, code: str) -> str:
    correlation_id = str(uuid.uuid4())

    try:
        result = await codemode.executor_client.execute_async(
            code=code,
            available_tools=list(codemode.registry.tools.keys()),
            config={},
            correlation_id=correlation_id,
        )
        return result.result
    except ExecutorClientError as e:
        logger.error(
            f"Execution failed",
            extra={
                "correlation_id": correlation_id,
                "error": str(e),
            }
        )
        raise
```

### Rich Error Information

```python
from dataclasses import dataclass

@dataclass
class ExecutionError:
    message: str
    correlation_id: str
    code_snippet: str
    timestamp: float
    retry_count: int

async def detailed_execute(codemode: Codemode, code: str) -> str:
    correlation_id = str(uuid.uuid4())
    start_time = time.time()

    try:
        return await codemode.execute_async(code)
    except ExecutorClientError as e:
        error = ExecutionError(
            message=str(e),
            correlation_id=correlation_id,
            code_snippet=code[:100],
            timestamp=start_time,
            retry_count=0,
        )
        logger.error(f"Execution error: {error}")
        raise
```

## FastAPI Error Handling

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(ExecutorConnectionError)
async def connection_error_handler(request: Request, exc: ExecutorConnectionError):
    return JSONResponse(
        status_code=503,
        content={
            "error": "service_unavailable",
            "message": "Code execution service is not available",
        },
    )

@app.exception_handler(ExecutorTimeoutError)
async def timeout_error_handler(request: Request, exc: ExecutorTimeoutError):
    return JSONResponse(
        status_code=504,
        content={
            "error": "timeout",
            "message": "Code execution timed out",
        },
    )

@app.exception_handler(ExecutorClientError)
async def executor_error_handler(request: Request, exc: ExecutorClientError):
    return JSONResponse(
        status_code=500,
        content={
            "error": "execution_error",
            "message": str(exc),
        },
    )

@app.post("/execute")
async def execute_code(code: str):
    # Errors are handled by exception handlers
    result = await codemode.execute_async(code)
    return {"result": result}
```

## Tool Error Handling

### In Tools

```python
class SafeTool:
    def run(self, query: str) -> dict:
        try:
            result = self._execute(query)
            return {"success": True, "data": result}
        except ValueError as e:
            # Expected error - return as result
            return {"success": False, "error": str(e)}
        except Exception as e:
            # Unexpected error - log and return generic message
            logger.exception(f"Tool error: {e}")
            return {"success": False, "error": "Internal error"}
```

### Wrapping Tool Errors

```python
class ToolError(Exception):
    """Base exception for tool errors."""
    pass

class ToolNotFoundError(ToolError):
    """Tool not found in registry."""
    pass

class ToolExecutionError(ToolError):
    """Tool execution failed."""
    pass

def safe_tool_call(registry, tool_name: str, **kwargs):
    try:
        tool = registry.get_tool(tool_name)
    except ComponentNotFoundError:
        raise ToolNotFoundError(f"Tool '{tool_name}' not found")

    try:
        return tool.run(**kwargs)
    except Exception as e:
        raise ToolExecutionError(f"Tool '{tool_name}' failed: {e}") from e
```

## Logging Best Practices

```python
import logging
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.get_logger()

async def logged_execute(codemode: Codemode, code: str, client_id: str) -> str:
    log = logger.bind(
        client_id=client_id,
        code_length=len(code),
    )

    log.info("Starting execution")

    try:
        result = await codemode.execute_async(code)
        log.info("Execution successful", result_length=len(result))
        return result
    except ExecutorTimeoutError:
        log.warning("Execution timed out")
        raise
    except ExecutorConnectionError:
        log.error("Connection failed")
        raise
    except ExecutorClientError as e:
        log.error("Execution failed", error=str(e))
        raise
```

## Best Practices

1. **Catch specific exceptions** before generic ones
2. **Use correlation IDs** for tracing across services
3. **Implement circuit breakers** for resilience
4. **Log errors with context** for debugging
5. **Return meaningful error messages** to users
6. **Don't expose internal details** in error responses
7. **Implement retries** for transient failures
8. **Set appropriate timeouts** for operations

## Next Steps

- [Async Patterns](async-patterns.md) - Async error handling
- [Concurrency](concurrency.md) - Error handling in concurrent contexts
- [Context Management](context-management.md) - Error context propagation
