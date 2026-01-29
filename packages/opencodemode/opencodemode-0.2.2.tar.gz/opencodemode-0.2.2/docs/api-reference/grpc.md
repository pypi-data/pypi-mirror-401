# gRPC Services API

Codemode uses gRPC for communication between the main application and the executor sidecar. This document describes the service definitions, message types, and usage patterns.

## Architecture Overview

```
+------------------+          +------------------+
|   Main App       |          |   Executor       |
|                  |          |   Sidecar        |
|  ToolService     |<---------|  ExecutorService |
|  (port 50051)    |  CallTool|  (port 8001)     |
|                  |          |                  |
|  ExecutorClient  |--------->|  CodeRunner      |
|                  |  Execute |                  |
+------------------+          +------------------+
```

- **ToolService**: Runs in the main app, handles tool calls from the executor
- **ExecutorService**: Runs in the sidecar, executes code in isolation

---

## ToolService

The ToolService runs in the main application and handles tool calls from the executor sidecar.

```protobuf
service ToolService {
  rpc CallTool(ToolCallRequest) returns (ToolCallResponse);
  rpc ListTools(google.protobuf.Empty) returns (ListToolsResponse);
  rpc GetToolSchema(GetToolSchemaRequest) returns (GetToolSchemaResponse);
}
```

### CallTool

Execute a registered tool.

**Request: ToolCallRequest**

| Field | Type | Description |
|-------|------|-------------|
| `tool_name` | `string` | Name of the tool to call |
| `arguments` | `google.protobuf.Struct` | Tool arguments as key-value pairs |
| `context` | `google.protobuf.Struct` | Optional runtime context |
| `correlation_id` | `string` | Optional correlation ID for tracing |

**Response: ToolCallResponse**

| Field | Type | Description |
|-------|------|-------------|
| `success` | `bool` | Whether the call succeeded |
| `error` | `string` | Error message if failed |
| `result` | `google.protobuf.Struct` | Tool result as key-value pairs |
| `correlation_id` | `string` | Echo back correlation ID |

**Example:**

```python
import grpc
from codemode.protos import codemode_pb2, codemode_pb2_grpc
from google.protobuf.struct_pb2 import Struct

channel = grpc.insecure_channel("localhost:50051")
stub = codemode_pb2_grpc.ToolServiceStub(channel)

# Build arguments
args = Struct()
args.update({"location": "NYC", "units": "celsius"})

request = codemode_pb2.ToolCallRequest(
    tool_name="weather",
    arguments=args,
    correlation_id="req-123"
)

response = stub.CallTool(request, timeout=30)
if response.success:
    print(response.result)
else:
    print(f"Error: {response.error}")
```

---

### ListTools

List all available tools with metadata.

**Request:** `google.protobuf.Empty`

**Response: ListToolsResponse**

| Field | Type | Description |
|-------|------|-------------|
| `tools` | `repeated ToolInfo` | List of tool information |

**ToolInfo:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Tool identifier |
| `is_async` | `bool` | Whether tool.run() is async |
| `has_context` | `bool` | Whether tool supports run_with_context() |
| `description` | `string` | Human-readable description |
| `input_schema` | `ToolSchema` | JSON Schema for input parameters |
| `output_schema` | `ToolSchema` | JSON Schema for return type |

**Example:**

```python
from google.protobuf import empty_pb2

response = stub.ListTools(empty_pb2.Empty())
for tool in response.tools:
    print(f"Tool: {tool.name}")
    print(f"  Async: {tool.is_async}")
    print(f"  Description: {tool.description}")
```

---

### GetToolSchema

Get detailed schema for a specific tool.

**Request: GetToolSchemaRequest**

| Field | Type | Description |
|-------|------|-------------|
| `tool_name` | `string` | Name of the tool |

**Response: GetToolSchemaResponse**

| Field | Type | Description |
|-------|------|-------------|
| `tool_name` | `string` | Tool name |
| `input_schema` | `ToolSchema` | JSON Schema for input |
| `output_schema` | `ToolSchema` | JSON Schema for output |
| `description` | `string` | Tool description |
| `is_async` | `bool` | Whether tool is async |
| `has_context` | `bool` | Whether tool supports context |

**Example:**

```python
request = codemode_pb2.GetToolSchemaRequest(tool_name="weather")
response = stub.GetToolSchema(request)
print(response.input_schema.json_schema)
```

---

## ExecutorService

The ExecutorService runs in the sidecar and executes code in isolation.

