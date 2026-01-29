# Example Project Structure

This shows how a user would structure their project using Codemode.

## Minimal Setup (5 minutes)

```
my-crewai-app/
├── app.py                  # Main application
├── codemode.yaml          # Codemode configuration
├── docker-compose.yml     # Docker setup
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

### 1. app.py

```python
"""
Minimal CrewAI app with Codemode
"""

from fastapi import FastAPI
from crewai import Agent, Task, Crew
from codemode import Codemode
from codemode.rpc import create_rpc_router

# Import your existing tools
from my_tools import WeatherTool, DatabaseTool

app = FastAPI()

# Setup codemode from config
codemode = Codemode.from_config('codemode.yaml')

# Add RPC endpoint (executor will call this)
rpc_router = create_rpc_router(codemode.registry)
app.include_router(rpc_router, prefix="/internal")

# Register your components
codemode.registry.register_tool('weather', WeatherTool())
codemode.registry.register_tool('database', DatabaseTool())

# Get codemode as a CrewAI tool
codemode_tool = codemode.as_crewai_tool()

# Create orchestrator agent
orchestrator = Agent(
    role="Code Orchestrator",
    goal="Generate and execute code to coordinate tools",
    backstory=f"""You write Python code to use tools.

    Available tools: {list(codemode.registry.tools.keys())}

    Example:
    ```python
    weather = tools['weather'].run(location='NYC')
    result = {{'weather': weather}}
    ```

    Always define 'result' variable.
    """,
    tools=[codemode_tool],
    verbose=True
)

# Your endpoints
@app.post("/chat")
async def chat(message: str):
    """Chat endpoint using orchestrator"""

    task = Task(
        description=message,
        agent=orchestrator,
        expected_output="Task completed"
    )

    crew = Crew(agents=[orchestrator], tasks=[task])
    result = crew.kickoff()

    return {"result": str(result)}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2. codemode.yaml

```yaml
# Codemode configuration

project:
  name: my-crewai-app

framework:
  type: crewai
  auto_discover: false  # Manual registration in code

executor:
  url: http://executor:8001
  api_key: ${CODEMODE_API_KEY}
  timeout: 35

  limits:
    code_timeout: 30
    memory_limit: 512Mi

config:
  environment: production

logging:
  level: INFO
```

### 3. docker-compose.yml

```yaml
version: '3.8'

services:
  # Main application
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - CODEMODE_API_KEY=dev-secret-key
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - executor
      - db
    networks:
      - app-network

  # Executor (isolated, no external network)
  executor:
    image: codemode/executor:latest  # We'll provide this
    environment:
      - CODEMODE_API_KEY=dev-secret-key
      - MAIN_APP_URL=http://app:8000
    # Security settings
    read_only: true
    security_opt:
      - no-new-privileges
    cap_drop:
      - ALL
    user: "65534:65534"
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=64m
    networks:
      - app-network  # Internal network only

  # Database
  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=pass
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### 4. requirements.txt

```
fastapi==0.104.1
uvicorn==0.24.0
crewai==0.1.0
codemode[crewai]==0.1.0  # Our library
pydantic==2.5.0
requests==2.31.0
```

### 5. .env

```bash
CODEMODE_API_KEY=dev-secret-key-change-in-production
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
```

---

## Run It

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start services
docker-compose up

# 3. Test it
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Get weather for NYC and save to database"}'

# Response:
# {
#   "result": "Successfully retrieved weather (72°F, Sunny) and saved to database"
# }
```

---

## What Happens Behind the Scenes

