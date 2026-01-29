# Core Concepts

This guide explains the fundamental concepts and architecture of Codemode, helping you understand how the system works and how to use it effectively.

## Architecture Overview

Codemode uses a client-sidecar architecture designed for secure, isolated code execution in multi-agent AI systems.

```
+-------------------+         gRPC/HTTP         +----------------------+
|                   |  ---------------------->  |                      |
|   Client App      |     Code Execution        |   Executor Sidecar   |
|   (Your Code)     |  <----------------------  |   (Docker Container) |
|                   |     Results + Callbacks   |                      |
+-------------------+                           +----------------------+
        |                                                  |
        |                                                  |
        v                                                  v
+-------------------+                           +----------------------+
|  Tool Registry    |                           |  Isolated Sandbox    |
|  (Local Tools)    |                           |  (Code Execution)    |
+-------------------+                           +----------------------+
```

### Request Flow

1. **Client sends code** - Your application sends Python code to the executor sidecar.
2. **Sidecar executes** - The sidecar runs the code in an isolated environment.
3. **Tool callbacks** - If the code needs tools (file access, APIs, etc.), the sidecar calls back to the client.
4. **Results returned** - Execution results (stdout, stderr, exit code) are returned to the client.

## Core Components

### Client

The `Codemode` class is the primary interface for interacting with the executor. It handles:

- Establishing connections to the executor sidecar
- Sending code for execution
- Receiving and processing results
- Managing tool callbacks

```python
from codemode import Codemode
from codemode.config import ClientConfig

config = ClientConfig(
    executor_url="http://localhost:8001",
    executor_api_key="your-secret-key"
)

codemode = Codemode.from_client_config(config)
```

Key methods:

| Method | Description |
|--------|-------------|
| `from_client_config(config)` | Create instance from ClientConfig object |
| `from_env()` | Create instance from environment variables |
| `execute(code)` | Execute Python code and return results |
| `as_crewai_tool()` | Return a CrewAI-compatible tool wrapper |

### Executor Sidecar

The executor sidecar is a Docker container that provides a secure, isolated environment for code execution. It:

- Runs untrusted code in a sandboxed environment
- Enforces resource limits (CPU, memory, time)
- Provides a consistent execution environment
- Handles tool callbacks to the client

The sidecar is designed to be stateless and disposable. Each execution runs in isolation, and the container can be restarted without losing critical state.

### Tools

Tools are functions that executed code can call back to on the client side. This allows sandboxed code to interact with external resources through a controlled interface.

```python
from codemode.tools import Tool

class FileReadTool(Tool):
    name = "read_file"
    description = "Read contents of a file"

    def execute(self, path: str) -> str:
        with open(path) as f:
            return f.read()
```

Tools enable:

- File system access (through the client, not the sidecar)
- API calls to external services
- Database queries
- Any operation that should be controlled by the host application

### Registry

The `ComponentRegistry` manages the collection of tools and agents available to your application. It provides:

- Registration of tools and agents
- Lookup by name or type
- Lifecycle management

```python
from codemode.core import ComponentRegistry
from codemode.tools import Tool

registry = ComponentRegistry()
registry.register_tool(my_custom_tool)
```

## Security Model

Codemode is designed with security as a primary concern. The architecture enforces multiple layers of protection:

### Isolation

- **Container isolation** - Code executes inside a Docker container, separated from the host system.
- **Network isolation** - The sidecar can be configured with restricted network access.
- **Resource limits** - CPU, memory, and execution time are bounded.

### Authentication

- **API key authentication** - All requests to the executor require a valid API key.
- **TLS encryption** - Communication between client and sidecar can be encrypted with TLS.

### Controlled Access

- **Tool callbacks** - Code cannot directly access host resources. It must use registered tools that the client controls.
- **No host filesystem access** - The sidecar has no access to the host filesystem unless explicitly mounted.

### Defense in Depth

```
+------------------+
|  API Key Auth    |  <-- First layer: Authentication
+------------------+
         |
+------------------+
|  TLS Encryption  |  <-- Second layer: Transport security
+------------------+
         |
+------------------+
|  Container       |  <-- Third layer: Process isolation
|  Isolation       |
+------------------+
         |
+------------------+
|  Resource Limits |  <-- Fourth layer: DoS protection
+------------------+
         |
+------------------+
|  Tool Callbacks  |  <-- Fifth layer: Controlled capabilities
+------------------+
```

## Configuration

Codemode uses separate configuration models for the client and sidecar, providing clear separation of concerns.

### ClientConfig

Configuration for the client application:

```python
from codemode.config import ClientConfig

config = ClientConfig(
    executor_url="http://localhost:8001",  # Sidecar URL
    executor_api_key="your-secret-key",    # Authentication key
    timeout=30,                            # Request timeout in seconds
    tls_enabled=False,                     # Enable TLS encryption
    tls_cert_path=None,                    # Path to TLS certificate
)
```

Key client settings:

| Setting | Environment Variable | Description |
|---------|---------------------|-------------|
| `executor_url` | `CODEMODE_EXECUTOR_URL` | URL of the executor sidecar |
| `executor_api_key` | `CODEMODE_EXECUTOR_API_KEY` | API key for authentication |
| `timeout` | `CODEMODE_TIMEOUT` | Request timeout in seconds |
| `tls_enabled` | `CODEMODE_TLS_ENABLED` | Enable TLS for secure communication |

### SidecarConfig

Configuration for the executor sidecar (set via environment variables in Docker):

| Setting | Environment Variable | Description |
|---------|---------------------|-------------|
| API Key | `CODEMODE_API_KEY` | Expected API key for authentication |
| Port | `CODEMODE_PORT` | Port to listen on (default: 8001) |
| Max Execution Time | `CODEMODE_MAX_EXEC_TIME` | Maximum execution time in seconds |
| Memory Limit | `CODEMODE_MEMORY_LIMIT` | Maximum memory usage |

Example Docker configuration:

```bash
docker run -d \
  -p 8001:8001 \
  -e CODEMODE_API_KEY=your-secret-key \
  -e CODEMODE_MAX_EXEC_TIME=60 \
  -e CODEMODE_MEMORY_LIMIT=512m \
  codemode/executor:latest
```

## Configuration Separation Rationale

The separation between ClientConfig and SidecarConfig serves several purposes:

1. **Security** - Client credentials and sidecar secrets are managed independently.
2. **Deployment flexibility** - Clients and sidecars can be configured, scaled, and updated independently.
3. **Environment parity** - Different environments (dev, staging, prod) can have different configurations without code changes.
4. **Least privilege** - Each component only has access to the configuration it needs.

## Execution Lifecycle

Understanding the execution lifecycle helps in debugging and optimizing your applications:

1. **Initialization** - Client establishes connection to sidecar
2. **Authentication** - API key is validated
3. **Code submission** - Python code is sent to the sidecar
4. **Sandbox creation** - Isolated execution environment is prepared
5. **Execution** - Code runs with resource limits enforced
6. **Tool callbacks** - Any tool calls are routed back to the client
7. **Result collection** - stdout, stderr, and exit code are captured
8. **Cleanup** - Sandbox resources are released
9. **Response** - Results are returned to the client

## Next Steps

- Follow the [Quickstart Guide](quickstart.md) to see these concepts in action.
- Explore [Hybrid Execution](../features/hybrid-execution.md) for advanced execution modes.
- Review [Secure Executor](../features/secure-executor.md) for detailed security configuration.
- Set up [TLS Encryption](../features/tls-encryption.md) for production deployments.
