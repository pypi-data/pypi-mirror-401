# Testing Guide

This guide covers how to run and write tests for Codemode.

## Test Structure

Tests are organized in the `tests/` directory:

```
tests/
├── __init__.py
└── unit/
    ├── __init__.py
    ├── test_codemode.py
    ├── test_config_loader.py
    ├── test_config_models.py
    ├── test_context.py
    ├── test_executor_client_grpc.py
    ├── test_executor_runner.py
    ├── test_executor_security.py
    ├── test_integrations_crewai.py
    ├── test_registry.py
    └── ...
```

- **Unit tests** (`tests/unit/`): Fast, isolated tests with mocked dependencies
- **E2E tests**: Integration tests requiring Docker and running services

## Running Tests

### Run All Tests

```bash
make test
```

Or using pytest directly:

```bash
uv run pytest tests/
```

### Run a Single Test

To run a specific test file:

```bash
uv run pytest tests/unit/test_codemode.py -v
```

To run a specific test class:

```bash
uv run pytest tests/unit/test_codemode.py::TestCodemodeClass -v
```

To run a specific test method:

```bash
uv run pytest tests/unit/test_codemode.py::TestCodemodeClass::test_method_name -v
```

### Run Tests with Output

Show print statements and logging:

```bash
uv run pytest tests/ -v -s
```

### Run Tests Matching a Pattern

```bash
uv run pytest tests/ -k "config" -v
```

## End-to-End Testing

E2E tests validate the full system including Docker containers and gRPC communication.

### Prerequisites

- Docker installed and running
- TLS certificates generated (for TLS tests)

### Generate TLS Certificates

Required before running TLS-enabled tests:

```bash
make generate-certs
```

### Run E2E Tests

Run the complete E2E test suite:

```bash
make e2e
```

This runs sync tests, async tests, and cleans up resources.

### E2E Test Variants

| Command | Description |
|---------|-------------|
| `make e2e-sync` | Run synchronous tool tests |
| `make e2e-async` | Run asynchronous tool tests |
| `make e2e-tls` | Run tests with TLS encryption enabled |
| `make e2e` | Run full E2E suite (sync + async + cleanup) |

### Manual E2E Drivers

For interactive testing and debugging:

```bash
# Synchronous driver
make driver

# Asynchronous driver
make driver-async
```

### Starting Services Manually

To run services for manual testing:

```bash
# Build and start the executor sidecar
make docker-build
make sidecar

# Start the tool service
make toolservice        # Sync version
make toolservice-async  # Async version
```

## Coverage Reports

Generate a coverage report:

```bash
uv run pytest tests/ --cov=codemode --cov-report=html
```

View the report by opening `htmlcov/index.html` in a browser.

For terminal output:

```bash
uv run pytest tests/ --cov=codemode --cov-report=term-missing
```

## Writing Tests

### Test File Naming

- Test files must be named `test_*.py`
- Test classes must be named `Test*`
- Test methods must be named `test_*`

### Using Pytest Fixtures

Fixtures provide reusable test setup:

```python
import pytest
from codemode.config import ConfigLoader

@pytest.fixture
def config_loader():
    """Provide a configured ConfigLoader instance."""
    return ConfigLoader()

@pytest.fixture
def sample_config(tmp_path):
    """Create a temporary config file."""
    config_file = tmp_path / "codemode.yaml"
    config_file.write_text("""
    executor:
      timeout: 30
      max_memory: "512m"
    """)
    return config_file

def test_load_config(config_loader, sample_config):
    """Test loading configuration from file."""
    config = config_loader.load(sample_config)
    assert config.executor.timeout == 30
```

### Mocking External Services

Use `unittest.mock` to isolate tests from external dependencies:

```python
from unittest.mock import Mock, patch, AsyncMock

def test_executor_client_connection():
    """Test executor client handles connection errors."""
    with patch("codemode.core.executor_client.grpc.insecure_channel") as mock_channel:
        mock_channel.side_effect = ConnectionError("Failed to connect")

        client = ExecutorClient(host="localhost", port=50051)

        with pytest.raises(ConnectionError):
            client.connect()

async def test_async_execution():
    """Test async code execution."""
    mock_stub = AsyncMock()
    mock_stub.Execute.return_value = ExecutionResponse(
        stdout="hello",
        stderr="",
        exit_code=0
    )

    with patch("codemode.core.executor_client.get_stub", return_value=mock_stub):
        result = await execute_async("print('hello')")
        assert result.stdout == "hello"
```

### Testing Async Code

Use `pytest-asyncio` for async tests:

```python
import pytest

@pytest.mark.asyncio
async def test_async_executor():
    """Test async executor functionality."""
    async with AsyncExecutor() as executor:
        result = await executor.run("print('test')")
        assert result.exit_code == 0
```

### Test Categories with Markers

Mark tests for selective execution:

```python
import pytest

@pytest.mark.slow
def test_large_file_processing():
    """Test that takes significant time."""
    pass

@pytest.mark.integration
def test_docker_executor():
    """Test requiring Docker."""
    pass
```

Run specific categories:

```bash
uv run pytest -m "not slow" tests/
uv run pytest -m integration tests/
```

## TLS Testing

TLS tests validate secure communication between components.

### Setup

1. Generate test certificates:

```bash
make generate-certs
```

2. Certificates are created in the configured directory (typically `certs/`)

### Running TLS Tests

```bash
make e2e-tls
```

### Writing TLS Tests

```python
import pytest
from pathlib import Path

@pytest.fixture
def tls_config():
    """Provide TLS configuration for tests."""
    cert_dir = Path("certs")
    return {
        "ca_cert": cert_dir / "ca.crt",
        "client_cert": cert_dir / "client.crt",
        "client_key": cert_dir / "client.key",
    }

def test_secure_connection(tls_config):
    """Test executor connection with TLS."""
    client = ExecutorClient(
        host="localhost",
        port=50051,
        tls_enabled=True,
        **tls_config
    )
    assert client.is_secure
```

## Troubleshooting

### Tests Failing Locally But Passing in CI

- Ensure you have the latest dependencies: `uv sync`
- Check Python version matches CI (3.11+)
- Verify Docker is running for E2E tests

### Slow Tests

- Use mocking to avoid network calls
- Use `pytest-xdist` for parallel execution: `uv run pytest -n auto tests/`

### Debugging Test Failures

```bash
# Drop into debugger on failure
uv run pytest tests/ --pdb

# Show local variables in tracebacks
uv run pytest tests/ --showlocals
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `make test` | Run all unit tests |
| `make e2e` | Run full E2E test suite |
| `make e2e-sync` | Run sync E2E tests |
| `make e2e-async` | Run async E2E tests |
| `make e2e-tls` | Run TLS E2E tests |
| `make generate-certs` | Generate TLS test certificates |
| `make docker-build` | Build executor Docker image |
| `make sidecar` | Start executor sidecar container |
| `make clean` | Remove build artifacts and containers |
