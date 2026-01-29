# Codemode

Secure code execution for multi-agent AI systems.

Codemode provides a secure, isolated execution environment for AI agents to run Python code. It bridges the gap between AI frameworks like CrewAI and safe code execution by running code in containerized sidecars with full security controls.

## Key Features

- **Secure Execution**: Run AI-generated code in isolated Docker containers with resource limits and security policies
- **Framework Integration**: Native support for CrewAI with LangChain and LangGraph coming soon
- **Tool System**: Register tools in your main application that code running in the sidecar can call back to
- **TLS Encryption**: Full mTLS support for secure communication between components
- **Retry Logic**: Automatic retries with exponential backoff for transient failures
- **Correlation IDs**: End-to-end request tracing across the distributed system

## Architecture Overview

Codemode uses a two-component architecture:

```
+------------------+        gRPC/HTTP         +------------------+
|                  | -----------------------> |                  |
|   Main App       |    Execute Code          |   Executor       |
|   (Client)       | <----------------------- |   Sidecar        |
|                  |    Tool Callbacks        |   (Docker)       |
+------------------+                          +------------------+
```

1. **Main Application (Client)**: Your AI application that sends code to the executor
2. **Executor Sidecar**: A Docker container that safely executes code and calls back to your app for tool access

## Quick Start

### Installation

```bash
pip install opencodemode
```

### Basic Usage

```python
from codemode import Codemode
from codemode.config import ClientConfig

# Configure the client
config = ClientConfig(
    executor_url="http://localhost:8001",
    executor_api_key="your-api-key",
)

# Create Codemode instance
codemode = Codemode.from_client_config(config)

# Execute code
result = codemode.execute("result = 2 + 2")
print(result)  # "4"
```

### With CrewAI

```python
from crewai import Agent, Task, Crew
from codemode import Codemode
from codemode.config import ClientConfig

# Initialize Codemode
config = ClientConfig(
    executor_url="http://executor:8001",
    executor_api_key="secret-key",
)
codemode = Codemode.from_client_config(config)

# Get the CrewAI tool
code_tool = codemode.as_crewai_tool()

# Create an agent with the code execution capability
developer = Agent(
    role="Python Developer",
    goal="Write and execute Python code to solve problems",
    tools=[code_tool],
    backstory="You are an expert Python developer",
)

# Create and run a task
task = Task(
    description="Calculate the first 10 Fibonacci numbers",
    agent=developer,
    expected_output="List of first 10 Fibonacci numbers",
)

crew = Crew(agents=[developer], tasks=[task])
result = crew.kickoff()
```

## Documentation Sections

- [Getting Started](getting-started/installation.md) - Installation, quickstart, and core concepts
- [Configuration](configuration/index.md) - Client and sidecar configuration reference
- [Architecture](architecture/overview.md) - System design and component breakdown
- [Features](features/tools.md) - Tools, schemas, and framework integrations
- [SDK Guide](sdk/index.md) - Async patterns, concurrency, and context management
- [Deployment](deployment/docker.md) - Docker and production deployment guides
- [API Reference](api-reference/core.md) - Complete API documentation
- [Development](development/contributing.md) - Contributing and testing guides
- [Migration](migration/v0.2.0.md) - Version migration guides

## Requirements

- Python 3.11+
- Docker (for the executor sidecar)

## License

MIT License - see [LICENSE](https://github.com/mldlwizard/code_mode/blob/main/LICENSE) for details.
