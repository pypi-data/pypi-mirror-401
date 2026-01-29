"""
Executor gRPC service (sidecar).

This module implements the executor sidecar service that receives code execution
requests from the main application. It supports configuration via:

1. SidecarConfig (recommended): Load from codemode-sidecar.yaml or environment
2. Environment variables (legacy): Direct env var configuration

Example:
    Using SidecarConfig:
        >>> from codemode.config import SidecarConfig
        >>> config = SidecarConfig.from_env()
        >>> service = ExecutorGrpcService.from_config(config)

    Running the service:
        $ python -m codemode.executor.service
"""

import asyncio
import logging
import os
from pathlib import Path

import grpc
from google.protobuf import empty_pb2
from google.protobuf.json_format import MessageToDict

from codemode.config.sidecar_config import SidecarConfig
from codemode.executor.runner import CodeRunner
from codemode.executor.security import SecurityValidator
from codemode.protos import codemode_pb2, codemode_pb2_grpc

logger = logging.getLogger(__name__)


def _load_sidecar_config() -> SidecarConfig:
    """
    Load sidecar configuration from file or environment.

    Priority:
    1. CODEMODE_SIDECAR_CONFIG env var (path to config file)
    2. codemode-sidecar.yaml in current directory
    3. Environment variables only

    Returns:
        SidecarConfig instance
    """
    # Check for explicit config file path
    config_path = os.environ.get("CODEMODE_SIDECAR_CONFIG")
    if config_path and Path(config_path).exists():
        from codemode.config.loader import ConfigLoader

        logger.info(f"Loading sidecar config from: {config_path}")
        return ConfigLoader.load_sidecar_config(config_path)

    # Check for default config file
    default_path = Path("codemode-sidecar.yaml")
    if default_path.exists():
        from codemode.config.loader import ConfigLoader

        logger.info(f"Loading sidecar config from: {default_path}")
        return ConfigLoader.load_sidecar_config(default_path)

    # Fall back to environment variables
    logger.info("Loading sidecar config from environment variables")
    return SidecarConfig.from_env()


