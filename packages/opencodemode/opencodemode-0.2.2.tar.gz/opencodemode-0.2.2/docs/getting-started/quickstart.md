# Quickstart

Get up and running with Codemode in 5 minutes. This guide walks you through setting up the executor sidecar, creating a client, and executing code securely.

## Overview

Codemode uses a client-sidecar architecture:

1. **Executor Sidecar** - A Docker container that securely executes code in isolation.
2. **Client** - Your application that sends code to the sidecar for execution.

## Step 1: Start the Executor Sidecar

Run the executor sidecar container:

```bash
docker run -d \
  --name codemode-executor \
  -p 8001:8001 \
  -e CODEMODE_API_KEY=your-secret-key \
  codemode/executor:latest
```

Verify the container is running:

```bash
docker ps | grep codemode-executor
```

The executor is now listening on `http://localhost:8001`.

## Step 2: Create a Client Application

Create a new Python file `app.py`:

```python
from codemode import Codemode
from codemode.config import ClientConfig

# Configure the client
config = ClientConfig(
    executor_url="http://localhost:8001",
    executor_api_key="your-secret-key"
)

# Initialize Codemode
codemode = Codemode.from_client_config(config)

# Execute code
result = codemode.execute("""
x = 5
y = 10
result = x + y
print(f"The sum is: {result}")
""")

print(f"Output: {result.stdout}")
print(f"Exit code: {result.exit_code}")
```

Run your application:

```bash
python app.py
```

Expected output:

```
Output: The sum is: 15
Exit code: 0
```

## Step 3: Using Environment Variables

For production deployments, use environment variables instead of hardcoding credentials:

```bash
export CODEMODE_EXECUTOR_URL="http://localhost:8001"
export CODEMODE_EXECUTOR_API_KEY="your-secret-key"
```

Then initialize the client from environment:

```python
from codemode import Codemode

# Automatically reads from environment variables
codemode = Codemode.from_env()

result = codemode.execute("print('Hello from Codemode!')")
print(result.stdout)
```

## Step 4: Handling Execution Results

The `execute()` method returns a result object with detailed information:

```python
from codemode import Codemode

codemode = Codemode.from_env()

result = codemode.execute("""
import sys
print("Standard output")
print("Error message", file=sys.stderr)
exit(0)
""")

# Access execution results
print(f"stdout: {result.stdout}")
print(f"stderr: {result.stderr}")
print(f"exit_code: {result.exit_code}")
print(f"success: {result.exit_code == 0}")
```

## Step 5: Using with CrewAI

Codemode integrates seamlessly with CrewAI for multi-agent workflows. First, install the CrewAI extra:

```bash
pip install opencodemode[crewai]
```

Create an agent with code execution capabilities:

```python
from crewai import Agent, Task, Crew
from codemode import Codemode

# Initialize Codemode
codemode = Codemode.from_env()

# Create a Codemode tool for CrewAI
code_execution_tool = codemode.as_crewai_tool()

# Create an agent with code execution capability
developer_agent = Agent(
    role="Python Developer",
    goal="Write and execute Python code to solve problems",
    backstory="An experienced Python developer who writes clean, efficient code.",
    tools=[code_execution_tool],
    verbose=True
)

# Define a task
coding_task = Task(
    description="Calculate the first 10 Fibonacci numbers and print them",
    expected_output="A list of the first 10 Fibonacci numbers",
    agent=developer_agent
)

# Create and run the crew
crew = Crew(
    agents=[developer_agent],
    tasks=[coding_task],
    verbose=True
)

result = crew.kickoff()
print(result)
```

## Complete Example

Here is a complete example combining all concepts:

```python
"""
Complete Codemode quickstart example.
"""
from codemode import Codemode
from codemode.config import ClientConfig

def main():
    # Option 1: Configure explicitly
    config = ClientConfig(
        executor_url="http://localhost:8001",
        executor_api_key="your-secret-key"
    )
    codemode = Codemode.from_client_config(config)

    # Option 2: Use environment variables (preferred for production)
    # codemode = Codemode.from_env()

    # Execute a simple calculation
    result = codemode.execute("""
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(f"fib({i}) = {fibonacci(i)}")
""")

    if result.exit_code == 0:
        print("Execution successful!")
        print(result.stdout)
    else:
        print(f"Execution failed with code {result.exit_code}")
        print(result.stderr)

if __name__ == "__main__":
    main()
```

## Stopping the Executor

When finished, stop the executor sidecar:

```bash
docker stop codemode-executor
docker rm codemode-executor
```

## Next Steps

- Read [Core Concepts](concepts.md) to understand the architecture in depth.
- Explore [Hybrid Execution](../features/hybrid-execution.md) for advanced use cases.
- Set up [TLS Encryption](../features/tls-encryption.md) for production deployments.
- Review the [Configuration Guide](../configuration.md) for all available options.
