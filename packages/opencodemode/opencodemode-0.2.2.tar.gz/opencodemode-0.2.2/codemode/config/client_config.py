"""
Client-side configuration for codemode main applications.

This module defines the ClientConfig model used by applications that connect
to the codemode executor sidecar. All fields support environment variable
overrides for production deployments.

Environment Variables:
    All configuration options can be set via environment variables with the
    CODEMODE_ prefix. See individual field descriptions for specific variable names.

Example:
    Loading from YAML file:
        >>> from codemode.config import ClientConfigLoader
        >>> config = ClientConfigLoader.load("codemode-client.yaml")

    Loading from environment only:
        >>> config = ClientConfigLoader.load_from_env()

    Programmatic configuration:
        >>> config = ClientConfig(
        ...     executor_url="http://executor:8001",
        ...     executor_api_key="secret-key",
        ... )
"""

import logging
import os
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

logger = logging.getLogger(__name__)


class RetryConfig(BaseModel):
    """Retry configuration for transient failures.

    Attributes:
        enabled: Whether retry is enabled. ENV: CODEMODE_RETRY_ENABLED
        max_attempts: Maximum retry attempts. ENV: CODEMODE_RETRY_MAX_ATTEMPTS
        backoff_base_ms: Base backoff time in milliseconds. ENV: CODEMODE_RETRY_BACKOFF_BASE_MS
        backoff_max_ms: Maximum backoff time in milliseconds. ENV: CODEMODE_RETRY_BACKOFF_MAX_MS
    """

    model_config = ConfigDict(extra="forbid")

    enabled: bool = Field(
        default=True,
        description="Enable automatic retry on transient failures",
    )
    max_attempts: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum number of retry attempts",
    )
    backoff_base_ms: int = Field(
        default=100,
        ge=10,
        le=10000,
        description="Base backoff time in milliseconds",
    )
    backoff_max_ms: int = Field(
        default=5000,
        ge=100,
        le=60000,
        description="Maximum backoff time in milliseconds",
    )

    @model_validator(mode="after")
    def validate_backoff_order(self) -> "RetryConfig":
        """Ensure backoff_base_ms <= backoff_max_ms."""
        if self.backoff_base_ms > self.backoff_max_ms:
            raise ValueError("backoff_base_ms must be <= backoff_max_ms")
        return self


class TlsClientConfig(BaseModel):
    """TLS configuration for client connections to executor.

    Attributes:
        enabled: Enable TLS encryption. ENV: CODEMODE_TLS_ENABLED
        mode: Certificate mode ('system' or 'custom'). ENV: CODEMODE_TLS_MODE
        ca_file: CA certificate for server verification. ENV: CODEMODE_TLS_CA_FILE
        client_cert_file: Client certificate for mTLS. ENV: CODEMODE_TLS_CLIENT_CERT_FILE
        client_key_file: Client private key for mTLS. ENV: CODEMODE_TLS_CLIENT_KEY_FILE
    """

    model_config = ConfigDict(extra="forbid")

    enabled: bool = Field(
        default=False,
        description="Enable TLS encryption for executor connections",
    )
    mode: Literal["system", "custom"] = Field(
        default="system",
        description="Certificate mode: 'system' uses system CA, 'custom' uses provided files",
    )
    ca_file: str | None = Field(
        default=None,
        description="Path to CA certificate file for server verification (PEM format)",
    )
    client_cert_file: str | None = Field(
        default=None,
        description="Path to client certificate file for mTLS (PEM format)",
    )
    client_key_file: str | None = Field(
        default=None,
        description="Path to client private key file for mTLS (PEM format)",
    )

    @model_validator(mode="after")
    def validate_tls_files(self) -> "TlsClientConfig":
        """Validate TLS file paths when TLS is enabled with custom mode."""
        if self.enabled and self.mode == "custom":
            # mTLS validation: if one client cert field is set, both must be set
            if (self.client_cert_file and not self.client_key_file) or (
                self.client_key_file and not self.client_cert_file
            ):
                raise ValueError("Both client_cert_file and client_key_file must be set for mTLS")
        return self


