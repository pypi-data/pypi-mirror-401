"""
ToolService gRPC server for main app (handles tool calls from executor).
"""

import asyncio
import inspect
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, Any

import grpc
from google.protobuf.json_format import MessageToDict
from google.protobuf.struct_pb2 import Struct

from codemode.core.registry import ComponentNotFoundError, ComponentRegistry
from codemode.protos import codemode_pb2, codemode_pb2_grpc
from codemode.tools.schema import schema_to_json_string

if TYPE_CHECKING:
    from codemode.config.models import GrpcTlsConfig

logger = logging.getLogger(__name__)


def _dict_to_struct(data: dict[str, Any] | None) -> Struct:
    struct = Struct()
    if data:
        struct.update(data)
    return struct


def _struct_to_dict(struct: Struct | None) -> dict[str, Any]:
    """
    Convert a protobuf Struct to a Python dictionary recursively.

    Uses MessageToDict for proper deep conversion of nested structures.

    Args:
        struct: Protobuf Struct message or None.

    Returns:
        Python dictionary with all nested structures properly converted.
    """
    if not struct:
        return {}
    return MessageToDict(struct, preserving_proto_field_name=True)


class ToolService(codemode_pb2_grpc.ToolServiceServicer):
    def __init__(
        self,
        registry: ComponentRegistry,
        api_key: str | None = None,
        enable_concurrency: bool = False,
        max_workers: int | None = None,
    ) -> None:
        self.registry = registry
        self.api_key = api_key
        self.enable_concurrency = enable_concurrency
        self._executor: ThreadPoolExecutor | None = (
            ThreadPoolExecutor(max_workers=max_workers) if enable_concurrency else None
        )

    def shutdown(self, wait: bool = True) -> None:
        """
        Shutdown the thread pool executor if it exists.

        Args:
            wait: If True, wait for pending tasks to complete before shutting down.
        """
        if self._executor:
            self._executor.shutdown(wait=wait)

    def __del__(self) -> None:
        """Cleanup thread pool executor on deletion (fallback)."""
        try:
            self.shutdown(wait=False)
        except Exception:  # Broad catch OK: __del__ must not raise exceptions
            # Ignore errors during cleanup
            pass

    def __enter__(self) -> "ToolService":
        """
        Context manager entry.

        Returns:
            The ToolService instance.

        Example:
            >>> with ToolService(registry) as service:
            ...     # use service
            ...     pass
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context manager exit - cleanup ThreadPoolExecutor.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        self.shutdown(wait=True)

    async def __aenter__(self) -> "ToolService":
        """
        Async context manager entry.

        Returns:
            The ToolService instance.

        Example:
            >>> async with ToolService(registry) as service:
            ...     # use service
            ...     pass
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Async context manager exit - cleanup ThreadPoolExecutor.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        self.shutdown(wait=True)

    async def CallTool(self, request, context):  # noqa: N802 gRPC naming
        if self.api_key:
            metadata = dict(context.invocation_metadata())
            if metadata.get("authorization") != f"Bearer {self.api_key}":
                context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid API key")

        tool_name = request.tool_name
        arguments = _struct_to_dict(request.arguments)
        ctx_dict = _struct_to_dict(request.context) if request.HasField("context") else None

        async def _handle() -> codemode_pb2.ToolCallResponse:
            try:
                tool = self.registry.get_tool(tool_name)

                async def invoke_async():
                    """Invoke tool, awaiting coroutines; run blocking calls in a thread.

                    Prefers async methods in this order:
                    1. run_async() - explicit async method (meta-tools pattern)
                    2. run_with_context() - context-aware method
                    3. run() - standard method
                    4. _run() - internal method (CrewAI pattern)
                    5. __call__() - callable tool
                    """

                    def call_target():
                        # Returns either a value or a coroutine
                        if hasattr(tool, "run_with_context") and ctx_dict is not None:
                            return tool.run_with_context(ctx_dict, **arguments)
                        if hasattr(tool, "run"):
                            sig = inspect.signature(tool.run)
                            if "context" in sig.parameters and ctx_dict is not None:
                                return tool.run(context=ctx_dict, **arguments)
                            return tool.run(**arguments)
                        if hasattr(tool, "_run"):
                            sig = inspect.signature(tool._run)
                            if "context" in sig.parameters and ctx_dict is not None:
                                return tool._run(context=ctx_dict, **arguments)
                            return tool._run(**arguments)
                        if callable(tool):
                            sig = inspect.signature(tool)
                            if "context" in sig.parameters and ctx_dict is not None:
                                return tool(context=ctx_dict, **arguments)
                            return tool(**arguments)
                        raise ValueError(f"Tool '{tool_name}' is not callable")

                    async def call_target_async():
                        """Async version that prefers run_async() method."""
                        # Prefer run_async() for meta-tools pattern
                        if hasattr(tool, "run_async"):
                            run_async_method = tool.run_async
                            if inspect.iscoroutinefunction(run_async_method):
                                return await run_async_method(**arguments)
                        # Fall back to run_with_context if async
                        if hasattr(tool, "run_with_context") and ctx_dict is not None:
                            return await tool.run_with_context(ctx_dict, **arguments)
                        # Fall back to run() if async
                        if hasattr(tool, "run"):
                            sig = inspect.signature(tool.run)
                            if "context" in sig.parameters and ctx_dict is not None:
                                return await tool.run(context=ctx_dict, **arguments)
                            return await tool.run(**arguments)
                        # Fall back to callable
                        if callable(tool):
                            sig = inspect.signature(tool)
                            if "context" in sig.parameters and ctx_dict is not None:
                                return await tool(context=ctx_dict, **arguments)
                            return await tool(**arguments)
                        raise ValueError(f"Tool '{tool_name}' is not callable")

                    # Check if tool has any async method (including run_async)
                    is_async = (
                        inspect.iscoroutinefunction(tool)
                        or inspect.iscoroutinefunction(getattr(tool, "run", None))
                        or inspect.iscoroutinefunction(getattr(tool, "run_with_context", None))
                        or inspect.iscoroutinefunction(getattr(tool, "run_async", None))
                    )

                    # Async tool functions: use async call path
                    if is_async:
                        return await call_target_async()

                    # For sync tools, offload the CALL itself to avoid blocking event loop
                    if self.enable_concurrency and self._executor:
                        loop = asyncio.get_running_loop()
                        result = await loop.run_in_executor(self._executor, call_target)
                    else:
                        result = await asyncio.to_thread(call_target)

                    # Handle case where sync tool dynamically returned a coroutine
                    if inspect.iscoroutine(result):
                        result = await result

                    return result

                result = await invoke_async()

                payload = result if isinstance(result, dict) else {"value": result}
                return codemode_pb2.ToolCallResponse(
                    success=True,
                    result=_dict_to_struct(payload),
                )
            except ComponentNotFoundError as e:
                return codemode_pb2.ToolCallResponse(success=False, error=str(e))
            except Exception as e:  # Broad catch OK: catch all tool errors for safe response
                logger.error("Tool '%s' execution failed: %s", tool_name, e)
                return codemode_pb2.ToolCallResponse(success=False, error=str(e))

        return await _handle()

    async def ListTools(self, request, context):  # noqa: N802 gRPC naming
        """
        List all available tools with metadata and schemas.

        Returns tool information including:
        - name: Tool identifier
        - is_async: Whether tool.run() is async
        - has_context: Whether tool supports run_with_context()
        - description: Human-readable description
        - input_schema: JSON Schema for input parameters
        - output_schema: JSON Schema for return type
        """
        tool_infos = []
        for name, registration in self.registry.get_tool_registrations().items():
            tool = registration.tool

            # Determine if tool is async
            is_async = self._is_tool_async(tool)

            # Check for context support
            has_context = hasattr(tool, "run_with_context")

            # Get description from registration (already extracted)
            description = registration.description or ""

            # Serialize schemas to JSON strings
            input_schema_json = ""
            output_schema_json = ""
            if registration.input_schema:
                input_schema_json = schema_to_json_string(registration.input_schema)
            if registration.output_schema:
                output_schema_json = schema_to_json_string(registration.output_schema)

            tool_infos.append(
                codemode_pb2.ToolInfo(
                    name=name,
                    is_async=is_async,
                    has_context=has_context,
                    description=description[:500],  # Allow longer descriptions
                    input_schema=codemode_pb2.ToolSchema(json_schema=input_schema_json),
                    output_schema=codemode_pb2.ToolSchema(json_schema=output_schema_json),
                )
            )

        return codemode_pb2.ListToolsResponse(tools=tool_infos)

    async def GetToolSchema(self, request, context):  # noqa: N802 gRPC naming
        """
        Get detailed schema for a specific tool.

        Args:
            request: GetToolSchemaRequest with tool_name.
            context: gRPC context.

        Returns:
            GetToolSchemaResponse with full schema details.

        Raises:
            grpc.StatusCode.NOT_FOUND: If tool not found.
        """
        tool_name = request.tool_name
        registration = self.registry.get_tool_registration(tool_name)

        if not registration:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Tool '{tool_name}' not found. Use ListTools to see available tools.",
            )

        tool = registration.tool

        # Serialize schemas
        input_schema_json = ""
        output_schema_json = ""
        if registration.input_schema:
            input_schema_json = schema_to_json_string(registration.input_schema)
        if registration.output_schema:
            output_schema_json = schema_to_json_string(registration.output_schema)

        return codemode_pb2.GetToolSchemaResponse(
            tool_name=tool_name,
            input_schema=codemode_pb2.ToolSchema(json_schema=input_schema_json),
            output_schema=codemode_pb2.ToolSchema(json_schema=output_schema_json),
            description=registration.description or "",
            is_async=self._is_tool_async(tool),
            has_context=hasattr(tool, "run_with_context"),
        )

    def _is_tool_async(self, tool: Any) -> bool:
        """
        Check if a tool is async (has async run/run_async method).

        Checks for async capability in the following order:
        1. Tool itself is a coroutine function
        2. Tool has async run() method
        3. Tool has async run_with_context() method
        4. Tool has async run_async() method (meta-tools pattern)

        Args:
            tool: Tool instance to check.

        Returns:
            True if the tool is async, False otherwise.
        """
        return (
            inspect.iscoroutinefunction(tool)
            or inspect.iscoroutinefunction(getattr(tool, "run", None))
            or inspect.iscoroutinefunction(getattr(tool, "run_with_context", None))
            or inspect.iscoroutinefunction(getattr(tool, "run_async", None))
        )


