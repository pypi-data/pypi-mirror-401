# Basic Codemode Example

This example demonstrates basic usage of Codemode with CrewAI.

## Setup

```bash
# Install dependencies
pip install opencodemode[crewai]

# Or with uv
uv add opencodemode[crewai]
```

## Files

- `codemode.yaml` - Configuration file
- `app.py` - Main application
- `tools.py` - Example tools
- `docker-compose.yml` - Docker compose setup (uses `../../docker_sidecar/Dockerfile`)

## Run

### Local Development

1. Start executor:
```bash
# Set environment variable
export CODEMODE_API_KEY=dev-secret-key

# Run executor
python -m codemode.executor.service
```

2. Run main app:
```bash
python app.py
```

3. Test:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Get weather for NYC"}'
```

### With Docker

**Note:** The Dockerfile is located in `../../docker_sidecar/Dockerfile` (project root bundle), not in this examples directory. This is a production-ready setup that all users can use. The main app should also start the gRPC ToolService on port `50051` (see `codemode.grpc.start_tool_service`). Build/tag the executor as `codemode-executor:0.1.0`.

For complete Docker documentation, see [../../docker_sidecar/README.md](../../docker_sidecar/README.md).

#### Option 1: Using codemode CLI (Recommended)

```bash
# 1. Initialize project (creates codemode.yaml)
codemode init

# 2. Check Docker is available
codemode docker check

# 3. Build the executor image (builds from ../../docker_sidecar/Dockerfile)
codemode docker build

# 4. Start the executor container
codemode docker start

# 5. Check container status
codemode docker status

# 6. When done, stop the container
codemode docker stop
```

#### Option 2: Using docker-compose

```bash
# Build and start all services
docker-compose up --build

# Or in detached mode
docker-compose up -d --build

# Stop services
docker-compose down
```

## How It Works

### Hybrid Execution Mode

Codemode supports two execution modes simultaneously:

1. **Direct Execution**: Run system commands (grep, cat, ls) and file operations directly in the executor
2. **Proxied Execution**: Call registered tools via RPC bridge to main app (with network access)

### Execution Flow

1. User sends message to `/chat` endpoint
2. Orchestrator agent (with codemode tool) receives message
3. LLM generates Python code to handle request
4. Code sent to executor container for execution
5. Code can:
   - Run direct commands: `subprocess.run(['grep', 'ERROR', '/workspace/app.log'])`
   - Access files: `open('/workspace/data.txt', 'r')`
   - Call proxied tools: `tools['weather'].run(location='NYC')`
6. Direct commands run in executor, tool calls proxy to main app via RPC
7. Result returned to user

### Example Code

**Direct file operations:**
```python
# Read project file
with open('/workspace/app.log', 'r') as f:
    logs = f.read()

# Use grep to find errors
import subprocess
result = subprocess.run(['grep', 'ERROR', '/workspace/app.log'],
                       capture_output=True, text=True)
errors = result.stdout

# Write to sandbox
with open('/sandbox/analysis.txt', 'w') as f:
    f.write(f"Found {len(errors.split())} errors")
```

**Proxied tool calls:**
```python
# Call weather tool (proxied to main app with network access)
weather = tools['weather'].run(location='NYC')

# Database query (proxied to main app)
db_results = tools['database'].run(query='SELECT * FROM users')
```

**Hybrid usage:**
```python
# Analyze local logs
import subprocess
errors = subprocess.run(['grep', 'ERROR', '/workspace/app.log'],
                       capture_output=True, text=True).stdout

# Send alert via API (proxied to main app)
alert_result = tools['alerting'].run(
    message=f"Found {len(errors.split())} errors in logs"
)
```

## Security

- **Executor Isolation**: Runs in isolated container with minimal privileges
- **Network Control**: No network access by default (except RPC to main app)
- **Filesystem Control**:
  - `/workspace`: Read-only project files
  - `/sandbox`: Read-write scratch space (size-limited)
  - `/outputs`: Read-write for results
- **Command Whitelist**: Only allowed system commands can run
- **Path Validation**: File operations restricted to mounted volumes
- **Resource Limits**: CPU, memory, and disk usage limited
- **All operations logged and audited**
