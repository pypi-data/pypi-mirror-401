# Contributing to Codemode

Thank you for your interest in contributing to Codemode. This guide will help you get started with the development process.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please read it before contributing to ensure a welcoming and inclusive environment for everyone.

## Getting Started

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR_USERNAME/codemode.git
cd codemode
```

3. Add the upstream repository as a remote:

```bash
git remote add upstream https://github.com/mldlwizard/code_mode.git
```

4. Checkout the develop branch:

```bash
git checkout develop
```

### Development Environment Setup

Codemode uses `uv` for dependency management. To set up your development environment:

**Using uv (recommended):**

```bash
uv sync
```

**Using pip:**

```bash
pip install -e ".[dev]"
```

This installs the package in editable mode with all development dependencies.

### Verify Your Setup

Run the test suite to ensure everything is working:

```bash
make test
```

## Code Style

We enforce consistent code style across the project. All contributions must adhere to these standards.

### Formatting

- **Black** for code formatting (line length: 100)
- **isort** for import sorting (profile: black)

Run the formatter before committing:

```bash
make format
```

### Linting

- **Ruff** for linting

Check for issues:

```bash
make lint
```

### Type Hints

Type hints are required for all public functions and methods:

- Use Python 3.10+ union syntax (`str | None` instead of `Optional[str]`)
- Prefer `pathlib.Path` over string paths
- All public APIs must be fully typed

### Docstrings

Use Google-style docstrings for all public classes, methods, and functions:

```python
def execute_code(code: str, timeout: int = 30) -> ExecutionResult:
    """Execute code in a sandboxed environment.

    Args:
        code: The Python code to execute.
        timeout: Maximum execution time in seconds.

    Returns:
        ExecutionResult containing stdout, stderr, and exit code.

    Raises:
        ExecutionTimeoutError: If execution exceeds the timeout.
        SecurityViolationError: If code violates security policies.

    Example:
        >>> result = execute_code("print('hello')")
        >>> print(result.stdout)
        hello
    """
```

## Branching Strategy

We use a structured branch workflow for releases:

### Branch Overview

| Branch | Purpose |
|--------|---------|
| `develop` | Active development branch - submit PRs here |
| `main` | Stable releases |
| `release-test` | Triggers Test PyPI publish |
| `release` | Triggers PyPI publish |

### Merge Flow

PRs follow this path:

```
feature branch -> develop -> main -> release-test -> release
```

1. **feature branch**: Your development work
2. **develop**: All PRs are merged here first
3. **main**: Merged from develop when ready for release
4. **release-test**: Merged from main to test on Test PyPI
5. **release**: Merged from release-test to publish to PyPI

### Branch Naming

Use descriptive branch names with a prefix:

- `feature/` - New features (e.g., `feature/async-executor`)
- `fix/` - Bug fixes (e.g., `fix/timeout-handling`)
- `docs/` - Documentation updates (e.g., `docs/api-reference`)
- `refactor/` - Code refactoring (e.g., `refactor/config-loader`)

### Keeping Your Branch Updated

Regularly sync your branch with upstream develop:

```bash
git fetch upstream
git rebase upstream/develop
```

## Pull Request Process

### Before Submitting

1. Ensure your code follows the style guidelines:

```bash
make format
make lint
```

2. Add or update tests for your changes:

```bash
make test
```

3. Update documentation if you changed public APIs

4. Update `CHANGELOG.md` with a summary of your changes

### Creating a Pull Request

1. Push your branch to your fork:

```bash
git push origin feature/your-feature
```

2. Open a pull request against the `develop` branch

3. Fill out the pull request template with:
   - A clear description of the changes
   - Related issue numbers (if applicable)
   - Testing performed
   - Breaking changes (if any)

### Review Process

- All pull requests require at least one review
- CI checks must pass (tests, linting, formatting)
- Address review feedback promptly
- Squash commits before merging if requested

## Issue Reporting

### Bug Reports

When reporting bugs, include:

- Python version and operating system
- Codemode version (`pip show codemode`)
- Minimal reproducible example
- Expected vs actual behavior
- Full error traceback

### Feature Requests

For feature requests, describe:

- The problem you are trying to solve
- Your proposed solution
- Alternative solutions considered
- Additional context or examples

### Security Issues

For security vulnerabilities, do not open a public issue. Instead, report them privately following the security policy in the repository.

## Development Commands Reference

| Command | Description |
|---------|-------------|
| `make test` | Run the test suite |
| `make lint` | Check code with Ruff |
| `make format` | Format code with Black and isort |
| `make clean` | Remove build artifacts |
| `make docker-build` | Build the executor Docker image |
| `make generate-certs` | Generate TLS certificates for testing |

## Getting Help

If you have questions about contributing:

- Check existing issues and pull requests
- Open a discussion on GitHub
- Review the documentation at [opencode.ai/docs](https://opencode.ai/docs)