```
1. POST /chat "Get weather for NYC and save to database"
   ↓
2. Orchestrator agent thinks: "I'll use codemode tool"
   ↓
3. LLM generates code:

   weather = tools['weather'].run(location='NYC')
   tools['database'].run(query=f"INSERT INTO weather VALUES ('{weather}')")
   result = {'weather': weather, 'saved': True}

   ↓
4. Codemode tool sends to executor container
   ↓
5. Executor runs code (no network access!)
   ↓
6. Code calls tools['weather'].run()
   ↓
7. Proxy sends RPC to main app: "call tool 'weather' with location='NYC'"
   ↓
8. Main app executes REAL WeatherTool (has network, calls weather API)
   ↓
9. Returns weather data to executor
   ↓
10. Code continues, calls tools['database'].run()
    ↓
11. Proxy sends RPC to main app: "call tool 'database' with query='...'"
    ↓
12. Main app executes REAL DatabaseTool (has network, connects to postgres)
    ↓
13. Returns success to executor
    ↓
14. Executor returns final result to codemode tool
    ↓
15. Agent responds to user: "Successfully retrieved weather and saved to database"
```

**Key Point**: Code executes in locked-down executor, but tools run in main app with full access! 🎉

---

## Advanced Setup (Auto-Discovery)

### Project Structure

```
my-crewai-app/
├── app.py              # Main application
├── codemode.yaml       # Configuration
├── docker-compose.yml
├── agents/
│   ├── __init__.py
│   ├── researcher.py   # Agent definitions
│   └── writer.py
├── tools/
│   ├── __init__.py
│   ├── weather.py      # Tool definitions
│   ├── database.py
│   └── email.py
├── crews/
│   ├── __init__.py
│   └── marketing.py    # Crew definitions
└── requirements.txt
```

### app.py (with auto-discovery)

```python
from fastapi import FastAPI
from codemode import Codemode
from codemode.rpc import create_rpc_router

app = FastAPI()

# Auto-discover all CrewAI components
codemode = Codemode.from_config('codemode.yaml')
codemode.auto_discover_crewai(
    tools_module='tools',
    agents_module='agents',
    crews_module='crews'
)

# Add RPC endpoint
rpc_router = create_rpc_router(codemode.registry)
app.include_router(rpc_router, prefix="/internal")

# Get tool
codemode_tool = codemode.as_crewai_tool()

# Create orchestrator
from crewai import Agent
orchestrator = Agent(
    role="Orchestrator",
    tools=[codemode_tool],
    backstory=f"""Available components:

    Tools: {list(codemode.registry.tools.keys())}
    Agents: {list(codemode.registry.agents.keys())}
    Crews: {list(codemode.registry.crews.keys())}
    """,
    verbose=True
)

# ... rest of app
```

### codemode.yaml (with auto-discovery)

```yaml
project:
  name: my-crewai-app

framework:
  type: crewai
  auto_discover: true

  # Where to find components
  discovery:
    tools_module: tools
    agents_module: agents
    crews_module: crews

executor:
  url: http://executor:8001
  api_key: ${CODEMODE_API_KEY}

# ... rest of config
```

---

## Kubernetes Deployment

### Project Structure

```
my-crewai-app/
├── app.py
├── codemode.yaml
├── requirements.txt
├── Dockerfile
└── k8s/
    ├── deployment.yaml
    ├── service.yaml
    └── configmap.yaml
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Default command (main app)
CMD ["python", "app.py"]
```

### k8s/deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crewai-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: crewai-app
  template:
    metadata:
      labels:
        app: crewai-app
    spec:
      containers:

      # Container 1: Main App
      - name: app
        image: myregistry/my-crewai-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: CODEMODE_API_KEY
          valueFrom:
            secretKeyRef:
              name: codemode-secret
              key: api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"

      # Container 2: Executor (Sidecar)
      - name: executor
        image: codemode/executor:latest
        ports:
        - containerPort: 8001
        env:
        - name: CODEMODE_API_KEY
          valueFrom:
            secretKeyRef:
              name: codemode-secret
              key: api-key
        - name: MAIN_APP_URL
          value: "http://localhost:8000"

        # SECURITY: Lock down executor
        securityContext:
          runAsUser: 65534
          runAsNonRoot: true
          readOnlyRootFilesystem: true
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL

        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

        volumeMounts:
        - name: tmp
          mountPath: /tmp

      volumes:
      - name: tmp
        emptyDir:
          sizeLimit: 64Mi
