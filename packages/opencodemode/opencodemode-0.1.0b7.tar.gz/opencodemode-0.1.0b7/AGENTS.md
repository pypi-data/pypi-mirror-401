# Codemode Repository Agent Guide

This repository contains the `codemode` package, a secure code execution framework for multi-agent AI systems.

For comprehensive documentation, see the [docs/](docs/) directory.

## Quick Reference

### Development Commands

```bash
# Setup
uv sync                    # Install dependencies
make generate-certs        # Generate TLS certs for testing

# Verification
make test                  # Run all tests
make lint                  # Run linting
make format                # Format code

# E2E Testing (requires Docker)
make e2e                   # Full E2E suite
make e2e-sync              # Sync tools only
make e2e-async             # Async tools only
make e2e-tls               # TLS enabled

# Docker
make docker-build          # Build executor image
make sidecar               # Run executor container
```

### Code Style

- Python 3.11+
- Formatting: `black` (line length 100)
- Imports: `isort` (profile "black")
- Type hints required, use `|` union syntax
- Google-style docstrings

### Repository Structure

```
codemode/           # Main package
  core/             # Codemode, ExecutorClient, Registry
  config/           # ClientConfig, SidecarConfig
  executor/         # CodeRunner, ExecutorGrpcService
  grpc/             # ToolService server
  tools/            # Tool schemas and meta-tools
  integrations/     # CrewAI integration
docker_sidecar/     # Executor Docker assets
docs/               # Full documentation
tests/              # Unit and integration tests
examples/           # Working examples
```

### Workflow Rules

1. Run `make format` and `make lint` before finishing
2. Run relevant tests (unit first, then E2E if touching core logic)
3. Update docstrings when changing function signatures
4. Never commit secrets

### Branch Strategy & Release Flow
Always make sure you are in a feature/fix branch, and not in any of the branches listed below.

```
feature/* ──► develop ──► main ──► release-test ──► release
                │           │            │              │
                │           │            │              └── Triggers PyPI publish
                │           │            └── Triggers Test PyPI publish
                │           └── Stable releases
                └── Active development (submit PRs here)
```

**Branches:**
- `develop` - Active development, submit PRs here
- `main` - Stable releases
- `release-test` - Triggers Test PyPI publish workflow
- `release` - Triggers PyPI publish workflow

**Release Process:**
1. Merge feature branch → `develop`
2. Merge `develop` → `main`
3. Merge `main` → `release-test` (publishes to Test PyPI)
4. Verify Test PyPI install works
5. Merge `release-test` → `release` (publishes to PyPI)

**PyPI Package:**
- Distribution name: `opencodemode` (what you `pip install`)
- Import name: `codemode` (what you `import` in Python)
- Install: `pip install opencodemode[crewai]`

## Documentation

- [Getting Started](docs/getting-started/installation.md)
- [Configuration](docs/configuration/index.md)
- [Architecture](docs/architecture/overview.md)
- [API Reference](docs/api-reference/core.md)
- [Development](docs/development/contributing.md)
