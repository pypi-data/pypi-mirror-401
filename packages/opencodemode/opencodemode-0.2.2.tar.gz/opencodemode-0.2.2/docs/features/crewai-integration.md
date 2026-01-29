# CrewAI Integration

## Overview

Codemode integrates seamlessly with CrewAI, providing a **codemode tool** that enables agents to dynamically generate and execute code to orchestrate other tools, agents, and crews.

## Quick Start

### Installation

```bash
# Install codemode with CrewAI support
uv add opencodemode[crewai]
# or
pip install opencodemode[crewai]
```

### Basic Usage

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI
from crewai import Agent, Task, Crew
from codemode import Codemode
from codemode.grpc import start_tool_service_async

# Your existing tools
from my_tools import WeatherTool, DatabaseTool

# Application state
codemode = None
orchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage ToolService lifecycle."""
    global codemode, orchestrator

    # Startup
    # 1. Create codemode from config
    codemode = Codemode.from_config('codemode.yaml')

    # 2. Register your tools
    codemode.registry.register_tool('weather', WeatherTool())
    codemode.registry.register_tool('database', DatabaseTool())

    # 3. Start gRPC ToolService for executor calls - properly waits for server to be ready
    server = await start_tool_service_async(codemode.registry, host="0.0.0.0", port=50051)

    # 4. Get codemode as a CrewAI tool
    codemode_tool = codemode.as_crewai_tool()

    # 5. Create orchestrator agent with codemode tool
    orchestrator = Agent(
        role="Code Orchestrator",
        goal="Generate and execute code to coordinate tools",
        backstory=f"""You write Python code to orchestrate tools.

        Available tools: {list(codemode.registry.tools.keys())}

        Example:
        ```python
        weather = tools['weather'].run(location='NYC')
        result = {{'weather': weather}}
        ```
        """,
        tools=[codemode_tool],
        verbose=True
    )

    yield

    # Shutdown: clean stop
    await server.stop(0)


# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)


# 6. Use in your application
@app.post("/chat")
async def chat(message: str):
    task = Task(
        description=message,
        agent=orchestrator,
        expected_output="Task completed"
    )

    crew = Crew(agents=[orchestrator], tasks=[task])
    result = crew.kickoff()

    return {"result": str(result)}
```

## Auto-Discovery

Codemode can automatically discover and register CrewAI components from your project.

### Project Structure

```
my-project/
├── agents/
│   ├── __init__.py
│   ├── researcher.py
│   └── writer.py
├── tools/
│   ├── __init__.py
│   ├── weather.py
│   └── database.py
├── crews/
│   ├── __init__.py
│   └── marketing.py
└── app.py
```

### Enable Auto-Discovery

```python
# app.py
from codemode import Codemode

codemode = Codemode.from_config('codemode.yaml')

# Auto-discover all CrewAI components
codemode.auto_discover_crewai(
    tools_module='tools',
    agents_module='agents',
    crews_module='crews'
)

print(f"Discovered tools: {list(codemode.registry.tools.keys())}")
print(f"Discovered agents: {list(codemode.registry.agents.keys())}")
print(f"Discovered crews: {list(codemode.registry.crews.keys())}")
```

### Configuration

```yaml
# codemode.yaml
framework:
  type: crewai
  auto_discover: true

  discovery:
    tools_module: tools
    agents_module: agents
    crews_module: crews
```

## Using Registered Components

Once registered, components are available in generated code:

### Tools

```python
# Generated code can call tools
weather = tools['weather'].run(location='NYC')
```

### Agents

```python
# Generated code can use agents
analysis = agents['researcher'].execute_task(
    task="Analyze this data",
    context={'data': weather}
)
```

### Crews

```python
# Generated code can kickoff crews
result = crews['marketing'].kickoff(inputs={
    'campaign_type': 'social_media',
    'data': analysis
})
```

## Advanced Patterns

### Multi-Agent Workflow

```python
# LLM generates this code:
# Step 1: Research
research = agents['researcher'].execute_task(
    task="Research market trends",
    context={}
)

# Step 2: Write content based on research
content = agents['writer'].execute_task(
    task="Write blog post",
    context={'research': str(research)}
)

# Step 3: Send via email
tools['email'].run(
    to='team@company.com',
    subject='New Blog Post',
    body=str(content)
)

result = {
    'research': str(research),
    'content': str(content),
    'sent': True
}
```

### Conditional Agent Selection

```python
# Select agent based on task type
task_type = config.get('task_type', 'general')

if task_type == 'technical':
    result = agents['technical_expert'].execute_task(
        task=config.get('task')
    )
elif task_type == 'creative':
    result = agents['creative_writer'].execute_task(
        task=config.get('task')
    )
else:
    result = agents['generalist'].execute_task(
        task=config.get('task')
    )
```

### Crew Orchestration

```python
# Run different crews based on priority
priority = config.get('priority', 'normal')

if priority == 'high':
    crew_result = crews['rapid_response'].kickoff(inputs={
        'urgency': 'high',
        'task': config.get('task')
    })
else:
    crew_result = crews['standard'].kickoff(inputs={
        'task': config.get('task')
    })

result = {'crew_output': str(crew_result)}
```

## Integration Patterns

### Pattern 1: Codemode as Primary Tool

Orchestrator agent has **only** the codemode tool:

```python
orchestrator = Agent(
    role="Orchestrator",
    tools=[codemode_tool],  # Only codemode
    backstory="You coordinate other agents via code"
)
```

**Use case**: Dynamic workflow generation

### Pattern 2: Codemode as Secondary Tool

Agent has codemode + other tools:

```python
agent = Agent(
    role="Hybrid Agent",
    tools=[
        WeatherTool(),
        DatabaseTool(),
        codemode_tool  # Also has codemode
    ],
    backstory="You can use tools directly or via code"
)
```

**Use case**: Complex tasks that need both direct tool access and orchestration

### Pattern 3: Multi-Agent with Codemode

Multiple agents, one with codemode:

```python
orchestrator = Agent(
    role="Orchestrator",
    tools=[codemode_tool]
)

researcher = Agent(
    role="Researcher",
    tools=[SearchTool(), DatabaseTool()]
)

writer = Agent(
    role="Writer",
    tools=[WritingTool()]
)

crew = Crew(
    agents=[orchestrator, researcher, writer],
    tasks=[...],
    process=Process.sequential
)
```

**Use case**: Orchestrator coordinates researchers and writers

## Custom Tool Registration

### Manual Registration

```python
from crewai.tools import tool

@tool("Custom Calculator")
def calculate(expression: str) -> float:
    """Evaluate a mathematical expression"""
    return eval(expression)

# Register with codemode
codemode.registry.register_tool('calculator', calculate)
```

### Class-Based Tool

```python
from crewai.tools import BaseTool

class MyCustomTool(BaseTool):
    name: str = "my_custom_tool"
    description: str = "Does something custom"

    def _run(self, input: str) -> str:
        return f"Processed: {input}"

# Register
codemode.registry.register_tool('custom', MyCustomTool())
```

## Error Handling

### In Generated Code

```python
# LLM should generate code with error handling
try:
    weather = tools['weather'].run(location='NYC')
    result = {'success': True, 'weather': weather}
except Exception as e:
    result = {'success': False, 'error': str(e)}
```

### In Application

```python
@app.post("/chat")
async def chat(message: str):
    try:
        task = Task(description=message, agent=orchestrator)
        crew = Crew(agents=[orchestrator], tasks=[task])
        result = crew.kickoff()
        return {"success": True, "result": str(result)}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Best Practices

### 1. Tool Naming

Use clear, descriptive names:

```python
# Good
codemode.registry.register_tool('weather_api', WeatherTool())
codemode.registry.register_tool('postgres_db', DatabaseTool())

# Avoid
codemode.registry.register_tool('tool1', WeatherTool())
codemode.registry.register_tool('t2', DatabaseTool())
```

### 2. Agent Backstory

Provide clear instructions in agent backstory:

```python
orchestrator = Agent(
    backstory=f"""You write Python code to use tools.

    Available tools:
    - tools['weather'].run(location='city') - Get weather
    - tools['database'].run(query='SQL') - Query database

    Example:
    ```python
    weather = tools['weather'].run(location='NYC')
    result = {{'weather': weather}}
    ```

    IMPORTANT: Always define 'result' variable.
    """,
    ...
)
```

### 3. Context Passing

Pass context efficiently:

```python
# In your app
codemode.registry.set_config('user_id', user_id)
codemode.registry.set_config('session_id', session_id)

# In generated code
user_id = config.get('user_id')
```

### 4. Testing

Test with mock tools:

```python
# test_crewai_integration.py
import pytest
from codemode import Codemode

@pytest.fixture
def codemode_with_mocks():
    cm = Codemode.from_config('test_config.yaml')

    class MockWeatherTool:
        def run(self, location):
            return f"Weather in {location}: 72°F"

    cm.registry.register_tool('weather', MockWeatherTool())
    return cm

def test_orchestrator(codemode_with_mocks):
    tool = codemode_with_mocks.as_crewai_tool()
    # Test with tool
```

## Configuration

### codemode.yaml

```yaml
project:
  name: my-crewai-app

framework:
  type: crewai
  auto_discover: true

  discovery:
    tools_module: tools
    agents_module: agents
    crews_module: crews

    # Optional: Filters
    exclude_patterns:
      - "*_test.py"
      - "*_deprecated.py"

executor:
  url: http://executor:8001
  api_key: ${CODEMODE_API_KEY}

config:
  # Passed to generated code
  environment: production
  features:
    - analytics
    - notifications
```

## Troubleshooting

### Issue: "Tool not found"

**Cause**: Tool not registered

**Solution**:
```python
# Check registered tools
print(codemode.registry.tools.keys())

# Register missing tool
codemode.registry.register_tool('missing_tool', MyTool())
```

### Issue: "Agent not found"

**Cause**: Agent not registered or auto-discovery failed

**Solution**:
```python
# Manual registration
from agents.researcher import create_researcher_agent
codemode.registry.register_agent('researcher', create_researcher_agent())
```

### Issue: "execute_task() missing argument"

**Cause**: Agent expects different method signature

**Solution**:
```python
# Check your agent's interface
# Codemode expects: agent.execute_task(task, context)
# If different, wrap it:

class AgentWrapper:
    def __init__(self, agent):
        self.agent = agent

    def execute_task(self, task, context):
        return self.agent.run(task, **context)

codemode.registry.register_agent('my_agent', AgentWrapper(my_agent))
```

## Examples

### Example 1: Simple Tool Chain

```python
# User: "Get weather for NYC and save to database"

# LLM generates:
weather = tools['weather'].run(location='NYC')
tools['database'].run(
    query=f"INSERT INTO weather (city, data) VALUES ('NYC', '{weather}')"
)
result = {'weather': weather, 'saved': True}
```

### Example 2: Agent Pipeline

```python
# User: "Research AI trends and write a blog post"

# LLM generates:
research = agents['researcher'].execute_task(
    task="Research latest AI trends",
    context={}
)

blog_post = agents['writer'].execute_task(
    task="Write blog post about AI trends",
    context={'research': str(research)}
)

result = {'blog_post': str(blog_post)}
```

### Example 3: Crew Execution

```python
# User: "Run marketing campaign"

# LLM generates:
campaign_result = crews['marketing'].kickoff(inputs={
    'campaign_type': 'product_launch',
    'target_audience': 'developers',
    'budget': 10000
})

result = {'campaign': str(campaign_result)}
```

## Performance Tips

1. **Reuse agents**: Register agents once, use many times
2. **Cache results**: Use config to pass cached data
3. **Limit iterations**: Set max_iter on agents
4. **Monitor execution time**: Track tool call duration

## Customizing CodemodeTool

### Custom Description

You can customize the tool description to better guide your LLM agent. The default description includes essential patterns for meta-tools, async execution, rules, and error handling:

```python
from codemode import Codemode

codemode = Codemode.from_config('codemode.yaml')

# Use a custom description to add your specific tool signatures
custom_desc = """Execute Python code to orchestrate tools in a secure sandbox.

