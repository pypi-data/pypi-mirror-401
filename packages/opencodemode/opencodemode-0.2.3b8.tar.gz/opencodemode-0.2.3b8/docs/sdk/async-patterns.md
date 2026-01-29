# Async Patterns

This guide covers async/await usage patterns in the Codemode SDK for building high-performance, non-blocking applications.

## Why Async?

The Codemode SDK is designed async-first for several reasons:

1. **Non-blocking I/O**: Code execution and tool callbacks involve network I/O
2. **Scalability**: Async code handles many concurrent requests efficiently
3. **Framework compatibility**: Modern frameworks like FastAPI are async-native
4. **Resource efficiency**: No thread pool overhead for waiting on I/O

## Basic Async Usage

### Simple Execution

```python
import asyncio
from codemode import Codemode
from codemode.config import ClientConfig

async def main():
    config = ClientConfig(
        executor_url="http://localhost:8001",
        executor_api_key="your-api-key",
    )

    codemode = Codemode.from_client_config(config)

    try:
        result = await codemode.execute_async("result = 2 + 2")
        print(result)  # "4"
    finally:
        codemode.close()

asyncio.run(main())
```

### Using Async Context Manager

```python
async def main():
    config = ClientConfig(
        executor_url="http://localhost:8001",
        executor_api_key="your-api-key",
    )

    async with Codemode.from_client_config(config) as codemode:
        result = await codemode.execute_async("result = 2 + 2")
        print(result)
```

## ExecutorClient Async Methods

The `ExecutorClient` provides async methods for low-level control:

### execute_async

Primary async execution method with non-blocking retries:

```python
from codemode.core import ExecutorClient

async def execute_code():
    client = ExecutorClient(
        executor_url="http://localhost:8001",
        api_key="your-api-key",
    )

    try:
        result = await client.execute_async(
            code="result = sum(range(100))",
            available_tools=["weather", "database"],
            config={},
            execution_timeout=30,
        )

        if result.success:
            print(f"Result: {result.result}")
        else:
            print(f"Error: {result.error}")
    finally:
        await client.close_async()
```

### Async Context Manager

```python
async with ExecutorClient(
    executor_url="http://localhost:8001",
    api_key="your-api-key",
) as client:
    result = await client.execute_async(
        code="result = 42",
        available_tools=[],
        config={},
    )
```

## Non-Blocking Retries

The SDK uses `asyncio.sleep()` for retry delays, ensuring the event loop remains responsive:

```python
# Internal retry logic (simplified)
async def _execute_with_retry(self, ...):
    for attempt in range(max_attempts):
        try:
            return await self._execute_once_async(...)
        except RetryableError:
            if attempt < max_attempts - 1:
                delay = self._calculate_backoff(attempt)
                await asyncio.sleep(delay / 1000)  # Non-blocking!
    raise ExecutorClientError("Max retries exceeded")
```

This is a key improvement over sync `time.sleep()` which would block the entire event loop.

## Concurrent Execution

Execute multiple code blocks concurrently:

```python
import asyncio
from codemode import Codemode
from codemode.config import ClientConfig

async def main():
    config = ClientConfig(
        executor_url="http://localhost:8001",
        executor_api_key="your-api-key",
    )

    async with Codemode.from_client_config(config) as codemode:
        # Execute multiple code blocks concurrently
        tasks = [
            codemode.execute_async("result = 1 + 1"),
            codemode.execute_async("result = 2 + 2"),
            codemode.execute_async("result = 3 + 3"),
        ]

        results = await asyncio.gather(*tasks)
        print(results)  # ["2", "4", "6"]
```

## FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from codemode import Codemode
from codemode.config import ClientConfig
from contextlib import asynccontextmanager

# Global codemode instance
codemode: Codemode = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global codemode
    config = ClientConfig(
        executor_url="http://localhost:8001",
        executor_api_key="your-api-key",
    )
    codemode = Codemode.from_client_config(config)
    yield
    codemode.close()

app = FastAPI(lifespan=lifespan)

@app.post("/execute")
async def execute_code(code: str, client_id: str):
    # Set context for this request
    codemode.with_context(client_id=client_id)

    try:
        result = await codemode.execute_async(code)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Sync vs Async Methods

| Method | Behavior | Use When |
|--------|----------|----------|
| `execute()` | Blocks until complete | Sync code, scripts, CLI tools |
| `execute_async()` | Non-blocking, returns awaitable | Async frameworks, concurrent requests |

### How Sync Methods Work