def _create_server_credentials(tls_config: "GrpcTlsConfig") -> grpc.ServerCredentials:
    """
    Create server credentials from TLS configuration.

    Args:
        tls_config: TLS configuration object

    Returns:
        gRPC server credentials

    Raises:
        ValueError: If required certificate files are missing
        FileNotFoundError: If certificate files don't exist
    """
    if tls_config.mode == "custom":
        # Load custom certificates
        if not tls_config.cert_file or not tls_config.key_file:
            raise ValueError("cert_file and key_file required for custom TLS mode")

        with open(tls_config.cert_file, "rb") as f:
            cert_chain = f.read()
        with open(tls_config.key_file, "rb") as f:
            private_key = f.read()

        # Optional: require client certificates (mTLS)
        root_certs = None
        require_client_auth = False
        if tls_config.ca_file:
            with open(tls_config.ca_file, "rb") as f:
                root_certs = f.read()
            require_client_auth = True
            logger.info("mTLS enabled: requiring client certificate authentication")

        return grpc.ssl_server_credentials(
            [(private_key, cert_chain)],
            root_certificates=root_certs,
            require_client_auth=require_client_auth,
        )
    else:
        # System certificates (rare for servers, but supported)
        logger.warning("System certificate mode not typical for servers, using default")
        return grpc.ssl_server_credentials([])


