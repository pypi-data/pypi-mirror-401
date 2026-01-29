"""
Executor client for communicating with the executor sidecar over gRPC.

This module provides the ExecutorClient class for sending code execution
requests to the isolated executor container. It includes:
- Automatic retry with exponential backoff on transient failures
- Correlation ID generation and propagation for request tracing
- TLS/mTLS support for secure communication
- Async-first design with sync wrappers for backward compatibility

Thread Safety:
    The ExecutorClient is designed to be thread-safe. The `_closed` flag
    is protected by a lock to prevent race conditions during close operations.
    Async channels are created lazily on first async call.
"""

from __future__ import annotations

import asyncio
import logging
import random
import threading
import time
from typing import TYPE_CHECKING, Any
from weakref import WeakKeyDictionary

import grpc
import grpc.aio
from google.protobuf import empty_pb2
from google.protobuf.struct_pb2 import Struct

from codemode.core.correlation import generate_correlation_id
from codemode.executor.models import ExecutionResult
from codemode.protos import codemode_pb2, codemode_pb2_grpc

if TYPE_CHECKING:
    from codemode.config.models import GrpcTlsConfig
    from codemode.core.context import RuntimeContext

logger = logging.getLogger(__name__)


class ExecutorClientError(Exception):
    """Base exception for executor client errors."""

    pass


class ExecutorConnectionError(ExecutorClientError):
    """Raised when connection to executor fails."""

    pass


class ExecutorTimeoutError(ExecutorClientError):
    """Raised when executor request times out."""

    pass


# Default gRPC status codes that are considered transient and safe to retry
DEFAULT_RETRY_STATUS_CODES = [
    grpc.StatusCode.UNAVAILABLE,
    grpc.StatusCode.DEADLINE_EXCEEDED,
    grpc.StatusCode.RESOURCE_EXHAUSTED,
]


def _to_struct(data: dict[str, Any] | None) -> Struct:
    """Convert a dictionary to a protobuf Struct."""
    struct = Struct()
    if data:
        struct.update(data)
    return struct


def _normalize_target(target: str) -> str:
    """Strip http/https prefixes so gRPC can dial host:port."""
    if target.startswith("http://"):
        return target[len("http://") :]
    if target.startswith("https://"):
        return target[len("https://") :]
    return target


