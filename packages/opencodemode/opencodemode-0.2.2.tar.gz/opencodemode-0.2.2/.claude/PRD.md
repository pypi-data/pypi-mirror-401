# Codemode: Secure Code Execution for Multi-Agent Systems

**Product Requirements Document (PRD)**

**Version**: 0.1.0
**Date**: 2025-01-15
**Status**: Draft
**Owner**: @mldlwizard

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Vision & Goals](#vision--goals)
3. [Target Audience](#target-audience)
4. [Architecture Overview](#architecture-overview)
5. [Component Design](#component-design)
6. [API Design](#api-design)
7. [Configuration Schema](#configuration-schema)
8. [Security Model](#security-model)
9. [Implementation Phases](#implementation-phases)
10. [Success Metrics](#success-metrics)
11. [Example Usage](#example-usage)
12. [Open Questions](#open-questions)

---

## Executive Summary

### Problem Statement

Developers building multi-agent AI systems (using CrewAI, Langchain, Langgraph) face a critical limitation: **agents cannot dynamically generate and execute code to orchestrate complex workflows**. Current solutions either:

1. **Lack code execution capabilities** - Agents are limited to predefined tools
2. **Execute code unsafely** - Direct `eval()`/`exec()` poses security risks
3. **Require complex infrastructure** - Setting up sandboxed execution is difficult
4. **Can't access existing tools** - Isolated execution environments lack tool access

### Solution

**Codemode** is an open-source Python library that provides **secure, isolated code execution** for multi-agent systems with an **RPC bridge pattern** that enables:

- ✅ **Isolated code execution** in a locked-down Docker container (no network, read-only FS)
- ✅ **Tool access via RPC** - Generated code can call tools that run in the main app (with network access)
- ✅ **Framework agnostic** - Start with CrewAI, expand to Langchain/Langgraph
- ✅ **Two deployment modes**:
  - **Library mode**: Use as a tool in your Python code
  - **MCP mode**: Connect via Model Context Protocol (for VSCode, etc.)
- ✅ **Simple setup** - Install with pip, configure with YAML, deploy with Docker Compose
- ✅ **Same codebase, two containers** - Main app + executor sidecar pattern

### Key Innovation: RPC Bridge Pattern

```
┌─────────────────────────────────────────────────────────────┐
│ POD (same deployment)                                        │
│                                                              │
│  ┌──────────────────┐              ┌──────────────────────┐ │
│  │ Main App         │◄────RPC─────►│ Executor             │ │
│  │ (HAS network)    │   (HTTP)     │ (NO network)         │ │
│  │                  │              │                      │ │
│  │ - Real tools     │              │ - Code execution    │ │
│  │ - Postgres ✅     │              │ - Tool proxies      │ │
│  │ - Redis ✅        │              │ - Read-only FS      │ │
│  │ - APIs ✅         │              │ - No capabilities   │ │
│  └────────┬─────────┘              └──────────────────────┘ │
│           │                                                  │
│           ▼                                                  │
│  [Database, APIs, External Services]                        │
└─────────────────────────────────────────────────────────────┘

Generated code calls: tools['postgres'].run(query="SELECT...")
                          ↓
                   Proxy sends RPC to main app
                          ↓
                   Main app executes REAL tool (with network)
                          ↓
                   Returns result to executor
                          ↓
                   Code continues with result ✅
```

**Result**: Code executes in isolation, but tools run with full access. Best of both worlds.

---

## Vision & Goals

### Vision

**Enable AI agents to dynamically orchestrate complex workflows by generating and safely executing code that coordinates tools, agents, and external systems.**

### Goals

#### Phase 1 (MVP - v0.1)
- ✅ Core library with RPC bridge architecture
- ✅ CrewAI integration (agents, tools, crews, flows)
- ✅ Docker-based secure executor
- ✅ Configuration via YAML + code
- ✅ Auto-discovery of CrewAI components
- ✅ Library mode (use as Python tool)
- ✅ MCP server mode (for VSCode integration)

#### Phase 2 (v0.2)
- ✅ Langchain integration
- ✅ Langgraph integration
- ✅ Enhanced monitoring/observability
- ✅ Rate limiting and resource controls
- ✅ Execution caching

#### Phase 3 (v0.3+)
- ✅ Multi-tenant support
- ✅ Kubernetes operator
- ✅ Hosted SaaS option
- ✅ Advanced security features (code signing, etc.)

### Non-Goals (Out of Scope for MVP)

- ❌ Session management (handled by calling agent)
- ❌ Built-in agent orchestration (use CrewAI/Langchain for this)
- ❌ Code generation (LLM generates code, we execute it)
- ❌ Cloud hosting (self-hosted only for MVP)
- ❌ Web UI (CLI + API only)

---

## Target Audience

### Primary Audience

1. **AI Application Developers** building multi-agent systems with CrewAI/Langchain
2. **DevOps/Platform Engineers** deploying AI agents in production
3. **AI Researchers** experimenting with agentic code generation

### User Personas

#### Persona 1: Sarah - AI App Developer
- **Background**: Building a CrewAI chatbot for customer support
- **Pain Point**: Agents can't dynamically query database + call APIs in one workflow
- **Needs**: Simple library to add codemode as a tool to her CrewAI agent
- **Success**: `pip install opencodemode[crewai]` + 10 lines of code

#### Persona 2: Mike - DevOps Engineer
- **Background**: Deploying AI agents on Kubernetes
- **Pain Point**: Code execution in production is risky (security, network access)
- **Needs**: Docker-based solution with strong isolation
- **Success**: Add sidecar container to existing deployment, minimal config

#### Persona 3: Alex - AI Researcher
- **Background**: Experimenting with LLMs generating code for tool orchestration
- **Pain Point**: Want to test in VSCode with MCP servers
- **Needs**: MCP server mode to connect local environment
- **Success**: `codemode mcp start` + connect from VSCode

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ USER'S MACHINE (for MCP mode)                                    │
│                                                                   │
│  ┌──────────────────┐                                            │
│  │ VSCode + MCP     │                                            │
│  │ OR               │                                            │
│  │ Python script    │                                            │
│  └────────┬─────────┘                                            │
└───────────┼───────────────────────────────────────────────────────┘
            │ (MCP protocol or Python import)
            ▼
┌─────────────────────────────────────────────────────────────────┐
│ DEPLOYMENT ENVIRONMENT (Kubernetes, Docker Compose, etc.)        │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ POD / Container Group                                      │  │
│  │                                                            │  │
│  │  ┌──────────────────────┐      ┌──────────────────────┐  │  │
│  │  │ Container 1:         │      │ Container 2:         │  │  │
│  │  │ Main App             │◄────►│ Executor (Sidecar)   │  │  │
│  │  │                      │ HTTP │                      │  │  │
│  │  │ - FastAPI/Flask      │      │ - FastAPI server     │  │  │
│  │  │ - CrewAI agents      │      │ - Python exec()      │  │  │
│  │  │ - Real tools:        │      │ - Tool proxies       │  │  │
│  │  │   * DatabaseTool ✅   │      │                      │  │  │
│  │  │   * APITool ✅        │      │ Security:            │  │  │
│  │  │   * EmailTool ✅      │      │ - No network ❌       │  │  │
│  │  │ - RPC handler        │      │ - Read-only FS ❌     │  │  │
│  │  │                      │      │ - User 65534 ❌       │  │  │
│  │  │ Network: ENABLED ✅   │      │ - No caps ❌          │  │  │
│  │  └──────────┬───────────┘      └──────────────────────┘  │  │
│  │             │                                             │  │
│  └─────────────┼─────────────────────────────────────────────┘  │
│                │                                                 │
│                ▼                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ External Services                                         │  │
│  │  - PostgreSQL                                             │  │
│  │  - Redis                                                  │  │
│  │  - External APIs                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Codemode Library** (`codemode` package)
   - Core orchestration logic
   - Registry for tools/agents/crews
   - Client for executor communication
   - MCP server implementation

2. **Executor Service** (Docker container)
   - Receives code execution requests
   - Runs code in isolated environment
   - Proxies tool calls back to main app
   - Returns results

3. **RPC Handler** (in main app)
   - Receives tool call requests from executor
   - Executes real tools (with network access)
   - Returns results to executor

4. **Configuration System**
   - YAML-based config
   - Auto-discovery of components
   - Environment variable support

---

## Component Design

### 1. Codemode Library (`codemode` package)

#### Package Structure

```
codemode/
├── __init__.py              # Main API exports
├── core/
│   ├── __init__.py
│   ├── registry.py          # ComponentRegistry class
│   ├── executor_client.py   # ExecutorClient (communicates with executor)
│   └── tool_proxy.py        # CodemodeToolProxy (CrewAI tool)
├── integrations/
│   ├── __init__.py
│   ├── crewai.py           # CrewAI integration
│   ├── langchain.py        # Langchain integration (future)
│   └── langgraph.py        # Langgraph integration (future)
├── mcp/
│   ├── __init__.py
│   └── server.py           # MCP server implementation
├── executor/
│   ├── __init__.py
│   ├── service.py          # FastAPI executor service
│   ├── runner.py           # Code execution logic
│   └── security.py         # Security validation
├── rpc/
│   ├── __init__.py
│   ├── handler.py          # RPC request handler
│   └── models.py           # RPC request/response models
├── config/
│   ├── __init__.py
│   ├── loader.py           # Config file loader
│   └── models.py           # Config models (Pydantic)
└── cli/
    ├── __init__.py
    └── main.py             # CLI commands
```

#### Installation

```bash
# Base installation
pip install opencodemode

# With CrewAI support
pip install opencodemode[crewai]

# With all integrations
pip install opencodemode[all]

# Development installation
pip install opencodemode[dev]
```

#### Core Classes

##### ComponentRegistry

```python
# codemode/core/registry.py

from typing import Dict, Any, Optional
from pydantic import BaseModel

class ComponentRegistry:
    """
    Central registry for tools, agents, crews, flows, etc.

    This is the bridge between user's components and the executor.
    """

    def __init__(self):
        self.tools: Dict[str, Any] = {}
        self.agents: Dict[str, Any] = {}
        self.crews: Dict[str, Any] = {}
        self.flows: Dict[str, Any] = {}
        self.config: Dict[str, Any] = {}

    def register_tool(self, name: str, tool: Any) -> None:
        """Register a tool (CrewAI tool, Langchain tool, etc.)"""
        self.tools[name] = tool

    def register_agent(self, name: str, agent: Any) -> None:
        """Register an agent"""
        self.agents[name] = agent

    def register_crew(self, name: str, crew: Any) -> None:
        """Register a crew"""
        self.crews[name] = crew

    def register_flow(self, name: str, flow: Any) -> None:
        """Register a flow"""
        self.flows[name] = flow

    def set_config(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value

    def get_component_names(self) -> Dict[str, list]:
        """Get all registered component names"""
        return {
            'tools': list(self.tools.keys()),
            'agents': list(self.agents.keys()),
            'crews': list(self.crews.keys()),
            'flows': list(self.flows.keys()),
        }
```

##### ExecutorClient

```python
# codemode/core/executor_client.py

import requests
from typing import Dict, Any, Optional
from pydantic import BaseModel

class ExecutionRequest(BaseModel):
    code: str
    available_tools: list
    config: Dict[str, Any]
    timeout: int = 30

class ExecutionResult(BaseModel):
    success: bool
    result: Optional[str] = None
    stdout: str = ""
    stderr: str = ""
    error: Optional[str] = None

class ExecutorClient:
    """
    Client for communicating with the executor service.
    """

    def __init__(
        self,
        executor_url: str,
        api_key: str,
        timeout: int = 35
    ):
        self.executor_url = executor_url
        self.api_key = api_key
        self.timeout = timeout

    def execute(
        self,
        code: str,
        available_tools: list,
        config: Dict[str, Any],
        execution_timeout: int = 30
    ) -> ExecutionResult:
        """
        Execute code in the executor service.

        Args:
            code: Python code to execute
            available_tools: List of tool names available
            config: Configuration dict
            execution_timeout: Timeout for code execution

        Returns:
            ExecutionResult with success status and output
        """

        request = ExecutionRequest(
            code=code,
            available_tools=available_tools,
            config=config,
            timeout=execution_timeout
        )

        try:
            response = requests.post(
                f'{self.executor_url}/execute',
                json=request.dict(),
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                timeout=self.timeout
            )

            response.raise_for_status()

            result_data = response.json()
            return ExecutionResult(**result_data)

        except requests.exceptions.RequestException as e:
            return ExecutionResult(
                success=False,
                error=f"Executor communication failed: {str(e)}"
            )
```

##### CodemodeToolProxy (CrewAI Integration)

```python
# codemode/integrations/crewai.py

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional
from codemode.core.registry import ComponentRegistry
from codemode.core.executor_client import ExecutorClient

class CodemodeInput(BaseModel):
    """Input schema for Codemode tool"""
    code: str = Field(
        ...,
        description="Python code to execute. Must define a 'result' variable."
    )

class CodemodeTool(BaseTool):
    """
    CrewAI tool that executes code in isolated executor.

    Usage:
        from codemode.integrations.crewai import CodemodeTool

        tool = CodemodeTool(
            registry=registry,
            executor_url="http://executor:8001",
            api_key="secret"
        )

        agent = Agent(
            role="Orchestrator",
            tools=[tool],
            ...
        )
    """

    name: str = "codemode"
    description: str = """
    Execute Python code to orchestrate tools, agents, and crews.

    Available in code:
    - tools['tool_name'].run(**kwargs) - Call registered tools
    - agents['agent_name'] - Access registered agents
    - crews['crew_name'] - Access registered crews
    - config['key'] - Access configuration

    MUST define 'result' variable with output.

    Example:
    ```python
    # Get weather data
    weather = tools['weather'].run(location='NYC')

    # Send via email
    tools['email'].run(to='team@co.com', body=weather)

    result = {'weather': weather, 'sent': True}
    ```
    """

    args_schema: type[BaseModel] = CodemodeInput

    registry: ComponentRegistry = Field(...)
    executor_client: ExecutorClient = Field(...)

    def _run(self, code: str) -> str:
        """Execute code via executor service"""

        # Get component names
        component_names = self.registry.get_component_names()

        # Execute code
        result = self.executor_client.execute(
            code=code,
            available_tools=component_names['tools'],
            config=dict(self.registry.config)
        )

        if result.success:
            return result.result or "Code executed successfully"
        else:
            return f"ERROR: {result.error}"
```

---

### 2. Executor Service

#### service.py (FastAPI app)

```python
# codemode/executor/service.py

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

from codemode.executor.runner import CodeRunner
from codemode.executor.security import SecurityValidator

logger = logging.getLogger(__name__)

app = FastAPI(title="Codemode Executor Service")

# Configuration
API_KEY = os.getenv('CODEMODE_API_KEY', 'change-me-in-production')
MAIN_APP_URL = os.getenv('MAIN_APP_URL', 'http://localhost:8000')

code_runner = CodeRunner(main_app_url=MAIN_APP_URL, api_key=API_KEY)
security_validator = SecurityValidator()

class ExecutionRequest(BaseModel):
    code: str
    available_tools: list[str] = []
    config: Dict[str, Any] = {}
    timeout: int = 30

class ExecutionResult(BaseModel):
    success: bool
    result: Optional[str] = None
    stdout: str = ""
    stderr: str = ""
    error: Optional[str] = None

@app.post("/execute", response_model=ExecutionResult)
async def execute_code(
    request: ExecutionRequest,
    authorization: str = Header(None)
):
    """Execute code in isolated environment"""

    # Validate API key
    if authorization != f'Bearer {API_KEY}':
        raise HTTPException(401, "Unauthorized")

    # Security validation
    validation_result = security_validator.validate(request.code)
    if not validation_result.is_safe:
        return ExecutionResult(
            success=False,
            error=f"Security violation: {validation_result.reason}"
        )

    # Execute code
    result = await code_runner.run(
        code=request.code,
        available_tools=request.available_tools,
        config=request.config,
        timeout=request.timeout
    )

    return result

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/ready")
async def ready():
    """Check if executor can reach main app"""
    try:
        response = requests.get(f'{MAIN_APP_URL}/health', timeout=2)
        if response.status_code == 200:
            return {"status": "ready"}
        raise HTTPException(503, "Main app not healthy")
    except:
        raise HTTPException(503, "Cannot reach main app")
```

---

### 3. RPC Handler (Main App)

```python
# codemode/rpc/handler.py

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class RPCRequest(BaseModel):
    type: str  # 'call_tool', 'list_tools'
    tool: Optional[str] = None
    arguments: Dict[str, Any] = {}

class RPCResponse(BaseModel):
    success: bool
    result: Any = None
    error: Optional[str] = None

class RPCHandler:
    """
    Handles RPC requests from executor.
    Executes REAL tools (with network access).
    """

    def __init__(self, registry):
        self.registry = registry
        self.call_count = 0

    async def handle_call_tool(self, request: RPCRequest) -> RPCResponse:
        """Execute real tool"""

        tool_name = request.tool
        arguments = request.arguments or {}

        if tool_name not in self.registry.tools:
            return RPCResponse(
                success=False,
                error=f"Tool '{tool_name}' not found"
            )

        real_tool = self.registry.tools[tool_name]

        logger.info(f"RPC: Executing tool {tool_name}")

        try:
            # Execute REAL tool (has network access!)
            result = real_tool.run(**arguments)

            return RPCResponse(success=True, result=result)

        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return RPCResponse(
                success=False,
                error=str(e)
            )

def create_rpc_router(registry) -> APIRouter:
    """Create RPC router for main app"""

    router = APIRouter()
    rpc_handler = RPCHandler(registry)

    API_KEY = os.getenv('CODEMODE_API_KEY', '')

    @router.post("/rpc", response_model=RPCResponse)
    async def handle_rpc(
        request: RPCRequest,
        authorization: str = Header(None),
        x_caller: str = Header(None)
    ):
        """RPC endpoint for executor"""

        # Validate caller
        if authorization != f'Bearer {API_KEY}':
            raise HTTPException(401, "Unauthorized")

        if x_caller != 'executor':
            raise HTTPException(403, "Only executor can call")

        # Handle request
        if request.type == 'call_tool':
            return await rpc_handler.handle_call_tool(request)
        else:
            return RPCResponse(
                success=False,
                error=f"Unknown RPC type: {request.type}"
            )

    return router
```

---

## API Design

### Library Mode (Python API)

#### Basic Usage

```python
# app.py - User's main application

from fastapi import FastAPI
from crewai import Agent, Task, Crew
from codemode import Codemode, ComponentRegistry
from codemode.rpc import create_rpc_router

# Import your tools
from my_tools import WeatherTool, DatabaseTool, EmailTool

app = FastAPI()

# 1. Create registry and register components
registry = ComponentRegistry()
registry.register_tool('weather', WeatherTool())
registry.register_tool('database', DatabaseTool())
registry.register_tool('email', EmailTool())

# 2. Add RPC endpoint for executor
rpc_router = create_rpc_router(registry)
app.include_router(rpc_router, prefix="/internal")

# 3. Create codemode client
codemode = Codemode(
    registry=registry,
    executor_url="http://executor:8001",
    api_key="your-secret-key"
)

# 4. Get the codemode tool
codemode_tool = codemode.as_crewai_tool()

# 5. Create orchestrator agent with ONLY codemode tool
orchestrator = Agent(
    role="Code Orchestrator",
    goal="Generate and execute code to coordinate tools",
    backstory="""You write Python code to orchestrate tools.

    Available tools:
    - tools['weather'].run(location='city')
    - tools['database'].run(query='SQL')
    - tools['email'].run(to='email', body='text')

    Always define 'result' variable.
    """,
    tools=[codemode_tool],
    verbose=True
)

# 6. Use in your endpoints
@app.post("/chat")
async def chat(message: str):
    task = Task(
        description=message,
        agent=orchestrator,
        expected_output="Task result"
    )

    crew = Crew(agents=[orchestrator], tasks=[task])
    result = crew.kickoff()

    return {"result": str(result)}
```

#### Configuration-Based Setup

```python
# app.py

from codemode import Codemode

# Load from config file
codemode = Codemode.from_config('codemode.yaml')

# Auto-discover CrewAI components
codemode.auto_discover_crewai()

# Get tool
tool = codemode.as_crewai_tool()
```

#### Advanced Usage

```python
# Custom error handling
result = codemode.execute("""
try:
    data = tools['database'].run(query='SELECT * FROM users')
    result = {'success': True, 'data': data}
except Exception as e:
    result = {'success': False, 'error': str(e)}
""")

# Direct execution (without CrewAI agent)
result = codemode.execute("""
weather = tools['weather'].run(location='NYC')
result = {'weather': weather}
""")
```

---

### MCP Mode (Model Context Protocol)

#### Starting MCP Server

```bash
# Start MCP server (runs locally)
codemode mcp start --config codemode.yaml --port 3000

# Server starts and listens for MCP connections
```

#### VSCode Configuration

```json
// .vscode/mcp.json
{
  "mcpServers": {
    "codemode": {
      "command": "codemode",
      "args": ["mcp", "start", "--config", "codemode.yaml"],
      "env": {
        "EXECUTOR_URL": "http://localhost:8001",
        "CODEMODE_API_KEY": "your-secret"
      }
    }
  }
}
```

#### MCP Tool Schema

```json
{
  "name": "codemode_execute",
  "description": "Execute Python code to orchestrate tools",
  "inputSchema": {
    "type": "object",
    "properties": {
      "code": {
        "type": "string",
        "description": "Python code to execute. Must define 'result' variable."
      }
    },
    "required": ["code"]
  }
}
```

---

## Configuration Schema

### codemode.yaml

```yaml
# Codemode Configuration File
# Full example with all options

project:
  name: my-crewai-app
  version: 1.0.0

# Framework integration
framework:
  type: crewai  # or 'langchain', 'langgraph'
  auto_discover: true  # Auto-discover agents, tools, crews

# Executor connection
executor:
  url: http://executor:8001
  api_key: ${CODEMODE_API_KEY}  # From environment variable
  timeout: 35  # seconds

  # Execution limits
  limits:
    code_timeout: 30  # seconds
    max_code_length: 10000  # characters
    memory_limit: 512Mi

# Component registration
components:
  # Tools (if not using auto-discover)
  tools:
    - name: weather
      module: my_tools.weather
      class: WeatherTool

    - name: database
      module: my_tools.database
      class: DatabaseTool
      config:
        connection_string: ${DATABASE_URL}

  # Agents
  agents:
    - name: researcher
      module: my_agents.researcher
      function: create_researcher_agent

  # Crews
  crews:
    - name: marketing_crew
      module: my_crews.marketing
      variable: marketing_crew

# Configuration passed to executed code
config:
  environment: production
  api_keys:
    weather_api: ${WEATHER_API_KEY}
  database:
    url: ${DATABASE_URL}

# Security settings
security:
  # Blocked imports in executed code
  blocked_imports:
    - subprocess
    - os.system
    - eval
    - exec

  # Allowed built-ins
  safe_builtins:
    - print
    - len
    - str
    - int
    - float
    - dict
    - list

# Logging
logging:
  level: INFO
  format: json
  output: stdout

# MCP server settings (for MCP mode)
mcp:
  enabled: true
  port: 3000
  tools:
    - codemode_execute
```

### Environment Variables

```bash
# .env file

# Required
CODEMODE_API_KEY=your-secret-key-here

# Executor connection
EXECUTOR_URL=http://executor:8001

# Tool configurations
DATABASE_URL=postgresql://user:pass@host:5432/db
WEATHER_API_KEY=your-weather-api-key
```

---

## Security Model

### Defense-in-Depth Layers

#### Layer 1: Container Isolation

```yaml
# docker-compose.yml - Executor container
services:
  executor:
    security_opt:
      - no-new-privileges
    read_only: true
    cap_drop:
      - ALL
    user: "65534:65534"  # nobody
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=64m
    networks:
      - internal  # No external network access
```

**Prevents**:
- Network access to external services
- File system writes (except tmpfs)
- Privilege escalation
- Container escape

#### Layer 2: Code Validation

```python
# codemode/executor/security.py

class SecurityValidator:
    """Validates code before execution"""

    BLOCKED_PATTERNS = [
        '__import__',
        'eval(',
        'exec(',
        'compile(',
        'open(',
        'subprocess',
        'os.system',
        'socket.',
        'urllib.',
        'requests.',
    ]

    def validate(self, code: str) -> ValidationResult:
        """Check for dangerous patterns"""

        for pattern in self.BLOCKED_PATTERNS:
            if pattern in code:
                return ValidationResult(
                    is_safe=False,
                    reason=f"Blocked pattern: {pattern}"
                )

        # Check code length
        if len(code) > 10000:
            return ValidationResult(
                is_safe=False,
                reason="Code exceeds max length"
            )

        return ValidationResult(is_safe=True)
```

**Prevents**:
- Import of dangerous modules
- Direct system calls
- Network operations
- File operations

#### Layer 3: RPC Mediation

```python
# All tool calls go through RPC handler
# Main app can:
# - Log all tool calls
# - Rate limit
# - Validate arguments
# - Apply access control
```

**Prevents**:
- Unauthorized tool access
- Excessive resource usage
- Data exfiltration

#### Layer 4: Resource Limits

```python
# Resource limits applied
resource.setrlimit(resource.RLIMIT_AS, (256*1024*1024, 256*1024*1024))  # 256MB
resource.setrlimit(resource.RLIMIT_CPU, (30, 30))  # 30 seconds CPU
resource.setrlimit(resource.RLIMIT_NPROC, (1, 1))  # No fork
```

**Prevents**:
- Memory exhaustion
- CPU hogging
- Fork bombs

### Security Rating: 9/10

**Why 9/10?**
- ✅ Strong container isolation
- ✅ No network access
- ✅ Read-only filesystem
- ✅ Code validation
- ✅ RPC mediation
- ✅ Resource limits

**Why not 10/10?**
- Container runtime vulnerabilities (Docker/K8s)
- Potential Python interpreter exploits
- API key compromise risk

**Good enough for production!** ✅

---

## Implementation Phases

### Phase 1: MVP (Weeks 1-4)

**Goal**: Working library mode with CrewAI integration

**Deliverables**:
- [ ] Core library structure
- [ ] ComponentRegistry implementation
- [ ] ExecutorClient implementation
- [ ] CodemodeTool (CrewAI integration)
- [ ] Executor service (FastAPI)
- [ ] RPC handler
- [ ] Security validation
- [ ] Docker Compose setup
- [ ] Basic documentation
- [ ] Example project

**Success Criteria**:
- User can `pip install opencodemode[crewai]`
- User can add codemode tool to CrewAI agent
- Code executes in isolated container
- Tools accessible via RPC
- Example project runs end-to-end

### Phase 2: MCP + Polish (Weeks 5-6)

**Goal**: MCP server mode + production readiness

**Deliverables**:
- [ ] MCP server implementation
- [ ] CLI commands (`codemode mcp start`)
- [ ] Configuration loader
- [ ] Auto-discovery for CrewAI components
- [ ] Monitoring/metrics endpoints
- [ ] Rate limiting
- [ ] Comprehensive tests
- [ ] Documentation site
- [ ] Kubernetes manifests

**Success Criteria**:
- User can connect from VSCode via MCP
- Auto-discovery finds components
- K8s deployment works
- Tests cover 80%+ of code

### Phase 3: Multi-Framework (Weeks 7-10)

**Goal**: Langchain + Langgraph support

**Deliverables**:
- [ ] Langchain integration
- [ ] Langgraph integration
- [ ] Framework-agnostic base classes
- [ ] Adapter pattern for frameworks
- [ ] Migration guides
- [ ] Advanced examples

### Phase 4: Production Features (Weeks 11-12)

**Goal**: Enterprise readiness

**Deliverables**:
- [ ] Execution caching
- [ ] Advanced monitoring
- [ ] Audit logging
- [ ] Multi-tenancy support
- [ ] Kubernetes operator
- [ ] Helm charts
- [ ] Security audit

---

## Success Metrics

### Adoption Metrics
- **Week 1**: 10 GitHub stars
- **Month 1**: 100 GitHub stars, 50 installs
- **Month 3**: 500 GitHub stars, 500 installs

### Technical Metrics
- **Reliability**: 99.9% uptime
- **Performance**: <100ms RPC latency
- **Security**: Zero security incidents

### User Success Metrics
- **Time to first success**: <15 minutes
- **Setup complexity**: <10 lines of code
- **Documentation clarity**: >4.5/5 rating

---

## Example Usage

### Example 1: Weather + Email Workflow

```python
# User's agent generates this code:

weather = tools['weather'].run(location='San Francisco')

tools['email'].run(
    to='team@company.com',
    subject='SF Weather Update',
    body=f'Current weather: {weather}'
)

result = {
    'weather': weather,
    'email_sent': True
}
```

**What happens**:
1. Code executes in executor (no network)
2. `tools['weather'].run()` → Proxy sends RPC to main app
3. Main app executes real WeatherTool (has API access)
4. Returns weather data to executor
5. `tools['email'].run()` → Proxy sends RPC to main app
6. Main app executes real EmailTool (has SMTP access)
7. Returns success to executor
8. Result returned to agent

### Example 2: Multi-Agent Pipeline

```python
# Query database
users = tools['database'].run(query='SELECT * FROM users LIMIT 10')

# Have researcher agent analyze
analysis = agents['researcher'].execute_task(
    task='Analyze user patterns',
    context={'users': users}
)

# Have writer create report
report = agents['writer'].execute_task(
    task='Create report',
    context={'analysis': str(analysis)}
)

# Email report
tools['email'].run(
    to='management@company.com',
    subject='User Analysis Report',
    body=str(report)
)

result = {
    'users_analyzed': len(users),
    'report': str(report)
}
```

### Example 3: Conditional Logic

```python
# Check for high-priority tasks
tasks = tools['database'].run(
    query="SELECT * FROM tasks WHERE priority='high'"
)

if tasks and len(tasks) > 0:
    # Alert team
    tools['email'].run(
        to='team@company.com',
        subject='HIGH PRIORITY TASKS',
        body=f'Found {len(tasks)} high-priority tasks'
    )
    result = {'alert_sent': True, 'count': len(tasks)}
else:
    # Just log
    print('No high-priority tasks')
    result = {'alert_sent': False, 'count': 0}
```

---

## Open Questions

### Technical Decisions Needed

1. **Python Version Support**
   - Minimum Python 3.9+?
   - Support 3.8?

2. **RPC Protocol**
   - HTTP/REST (current plan) ✅
   - gRPC (better performance)?
   - WebSocket (for streaming)?

3. **Code Wrapping Strategy**
   - Inject tool proxies via string template (current) ✅
   - Use AST manipulation?
   - Custom import hooks?

4. **Error Handling**
   - Return error string (current) ✅
   - Raise exceptions?
   - Structured error objects?

5. **Monitoring/Observability**
   - Prometheus metrics?
   - OpenTelemetry?
   - Custom logging?

### Product Decisions Needed

1. **Naming**
   - `codemode` (current) ✅
   - `codemode-ai`?
   - `agent-codemode`?

2. **License**
   - MIT ✅
   - Apache 2.0?
   - GPL?

3. **Distribution**
   - PyPI only ✅
   - Conda?
   - Docker Hub images?

4. **Documentation Platform**
   - GitHub Pages?
   - ReadTheDocs?
   - Docusaurus?

5. **Community**
   - Discord server?
   - GitHub Discussions ✅
   - Slack?

---

## Next Steps

1. **Review & Feedback** (You!)
   - Review this PRD
   - Provide feedback on architecture
   - Clarify any open questions
   - Approve to proceed

2. **Project Setup**
   - Initialize Git repository
   - Set up project structure
   - Create pyproject.toml
   - Set up CI/CD

3. **Core Implementation**
   - Implement ComponentRegistry
   - Implement ExecutorClient
   - Implement basic executor service
   - Implement RPC handler

4. **Testing**
   - Write unit tests
   - Create integration tests
   - Set up test fixtures

5. **Documentation**
   - Write README
   - Create quickstart guide
   - Write API docs
   - Create examples

---

## Appendix A: Comparison to Alternatives

| Feature | Codemode | MCP Fresh Containers | Jupyter Kernels | AWS Lambda |
|---------|----------|---------------------|-----------------|------------|
| Security | 9/10 | 9/10 | 6/10 | 8/10 |
| Speed | Fast (<100ms) | Slow (>5s) | Medium | Medium |
| Tool Access | ✅ RPC bridge | ✅ MCP servers | ❌ Limited | ❌ Limited |
| Setup | Easy | Medium | Easy | Hard |
| Cost | $0 extra | VM costs | $0 extra | Per-execution |
| Framework Support | CrewAI/Langchain | Any | Any | Any |
| Self-hosted | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |

**Codemode's Advantage**: Same security as MCP, but faster and self-contained.

---

## Appendix B: Glossary

- **RPC**: Remote Procedure Call - Method for one system to call functions in another
- **MCP**: Model Context Protocol - Standard for connecting AI tools
- **Sidecar**: Container pattern where helper container runs alongside main container
- **Tool Proxy**: Object that looks like a tool but sends RPC requests
- **Executor**: Container that runs user-generated code in isolation
- **Registry**: Central catalog of available tools, agents, crews
- **Stateless**: Each execution is independent, no memory of previous executions

---

**End of PRD**

---

## Feedback & Approvals

- [ ] Architecture approved
- [ ] Security model approved
- [ ] API design approved
- [ ] Implementation plan approved
- [ ] Ready to proceed

**Reviewer**: @mldlwizard
**Date**: 2025-01-15
