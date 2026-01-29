# Production Checklist

This guide provides a comprehensive checklist for deploying codemode in production environments, covering security, reliability, monitoring, and performance.

## Security

### Enable TLS Encryption

All production deployments should use TLS for encrypted communication between services.

```yaml
# Executor configuration
environment:
  - CODEMODE_TLS_ENABLED=true
  - CODEMODE_TLS_MODE=custom
  - CODEMODE_TLS_CERT_FILE=/certs/server.crt
  - CODEMODE_TLS_KEY_FILE=/certs/server.key
  - CODEMODE_TLS_CA_FILE=/certs/ca.crt
```

For mutual TLS (mTLS), enable client certificate authentication:

```yaml
environment:
  - CODEMODE_TLS_REQUIRE_CLIENT_AUTH=true
```

Generate production certificates using a trusted CA or your organization's PKI infrastructure. For testing, use the provided script:

```bash
make generate-certs
```

### Strong API Keys

Generate cryptographically secure API keys:

```bash
# Generate a 32-byte random key
openssl rand -base64 32
```

Use Docker secrets or a secrets manager rather than environment variables:

```yaml
secrets:
  codemode_api_key:
    external: true  # Managed by Docker Swarm or external secret store
```

### Network Policies

Isolate the executor service from external networks:

```yaml
networks:
  executor-network:
    driver: bridge
    internal: true  # No external internet access
```

Apply the principle of least privilege:

- Executor should only communicate with the main application
- Block all outbound internet access from the executor
- Use firewall rules to restrict ingress to known sources

### Container Security Hardening

Apply security options to all containers:

```yaml
services:
  executor:
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=100m
    user: "1000:1000"
```

| Option | Purpose |
|--------|---------|
| `no-new-privileges` | Prevents privilege escalation |
| `cap_drop: ALL` | Removes all Linux capabilities |
| `read_only` | Makes the root filesystem read-only |
| `tmpfs` with `noexec` | Prevents execution from temp directories |
| `user` | Runs as non-root user |

## Resource Limits

### CPU and Memory Limits

Set explicit resource limits to prevent resource exhaustion:

```yaml
services:
  executor:
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 128M
```

Recommended limits by workload:

| Workload | CPU Limit | Memory Limit |
|----------|-----------|--------------|
| Light (simple scripts) | 0.5 | 256M |
| Medium (data processing) | 1.0 | 512M |
| Heavy (ML inference) | 2.0 | 2G |

### Execution Timeouts

Configure appropriate timeouts for your use case:

```yaml
environment:
  - CODEMODE_CODE_TIMEOUT=30  # Maximum 30 seconds per execution
  - CODEMODE_MAX_CODE_LENGTH=10000  # Maximum 10KB code size
```

## Monitoring

### Log Aggregation

Configure structured logging for centralized log management:

```yaml
services:
  executor:
    environment:
      - CODEMODE_LOG_LEVEL=INFO
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
        labels: "service,environment"
```

For production, use a log aggregation service:

```yaml
logging:
  driver: fluentd
  options:
    fluentd-address: "localhost:24224"
    tag: "codemode.executor"
```

### Correlation IDs for Tracing

Codemode supports correlation IDs for distributed tracing. Include correlation IDs in your requests to trace execution across services:

```python
from codemode import Codemode

cm = Codemode()
result = cm.execute(
    code="print('hello')",
    correlation_id="req-12345-abc"  # Trace ID from your system
)
```

Correlation IDs appear in logs and can be used to trace requests across:

- Main application logs
- Executor service logs
- gRPC call traces

### Health Check Endpoints

The executor exposes a health check via TCP socket on port 8001. Monitor container health:

```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import socket; s=socket.socket(); s.settimeout(5); s.connect(('localhost', 8001)); s.close()"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

Configure alerts based on health status:

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' codemode-executor
```

### Metrics Collection

Integrate with your monitoring stack by exposing metrics:

```python
# Example: Custom metrics in your application
import time

start = time.time()
result = cm.execute(code=code)
duration = time.time() - start

# Send to your metrics system
metrics.histogram("codemode.execution.duration", duration)
metrics.counter("codemode.execution.count", 1, tags={"success": result.success})
```

## High Availability

### Multiple Executor Replicas

Deploy multiple executor instances for redundancy and load distribution:

```yaml
services:
  executor:
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
```

### Load Balancing

Use a load balancer or service mesh for distributing requests:

