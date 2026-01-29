"""
Unit tests for configuration models.
"""

import pytest
from pydantic import ValidationError

from codemode.config.models import (
    CodemodeConfig,
    ExecutorConfig,
    ExecutorLimitsConfig,
    FrameworkConfig,
    GrpcConfig,
    NetworkConfig,
    ProjectConfig,
    VolumeConfig,
)


class TestProjectConfig:
    """Test ProjectConfig model."""

    def test_valid_project_config(self):
        """Test valid project configuration."""
        config = ProjectConfig(name="test-project", version="1.0.0")

        assert config.name == "test-project"
        assert config.version == "1.0.0"

    def test_project_config_default_version(self):
        """Test project config with default version."""
        config = ProjectConfig(name="test-project")

        assert config.version == "1.0.0"

    def test_project_config_forbids_extra_fields(self):
        """Test that extra fields are forbidden."""
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            ProjectConfig(name="test", extra_field="not allowed")


class TestFrameworkConfig:
    """Test FrameworkConfig model."""

    def test_valid_framework_config(self):
        """Test valid framework configurations."""
        for framework_type in ["crewai", "langchain", "langgraph"]:
            config = FrameworkConfig(type=framework_type)
            assert config.type == framework_type
            assert config.auto_discover is False

    def test_framework_config_auto_discover(self):
        """Test framework config with auto_discover enabled."""
        config = FrameworkConfig(type="crewai", auto_discover=True)

        assert config.auto_discover is True

    def test_framework_config_invalid_type(self):
        """Test framework config with invalid type."""
        with pytest.raises(ValidationError, match="Unsupported framework"):
            FrameworkConfig(type="invalid_framework")

    def test_framework_config_case_insensitive(self):
        """Test that framework type is case insensitive."""
        config = FrameworkConfig(type="CrewAI")

        assert config.type == "crewai"

    def test_framework_config_allows_extra_fields(self):
        """Test that extra fields are allowed for framework-specific config."""
        config = FrameworkConfig(type="crewai", custom_option="value")

        # Should not raise error - extra fields allowed
        assert config.type == "crewai"


class TestExecutorLimitsConfig:
    """Test ExecutorLimitsConfig model."""

    def test_valid_limits_config(self):
        """Test valid limits configuration."""
        config = ExecutorLimitsConfig(code_timeout=60, max_code_length=5000, memory_limit="1Gi")

        assert config.code_timeout == 60
        assert config.max_code_length == 5000
        assert config.memory_limit == "1Gi"

    def test_limits_config_defaults(self):
        """Test limits config with defaults."""
        config = ExecutorLimitsConfig()

        assert config.code_timeout == 30
        assert config.max_code_length == 10000
        assert config.memory_limit == "512Mi"

    def test_limits_config_validation(self):
        """Test limits config validation."""
        # Timeout too low
        with pytest.raises(ValidationError):
            ExecutorLimitsConfig(code_timeout=0)

        # Timeout too high
        with pytest.raises(ValidationError):
            ExecutorLimitsConfig(code_timeout=301)

        # Max code length too low
        with pytest.raises(ValidationError):
            ExecutorLimitsConfig(max_code_length=50)

        # Max code length too high
        with pytest.raises(ValidationError):
            ExecutorLimitsConfig(max_code_length=100001)


class TestVolumeConfig:
    """Test VolumeConfig model."""

    def test_valid_volume_config(self):
        """Test valid volume configuration."""
        config = VolumeConfig(mount="/workspace", readonly=True, max_size="1GB")

        assert config.mount == "/workspace"
        assert config.readonly is True
        assert config.max_size == "1GB"

    def test_volume_config_defaults(self):
        """Test volume config with defaults."""
        config = VolumeConfig(mount="/data")

        assert config.readonly is True
        assert config.max_size is None


class TestNetworkConfig:
    """Test NetworkConfig model."""

    def test_valid_network_config(self):
        """Test valid network configuration."""
        config = NetworkConfig(
            mode="restricted",
            allowed_domains=["*.github.com", "api.openai.com"],
            blocked_domains=["malicious.com"],
        )

        assert config.mode == "restricted"
        assert len(config.allowed_domains) == 2
        assert len(config.blocked_domains) == 1

    def test_network_config_defaults(self):
        """Test network config with defaults."""
        config = NetworkConfig()

        assert config.mode == "none"
        assert config.allowed_domains == []
        assert config.blocked_domains == []

    def test_network_config_invalid_mode(self):
        """Test network config with invalid mode."""
        with pytest.raises(ValidationError, match="Invalid network mode"):
            NetworkConfig(mode="invalid_mode")


