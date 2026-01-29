"""Configuration management for Codemode.

This module provides configuration classes for both client applications and
executor sidecars:

- ClientConfig: For main applications connecting to the executor
- SidecarConfig: For the executor sidecar service
- CodemodeConfig: Legacy unified configuration (deprecated)

Example:
    Load client configuration:
        >>> from codemode.config import ConfigLoader, ClientConfig
        >>> config = ConfigLoader.load_client_config("codemode-client.yaml")

    Load from environment:
        >>> config = ConfigLoader.load_client_config_from_env()

    Load sidecar configuration:
        >>> config = ConfigLoader.load_sidecar_config("codemode-sidecar.yaml")
"""

from codemode.config.client_config import (
    ClientConfig,
    ObservabilityConfig,
    RetryConfig,
    TlsClientConfig,
)
from codemode.config.loader import ConfigLoader, ConfigLoadError
from codemode.config.models import (
    CodemodeConfig,
    ExecutorConfig,
    ExecutorLimitsConfig,
    FrameworkConfig,
    ProjectConfig,
)
from codemode.config.sidecar_config import (
    CallbackTlsConfig,
    ExecutionLimitsConfig,
    SecurityConfig,
    SidecarConfig,
    TlsServerConfig,
)

__all__ = [
    # New configuration models (recommended)
    "ClientConfig",
    "SidecarConfig",
    # Client config components
    "RetryConfig",
    "TlsClientConfig",
    "ObservabilityConfig",
    # Sidecar config components
    "ExecutionLimitsConfig",
    "SecurityConfig",
    "TlsServerConfig",
    "CallbackTlsConfig",
    # Legacy configuration (deprecated)
    "CodemodeConfig",
    "ProjectConfig",
    "FrameworkConfig",
    "ExecutorConfig",
    "ExecutorLimitsConfig",
    # Loader
    "ConfigLoader",
    "ConfigLoadError",
]
