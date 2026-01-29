"""
Sidecar (executor) configuration for codemode executor service.

This module defines the SidecarConfig model used by the executor sidecar
that runs code in isolation. All fields support environment variable
overrides for containerized deployments.

Environment Variables:
    All configuration options can be set via environment variables with the
    CODEMODE_ prefix. See individual field descriptions for specific variable names.

Example:
    Loading from YAML file:
        >>> from codemode.config import SidecarConfigLoader
        >>> config = SidecarConfigLoader.load("codemode-sidecar.yaml")

    Loading from environment only:
        >>> config = SidecarConfig.from_env()

    Programmatic configuration:
        >>> config = SidecarConfig(
        ...     port=8001,
        ...     main_app_grpc_target="app:50051",
        ... )
"""

import logging
import os
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

logger = logging.getLogger(__name__)


class ExecutionLimitsConfig(BaseModel):
    """Execution limits for code safety.

    Attributes:
        code_timeout: Maximum execution time in seconds. ENV: CODEMODE_CODE_TIMEOUT
        max_code_length: Maximum code length in characters. ENV: CODEMODE_MAX_CODE_LENGTH
    """

    model_config = ConfigDict(extra="forbid")

    code_timeout: int = Field(
        default=30,
        ge=1,
        le=300,
        description="Maximum code execution time in seconds",
    )
    max_code_length: int = Field(
        default=10000,
        ge=100,
        le=100000,
        description="Maximum code length in characters",
    )


class SecurityConfig(BaseModel):
    """Security settings for code execution.

    Attributes:
        allow_direct_execution: Allow direct system commands. ENV: CODEMODE_ALLOW_DIRECT_EXECUTION
        allowed_commands: List of allowed system commands. ENV: CODEMODE_ALLOWED_COMMANDS
    """

    model_config = ConfigDict(extra="forbid")

    allow_direct_execution: bool = Field(
        default=False,
        description="Allow direct system commands and file operations",
    )
    allowed_commands: list[str] = Field(
        default_factory=list,
        description="List of allowed system commands when direct execution is enabled",
    )


class TlsServerConfig(BaseModel):
    """TLS configuration for the sidecar gRPC server.

    Attributes:
        enabled: Enable TLS encryption. ENV: CODEMODE_TLS_ENABLED
        mode: Certificate mode ('system' or 'custom'). ENV: CODEMODE_TLS_MODE
        cert_file: Server certificate path. ENV: CODEMODE_TLS_CERT_FILE
        key_file: Server private key path. ENV: CODEMODE_TLS_KEY_FILE
        ca_file: CA certificate for client verification. ENV: CODEMODE_TLS_CA_FILE
        require_client_auth: Require mTLS client authentication. ENV: CODEMODE_TLS_REQUIRE_CLIENT_AUTH
    """

    model_config = ConfigDict(extra="forbid")

    enabled: bool = Field(
        default=False,
        description="Enable TLS encryption for incoming connections",
    )
    mode: Literal["system", "custom"] = Field(
        default="system",
        description="Certificate mode: 'system' uses system CA, 'custom' uses provided files",
    )
    cert_file: str | None = Field(
        default=None,
        description="Path to server certificate file (PEM format)",
    )
    key_file: str | None = Field(
        default=None,
        description="Path to server private key file (PEM format)",
    )
    ca_file: str | None = Field(
        default=None,
        description="Path to CA certificate file for client verification (PEM format)",
    )
    require_client_auth: bool = Field(
        default=False,
        description="Require mTLS client certificate authentication",
    )

    @model_validator(mode="after")
    def validate_tls_files(self) -> "TlsServerConfig":
        """Validate TLS file paths when TLS is enabled with custom mode."""
        if self.enabled and self.mode == "custom":
            # Server must have both cert and key
            if not self.cert_file or not self.key_file:
                raise ValueError(
                    "Both cert_file and key_file are required when TLS is enabled with custom mode"
                )
            # If requiring client auth, CA file should be provided
            if self.require_client_auth and not self.ca_file:
                raise ValueError("ca_file is required when require_client_auth is True")
        return self


