# Hybrid Execution Mode

## Overview

Codemode's hybrid execution mode enables AI agents to run both **direct system commands** and **proxied tool calls** within the same code execution environment. This provides the best of both worlds:

- **Direct Execution**: Run system commands (grep, cat, ls) and file operations directly in the executor container
- **Proxied Execution**: Call registered tools via RPC bridge to the main application (with network access)

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          User Request                            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Main Application (Orchestrator)               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • CrewAI Agents                                           │  │
│  │ • Registered Tools (weather, database, alerting, etc.)   │  │
│  │ • Network Access (APIs, databases)                       │  │
│  │ • RPC Server (receives tool calls from executor)         │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────┘
                                │ RPC Bridge
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Executor Container (Isolated)                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Direct Execution:                                         │  │
│  │ • System commands (grep, cat, ls, find, etc.)           │  │
│  │ • File operations (read/write)                           │  │
│  │ • Bash scripts                                           │  │
│  │ • Python subprocess calls                                │  │
│  │                                                           │  │
│  │ Proxied Execution:                                       │  │
│  │ • tools['weather'].run(location='NYC')                  │  │
│  │ • tools['database'].run(query='...')                    │  │
│  │ • All tool calls send RPC to main app                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Volumes:                                                        │
│  • /workspace (read-only project files)                         │
│  • /sandbox (read-write scratch space)                          │
│  • /outputs (read-write results)                                │
│                                                                  │
│  Security:                                                       │
│  • Command whitelist                                             │
│  • Path validation                                               │
│  • No network access (except RPC)                                │
│  • Resource limits                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Configuration

### Basic Hybrid Execution

```yaml
executor:
  url: http://executor:8001
  api_key: ${CODEMODE_API_KEY}

  # Enable hybrid execution
  execution:
    allow_direct_execution: true
    allowed_commands:
      - grep
      - cat
      - ls
      - find
      - wc
      - head
      - tail
      - bash

  # Filesystem access control
  filesystem:
    workspace:
      mount: ./project_files
      readonly: true
    sandbox:
      mount: /sandbox
      readonly: false
      max_size: 1GB
    outputs:
      mount: ./outputs
      readonly: false

  # Network control (executor has no network access)
  network:
    mode: none
```

### Advanced Configuration with Network Access

```yaml
executor:
  execution:
    allow_direct_execution: true
    allowed_commands:
      - grep
      - cat
      - curl  # Allow network commands

  network:
    mode: restricted
    allowed_domains:
      - "*.github.com"
      - "api.openai.com"
      - "pypi.org"
    blocked_domains:
      - "malware.com"
```

## Usage Examples

### 1. Direct File Operations

```python
# Read project files
with open('/workspace/app.log', 'r') as f:
    logs = f.read()

# Parse and analyze
errors = [line for line in logs.split('\n') if 'ERROR' in line]

# Write to sandbox
with open('/sandbox/error_analysis.txt', 'w') as f:
    f.write(f"Found {len(errors)} errors\n")
    for error in errors:
        f.write(f"{error}\n")
```

### 2. System Commands

```python
import subprocess

# Use grep to find errors in logs
result = subprocess.run(
    ['grep', 'ERROR', '/workspace/app.log'],
    capture_output=True,
    text=True
)
errors = result.stdout

# Count lines
line_count = subprocess.run(
    ['wc', '-l', '/workspace/data.txt'],
    capture_output=True,
    text=True
).stdout.strip()

print(f"Found {len(errors.split())} errors")
print(f"Data file has {line_count} lines")
```

### 3. Bash Scripts

```python
import subprocess

# Run bash script for complex operations
bash_script = """
#!/bin/bash
cd /workspace
find . -name "*.log" -type f | while read file; do
    echo "Processing $file"
    grep -c ERROR "$file"
done
"""

result = subprocess.run(
    ['bash', '-c', bash_script],
    capture_output=True,
    text=True
)
print(result.stdout)
```

### 4. Proxied Tool Calls

```python
# Call weather API (proxied to main app with network access)
weather = tools['weather'].run(location='NYC', units='metric')
print(f"Temperature: {weather['temperature']}°C")

# Query database (proxied to main app)
db_results = tools['database'].run(
    query='SELECT * FROM users WHERE status = "active"'
)
print(f"Active users: {len(db_results)}")

# Send alert (proxied to main app)
alert_result = tools['alerting'].run(
    message='Daily report generated',
    priority='low'
)
```

### 5. Hybrid Usage - The Best of Both Worlds