class ObservabilityConfig(BaseModel):
    """Observability and logging configuration.

    Attributes:
        log_level: Logging level. ENV: CODEMODE_LOG_LEVEL
        include_correlation_id: Include correlation IDs in requests. ENV: CODEMODE_INCLUDE_CORRELATION_ID
        correlation_id_prefix: Prefix for generated correlation IDs. ENV: CODEMODE_CORRELATION_ID_PREFIX
        traceback_limit: Max traceback frames to include in errors. ENV: CODEMODE_TRACEBACK_LIMIT
    """

    model_config = ConfigDict(extra="forbid")

    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    include_correlation_id: bool = Field(
        default=True,
        description="Include correlation IDs in all requests for tracing",
    )
    correlation_id_prefix: str = Field(
        default="cm",
        min_length=1,
        max_length=8,
        description="Prefix for generated correlation IDs (e.g., 'cm' -> 'cm-2x5f9k-a7b3')",
    )
    traceback_limit: int = Field(
        default=5,
        ge=0,
        le=50,
        description="Maximum number of traceback frames to include in error responses (0 to disable)",
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is a valid Python logging level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Valid levels: {valid_levels}")
        return v_upper


class ClientConfig(BaseModel):
    """
    Configuration for the main application (client side).

    This configuration is used by applications that connect to the codemode
    executor sidecar. All fields support environment variable overrides.

    Attributes:
        executor_url: Executor service URL. ENV: CODEMODE_EXECUTOR_URL
        executor_api_key: API key for authentication. ENV: CODEMODE_EXECUTOR_API_KEY
        executor_timeout: Request timeout in seconds. ENV: CODEMODE_EXECUTOR_TIMEOUT
        max_code_length: Maximum code length to send. ENV: CODEMODE_MAX_CODE_LENGTH
        retry: Retry configuration for transient failures.
        tls: TLS configuration for secure connections.
        observability: Logging and tracing configuration.

    Example:
        >>> config = ClientConfig(
        ...     executor_url="http://executor:8001",
        ...     executor_api_key="secret-key",
        ...     executor_timeout=30,
        ...     retry=RetryConfig(enabled=True, max_attempts=3),
        ... )

    Environment Variables:
        CODEMODE_EXECUTOR_URL: Executor service URL
        CODEMODE_EXECUTOR_API_KEY: API key for authentication
        CODEMODE_EXECUTOR_TIMEOUT: Request timeout in seconds
        CODEMODE_MAX_CODE_LENGTH: Maximum code length in characters
        CODEMODE_RETRY_ENABLED: Enable retry on transient failures
        CODEMODE_RETRY_MAX_ATTEMPTS: Maximum retry attempts
        CODEMODE_RETRY_BACKOFF_BASE_MS: Base backoff time in ms
        CODEMODE_RETRY_BACKOFF_MAX_MS: Maximum backoff time in ms
        CODEMODE_TLS_ENABLED: Enable TLS encryption
        CODEMODE_TLS_MODE: 'system' or 'custom'
        CODEMODE_TLS_CA_FILE: CA certificate path
        CODEMODE_TLS_CLIENT_CERT_FILE: Client certificate path
        CODEMODE_TLS_CLIENT_KEY_FILE: Client key path
        CODEMODE_LOG_LEVEL: Logging level
        CODEMODE_INCLUDE_CORRELATION_ID: Include correlation IDs
        CODEMODE_CORRELATION_ID_PREFIX: Correlation ID prefix
        CODEMODE_TRACEBACK_LIMIT: Max traceback frames
    """

    model_config = ConfigDict(extra="forbid")

    # Executor connection
    executor_url: str = Field(
        ...,
        description="Executor service URL (e.g., 'http://executor:8001')",
    )
    executor_api_key: str = Field(
        ...,
        description="API key for executor authentication",
    )
    executor_timeout: int = Field(
        default=35,
        ge=1,
        le=600,
        description="Request timeout in seconds",
    )

    # Code limits
    max_code_length: int = Field(
        default=10000,
        ge=100,
        le=100000,
        description="Maximum code length in characters (validated before sending)",
    )

    # Nested configurations
    retry: RetryConfig = Field(
        default_factory=RetryConfig,
        description="Retry configuration for transient failures",
    )
    tls: TlsClientConfig = Field(
        default_factory=TlsClientConfig,
        description="TLS configuration for secure connections",
    )
    observability: ObservabilityConfig = Field(
        default_factory=ObservabilityConfig,
        description="Logging and tracing configuration",
    )

    @field_validator("executor_url")
    @classmethod
    def validate_executor_url(cls, v: str) -> str:
        """Validate and normalize executor URL."""
        if not v.startswith(("http://", "https://", "grpc://", "grpcs://")):
            raise ValueError("executor_url must start with http://, https://, grpc://, or grpcs://")
        return v.rstrip("/")

    @classmethod
    def from_env(cls) -> "ClientConfig":
        """
        Create ClientConfig from environment variables only.

        This method allows configuration without any YAML files, useful for
        containerized deployments where all config comes from env vars.

        Returns:
            ClientConfig instance populated from environment variables.

        Raises:
            ValueError: If required environment variables are missing.

        Example:
            >>> import os
            >>> os.environ["CODEMODE_EXECUTOR_URL"] = "http://executor:8001"
            >>> os.environ["CODEMODE_EXECUTOR_API_KEY"] = "secret"
            >>> config = ClientConfig.from_env()
        """
        # Required fields
        executor_url = os.environ.get("CODEMODE_EXECUTOR_URL")
        executor_api_key = os.environ.get("CODEMODE_EXECUTOR_API_KEY")

        if not executor_url:
            raise ValueError("CODEMODE_EXECUTOR_URL environment variable is required")
        if not executor_api_key:
            raise ValueError("CODEMODE_EXECUTOR_API_KEY environment variable is required")

        # Optional fields with defaults
        executor_timeout = int(os.environ.get("CODEMODE_EXECUTOR_TIMEOUT", "35"))
        max_code_length = int(os.environ.get("CODEMODE_MAX_CODE_LENGTH", "10000"))

        # Retry config
        retry = RetryConfig(
            enabled=os.environ.get("CODEMODE_RETRY_ENABLED", "true").lower() == "true",
            max_attempts=int(os.environ.get("CODEMODE_RETRY_MAX_ATTEMPTS", "3")),
            backoff_base_ms=int(os.environ.get("CODEMODE_RETRY_BACKOFF_BASE_MS", "100")),
            backoff_max_ms=int(os.environ.get("CODEMODE_RETRY_BACKOFF_MAX_MS", "5000")),
        )

        # TLS config
        tls = TlsClientConfig(
            enabled=os.environ.get("CODEMODE_TLS_ENABLED", "false").lower() == "true",
            mode=os.environ.get("CODEMODE_TLS_MODE", "system"),  # type: ignore[arg-type]
            ca_file=os.environ.get("CODEMODE_TLS_CA_FILE"),
            client_cert_file=os.environ.get("CODEMODE_TLS_CLIENT_CERT_FILE"),
            client_key_file=os.environ.get("CODEMODE_TLS_CLIENT_KEY_FILE"),
        )

        # Observability config
        observability = ObservabilityConfig(
            log_level=os.environ.get("CODEMODE_LOG_LEVEL", "INFO"),
            include_correlation_id=os.environ.get("CODEMODE_INCLUDE_CORRELATION_ID", "true").lower()
            == "true",
            correlation_id_prefix=os.environ.get("CODEMODE_CORRELATION_ID_PREFIX", "cm"),
            traceback_limit=int(os.environ.get("CODEMODE_TRACEBACK_LIMIT", "5")),
        )

        return cls(
            executor_url=executor_url,
            executor_api_key=executor_api_key,
            executor_timeout=executor_timeout,
            max_code_length=max_code_length,
            retry=retry,
            tls=tls,
            observability=observability,
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert configuration to dictionary for serialization.

        Returns:
            Dictionary representation of the configuration.
        """
        return self.model_dump()

    def __repr__(self) -> str:
        """Return string representation (hides API key)."""
        return (
            f"ClientConfig("
            f"executor_url={self.executor_url!r}, "
            f"executor_api_key='***', "
            f"executor_timeout={self.executor_timeout})"
        )
