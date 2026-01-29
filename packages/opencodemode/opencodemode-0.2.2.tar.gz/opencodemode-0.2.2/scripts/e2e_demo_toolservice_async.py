"""
Starts a standalone gRPC ToolService with ASYNC tools for the executor sidecar to call.
Run in a separate terminal:

  CODEMODE_API_KEY=dev-secret-key uv run python scripts/e2e_demo_toolservice_async.py

The service exposes:
- ToolService on port 50051 (gRPC)
- Example ASYNC tools: weather_async, database_async, sleep_ctx_async
"""

import asyncio
import logging
import os
from pathlib import Path

from codemode import Codemode
from codemode.core.registry import ComponentRegistry
from codemode.grpc import create_tool_server
from codemode.tools.base import ContextAwareTool


# Example ASYNC tools
class WeatherToolAsync:
    async def run(self, location: str) -> str:
        await asyncio.sleep(0.1)  # Simulate async I/O
        return f"Weather in {location}: 72F (async)"


class DatabaseToolAsync:
    async def run(self, query: str) -> str:
        await asyncio.sleep(0.1)  # Simulate async I/O
        return f"Ran query: {query} (async)"


class SleepContextToolAsync(ContextAwareTool):
    """Context-aware ASYNC tool that sleeps for 5s and echoes context."""

    async def run_with_context(self, context, value: str):
        await asyncio.sleep(5)
        return {"value": value, "context": context, "type": "async"}


async def main() -> None:
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    api_key = os.environ.get("CODEMODE_API_KEY", "dev-secret-key")

    config_path = Path("codemode.yaml")
    if config_path.exists():
        codemode = Codemode.from_config(str(config_path))
        registry = codemode.registry
    else:
        # Minimal inline registry for the demo if no codemode.yaml is present
        registry = ComponentRegistry()
    print("Registering ASYNC tools: weather_async, database_async, sleep_ctx_async")
    registry.register_tool("weather_async", WeatherToolAsync())
    registry.register_tool("database_async", DatabaseToolAsync())
    registry.register_tool("sleep_ctx_async", SleepContextToolAsync())

    # Load TLS config from environment variables
    tls_config = None
    if os.environ.get("CODEMODE_GRPC_TLS_ENABLED", "false").lower() == "true":
        from codemode.config.models import GrpcTlsConfig

        tls_config = GrpcTlsConfig(
            enabled=True,
            mode=os.environ.get("CODEMODE_GRPC_TLS_MODE", "system"),
            cert_file=os.environ.get("CODEMODE_GRPC_TLS_CERT_FILE"),
            key_file=os.environ.get("CODEMODE_GRPC_TLS_KEY_FILE"),
            ca_file=os.environ.get("CODEMODE_GRPC_TLS_CA_FILE"),
            client_cert_file=os.environ.get("CODEMODE_GRPC_TLS_CLIENT_CERT_FILE"),
            client_key_file=os.environ.get("CODEMODE_GRPC_TLS_CLIENT_KEY_FILE"),
        )
        print(f"🔒 TLS enabled (mode: {tls_config.mode})")

    # Start gRPC ToolService with concurrency enabled
    server = create_tool_server(
        registry,
        host="0.0.0.0",
        port=50051,
        api_key=api_key,
        enable_concurrency=True,
        max_workers=4,
        tls_config=tls_config,
    )
    await server.start()

    print("ToolService (ASYNC) running on 0.0.0.0:50051 (gRPC)")
    print(f"API key required: {api_key}")
    print("Press Ctrl+C to stop.")
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down ToolService")
        await server.stop(0)


if __name__ == "__main__":
    asyncio.run(main())
