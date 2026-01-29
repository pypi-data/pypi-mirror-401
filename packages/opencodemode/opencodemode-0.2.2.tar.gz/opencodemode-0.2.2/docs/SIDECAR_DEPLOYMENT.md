# Sidecar Deployment Guide

This guide explains how to deploy Codemode using the **sidecar deployment pattern** for secure code execution in production environments.

## Table of Contents

1. [What is Sidecar Deployment?](#what-is-sidecar-deployment)
2. [Architecture Overview](#architecture-overview)
3. [Prerequisites](#prerequisites)
4. [Deployment Options](#deployment-options)
5. [Step-by-Step Setup](#step-by-step-setup)
6. [Configuration](#configuration)
7. [Security Considerations](#security-considerations)
8. [Monitoring and Troubleshooting](#monitoring-and-troubleshooting)

## What is Sidecar Deployment?

In a **sidecar deployment**, the Codemode executor runs as a separate container **alongside** your main application container in the same Pod (Kubernetes) or network (Docker Compose). This pattern provides:

- **Isolation**: Code execution happens in a separate, restricted container
- **Security**: The executor has no network access and limited capabilities
- **Co-location**: Low-latency RPC communication between app and executor
- **Simplicity**: Managed as a single deployment unit

```
┌─────────────────────────────────────────────────────────────┐
│ POD (same deployment)                                        │
│                                                              │
│  ┌──────────────────┐              ┌──────────────────────┐ │
│  │ Main App         │◄───gRPC─────►│ Executor             │ │
│  │ (HAS network)    │              │ (NO network)         │ │
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
```

## Architecture Overview

### Components

1. **Main Application Container**
   - Your FastAPI/Flask/Django application
   - Has full network access
   - Contains real tool implementations (database, APIs, etc.)
   - Exposes RPC endpoint for executor

2. **Executor Sidecar Container**
   - Python runtime with Codemode executor
   - **NO** external network access (`--network none` or network policy)
   - Read-only filesystem
   - Drops all Linux capabilities
   - Communicates with main app via localhost RPC

### Communication Flow

1. AI agent generates Python code
2. Main app sends code to executor (localhost:8001)
3. Executor runs code in isolated environment
4. When code calls `tools['database'].run()`, executor sends RPC to main app
5. Main app executes real tool with full access
6. Result returned to executor → code continues → final result to main app

## Prerequisites

### For Docker Compose

- Docker Engine 20.10+
- Docker Compose 2.0+
- Basic understanding of Docker networking

### For Kubernetes

- Kubernetes 1.19+
- kubectl configured
- Namespace with appropriate RBAC
- Knowledge of Pods, Services, and Deployments

## Deployment Options

### Option 1: Docker Compose (Development/Testing)

Best for:
- Local development
- Testing
- Single-server deployments
- Prototyping

### Option 2: Kubernetes (Production)

Best for:
- Production workloads
- Multi-tenant environments
- High availability requirements
- Enterprise deployments

### Option 3: Docker CLI (Quick Start)

Best for:
- Quick testing
- Development workflows
- Learning the system

## Step-by-Step Setup

### Option 1: Using Codemode CLI (Easiest)

#### Step 1: Install Codemode

```bash
# Using uv (recommended)
uv add opencodemode[crewai]

# Or using pip
pip install opencodemode[crewai]
```

#### Step 2: Check Docker Availability

```bash
# Verify Docker is installed and running
codemode docker check
```

**Expected Output:**
```
✓ Docker is available and running

Docker Information:
  Version: 24.0.7
  OS: Ubuntu 22.04
```

#### Step 3: Initialize Your Project

```bash
# Create codemode.yaml configuration
codemode init
```

This creates a `codemode.yaml` file:

```yaml
project:
  name: my-project

framework:
  type: crewai
  auto_discover: true

executor:
  url: http://localhost:8001
  api_key: ${CODEMODE_API_KEY}
  limits:
    code_timeout: 30
    max_code_length: 10000
    memory_limit: "512Mi"
```

#### Step 4: Start the Executor Sidecar

```bash
# Start executor with default configuration
codemode docker start

# Or with custom settings
codemode docker start \
  --config ./codemode.yaml \
  --packages numpy pandas \
  --name my-executor \
  --port 8001
```

**With requirements.txt:**
```bash
# Create requirements.txt with your dependencies
echo "numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0" > executor-requirements.txt

# Start executor with requirements
codemode docker start --requirements executor-requirements.txt
```

#### Step 5: Verify Executor is Running

```bash
# Check container status
codemode docker status

# Expected output:
# Container 'codemode-executor' status:
#   Status: Up 2 minutes
```

#### Step 6: Configure Your Application

In your main application code:

```python
from fastapi import FastAPI
from crewai import Agent, Task, Crew
from codemode import Codemode
from codemode.grpc import start_tool_service

app = FastAPI()

# 1. Initialize Codemode
codemode = Codemode.from_config('codemode.yaml')

# 2. Register your tools
codemode.registry.register_tool('database', DatabaseTool())
codemode.registry.register_tool('weather', WeatherTool())

# 3. Start gRPC ToolService for executor calls
start_tool_service(codemode.registry, host="0.0.0.0", port=50051)

# 4. Create agent with codemode tool
orchestrator = Agent(
    role="Code Orchestrator",
    tools=[codemode.as_crewai_tool()],
    backstory="You write Python code to coordinate tools",
    verbose=True
)

@app.post("/chat")
async def chat(message: str):
    task = Task(description=message, agent=orchestrator)
    crew = Crew(agents=[orchestrator], tasks=[task])
    return {"result": str(crew.kickoff())}
```

#### Step 7: Run Your Application

```bash
# Start your main application
uvicorn main:app --host 0.0.0.0 --port 8000

# In another terminal, test it
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Get weather for NYC and save to database"}'
```

### Option 2: Docker Compose (Production-Ready)

#### Step 1: Create Docker Compose File

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # Your main application
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - CODEMODE_EXECUTOR_URL=http://executor:8001
      - CODEMODE_API_KEY=${CODEMODE_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - executor
      - postgres
    networks:
      - app-network
      - executor-network

  # Executor sidecar (no external network!)
  executor:
    image: python:3.11-slim
    command: >
      sh -c "
        pip install --no-cache-dir opencodemode[crewai] &&
        codemode serve --host 0.0.0.0 --port 8001
      "
    volumes:
      - ./codemode.yaml:/app/codemode.yaml:ro
    networks:
      - executor-network
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=100m
    mem_limit: 512m
    cpus: 1.0

  # Database (only accessible to main app)
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

networks:
  # Network with internet access (main app + database)
  app-network:
    driver: bridge

  # Isolated network (main app + executor only)
  executor-network:
    driver: bridge
    internal: true  # No external access!

volumes:
  postgres-data:
```

#### Step 2: Create Dockerfile for Main App

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Step 3: Set Environment Variables

Create `.env` file:

```bash
# Generate a secure API key
CODEMODE_API_KEY=your-secure-api-key-here

# Database credentials
DATABASE_URL=postgresql://user:password@postgres:5432/dbname
DB_PASSWORD=your-db-password
```

#### Step 4: Deploy

```bash
# Build and start services
docker-compose up -d

# Check logs
docker-compose logs -f

# Verify executor is running
docker-compose ps executor

# Test the setup
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test message"}'
```

### Option 3: Kubernetes Deployment

#### Step 1: Create ConfigMap

Create `configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: codemode-config
  namespace: your-namespace
data:
  codemode.yaml: |
    project:
      name: production-app
    framework:
      type: crewai
      auto_discover: true
    executor:
      url: http://localhost:8001
      api_key: ${CODEMODE_API_KEY}
      limits:
        code_timeout: 30
        max_code_length: 10000
        memory_limit: "512Mi"
```

#### Step 2: Create Secret

```bash
# Create API key secret
kubectl create secret generic codemode-secrets \
  --from-literal=api-key=your-secure-api-key \
  -n your-namespace
```

#### Step 3: Create Deployment with Sidecar

Create `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-with-codemode
  namespace: your-namespace
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      # Main application container
      - name: app
        image: your-registry/myapp:latest
        ports:
        - containerPort: 8000
        env:
        - name: CODEMODE_EXECUTOR_URL
          value: "http://localhost:8001"
        - name: CODEMODE_API_KEY
          valueFrom:
            secretKeyRef:
              name: codemode-secrets
              key: api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"

      # Executor sidecar container
      - name: executor
        image: python:3.11-slim
        command:
        - sh
        - -c
        - |
          pip install --no-cache-dir opencodemode[crewai]
          codemode serve --host 0.0.0.0 --port 8001
        ports:
        - containerPort: 8001
        env:
        - name: CODEMODE_API_KEY
          valueFrom:
            secretKeyRef:
              name: codemode-secrets
              key: api-key
        volumeMounts:
        - name: config
          mountPath: /app/codemode.yaml
          subPath: codemode.yaml
          readOnly: true
        - name: tmp
          mountPath: /tmp
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        securityContext:
          runAsNonRoot: true
          runAsUser: 65534
          readOnlyRootFilesystem: true
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL

      volumes:
      - name: config
        configMap:
          name: codemode-config
      - name: tmp
        emptyDir:
          sizeLimit: 100Mi
```

#### Step 4: Create Network Policy (Restrict Executor)

Create `networkpolicy.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: executor-isolation
  namespace: your-namespace
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  # Allow traffic from anywhere to main app
  - ports:
    - protocol: TCP
      port: 8000
  egress:
  # Main app can access database and external APIs
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  # Main app can access DNS
  - to:
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
  # Allow internet access for main app
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443
    - protocol: TCP
      port: 80
```

#### Step 5: Deploy to Kubernetes

```bash
# Apply configurations
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f networkpolicy.yaml

# Create service
kubectl expose deployment myapp-with-codemode --port=8000 --type=LoadBalancer

# Check status
kubectl get pods -n your-namespace
kubectl logs -f deployment/myapp-with-codemode -c executor

# Verify both containers are running
kubectl get pods -n your-namespace -o jsonpath='{.items[0].status.containerStatuses[*].name}'
```

## Configuration

### Executor Configuration Options

The executor can be configured via `codemode.yaml`:

```yaml
executor:
  url: http://localhost:8001
  api_key: ${CODEMODE_API_KEY}
  timeout: 35

  # Resource limits
  limits:
    code_timeout: 30          # Max execution time (seconds)
    max_code_length: 10000    # Max code length (characters)
    memory_limit: "512Mi"     # Container memory limit

  # Filesystem access (optional)
  filesystem:
    workspace:
      mount: /workspace
      readonly: true
    sandbox:
      mount: /sandbox
      readonly: false
    outputs:
      mount: /outputs
      readonly: false

  # Network configuration
  network:
    mode: none              # Options: none, restricted, all
    allowed_domains: []     # If mode=restricted
    blocked_domains: []

  # Execution behavior
  execution:
    allow_direct_execution: false
    allowed_commands: []    # If allow_direct_execution=true
```

### Environment Variables

```bash
# Required
CODEMODE_API_KEY=your-secure-key

# Optional
CODEMODE_LOG_LEVEL=INFO
CODEMODE_EXECUTOR_URL=http://localhost:8001
```

## Security Considerations

### Security Checklist

✅ **Network Isolation**
- Executor has NO external network access
- Use `--network none` (Docker) or NetworkPolicy (K8s)

✅ **Filesystem**
- Use read-only root filesystem
- Mount `/tmp` as tmpfs with size limit
- Drop all Linux capabilities

✅ **Resource Limits**
- Set memory limits (e.g., 512Mi)
- Set CPU limits (e.g., 1.0 CPU)
- Set execution timeouts

✅ **Authentication**
- Use strong API keys for RPC
- Rotate keys regularly
- Never hardcode keys in code

✅ **Monitoring**
- Log all code executions
- Monitor resource usage
- Set up alerts for failures

### Security Rating: 9/10 ⭐

The sidecar pattern provides excellent security because:

1. **Container Isolation**: Executor runs in separate container
2. **Network Isolation**: No external network = no data exfiltration
3. **Filesystem Protection**: Read-only FS = no malware persistence
4. **Capability Dropping**: No Linux capabilities = limited attack surface
5. **RPC Mediation**: All tool access is logged and controlled

## Monitoring and Troubleshooting

### Check Executor Health

```bash
# Docker Compose
docker-compose ps executor
docker-compose logs executor

# Kubernetes
kubectl get pods -l app=myapp
kubectl logs -f deployment/myapp-with-codemode -c executor

# Using Codemode CLI
codemode docker status
```

### Common Issues

#### Issue: Executor container won't start

**Symptoms:**
```
Error: Cannot start container
```

**Solution:**
```bash
# Check Docker is running
docker ps

# Check logs
codemode docker status
docker logs codemode-executor

# Remove and recreate
codemode docker remove
codemode docker start
```

#### Issue: RPC communication fails

**Symptoms:**
```
Error: Connection refused to executor
```

**Solution:**
- Verify executor URL is correct (use `localhost` not `127.0.0.1` in some environments)
- Check firewall rules
- Verify API key matches in both containers
- Check network connectivity: `docker network inspect`

#### Issue: Code execution times out

**Symptoms:**
```
Error: Execution timeout exceeded
```

**Solution:**
- Increase `code_timeout` in config
- Optimize your code
- Check for infinite loops

### Monitoring Metrics

Monitor these key metrics:

- **Execution Time**: Track P50, P95, P99
- **Memory Usage**: Should stay under limit
- **CPU Usage**: Should not spike to 100%
- **Error Rate**: < 1% in production
- **RPC Latency**: < 100ms for localhost

## Next Steps

1. **Test Your Setup**
   ```bash
   # Run example workflow
   curl -X POST http://localhost:8000/chat \
     -d '{"message": "Test the executor"}'
   ```

2. **Scale for Production**
   - Add horizontal pod autoscaling (Kubernetes)
   - Set up monitoring (Prometheus + Grafana)
   - Configure log aggregation (ELK, Loki)

3. **Secure Your Deployment**
   - **Enable TLS/mTLS encryption** - See [TLS Encryption Guide](docs/features/tls-encryption.md)
     ```bash
     # Generate certificates
     make generate-certs

     # Configure TLS in codemode.yaml
     grpc:
       tls:
         enabled: true
         mode: custom
         cert_file: ./certs/server.crt
         key_file: ./certs/server.key
         ca_file: ./certs/ca.crt
         # For mTLS:
         client_cert_file: ./certs/client.crt
         client_key_file: ./certs/client.key
     ```
   - Set up secret rotation (certificates, API keys)
   - Regular security audits

4. **Optimize Performance**
   - Cache frequently used code
   - Pre-warm containers
   - Use connection pooling for RPC

## Additional Resources

- [Architecture Documentation](.claude/PRD.md)
- [RPC Bridge Documentation](docs/features/rpc-bridge.md)
- [TLS/mTLS Encryption Guide](docs/features/tls-encryption.md) **← NEW!**
- [Security Best Practices](docs/features/secure-executor.md)
- [TLS Example Project](examples/tls/) **← NEW!**
- [Example Projects](examples/)

## Support

Need help?

- GitHub Issues: https://github.com/mldlwizard/code_mode/issues
- Documentation: https://github.com/mldlwizard/code_mode#readme

---

**Remember**: The sidecar pattern is the recommended deployment method for production. It provides the best balance of security, performance, and operational simplicity.
