# SDK Core Concepts

This document explains the fundamental concepts and design patterns used in the Codemode SDK.

## Architecture Overview

The Codemode SDK consists of several layers:

```
+------------------+
|   Codemode       |  High-level API with sync/async methods
+------------------+
         |
+------------------+
|   Registry       |  Component and context management
+------------------+
         |
+------------------+
| ExecutorClient   |  gRPC communication with retry logic
+------------------+
         |
+------------------+
|   Executor       |  Docker sidecar for code execution
+------------------+
```

## Key Components

### Codemode

The main entry point providing a unified interface:

```python
from codemode import Codemode

# High-level API
codemode = Codemode.from_client_config(config)
result = codemode.execute(code)  # Sync
result = await codemode.execute_async(code)  # Async
```

**Responsibilities:**
- Configuration management
- Registry access
- ExecutorClient lifecycle
- Framework integrations (CrewAI, etc.)

### ComponentRegistry

Manages tools, agents, and runtime context:

```python
from codemode.core import ComponentRegistry

registry = ComponentRegistry()

# Register components
registry.register_tool("weather", weather_tool)
registry.register_agent("researcher", researcher_agent)

# Set/get runtime context
registry.set_context(RuntimeContext(variables={"client_id": "acme"}))
context = registry.get_context()
```

**Key Features:**
- Thread-safe context using `ContextVar`
- Framework-agnostic component storage
- Schema management for tools

### ExecutorClient

Low-level gRPC client with enterprise features:

```python
from codemode.core import ExecutorClient

client = ExecutorClient(
    executor_url="http://localhost:8001",
    api_key="secret",
    retry_max_attempts=3,
)

# Execute with full control
result = await client.execute_async(
    code="result = 42",
    available_tools=["weather"],
    config={},
    context=runtime_context,
    correlation_id="req-123",
)
```

**Key Features:**
- Automatic retry with exponential backoff
- Correlation ID propagation
- Non-blocking async execution
- TLS support

## Execution Flow

### Synchronous Execution

```
execute()
    └── execute_async()  [wrapped in asyncio.run() or thread pool]
            └── _execute_with_retry()
                    └── gRPC Execute()
                            └── Executor processes code
                                    └── Tool callbacks (if needed)
```

### Asynchronous Execution

```
await execute_async()
    └── _execute_with_retry()  [non-blocking asyncio.sleep() retries]
            └── gRPC async Execute()
                    └── Executor processes code
                            └── Tool callbacks (if needed)
```

## Context Isolation

Context is isolated per async task using Python's `ContextVar`:

```python
# Task A                          # Task B
registry.set_context(             registry.set_context(
    RuntimeContext(                   RuntimeContext(
        variables={                       variables={
            "client": "A"                     "client": "B"
        }                                 }
    )                                 )
)                                 )

# Each task sees only its own context
registry.get_context()            registry.get_context()
# -> {"client": "A"}              # -> {"client": "B"}
```

## Lifecycle Management

### Automatic Cleanup

Use context managers for automatic resource cleanup:

```python
# Resources automatically released
async with Codemode.from_client_config(config) as codemode:
    result = await codemode.execute_async(code)
# Connection closed here
```

### Manual Cleanup

```python
codemode = Codemode.from_client_config(config)
try:
    result = codemode.execute(code)
finally:
    codemode.close()  # Always close to release resources
```

## Configuration Hierarchy

Configuration can come from multiple sources:

```
1. Explicit parameters (highest priority)
   └── ClientConfig(executor_url="...")

2. YAML configuration file
   └── Codemode.from_client_config(config_path="codemode-client.yaml")

3. Environment variables (lowest priority)
   └── CODEMODE_EXECUTOR_URL, CODEMODE_EXECUTOR_API_KEY
```

## Tool Registration

Tools are registered with the ComponentRegistry and made available to executed code:

```python
# 1. Define tool
class DatabaseTool:
    def run(self, query: str) -> list:
        return db.execute(query)

# 2. Register with schema
from pydantic import BaseModel

class QueryInput(BaseModel):
    query: str

registry.register_tool(
    name="database",
    tool=DatabaseTool(),
    input_schema=QueryInput,
    description="Execute database queries",
)

# 3. Use in executed code
code = """
results = tools['database'].run(query='SELECT * FROM users')
result = len(results)
"""
```

## Retry Semantics

ExecutorClient implements automatic retry with exponential backoff:

```
Attempt 1: Immediate
    └── Failure (UNAVAILABLE)
Attempt 2: Wait 100ms (base)
    └── Failure (DEADLINE_EXCEEDED)
Attempt 3: Wait 200ms (100ms * 2)
    └── Success

Total wait: 300ms
```

**Retryable status codes:**
- `UNAVAILABLE` - Service temporarily unavailable
- `DEADLINE_EXCEEDED` - Request timeout
- `RESOURCE_EXHAUSTED` - Rate limiting

## Correlation IDs

Every request can be traced with a correlation ID:

```python
# Auto-generated
result = await client.execute_async(code=code, ...)
print(result.correlation_id)  # "cm-2x5f9k-a7b3"

# Custom ID
result = await client.execute_async(
    code=code,
    correlation_id="my-request-123",
    ...
)
```

Correlation IDs flow through:
1. Client request
2. Executor processing
3. Tool callbacks
4. Response

## Best Practices

1. **Use async methods in async contexts**
   ```python
   # In FastAPI, use execute_async
   @app.post("/execute")
   async def run_code(code: str):
       return await codemode.execute_async(code)
   ```

2. **Always use context managers**
   ```python
   async with Codemode.from_client_config(config) as codemode:
       result = await codemode.execute_async(code)
   ```

3. **Set context before execution**
   ```python
   codemode.with_context(client_id=client_id)
   result = await codemode.execute_async(code)
   ```

4. **Handle errors appropriately**
   ```python
   try:
       result = await codemode.execute_async(code)
   except ExecutorTimeoutError:
       # Handle timeout
   except ExecutorConnectionError:
       # Handle connection issues
   ```

## Next Steps

- [Async Patterns](async-patterns.md) - Deep dive into async/await usage
- [Concurrency](concurrency.md) - Thread safety and concurrent execution
- [Context Management](context-management.md) - RuntimeContext details