class ExecutorClient:
    """
    Client for communicating with the executor sidecar via gRPC.

    Features:
    - Async-first design with sync wrappers for backward compatibility
    - Automatic retry with exponential backoff on transient failures
    - Correlation ID generation and propagation for request tracing
    - TLS/mTLS support for secure communication
    - Thread-safe close operations with idempotent close protection

    Attributes:
        executor_target: gRPC target address (host:port)
        api_key: API key for authentication
        timeout: Request timeout in seconds
        retry_enabled: Whether automatic retry is enabled
        retry_max_attempts: Maximum number of retry attempts
        include_correlation_id: Whether to auto-generate correlation IDs

    Example:
        >>> # Sync usage (backward compatible)
        >>> client = ExecutorClient(
        ...     executor_url="http://executor:8001",
        ...     api_key="secret-key",
        ...     retry_enabled=True,
        ...     retry_max_attempts=3
        ... )
        >>> result = client.execute(code="result = 2 + 2", available_tools=[], config={})
        >>> print(result.correlation_id)
        'cm-2x5f9k-a7b3'
        >>>
        >>> # Async usage (recommended)
        >>> async with ExecutorClient(...) as client:
        ...     result = await client.execute_async(code="result = 2 + 2", ...)
    """

    def __init__(
        self,
        executor_url: str,
        api_key: str,
        timeout: int = 35,
        tls_config: GrpcTlsConfig | None = None,
        # Retry configuration
        retry_enabled: bool = True,
        retry_max_attempts: int = 3,
        retry_backoff_base_ms: int = 100,
        retry_backoff_max_ms: int = 5000,
        retry_status_codes: list[grpc.StatusCode] | None = None,
        # Correlation ID configuration
        include_correlation_id: bool = True,
        correlation_id_prefix: str = "cm",
    ) -> None:
        """
        Initialize executor client with retry and correlation ID support.

        Args:
            executor_url: URL of the executor service (e.g., "http://executor:8001")
            api_key: API key for authentication
            timeout: Request timeout in seconds (default: 35)
            tls_config: Optional TLS configuration for secure communication
            retry_enabled: Enable automatic retry on transient failures (default: True)
            retry_max_attempts: Maximum number of retry attempts (default: 3)
            retry_backoff_base_ms: Base backoff time in milliseconds (default: 100)
            retry_backoff_max_ms: Maximum backoff time in milliseconds (default: 5000)
            retry_status_codes: gRPC status codes to retry on (default: UNAVAILABLE,
                DEADLINE_EXCEEDED, RESOURCE_EXHAUSTED)
            include_correlation_id: Auto-generate correlation IDs (default: True)
            correlation_id_prefix: Prefix for generated correlation IDs (default: "cm")

        Example:
            >>> client = ExecutorClient(
            ...     executor_url="http://executor:8001",
            ...     api_key="secret",
            ...     retry_max_attempts=5,
            ...     correlation_id_prefix="myapp"
            ... )
        """
        self.executor_target = _normalize_target(executor_url.rstrip("/"))
        self.api_key = api_key
        self.timeout = timeout
        self.tls_config = tls_config

        # Retry configuration
        self.retry_enabled = retry_enabled
        self.retry_max_attempts = retry_max_attempts
        self.retry_backoff_base_ms = retry_backoff_base_ms
        self.retry_backoff_max_ms = retry_backoff_max_ms
        self.retry_status_codes = retry_status_codes or DEFAULT_RETRY_STATUS_CODES

        # Correlation ID configuration
        self.include_correlation_id = include_correlation_id
        self.correlation_id_prefix = correlation_id_prefix

        # Close protection with thread-safe locking
        self._closed = False
        self._close_lock = threading.Lock()

        # Sync channel (created immediately for backward compatibility)
        if tls_config and tls_config.enabled:
            credentials = self._create_client_credentials(tls_config)
            self.channel = grpc.secure_channel(self.executor_target, credentials)
            logger.info(f"ExecutorClient using secure channel (TLS mode: {tls_config.mode})")
        else:
            self.channel = grpc.insecure_channel(self.executor_target)
            logger.info("ExecutorClient using insecure channel")

        self.stub = codemode_pb2_grpc.ExecutorServiceStub(self.channel)

        # Per-event-loop async channel cache
        # WeakKeyDictionary automatically removes entries when event loops are garbage collected,
        # preventing memory leaks in scenarios with many short-lived loops.
        # This is necessary because gRPC async channels are bound to the event loop that created them.
        self._loop_channels: WeakKeyDictionary[asyncio.AbstractEventLoop, grpc.aio.Channel] = (
            WeakKeyDictionary()
        )
        self._loop_stubs: WeakKeyDictionary[
            asyncio.AbstractEventLoop, codemode_pb2_grpc.ExecutorServiceStub
        ] = WeakKeyDictionary()
        # Use threading.Lock (not asyncio.Lock) for thread-safety across different event loops
        self._async_channel_creation_lock = threading.Lock()

        logger.info(
            f"Initialized ExecutorClient for {self.executor_target} "
            f"(retry={retry_enabled}, max_attempts={retry_max_attempts})"
        )

    def _calculate_backoff(self, attempt: int) -> float:
        """
        Calculate backoff time with jitter for retry.

        Uses exponential backoff with random jitter (0.8-1.2x) to prevent
        thundering herd issues.

        Args:
            attempt: Current attempt number (0-indexed)

        Returns:
            Backoff time in seconds
        """
        base = self.retry_backoff_base_ms * (2**attempt)
        jitter = random.uniform(0.8, 1.2)
        backoff = min(base * jitter, self.retry_backoff_max_ms)
        return backoff / 1000  # Convert to seconds

    def _ensure_not_closed(self) -> None:
        """
        Raise an error if the client has been closed.

        Raises:
            ExecutorClientError: If the client has been closed.
        """
        if self._closed:
            raise ExecutorClientError("ExecutorClient has been closed")

    async def _get_async_channel(
        self,
    ) -> tuple[grpc.aio.Channel, codemode_pb2_grpc.ExecutorServiceStub]:
        """
        Get or create an async gRPC channel for the current event loop.

        This method maintains a per-event-loop cache of channels because gRPC async
        channels are bound to the event loop that created them. This is essential for
        scenarios where the same ExecutorClient is used across different event loops,
        such as:
        - FastAPI + CrewAI with `kickoff_async()` (uses `asyncio.to_thread`)
        - Multiple `asyncio.run()` calls in sequence
        - Thread pool executors running async code

        The cache uses WeakKeyDictionary to automatically clean up channels when
        their associated event loops are garbage collected.

        Thread Safety:
            Uses threading.Lock (not asyncio.Lock) to ensure thread-safety when
            channels are created from different threads with different event loops.

        Returns:
            Tuple of (async channel, async stub) bound to the current event loop

        Raises:
            ExecutorClientError: If the client has been closed.
        """
        self._ensure_not_closed()

        current_loop = asyncio.get_running_loop()

        # Fast path: check if we have a channel for this loop (no lock needed for read)
        if current_loop in self._loop_channels:
            channel = self._loop_channels[current_loop]
            stub = self._loop_stubs[current_loop]
            return channel, stub

        # Slow path: create new channel (thread-safe lock for creation)
        with self._async_channel_creation_lock:
            # Double-check after acquiring lock (another thread may have created it)
            if current_loop in self._loop_channels:
                channel = self._loop_channels[current_loop]
                stub = self._loop_stubs[current_loop]
                return channel, stub

            # Create new channel for this event loop
            if self.tls_config and self.tls_config.enabled:
                credentials = self._create_client_credentials(self.tls_config)
                channel = grpc.aio.secure_channel(self.executor_target, credentials)
                logger.debug(f"Created async secure channel for event loop {id(current_loop)}")
            else:
                channel = grpc.aio.insecure_channel(self.executor_target)
                logger.debug(f"Created async insecure channel for event loop {id(current_loop)}")

            stub = codemode_pb2_grpc.ExecutorServiceStub(channel)

            # Cache for this event loop
            self._loop_channels[current_loop] = channel
            self._loop_stubs[current_loop] = stub

            return channel, stub

    async def execute_async(
        self,
        code: str,
        available_tools: list[str],
        config: dict[str, Any],
        execution_timeout: int = 30,
        context: RuntimeContext | None = None,
        correlation_id: str | None = None,
    ) -> ExecutionResult:
        """
        Execute code in the executor service asynchronously with automatic retry.

        This is the primary async execution method. Uses non-blocking asyncio.sleep()
        for retry backoff, preventing event loop blocking.

        Args:
            code: Python code to execute
            available_tools: List of tool names available for use
            config: Configuration dictionary
            execution_timeout: Timeout for code execution (gRPC deadline)
            context: Optional runtime context to inject
            correlation_id: Optional correlation ID (auto-generated if not provided
                and include_correlation_id is True)

        Returns:
            ExecutionResult with execution outcome

        Raises:
            ExecutorTimeoutError: If request times out after all retries
            ExecutorConnectionError: If connection fails after all retries
            ExecutorClientError: For other gRPC errors or if client is closed

        Example:
            >>> async with ExecutorClient(...) as client:
            ...     result = await client.execute_async(
            ...         code="result = tools['weather'].run(location='NYC')",
            ...         available_tools=["weather"],
            ...         config={},
            ...     )
        """
        self._ensure_not_closed()

        # Generate correlation ID if needed
        if correlation_id is None and self.include_correlation_id:
            correlation_id = generate_correlation_id(self.correlation_id_prefix)

        start_time = time.perf_counter()
        last_error: grpc.RpcError | None = None

        # Get async channel/stub
        _, async_stub = await self._get_async_channel()

        for attempt in range(self.retry_max_attempts):
            try:
                result = await self._execute_once_async(
                    stub=async_stub,
                    code=code,
                    available_tools=available_tools,
                    config=config,
                    execution_timeout=execution_timeout,
                    context=context,
                    correlation_id=correlation_id,
                )
                # Add duration to result
                duration_ms = (time.perf_counter() - start_time) * 1000
                return ExecutionResult(
                    success=result.success,
                    result=result.result,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    error=result.error,
                    error_details=result.error_details,
                    correlation_id=correlation_id,
                    duration_ms=duration_ms,
                )

            except grpc.RpcError as e:
                last_error = e

                # Don't retry if retry is disabled
                if not self.retry_enabled:
                    break

                # Don't retry non-transient errors
                if e.code() not in self.retry_status_codes:
                    break

                # Don't retry if this was the last attempt
                if attempt == self.retry_max_attempts - 1:
                    break

                # Calculate backoff and wait (non-blocking!)
                backoff = self._calculate_backoff(attempt)
                logger.warning(
                    "Async retry attempt %d/%d after %.2fs: %s",
                    attempt + 1,
                    self.retry_max_attempts,
                    backoff,
                    e.code(),
                    extra={"correlation_id": correlation_id, "attempt": attempt + 1},
                )
                await asyncio.sleep(backoff)  # Non-blocking sleep!

        # All retries exhausted, raise appropriate exception
        duration_ms = (time.perf_counter() - start_time) * 1000
        if last_error is not None:
            if last_error.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                raise ExecutorTimeoutError(
                    f"Request to executor timed out after {self.timeout}s "
                    f"(correlation_id={correlation_id})"
                ) from last_error
            if last_error.code() in (
                grpc.StatusCode.UNAVAILABLE,
                grpc.StatusCode.UNAUTHENTICATED,
            ):
                raise ExecutorConnectionError(
                    f"Failed to connect to executor at {self.executor_target} "
                    f"after {self.retry_max_attempts} attempts "
                    f"(correlation_id={correlation_id})"
                ) from last_error
            raise ExecutorClientError(
                f"Executor communication failed: {last_error.details()} "
                f"(correlation_id={correlation_id})"
            ) from last_error

        # This shouldn't happen, but handle it gracefully
        raise ExecutorClientError(
            f"Executor communication failed unexpectedly (correlation_id={correlation_id})"
        )

    async def _execute_once_async(
        self,
        stub: codemode_pb2_grpc.ExecutorServiceStub,
        code: str,
        available_tools: list[str],
        config: dict[str, Any],
        execution_timeout: int,
        context: RuntimeContext | None,
        correlation_id: str | None,
    ) -> ExecutionResult:
        """
        Execute a single async request without retry logic.

        Args:
            stub: Async gRPC stub to use
            code: Python code to execute
            available_tools: List of tool names
            config: Configuration dictionary
            execution_timeout: Timeout for code execution
            context: Optional runtime context
            correlation_id: Correlation ID for tracing

        Returns:
            ExecutionResult from the executor

        Raises:
            grpc.RpcError: On any gRPC failure
        """
        context_dict = context.to_dict() if context else None

        request = codemode_pb2.ExecutionRequest(
            code=code,
            available_tools=available_tools,
            config=_to_struct(config),
            timeout=execution_timeout,
            context=_to_struct(context_dict) if context_dict else None,
            correlation_id=correlation_id or "",
        )

        # Build metadata with auth and correlation ID
        metadata = []
        if self.api_key:
            metadata.append(("authorization", f"Bearer {self.api_key}"))
        if correlation_id:
            metadata.append(("x-correlation-id", correlation_id))

        logger.debug(
            "Executing code async (%d chars, %d tools)",
            len(code),
            len(available_tools),
            extra={"correlation_id": correlation_id},
        )

        response = await stub.Execute(request, timeout=self.timeout, metadata=metadata)

        result = ExecutionResult(
            success=response.success,
            result=response.result or None,
            stdout=response.stdout,
            stderr=response.stderr,
            error=response.error or None,
            error_details=None,
            correlation_id=correlation_id,
            duration_ms=0.0,
        )

        if result.success:
            logger.info(
                "Async code execution successful",
                extra={"correlation_id": correlation_id},
            )
        else:
            logger.warning(
                "Async code execution failed: %s",
                result.error,
                extra={"correlation_id": correlation_id},
            )

        return result

    def execute(
        self,
        code: str,
        available_tools: list[str],
        config: dict[str, Any],
        execution_timeout: int = 30,
        context: RuntimeContext | None = None,
        correlation_id: str | None = None,
    ) -> ExecutionResult:
        """
        Execute code in the executor service with automatic retry.

        Sends code to the isolated executor container for safe execution.
        Automatically retries on transient failures with exponential backoff.

        Args:
            code: Python code to execute
            available_tools: List of tool names available for use
            config: Configuration dictionary
            execution_timeout: Timeout for code execution (gRPC deadline)
            context: Optional runtime context to inject
            correlation_id: Optional correlation ID (auto-generated if not provided
                and include_correlation_id is True)

        Returns:
            ExecutionResult with execution outcome

        Raises:
            ExecutorTimeoutError: If request times out after all retries
            ExecutorConnectionError: If connection fails after all retries
            ExecutorClientError: For other gRPC errors

        Example:
            >>> result = client.execute(
            ...     code="result = tools['weather'].run(location='NYC')",
            ...     available_tools=["weather"],
            ...     config={},
            ...     correlation_id="req-abc123"
            ... )
        """
        self._ensure_not_closed()

        # Generate correlation ID if needed
        if correlation_id is None and self.include_correlation_id:
            correlation_id = generate_correlation_id(self.correlation_id_prefix)

        start_time = time.perf_counter()
        last_error: grpc.RpcError | None = None

        for attempt in range(self.retry_max_attempts):
            try:
                result = self._execute_once(
                    code=code,
                    available_tools=available_tools,
                    config=config,
                    execution_timeout=execution_timeout,
                    context=context,
                    correlation_id=correlation_id,
                )
                # Add duration to result
                duration_ms = (time.perf_counter() - start_time) * 1000
                # Create new result with duration (ExecutionResult is a Pydantic model)
                return ExecutionResult(
                    success=result.success,
                    result=result.result,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    error=result.error,
                    error_details=result.error_details,
                    correlation_id=correlation_id,
                    duration_ms=duration_ms,
                )

            except grpc.RpcError as e:
                last_error = e

                # Don't retry if retry is disabled
                if not self.retry_enabled:
                    break

                # Don't retry non-transient errors
                if e.code() not in self.retry_status_codes:
                    break

                # Don't retry if this was the last attempt
                if attempt == self.retry_max_attempts - 1:
                    break

                # Calculate backoff and wait
                backoff = self._calculate_backoff(attempt)
                logger.warning(
                    "Retry attempt %d/%d after %.2fs: %s",
                    attempt + 1,
                    self.retry_max_attempts,
                    backoff,
                    e.code(),
                    extra={"correlation_id": correlation_id, "attempt": attempt + 1},
                )
                time.sleep(backoff)

        # All retries exhausted, raise appropriate exception
        duration_ms = (time.perf_counter() - start_time) * 1000
        if last_error is not None:
            if last_error.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                raise ExecutorTimeoutError(
                    f"Request to executor timed out after {self.timeout}s "
                    f"(correlation_id={correlation_id})"
                ) from last_error
            if last_error.code() in (
                grpc.StatusCode.UNAVAILABLE,
                grpc.StatusCode.UNAUTHENTICATED,
            ):
                raise ExecutorConnectionError(
                    f"Failed to connect to executor at {self.executor_target} "
                    f"after {self.retry_max_attempts} attempts "
                    f"(correlation_id={correlation_id})"
                ) from last_error
            raise ExecutorClientError(
                f"Executor communication failed: {last_error.details()} "
                f"(correlation_id={correlation_id})"
            ) from last_error

        # This shouldn't happen, but handle it gracefully
        raise ExecutorClientError(
            f"Executor communication failed unexpectedly (correlation_id={correlation_id})"
        )

    def _execute_once(
        self,
        code: str,
        available_tools: list[str],
        config: dict[str, Any],
        execution_timeout: int,
        context: RuntimeContext | None,
        correlation_id: str | None,
    ) -> ExecutionResult:
        """
        Execute a single request without retry logic.

        Args:
            code: Python code to execute
            available_tools: List of tool names
            config: Configuration dictionary
            execution_timeout: Timeout for code execution
            context: Optional runtime context
            correlation_id: Correlation ID for tracing

        Returns:
            ExecutionResult from the executor

        Raises:
            grpc.RpcError: On any gRPC failure
        """
        context_dict = context.to_dict() if context else None

        request = codemode_pb2.ExecutionRequest(
            code=code,
            available_tools=available_tools,
            config=_to_struct(config),
            timeout=execution_timeout,
            context=_to_struct(context_dict) if context_dict else None,
            correlation_id=correlation_id or "",
        )

        # Build metadata with auth and correlation ID
        metadata = []
        if self.api_key:
            metadata.append(("authorization", f"Bearer {self.api_key}"))
        if correlation_id:
            metadata.append(("x-correlation-id", correlation_id))

        logger.debug(
            "Executing code (%d chars, %d tools)",
            len(code),
            len(available_tools),
            extra={"correlation_id": correlation_id},
        )

        response = self.stub.Execute(request, timeout=self.timeout, metadata=metadata)

        result = ExecutionResult(
            success=response.success,
            result=response.result or None,
            stdout=response.stdout,
            stderr=response.stderr,
            error=response.error or None,
            correlation_id=correlation_id,
        )

        if result.success:
            logger.info(
                "Code execution successful",
                extra={"correlation_id": correlation_id},
            )
        else:
            logger.warning(
                "Code execution failed: %s",
                result.error,
                extra={"correlation_id": correlation_id},
            )

        return result

    def health_check(self) -> bool:
        """
        Check if executor service is healthy.

        Returns:
            True if executor is healthy, False otherwise

        Example:
            >>> if client.health_check():
            ...     print("Executor is healthy")
        """
        try:
            resp = self.stub.Health(empty_pb2.Empty(), timeout=5)
            return resp.status == "healthy"
        except grpc.RpcError as e:
            logger.error(f"Executor health check failed: {e}")
            return False

    def ready_check(self) -> bool:
        """
        Check if executor can reach main app.

        Returns:
            True if executor is ready, False otherwise

        Example:
            >>> if client.ready_check():
            ...     print("Executor is ready")
        """
        try:
            resp = self.stub.Ready(empty_pb2.Empty(), timeout=5)
            return resp.status == "ready"
        except grpc.RpcError as e:
            logger.error(f"Executor ready check failed: {e}")
            return False

    def close(self) -> None:
        """
        Close gRPC channels.

        This method is idempotent - calling it multiple times is safe.
        Uses a lock to ensure thread-safety.
        """
        with self._close_lock:
            if self._closed:
                return  # Already closed, nothing to do

            self._closed = True

            # Close sync channel
            try:
                self.channel.close()
            except Exception as e:
                logger.warning(f"Error closing sync channel: {e}")

            # Close all cached async channels
            for loop, channel in list(self._loop_channels.items()):
                try:
                    # Note: grpc.aio.Channel.close() is not a coroutine in all versions
                    # Just mark it for closure; actual cleanup happens on next event loop
                    channel.close()
                except Exception as e:
                    logger.warning(f"Error closing async channel for loop {id(loop)}: {e}")

            # Clear the caches
            self._loop_channels.clear()
            self._loop_stubs.clear()

            logger.debug("Closed executor client channels")

    async def close_async(self) -> None:
        """
        Close gRPC channels asynchronously.

        This method is idempotent - calling it multiple times is safe.
        Properly awaits async channel closure.
        """
        with self._close_lock:
            if self._closed:
                return  # Already closed, nothing to do

            self._closed = True

        # Close sync channel (outside lock since it may block briefly)
        try:
            self.channel.close()
        except Exception as e:
            logger.warning(f"Error closing sync channel: {e}")

        # Close all cached async channels
        for loop, channel in list(self._loop_channels.items()):
            try:
                await channel.close()
            except Exception as e:
                logger.warning(f"Error closing async channel for loop {id(loop)}: {e}")

        # Clear the caches
        self._loop_channels.clear()
        self._loop_stubs.clear()

        logger.debug("Closed executor client channels (async)")

    def __enter__(self) -> ExecutorClient:
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()

    async def __aenter__(self) -> ExecutorClient:
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close_async()

    def _create_client_credentials(self, tls_config: GrpcTlsConfig) -> grpc.ChannelCredentials:
        """Create gRPC channel credentials from TLS config."""
        if tls_config.mode == "custom":
            # Load custom certificates
            root_certs = None
            if tls_config.ca_file:
                with open(tls_config.ca_file, "rb") as f:
                    root_certs = f.read()

            # Optional: client certificate for mTLS
            private_key = None
            cert_chain = None
            if tls_config.client_cert_file and tls_config.client_key_file:
                with open(tls_config.client_key_file, "rb") as f:
                    private_key = f.read()
                with open(tls_config.client_cert_file, "rb") as f:
                    cert_chain = f.read()
                logger.info("mTLS client authentication enabled")

            return grpc.ssl_channel_credentials(
                root_certificates=root_certs,
                private_key=private_key,
                certificate_chain=cert_chain,
            )
        else:
            # Use system certificates
            return grpc.ssl_channel_credentials()

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"ExecutorClient(target={self.executor_target}, "
            f"retry={self.retry_enabled}, max_attempts={self.retry_max_attempts})"
        )
