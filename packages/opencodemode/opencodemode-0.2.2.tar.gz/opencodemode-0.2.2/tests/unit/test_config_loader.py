"""
Unit tests for ConfigLoader.
"""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from codemode.config.loader import ConfigLoader, ConfigLoadError


class TestConfigLoaderLoad:
    """Test loading configuration from files."""

    def test_load_valid_config(self, tmp_path):
        """Test loading valid configuration file."""
        config_file = tmp_path / "codemode.yaml"
        config_file.write_text(
            """
project:
  name: test-project

framework:
  type: crewai

executor:
  url: http://localhost:8001
  api_key: test-key
"""
        )

        config = ConfigLoader.load(config_file)

        assert config.project.name == "test-project"
        assert config.framework.type == "crewai"
        assert config.executor.url == "http://localhost:8001"

    def test_load_with_path_object(self, tmp_path):
        """Test loading with Path object."""
        config_file = tmp_path / "codemode.yaml"
        config_file.write_text(
            """
project:
  name: test

framework:
  type: crewai

executor:
  url: http://localhost:8001
  api_key: key
"""
        )

        config = ConfigLoader.load(Path(config_file))

        assert config.project.name == "test"

    def test_load_file_not_found(self):
        """Test loading non-existent file."""
        with pytest.raises(FileNotFoundError, match="Configuration file not found"):
            ConfigLoader.load("nonexistent.yaml")

    def test_load_empty_file(self, tmp_path):
        """Test loading empty configuration file."""
        config_file = tmp_path / "empty.yaml"
        config_file.write_text("")

        with pytest.raises(ConfigLoadError, match="Configuration file is empty"):
            ConfigLoader.load(config_file)

    def test_load_invalid_yaml(self, tmp_path):
        """Test loading file with invalid YAML syntax."""
        config_file = tmp_path / "invalid.yaml"
        config_file.write_text("{ invalid yaml [")

        with pytest.raises(ConfigLoadError, match="Invalid YAML syntax"):
            ConfigLoader.load(config_file)

    def test_load_invalid_schema(self, tmp_path):
        """Test loading file with invalid schema."""
        config_file = tmp_path / "invalid_schema.yaml"
        config_file.write_text(
            """
project:
  name: test
# Missing required fields
"""
        )

        with pytest.raises(ConfigLoadError, match="Failed to load configuration"):
            ConfigLoader.load(config_file)


class TestConfigLoaderLoadDict:
    """Test loading configuration from dictionary."""

    def test_load_dict_valid(self):
        """Test loading valid configuration dictionary."""
        config_dict = {
            "project": {"name": "test"},
            "framework": {"type": "crewai"},
            "executor": {
                "url": "http://localhost:8001",
                "api_key": "key",
            },
        }

        config = ConfigLoader.load_dict(config_dict)

        assert config.project.name == "test"
        assert config.framework.type == "crewai"

    def test_load_dict_invalid(self):
        """Test loading invalid configuration dictionary."""
        config_dict = {"invalid": "config"}

        with pytest.raises(ConfigLoadError, match="Failed to load configuration from dict"):
            ConfigLoader.load_dict(config_dict)


