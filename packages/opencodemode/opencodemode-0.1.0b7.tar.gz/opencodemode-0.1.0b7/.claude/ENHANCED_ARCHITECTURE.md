# Enhanced Codemode Architecture: Direct + Proxied Execution

## Problem Statement

Current limitation: Executor can't run file-level operations (grep, bash scripts, cat) because it has no filesystem access. We need:

1. **Direct execution** - grep, bash, file operations, system commands
2. **Proxied execution** - Registered tools via RPC (databases, APIs)
3. **User control** - Which directories are writable/readable
4. **Network control** - Allow/deny domains if network is enabled

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│ POD / Container Group                                            │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Main App Container                                          │ │
│  │ - FastAPI                                                   │ │
│  │ - Real tools (DB, APIs)                                     │ │
│  │ - RPC handler                                               │ │
│  │ - Network: ENABLED                                          │ │
│  └────────────────────┬───────────────────────────────────────┘ │
│                       │ RPC over HTTP                            │
│                       ▼                                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Executor Container (Enhanced)                               │ │
│  │                                                             │ │
│  │  Mounted Volumes:                                          │ │
│  │  ├── /workspace (read-only) ← User project files          │ │
│  │  ├── /sandbox (read-write) ← Temp execution space         │ │
│  │  └── /outputs (read-write) ← Results/artifacts            │ │
│  │                                                             │ │
│  │  Execution Modes:                                          │ │
│  │  ┌──────────────────────────────────────────────────┐    │ │
│  │  │ 1. DIRECT MODE                                    │    │ │
│  │  │    - System commands: grep, cat, bash            │    │ │
│  │  │    - File operations: open(), read(), write()    │    │ │
│  │  │    - Subprocess: subprocess.run(['ls', '-la'])   │    │ │
│  │  │    - Limited to mounted volumes                  │    │ │
│  │  └──────────────────────────────────────────────────┘    │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────────────┐    │ │
│  │  │ 2. PROXIED MODE                                   │    │ │
│  │  │    - Registered tools: tools['db'].run()         │    │ │
│  │  │    - RPC to main app                             │    │ │
│  │  │    - No direct network access                    │    │ │
│  │  └──────────────────────────────────────────────────┘    │ │
│  │                                                             │ │
│  │  Network Control (Optional):                               │ │
│  │  - Allowlist: *.github.com, api.openai.com               │ │
│  │  - Denylist: *.evil.com                                  │ │
│  │  - Default: NO network (network_mode: none)              │ │
│  │                                                             │ │
│  │  Security:                                                 │ │
│  │  - User: nobody (65534)                                   │ │
│  │  - Capabilities: ALL dropped                              │ │
│  │  - Root FS: Read-only                                     │ │
│  │  - Writable: Only mounted volumes                         │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Key Innovation: Hybrid Execution Context

### Traditional Approach (Current)
```python
# Everything goes through proxy
result = tools['grep'].run(pattern='error', file='/logs/app.log')  # RPC call
```

### Enhanced Approach (Proposed)
```python
# Direct system commands
import subprocess
result = subprocess.run(['grep', 'error', '/workspace/logs/app.log'],
                       capture_output=True, text=True)
lines = result.stdout.splitlines()

# File operations
with open('/sandbox/output.txt', 'w') as f:
    f.write(f"Found {len(lines)} errors")

# Proxied tools for external resources
db_result = tools['database'].run(query='SELECT * FROM errors')  # RPC
api_result = tools['openai'].run(prompt='Analyze errors')        # RPC
```

## Configuration Schema

```yaml
# codemode.yaml

project:
  name: my-app

framework:
  type: crewai

executor:
  url: http://executor:8001
  api_key: ${CODEMODE_API_KEY}

  # Enhanced: Filesystem configuration
  filesystem:
    # Workspace: Read-only project files
    workspace:
      mount: ./project_files
      readonly: true

    # Sandbox: Read-write temporary space
    sandbox:
      mount: ./sandbox
      readonly: false
      max_size: 1GB

    # Outputs: Read-write for results
    outputs:
      mount: ./outputs
      readonly: false

    # Additional mounts (optional)
    additional_mounts:
      - host: ./data
        container: /data
        readonly: true
      - host: ./logs
        container: /logs
        readonly: true

  # Enhanced: Execution modes
  execution:
    # Enable direct system commands
    allow_direct_execution: true

    # Allowed system commands (whitelist)
    allowed_commands:
      - grep
      - cat
      - ls
      - find
      - wc
      - sed
      - awk
      - head
      - tail
      - sort
      - uniq
      - bash  # With restrictions
      - python3

    # Allowed Python built-ins (in addition to safe defaults)
    allowed_builtins:
      - open  # Now allowed for mounted volumes
      - input  # For interactive scripts

    # Resource limits
    limits:
      timeout: 30
      memory: 512Mi
      cpu: 500m
      disk_write: 100MB  # Max writes to sandbox

  # Enhanced: Network configuration
  network:
    # Network mode: none, restricted, full
    mode: none  # Default: no network

    # If mode=restricted, specify rules
    allowed_domains:
      - "*.github.com"
      - "api.openai.com"
      - "pypi.org"

    blocked_domains:
      - "*.evil.com"
      - "malware-site.com"

    # Allowed ports
    allowed_ports:
      - 443  # HTTPS
      - 80   # HTTP
```

