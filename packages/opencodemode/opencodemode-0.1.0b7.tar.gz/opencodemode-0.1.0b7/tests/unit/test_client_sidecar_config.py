"""
Unit tests for ClientConfig and SidecarConfig models.

Tests the new configuration models for client applications and sidecar services.
"""

import os
from unittest.mock import patch

import pytest

from codemode.config import (
    ClientConfig,
    ConfigLoader,
    ExecutionLimitsConfig,
    ObservabilityConfig,
    RetryConfig,
    SecurityConfig,
    SidecarConfig,
    TlsClientConfig,
    TlsServerConfig,
)

# =============================================================================
# ClientConfig Tests
# =============================================================================


class TestClientConfigBasic:
    """Test basic ClientConfig functionality."""

    def test_minimal_config(self):
        """Test creating ClientConfig with minimal required fields."""
        config = ClientConfig(
            executor_url="http://localhost:8001",
            executor_api_key="test-key",
        )

        assert config.executor_url == "http://localhost:8001"
        assert config.executor_api_key == "test-key"
        assert config.executor_timeout == 35  # Default
        assert config.max_code_length == 10000  # Default

    def test_full_config(self):
        """Test creating ClientConfig with all fields."""
        config = ClientConfig(
            executor_url="https://executor.example.com:8001",
            executor_api_key="secret-key",
            executor_timeout=60,
            max_code_length=20000,
            retry=RetryConfig(
                enabled=True,
                max_attempts=5,
                backoff_base_ms=200,
                backoff_max_ms=10000,
            ),
            tls=TlsClientConfig(
                enabled=True,
                mode="custom",
                ca_file="/path/to/ca.crt",
            ),
            observability=ObservabilityConfig(
                log_level="DEBUG",
                include_correlation_id=True,
                correlation_id_prefix="myapp",
                traceback_limit=10,
            ),
        )

        assert config.executor_timeout == 60
        assert config.retry.max_attempts == 5
        assert config.tls.enabled is True
        assert config.observability.log_level == "DEBUG"

    def test_url_validation_http(self):
        """Test that http:// URLs are valid."""
        config = ClientConfig(
            executor_url="http://localhost:8001",
            executor_api_key="key",
        )
        assert config.executor_url == "http://localhost:8001"

    def test_url_validation_https(self):
        """Test that https:// URLs are valid."""
        config = ClientConfig(
            executor_url="https://executor.example.com:8001",
            executor_api_key="key",
        )
        assert config.executor_url == "https://executor.example.com:8001"

    def test_url_validation_grpc(self):
        """Test that grpc:// URLs are valid."""
        config = ClientConfig(
            executor_url="grpc://localhost:8001",
            executor_api_key="key",
        )
        assert config.executor_url == "grpc://localhost:8001"

    def test_url_validation_invalid(self):
        """Test that invalid URLs are rejected."""
        with pytest.raises(ValueError, match="executor_url must start with"):
            ClientConfig(
                executor_url="localhost:8001",  # Missing scheme
                executor_api_key="key",
            )

    def test_url_trailing_slash_removed(self):
        """Test that trailing slashes are removed from URLs."""
        config = ClientConfig(
            executor_url="http://localhost:8001/",
            executor_api_key="key",
        )
        assert config.executor_url == "http://localhost:8001"

    def test_repr_hides_api_key(self):
        """Test that __repr__ hides the API key."""
        config = ClientConfig(
            executor_url="http://localhost:8001",
            executor_api_key="super-secret-key",
        )
        repr_str = repr(config)
        assert "super-secret-key" not in repr_str
        assert "***" in repr_str

    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = ClientConfig(
            executor_url="http://localhost:8001",
            executor_api_key="key",
        )
        d = config.to_dict()

        assert d["executor_url"] == "http://localhost:8001"
        assert d["executor_api_key"] == "key"
        assert "retry" in d
        assert "tls" in d


