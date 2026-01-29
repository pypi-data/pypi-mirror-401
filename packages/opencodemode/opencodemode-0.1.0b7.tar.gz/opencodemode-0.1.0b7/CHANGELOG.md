# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Version scheme**: Moved to beta versioning (`0.1.0b{build_number}`) for both PyPI and Test PyPI
- **CodemodeTool `_run()` method**: Changed from async to sync, using sync gRPC channel for thread safety
- **CodemodeTool `_arun()` method**: Now a full async implementation (not delegating to `_run`)

### Fixed
- **Event loop closure errors**: Fixed `RuntimeError: Event loop is closed` when using CrewAI's `kickoff_async()` with concurrent FastAPI users
  - Root cause: gRPC async channels were cached at instance level but bound to specific event loops
  - Solution 1: `ExecutorClient` now uses per-event-loop channel cache with `WeakKeyDictionary`
  - Solution 2: `CodemodeTool._run()` uses sync gRPC (thread-safe, no event loop binding)

### Added
- **Thread safety documentation**: Added comprehensive docstring to `CodemodeTool._run()` explaining `ContextVar` propagation behavior with `asyncio.to_thread()` vs manual threading

## [0.2.2] - 2026-01-15

### Changed
- **CodemodeTool Description**: Completely rewritten tool description with clean XML-tagged format
  - `<META_TOOLS>`: Meta-tool discovery (`__list__`, `__schema__`)
  - `<EXECUTION_PATTERN>`: Async pattern with sequential, parallel, and chaining examples
  - `<RULES>`: Essential constraints (result variable, async tools, forbidden operations)
  - `<ERROR_HANDLING>`: Simple try-except pattern
- Reduced description from ~100 lines to ~50 focused lines

### Removed
- `DEFAULT_CODEMODE_PATTERNS` constant (unnecessary complexity)
- `get_default_description()` helper function (unused)

### Fixed
- **CodemodeTool async handling**: Both `_run()` and `_arun()` are now properly async
- **Error formatting**: Added `_format_error()` method with comprehensive error info including:
  - Error type and message
  - Traceback (limited frames)
  - Stderr output
  - Correlation ID for tracing
  - Execution duration

## [0.2.1] - 2026-01-14

### Fixed
- Dockerfile base image path correction for executor sidecar

## [0.2.0] - 2026-01-09

### Added
- **Configuration Separation**: New `ClientConfig` and `SidecarConfig` models for cleaner separation between client applications and executor sidecars
- **Environment Variable Support**: Full configuration via environment variables for production deployments
  - Client: `CODEMODE_EXECUTOR_URL`, `CODEMODE_EXECUTOR_API_KEY`, `CODEMODE_RETRY_*`, `CODEMODE_TLS_*`
  - Sidecar: `CODEMODE_SIDECAR_PORT`, `CODEMODE_API_KEY`, `CODEMODE_CODE_TIMEOUT`, etc.
- **Retry Logic**: Automatic retries with exponential backoff and jitter for transient failures
  - Configurable via `RetryConfig`: `enabled`, `max_attempts`, `backoff_base_ms`, `backoff_max_ms`
- **Correlation IDs**: End-to-end request tracing across the distributed system
  - Automatic generation with configurable prefix
  - Propagation via gRPC metadata
- **Structured Errors**: New `ExecutionError` model with detailed error information
  - Error type classification (syntax, runtime, timeout, security)
  - Traceback frames with configurable limit
  - Line number extraction for debugging
- **Tool Schema Support**: Input/output schema definitions for tools
  - `ToolRegistration` class for schema-aware tool registration
  - Meta-tools: `__list__` and `__schema__` for tool discovery
  - Pydantic model to JSON schema conversion
- **New Factory Methods**:
  - `Codemode.from_client_config()` for new-style configuration
  - `Codemode.from_env()` for environment-only configuration
- **Enhanced ExecutionResult**: New fields `error_details`, `correlation_id`, `duration_ms`
- **Production Docker Configuration**: Updated Dockerfile and docker-compose.yml with security hardening
- **Comprehensive Documentation**: New documentation structure with mkdocs integration

### Changed
- **ExecutorClient**: Complete rewrite with retry logic and correlation ID support
- **Docker Sidecar**: Now installs from PyPI instead of requiring local source
- **ConfigLoader**: Extended with `load_client_config()` and `load_sidecar_config()` methods
- **CLI**: New `init client` and `init sidecar` commands for generating configuration files

### Fixed
- **gRPC Server**: Fixed `_struct_to_dict` bug that caused nested object serialization issues
- **Tool Registration**: Schema information now properly included in ListTools response

### Documentation
- Added full documentation structure under `docs/`:
  - Getting Started: installation, quickstart, concepts
  - Configuration: client-config, sidecar-config, environment-variables
  - Architecture: overview, components, security-model
  - Features: tools, schemas, crewai-integration, hybrid-execution
  - Deployment: docker, docker-compose, production
  - API Reference: core, executor, config, grpc
  - Development: contributing, testing, releasing
  - Migration: v0.2.0 migration guide
- Updated README.md to be more concise with references to full documentation
- Updated AGENTS.md with simplified quick reference

### Migration
See [Migration Guide](docs/migration/v0.2.0.md) for upgrading from v0.1.x.

## [0.1.0] - 2025-12-09

### Changed
- Switched executor/main bridge to gRPC-only (HTTP RPC removed).
- Docker sidecar isolated to `docker_sidecar/` bundle; export via `codemode docker assets`.
- Updated docs/examples to gRPC-only flow; executor image tag guidance `codemode-executor:0.1.0`.
- Bumped package version to 0.1.0.

### Fixed
- Regenerated protobuf handling to avoid runtime parse errors with current protobuf versions.

## [0.0.8] - 2025-11-17

### Fixed
- Pydantic deprecation warnings - migrated from `class Config` to `ConfigDict` (#9)
- Test PyPI workflow now auto-bumps version to prevent upload conflicts (#9)

### Changed
- Updated to Pydantic v2 modern configuration syntax
- Test PyPI uploads now use `.dev<run_number>` suffix for unique versions

[Unreleased]: https://github.com/mldlwizard/code_mode/compare/v0.2.2...HEAD
[0.2.2]: https://github.com/mldlwizard/code_mode/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/mldlwizard/code_mode/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/mldlwizard/code_mode/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/mldlwizard/code_mode/compare/v0.0.8...v0.1.0
[0.0.8]: https://github.com/mldlwizard/code_mode/releases/tag/v0.0.8