```python
import subprocess

# 1. Analyze local log files directly
log_errors = subprocess.run(
    ['grep', '-i', 'ERROR', '/workspace/app.log'],
    capture_output=True,
    text=True
).stdout

error_count = len(log_errors.split('\n'))

# 2. Get additional context from database (proxied)
error_details = tools['database'].run(
    query=f"SELECT * FROM error_logs WHERE timestamp > NOW() - INTERVAL '1 hour'"
)

# 3. Generate analysis file
with open('/sandbox/hourly_report.txt', 'w') as f:
    f.write(f"Hourly Error Report\n")
    f.write(f"=" * 50 + "\n\n")
    f.write(f"Log file errors: {error_count}\n")
    f.write(f"Database errors: {len(error_details)}\n\n")
    f.write("Recent errors:\n")
    for error in error_details[:10]:
        f.write(f"- {error['message']}\n")

# 4. Send notification (proxied)
if error_count > 100:
    alert_result = tools['alerting'].run(
        message=f"High error rate detected: {error_count} errors in last hour",
        priority='high',
        channels=['email', 'slack']
    )
    print(f"Alert sent: {alert_result}")

# 5. Copy report to outputs
subprocess.run(['cp', '/sandbox/hourly_report.txt', '/outputs/'])

result = f"Report generated: {error_count} errors found"
```

## Security Features

### Command Whitelisting

Only explicitly allowed commands can be executed:

```yaml
execution:
  allowed_commands:
    - grep
    - cat
    - ls
    # rm, dd, and other dangerous commands are NOT allowed
```

If code tries to run an unauthorized command:

```python
subprocess.run(['rm', '-rf', '/'])  # ❌ Blocked: unauthorized command
```

### Path Validation

File operations are restricted to mounted volumes:

```python
# ✅ Allowed: within /workspace
with open('/workspace/data.txt', 'r') as f:
    data = f.read()

# ✅ Allowed: within /sandbox
with open('/sandbox/output.txt', 'w') as f:
    f.write("results")

# ❌ Blocked: outside allowed paths
with open('/etc/passwd', 'r') as f:  # Security violation
    data = f.read()
```

### Network Control

Three network modes:

1. **none** (default): No network access except RPC to main app
2. **restricted**: Only allowed domains accessible
3. **all**: Full network access (use with caution)

```yaml
network:
  mode: restricted
  allowed_domains:
    - "*.github.com"    # Wildcard patterns supported
    - "api.openai.com"  # Exact domain match
  blocked_domains:
    - "malware.com"     # Explicit blocks
```

### Resource Limits

```yaml
limits:
  code_timeout: 30        # Max execution time (seconds)
  max_code_length: 10000  # Max code size (characters)
  memory_limit: 512Mi     # Container memory limit
```

```yaml
filesystem:
  sandbox:
    max_size: 1GB  # Limit sandbox disk usage
```

## Docker Configuration

### docker-compose.yml

```yaml
services:
  executor:
    volumes:
      # Read-only workspace
      - ./project_files:/workspace:ro
      # Read-write sandbox with size limit
      - executor-sandbox:/sandbox:rw
      # Read-write outputs
      - ./outputs:/outputs:rw

    security_opt:
      - no-new-privileges:true

    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETUID
      - SETGID

    read_only: false  # Allow writes to sandbox/outputs

    tmpfs:
      - /tmp:size=100M,mode=1777

    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M

volumes:
  executor-sandbox:
    driver: local
    driver_opts:
      type: tmpfs
      device: tmpfs
      o: size=1024m
```

## Common Patterns

### Log Analysis with Alerting

```python
import subprocess

# Analyze logs with grep
critical_errors = subprocess.run(
    ['grep', '-i', 'CRITICAL', '/workspace/app.log'],
    capture_output=True, text=True
).stdout

if critical_errors:
    # Alert via proxied tool
    tools['alerting'].run(
        message=f"Critical errors found:\n{critical_errors[:500]}",
        priority='high'
    )
```

### Data Processing Pipeline

```python
import subprocess
import json

# 1. Extract data from files
data = subprocess.run(
    ['cat', '/workspace/data.json'],
    capture_output=True, text=True
).stdout

# 2. Process data
records = json.loads(data)
processed = [r for r in records if r['status'] == 'pending']

# 3. Store results in sandbox
with open('/sandbox/processed.json', 'w') as f:
    json.dump(processed, f)

# 4. Upload to database (proxied)
result = tools['database'].run(
    operation='bulk_insert',
    table='processed_records',
    data=processed
)

# 5. Generate report
subprocess.run([
    'bash', '-c',
    'wc -l /workspace/data.json > /outputs/report.txt'
])
```