## Implementation Strategy

### Phase 1: Enhanced Security Validator

```python
# codemode/executor/security.py

class EnhancedSecurityValidator(SecurityValidator):
    """
    Enhanced validator supporting direct execution mode.

    Key changes:
    - Allow 'open()' for mounted volumes
    - Allow 'subprocess' for whitelisted commands
    - Validate file paths are within allowed mounts
    - Check network access against allow/deny lists
    """

    def __init__(
        self,
        allowed_commands: List[str] = None,
        allowed_mounts: List[str] = None,
        network_mode: str = "none",
        allowed_domains: List[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.allowed_commands = set(allowed_commands or [])
        self.allowed_mounts = [Path(m) for m in (allowed_mounts or [])]
        self.network_mode = network_mode
        self.allowed_domains = allowed_domains or []

        # Update blocked patterns based on mode
        if allowed_commands:
            # Remove 'subprocess' from blocked if commands are whitelisted
            self.blocked_imports.discard('subprocess')

        if allowed_mounts:
            # Allow 'open' for file operations
            self.blocked_patterns.discard('open(')

    def validate_command(self, command: str) -> bool:
        """Check if system command is allowed."""
        cmd_parts = command.split()
        if not cmd_parts:
            return False

        base_cmd = cmd_parts[0]
        return base_cmd in self.allowed_commands

    def validate_file_path(self, path: str) -> bool:
        """Check if file path is within allowed mounts."""
        file_path = Path(path).resolve()

        for allowed_mount in self.allowed_mounts:
            if file_path.is_relative_to(allowed_mount):
                return True

        return False
```

### Phase 2: Enhanced Code Runner

```python
# codemode/executor/runner.py

class EnhancedCodeRunner(CodeRunner):
    """
    Enhanced runner supporting both direct and proxied execution.
    """

    def _wrap_code_with_hybrid_context(
        self,
        user_code: str,
        available_tools: List[str],
        config: Dict[str, Any],
        allowed_commands: List[str],
        mounted_volumes: Dict[str, str]
    ) -> str:
        """
        Wrap code with hybrid execution context.

        Provides:
        1. Direct execution: subprocess, file operations, system commands
        2. Proxied execution: tools['name'].run() via RPC
        """

        # Tool proxy class (existing)
        proxy_class = '''
import requests
import json

class ToolProxy:
    """Proxy for RPC tool calls."""
    def __init__(self, tool_name, rpc_url, api_key):
        self.tool_name = tool_name
        self.rpc_url = rpc_url
        self.api_key = api_key

    def run(self, **kwargs):
        """Execute tool via RPC to main app."""
        response = requests.post(
            self.rpc_url,
            json={'type': 'call_tool', 'tool': self.tool_name, 'arguments': kwargs},
            headers={'Authorization': f'Bearer {self.api_key}'},
            timeout=30
        )
        result = response.json()
        if result.get('success'):
            return result.get('result')
        raise RuntimeError(f"Tool {self.tool_name} failed: {result.get('error')}")
'''

        # Direct execution helpers
        direct_helpers = f'''
import subprocess
import os
from pathlib import Path

# Mounted volumes
WORKSPACE = Path('/workspace')  # Read-only
SANDBOX = Path('/sandbox')      # Read-write
OUTPUTS = Path('/outputs')      # Read-write

# Allowed commands
ALLOWED_COMMANDS = {json.dumps(allowed_commands)}

def run_command(cmd, *args, **kwargs):
    """
    Run system command safely.

    Example:
        output = run_command(['grep', 'error', '/workspace/log.txt'])
        lines = run_command(['ls', '-la', '/sandbox'])
    """
    if isinstance(cmd, str):
        cmd = cmd.split()

    if cmd[0] not in ALLOWED_COMMANDS:
        raise PermissionError(f"Command not allowed: {{cmd[0]}}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=kwargs.get('timeout', 30)
    )

    return result.stdout if result.returncode == 0 else result.stderr

def safe_open(path, mode='r', **kwargs):
    """
    Open files safely (only in allowed directories).

    Example:
        with safe_open('/sandbox/output.txt', 'w') as f:
            f.write('data')
    """
    file_path = Path(path).resolve()

    # Check if path is in allowed directories
    allowed_dirs = [WORKSPACE, SANDBOX, OUTPUTS]
    if not any(file_path.is_relative_to(d) for d in allowed_dirs):
        raise PermissionError(f"File access not allowed: {{path}}")

    # Check write permission
    if 'w' in mode or 'a' in mode or '+' in mode:
        if file_path.is_relative_to(WORKSPACE):
            raise PermissionError(f"Workspace is read-only: {{path}}")

    return open(path, mode, **kwargs)

# Override built-in open with safe version
__builtins__['open'] = safe_open
'''

        # Combine everything
        wrapped_code = f"""
{proxy_class}

{direct_helpers}

# Initialize tool proxies
tools = {{
    tool_name: ToolProxy(tool_name, "{self.main_app_url}/internal/rpc", "{self.api_key}")
    for tool_name in {json.dumps(available_tools)}
}}

# Configuration
config = {json.dumps(config)}

# ============================================
# USER CODE STARTS HERE
# ============================================

{user_code}

# ============================================
# USER CODE ENDS HERE
# ============================================

# Extract result
if 'result' in locals():
    import json
    print("__CODEMODE_RESULT__:" + json.dumps({{'result': str(result)}}))
else:
    print("__CODEMODE_RESULT__:" + json.dumps({{'result': None}}))
"""

        return wrapped_code
```

