# Codemode

**Secure code execution for multi-agent AI systems**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11-3.13](https://img.shields.io/badge/python-3.11--3.13-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Codemode enables AI agents to dynamically generate and execute code to orchestrate complex workflows while maintaining production-grade security through isolated execution environments.

## Key Features

- **Secure Execution**: Code runs in isolated Docker containers with security hardening
- **RPC Bridge**: Tools execute in main app with full access, code runs in isolation
- **TLS/mTLS Encryption**: End-to-end encryption for all gRPC communications
- **Retry Logic**: Automatic retries with exponential backoff for transient failures
- **Correlation IDs**: End-to-end request tracing across the distributed system
- **Framework Support**: Native CrewAI integration, LangChain and LangGraph coming soon

## Quick Start

### Installation

```bash
pip install opencodemode[crewai]
```

### Basic Usage

```python
from codemode import Codemode
from codemode.config import ClientConfig

# Configure the client
config = ClientConfig(
    executor_url="http://localhost:8001",
    executor_api_key="your-api-key",
)

# Create Codemode instance
codemode = Codemode.from_client_config(config)

# Execute code
result = codemode.execute("result = 2 + 2")
print(result)  # "4"
```

### Environment Variables

Configure via environment variables for production:

```bash
export CODEMODE_EXECUTOR_URL="http://executor:8001"
export CODEMODE_EXECUTOR_API_KEY="your-api-key"
```

```python
from codemode import Codemode

codemode = Codemode.from_env()
result = codemode.execute("result = 2 + 2")
```

### With CrewAI

```python
from crewai import Agent, Task, Crew
from codemode import Codemode

codemode = Codemode.from_env()
code_tool = codemode.as_crewai_tool()

developer = Agent(
    role="Python Developer",
    goal="Write and execute Python code",
    tools=[code_tool],
    backstory="You are an expert Python developer",
)

task = Task(
    description="Calculate the first 10 Fibonacci numbers",
    agent=developer,
    expected_output="List of first 10 Fibonacci numbers",
)

crew = Crew(agents=[developer], tasks=[task])
result = crew.kickoff()
```

## Architecture

```
+------------------+        gRPC/HTTP         +------------------+
|                  | -----------------------> |                  |
|   Main App       |    Execute Code          |   Executor       |
|   (Client)       | <----------------------- |   Sidecar        |
|                  |    Tool Callbacks        |   (Docker)       |
+------------------+                          +------------------+
```

1. AI agent generates Python code
2. Code executes in isolated executor (no network, read-only FS)
3. When code calls `tools['database'].run()`, gRPC callback to main app
4. Main app executes real tool with full access
5. Result returned to executor, code continues

## Documentation

Full documentation is available in the `docs/` directory:

- [Getting Started](docs/getting-started/installation.md) - Installation and quickstart
- [Configuration](docs/configuration/index.md) - Client and sidecar configuration
- [Architecture](docs/architecture/overview.md) - System design and components
- [Features](docs/features/) - Tools, schemas, and integrations
- [Deployment](docs/deployment/docker.md) - Docker and production deployment
- [API Reference](docs/api-reference/core.md) - Complete API documentation
- [Development](docs/development/contributing.md) - Contributing and testing
- [Migration](docs/migration/v0.2.0.md) - Version migration guides

## Docker Setup

```bash
# Initialize project
codemode init

# Build executor image
codemode docker build

# Start executor container
codemode docker start

# Verify status
codemode docker status
```

### Additional Docker Commands

```bash
# Generate .env file from codemode.yaml (for docker-compose)
codemode docker env --config codemode.yaml --output .env

# Export Docker assets for custom deployment
codemode docker assets --dest ./deploy

# Start with custom configuration
codemode docker start --config custom.yaml --port 8001

# Remove executor container
codemode docker remove
```

### Docker Compose

For multi-container setups:

```bash
# Generate .env from your config
codemode docker env --output .env

# Start with docker-compose
docker-compose --env-file .env -f docker_sidecar/docker-compose.yml up -d
```

See [Deployment Guide](docs/deployment/docker.md) for detailed Docker instructions.

## Security

Codemode implements defense-in-depth security:

- **Container Isolation**: Separate container with no external network access
- **Import Blocking**: Dangerous modules blocked before execution
- **TLS Encryption**: Optional end-to-end encryption with mTLS support
- **Filesystem Protection**: Read-only root filesystem
- **Resource Limits**: CPU, memory, and process limits
- **Code Validation**: Pattern matching for dangerous code

See [Security Model](docs/architecture/security-model.md) for details.

## Contributing

We welcome contributions! Here's the workflow:

1. Fork the repository
2. Create a feature branch from `develop` (`git checkout -b feature/amazing-feature develop`)
3. Make your changes and commit (`git commit -m 'Add amazing feature'`)
4. Push to your fork (`git push origin feature/amazing-feature`)
5. Open a Pull Request against `develop`

### Branch Strategy

- `develop` - Active development branch (submit PRs here)
- `main` - Stable releases
- `release-test` - Triggers Test PyPI publish
- `release` - Triggers PyPI publish

PRs are merged: `feature branch` -> `develop` -> `main` -> `release-test` -> `release`

### Development Setup

```bash
# Clone and setup
git clone https://github.com/mldlwizard/code_mode.git
cd code_mode
git checkout develop
uv sync --extra dev

# Run tests
make test

# Run linting
make lint

# Run E2E tests (requires Docker)
make e2e
```

See [Development Guide](docs/development/contributing.md) for details.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- **GitHub Issues**: [Report bugs](https://github.com/mldlwizard/code_mode/issues)
- **Documentation**: [Full docs](docs/index.md)
