# Concurrency and Thread Safety

This guide covers the thread-safety guarantees provided by the Codemode SDK and best practices for concurrent usage.

## Thread Safety Guarantees

The Codemode SDK provides the following thread-safety guarantees:

| Component | Thread-Safe | Notes |
|-----------|-------------|-------|
| `RuntimeContext` | Yes | Uses `ContextVar` for per-task isolation |
| `ExecutorClient.execute_async()` | Yes | Each call is independent |
| `ExecutorClient.close()` | Yes | Idempotent with locking |
| `ComponentRegistry.get_context()` | Yes | Returns task-local context |
| `ComponentRegistry.register_tool()` | Partially | Safe if done at startup |

## Context Isolation with ContextVar

The SDK uses Python's `ContextVar` to ensure context isolation across concurrent async tasks:

```python
from contextvars import ContextVar

# Internal implementation
_runtime_context_var: ContextVar[RuntimeContext | None] = ContextVar(
    'codemode_runtime_context', default=None
)
```

This means each async task maintains its own context:

```python
import asyncio
from codemode import Codemode
from codemode.config import ClientConfig

async def handle_request(client_id: str, codemode: Codemode):
    # Set context - isolated to this task
    codemode.with_context(client_id=client_id)

    # Simulate work
    await asyncio.sleep(0.1)

    # Context is still correct for this task
    context = codemode.registry.get_context()
    assert context.get("client_id") == client_id

    result = await codemode.execute_async("result = 'done'")
    return result

async def main():
    config = ClientConfig(
        executor_url="http://localhost:8001",
        executor_api_key="your-api-key",
    )

    async with Codemode.from_client_config(config) as codemode:
        # Run concurrent requests with different contexts
        results = await asyncio.gather(
            handle_request("client_a", codemode),
            handle_request("client_b", codemode),
            handle_request("client_c", codemode),
        )
        # Each request sees its own context - no data leakage!
```

## Multi-Tenant Isolation

For multi-tenant applications, context isolation prevents data leakage between tenants:

```python
from fastapi import FastAPI, Request
from codemode import Codemode

app = FastAPI()

@app.middleware("http")
async def tenant_middleware(request: Request, call_next):
    # Extract tenant from request
    tenant_id = request.headers.get("X-Tenant-ID", "default")

    # Set context for this request
    codemode.with_context(
        tenant_id=tenant_id,
        request_id=str(uuid.uuid4()),
    )

    return await call_next(request)

@app.post("/execute")
async def execute(code: str):
    # Context is automatically isolated per request
    # Tenant A's context never leaks to Tenant B
    result = await codemode.execute_async(code)
    return {"result": result}
```

## Concurrent Test Example

Here's a test demonstrating context isolation:

```python
import asyncio
import pytest
from codemode.core import ComponentRegistry
from codemode.core.registry import RuntimeContext

@pytest.mark.asyncio
async def test_concurrent_context_isolation():
    """Verify contexts don't leak between concurrent tasks."""
    registry = ComponentRegistry()
    results = []

    async def task(client_id: str, delay: float):
        # Set unique context for this task
        context = RuntimeContext(variables={"client_id": client_id})
        registry.set_context(context)

        # Simulate async work (context switch point)
        await asyncio.sleep(delay)

        # Verify we still have our context
        retrieved = registry.get_context()
        results.append({
            "expected": client_id,
            "actual": retrieved.get("client_id") if retrieved else None
        })

        registry.clear_context()

    # Run concurrent tasks with overlapping execution
    await asyncio.gather(
        task("client_a", 0.1),
        task("client_b", 0.05),
        task("client_c", 0.15),
    )

    # Verify each task got its own context
    for r in results:
        assert r["expected"] == r["actual"], f"Context leaked: {r}"
```

## ExecutorClient Thread Safety

### Safe Concurrent Usage

```python
async def main():
    client = ExecutorClient(
        executor_url="http://localhost:8001",
        api_key="your-api-key",
    )

    try:
        # Safe: concurrent execute_async calls
        results = await asyncio.gather(
            client.execute_async(code="result = 1", available_tools=[], config={}),
            client.execute_async(code="result = 2", available_tools=[], config={}),
            client.execute_async(code="result = 3", available_tools=[], config={}),
        )
    finally:
        await client.close_async()
```

