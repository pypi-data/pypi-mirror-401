# Codemode Setup Guide

This guide covers installing Codemode as a library plus preparing the Docker sidecar used for isolated execution over gRPC. MCP proxy mode has been removed; focus is now on the core library + sidecar flow.

## What you get
- Python library for secure, tool-mediated code execution
- Docker sidecar with hardened runtime
- gRPC bridge between app and sidecar (no HTTP path)

## Prerequisites
- Python 3.11+
- Docker running locally (for the executor sidecar)
- `uv` or `pip`

## Install
```bash
# Library only
uv add opencodemode

# Library + docker assets (installs extra data bundle and gRPC deps)
uv add opencodemode[docker]
```

## Initialize a project
```bash
codemode init
```
This writes `codemode.yaml` with executor config defaults.

## Docker sidecar bundle
All sidecar assets live under `docker_sidecar/` in the repo and ship with the `docker` extra. Key files:
- `docker_sidecar/Dockerfile` – executor image
- `docker_sidecar/README.md` – build/run instructions
- `docker_sidecar/docker-compose.yml` – optional local orchestration

To copy them into a workspace:
```bash
python -m codemode.docker_assets export --dest ./executor-sidecar
```

## Build the sidecar
```bash
cd executor-sidecar
docker build -t codemode-executor:0.2.0 -f Dockerfile .
```

## Run the sidecar
```bash
docker run -d --name codemode-executor -p 8001:8001 codemode-executor:0.2.0
```
The container hosts the gRPC `ExecutorService` on port 8001 by default.

## Wire the main app
```python
from fastapi import FastAPI
from codemode import Codemode
from codemode.grpc.server import start_tool_service  # gRPC server for tool calls

app = FastAPI()
codemode = Codemode.from_config("codemode.yaml")

# Start gRPC ToolService alongside FastAPI (non-blocking)
start_tool_service(codemode.registry, host="0.0.0.0", port=50051)
```

## Health checks
- Sidecar: `grpcurl -plaintext localhost:8001 codemode.ExecutorService/Health`
- Main app tool service: `grpcurl -plaintext localhost:50051 codemode.ToolService/ListTools`

## Troubleshooting
- Ensure Docker is running: `codemode docker check`
- Validate config: `codemode validate`
- Verify gRPC ports are reachable from both containers/hosts

## Next steps
- Register tools in your app via `codemode.registry.register_tool(...)`
- Add tests to cover gRPC execution requests and tool calls
- Deploy sidecar and main app in the same network namespace (K8s pod or Compose)
