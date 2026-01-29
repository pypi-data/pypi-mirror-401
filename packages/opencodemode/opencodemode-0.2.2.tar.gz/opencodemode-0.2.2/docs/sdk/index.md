# SDK Documentation

This section provides comprehensive documentation for using the Codemode SDK effectively in your applications. It covers async patterns, concurrency, context management, and best practices for building robust multi-agent AI systems.

## Overview

The Codemode SDK is designed with the following principles:

- **Async-First**: All core operations have async variants for non-blocking execution
- **Thread-Safe**: Context isolation ensures safe concurrent usage in multi-tenant environments
- **Framework-Agnostic**: Works with CrewAI, LangChain, and custom agent frameworks
- **Production-Ready**: Built-in retry logic, error handling, and lifecycle management

## Documentation Structure

| Document | Description |
|----------|-------------|
| [Getting Started](getting-started.md) | Quick setup and basic usage examples |
| [Core Concepts](core-concepts.md) | SDK architecture and design patterns |
| [Async Patterns](async-patterns.md) | Async/await usage and best practices |
| [Concurrency](concurrency.md) | Thread safety guarantees and concurrent execution |
| [Context Management](context-management.md) | RuntimeContext for multi-tenant isolation |
| [Tool Development](tool-development.md) | Building custom tools with async support |
| [Error Handling](error-handling.md) | Exception handling and recovery patterns |

## Key Features

### Async-First Design

The SDK provides both sync and async interfaces:

```python
# Synchronous (blocking)
result = codemode.execute("result = 2 + 2")

# Asynchronous (non-blocking)
result = await codemode.execute_async("result = 2 + 2")
```

### Thread-Safe Context Isolation

Each async task maintains isolated context, preventing data leakage between concurrent requests:

```python
async def handle_request(client_id: str):
    codemode.with_context(client_id=client_id)
    # Context is isolated to this task
    result = await codemode.execute_async(code)
```

### Context Managers

Clean resource management with both sync and async context managers:

```python
# Sync context manager
with Codemode.from_client_config(config) as codemode:
    result = codemode.execute(code)

# Async context manager
async with ExecutorClient(...) as client:
    result = await client.execute_async(...)
```

## Quick Example

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
        # Set context for this request
        codemode.with_context(
            client_id="acme",
            user_id="user_123",
        )

        # Execute code asynchronously
        result = await codemode.execute_async("""
            import json
            data = {"status": "success", "value": 42}
            result = json.dumps(data)
        """)

        print(result)

asyncio.run(main())
```

## Version Compatibility

This documentation covers Codemode version 0.2.x and later. Key changes from earlier versions:

- `execute_async()` now uses non-blocking retries
- Context is now isolated per async task using `ContextVar`
- `ExecutorClient` supports async context manager

## Next Steps

- Start with [Getting Started](getting-started.md) for setup instructions
- Read [Async Patterns](async-patterns.md) for async/await best practices
- Review [Concurrency](concurrency.md) for multi-tenant deployments