def _configure_logging(config: SidecarConfig) -> None:
    """Configure logging based on sidecar config."""
    log_level = getattr(logging, config.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def _load_server_credentials(config: SidecarConfig) -> grpc.ServerCredentials | None:
    """
    Load server TLS credentials from SidecarConfig.

    Args:
        config: SidecarConfig instance

    Returns:
        ServerCredentials if TLS is enabled, None otherwise
    """
    if not config.tls.enabled:
        return None

    if config.tls.mode == "custom":
        if not config.tls.cert_file or not config.tls.key_file:
            logger.error("TLS enabled but cert_file or key_file not set")
            raise ValueError("TLS certificate and key files required when TLS is enabled")

        with open(config.tls.cert_file, "rb") as f:
            cert_chain = f.read()
        with open(config.tls.key_file, "rb") as f:
            private_key = f.read()

        # Optional: require client certificates (mTLS)
        root_certs = None
        require_client_auth = config.tls.require_client_auth
        if config.tls.ca_file:
            with open(config.tls.ca_file, "rb") as f:
                root_certs = f.read()
            if require_client_auth:
                logger.info("mTLS enabled: requiring client certificate authentication")

        return grpc.ssl_server_credentials(
            [(private_key, cert_chain)],
            root_certificates=root_certs,
            require_client_auth=require_client_auth,
        )
    else:
        # System certificates (typically not used for servers, but supported)
        logger.warning("System certificate mode not typical for servers, using default")
        return grpc.ssl_server_credentials([])


def _get_callback_credentials(config: SidecarConfig) -> grpc.ChannelCredentials | None:
    """
    Load client TLS credentials for callbacks to main app.

    Args:
        config: SidecarConfig instance

    Returns:
        ChannelCredentials if callback TLS is enabled, None otherwise
    """
    if not config.callback_tls.enabled:
        return None

    root_certs = None
    if config.callback_tls.ca_file:
        with open(config.callback_tls.ca_file, "rb") as f:
            root_certs = f.read()

    # Optional: client cert for mTLS
    private_key = None
    cert_chain = None
    if config.callback_tls.client_cert and config.callback_tls.client_key:
        with open(config.callback_tls.client_key, "rb") as f:
            private_key = f.read()
        with open(config.callback_tls.client_cert, "rb") as f:
            cert_chain = f.read()
        logger.info("mTLS client authentication enabled for callbacks")

    return grpc.ssl_channel_credentials(
        root_certificates=root_certs,
        private_key=private_key,
        certificate_chain=cert_chain,
    )


# Legacy environment variable support
def _load_server_credentials_from_env() -> grpc.ServerCredentials | None:
    """Load server TLS credentials from environment variables (legacy)."""
    tls_enabled = os.getenv("CODEMODE_GRPC_TLS_ENABLED", "false").lower() == "true"
    if not tls_enabled:
        return None

    mode = os.getenv("CODEMODE_GRPC_TLS_MODE", "system")

    if mode == "custom":
        cert_file = os.getenv("CODEMODE_GRPC_TLS_CERT_FILE")
        key_file = os.getenv("CODEMODE_GRPC_TLS_KEY_FILE")

        if not cert_file or not key_file:
            logger.error("TLS enabled but CODEMODE_GRPC_TLS_CERT_FILE or KEY_FILE not set")
            raise ValueError("TLS certificate and key files required when TLS is enabled")

        with open(cert_file, "rb") as f:
            cert_chain = f.read()
        with open(key_file, "rb") as f:
            private_key = f.read()

        # Optional: require client certificates (mTLS)
        ca_file = os.getenv("CODEMODE_GRPC_TLS_CA_FILE")
        root_certs = None
        require_client_auth = False
        if ca_file:
            with open(ca_file, "rb") as f:
                root_certs = f.read()
            require_client_auth = (
                os.getenv("CODEMODE_GRPC_TLS_REQUIRE_CLIENT_AUTH", "false").lower() == "true"
            )
            if require_client_auth:
                logger.info("mTLS enabled: requiring client certificate authentication")

        return grpc.ssl_server_credentials(
            [(private_key, cert_chain)],
            root_certificates=root_certs,
            require_client_auth=require_client_auth,
        )
    else:
        # System certificates (typically not used for servers, but supported)
        logger.warning("System certificate mode not typical for servers, using default")
        return grpc.ssl_server_credentials([])


def _get_client_credentials_from_env() -> grpc.ChannelCredentials | None:
    """Load client TLS credentials from environment variables (legacy)."""
    tls_enabled = os.getenv("CODEMODE_GRPC_TLS_ENABLED", "false").lower() == "true"
    if not tls_enabled:
        return None

    mode = os.getenv("CODEMODE_GRPC_TLS_MODE", "system")

    if mode == "custom":
        ca_file = os.getenv("CODEMODE_GRPC_TLS_CA_FILE")
        root_certs = None
        if ca_file:
            with open(ca_file, "rb") as f:
                root_certs = f.read()

        # Optional: client cert for mTLS
        client_cert_file = os.getenv("CODEMODE_GRPC_TLS_CLIENT_CERT_FILE")
        client_key_file = os.getenv("CODEMODE_GRPC_TLS_CLIENT_KEY_FILE")
        private_key = None
        cert_chain = None
        if client_cert_file and client_key_file:
            with open(client_key_file, "rb") as f:
                private_key = f.read()
            with open(client_cert_file, "rb") as f:
                cert_chain = f.read()
            logger.info("mTLS client authentication enabled")

        return grpc.ssl_channel_credentials(
            root_certificates=root_certs,
            private_key=private_key,
            certificate_chain=cert_chain,
        )
    else:
        # System certificates
        return grpc.ssl_channel_credentials()


class ExecutorGrpcService(codemode_pb2_grpc.ExecutorServiceServicer):
    """
    Handles Execute/Health/Ready via gRPC.

    This service can be initialized either with a SidecarConfig (recommended)
    or with individual parameters for backward compatibility.

    Attributes:
        config: SidecarConfig instance (if using config-based initialization)
        code_runner: CodeRunner instance for executing code
    """

    def __init__(
        self,
        code_runner: CodeRunner,
        config: SidecarConfig | None = None,
        main_app_target: str | None = None,
        api_key: str | None = None,
    ) -> None:
        """
        Initialize the executor service.

        Args:
            code_runner: CodeRunner instance for executing code
            config: SidecarConfig for configuration (recommended)
            main_app_target: Main app gRPC target (legacy, use config instead)
            api_key: API key for authentication (legacy, use config instead)
        """
        self.code_runner = code_runner
        self.config = config
        self._tool_metadata: dict[str, dict] | None = None  # None = not fetched yet
        self._metadata_fetch_failed: bool = False
        self._metadata_lock = asyncio.Lock()  # Prevent concurrent fetches

        # Use config values or fall back to explicit params / env vars
        if config:
            self._main_app_target = config.main_app_grpc_target
            self._api_key = config.api_key or ""
            self._get_callback_creds = lambda: _get_callback_credentials(config)
        else:
            self._main_app_target = main_app_target or os.getenv(
                "MAIN_APP_GRPC_TARGET", "localhost:50051"
            )
            self._api_key = api_key or os.getenv("CODEMODE_API_KEY", "")
            self._get_callback_creds = _get_client_credentials_from_env

    @classmethod
    def from_config(
        cls, config: SidecarConfig, security_validator: SecurityValidator | None = None
    ) -> "ExecutorGrpcService":
        """
        Create an ExecutorGrpcService from a SidecarConfig.

        Args:
            config: SidecarConfig instance
            security_validator: Optional SecurityValidator (created if not provided)

        Returns:
            Configured ExecutorGrpcService instance
        """
        if security_validator is None:
            security_validator = SecurityValidator()

        code_runner = CodeRunner(
            main_app_target=config.main_app_grpc_target,
            api_key=config.api_key or "",
            security_validator=security_validator,
        )

        return cls(code_runner=code_runner, config=config)

    async def _fetch_tool_metadata(self, max_retries: int = 3) -> bool:
        """
        Fetch tool metadata from main app ToolService with retry logic.

        Args:
            max_retries: Maximum number of retry attempts

        Returns:
            True if metadata was successfully fetched, False otherwise
        """
        for attempt in range(max_retries):
            try:
                # Create channel with TLS support
                credentials = self._get_callback_creds()
                if credentials:
                    channel = grpc.aio.secure_channel(self._main_app_target, credentials)
                else:
                    channel = grpc.aio.insecure_channel(self._main_app_target)

                async with channel:
                    stub = codemode_pb2_grpc.ToolServiceStub(channel)
                    resp = await stub.ListTools(empty_pb2.Empty(), timeout=5)

                    # Initialize metadata dict (empty dict means "fetched but no tools")
                    self._tool_metadata = {}
                    for info in resp.tools:
                        self._tool_metadata[info.name] = {
                            "is_async": info.is_async,
                            "has_context": info.has_context,
                            "description": info.description,
                        }

                    logger.info("Fetched metadata for %d tools", len(self._tool_metadata))
                    self._metadata_fetch_failed = False
                    return True

            except grpc.RpcError as e:
                logger.warning(
                    "Metadata fetch attempt %d/%d failed: %s",
                    attempt + 1,
                    max_retries,
                    e,
                )
                if attempt < max_retries - 1:
                    # Exponential backoff: 0.5s, 1s, 1.5s
                    backoff = 0.5 * (attempt + 1)
                    logger.debug("Retrying in %.1fs...", backoff)
                    await asyncio.sleep(backoff)

        # All retries failed
        self._metadata_fetch_failed = True
        logger.error(
            "Failed to fetch tool metadata from %s after %d attempts",
            self._main_app_target,
            max_retries,
        )
        return False

    async def Execute(self, request, context):
        """Execute code with tool access.

        Reads correlation ID from both request field and x-correlation-id metadata header.
        Correlation ID is logged and included in the response for request tracing.
        """
        # Extract metadata
        metadata = dict(context.invocation_metadata())

        # API key validation
        if self._api_key:
            if metadata.get("authorization") != f"Bearer {self._api_key}":
                context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid API key")

        # Extract correlation ID from metadata header or request field
        correlation_id = metadata.get("x-correlation-id") or getattr(request, "correlation_id", "")
        log_extra = {"correlation_id": correlation_id} if correlation_id else {}

        # Fetch tool metadata if not cached (None means never fetched)
        # Use lock to prevent race condition with concurrent requests
        if self._tool_metadata is None:
            async with self._metadata_lock:
                # Double-check after acquiring lock (another request may have fetched)
                if self._tool_metadata is None:
                    success = await self._fetch_tool_metadata()
                    if not success:
                        # Critical: cannot proceed without metadata - tool signatures would be wrong
                        error_msg = (
                            f"Failed to fetch tool metadata from ToolService at {self._main_app_target}. "
                            "Cannot determine tool signatures (sync vs async). "
                            "Ensure ToolService is running and accessible.\n\n"
                            "Troubleshooting:\n"
                            "• If executor is in Docker, ensure MAIN_APP_GRPC_TARGET=host.docker.internal:50051\n"
                            "• Check ToolService is running on host: lsof -i :50051\n"
                            "• Verify API key matches: CODEMODE_API_KEY\n"
                            "• Check network connectivity between executor and ToolService"
                        )
                        logger.error(error_msg, extra=log_extra)
                        return codemode_pb2.ExecutionResponse(
                            success=False,
                            result="",
                            stdout="",
                            stderr="",
                            error=error_msg,
                            correlation_id=correlation_id,
                        )

        logger.info(
            "Execution request: %s chars, %s tools, timeout=%ss%s",
            len(request.code),
            len(request.available_tools),
            request.timeout,
            ", with context" if request.HasField("context") else "",
            extra=log_extra,
        )

        result = await self.code_runner.run(
            code=request.code,
            available_tools=list(request.available_tools),
            tool_metadata=self._tool_metadata,
            config=MessageToDict(request.config, preserving_proto_field_name=True),
            timeout=request.timeout,
            context=(
                MessageToDict(request.context, preserving_proto_field_name=True)
                if request.HasField("context")
                else None
            ),
            correlation_id=correlation_id if correlation_id else None,
        )

        if result.success:
            logger.info("Execution completed successfully", extra=log_extra)
        else:
            logger.warning("Execution failed: %s", result.error, extra=log_extra)

        return codemode_pb2.ExecutionResponse(
            success=result.success,
            result=result.result or "",
            stdout=result.stdout,
            stderr=result.stderr,
            error=result.error or "",
            correlation_id=correlation_id,
        )

    async def Health(self, request, context):  # noqa: N802 gRPC naming
        """Return health status."""
        return codemode_pb2.HealthResponse(
            status="healthy", version="0.1.0", main_app_target=self._main_app_target
        )

    async def Ready(self, request, context):  # noqa: N802 gRPC naming
        """Check readiness by pinging main app ToolService."""
        status = "ready"
        try:
            # Create channel with TLS support
            credentials = self._get_callback_creds()
            if credentials:
                channel = grpc.aio.secure_channel(self._main_app_target, credentials)
            else:
                channel = grpc.aio.insecure_channel(self._main_app_target)

            async with channel:
                stub = codemode_pb2_grpc.ToolServiceStub(channel)
                await stub.ListTools(empty_pb2.Empty(), timeout=2)
        except grpc.RpcError as e:
            logger.warning("Readiness check failed: %s", e)
            status = "unreachable"
        return codemode_pb2.HealthResponse(
            status=status, version="0.1.0", main_app_target=self._main_app_target
        )


async def serve(config: SidecarConfig | None = None) -> None:
    """
    Start the executor gRPC server.

    Args:
        config: Optional SidecarConfig. If not provided, will auto-load from
               file or environment variables.
    """
    # Load config if not provided
    if config is None:
        config = _load_sidecar_config()

    # Configure logging
    _configure_logging(config)

    # Create service
    security_validator = SecurityValidator()
    service = ExecutorGrpcService.from_config(config, security_validator)

    # Create server
    server = grpc.aio.server()
    codemode_pb2_grpc.add_ExecutorServiceServicer_to_server(service, server)

    listen_addr = f"[::]:{config.port}"

    # TLS support
    credentials = _load_server_credentials(config)
    if credentials:
        server.add_secure_port(listen_addr, credentials)
        logger.info("=" * 60)
        logger.info("Codemode Executor gRPC Service Starting (TLS ENABLED)")
    else:
        server.add_insecure_port(listen_addr)
        logger.info("=" * 60)
        logger.info("Codemode Executor gRPC Service Starting (insecure)")

    logger.info("Main App gRPC Target: %s", config.main_app_grpc_target)
    logger.info("Port: %s", config.port)
    logger.info("API Key Configured: %s", bool(config.api_key))
    logger.info("=" * 60)

    await server.start()
    await server.wait_for_termination()


def main() -> None:
    """Entry point for the executor service."""
    asyncio.run(serve())


if __name__ == "__main__":
    main()
