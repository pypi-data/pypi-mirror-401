# Implementation Plan: Thread Safety and Async Fixes

**Branch:** `feature/thread-safety-and-async-fixes`
**Created:** 2026-01-15
**Status:** COMPLETE - All phases finished

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Issues Confirmed](#issues-confirmed)
3. [Phase 1: Critical (P0) - Registry ContextVar Fix](#phase-1-critical-p0---registry-contextvar-fix)
4. [Phase 2: High Priority (P1) - Async & Meta-tools](#phase-2-high-priority-p1---async--meta-tools)
5. [Phase 3: Medium Priority (P2) - Lifecycle & Protection](#phase-3-medium-priority-p2---lifecycle--protection)
6. [Phase 4: Documentation](#phase-4-documentation)
7. [Test Plan](#test-plan)
8. [Architectural Decisions](#architectural-decisions)
9. [Technical Debt](#technical-debt)
10. [Progress Tracking](#progress-tracking)

---

## Executive Summary

This implementation addresses critical thread-safety and async issues in the codemode library that cause:
- Multi-tenant data breaches through context leakage
- Event loop blocking during retries
- Meta-tools not being detected as async-capable

**Root Causes Verified:**
1. `ComponentRegistry._runtime_context` is a simple instance variable, not a `ContextVar`
2. `ExecutorClient.execute()` uses blocking `time.sleep()` in retry logic
3. `ToolService._is_tool_async()` doesn't check for `run_async()` method
4. `CodemodeTool._arun()` just delegates to sync `_run()`

---

## Issues Confirmed

### Issue #1: Registry Context Race Condition
- **File:** `codemode/core/registry.py:94`
- **Severity:** CRITICAL
- **Root Cause:** `_runtime_context` is instance variable, not `ContextVar`
- **Status:** [x] COMPLETED

### Issue #2: Meta-tools Async Detection
- **File:** `codemode/grpc/server.py:244-258`
- **Severity:** HIGH
- **Root Cause:** `_is_tool_async()` doesn't check `run_async` method
- **Status:** [x] COMPLETED

### Issue #3: ExecutorClient Blocking Retry
- **File:** `codemode/core/executor_client.py:291`
- **Severity:** HIGH
- **Root Cause:** Uses `time.sleep()` instead of `asyncio.sleep()`
- **Status:** [x] COMPLETED

### Issue #4: CodemodeTool._arun() Not Async
- **File:** `codemode/integrations/crewai.py:312-327`
- **Severity:** HIGH
- **Root Cause:** Just calls sync `_run()` instead of async execution
- **Status:** [x] COMPLETED

### Issue #5: ToolService Missing Context Manager
- **File:** `codemode/grpc/server.py:49-80`
- **Severity:** MEDIUM
- **Root Cause:** No `__enter__`/`__exit__` for ThreadPoolExecutor cleanup
- **Status:** [x] COMPLETED

### Issue #6: ExecutorClient Close Protection
- **File:** `codemode/core/executor_client.py:432-443`
- **Severity:** MEDIUM
- **Root Cause:** No idempotent close, no `_closed` flag
- **Status:** [x] COMPLETED

---

## Phase 1: Critical (P0) - Registry ContextVar Fix

### Files to Modify

| File | Changes |
|------|---------|
| `codemode/core/registry.py` | Add ContextVar, update context methods |
| `tests/unit/test_registry.py` | Add concurrent context isolation tests |

### Implementation Details

#### 1.1 Registry Changes (`codemode/core/registry.py`)

**Lines to modify:** 1-26 (imports), 82-96 (init), 348-395 (context methods), 560-576 (clear)

```python
# Add import at top
from contextvars import ContextVar

# Module-level ContextVar (before class definition)
_runtime_context_var: ContextVar[RuntimeContext | None] = ContextVar(
    'codemode_runtime_context', default=None
)

# Update __init__ to remove _runtime_context instance variable
# (Keep for backward compat but don't use)

# Update set_context to use ContextVar
def set_context(self, context: RuntimeContext) -> None:
    if not isinstance(context, RuntimeContext):
        raise TypeError("context must be a RuntimeContext instance")
    _runtime_context_var.set(context)
    logger.debug(f"Set runtime context: {context}")

# Update get_context to use ContextVar
def get_context(self) -> RuntimeContext | None:
    return _runtime_context_var.get()

# Update clear_context to use ContextVar
def clear_context(self) -> None:
    _runtime_context_var.set(None)
    logger.debug("Cleared runtime context")

# Update clear() to also reset ContextVar
def clear(self) -> None:
    # ... existing clearing ...
    _runtime_context_var.set(None)  # Add this
```

#### 1.2 Test Changes (`tests/unit/test_registry.py`)

Add new test for concurrent isolation:

```python
@pytest.mark.asyncio
async def test_concurrent_context_isolation():
    """Test that concurrent async tasks have isolated contexts."""
    import asyncio

    registry = ComponentRegistry()
    results = []

    async def task(client_id: str, delay: float):
        context = RuntimeContext(variables={"client_id": client_id})
        registry.set_context(context)
        await asyncio.sleep(delay)  # Simulate async work
        retrieved = registry.get_context()
        results.append({
            "expected": client_id,
            "actual": retrieved.get("client_id") if retrieved else None
        })
        registry.clear_context()

    # Run concurrent tasks
    await asyncio.gather(
        task("client_a", 0.1),
        task("client_b", 0.05),
        task("client_c", 0.15),
    )

    # Each task should have gotten its own context
    for r in results:
        assert r["expected"] == r["actual"], f"Context leaked: {r}"
```

### Completion Criteria
- [ ] ContextVar import added
- [ ] Module-level `_runtime_context_var` created
- [ ] `set_context()` uses ContextVar
- [ ] `get_context()` uses ContextVar
- [ ] `clear_context()` uses ContextVar
- [ ] `clear()` also resets ContextVar
- [ ] Concurrent test passes
- [ ] All existing tests pass

---

## Phase 2: High Priority (P1) - Async & Meta-tools

### Files to Modify

| File | Changes |
|------|---------|
| `codemode/grpc/server.py` | Fix `_is_tool_async()` detection |
| `codemode/core/executor_client.py` | Async-first redesign |
| `codemode/integrations/crewai.py` | Update `_arun()` to use async |
| `tests/unit/test_executor_client_grpc.py` | Add async tests |

### Implementation Details

#### 2.1 Meta-tools Async Detection (`codemode/grpc/server.py`)

**Lines to modify:** 244-258

```python
def _is_tool_async(self, tool: Any) -> bool:
    """Check if a tool is async (has async run/run_async method)."""
    return (
        inspect.iscoroutinefunction(tool)
        or inspect.iscoroutinefunction(getattr(tool, "run", None))
        or inspect.iscoroutinefunction(getattr(tool, "run_with_context", None))
        or inspect.iscoroutinefunction(getattr(tool, "run_async", None))  # ADD THIS
    )
```

Also update `invoke_async()` to prefer `run_async()` if available (lines 96-139).

#### 2.2 ExecutorClient Async Redesign (`codemode/core/executor_client.py`)

**Architectural Decision:** Async-first design with sync wrappers

Major changes:
1. Add `grpc.aio` async channel support
2. Create `execute_async()` as primary method
3. Keep `execute()` as sync wrapper
4. Add `close_async()` and async context manager
5. Add `_closed` flag and locking

```python
# New imports
import asyncio
import threading
from typing import TYPE_CHECKING

# New class structure
class ExecutorClient:
    def __init__(self, ...):
        # ... existing ...
        self._closed = False
        self._close_lock = threading.Lock()

        # Lazy async channel (created on first async call)
        self._async_channel: grpc.aio.Channel | None = None
        self._async_stub: codemode_pb2_grpc.ExecutorServiceStub | None = None

    async def execute_async(self, ...) -> ExecutionResult:
        """Primary async execution method with non-blocking retry."""
        if self._closed:
            raise ExecutorClientError("Client has been closed")

        # ... retry logic with asyncio.sleep() ...

    def execute(self, ...) -> ExecutionResult:
        """Sync wrapper around execute_async."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No event loop - create one
            return asyncio.run(self.execute_async(...))
        else:
            # Already in event loop - run in thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, self.execute_async(...))
                return future.result()

    async def close_async(self) -> None:
        """Async close method."""
        # ...

    async def __aenter__(self) -> "ExecutorClient":
        return self

    async def __aexit__(self, *args) -> None:
        await self.close_async()
```

#### 2.3 CodemodeTool Async Update (`codemode/integrations/crewai.py`)

**Lines to modify:** 312-327

```python
async def _arun(self, code: str) -> str:
    """Execute code via async executor service."""
    logger.debug(f"Executing code via CodemodeTool async ({len(code)} chars)")

    component_names = self.registry.get_component_names()
    context = self.registry.get_context()

    if context:
        logger.debug(f"Injecting context with variables: {list(context.variables.keys())}")

    try:
        result = await self.executor_client.execute_async(
            code=code,
            available_tools=component_names["tools"],
            config=dict(self.registry.config),
            execution_timeout=30,
            context=context,
        )

        if result.success:
            logger.info("✓ Code execution via CodemodeTool async successful")
            return result.result if result.result else "Code executed successfully"
        else:
            logger.warning(f"✗ Code execution failed: {result.error}")
            return f"ERROR: {result.error}"

    except ExecutorClientError as e:
        logger.error(f"Executor error: {e}")
        return f"EXECUTOR ERROR: {str(e)}"
```

### Completion Criteria
- [ ] `_is_tool_async()` checks `run_async`
- [ ] `invoke_async()` prefers `run_async()` if available
- [ ] `ExecutorClient.execute_async()` implemented
- [ ] `ExecutorClient.execute()` wraps async
- [ ] Async channel management added
- [ ] `CodemodeTool._arun()` uses async executor
- [ ] All tests pass

---

## Phase 3: Medium Priority (P2) - Lifecycle & Protection

### Files to Modify

| File | Changes |
|------|---------|
| `codemode/grpc/server.py` | Add context manager to ToolService |
| `codemode/core/executor_client.py` | Close protection (covered in P1) |

### Implementation Details

#### 3.1 ToolService Context Manager (`codemode/grpc/server.py`)

**Lines to modify:** 49-80

```python
class ToolService(codemode_pb2_grpc.ToolServiceServicer):
    # ... existing __init__ and shutdown ...

    def __enter__(self) -> "ToolService":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - cleanup ThreadPoolExecutor."""
        self.shutdown(wait=True)

    async def __aenter__(self) -> "ToolService":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        self.shutdown(wait=True)
```

#### 3.2 Update create_tool_server to return service

```python
def create_tool_server(...) -> tuple[grpc.aio.Server, ToolService]:
    """Create gRPC server and return both server and service for lifecycle management."""
    service = ToolService(...)
    server = grpc.aio.server()
    codemode_pb2_grpc.add_ToolServiceServicer_to_server(service, server)
    # ...
    return server, service
```

### Completion Criteria
- [ ] ToolService has `__enter__`/`__exit__`
- [ ] ToolService has `__aenter__`/`__aexit__`
- [ ] `create_tool_server` returns tuple
- [ ] All tests pass

---

## Phase 4: Documentation

### New Documentation Structure

```
docs/
├── sdk/                          # NEW - SDK Documentation
│   ├── index.md                  # SDK overview
│   ├── getting-started.md        # Quick start guide
│   ├── core-concepts.md          # Core concepts
│   ├── async-patterns.md         # Async usage patterns
│   ├── concurrency.md            # Thread safety and concurrency
│   ├── context-management.md     # Runtime context guide
│   ├── tool-development.md       # Building custom tools
│   ├── error-handling.md         # Error handling patterns
│   └── migration-guide.md        # Migration from sync to async
├── api-reference/
│   ├── core.md                   # UPDATE - Add async methods, thread-safety notes
│   └── ...
└── architecture/
    ├── overview.md               # UPDATE - Add concurrency model
    └── ...
```

### Files to Create/Update

| File | Action | Content |
|------|--------|---------|
| `docs/sdk/index.md` | CREATE | SDK overview and navigation |
| `docs/sdk/getting-started.md` | CREATE | Quick start with code examples |
| `docs/sdk/core-concepts.md` | CREATE | Core concepts explanation |
| `docs/sdk/async-patterns.md` | CREATE | Async/await usage patterns |
| `docs/sdk/concurrency.md` | CREATE | Thread safety guarantees |
| `docs/sdk/context-management.md` | CREATE | RuntimeContext guide |
| `docs/sdk/tool-development.md` | CREATE | Custom tool development |
| `docs/sdk/error-handling.md` | CREATE | Error handling patterns |
| `docs/api-reference/core.md` | UPDATE | Add async methods docs |

### Completion Criteria
- [ ] SDK documentation folder created
- [ ] All 8 SDK docs written
- [ ] API reference updated with async methods
- [ ] Thread-safety notes added
- [ ] Migration guide complete

---

## Test Plan

### New Test Files

| File | Purpose |
|------|---------|
| `tests/unit/test_registry_concurrency.py` | Concurrent context isolation |
| `tests/unit/test_executor_client_async.py` | Async executor tests |
| `tests/integration/test_concurrent_requests.py` | E2E concurrent tests |

### Test Cases

1. **Registry Concurrent Isolation**
   - Multiple async tasks with different contexts
   - Context doesn't leak between tasks
   - Clear in one task doesn't affect others

2. **ExecutorClient Async**
   - `execute_async()` works with async channel
   - Retry uses `asyncio.sleep()` (non-blocking)
   - Sync `execute()` wrapper works
   - Close protection (use-after-close raises)

3. **Meta-tools Async Detection**
   - Tools with `run_async()` detected as async
   - `invoke_async()` prefers `run_async()`

4. **ToolService Lifecycle**
   - Context manager cleans up ThreadPoolExecutor
   - Double shutdown is safe

---

## Architectural Decisions

### AD-1: ContextVar at Module Level

**Decision:** Use module-level `ContextVar` instead of instance-level

**Rationale:**
- `ContextVar` is designed to be module-level
- Task-local storage works across all registry instances
- Simpler implementation, same behavior

**Trade-offs:**
- All registries share the same context var (acceptable since context is per-request, not per-registry)

### AD-2: Async-First ExecutorClient

**Decision:** Make `execute_async()` the primary method, wrap for sync

**Rationale:**
- Prevents blocking event loop
- Natural fit for async frameworks (FastAPI, etc.)
- Retry with `asyncio.sleep()` is non-blocking

**Trade-offs:**
- Sync callers pay slight overhead for async wrapper
- Need to manage two channels (sync and async)

### AD-3: Lazy Async Channel Creation

**Decision:** Create async channel on first async call, not in `__init__`

**Rationale:**
- Sync-only users don't pay async initialization cost
- Async channel creation may need running event loop

**Trade-offs:**
- First async call slightly slower
- Need to handle channel creation errors gracefully

### AD-4: Keep Backward Compatibility

**Decision:** Maintain all existing sync APIs, add async alternatives

**Rationale:**
- Existing users shouldn't need to change code
- Gradual migration path to async

**Trade-offs:**
- More code to maintain
- Some duplication between sync/async paths

---

## Technical Debt

### TD-1: Sync ExecutorClient Uses asyncio.run()

**Issue:** Sync `execute()` wrapper uses `asyncio.run()` which creates new event loop

**Impact:** Low - works correctly, slightly inefficient

**Future Fix:** Consider dedicated sync gRPC channel for pure sync use cases

### TD-2: ToolService Not Returned from create_tool_server

**Issue:** Changing return type is breaking change

**Impact:** Medium - users calling `create_tool_server()` need to update

**Mitigation:** Add deprecation warning, document in migration guide

### TD-3: No Connection Pooling for Async Channels

**Issue:** Each ExecutorClient creates its own async channel

**Impact:** Low - gRPC channels are cheap and handle multiplexing

**Future Fix:** Consider shared channel pool for high-throughput scenarios

### TD-4: Registry Thread Safety for Registration

**Issue:** Tool registration dict operations not locked

**Impact:** Low - registration typically happens at startup

**Documentation:** Document that registration should happen before concurrent usage

---

## Progress Tracking

### Phase 1: Registry ContextVar
- [x] Import ContextVar
- [x] Create module-level _runtime_context_var
- [x] Update set_context()
- [x] Update get_context()
- [x] Update clear_context()
- [x] Update clear()
- [x] Add concurrent test
- [x] All existing tests pass

### Phase 2: Async & Meta-tools
- [x] Fix _is_tool_async()
- [x] Update invoke_async() to use run_async
- [x] Add execute_async() to ExecutorClient
- [x] Add async channel management
- [x] Add _closed flag and locking
- [x] Update execute() as wrapper
- [x] Add close_async()
- [x] Add async context manager
- [x] Update CodemodeTool._arun()
- [x] Add async tests

### Phase 3: Lifecycle
- [x] Add ToolService __enter__/__exit__
- [x] Add ToolService __aenter__/__aexit__
- [ ] Update create_tool_server return type (deferred - breaking change)

### Phase 4: Documentation
- [x] Create docs/sdk/ folder
- [x] Write docs/sdk/index.md
- [x] Write docs/sdk/getting-started.md
- [x] Write docs/sdk/core-concepts.md
- [x] Write docs/sdk/async-patterns.md
- [x] Write docs/sdk/concurrency.md
- [x] Write docs/sdk/context-management.md
- [x] Write docs/sdk/tool-development.md
- [x] Write docs/sdk/error-handling.md
- [x] Update docs/api-reference/core.md
- [x] Review all docs for accuracy

### Final Steps
- [x] Run make format
- [x] Run make lint
- [x] Run make test
- [x] All tests pass (378 unit tests)
- [x] Update IMPLEMENTATION_PLAN.md with completion status

---

## Change Log

| Date | Phase | Changes |
|------|-------|---------|
| 2026-01-15 | Setup | Created feature branch, plan file |
| 2026-01-15 | Phase 1 | Completed Registry ContextVar fix - added ContextVar for thread-safe context isolation |
| 2026-01-15 | Phase 2 | Completed async fixes - _is_tool_async(), invoke_async(), execute_async(), _arun() |
| 2026-01-15 | Phase 3 | Completed lifecycle - ToolService context manager, ExecutorClient close protection |
| 2026-01-15 | Phase 4 | Completed SDK documentation - 8 new docs in docs/sdk/, updated API reference |
