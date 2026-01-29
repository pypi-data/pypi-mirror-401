# Tool System

Codemode provides a flexible tool system that allows code executing in the isolated sidecar to call functions registered in your main application. This creates a secure bridge between isolated execution and your application's capabilities.

## Overview

The tool system works through an RPC bridge:

1. You register tools in your main application
2. Code running in the executor sidecar can call these tools
3. Tool calls are routed back to your main app via gRPC
4. Results are returned to the executing code

```
+------------------+                    +------------------+
|   Main App       |                    |   Executor       |
|                  |                    |   Sidecar        |
|  registry.       |  <-- gRPC call --  |  tools['db']     |
|  register_tool() |                    |    .run(...)     |
|                  |  -- result -->     |                  |
+------------------+                    +------------------+
```

## Registering Tools

### Basic Registration

Register tools in your main application using the `ComponentRegistry`:

```python
from codemode import Codemode

codemode = Codemode.from_env()

# Register a simple function
def get_weather(location: str) -> dict:
    """Get current weather for a location."""
    return {"location": location, "temperature": 72, "conditions": "sunny"}

codemode.registry.register_tool(
    name="weather",
    func=get_weather,
    description="Get current weather for a location",
)
```

### With Input/Output Schemas

For better validation and documentation, register tools with Pydantic schemas:

```python
from pydantic import BaseModel

class WeatherInput(BaseModel):
    location: str
    units: str = "fahrenheit"

class WeatherOutput(BaseModel):
    location: str
    temperature: float
    conditions: str
    units: str

def get_weather(location: str, units: str = "fahrenheit") -> dict:
    # Implementation
    return {
        "location": location,
        "temperature": 72,
        "conditions": "sunny",
        "units": units,
    }

codemode.registry.register_tool(
    name="weather",
    func=get_weather,
    description="Get current weather for a location",
    input_schema=WeatherInput,
    output_schema=WeatherOutput,
)
```

### Async Tools

Register async functions for I/O-bound operations:

```python
async def query_database(query: str) -> list:
    """Execute a database query."""
    async with get_connection() as conn:
        return await conn.fetch(query)

codemode.registry.register_tool(
    name="database",
    func=query_database,
    description="Execute a database query",
)
```

## Using Tools in Executed Code

When code runs in the executor, tools are available through the `tools` dictionary:

```python
# Code executed in the sidecar
result = tools['weather'].run(location='New York')
print(result)  # {'location': 'New York', 'temperature': 72, ...}

# With multiple tools
weather = tools['weather'].run(location='NYC')
db_result = tools['database'].run(query=f"INSERT INTO weather VALUES ('{weather}')")
result = {'weather': weather, 'saved': True}
```

### Async Tools in Executed Code

For async tools, use `await`:

```python
# Async tool call
data = await tools['api'].run(endpoint='/users')

# Multiple async calls with gather
import asyncio

results = await asyncio.gather(
    tools['api'].run(endpoint='/users'),
    tools['api'].run(endpoint='/orders'),
)
```

## Meta-Tools

Codemode provides built-in meta-tools for tool discovery:

### __list__

List all available tools:

```python
# In executed code
all_tools = tools['__list__'].run()
print(all_tools)  # ['weather', 'database', 'api', ...]
```

### __schema__

Get schema information for a tool:

```python
# In executed code
schema = tools['__schema__'].run(tool_name='weather')
print(schema)
# {
#     'name': 'weather',
#     'description': 'Get current weather for a location',
#     'input_schema': {...},
#     'output_schema': {...}
# }
```

## Tool Service Setup

For the tool system to work, you need to run the ToolService in your main application:

```python
from codemode import Codemode
from codemode.grpc import start_tool_service_async
import asyncio

codemode = Codemode.from_env()

# Register tools
codemode.registry.register_tool("weather", get_weather, "Get weather")
codemode.registry.register_tool("database", query_database, "Query database")

# Start the tool service
async def main():
    await start_tool_service_async(
        registry=codemode.registry,
        host="0.0.0.0",
        port=50051,
    )

asyncio.run(main())
```

### With FastAPI

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from codemode import Codemode
from codemode.grpc import start_tool_service_async

codemode = Codemode.from_env()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start tool service on startup
    await start_tool_service_async(
        registry=codemode.registry,
        host="0.0.0.0",
        port=50051,
    )
    yield
    # Cleanup on shutdown

app = FastAPI(lifespan=lifespan)
```

## Best Practices

### 1. Descriptive Names and Descriptions

Use clear, descriptive names and comprehensive descriptions:

```python
# Good
codemode.registry.register_tool(
    name="customer_lookup",
    func=lookup_customer,
    description="Look up customer information by ID or email. Returns customer profile including name, email, and purchase history.",
)

# Avoid
codemode.registry.register_tool(
    name="lookup",
    func=lookup_customer,
    description="Looks up data",
)
```

### 2. Use Schemas for Complex Inputs

Define Pydantic models for tools with multiple parameters:

```python
class SearchInput(BaseModel):
    query: str
    filters: dict = {}
    limit: int = 10
    offset: int = 0

codemode.registry.register_tool(
    name="search",
    func=search_items,
    description="Search items in the catalog",
    input_schema=SearchInput,
)
```

### 3. Handle Errors Gracefully

Tools should handle errors and return meaningful error messages:

```python
def safe_database_query(query: str) -> dict:
    try:
        result = execute_query(query)
        return {"success": True, "data": result}
    except DatabaseError as e:
        return {"success": False, "error": str(e)}
```

### 4. Validate Inputs

Validate inputs before performing operations:

```python
from pydantic import BaseModel, field_validator

class EmailInput(BaseModel):
    email: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v
```

## Security Considerations

- Tools execute in your main application with full access to your resources
- The executor sidecar only sees the results, not your implementation
- Use API key authentication between sidecar and main app
- Enable TLS for secure communication
- Validate and sanitize all tool inputs
- Implement rate limiting for expensive operations

See [Security Model](../architecture/security-model.md) for more details.

## Related Documentation

- [Input/Output Schemas](schemas.md) - Detailed schema documentation
- [RPC Bridge](rpc-bridge.md) - How tool calls are routed
- [API Reference](../api-reference/core.md) - ComponentRegistry API