```protobuf
service ExecutorService {
  rpc Execute(ExecutionRequest) returns (ExecutionResponse);
  rpc Health(google.protobuf.Empty) returns (HealthResponse);
  rpc Ready(google.protobuf.Empty) returns (HealthResponse);
}
```

### Execute

Execute Python code in the isolated environment.

**Request: ExecutionRequest**

| Field | Type | Description |
|-------|------|-------------|
| `code` | `string` | Python code to execute |
| `available_tools` | `repeated string` | List of tool names available |
| `config` | `google.protobuf.Struct` | Configuration dictionary |
| `timeout` | `int32` | Execution timeout in seconds |
| `context` | `google.protobuf.Struct` | Optional runtime context |
| `correlation_id` | `string` | Optional correlation ID |

**Response: ExecutionResponse**

| Field | Type | Description |
|-------|------|-------------|
| `success` | `bool` | Whether execution succeeded |
| `result` | `string` | Execution result |
| `stdout` | `string` | Standard output |
| `stderr` | `string` | Standard error |
| `error` | `string` | Error message if failed |
| `correlation_id` | `string` | Echo back correlation ID |
| `error_type` | `string` | Error classification |
| `duration_ms` | `float` | Execution duration in milliseconds |

**Example:**

```python
import grpc
from codemode.protos import codemode_pb2, codemode_pb2_grpc
from google.protobuf.struct_pb2 import Struct

channel = grpc.insecure_channel("localhost:8001")
stub = codemode_pb2_grpc.ExecutorServiceStub(channel)

config = Struct()
config.update({"max_retries": 3})

request = codemode_pb2.ExecutionRequest(
    code="result = 2 + 2",
    available_tools=["weather", "database"],
    config=config,
    timeout=30,
    correlation_id="cm-abc123"
)

# Add authentication
metadata = [("authorization", "Bearer secret-key")]

response = stub.Execute(request, timeout=35, metadata=metadata)
if response.success:
    print(f"Result: {response.result}")
    print(f"Duration: {response.duration_ms}ms")
else:
    print(f"Error ({response.error_type}): {response.error}")
```

---

### Health

Check if the executor service is healthy.

**Request:** `google.protobuf.Empty`

**Response: HealthResponse**

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Health status (`"healthy"`) |
| `version` | `string` | Service version |
| `main_app_target` | `string` | Configured main app target |

**Example:**

```python
from google.protobuf import empty_pb2

response = stub.Health(empty_pb2.Empty(), timeout=5)
print(f"Status: {response.status}")
print(f"Version: {response.version}")
```

---

### Ready

Check if the executor can reach the main application.

**Request:** `google.protobuf.Empty`

**Response: HealthResponse**

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | `"ready"` or `"unreachable"` |
| `version` | `string` | Service version |
| `main_app_target` | `string` | Main app target being checked |

---

## Proto Message Definitions

### Complete Proto File

```protobuf
syntax = "proto3";

package codemode;

import "google/protobuf/struct.proto";
import "google/protobuf/empty.proto";

message ExecutionRequest {
  string code = 1;
  repeated string available_tools = 2;
  google.protobuf.Struct config = 3;
  int32 timeout = 4;
  google.protobuf.Struct context = 5;
  string correlation_id = 6;
}

message ExecutionResponse {
  bool success = 1;
  string result = 2;
  string stdout = 3;
  string stderr = 4;
  string error = 5;
  string correlation_id = 6;
  string error_type = 7;
  float duration_ms = 8;
}

message HealthResponse {
  string status = 1;
  string version = 2;
  string main_app_target = 3;
}

message ToolCallRequest {
  string tool_name = 1;
  google.protobuf.Struct arguments = 2;
  google.protobuf.Struct context = 3;
  string correlation_id = 4;
}

message ToolCallResponse {
  bool success = 1;
  string error = 2;
  google.protobuf.Struct result = 3;
  string correlation_id = 4;
}

message ToolSchema {
  string json_schema = 1;
}

message ToolInfo {
  string name = 1;
  bool is_async = 2;
  bool has_context = 3;
  string description = 4;
  ToolSchema input_schema = 5;
  ToolSchema output_schema = 6;
}

message ListToolsResponse {
  repeated ToolInfo tools = 1;
}

message GetToolSchemaRequest {
  string tool_name = 1;
}

message GetToolSchemaResponse {
  string tool_name = 1;
  ToolSchema input_schema = 2;
  ToolSchema output_schema = 3;
  string description = 4;
  bool is_async = 5;
  bool has_context = 6;
}

service ExecutorService {
  rpc Execute(ExecutionRequest) returns (ExecutionResponse);
  rpc Health(google.protobuf.Empty) returns (HealthResponse);
  rpc Ready(google.protobuf.Empty) returns (HealthResponse);
}

service ToolService {
  rpc CallTool(ToolCallRequest) returns (ToolCallResponse);
  rpc ListTools(google.protobuf.Empty) returns (ListToolsResponse);
  rpc GetToolSchema(GetToolSchemaRequest) returns (GetToolSchemaResponse);
}
```