```yaml
services:
  executor:
    deploy:
      replicas: 3
      endpoint_mode: vip  # Virtual IP for load balancing
```

For gRPC load balancing, consider:

- Client-side load balancing with gRPC's built-in support
- Service mesh (Istio, Linkerd) for transparent load balancing
- Envoy proxy for gRPC-aware routing

### Rolling Updates

Configure rolling updates for zero-downtime deployments:

```yaml
deploy:
  update_config:
    parallelism: 1      # Update one container at a time
    delay: 10s          # Wait between updates
    failure_action: rollback
    monitor: 60s        # Monitor for failures
    order: start-first  # Start new before stopping old
```

## Backup and Recovery

### Configuration Backup

Store configuration in version control:

```
config/
  production/
    docker-compose.yml
    codemode-sidecar.yaml
  staging/
    docker-compose.yml
    codemode-sidecar.yaml
```

### Certificate Management

Implement certificate rotation:

```bash
# Rotate certificates without downtime
docker secret create codemode_cert_v2 ./new-cert.pem
docker service update --secret-rm codemode_cert_v1 --secret-add codemode_cert_v2 executor
```

### Disaster Recovery

Document and test recovery procedures:

1. Container failure: Automatic restart via `restart: unless-stopped`
2. Host failure: Swarm/Kubernetes reschedules containers
3. Data center failure: Multi-region deployment with DNS failover

## Performance Tuning

### Timeout Configuration

Tune timeouts based on your workload characteristics:

| Setting | Light Workload | Heavy Workload |
|---------|----------------|----------------|
| `CODEMODE_CODE_TIMEOUT` | 10s | 120s |
| Health check interval | 30s | 60s |
| Health check timeout | 5s | 30s |

### Retry Settings

Configure retry behavior for transient failures:

```python
from codemode import Codemode

cm = Codemode(
    retry_attempts=3,
    retry_delay=1.0,  # seconds
    retry_backoff=2.0  # exponential backoff multiplier
)
```

### Connection Pooling

For high-throughput scenarios, configure connection management:

```python
from codemode import Codemode

cm = Codemode(
    max_connections=10,
    connection_timeout=30.0
)
```

## Kubernetes Deployment

For Kubernetes deployments, consider these patterns:

### Basic Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: codemode-executor
spec:
  replicas: 3
  selector:
    matchLabels:
      app: codemode-executor
  template:
    metadata:
      labels:
        app: codemode-executor
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
        - name: executor
          image: codemode-executor:latest
          ports:
            - containerPort: 8001
          env:
            - name: CODEMODE_API_KEY
              valueFrom:
                secretKeyRef:
                  name: codemode-secrets
                  key: api-key
          resources:
            limits:
              cpu: "1"
              memory: 512Mi
            requests:
              cpu: "250m"
              memory: 128Mi
          securityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
                - ALL
            readOnlyRootFilesystem: true
          livenessProbe:
            tcpSocket:
              port: 8001
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            tcpSocket:
              port: 8001
            initialDelaySeconds: 5
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: codemode-executor
spec:
  selector:
    app: codemode-executor
  ports:
    - port: 8001
      targetPort: 8001
```

### Network Policy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: executor-isolation
spec:
  podSelector:
    matchLabels:
      app: codemode-executor
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: main-app
      ports:
        - port: 8001
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: main-app
      ports:
        - port: 50051
```

### Pod Disruption Budget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: codemode-executor-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: codemode-executor
```

## Deployment Checklist

Use this checklist before deploying to production:

### Security
- [ ] TLS enabled for all gRPC communication
- [ ] Strong API keys generated and stored securely
- [ ] Network isolation configured (internal network)
- [ ] Container security hardening applied
- [ ] No secrets in environment variables or images

### Reliability
- [ ] Resource limits configured
- [ ] Health checks enabled
- [ ] Restart policies defined
- [ ] Multiple replicas for high availability
- [ ] Rolling update strategy configured

### Monitoring
- [ ] Log aggregation configured
- [ ] Correlation IDs implemented
- [ ] Health check alerts configured
- [ ] Metrics collection enabled

### Operations
- [ ] Backup procedures documented
- [ ] Certificate rotation process defined
- [ ] Disaster recovery plan tested
- [ ] Runbook for common issues created

## Next Steps

- [Docker Deployment](docker.md) - Single container deployment guide
- [Docker Compose Setup](docker-compose.md) - Multi-service deployment
- [TLS Encryption](../features/tls-encryption.md) - Certificate configuration details