class CallbackTlsConfig(BaseModel):
    """TLS configuration for callback connections to the main app.

    Attributes:
        enabled: Enable TLS for callback connections. ENV: CODEMODE_CALLBACK_TLS_ENABLED
        ca_file: CA certificate for server verification. ENV: CODEMODE_CALLBACK_TLS_CA_FILE
        client_cert: Client certificate for mTLS. ENV: CODEMODE_CALLBACK_TLS_CLIENT_CERT
        client_key: Client private key for mTLS. ENV: CODEMODE_CALLBACK_TLS_CLIENT_KEY
    """

    model_config = ConfigDict(extra="forbid")

    enabled: bool = Field(
        default=False,
        description="Enable TLS for callback connections to main app",
    )
    ca_file: str | None = Field(
        default=None,
        description="Path to CA certificate for main app verification (PEM format)",
    )
    client_cert: str | None = Field(
        default=None,
        description="Path to client certificate for mTLS callbacks (PEM format)",
    )
    client_key: str | None = Field(
        default=None,
        description="Path to client private key for mTLS callbacks (PEM format)",
    )

    @model_validator(mode="after")
    def validate_callback_tls(self) -> "CallbackTlsConfig":
        """Validate callback TLS configuration."""
        if self.enabled:
            # mTLS validation: if one client cert field is set, both must be set
            if (self.client_cert and not self.client_key) or (
                self.client_key and not self.client_cert
            ):
                raise ValueError("Both client_cert and client_key must be set for mTLS callbacks")
        return self


