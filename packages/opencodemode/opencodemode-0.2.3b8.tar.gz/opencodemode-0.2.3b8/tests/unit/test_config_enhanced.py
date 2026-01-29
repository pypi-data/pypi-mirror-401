"""
Unit tests for enhanced configuration models.
"""

import pytest
from pydantic import ValidationError

from codemode.config.models import (
    ExecutionConfig,
    ExecutorConfig,
    FilesystemConfig,
    NetworkConfig,
    VolumeConfig,
)


class TestVolumeConfig:
    """Test VolumeConfig model."""

    def test_valid_volume(self):
        """Test valid volume configuration."""
        volume = VolumeConfig(mount="./project_files", readonly=True, max_size="1GB")

        assert volume.mount == "./project_files"
        assert volume.readonly is True
        assert volume.max_size == "1GB"

    def test_readonly_default(self):
        """Test readonly defaults to True."""
        volume = VolumeConfig(mount="/workspace")

        assert volume.readonly is True
        assert volume.max_size is None


class TestFilesystemConfig:
    """Test FilesystemConfig model."""

    def test_valid_filesystem_config(self):
        """Test valid filesystem configuration."""
        config = FilesystemConfig(
            workspace=VolumeConfig(mount="./project_files", readonly=True),
            sandbox=VolumeConfig(mount="/sandbox", readonly=False, max_size="1GB"),
            outputs=VolumeConfig(mount="./outputs", readonly=False),
        )

        assert config.workspace.mount == "./project_files"
        assert config.workspace.readonly is True
        assert config.sandbox.readonly is False
        assert config.outputs.mount == "./outputs"

    def test_optional_volumes(self):
        """Test that all volumes are optional."""
        config = FilesystemConfig()

        assert config.workspace is None
        assert config.sandbox is None
        assert config.outputs is None


class TestNetworkConfig:
    """Test NetworkConfig model."""

    def test_default_network_config(self):
        """Test default network configuration."""
        config = NetworkConfig()

        assert config.mode == "none"
        assert len(config.allowed_domains) == 0
        assert len(config.blocked_domains) == 0

    def test_restricted_network_mode(self):
        """Test restricted network mode with allow/deny lists."""
        config = NetworkConfig(
            mode="restricted",
            allowed_domains=["*.github.com", "api.openai.com"],
            blocked_domains=["malware.com"],
        )

        assert config.mode == "restricted"
        assert "*.github.com" in config.allowed_domains
        assert "malware.com" in config.blocked_domains

    def test_invalid_network_mode(self):
        """Test invalid network mode raises error."""
        with pytest.raises(ValidationError):
            NetworkConfig(mode="invalid_mode")

    def test_valid_network_modes(self):
        """Test all valid network modes."""
        for mode in ["none", "restricted", "all"]:
            config = NetworkConfig(mode=mode)
            assert config.mode == mode


class TestExecutionConfig:
    """Test ExecutionConfig model."""

    def test_default_execution_config(self):
        """Test default execution configuration."""
        config = ExecutionConfig()

        assert config.allow_direct_execution is False
        assert len(config.allowed_commands) == 0

    def test_direct_execution_enabled(self):
        """Test direct execution with command whitelist."""
        config = ExecutionConfig(
            allow_direct_execution=True, allowed_commands=["grep", "cat", "ls", "find"]
        )

        assert config.allow_direct_execution is True
        assert "grep" in config.allowed_commands
        assert len(config.allowed_commands) == 4


class TestExecutorConfigEnhanced:
    """Test enhanced ExecutorConfig with filesystem and network."""

    def test_executor_with_all_features(self):
        """Test executor config with all enhanced features."""
        config = ExecutorConfig(
            url="http://executor:8001",
            api_key="secret123",
            execution=ExecutionConfig(
                allow_direct_execution=True, allowed_commands=["grep", "cat"]
            ),
            filesystem=FilesystemConfig(
                workspace=VolumeConfig(mount="./project_files", readonly=True),
                sandbox=VolumeConfig(mount="/sandbox", readonly=False),
            ),
            network=NetworkConfig(mode="restricted", allowed_domains=["*.github.com"]),
        )

        assert config.execution.allow_direct_execution is True
        assert config.filesystem.workspace.mount == "./project_files"
        assert config.network.mode == "restricted"
        assert "*.github.com" in config.network.allowed_domains

    def test_executor_defaults(self):
        """Test executor config with default values."""
        config = ExecutorConfig(url="http://executor:8001", api_key="secret123")

        # Execution defaults
        assert config.execution.allow_direct_execution is False

        # Filesystem defaults
        assert config.filesystem is None

        # Network defaults
        assert config.network.mode == "none"

    def test_hybrid_execution_config(self):
        """Test realistic hybrid execution configuration."""
        config = ExecutorConfig(
            url="http://executor:8001",
            api_key="secret123",
            execution=ExecutionConfig(
                allow_direct_execution=True,
                allowed_commands=["grep", "cat", "ls", "find", "wc", "head", "tail", "bash"],
            ),
            filesystem=FilesystemConfig(
                workspace=VolumeConfig(mount="./project_files", readonly=True),
                sandbox=VolumeConfig(mount="/sandbox", readonly=False, max_size="1GB"),
                outputs=VolumeConfig(mount="./outputs", readonly=False),
            ),
            network=NetworkConfig(mode="none"),
        )

        # Verify hybrid setup
        assert config.execution.allow_direct_execution is True
        assert len(config.execution.allowed_commands) == 8
        assert config.filesystem.workspace.readonly is True
        assert config.filesystem.sandbox.readonly is False
        assert config.network.mode == "none"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