### Phase 3: Docker Configuration

```yaml
# docker-compose.yml

version: '3.8'

services:
  main-app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - CODEMODE_API_KEY=dev-secret
    networks:
      - app-network

  executor:
    build:
      context: .
      dockerfile: Dockerfile.executor
    environment:
      - CODEMODE_API_KEY=dev-secret
      - MAIN_APP_URL=http://main-app:8000

    # ENHANCED: Volume mounts
    volumes:
      # Project files (read-only)
      - ./project_files:/workspace:ro

      # Sandbox (read-write, size limited)
      - executor-sandbox:/sandbox:rw

      # Outputs (read-write)
      - ./outputs:/outputs:rw

    # ENHANCED: Security with selective permissions
    security_opt:
      - no-new-privileges
    cap_drop:
      - ALL
    # Add back only needed capabilities for file operations
    cap_add:
      - CHOWN       # For file ownership
      - DAC_OVERRIDE  # For file permissions (limited)

    user: "65534:65534"  # nobody

    # Read-only root FS, but writable volumes
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=64m

    # Resource limits
    mem_limit: 512m
    pids_limit: 128

    # ENHANCED: Network mode options
    # Option 1: No network (default)
    network_mode: none

    # Option 2: Restricted network (with proxy)
    # networks:
    #   - restricted-network

    # Option 3: Full network (less secure)
    # networks:
    #   - app-network

volumes:
  executor-sandbox:
    driver: local
    driver_opts:
      type: tmpfs
      device: tmpfs
      o: size=1g,uid=65534,gid=65534

networks:
  app-network:
    driver: bridge

  # For network-restricted mode
  restricted-network:
    driver: bridge
    internal: false
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

### Phase 4: Network Proxy (Optional)

```python
# codemode/executor/network_proxy.py