class TestClientConfigRetry:
    """Test RetryConfig validation."""

    def test_retry_defaults(self):
        """Test retry default values."""
        config = RetryConfig()

        assert config.enabled is True
        assert config.max_attempts == 3
        assert config.backoff_base_ms == 100
        assert config.backoff_max_ms == 5000

    def test_retry_backoff_validation(self):
        """Test that backoff_base_ms must be <= backoff_max_ms."""
        with pytest.raises(ValueError, match="backoff_base_ms must be <= backoff_max_ms"):
            RetryConfig(
                backoff_base_ms=10000,
                backoff_max_ms=5000,
            )


class TestClientConfigTls:
    """Test TlsClientConfig validation."""

    def test_tls_disabled_by_default(self):
        """Test TLS is disabled by default."""
        config = TlsClientConfig()
        assert config.enabled is False

    def test_tls_mtls_validation(self):
        """Test that mTLS requires both cert and key."""
        with pytest.raises(ValueError, match="Both client_cert_file and client_key_file"):
            TlsClientConfig(
                enabled=True,
                mode="custom",
                client_cert_file="/path/to/cert.crt",
                # Missing client_key_file
            )


class TestClientConfigObservability:
    """Test ObservabilityConfig validation."""

    def test_log_level_validation(self):
        """Test that log level is validated."""
        with pytest.raises(ValueError, match="Invalid log level"):
            ObservabilityConfig(log_level="INVALID")

    def test_log_level_case_insensitive(self):
        """Test that log level is case-insensitive."""
        config = ObservabilityConfig(log_level="debug")
        assert config.log_level == "DEBUG"


class TestClientConfigFromEnv:
    """Test loading ClientConfig from environment variables."""

    def test_from_env_minimal(self):
        """Test loading from env with minimal config."""
        with patch.dict(
            os.environ,
            {
                "CODEMODE_EXECUTOR_URL": "http://executor:8001",
                "CODEMODE_EXECUTOR_API_KEY": "env-secret",
            },
            clear=False,
        ):
            config = ClientConfig.from_env()

        assert config.executor_url == "http://executor:8001"
        assert config.executor_api_key == "env-secret"

    def test_from_env_missing_url(self):
        """Test error when CODEMODE_EXECUTOR_URL is missing."""
        with patch.dict(
            os.environ,
            {
                "CODEMODE_EXECUTOR_API_KEY": "secret",
            },
            clear=True,
        ):
            with pytest.raises(ValueError, match="CODEMODE_EXECUTOR_URL"):
                ClientConfig.from_env()

    def test_from_env_missing_api_key(self):
        """Test error when CODEMODE_EXECUTOR_API_KEY is missing."""
        with patch.dict(
            os.environ,
            {
                "CODEMODE_EXECUTOR_URL": "http://localhost:8001",
            },
            clear=True,
        ):
            with pytest.raises(ValueError, match="CODEMODE_EXECUTOR_API_KEY"):
                ClientConfig.from_env()

    def test_from_env_all_options(self):
        """Test loading all options from env."""
        with patch.dict(
            os.environ,
            {
                "CODEMODE_EXECUTOR_URL": "http://executor:8001",
                "CODEMODE_EXECUTOR_API_KEY": "key",
                "CODEMODE_EXECUTOR_TIMEOUT": "60",
                "CODEMODE_MAX_CODE_LENGTH": "20000",
                "CODEMODE_RETRY_ENABLED": "false",
                "CODEMODE_RETRY_MAX_ATTEMPTS": "5",
                "CODEMODE_LOG_LEVEL": "DEBUG",
                "CODEMODE_CORRELATION_ID_PREFIX": "myapp",
            },
            clear=False,
        ):
            config = ClientConfig.from_env()

        assert config.executor_timeout == 60
        assert config.max_code_length == 20000
        assert config.retry.enabled is False
        assert config.retry.max_attempts == 5
        assert config.observability.log_level == "DEBUG"
        assert config.observability.correlation_id_prefix == "myapp"


# =============================================================================
# SidecarConfig Tests
# =============================================================================