### Close Protection

The client includes protection against use-after-close:

```python
client = ExecutorClient(...)

await client.close_async()

# This will raise ExecutorClientError
try:
    await client.execute_async(...)
except ExecutorClientError as e:
    print(e)  # "Client has been closed"
```

Close is idempotent - calling it multiple times is safe:

```python
await client.close_async()  # First call closes
await client.close_async()  # Second call is a no-op
```

## Registration Thread Safety

Tool registration is thread-safe only when done at startup:

```python
# GOOD: Register at startup before any concurrent usage
def setup_codemode():
    codemode = Codemode.from_client_config(config)

    # Registration happens before any concurrent requests
    codemode.registry.register_tool("weather", WeatherTool())
    codemode.registry.register_tool("database", DatabaseTool())

    return codemode

# BAD: Don't register tools during concurrent request handling
@app.post("/register-tool")  # DON'T DO THIS
async def register_tool(name: str):
    codemode.registry.register_tool(name, SomeTool())  # Unsafe!
```

**Recommended Pattern:**

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

codemode: Codemode = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global codemode

    # Setup: register all tools at startup
    config = ClientConfig(...)
    codemode = Codemode.from_client_config(config)
    codemode.registry.register_tool("weather", WeatherTool())
    codemode.registry.register_tool("database", DatabaseTool())

    yield

    # Cleanup
    codemode.close()

app = FastAPI(lifespan=lifespan)
```

## Thread Pool Considerations

When using sync `execute()` from an async context, a thread pool is used:

```python
# Internal implementation (simplified)
def execute(self, code: str, ...) -> str:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(self.execute_async(code, ...))
    else:
        # Run in thread pool to avoid blocking event loop
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(asyncio.run, self.execute_async(code, ...))
            return future.result()
```

**Important**: Always prefer `execute_async()` in async contexts to avoid thread pool overhead.

## gRPC Channel Management

The SDK manages separate channels for sync and async usage:

```python
class ExecutorClient:
    def __init__(self, ...):
        # Sync channel (created immediately)
        self._channel = grpc.insecure_channel(...)
        self._stub = codemode_pb2_grpc.ExecutorServiceStub(self._channel)

        # Async channel (created lazily on first async call)
        self._async_channel: grpc.aio.Channel | None = None
        self._async_stub = None
```

gRPC channels handle their own connection pooling and are safe for concurrent use.

## Best Practices

### 1. Set Context Per Request

```python
async def handle_request(request: Request):
    codemode.with_context(
        client_id=request.client_id,
        request_id=str(uuid.uuid4()),
    )
    return await codemode.execute_async(code)
```

### 2. Register Tools at Startup

```python
# During application initialization
codemode.registry.register_tool("tool1", Tool1())
codemode.registry.register_tool("tool2", Tool2())
# ... then start accepting requests
```

### 3. Use One Client Per Application

```python
# Good: single shared client
codemode = Codemode.from_client_config(config)

# Avoid: creating new clients per request
@app.post("/execute")
async def execute(code: str):
    # DON'T create a new client per request
    codemode = Codemode.from_client_config(config)  # Bad!
    return await codemode.execute_async(code)
```

### 4. Clear Context When Done

```python
async def handle_request():
    try:
        codemode.with_context(client_id="acme")
        return await codemode.execute_async(code)
    finally:
        codemode.registry.clear_context()
```

## Debugging Concurrency Issues

### Enable Debug Logging

```python
import logging
logging.getLogger("codemode").setLevel(logging.DEBUG)
```

### Check Context State

```python
from codemode.core.registry import get_current_context

# Direct access to context (bypasses registry)
context = get_current_context()
print(f"Current context: {context}")
```

### Verify Isolation

```python
async def debug_task(task_id: str, registry: ComponentRegistry):
    registry.set_context(RuntimeContext(variables={"task_id": task_id}))

    context_before = registry.get_context()
    await asyncio.sleep(0.1)  # Allow context switches
    context_after = registry.get_context()

    assert context_before == context_after, "Context changed unexpectedly!"
```

## Next Steps

- [Context Management](context-management.md) - RuntimeContext details
- [Async Patterns](async-patterns.md) - Async/await best practices
- [Error Handling](error-handling.md) - Exception patterns