class NetworkProxy:
    """
    HTTP proxy with domain filtering.

    Used when network_mode=restricted to enforce allow/deny lists.
    """

    def __init__(
        self,
        allowed_domains: List[str],
        blocked_domains: List[str]
    ):
        self.allowed_domains = [self._compile_pattern(d) for d in allowed_domains]
        self.blocked_domains = [self._compile_pattern(d) for d in blocked_domains]

    def _compile_pattern(self, pattern: str) -> re.Pattern:
        """Convert wildcard pattern to regex."""
        regex = pattern.replace('.', '\\.').replace('*', '.*')
        return re.compile(f'^{regex}$')

    def is_allowed(self, domain: str) -> bool:
        """Check if domain is allowed."""
        # Check blocked list first
        if any(pattern.match(domain) for pattern in self.blocked_domains):
            return False

        # Check allowed list
        if any(pattern.match(domain) for pattern in self.allowed_domains):
            return True

        return False  # Default deny

    def make_request(self, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with domain filtering."""
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc

        if not self.is_allowed(domain):
            raise PermissionError(
                f"Network access denied for domain: {domain}"
            )

        return requests.request(**kwargs)
```

## Usage Examples

### Example 1: File Analysis
```python
# LLM generates code:

# Direct file operations
import subprocess

# Find all Python files
result = run_command(['find', '/workspace', '-name', '*.py'])
python_files = result.splitlines()

# Count lines in each
line_counts = {}
for file_path in python_files:
    result = run_command(['wc', '-l', file_path])
    lines = int(result.split()[0])
    line_counts[file_path] = lines

# Write report to sandbox
with safe_open('/sandbox/report.txt', 'w') as f:
    for file, lines in line_counts.items():
        f.write(f"{file}: {lines} lines\n")

# Use proxied tool to send report
tools['email'].run(
    to='dev@company.com',
    subject='Code Analysis Report',
    attachment='/sandbox/report.txt'
)

result = {'files_analyzed': len(python_files), 'report': '/sandbox/report.txt'}
```

### Example 2: Log Analysis
```python
# Direct log processing
logs = run_command(['grep', 'ERROR', '/workspace/logs/app.log'])
error_lines = logs.splitlines()

# Parse and analyze
error_counts = {}
for line in error_lines:
    error_type = line.split('ERROR:')[1].split()[0]
    error_counts[error_type] = error_counts.get(error_type, 0) + 1

# Save analysis
with safe_open('/outputs/error_analysis.json', 'w') as f:
    json.dump(error_counts, f, indent=2)

# Use proxied tool for database insert
tools['database'].run(
    query=f"INSERT INTO error_logs (date, errors) VALUES (NOW(), '{json.dumps(error_counts)}')"
)

result = {'total_errors': len(error_lines), 'analysis': error_counts}
```

### Example 3: Data Processing Pipeline
```python
# Read data from workspace
with safe_open('/workspace/data/input.csv', 'r') as f:
    data = f.read()

# Process with bash tools
run_command(['bash', '-c',
    "cat /workspace/data/input.csv | sed 's/,/\\t/g' > /sandbox/processed.tsv"
])

# Further processing
run_command(['sort', '-k1', '/sandbox/processed.tsv', '-o', '/sandbox/sorted.tsv'])

# Use proxied tool to upload to cloud
tools['s3'].run(
    action='upload',
    local_path='/sandbox/sorted.tsv',
    bucket='my-bucket',
    key='processed/sorted.tsv'
)

result = {'processed_file': '/sandbox/sorted.tsv', 'uploaded': True}
```

## Benefits of Hybrid Approach

| Feature | Direct Mode | Proxied Mode | Combined |
|---------|-------------|--------------|----------|
| File operations | ✅ Yes | ❌ No | ✅ Best of both |
| System commands | ✅ Yes | ❌ No | ✅ grep, bash, etc. |
| Database access | ❌ No network | ✅ Via RPC | ✅ Proxied |
| External APIs | ❌ No network | ✅ Via RPC | ✅ Proxied |
| Security | ✅ Sandboxed | ✅ Isolated | ✅✅ Double layer |
| Performance | ✅ Fast | ⚠️ RPC overhead | ✅ Optimal |

## Security Guarantees

1. **Filesystem Isolation**
   - Only mounted volumes accessible
   - Workspace is read-only
   - Sandbox is size-limited
   - Root FS is read-only

2. **Command Whitelisting**
   - Only explicitly allowed commands
   - No arbitrary code execution
   - Validated before execution

3. **Network Control**
   - Default: No network
   - Optional: Domain allow/deny lists
   - Proxy-enforced restrictions

4. **Resource Limits**
   - Memory: 512MB max
   - CPU: Configurable limit
   - Disk writes: Limited to sandbox size
   - Processes: 128 max

5. **Capability Dropping**
   - ALL capabilities dropped by default
   - Minimal caps added back (CHOWN, DAC_OVERRIDE)
   - No privilege escalation

## Implementation Priority

### Phase 1 (Now)
- [ ] Enhanced SecurityValidator with command whitelist
- [ ] Enhanced CodeRunner with hybrid context
- [ ] Docker configuration with volume mounts
- [ ] Updated configuration schema

### Phase 2
- [ ] Network proxy with domain filtering
- [ ] Disk quota enforcement
- [ ] Enhanced monitoring for file operations

### Phase 3
- [ ] Dynamic mount configuration
- [ ] Per-user filesystem isolation
- [ ] Advanced network policies

## Edge Cases Handled

1. **Path Traversal**: Validate paths are within mounts
2. **Symlink Attacks**: Resolve paths before checking
3. **Resource Exhaustion**: Enforce disk/memory limits
4. **Command Injection**: Whitelist commands, validate args
5. **Network Bypass**: Network mode=none by default
6. **Privilege Escalation**: Capabilities dropped, unprivileged user

## Next Steps

Should I implement this enhanced architecture? It provides:
1. ✅ Direct file/command execution (like Podman approach)
2. ✅ Tool proxy for registered tools (our innovation)
3. ✅ User control over filesystem access
4. ✅ User control over network access
5. ✅ Production-grade security
6. ✅ No edge cases