---

## Connection Setup Examples

### Insecure Connection

```python
import grpc
from codemode.protos import codemode_pb2_grpc

# Connect to executor
channel = grpc.insecure_channel("localhost:8001")
executor_stub = codemode_pb2_grpc.ExecutorServiceStub(channel)

# Connect to tool service
channel = grpc.insecure_channel("localhost:50051")
tool_stub = codemode_pb2_grpc.ToolServiceStub(channel)
```

### Secure Connection (TLS)

```python
import grpc
from codemode.protos import codemode_pb2_grpc

# Load CA certificate
with open("ca.pem", "rb") as f:
    ca_cert = f.read()

credentials = grpc.ssl_channel_credentials(root_certificates=ca_cert)
channel = grpc.secure_channel("executor:8001", credentials)
stub = codemode_pb2_grpc.ExecutorServiceStub(channel)
```

### Mutual TLS (mTLS)

```python
import grpc
from codemode.protos import codemode_pb2_grpc

# Load certificates
with open("ca.pem", "rb") as f:
    ca_cert = f.read()
with open("client.pem", "rb") as f:
    client_cert = f.read()
with open("client-key.pem", "rb") as f:
    client_key = f.read()

credentials = grpc.ssl_channel_credentials(
    root_certificates=ca_cert,
    private_key=client_key,
    certificate_chain=client_cert
)

channel = grpc.secure_channel("executor:8001", credentials)
stub = codemode_pb2_grpc.ExecutorServiceStub(channel)
```

### Async Connection

```python
import grpc.aio
from codemode.protos import codemode_pb2, codemode_pb2_grpc

async def execute_code():
    async with grpc.aio.insecure_channel("localhost:8001") as channel:
        stub = codemode_pb2_grpc.ExecutorServiceStub(channel)

        request = codemode_pb2.ExecutionRequest(
            code="result = 42",
            available_tools=[],
            timeout=30
        )

        response = await stub.Execute(request, timeout=35)
        return response.result
```

---

## Starting the Services

### ToolService (Main App)

```python
from codemode.core import ComponentRegistry
from codemode.grpc.server import start_tool_service

registry = ComponentRegistry()
registry.register_tool("weather", weather_tool)

# Blocking (standalone server)
start_tool_service(
    registry=registry,
    host="0.0.0.0",
    port=50051,
    api_key="secret-key"
)
```

### ToolService (Async)

```python
from codemode.grpc.server import start_tool_service_async

async def main():
    server = await start_tool_service_async(
        registry=registry,
        port=50051,
        api_key="secret-key"
    )
    # Server is now running in background
    await some_other_task()
```

### ExecutorService (Sidecar)

```python
from codemode.executor.service import serve
from codemode.config import SidecarConfig

config = SidecarConfig(
    port=8001,
    main_app_grpc_target="app:50051",
    api_key="secret-key"
)

import asyncio
asyncio.run(serve(config))
```

Or via command line:

```bash
python -m codemode.executor.service
```

---

## Authentication

Both services support API key authentication via the `authorization` metadata header.

```python
metadata = [("authorization", "Bearer your-api-key")]
response = stub.Execute(request, metadata=metadata)
```

The correlation ID can be passed via the `x-correlation-id` header:

```python
metadata = [
    ("authorization", "Bearer your-api-key"),
    ("x-correlation-id", "cm-abc123")
]
```

---

## Error Handling

### gRPC Status Codes

| Code | Meaning |
|------|---------|
| `OK` | Success |
| `UNAUTHENTICATED` | Invalid or missing API key |
| `NOT_FOUND` | Tool not found |
| `DEADLINE_EXCEEDED` | Request timed out |
| `UNAVAILABLE` | Service unavailable |
| `RESOURCE_EXHAUSTED` | Rate limited |

### Example Error Handling

```python
import grpc

try:
    response = stub.Execute(request, timeout=35)
except grpc.RpcError as e:
    if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
        print("Request timed out")
    elif e.code() == grpc.StatusCode.UNAUTHENTICATED:
        print("Invalid API key")
    elif e.code() == grpc.StatusCode.UNAVAILABLE:
        print("Service unavailable")
    else:
        print(f"gRPC error: {e.details()}")
```
