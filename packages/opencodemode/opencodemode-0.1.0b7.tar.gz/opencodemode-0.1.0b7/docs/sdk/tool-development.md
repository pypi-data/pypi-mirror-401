# Tool Development

This guide covers building custom tools for the Codemode SDK, including async support and schema definitions.

## Tool Basics

Tools are Python objects that executed code can call back to. They allow sandboxed code to interact with external resources through a controlled interface.

### Simple Tool

```python
class CalculatorTool:
    """A simple calculator tool."""

    def run(self, expression: str) -> float:
        """Evaluate a mathematical expression."""
        # Use a safe evaluator in production
        return eval(expression)

# Register the tool
codemode.registry.register_tool("calculator", CalculatorTool())

# Use in executed code
code = """
result = tools['calculator'].run(expression='2 + 2 * 3')
"""
result = codemode.execute(code)  # "8"
```

## Async Tools

For I/O-bound operations, implement async tools using `run_async()`:

```python
import aiohttp

class AsyncWeatherTool:
    """Weather tool with async support."""

    async def run_async(self, location: str) -> dict:
        """Async implementation - preferred for I/O operations."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.weather.com/{location}"
            ) as resp:
                return await resp.json()

    def run(self, location: str) -> dict:
        """Sync fallback for non-async contexts."""
        import asyncio
        return asyncio.run(self.run_async(location))
```

The SDK's `_is_tool_async()` automatically detects `run_async()` methods:

```python
def _is_tool_async(self, tool: Any) -> bool:
    """Check if a tool supports async execution."""
    return (
        inspect.iscoroutinefunction(tool)
        or inspect.iscoroutinefunction(getattr(tool, "run", None))
        or inspect.iscoroutinefunction(getattr(tool, "run_with_context", None))
        or inspect.iscoroutinefunction(getattr(tool, "run_async", None))
    )
```

## Tool with Schemas

Define input/output schemas for validation and documentation:

```python
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    """Input schema for weather tool."""
    location: str = Field(..., description="City name or coordinates")
    units: str = Field("celsius", description="Temperature units: celsius or fahrenheit")

class WeatherOutput(BaseModel):
    """Output schema for weather tool."""
    temperature: float = Field(..., description="Current temperature")
    conditions: str = Field(..., description="Weather conditions")
    humidity: int = Field(..., description="Humidity percentage")

class WeatherTool:
    def run(self, location: str, units: str = "celsius") -> dict:
        # Implementation
        return {
            "temperature": 22.5,
            "conditions": "partly cloudy",
            "humidity": 65,
        }

# Register with schemas
codemode.registry.register_tool(
    name="weather",
    tool=WeatherTool(),
    input_schema=WeatherInput,
    output_schema=WeatherOutput,
    description="Get current weather for a location",
)
```

## Context-Aware Tools

Access runtime context within tools:

```python
class TenantDatabaseTool:
    """Database tool that respects tenant context."""

    def __init__(self, registry):
        self.registry = registry
        self.db = DatabaseConnection()

    def run(self, query: str) -> list:
        # Get context set by the caller
        context = self.registry.get_context()

        if not context:
            raise ValueError("No tenant context provided")

        tenant_id = context.get("tenant_id")
        if not tenant_id:
            raise ValueError("tenant_id required in context")

        # Query scoped to tenant
        return self.db.query(
            query,
            schema=f"tenant_{tenant_id}",
        )

# Usage
codemode.with_context(tenant_id="acme")
codemode.registry.register_tool("database", TenantDatabaseTool(codemode.registry))

code = """
users = tools['database'].run(query='SELECT * FROM users')
result = len(users)
"""
result = codemode.execute(code)
```

## Meta-Tools Pattern

Meta-tools dynamically invoke other tools:

```python
class ToolDispatcher:
    """Meta-tool that dispatches to registered tools."""

    def __init__(self, registry):
        self.registry = registry

    async def run_async(self, tool_name: str, **kwargs) -> Any:
        """Async dispatch to another tool."""
        tool = self.registry.get_tool(tool_name)

        # Check if target tool is async
        if hasattr(tool, "run_async"):
            return await tool.run_async(**kwargs)
        elif hasattr(tool, "run"):
            return tool.run(**kwargs)
        else:
            raise ValueError(f"Tool {tool_name} has no run method")

    def run(self, tool_name: str, **kwargs) -> Any:
        """Sync dispatch."""
        tool = self.registry.get_tool(tool_name)
        return tool.run(**kwargs)
```

## Tool Lifecycle

### Initialization

```python
class DatabaseTool:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._pool = None

    async def _ensure_pool(self):
        if self._pool is None:
            self._pool = await create_pool(self.connection_string)

    async def run_async(self, query: str) -> list:
        await self._ensure_pool()
        return await self._pool.fetch(query)
```