```

### k8s/service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: crewai-app
spec:
  selector:
    app: crewai-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

---

## MCP Mode Setup

### Project Structure

```
my-local-project/
├── codemode.yaml
├── .env
└── .vscode/
    └── mcp.json
```

### codemode.yaml (for MCP)

```yaml
project:
  name: local-codemode

framework:
  type: crewai
  auto_discover: true

# Connect to remote executor (or local Docker)
executor:
  url: http://localhost:8001  # Or remote URL
  api_key: ${CODEMODE_API_KEY}

mcp:
  enabled: true
  port: 3000
```

### .vscode/mcp.json

```json
{
  "mcpServers": {
    "codemode": {
      "command": "codemode",
      "args": ["mcp", "start", "--config", "codemode.yaml"],
      "env": {
        "CODEMODE_API_KEY": "your-secret"
      }
    }
  }
}
```

### Usage

```bash
# Start MCP server
codemode mcp start --config codemode.yaml

# Server listens on port 3000
# VSCode connects automatically
```

In VSCode, you can now:
- Ask Claude to "Execute code to get weather"
- Claude calls codemode MCP tool
- Code executes in secure executor
- Results returned to VSCode

---

## Testing Setup

### Project Structure

```
my-crewai-app/
├── app.py
├── tests/
│   ├── __init__.py
│   ├── test_codemode.py
│   ├── test_integration.py
│   └── fixtures/
│       └── test_tools.py
└── pytest.ini
```

### tests/test_codemode.py

```python
import pytest
from codemode import Codemode, ComponentRegistry
from codemode.rpc import RPCHandler

@pytest.fixture
def registry():
    """Create test registry"""
    reg = ComponentRegistry()

    # Register test tools
    class MockWeatherTool:
        def run(self, location):
            return f"Weather in {location}: 72°F"

    reg.register_tool('weather', MockWeatherTool())
    return reg

@pytest.fixture
def codemode_client(registry):
    """Create codemode client"""
    return Codemode(
        registry=registry,
        executor_url="http://localhost:8001",
        api_key="test-key"
    )

def test_tool_registration(registry):
    """Test tool registration"""
    assert 'weather' in registry.tools
    assert registry.tools['weather'].run(location='NYC') == "Weather in NYC: 72°F"

def test_code_execution(codemode_client):
    """Test code execution"""
    result = codemode_client.execute("""
weather = tools['weather'].run(location='NYC')
result = {'weather': weather}
""")

    assert result.success
    assert 'NYC' in result.result

@pytest.mark.integration
def test_full_workflow(codemode_client):
    """Test complete workflow"""
    code = """
# Multi-step workflow
w1 = tools['weather'].run(location='NYC')
w2 = tools['weather'].run(location='LA')

result = {
    'nyc': w1,
    'la': w2,
    'comparison': 'NYC' if '72' in w1 else 'LA'
}
"""

    result = codemode_client.execute(code)
    assert result.success
    assert 'nyc' in result.result
    assert 'la' in result.result
```

### Run Tests

```bash
# Unit tests
pytest tests/ -v

# Integration tests (requires executor running)
docker-compose up -d executor
pytest tests/ -v -m integration

# With coverage
pytest tests/ --cov=codemode --cov-report=html
```

---

## Summary

### Minimal Setup (5 minutes)
1. `pip install opencodemode[crewai]`
2. Create `codemode.yaml`
3. Add 10 lines to your app
4. Run `docker-compose up`

### What You Get
- ✅ Secure code execution in isolated container
- ✅ Tools accessible via RPC bridge
- ✅ Same codebase, two containers (main + executor)
- ✅ Production-ready security (9/10)
- ✅ Easy to test and deploy

### Next Steps
1. Review PRD
2. Provide feedback
3. Approve architecture
4. Start implementation!
