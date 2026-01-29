# Context Management

This guide covers the `RuntimeContext` system for managing per-request state in multi-tenant applications.

## Overview

`RuntimeContext` provides a way to pass request-specific variables (client ID, user ID, session data) through the execution pipeline. It uses Python's `ContextVar` for automatic isolation across concurrent async tasks.

## Basic Usage

### Setting Context

```python
from codemode import Codemode
from codemode.config import ClientConfig

config = ClientConfig(
    executor_url="http://localhost:8001",
    executor_api_key="your-api-key",
)
codemode = Codemode.from_client_config(config)

# Set context using fluent API
codemode.with_context(
    client_id="acme-corp",
    user_id="user_123",
    session_id="sess_abc",
)

# Execute with context
result = await codemode.execute_async("result = 'done'")
```

### Getting Context

```python
# Get current context
context = codemode.registry.get_context()

if context:
    client_id = context.get("client_id")
    user_id = context.get("user_id")
```

### Clearing Context

```python
# Clear context for current task
codemode.registry.clear_context()
```

## RuntimeContext Class

The `RuntimeContext` dataclass holds request-specific variables:

```python
from codemode.core.registry import RuntimeContext

# Create context
context = RuntimeContext(
    variables={
        "client_id": "acme",
        "user_id": "user_123",
        "custom_data": {"key": "value"},
    }
)

# Access variables
client_id = context.get("client_id")  # "acme"
missing = context.get("missing", "default")  # "default"

# Check if variable exists
if "user_id" in context.variables:
    print(context.variables["user_id"])
```

## Direct Registry Access

For low-level control, use the registry directly:

```python
from codemode.core import ComponentRegistry
from codemode.core.registry import RuntimeContext

registry = ComponentRegistry()

# Set context
context = RuntimeContext(variables={"tenant": "acme"})
registry.set_context(context)

# Get context
current = registry.get_context()

# Clear context
registry.clear_context()
```

## Module-Level Access

Access context outside the registry using the module-level function:

```python
from codemode.core.registry import get_current_context, reset_context

# Get context directly (same as registry.get_context())
context = get_current_context()

# Reset context (useful in testing)
reset_context()
```

## Context in Tools

Context is automatically available in tool callbacks:

```python
class TenantAwareTool:
    def __init__(self, registry: ComponentRegistry):
        self.registry = registry

    def run(self, query: str) -> dict:
        # Access context set by the caller
        context = self.registry.get_context()

        if not context:
            raise ValueError("No context set")

        tenant_id = context.get("tenant_id")

        # Use tenant for multi-tenant database access
        return self.db.query(query, tenant=tenant_id)
```

## Context Flow

Context flows through the execution pipeline:

```
1. Request arrives
   └── codemode.with_context(client_id="acme")
       └── Context stored in ContextVar (task-local)

2. Code execution
   └── codemode.execute_async(code)
       └── Context passed to executor

3. Tool callback
   └── tools['database'].run(query)
       └── Tool accesses context via registry

4. Response
   └── Result returned with context metadata
```

## Multi-Tenant Example

Complete example for a multi-tenant SaaS application:

```python
from fastapi import FastAPI, Request, HTTPException
from codemode import Codemode
from codemode.config import ClientConfig
import uuid

app = FastAPI()
codemode: Codemode = None

@app.on_event("startup")
async def startup():
    global codemode
    config = ClientConfig(
        executor_url="http://localhost:8001",
        executor_api_key="your-api-key",
    )
    codemode = Codemode.from_client_config(config)

    # Register tenant-aware tools
    codemode.registry.register_tool("database", TenantDatabaseTool(codemode.registry))

@app.middleware("http")
async def context_middleware(request: Request, call_next):
    # Extract tenant from auth token or header
    tenant_id = request.headers.get("X-Tenant-ID")
    user_id = request.headers.get("X-User-ID")

    if not tenant_id:
        return HTTPException(status_code=401, detail="Missing tenant")

    # Set context for this request
    codemode.with_context(
        tenant_id=tenant_id,
        user_id=user_id,
        request_id=str(uuid.uuid4()),
    )

    try:
        response = await call_next(request)
        return response
    finally:
        # Clean up context
        codemode.registry.clear_context()

@app.post("/execute")
async def execute_code(code: str):
    # Context is already set by middleware
    # Tools will automatically see tenant context
    result = await codemode.execute_async(code)
    return {"result": result}


class TenantDatabaseTool:
    """Database tool that respects tenant context."""

    def __init__(self, registry):
        self.registry = registry

    def run(self, query: str) -> list:
        context = self.registry.get_context()

        if not context:
            raise ValueError("No tenant context")

        tenant_id = context.get("tenant_id")

        # Query is automatically scoped to tenant
        return db.query(query, tenant_schema=tenant_id)
```