def create_tool_server(
    registry: ComponentRegistry,
    host: str = "0.0.0.0",
    port: int = 50051,
    api_key: str | None = None,
    enable_concurrency: bool = False,
    max_workers: int | None = None,
    tls_config: "GrpcTlsConfig | None" = None,
) -> grpc.aio.Server:
    server = grpc.aio.server()
    codemode_pb2_grpc.add_ToolServiceServicer_to_server(
        ToolService(
            registry, api_key, enable_concurrency=enable_concurrency, max_workers=max_workers
        ),
        server,
    )

    # TLS support
    if tls_config and tls_config.enabled:
        credentials = _create_server_credentials(tls_config)
        server.add_secure_port(f"{host}:{port}", credentials)
        logger.info("ToolService bound to %s:%s with TLS (mode: %s)", host, port, tls_config.mode)
    else:
        server.add_insecure_port(f"{host}:{port}")
        logger.info("ToolService bound to %s:%s (insecure)", host, port)

    return server


def start_tool_service(
    registry: ComponentRegistry,
    host: str = "0.0.0.0",
    port: int = 50051,
    api_key: str | None = None,
    enable_concurrency: bool = False,
    max_workers: int | None = None,
    tls_config: "GrpcTlsConfig | None" = None,
) -> None:
    """
    Start the gRPC ToolService and block until terminated (sync version).

    This function starts the server and blocks forever, suitable for standalone
    server processes. For web framework integration, use start_tool_service_async().

    Args:
        registry: Component registry with tools
        host: Host to bind to
        port: Port to bind to
        api_key: Optional API key for authentication
        enable_concurrency: Enable concurrent tool execution
        max_workers: Max workers for thread pool (if concurrency enabled)
        tls_config: Optional TLS configuration for secure communication

    Example:
        >>> # Standalone server - blocks forever
        >>> if __name__ == "__main__":
        >>>     start_tool_service(registry, port=50051)
    """
    server = create_tool_server(
        registry,
        host=host,
        port=port,
        api_key=api_key,
        enable_concurrency=enable_concurrency,
        max_workers=max_workers,
        tls_config=tls_config,
    )

    async def _serve():
        await server.start()
        logger.info("ToolService gRPC started on %s:%s", host, port)
        await server.wait_for_termination()

    asyncio.run(_serve())


