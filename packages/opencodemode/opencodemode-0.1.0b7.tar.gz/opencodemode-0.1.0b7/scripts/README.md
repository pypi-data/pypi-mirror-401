# Scripts

This directory contains utility scripts for the codemode project.

## test_installation.sh

Automated script to test package installation from Test PyPI using multiple methods:
- `pip install`
- `uv pip install`
- `uv add`

### Usage

```bash
bash scripts/test_installation.sh
```

### Requirements

- Python 3.11+
- Internet connection
- Package must be published to Test PyPI first

### What it does

1. Creates isolated test environments
2. Installs the package using different methods
3. Verifies installation by:
   - Checking package metadata
   - Testing Python imports
   - Running CLI commands
4. Cleans up test environments automatically

### When to use

Run this script after:
- Publishing to Test PyPI
- Making changes to package structure
- Before releasing to production PyPI

See [docs/testing-installation.md](../docs/testing-installation.md) for detailed testing instructions.

## E2E Demo (gRPC-only)

This directory contains E2E test scripts for validating the gRPC communication between the main app's ToolService and the executor sidecar.

### Test Suites

1. **SYNC Tools** (`e2e_demo_toolservice.py` + `e2e_demo_driver.py`)
   - Tests synchronous tool execution with thread-pool concurrency
   - Tools: `weather`, `database`, `sleep_ctx` (blocking sleep)
   - Validates sequential vs concurrent execution timing

2. **ASYNC Tools** (`e2e_demo_toolservice_async.py` + `e2e_demo_driver_async.py`)
   - Tests asynchronous tool execution with native async/await
   - Tools: `weather_async`, `database_async`, `sleep_ctx_async` (async sleep)
   - Validates sequential vs concurrent async execution timing

### Automated Testing (Recommended)

Use the `Makefile` targets from the repo root:

```bash
# Run both SYNC and ASYNC test suites (with timing and pass/fail reporting)
make e2e

# Run only SYNC test suite
make e2e-sync

# Run only ASYNC test suite
make e2e-async
```

The `make e2e` target will:
- Build the executor Docker image
- Start the ToolService (sync or async)
- Start the executor sidecar container
- Run the driver tests
- Report timing and pass/fail status for each suite
- Clean up all resources automatically

### Manual Testing

If you prefer to run components separately:

#### SYNC Tools

1) Build sidecar (from repo root):
```bash
docker build -t codemode-executor:0.1.0 -f docker_sidecar/Dockerfile .
```

2) Run sidecar:
```bash
docker run -d \
  --name codemode-executor \
  -p 8001:8001 \
  -e CODEMODE_API_KEY=dev-secret-key \
  -e MAIN_APP_GRPC_TARGET=host.docker.internal:50051 \
  codemode-executor:0.1.0
```

3) In another terminal, start SYNC ToolService:
```bash
CODEMODE_API_KEY=dev-secret-key uv run python scripts/e2e_demo_toolservice.py
```

4) In a third terminal, send code to executor:
```bash
CODEMODE_API_KEY=dev-secret-key uv run python scripts/e2e_demo_driver.py
```

#### ASYNC Tools

Follow the same steps as SYNC, but use:
- `scripts/e2e_demo_toolservice_async.py` for step 3
- `scripts/e2e_demo_driver_async.py` for step 4

### Expected Results

**SYNC Tests:**
- Test 1: Basic weather + database → Success
- Test 2: Sequential sleep (2 × 5s) → ~10s elapsed
- Test 3: Concurrent sleep (2 × 5s) → ~5s elapsed (parallel execution via ThreadPoolExecutor)

**ASYNC Tests:**
- Test 1: Basic async weather + database → Success
- Test 2: Sequential async sleep (2 × 5s) → ~10s elapsed
- Test 3: Concurrent async sleep (2 × 5s) → ~5s elapsed (parallel execution via asyncio.gather)