class TestSidecarConfigBasic:
    """Test basic SidecarConfig functionality."""

    def test_defaults(self):
        """Test SidecarConfig with all defaults."""
        config = SidecarConfig()

        assert config.port == 8001
        assert config.host == "0.0.0.0"
        assert config.main_app_grpc_target == "localhost:50051"
        assert config.api_key is None
        assert config.log_level == "INFO"

    def test_full_config(self):
        """Test SidecarConfig with all fields."""
        config = SidecarConfig(
            port=9001,
            host="127.0.0.1",
            main_app_grpc_target="app:50051",
            api_key="sidecar-key",
            limits=ExecutionLimitsConfig(
                code_timeout=60,
                max_code_length=50000,
            ),
            security=SecurityConfig(
                allow_direct_execution=True,
                allowed_commands=["grep", "cat", "ls"],
            ),
            log_level="DEBUG",
        )

        assert config.port == 9001
        assert config.limits.code_timeout == 60
        assert config.security.allow_direct_execution is True
        assert "grep" in config.security.allowed_commands

    def test_grpc_target_validation(self):
        """Test that main_app_grpc_target must have host:port format."""
        with pytest.raises(ValueError, match="host:port format"):
            SidecarConfig(main_app_grpc_target="localhost")  # Missing port

    def test_log_level_validation(self):
        """Test that log level is validated."""
        with pytest.raises(ValueError, match="Invalid log level"):
            SidecarConfig(log_level="INVALID")

    def test_get_grpc_address(self):
        """Test get_grpc_address helper."""
        config = SidecarConfig(host="0.0.0.0", port=9001)
        assert config.get_grpc_address() == "0.0.0.0:9001"

    def test_repr_hides_api_key(self):
        """Test that __repr__ hides the API key."""
        config = SidecarConfig(api_key="super-secret")
        repr_str = repr(config)
        assert "super-secret" not in repr_str
        assert "***" in repr_str


class TestSidecarConfigTls:
    """Test TLS configuration for sidecar."""

    def test_server_tls_requires_cert_and_key(self):
        """Test that server TLS requires both cert and key."""
        with pytest.raises(ValueError, match="Both cert_file and key_file are required"):
            TlsServerConfig(
                enabled=True,
                mode="custom",
                cert_file="/path/to/cert.crt",
                # Missing key_file
            )

    def test_mtls_requires_ca_file(self):
        """Test that mTLS client auth requires CA file."""
        with pytest.raises(ValueError, match="ca_file is required"):
            TlsServerConfig(
                enabled=True,
                mode="custom",
                cert_file="/path/to/cert.crt",
                key_file="/path/to/key.key",
                require_client_auth=True,
                # Missing ca_file
            )


class TestSidecarConfigFromEnv:
    """Test loading SidecarConfig from environment variables."""

    def test_from_env_defaults(self):
        """Test loading from env with defaults."""
        with patch.dict(os.environ, {}, clear=True):
            config = SidecarConfig.from_env()

        assert config.port == 8001
        assert config.host == "0.0.0.0"
        assert config.api_key is None

    def test_from_env_all_options(self):
        """Test loading all options from env."""
        with patch.dict(
            os.environ,
            {
                "CODEMODE_SIDECAR_PORT": "9001",
                "CODEMODE_SIDECAR_HOST": "127.0.0.1",
                "CODEMODE_MAIN_APP_TARGET": "app:50051",
                "CODEMODE_API_KEY": "env-key",
                "CODEMODE_CODE_TIMEOUT": "60",
                "CODEMODE_MAX_CODE_LENGTH": "50000",
                "CODEMODE_ALLOW_DIRECT_EXECUTION": "true",
                "CODEMODE_ALLOWED_COMMANDS": "grep,cat,ls",
                "CODEMODE_LOG_LEVEL": "DEBUG",
            },
            clear=True,
        ):
            config = SidecarConfig.from_env()

        assert config.port == 9001
        assert config.host == "127.0.0.1"
        assert config.main_app_grpc_target == "app:50051"
        assert config.api_key == "env-key"
        assert config.limits.code_timeout == 60
        assert config.limits.max_code_length == 50000
        assert config.security.allow_direct_execution is True
        assert config.security.allowed_commands == ["grep", "cat", "ls"]
        assert config.log_level == "DEBUG"