### File Search and Analysis

```python
import subprocess

# Find all Python files
py_files = subprocess.run(
    ['find', '/workspace', '-name', '*.py', '-type', 'f'],
    capture_output=True, text=True
).stdout.strip().split('\n')

# Count lines of code
total_lines = 0
for file in py_files:
    lines = subprocess.run(
        ['wc', '-l', file],
        capture_output=True, text=True
    ).stdout.split()[0]
    total_lines += int(lines)

# Store metrics (proxied)
tools['metrics'].run(
    metric='codebase_size',
    value=total_lines,
    tags={'language': 'python'}
)
```

## Best Practices

### 1. Use Direct Execution for File Operations

```python
# ✅ Good: Direct file operations
with open('/workspace/config.json', 'r') as f:
    config = json.load(f)

# ❌ Avoid: Proxying simple file reads
# config = tools['file_reader'].run(path='/workspace/config.json')
```

### 2. Use Proxied Tools for External Resources

```python
# ✅ Good: Proxy for API calls
weather = tools['weather'].run(location='NYC')

# ❌ Avoid: Direct API calls (no network in executor)
# response = requests.get('https://api.weather.com/...')
```

### 3. Validate Paths

```python
# ✅ Good: Use allowed paths
output_path = '/sandbox/results.txt'

# ❌ Avoid: Absolute paths outside mounted volumes
# output_path = '/tmp/results.txt'  # May be blocked
```

### 4. Handle Errors

```python
import subprocess

try:
    result = subprocess.run(
        ['grep', 'PATTERN', '/workspace/file.txt'],
        capture_output=True,
        text=True,
        check=True  # Raise on non-zero exit
    )
except subprocess.CalledProcessError as e:
    print(f"Command failed: {e.stderr}")
```

### 5. Limit Data in Memory

```python
# ✅ Good: Stream large files
def process_large_file():
    with open('/workspace/large.log', 'r') as f:
        for line in f:  # Process line by line
            if 'ERROR' in line:
                yield line

# ❌ Avoid: Loading entire file into memory
# with open('/workspace/large.log', 'r') as f:
#     all_data = f.read()  # May exceed memory limits
```

## Troubleshooting

### Command Not Allowed

**Error**: `unauthorized_command: rm`

**Solution**: Add command to whitelist in `codemode.yaml`:

```yaml
execution:
  allowed_commands:
    - rm  # Only if absolutely necessary
```

### Path Access Denied

**Error**: `unauthorized_path: /etc/passwd`

**Solution**: Ensure files are in mounted volumes:

```yaml
filesystem:
  workspace:
    mount: ./my_files
    readonly: true
```

### Import Error: No module 'subprocess'

**Error**: `ModuleNotFoundError: No module named 'subprocess'`

**Solution**: Enable direct execution:

```yaml
execution:
  allow_direct_execution: true
```

### Network Access Denied

**Error**: `requests.exceptions.ConnectionError`

**Solution**: Either:

1. Use proxied tool instead of direct network call
2. Enable network access (not recommended):

```yaml
network:
  mode: restricted
  allowed_domains:
    - "your-domain.com"
```

## Performance Considerations

### Direct vs Proxied

| Operation | Mode | Performance |
|-----------|------|-------------|
| File read/write | Direct | Fast (local FS) |
| System commands | Direct | Fast (subprocess) |
| API calls | Proxied | Slower (RPC overhead) |
| Database queries | Proxied | Slower (RPC overhead) |

### Optimization Tips

1. **Batch operations**: Minimize RPC calls by batching tool invocations
2. **Cache results**: Store proxied tool results in sandbox if reused
3. **Use direct operations**: Prefer direct file/command operations when possible
4. **Stream large files**: Don't load entire files into memory

## Security Considerations

### ✅ Safe Practices

- Use command whitelist
- Validate all paths
- Limit network access
- Set resource limits
- Monitor execution logs

### ❌ Avoid

- Disabling security features
- Allowing dangerous commands (rm, dd, chmod, etc.)
- Granting full network access
- Using root user in container
- Skipping path validation

## Related Documentation

- [RPC Bridge Architecture](./rpc-bridge.md)
- [Security Validator](./secure-executor.md)
- [CrewAI Integration](./crewai-integration.md)
- [Configuration Reference](./configuration.md)
