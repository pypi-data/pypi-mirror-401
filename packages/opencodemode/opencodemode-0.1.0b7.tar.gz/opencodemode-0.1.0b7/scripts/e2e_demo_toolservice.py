"""
Starts a standalone gRPC ToolService for the executor sidecar to call.
Run in a separate terminal:

  CODEMODE_API_KEY=dev-secret-key uv run python scripts/e2e_demo_toolservice.py

The service exposes:
- ToolService on port 50051 (gRPC)
- Example tools: weather, database
"""

import asyncio
import logging
import os
from pathlib import Path

from codemode import Codemode
from codemode.core.registry import ComponentRegistry
from codemode.grpc import create_tool_server
from codemode.tools.base import ContextAwareTool


# Example tools
class WeatherTool:
    def run(self, location: str) -> str:
        return f"Weather in {location}: 72F"


class DatabaseTool:
    def run(self, query: str) -> str:
        return f"Ran query: {query}"


class SleepContextTool(ContextAwareTool):
    """Context-aware tool that sleeps for 5s and echoes context."""

    def run_with_context(self, context, value: str):
        import time

        time.sleep(5)
        return {"value": value, "context": context}


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
    print("Registering tools: weather, database, sleep_ctx")
    registry.register_tool("weather", WeatherTool())
    registry.register_tool("database", DatabaseTool())
    registry.register_tool("sleep_ctx", SleepContextTool())

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

    # Start gRPC ToolService
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

    print("ToolService running on 0.0.0.0:50051 (gRPC)")
    print(f"API key required: {api_key}")
    print("Press Ctrl+C to stop.")
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down ToolService")
        await server.stop(0)


if __name__ == "__main__":
    asyncio.run(main())
