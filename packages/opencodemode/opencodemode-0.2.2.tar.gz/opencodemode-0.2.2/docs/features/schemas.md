# Input/Output Schemas

Codemode supports defining input and output schemas for tools using Pydantic models. Schemas provide validation, documentation, and help AI agents understand how to use tools correctly.

## Overview

Tool schemas serve multiple purposes:

1. **Validation**: Ensure tool inputs match expected types and constraints
2. **Documentation**: Generate API documentation for tools
3. **AI Guidance**: Help AI agents construct valid tool calls
4. **Type Safety**: Catch errors before execution

## Defining Schemas

### Input Schemas

Define input schemas using Pydantic `BaseModel`:

```python
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    """Input schema for the search tool."""

    query: str = Field(
        description="Search query string"
    )
    max_results: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of results to return"
    )
    filters: dict = Field(
        default_factory=dict,
        description="Optional filters to apply"
    )
```

### Output Schemas

Define output schemas to document what tools return:

```python
class SearchResult(BaseModel):
    """Single search result."""

    id: str
    title: str
    score: float
    snippet: str

class SearchOutput(BaseModel):
    """Output schema for the search tool."""

    results: list[SearchResult]
    total_count: int
    query: str
    execution_time_ms: int
```

## Registering Tools with Schemas

Register tools with both input and output schemas:

```python
from codemode import Codemode

codemode = Codemode.from_env()

def search(query: str, max_results: int = 10, filters: dict = None) -> dict:
    """Search the catalog."""
    # Implementation
    return {
        "results": [...],
        "total_count": 42,
        "query": query,
        "execution_time_ms": 15,
    }

codemode.registry.register_tool(
    name="search",
    func=search,
    description="Search the product catalog",
    input_schema=SearchInput,
    output_schema=SearchOutput,
)
```

## Schema Features

### Field Constraints

Use Pydantic's field validators for constraints:

```python
from pydantic import BaseModel, Field, field_validator

class OrderInput(BaseModel):
    product_id: str = Field(min_length=1, max_length=50)
    quantity: int = Field(ge=1, le=1000)
    price: float = Field(gt=0)

    @field_validator('product_id')
    @classmethod
    def validate_product_id(cls, v):
        if not v.startswith('PROD-'):
            raise ValueError('Product ID must start with PROD-')
        return v
```

### Optional Fields

Use `None` default or `Optional` for optional fields:

```python
class CustomerInput(BaseModel):
    email: str
    name: str | None = None
    phone: str | None = None
```

### Nested Models

Compose complex schemas with nested models:

```python
class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class CustomerInput(BaseModel):
    name: str
    email: str
    shipping_address: Address
    billing_address: Address | None = None
```

### Enums

Use enums for fixed choices:

```python
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskInput(BaseModel):
    title: str
    priority: Priority = Priority.MEDIUM
```

## JSON Schema Generation

Codemode converts Pydantic models to JSON Schema for interoperability:

```python
from codemode.tools.schema import pydantic_to_json_schema

json_schema = pydantic_to_json_schema(SearchInput)
print(json_schema)
```

Output:
```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Search query string"
    },
    "max_results": {
      "type": "integer",
      "default": 10,
      "minimum": 1,
      "maximum": 100,
      "description": "Maximum number of results to return"
    },
    "filters": {
      "type": "object",
      "default": {},
      "description": "Optional filters to apply"
    }
  },
  "required": ["query"]
}
```

## ToolRegistration Class

For advanced use cases, use the `ToolRegistration` class directly:

```python
from codemode.tools.schema import ToolRegistration

registration = ToolRegistration(
    name="search",
    func=search,
    description="Search the product catalog",
    input_schema=SearchInput,
    output_schema=SearchOutput,
)

# Access schema information
print(registration.input_json_schema)
print(registration.output_json_schema)
```

## Querying Schemas at Runtime

### Using Meta-Tools

In executed code, use the `__schema__` meta-tool:

```python
# Get schema for a specific tool
schema = tools['__schema__'].run(tool_name='search')
print(schema['input_schema'])
print(schema['output_schema'])
```

### Using gRPC API

The `GetToolSchema` RPC returns schema information:

```python
import grpc
from codemode.protos import codemode_pb2, codemode_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = codemode_pb2_grpc.ToolServiceStub(channel)

request = codemode_pb2.GetToolSchemaRequest(tool_name='search')
response = stub.GetToolSchema(request)

print(response.schema.input_schema)
print(response.schema.output_schema)
```

## Best Practices

### 1. Always Document Fields

Use `Field` with descriptions for all parameters:

```python
class APIInput(BaseModel):
    endpoint: str = Field(
        description="API endpoint path (e.g., '/users/123')"
    )
    method: str = Field(
        default="GET",
        description="HTTP method: GET, POST, PUT, DELETE"
    )
    body: dict | None = Field(
        default=None,
        description="Request body for POST/PUT requests"
    )
```

### 2. Use Sensible Defaults

Provide defaults where appropriate:

```python
class PaginationInput(BaseModel):
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)
```

### 3. Keep Schemas Focused

Each schema should represent a single concept:

```python
# Good: Focused schemas
class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None

# Avoid: Overloaded schema
class UserOperation(BaseModel):
    operation: str  # "create" or "update"
    name: str | None
    email: str | None
```

### 4. Validate Early

Use validators to catch errors before execution:

```python
from pydantic import field_validator
import re

class EmailInput(BaseModel):
    email: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()
```

### 5. Use Type Hints Consistently

Leverage Python's type system:

```python
from datetime import datetime
from typing import Literal

class EventInput(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    event_type: Literal["meeting", "reminder", "deadline"]
    attendees: list[str] = []
```

## Related Documentation

- [Tool System](tools.md) - Tool registration and usage
- [API Reference](../api-reference/core.md) - ComponentRegistry API
- [gRPC Services](../api-reference/grpc.md) - Schema-related RPCs