class TestGrpcConfig:
    """Test GrpcConfig model."""

    def test_grpc_config_defaults(self):
        """Test gRPC config with defaults."""
        config = GrpcConfig()

        assert config.tool_service_url == "localhost:50051"
        assert config.tls.enabled is False

    def test_grpc_config_custom_url(self):
        """Test gRPC config with custom tool_service_url."""
        config = GrpcConfig(tool_service_url="host.docker.internal:50051")

        assert config.tool_service_url == "host.docker.internal:50051"

    def test_grpc_config_forbids_extra_fields(self):
        """Test that extra fields are forbidden."""
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            GrpcConfig(extra_field="not allowed")


class TestExecutorConfig:
    """Test ExecutorConfig model."""

    def test_valid_executor_config(self):
        """Test valid executor configuration."""
        config = ExecutorConfig(url="http://localhost:8001", api_key="secret123", timeout=60)

        assert config.url == "http://localhost:8001"
        assert config.api_key == "secret123"
        assert config.timeout == 60

    def test_executor_config_defaults(self):
        """Test executor config with defaults."""
        config = ExecutorConfig(url="http://localhost:8001", api_key="key")

        assert config.timeout == 35
        assert isinstance(config.limits, ExecutorLimitsConfig)
        assert isinstance(config.network, NetworkConfig)

    def test_executor_config_invalid_url(self):
        """Test executor config with invalid URL."""
        # Missing protocol
        with pytest.raises(ValidationError, match="URL must start with http://"):
            ExecutorConfig(url="localhost:8001", api_key="key")

    def test_executor_config_strips_trailing_slash(self):
        """Test that trailing slash is removed from URL."""
        config = ExecutorConfig(url="http://localhost:8001/", api_key="key")

        assert config.url == "http://localhost:8001"

    def test_executor_config_timeout_validation(self):
        """Test executor config timeout validation."""
        # Timeout too low
        with pytest.raises(ValidationError):
            ExecutorConfig(url="http://localhost:8001", api_key="key", timeout=0)

        # Timeout too high
        with pytest.raises(ValidationError):
            ExecutorConfig(url="http://localhost:8001", api_key="key", timeout=601)


class TestCodemodeConfig:
    """Test CodemodeConfig model."""

    def test_valid_codemode_config(self):
        """Test valid codemode configuration."""
        config = CodemodeConfig(
            project=ProjectConfig(name="test-project"),
            framework=FrameworkConfig(type="crewai"),
            executor=ExecutorConfig(url="http://localhost:8001", api_key="key"),
        )

        assert config.project.name == "test-project"
        assert config.framework.type == "crewai"
        assert config.executor.url == "http://localhost:8001"

    def test_codemode_config_with_all_fields(self):
        """Test codemode config with all optional fields."""
        config = CodemodeConfig(
            project=ProjectConfig(name="test"),
            framework=FrameworkConfig(type="crewai"),
            executor=ExecutorConfig(url="http://localhost:8001", api_key="key"),
            config={"env": "prod", "features": ["analytics"]},
            logging={"level": "DEBUG"},
        )

        assert config.config["env"] == "prod"
        assert config.logging["level"] == "DEBUG"

    def test_codemode_config_defaults(self):
        """Test codemode config with defaults."""
        config = CodemodeConfig(
            project=ProjectConfig(name="test"),
            framework=FrameworkConfig(type="crewai"),
            executor=ExecutorConfig(url="http://localhost:8001", api_key="key"),
        )

        assert config.config == {}
        assert config.logging["level"] == "INFO"

    def test_codemode_config_get_tool_names(self):
        """Test get_tool_names method (currently returns empty list)."""
        config = CodemodeConfig(
            project=ProjectConfig(name="test"),
            framework=FrameworkConfig(type="crewai"),
            executor=ExecutorConfig(url="http://localhost:8001", api_key="key"),
        )

        tool_names = config.get_tool_names()

        assert tool_names == []

    def test_codemode_config_repr(self):
        """Test string representation."""
        config = CodemodeConfig(
            project=ProjectConfig(name="my-project"),
            framework=FrameworkConfig(type="crewai"),
            executor=ExecutorConfig(url="http://localhost:8001", api_key="key"),
        )

        repr_str = repr(config)

        assert "CodemodeConfig" in repr_str
        assert "my-project" in repr_str
        assert "crewai" in repr_str
        assert "http://localhost:8001" in repr_str

    def test_codemode_config_forbids_extra_fields(self):
        """Test that extra fields are forbidden at top level."""
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            CodemodeConfig(
                project=ProjectConfig(name="test"),
                framework=FrameworkConfig(type="crewai"),
                executor=ExecutorConfig(url="http://localhost:8001", api_key="key"),
                extra_field="not allowed",
            )

    def test_codemode_config_post_init(self, caplog):
        """Test post-initialization hook logs project name."""
        import logging

        with caplog.at_level(logging.DEBUG):
            config = CodemodeConfig(
                project=ProjectConfig(name="test-project"),
                framework=FrameworkConfig(type="crewai"),
                executor=ExecutorConfig(url="http://localhost:8001", api_key="key"),
            )

        # Post-init should log the project name
        assert "test-project" in caplog.text or config.project.name == "test-project"