## Context Isolation Guarantee

Context is isolated per async task using `ContextVar`:

```python
import asyncio
from codemode.core import ComponentRegistry
from codemode.core.registry import RuntimeContext

async def demonstrate_isolation():
    registry = ComponentRegistry()

    async def task_a():
        registry.set_context(RuntimeContext(variables={"task": "A"}))
        await asyncio.sleep(0.1)  # Allow context switches
        ctx = registry.get_context()
        assert ctx.get("task") == "A"  # Still "A", not affected by task_b

    async def task_b():
        registry.set_context(RuntimeContext(variables={"task": "B"}))
        await asyncio.sleep(0.05)
        ctx = registry.get_context()
        assert ctx.get("task") == "B"  # Still "B", not affected by task_a

    # Run concurrently - contexts don't interfere
    await asyncio.gather(task_a(), task_b())
```

## Context with CrewAI

When using CrewAI integration, context is passed to tool executions:

```python
from crewai import Agent, Task, Crew

# Set context before crew execution
codemode.with_context(
    client_id="acme",
    execution_id="exec_123",
)

# Get the CrewAI tool
code_tool = codemode.as_crewai_tool()

# Create agent with context-aware tool
agent = Agent(
    role="Analyst",
    tools=[code_tool],
    backstory="You analyze data",
)

task = Task(
    description="Analyze customer data",
    agent=agent,
    expected_output="Analysis report",
)

# Context is available during all tool executions
crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```

## Common Patterns

### Request ID Tracking

```python
import uuid

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())

    codemode.with_context(request_id=request_id)

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    return response
```

### Audit Logging

```python
class AuditTool:
    def __init__(self, registry):
        self.registry = registry

    def run(self, action: str) -> str:
        context = self.registry.get_context()

        # Log with context
        logger.info(
            f"Action: {action}",
            extra={
                "client_id": context.get("client_id"),
                "user_id": context.get("user_id"),
                "request_id": context.get("request_id"),
            }
        )

        return "logged"
```

### Feature Flags

```python
codemode.with_context(
    client_id="acme",
    features={
        "new_algorithm": True,
        "beta_access": False,
    },
)

class FeatureAwareTool:
    def run(self, operation: str) -> str:
        context = self.registry.get_context()
        features = context.get("features", {})

        if features.get("new_algorithm"):
            return self.new_algorithm(operation)
        else:
            return self.legacy_algorithm(operation)
```

## Best Practices

### 1. Set Context Early

Set context at the request boundary, before any business logic:

```python
@app.middleware("http")
async def context_middleware(request: Request, call_next):
    codemode.with_context(...)  # Set early
    return await call_next(request)
```

### 2. Always Clear Context

Clear context to prevent memory leaks in long-running processes:

```python
try:
    codemode.with_context(client_id="acme")
    result = await codemode.execute_async(code)
finally:
    codemode.registry.clear_context()
```

### 3. Use Meaningful Keys

Use descriptive, consistent key names:

```python
# Good
codemode.with_context(
    tenant_id="acme",
    user_id="user_123",
    correlation_id="req_abc",
)

# Avoid
codemode.with_context(
    t="acme",
    u="user_123",
    c="req_abc",
)
```

### 4. Don't Store Sensitive Data

Avoid storing passwords, tokens, or PII in context:

```python
# Bad - sensitive data in context
codemode.with_context(
    api_key="secret_123",  # Don't do this
    password="hunter2",    # Don't do this
)

# Good - store references only
codemode.with_context(
    user_id="user_123",  # Reference, not the actual data
)
```

## Next Steps

- [Concurrency](concurrency.md) - Thread safety guarantees
- [Tool Development](tool-development.md) - Building context-aware tools
- [Error Handling](error-handling.md) - Exception patterns