class SidecarConfig(BaseModel):
    """
    Configuration for the executor sidecar.

    This configuration is used by the codemode executor sidecar service that
    runs code in isolation. All fields support environment variable overrides.

    Attributes:
        port: gRPC server port. ENV: CODEMODE_SIDECAR_PORT
        host: gRPC server host binding. ENV: CODEMODE_SIDECAR_HOST
        main_app_grpc_target: Main app gRPC target for callbacks. ENV: CODEMODE_MAIN_APP_TARGET
        api_key: API key for authentication. ENV: CODEMODE_API_KEY
        limits: Execution limits configuration.
        security: Security settings for code execution.
        tls: TLS configuration for the gRPC server.
        callback_tls: TLS configuration for callbacks to main app.
        log_level: Logging level. ENV: CODEMODE_LOG_LEVEL

    Example:
        >>> config = SidecarConfig(
        ...     port=8001,
        ...     main_app_grpc_target="app:50051",
        ...     api_key="secret-key",
        ... )

    Environment Variables:
        CODEMODE_SIDECAR_PORT: gRPC server port (default: 8001)
        CODEMODE_SIDECAR_HOST: gRPC server host (default: 0.0.0.0)
        CODEMODE_MAIN_APP_TARGET: Main app gRPC target (default: localhost:50051)
        CODEMODE_API_KEY: API key for authentication
        CODEMODE_CODE_TIMEOUT: Max execution time in seconds
        CODEMODE_MAX_CODE_LENGTH: Max code length in characters
        CODEMODE_ALLOW_DIRECT_EXECUTION: Allow direct system commands
        CODEMODE_ALLOWED_COMMANDS: Comma-separated list of allowed commands
        CODEMODE_TLS_ENABLED: Enable TLS for incoming connections
        CODEMODE_TLS_MODE: 'system' or 'custom'
        CODEMODE_TLS_CERT_FILE: Server certificate path
        CODEMODE_TLS_KEY_FILE: Server private key path
        CODEMODE_TLS_CA_FILE: CA certificate path
        CODEMODE_TLS_REQUIRE_CLIENT_AUTH: Require mTLS
        CODEMODE_CALLBACK_TLS_ENABLED: Enable TLS for callbacks
        CODEMODE_CALLBACK_TLS_CA_FILE: Callback CA certificate
        CODEMODE_CALLBACK_TLS_CLIENT_CERT: Callback client certificate
        CODEMODE_CALLBACK_TLS_CLIENT_KEY: Callback client key
        CODEMODE_LOG_LEVEL: Logging level
    """

    model_config = ConfigDict(extra="forbid")

    # Service binding
    port: int = Field(
        default=8001,
        ge=1,
        le=65535,
        description="gRPC server port",
    )
    host: str = Field(
        default="0.0.0.0",
        description="gRPC server host binding (use '0.0.0.0' for all interfaces)",
    )
    main_app_grpc_target: str = Field(
        default="localhost:50051",
        description="Main app gRPC target for tool callbacks (host:port)",
    )
    api_key: str | None = Field(
        default=None,
        description="API key for authentication (optional, but recommended)",
    )

    # Nested configurations
    limits: ExecutionLimitsConfig = Field(
        default_factory=ExecutionLimitsConfig,
        description="Execution limits for code safety",
    )
    security: SecurityConfig = Field(
        default_factory=SecurityConfig,
        description="Security settings for code execution",
    )
    tls: TlsServerConfig = Field(
        default_factory=TlsServerConfig,
        description="TLS configuration for the gRPC server",
    )
    callback_tls: CallbackTlsConfig = Field(
        default_factory=CallbackTlsConfig,
        description="TLS configuration for callbacks to main app",
    )

    # Observability
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
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

    @field_validator("main_app_grpc_target")
    @classmethod
    def validate_grpc_target(cls, v: str) -> str:
        """Validate gRPC target format (host:port)."""
        if ":" not in v:
            raise ValueError(
                "main_app_grpc_target must be in host:port format (e.g., 'localhost:50051')"
            )
        return v

    @classmethod
    def from_env(cls) -> "SidecarConfig":
        """
        Create SidecarConfig from environment variables only.

        This method allows configuration without any YAML files, useful for
        containerized deployments where all config comes from env vars.

        Returns:
            SidecarConfig instance populated from environment variables.

        Example:
            >>> import os
            >>> os.environ["CODEMODE_API_KEY"] = "secret"
            >>> config = SidecarConfig.from_env()
        """
        # Service binding
        port = int(os.environ.get("CODEMODE_SIDECAR_PORT", "8001"))
        host = os.environ.get("CODEMODE_SIDECAR_HOST", "0.0.0.0")
        main_app_grpc_target = os.environ.get("CODEMODE_MAIN_APP_TARGET", "localhost:50051")
        api_key = os.environ.get("CODEMODE_API_KEY")

        # Execution limits
        limits = ExecutionLimitsConfig(
            code_timeout=int(os.environ.get("CODEMODE_CODE_TIMEOUT", "30")),
            max_code_length=int(os.environ.get("CODEMODE_MAX_CODE_LENGTH", "10000")),
        )

        # Security config
        allowed_commands_str = os.environ.get("CODEMODE_ALLOWED_COMMANDS", "")
        allowed_commands = (
            [cmd.strip() for cmd in allowed_commands_str.split(",") if cmd.strip()]
            if allowed_commands_str
            else []
        )
        security = SecurityConfig(
            allow_direct_execution=os.environ.get(
                "CODEMODE_ALLOW_DIRECT_EXECUTION", "false"
            ).lower()
            == "true",
            allowed_commands=allowed_commands,
        )

        # TLS server config
        tls = TlsServerConfig(
            enabled=os.environ.get("CODEMODE_TLS_ENABLED", "false").lower() == "true",
            mode=os.environ.get("CODEMODE_TLS_MODE", "system"),  # type: ignore[arg-type]
            cert_file=os.environ.get("CODEMODE_TLS_CERT_FILE"),
            key_file=os.environ.get("CODEMODE_TLS_KEY_FILE"),
            ca_file=os.environ.get("CODEMODE_TLS_CA_FILE"),
            require_client_auth=os.environ.get("CODEMODE_TLS_REQUIRE_CLIENT_AUTH", "false").lower()
            == "true",
        )

        # Callback TLS config
        callback_tls = CallbackTlsConfig(
            enabled=os.environ.get("CODEMODE_CALLBACK_TLS_ENABLED", "false").lower() == "true",
            ca_file=os.environ.get("CODEMODE_CALLBACK_TLS_CA_FILE"),
            client_cert=os.environ.get("CODEMODE_CALLBACK_TLS_CLIENT_CERT"),
            client_key=os.environ.get("CODEMODE_CALLBACK_TLS_CLIENT_KEY"),
        )

        # Log level
        log_level = os.environ.get("CODEMODE_LOG_LEVEL", "INFO")

        return cls(
            port=port,
            host=host,
            main_app_grpc_target=main_app_grpc_target,
            api_key=api_key,
            limits=limits,
            security=security,
            tls=tls,
            callback_tls=callback_tls,
            log_level=log_level,
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert configuration to dictionary for serialization.

        Returns:
            Dictionary representation of the configuration.
        """
        return self.model_dump()

    def get_grpc_address(self) -> str:
        """
        Get the full gRPC address for server binding.

        Returns:
            Address string in format 'host:port'.
        """
        return f"{self.host}:{self.port}"

    def __repr__(self) -> str:
        """Return string representation (hides API key)."""
        api_key_display = "'***'" if self.api_key else "None"
        return (
            f"SidecarConfig("
            f"host={self.host!r}, "
            f"port={self.port}, "
            f"api_key={api_key_display}, "
            f"main_app_grpc_target={self.main_app_grpc_target!r})"
        )