### Cleanup

```python
class CleanupAwareTool:
    def __init__(self):
        self.resources = []

    def run(self, data: str) -> str:
        # Use resources
        return processed_data

    def close(self):
        """Called when registry is cleared."""
        for resource in self.resources:
            resource.close()
```

## Error Handling in Tools

```python
class RobustTool:
    """Tool with proper error handling."""

    def run(self, query: str) -> dict:
        try:
            result = self._execute_query(query)
            return {"success": True, "data": result}
        except ConnectionError:
            return {"success": False, "error": "Database connection failed"}
        except TimeoutError:
            return {"success": False, "error": "Query timed out"}
        except Exception as e:
            # Log the full error, return safe message
            logger.exception(f"Tool error: {e}")
            return {"success": False, "error": "Internal error"}
```

## Validation with Pydantic

```python
from pydantic import BaseModel, Field, field_validator

class EmailInput(BaseModel):
    to: str = Field(..., description="Recipient email")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body")

    @field_validator("to")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v

class EmailTool:
    def run(self, to: str, subject: str, body: str) -> dict:
        # Validate input
        input_data = EmailInput(to=to, subject=subject, body=body)

        # Send email
        send_email(input_data.to, input_data.subject, input_data.body)

        return {"sent": True}
```

## Testing Tools

```python
import pytest
from codemode.core import ComponentRegistry

class TestWeatherTool:
    @pytest.fixture
    def registry(self):
        return ComponentRegistry()

    @pytest.fixture
    def tool(self, registry):
        tool = WeatherTool()
        registry.register_tool("weather", tool)
        return tool

    def test_run_returns_weather(self, tool):
        result = tool.run(location="NYC")
        assert "temperature" in result
        assert "conditions" in result

    @pytest.mark.asyncio
    async def test_run_async(self, tool):
        result = await tool.run_async(location="NYC")
        assert "temperature" in result

class TestContextAwareTool:
    @pytest.fixture
    def registry(self):
        return ComponentRegistry()

    def test_requires_context(self, registry):
        tool = TenantDatabaseTool(registry)

        # Should fail without context
        with pytest.raises(ValueError, match="No tenant context"):
            tool.run(query="SELECT 1")

    def test_uses_context(self, registry):
        tool = TenantDatabaseTool(registry)

        registry.set_context(RuntimeContext(variables={"tenant_id": "acme"}))

        # Should succeed with context
        result = tool.run(query="SELECT 1")
        assert result is not None
```

## Tool Patterns

### HTTP API Tool

```python
import httpx

class APITool:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    async def run_async(self, endpoint: str, method: str = "GET", **kwargs) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                f"{self.base_url}/{endpoint}",
                headers={"Authorization": f"Bearer {self.api_key}"},
                **kwargs,
            )
            response.raise_for_status()
            return response.json()
```

### Caching Tool Wrapper

```python
from functools import lru_cache
import hashlib
import json

class CachedTool:
    def __init__(self, tool, ttl_seconds: int = 300):
        self.tool = tool
        self.cache = {}
        self.ttl = ttl_seconds

    def _cache_key(self, **kwargs) -> str:
        return hashlib.md5(
            json.dumps(kwargs, sort_keys=True).encode()
        ).hexdigest()

    def run(self, **kwargs) -> Any:
        key = self._cache_key(**kwargs)

        if key in self.cache:
            cached, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return cached

        result = self.tool.run(**kwargs)
        self.cache[key] = (result, time.time())
        return result
```

### Rate-Limited Tool

```python
import asyncio
from collections import deque
import time

class RateLimitedTool:
    def __init__(self, tool, max_calls: int, period_seconds: int):
        self.tool = tool
        self.max_calls = max_calls
        self.period = period_seconds
        self.calls = deque()
        self.lock = asyncio.Lock()

    async def run_async(self, **kwargs) -> Any:
        async with self.lock:
            now = time.time()

            # Remove old calls
            while self.calls and self.calls[0] < now - self.period:
                self.calls.popleft()

            # Wait if at limit
            if len(self.calls) >= self.max_calls:
                wait_time = self.calls[0] + self.period - now
                await asyncio.sleep(wait_time)

            self.calls.append(now)

        return await self.tool.run_async(**kwargs)
```

## Best Practices

1. **Implement both sync and async methods** for flexibility
2. **Use Pydantic for input validation**
3. **Handle errors gracefully** - don't leak internal details
4. **Access context for multi-tenant isolation**
5. **Register tools at startup** before concurrent usage
6. **Document your tools** with clear descriptions and schemas

## Next Steps

- [Context Management](context-management.md) - Using context in tools
- [Error Handling](error-handling.md) - Exception patterns
- [Async Patterns](async-patterns.md) - Async tool best practices