The sync `execute()` method wraps async execution:

```python
def execute(self, code: str, ...) -> str:
    """Sync wrapper around execute_async."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # No event loop - create one
        return asyncio.run(self.execute_async(code, ...))
    else:
        # Already in event loop - run in thread pool
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(asyncio.run, self.execute_async(code, ...))
            return future.result()
```

**Important**: Avoid calling `execute()` from within an async context. Use `execute_async()` instead.

## Async Tool Callbacks

When executed code calls back to tools, the SDK properly handles async tools:

```python
class AsyncDatabaseTool:
    """Tool with async run method."""

    async def run_async(self, query: str) -> list:
        """Async execution method - preferred."""
        async with aiohttp.ClientSession() as session:
            async with session.post(DB_URL, json={"query": query}) as resp:
                return await resp.json()

    def run(self, query: str) -> list:
        """Sync fallback."""
        return asyncio.run(self.run_async(query))

# Register the tool
registry.register_tool("database", AsyncDatabaseTool())
```

The SDK's `_is_tool_async()` detects `run_async()` methods and calls them appropriately.

## Error Handling in Async Code

```python
from codemode.core.executor_client import (
    ExecutorClientError,
    ExecutorTimeoutError,
    ExecutorConnectionError,
)

async def safe_execute(codemode, code: str) -> str | None:
    try:
        return await codemode.execute_async(code)
    except ExecutorTimeoutError:
        logger.error("Execution timed out")
        return None
    except ExecutorConnectionError:
        logger.error("Connection to executor failed")
        return None
    except ExecutorClientError as e:
        logger.error(f"Execution error: {e}")
        return None
```

## Timeouts

Set timeouts at multiple levels:

```python
# Client-level timeout (applies to all requests)
client = ExecutorClient(
    executor_url="http://localhost:8001",
    api_key="your-api-key",
    timeout=60,  # 60 second default
)

# Per-request timeout
result = await client.execute_async(
    code="result = long_running_computation()",
    available_tools=[],
    config={},
    execution_timeout=120,  # 2 minutes for this specific request
)

# asyncio timeout wrapper
async def execute_with_timeout(codemode, code: str, timeout: float):
    try:
        return await asyncio.wait_for(
            codemode.execute_async(code),
            timeout=timeout,
        )
    except asyncio.TimeoutError:
        raise ExecutorTimeoutError("Client-side timeout exceeded")
```

## Best Practices

### 1. Always Use Async in Async Contexts

```python
# Bad - blocks the event loop
@app.post("/execute")
async def run_code(code: str):
    return codemode.execute(code)  # DON'T DO THIS

# Good - non-blocking
@app.post("/execute")
async def run_code(code: str):
    return await codemode.execute_async(code)
```

### 2. Use Context Managers

```python
# Good - automatic cleanup
async with Codemode.from_client_config(config) as codemode:
    result = await codemode.execute_async(code)
```

### 3. Handle Cancellation

```python
async def cancellable_execution(codemode, code: str):
    try:
        return await codemode.execute_async(code)
    except asyncio.CancelledError:
        logger.info("Execution was cancelled")
        raise
```

### 4. Limit Concurrency

```python
import asyncio

async def rate_limited_execution(codemode, codes: list[str], max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def execute_one(code: str):
        async with semaphore:
            return await codemode.execute_async(code)

    return await asyncio.gather(*[execute_one(code) for code in codes])
```

## CrewAI Integration

The `CodemodeTool` for CrewAI uses async methods internally. Both `_run()` and `_arun()` are async:

```python
from codemode import Codemode
from crewai import Agent, Crew, Task

codemode = Codemode.from_config("codemode.yaml")
tool = codemode.as_crewai_tool()

# CrewAI handles async tools transparently
orchestrator = Agent(
    role="Orchestrator",
    tools=[tool],  # Async tool works seamlessly
    ...
)

# Sync kickoff - CrewAI awaits the tool internally
crew = Crew(agents=[orchestrator], tasks=[...])
result = crew.kickoff()

# Async kickoff - fully non-blocking
async def run_crew():
    crew = Crew(agents=[orchestrator], tasks=[...])
    return await crew.kickoff_async()
```

The async implementation ensures:
- Non-blocking execution in async contexts
- Proper error propagation with detailed diagnostics
- Correlation IDs for tracing across services

## Next Steps

- [Concurrency](concurrency.md) - Thread safety guarantees
- [Context Management](context-management.md) - Per-request isolation
- [Error Handling](error-handling.md) - Exception patterns