# =============================================================================
# ConfigLoader Tests for New Configs
# =============================================================================


class TestConfigLoaderClientConfig:
    """Test ConfigLoader methods for ClientConfig."""

    def test_load_client_config_from_file(self, tmp_path):
        """Test loading ClientConfig from YAML file."""
        config_file = tmp_path / "codemode-client.yaml"
        config_file.write_text(
            """
executor_url: http://executor:8001
executor_api_key: file-key
executor_timeout: 45
max_code_length: 15000

retry:
  enabled: true
  max_attempts: 5

observability:
  log_level: DEBUG
"""
        )

        config = ConfigLoader.load_client_config(config_file)

        assert config.executor_url == "http://executor:8001"
        assert config.executor_api_key == "file-key"
        assert config.executor_timeout == 45
        assert config.retry.max_attempts == 5
        assert config.observability.log_level == "DEBUG"

    def test_load_client_config_from_dict(self):
        """Test loading ClientConfig from dictionary."""
        config = ConfigLoader.load_client_config_from_dict(
            {
                "executor_url": "http://localhost:8001",
                "executor_api_key": "dict-key",
            }
        )

        assert config.executor_url == "http://localhost:8001"
        assert config.executor_api_key == "dict-key"

    def test_load_client_config_from_env(self):
        """Test loading ClientConfig from environment."""
        with patch.dict(
            os.environ,
            {
                "CODEMODE_EXECUTOR_URL": "http://executor:8001",
                "CODEMODE_EXECUTOR_API_KEY": "env-key",
            },
            clear=False,
        ):
            config = ConfigLoader.load_client_config_from_env()

        assert config.executor_url == "http://executor:8001"
        assert config.executor_api_key == "env-key"

    def test_load_client_config_file_not_found(self):
        """Test error when client config file not found."""
        with pytest.raises(FileNotFoundError, match="Client configuration file not found"):
            ConfigLoader.load_client_config("nonexistent.yaml")

    def test_load_client_config_with_env_substitution(self, tmp_path):
        """Test env var substitution in client config."""
        config_file = tmp_path / "codemode-client.yaml"
        config_file.write_text(
            """
executor_url: ${MY_EXECUTOR_URL}
executor_api_key: ${MY_API_KEY}
"""
        )

        with patch.dict(
            os.environ,
            {
                "MY_EXECUTOR_URL": "http://from-env:8001",
                "MY_API_KEY": "from-env-key",
            },
        ):
            config = ConfigLoader.load_client_config(config_file)

        assert config.executor_url == "http://from-env:8001"
        assert config.executor_api_key == "from-env-key"


class TestConfigLoaderSidecarConfig:
    """Test ConfigLoader methods for SidecarConfig."""

    def test_load_sidecar_config_from_file(self, tmp_path):
        """Test loading SidecarConfig from YAML file."""
        config_file = tmp_path / "codemode-sidecar.yaml"
        config_file.write_text(
            """
port: 9001
host: "0.0.0.0"
main_app_grpc_target: app:50051
api_key: file-key

limits:
  code_timeout: 60
  max_code_length: 50000

security:
  allow_direct_execution: true
  allowed_commands:
    - grep
    - cat

log_level: DEBUG
"""
        )

        config = ConfigLoader.load_sidecar_config(config_file)

        assert config.port == 9001
        assert config.main_app_grpc_target == "app:50051"
        assert config.limits.code_timeout == 60
        assert config.security.allow_direct_execution is True
        assert config.log_level == "DEBUG"

    def test_load_sidecar_config_from_dict(self):
        """Test loading SidecarConfig from dictionary."""
        config = ConfigLoader.load_sidecar_config_from_dict(
            {
                "port": 9001,
                "api_key": "dict-key",
            }
        )

        assert config.port == 9001
        assert config.api_key == "dict-key"

    def test_load_sidecar_config_file_not_found(self):
        """Test error when sidecar config file not found."""
        with pytest.raises(FileNotFoundError, match="Sidecar configuration file not found"):
            ConfigLoader.load_sidecar_config("nonexistent.yaml")
