"""
Configuration models using Pydantic for validation.

This module defines the schema for codemode.yaml configuration files.
"""

import logging
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

logger = logging.getLogger(__name__)


class ProjectConfig(BaseModel):
    """Project metadata configuration."""

    model_config = ConfigDict(extra="forbid")  # Raise error on unknown fields

    name: str = Field(..., description="Project name")
    version: str | None = Field("1.0.0", description="Project version")


class FrameworkConfig(BaseModel):
    """Framework integration configuration."""

    model_config = ConfigDict(extra="allow")  # Allow framework-specific config

    type: str = Field(..., description="Framework type (crewai, langchain, langgraph)")
    auto_discover: bool = Field(False, description="Enable auto-discovery of components")

    @field_validator("type")
    @classmethod
    def validate_framework_type(cls, v: str) -> str:
        """Validate framework type is supported."""
        supported = ["crewai", "langchain", "langgraph"]
        if v.lower() not in supported:
            raise ValueError(f"Unsupported framework: {v}. Supported frameworks: {supported}")
        return v.lower()


class ExecutorLimitsConfig(BaseModel):
    """Resource limits for code execution."""

    model_config = ConfigDict(extra="forbid")

    code_timeout: int = Field(
        30, ge=1, le=300, description="Maximum code execution time in seconds"
    )
    max_code_length: int = Field(
        10000, ge=100, le=100000, description="Maximum code length in characters"
    )
    memory_limit: str = Field("512Mi", description="Container memory limit (e.g., '512Mi', '1Gi')")


class VolumeConfig(BaseModel):
    """Volume mount configuration."""

    model_config = ConfigDict(extra="forbid")

    mount: str = Field(..., description="Local path to mount")
    readonly: bool = Field(True, description="Whether volume is read-only")
    max_size: str | None = Field(None, description="Maximum size (e.g., '1GB', '512MB')")


class FilesystemConfig(BaseModel):
    """Filesystem access configuration."""

    model_config = ConfigDict(extra="allow")  # Allow additional custom volumes

    workspace: VolumeConfig | None = Field(
        None, description="Workspace volume (typically read-only project files)"
    )
    sandbox: VolumeConfig | None = Field(
        None, description="Sandbox volume (read-write scratch space)"
    )
    outputs: VolumeConfig | None = Field(
        None, description="Outputs volume (read-write for results)"
    )


class NetworkConfig(BaseModel):
    """Network access configuration."""

    model_config = ConfigDict(extra="forbid")

    mode: str = Field(
        "none",
        description="Network mode: 'none' (no network), 'restricted' (allow/deny lists), 'all' (full access)",
    )
    allowed_domains: list[str] = Field(
        default_factory=list,
        description="List of allowed domains (e.g., ['*.github.com', 'api.openai.com'])",
    )
    blocked_domains: list[str] = Field(default_factory=list, description="List of blocked domains")

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        """Validate network mode."""
        valid_modes = ["none", "restricted", "all"]
        if v not in valid_modes:
            raise ValueError(f"Invalid network mode: {v}. Valid modes: {valid_modes}")
        return v


class ExecutionConfig(BaseModel):
    """Execution behavior configuration."""

    model_config = ConfigDict(extra="forbid")

    allow_direct_execution: bool = Field(
        False, description="Allow direct system commands and file operations"
    )
    allowed_commands: list[str] = Field(
        default_factory=list,
        description="List of allowed system commands (e.g., ['grep', 'cat', 'ls'])",
    )