<META_TOOLS>
tools['__list__'].run() - List all available tools with descriptions
tools['__schema__'].run(name='tool_name') - Get input/output schema for a tool
</META_TOOLS>

<YOUR_TOOLS>
1. weather
   Signature: await tools['weather'].run(location: str) -> dict
   Returns weather data for the given location

2. database
   Signature: await tools['database'].run(query: str) -> dict
   Execute SQL query and return results
</YOUR_TOOLS>

<EXECUTION_PATTERN>
Code MUST use async pattern with result variable:

```python
import asyncio

async def main():
    weather = await tools['weather'].run(location='NYC')
    return {'weather': weather}

result = asyncio.run(main())
```
</EXECUTION_PATTERN>

<RULES>
- MUST set 'result' variable - this is extracted as output
- ALL tools are async: await tools['name'].run(**kwargs)
- Runtime context (client_id, user_id) auto-injected - never hardcode
- Only stdlib imports allowed (asyncio, json, datetime, re, math)
</RULES>
"""

tool = codemode.as_crewai_tool(description=custom_desc)
```

### Async Execution

Both `_run()` and `_arun()` are async methods. CrewAI handles async tools properly:

```python
# The tool works in both sync and async contexts
# CrewAI automatically awaits the result

# In an async context (FastAPI, etc.)
async def handle_request():
    crew = Crew(agents=[orchestrator], tasks=[task])
    result = await crew.kickoff_async()  # async execution
    return result

# In a sync context
def handle_request_sync():
    crew = Crew(agents=[orchestrator], tasks=[task])
    result = crew.kickoff()  # CrewAI handles awaiting
    return result
```

### Error Information

When code execution fails, the tool returns comprehensive error information including:

- **Error message**: The main error
- **Error type**: Classification (TypeError, ValueError, SecurityViolation, etc.)
- **Traceback**: Limited stack trace for debugging
- **Stderr**: Additional error output
- **Correlation ID**: For tracing in logs
- **Duration**: Execution time in milliseconds

Example error response:
```
ERROR: NameError: name 'undefined_var' is not defined
Type: NameError
Traceback:
  File '<string>', line 5
    result = undefined_var
Correlation ID: cm-abc123
Duration: 15.5ms
```

This helps agents understand failures and retry with corrected code.

## Related Features

- [Tool Registry](./tool-registry.md) - Managing tools
- [RPC Bridge](./rpc-bridge.md) - How tools are called
- [Configuration](./configuration.md) - Configuration options
