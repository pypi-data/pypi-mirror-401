# Getting Started with the SDK

This guide walks you through setting up and using the Codemode SDK in your Python application.

## Installation

Install the Codemode package with your preferred framework integration:

```bash
# Basic installation
pip install opencodemode

# With CrewAI support
pip install opencodemode[crewai]
```

## Basic Setup

### 1. Start the Executor Sidecar

The executor runs in a Docker container:

```bash
docker run -d \
  --name codemode-executor \
  -p 8001:8001 \
  -e CODEMODE_API_KEY=your-secret-key \
  ghcr.io/anomalyco/codemode-executor:latest
```

### 2. Initialize the Client

```python
from codemode import Codemode
from codemode.config import ClientConfig

config = ClientConfig(
    executor_url="http://localhost:8001",
    executor_api_key="your-secret-key",
)

codemode = Codemode.from_client_config(config)
```

### 3. Execute Code

```python
# Synchronous execution
result = codemode.execute("result = 2 + 2")
print(result)  # "4"
```

## Async Usage

For async applications (FastAPI, aiohttp, etc.), use the async methods:

```python
import asyncio
from codemode import Codemode
from codemode.config import ClientConfig

async def main():
    config = ClientConfig(
        executor_url="http://localhost:8001",
        executor_api_key="your-secret-key",
    )

    codemode = Codemode.from_client_config(config)

    try:
        # Async execution - non-blocking
        result = await codemode.execute_async("result = sum(range(100))")
        print(result)  # "4950"
    finally:
        codemode.close()

asyncio.run(main())
```

## Using Context Managers

The recommended pattern is using context managers for automatic cleanup:

```python
# Synchronous context manager
with Codemode.from_client_config(config) as codemode:
    result = codemode.execute("result = 'hello world'")

# Async context manager (Codemode class)
async with Codemode.from_client_config(config) as codemode:
    result = await codemode.execute_async("result = 'hello world'")
```

## Environment Variables

You can configure the client using environment variables:

```bash
export CODEMODE_EXECUTOR_URL="http://localhost:8001"
export CODEMODE_EXECUTOR_API_KEY="your-secret-key"
```

```python
# Initialize from environment
codemode = Codemode.from_env()
```

## With CrewAI

Integrate Codemode as a CrewAI tool:

```python
from crewai import Agent, Task, Crew
from codemode import Codemode
from codemode.config import ClientConfig

# Initialize Codemode
config = ClientConfig(
    executor_url="http://localhost:8001",
    executor_api_key="your-secret-key",
)
codemode = Codemode.from_client_config(config)

# Get the CrewAI tool
code_tool = codemode.as_crewai_tool()

# Create an agent with code execution capability
developer = Agent(
    role="Python Developer",
    goal="Write and execute Python code",
    tools=[code_tool],
    backstory="You are an expert Python developer",
)

# Create and run a task
task = Task(
    description="Calculate the factorial of 10",
    agent=developer,
    expected_output="The factorial of 10",
)

crew = Crew(agents=[developer], tasks=[task])
result = crew.kickoff()
```

## Registering Custom Tools

Make tools available to executed code:

```python
from codemode import Codemode
from codemode.config import ClientConfig

# Define a tool
class WeatherTool:
    def run(self, location: str) -> dict:
        # In production, call a real weather API
        return {"location": location, "temperature": 72, "conditions": "sunny"}

# Register the tool
config = ClientConfig(
    executor_url="http://localhost:8001",
    executor_api_key="your-secret-key",
)
codemode = Codemode.from_client_config(config)
codemode.registry.register_tool("weather", WeatherTool())

# Execute code that uses the tool
code = """
weather = tools['weather'].run(location='New York')
result = f"Temperature in {weather['location']}: {weather['temperature']}F"
"""
result = codemode.execute(code)
print(result)  # "Temperature in New York: 72F"
```

## Setting Runtime Context

Inject context variables for multi-tenant isolation:

```python
# Set context for this request
codemode.with_context(
    client_id="acme-corp",
    user_id="user_123",
    request_id="req_abc",
)

# Context is available in tools and execution
result = codemode.execute("result = 'processed'")
```

## Health Checks

Verify the executor is running:

```python
if codemode.health_check():
    print("Executor is healthy")
else:
    print("Executor is not responding")

if codemode.ready_check():
    print("Executor can reach the main application")
```

## Error Handling

Handle execution errors gracefully:

```python
from codemode.core.executor_client import (
    ExecutorClientError,
    ExecutorTimeoutError,
    ExecutorConnectionError,
)

try:
    result = codemode.execute("result = 1/0")
except ExecutorTimeoutError:
    print("Execution timed out")
except ExecutorConnectionError:
    print("Could not connect to executor")
except ExecutorClientError as e:
    print(f"Execution failed: {e}")
```

## Next Steps

- Learn about [Async Patterns](async-patterns.md) for non-blocking execution
- Understand [Concurrency](concurrency.md) guarantees for multi-tenant apps
- Explore [Context Management](context-management.md) for request isolation
- Build custom [Tools](tool-development.md) for your use case