async def start_tool_service_async(
    registry: ComponentRegistry,
    host: str = "0.0.0.0",
    port: int = 50051,
    api_key: str | None = None,
    enable_concurrency: bool = False,
    max_workers: int | None = None,
    tls_config: "GrpcTlsConfig | None" = None,
) -> grpc.aio.Server:
    """
    Start the gRPC ToolService in the background (async version).

    This async function properly waits for the server to start before returning,
    eliminating race conditions. Use this in async contexts when you need to
    immediately connect to the server after starting it.

    Args:
        registry: Component registry with tools
        host: Host to bind to
        port: Port to bind to
        api_key: Optional API key for authentication
        enable_concurrency: Enable concurrent tool execution
        max_workers: Max workers for thread pool (if concurrency enabled)
        tls_config: Optional TLS configuration for secure communication

    Returns:
        The gRPC server instance (already started and ready)

    Example:
        >>> server = await start_tool_service_async(registry)
        >>> # Server is now ready to accept connections
    """
    server = create_tool_server(
        registry,
        host=host,
        port=port,
        api_key=api_key,
        enable_concurrency=enable_concurrency,
        max_workers=max_workers,
        tls_config=tls_config,
    )

    # Start the server and wait for it to be ready
    await server.start()
    logger.info("ToolService gRPC started on %s:%s", host, port)

    # Schedule background task to keep server running
    async def _wait_for_termination():
        await server.wait_for_termination()

    asyncio.create_task(_wait_for_termination())

    return server