class GrpcTlsConfig(BaseModel):
    """TLS/mTLS configuration for gRPC connections."""

    model_config = ConfigDict(extra="forbid")

    enabled: bool = Field(False, description="Enable TLS encryption for gRPC connections")
    mode: Literal["system", "custom"] = Field(
        "system",
        description="Certificate mode: 'system' (use system certs) or 'custom' (use provided files)",
    )
    cert_file: str | None = Field(None, description="Path to server certificate file (PEM format)")
    key_file: str | None = Field(None, description="Path to server private key file (PEM format)")
    ca_file: str | None = Field(
        None, description="Path to CA certificate file for verification (PEM format)"
    )
    client_cert_file: str | None = Field(
        None, description="Path to client certificate file for mTLS (PEM format)"
    )
    client_key_file: str | None = Field(
        None, description="Path to client private key file for mTLS (PEM format)"
    )

    @model_validator(mode="after")
    def validate_tls_files(self) -> "GrpcTlsConfig":
        """Validate TLS file paths when TLS is enabled."""
        if self.enabled and self.mode == "custom":
            # Server cert validation: if one is provided, both must be provided
            # Note: cert_file/key_file are ONLY needed for servers, not clients
            if (self.cert_file and not self.key_file) or (self.key_file and not self.cert_file):
                raise ValueError("Both cert_file and key_file must be set together")

            # mTLS validation: if one client cert field is set, both must be set
            if (self.client_cert_file and not self.client_key_file) or (
                self.client_key_file and not self.client_cert_file
            ):
                raise ValueError(
                    "Both client_cert_file and client_key_file must be set for mTLS client authentication"
                )
        return self


class GrpcConfig(BaseModel):
    """gRPC communication configuration."""

    model_config = ConfigDict(extra="forbid")

    tls: GrpcTlsConfig = Field(
        default_factory=GrpcTlsConfig, description="TLS/mTLS configuration for secure communication"
    )
    tool_service_url: str = Field(
        default="localhost:50051",
        description="ToolService gRPC URL. Use 'host.docker.internal:50051' when executor runs in Docker.",
    )


class ExecutorConfig(BaseModel):
    """Executor service configuration."""

    model_config = ConfigDict(extra="forbid")

    url: str = Field(..., description="Executor service URL")
    api_key: str = Field(..., description="API key for executor authentication")
    timeout: int = Field(35, ge=1, le=600, description="HTTP request timeout in seconds")
    limits: ExecutorLimitsConfig = Field(
        default_factory=ExecutorLimitsConfig, description="Execution resource limits"
    )
    filesystem: FilesystemConfig | None = Field(None, description="Filesystem access configuration")
    network: NetworkConfig = Field(
        default_factory=NetworkConfig, description="Network access configuration"
    )
    execution: ExecutionConfig = Field(
        default_factory=ExecutionConfig, description="Execution behavior configuration"
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate URL format."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v.rstrip("/")  # Remove trailing slash


class CodemodeConfig(BaseModel):
    """
    Main configuration model for Codemode.

    This model validates and parses the codemode.yaml configuration file.

    Example:
        ```yaml
        project:
          name: my-app
          version: 1.0.0

        framework:
          type: crewai
          auto_discover: true

        executor:
          url: http://executor:8001
          api_key: secret123
          limits:
            code_timeout: 30
            max_code_length: 10000

        config:
          environment: production
          features:
            - analytics

        ```
    """

    model_config = ConfigDict(extra="forbid")  # Strict validation

    project: ProjectConfig = Field(..., description="Project configuration")
    framework: FrameworkConfig = Field(..., description="Framework configuration")
    executor: ExecutorConfig = Field(..., description="Executor configuration")
    grpc: GrpcConfig = Field(
        default_factory=GrpcConfig, description="gRPC communication configuration"
    )
    config: dict[str, Any] = Field(
        default_factory=dict, description="Additional configuration passed to executed code"
    )
    logging: dict[str, Any] = Field(
        default_factory=lambda: {"level": "INFO"}, description="Logging configuration"
    )

    def model_post_init(self, __context: Any) -> None:
        """Post-initialization hook for logging."""
        logger.debug(f"Loaded configuration for project: {self.project.name}")

    def get_tool_names(self) -> list[str]:
        """Get list of configured tool names (placeholder for future use)."""
        return []

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"CodemodeConfig("
            f"project={self.project.name}, "
            f"framework={self.framework.type}, "
            f"executor={self.executor.url})"
        )