class TestConfigLoaderEnvVarSubstitution:
    """Test environment variable substitution."""

    def test_substitute_simple_var(self):
        """Test simple environment variable substitution."""
        with patch.dict(os.environ, {"TEST_VAR": "test_value"}):
            obj = {"key": "${TEST_VAR}"}
            result = ConfigLoader._substitute_env_vars(obj)

            assert result["key"] == "test_value"

    def test_substitute_var_in_nested_dict(self):
        """Test substitution in nested dictionary."""
        with patch.dict(os.environ, {"API_KEY": "secret123"}):
            obj = {"nested": {"key": "${API_KEY}"}}
            result = ConfigLoader._substitute_env_vars(obj)

            assert result["nested"]["key"] == "secret123"

    def test_substitute_var_in_list(self):
        """Test substitution in list."""
        with patch.dict(os.environ, {"ITEM": "value"}):
            obj = ["${ITEM}", "static"]
            result = ConfigLoader._substitute_env_vars(obj)

            assert result == ["value", "static"]

    def test_substitute_var_not_found(self):
        """Test substitution with missing variable."""
        with patch.dict(os.environ, {}, clear=True):
            obj = {"key": "${MISSING_VAR}"}

            with pytest.raises(ConfigLoadError, match="Required environment variable not found"):
                ConfigLoader._substitute_env_vars(obj)

    def test_substitute_var_with_default(self):
        """Test substitution with default value."""
        with patch.dict(os.environ, {}, clear=True):
            obj = {"key": "${MISSING_VAR:-default_value}"}
            result = ConfigLoader._substitute_env_vars(obj)

            assert result["key"] == "default_value"

    def test_substitute_var_with_default_when_exists(self):
        """Test that existing var is used even when default is provided."""
        with patch.dict(os.environ, {"EXISTING_VAR": "actual_value"}):
            obj = {"key": "${EXISTING_VAR:-default_value}"}
            result = ConfigLoader._substitute_env_vars(obj)

            assert result["key"] == "actual_value"

    def test_substitute_non_string_values(self):
        """Test substitution with non-string values."""
        obj = {"number": 42, "boolean": True, "none": None}
        result = ConfigLoader._substitute_env_vars(obj)

        assert result == obj  # Should remain unchanged

    def test_substitute_mixed_content(self):
        """Test substitution with mixed content."""
        with patch.dict(os.environ, {"VAR": "value"}):
            obj = {
                "str_with_var": "prefix-${VAR}-suffix",
                "just_string": "no_var_here",
                "number": 123,
            }
            result = ConfigLoader._substitute_env_vars(obj)

            assert result["str_with_var"] == "prefix-value-suffix"
            assert result["just_string"] == "no_var_here"
            assert result["number"] == 123

    def test_substitute_env_var_in_string(self):
        """Test string substitution directly."""
        with patch.dict(os.environ, {"KEY": "secret"}):
            result = ConfigLoader._substitute_env_var_in_string("api_key=${KEY}")

            assert result == "api_key=secret"

    def test_substitute_multiple_vars_in_string(self):
        """Test multiple variables in one string."""
        with patch.dict(os.environ, {"HOST": "localhost", "PORT": "8001"}):
            result = ConfigLoader._substitute_env_var_in_string("http://${HOST}:${PORT}")

            assert result == "http://localhost:8001"

    def test_substitute_var_with_whitespace(self):
        """Test variable substitution with whitespace."""
        with patch.dict(os.environ, {"VAR": "value"}):
            result = ConfigLoader._substitute_env_var_in_string("${ VAR }")

            assert result == "value"

    def test_substitute_default_with_whitespace(self):
        """Test default value with whitespace."""
        with patch.dict(os.environ, {}, clear=True):
            result = ConfigLoader._substitute_env_var_in_string("${ VAR :- default }")

            assert result == "default"


class TestConfigLoaderValidation:
    """Test configuration validation."""

    def test_validate_valid_config(self, tmp_path):
        """Test validating valid configuration."""
        config_file = tmp_path / "valid.yaml"
        config_file.write_text(
            """
project:
  name: test

framework:
  type: crewai

executor:
  url: http://localhost:8001
  api_key: key
"""
        )

        is_valid = ConfigLoader.validate_config_file(config_file)

        assert is_valid

    def test_validate_invalid_config(self, tmp_path):
        """Test validating invalid configuration."""
        config_file = tmp_path / "invalid.yaml"
        config_file.write_text("{ invalid")

        is_valid = ConfigLoader.validate_config_file(config_file)

        assert not is_valid

    def test_validate_nonexistent_file(self):
        """Test validating non-existent file."""
        is_valid = ConfigLoader.validate_config_file("nonexistent.yaml")

        assert not is_valid


class TestConfigLoaderIntegration:
    """Integration tests for ConfigLoader."""

    def test_load_with_env_vars(self, tmp_path):
        """Test loading config with environment variable substitution."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            """
project:
  name: ${PROJECT_NAME:-default-project}

framework:
  type: crewai

executor:
  url: ${EXECUTOR_URL}
  api_key: ${API_KEY}
"""
        )

        with patch.dict(
            os.environ,
            {"EXECUTOR_URL": "http://executor:8001", "API_KEY": "secret123"},
            clear=True,
        ):
            config = ConfigLoader.load(config_file)

            assert config.project.name == "default-project"  # Using default
            assert config.executor.url == "http://executor:8001"
            assert config.executor.api_key == "secret123"

    def test_load_dict_with_env_vars(self):
        """Test loading dictionary with environment variables."""
        config_dict = {
            "project": {"name": "test"},
            "framework": {"type": "crewai"},
            "executor": {
                "url": "${EXECUTOR_URL}",
                "api_key": "${API_KEY:-default_key}",
            },
        }

        with patch.dict(os.environ, {"EXECUTOR_URL": "http://localhost:8001"}, clear=True):
            config = ConfigLoader.load_dict(config_dict)

            assert config.executor.url == "http://localhost:8001"
            assert config.executor.api_key == "default_key"  # Using default


class TestConfigLoadError:
    """Test ConfigLoadError exception."""

    def test_config_load_error(self):
        """Test ConfigLoadError can be raised and caught."""
        with pytest.raises(ConfigLoadError):
            raise ConfigLoadError("Test error")

        with pytest.raises(ConfigLoadError):  # More specific exception
            raise ConfigLoadError("Test error")
