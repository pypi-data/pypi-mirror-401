# Installation

This guide covers how to install Codemode and its dependencies.

## Prerequisites

Before installing Codemode, ensure your system meets the following requirements:

- **Python 3.11 or higher** - Codemode uses modern Python features including native union types and improved asyncio support.
- **Docker** - Required to run the secure executor sidecar container.
- **pip or uv** - Python package manager for installation.

### Verifying Prerequisites

Check your Python version:

```bash
python --version  # Should output Python 3.11.x or higher
```

Check Docker is installed and running:

```bash
docker --version
docker info  # Verify Docker daemon is running
```

## Installation Methods

### Standard Installation

Install Codemode from PyPI:

```bash
pip install opencodemode
```

Or using uv (recommended for faster installation):

```bash
uv pip install opencodemode
```

### Installation with Extras

Codemode provides optional extras for framework integrations and development:

#### CrewAI Integration

For use with CrewAI multi-agent framework:

```bash
pip install opencodemode[crewai]
```

#### LangChain Integration

For use with LangChain:

```bash
pip install opencodemode[langchain]
```

#### Development Dependencies

For contributing or running tests:

```bash
pip install opencodemode[dev]
```

#### Multiple Extras

Combine extras as needed:

```bash
pip install opencodemode[crewai,langchain,dev]
```

### Installing from Source

For the latest development version or to contribute:

1. Clone the repository:

```bash
git clone https://github.com/codemode-ai/codemode.git
cd codemode
```

2. Install in development mode:

```bash
# Using pip
pip install -e ".[dev]"

# Using uv (recommended)
uv sync
```

3. Generate TLS certificates for secure communication (optional, for TLS testing):

```bash
make generate-certs
```

## Verifying Installation

After installation, verify Codemode is correctly installed:

### Check Package Version

```bash
python -c "import codemode; print(codemode.__version__)"
```

### Verify Core Imports

```python
from codemode import Codemode
from codemode.config import ClientConfig

print("Codemode installed successfully")
```

### Verify CrewAI Integration (if installed)

```python
from codemode.integrations.crewai import CodemodeCrewAITool

print("CrewAI integration available")
```

## Next Steps

Once installation is complete:

- Follow the [Quickstart Guide](quickstart.md) to run your first code execution.
- Review [Core Concepts](concepts.md) to understand the architecture.
- See the [Configuration Guide](../configuration.md) for advanced setup options.

## Troubleshooting

### Python Version Error

If you see errors about unsupported Python features, verify you are using Python 3.11+:

```bash
python3.11 -m pip install opencodemode
```

### Docker Connection Issues

If Docker commands fail, ensure the Docker daemon is running:

```bash
# Linux
sudo systemctl start docker

# macOS/Windows
# Start Docker Desktop application
```

### Permission Errors

On Linux, you may need to add your user to the docker group:

```bash
sudo usermod -aG docker $USER
# Log out and back in for changes to take effect
```
