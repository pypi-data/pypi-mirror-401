"""
Configuration loader with YAML parsing and environment variable substitution.

This module provides functionality to load and parse configuration files
with support for environment variable interpolation. It supports:

- Legacy CodemodeConfig (codemode.yaml) - deprecated
- ClientConfig (codemode-client.yaml) - for main applications
- SidecarConfig (codemode-sidecar.yaml) - for executor sidecar

Example:
    Loading client config:
        >>> config = ConfigLoader.load_client_config("codemode-client.yaml")

    Loading from environment only:
        >>> config = ConfigLoader.load_client_config_from_env()

    Loading sidecar config:
        >>> config = ConfigLoader.load_sidecar_config("codemode-sidecar.yaml")
"""

import logging
import os
import re
from pathlib import Path
from typing import Any, TypeVar

import yaml

from codemode.config.client_config import ClientConfig
from codemode.config.models import CodemodeConfig
from codemode.config.sidecar_config import SidecarConfig

logger = logging.getLogger(__name__)

# Type variable for config models
T = TypeVar("T", ClientConfig, SidecarConfig)


class ConfigLoadError(Exception):
    """Raised when configuration loading fails."""

    pass


class ConfigLoader:
    """
    Loads and parses Codemode configuration files.

    Supports:
    - YAML parsing
    - Environment variable substitution (${VAR_NAME})
    - Configuration validation via Pydantic models

    Example:
        >>> loader = ConfigLoader()
        >>> config = loader.load("codemode.yaml")
        >>> print(config.project.name)
    """

    # Regex pattern for environment variable substitution: ${VAR_NAME}
    ENV_VAR_PATTERN = re.compile(r"\$\{([^}]+)\}")

    @classmethod
    def load(cls, config_path: str | Path) -> CodemodeConfig:
        """
        Load configuration from a YAML file.

        Args:
            config_path: Path to configuration file

        Returns:
            Validated CodemodeConfig instance

        Raises:
            ConfigLoadError: If file not found or invalid
            FileNotFoundError: If config file doesn't exist

        Example:
            >>> config = ConfigLoader.load("codemode.yaml")
        """
        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        logger.info(f"Loading configuration from: {config_path}")

        try:
            # Read and parse YAML
            with open(config_path) as f:
                raw_config = yaml.safe_load(f)

            if not raw_config:
                raise ConfigLoadError("Configuration file is empty")

            # Substitute environment variables
            processed_config = cls._substitute_env_vars(raw_config)

            # Validate and create config object
            config = CodemodeConfig(**processed_config)

            logger.info(f"Successfully loaded configuration for project: {config.project.name}")

            return config

        except yaml.YAMLError as e:
            raise ConfigLoadError(f"Invalid YAML syntax: {e}") from e
        except Exception as e:
            raise ConfigLoadError(f"Failed to load configuration: {e}") from e

    @classmethod
    def load_dict(cls, config_dict: dict[str, Any]) -> CodemodeConfig:
        """
        Load configuration from a dictionary.

        Args:
            config_dict: Configuration dictionary

        Returns:
            Validated CodemodeConfig instance

        Raises:
            ConfigLoadError: If configuration is invalid

        Example:
            >>> config = ConfigLoader.load_dict({
            ...     "project": {"name": "test"},
            ...     "framework": {"type": "crewai"},
            ...     "executor": {"url": "http://localhost:8001", "api_key": "key"}
            ... })
        """
        try:
            # Substitute environment variables
            processed_config = cls._substitute_env_vars(config_dict)

            # Validate and create config object
            config = CodemodeConfig(**processed_config)

            logger.debug("Loaded configuration from dictionary")

            return config

        except Exception as e:
            raise ConfigLoadError(f"Failed to load configuration from dict: {e}") from e

    @classmethod
    def _substitute_env_vars(cls, obj: Any) -> Any:
        """
        Recursively substitute environment variables in configuration.

        Supports ${VAR_NAME} and ${VAR_NAME:-default} syntax.

        Args:
            obj: Configuration object (dict, list, str, etc.)

        Returns:
            Object with environment variables substituted

        Example:
            >>> os.environ['API_KEY'] = 'secret123'
            >>> result = cls._substitute_env_vars({"key": "${API_KEY}"})
            >>> result
            {'key': 'secret123'}
        """
        if isinstance(obj, dict):
            return {k: cls._substitute_env_vars(v) for k, v in obj.items()}

        elif isinstance(obj, list):
            return [cls._substitute_env_vars(item) for item in obj]

        elif isinstance(obj, str):
            return cls._substitute_env_var_in_string(obj)

        else:
            return obj

    @classmethod
    def _substitute_env_var_in_string(cls, value: str) -> str:
        """
        Substitute environment variables in a string.

        Supports:
        - ${VAR_NAME} - Replace with env var or raise error if not found
        - ${VAR_NAME:-default} - Replace with env var or use default

        Args:
            value: String potentially containing ${VAR_NAME}

        Returns:
            String with substituted values

        Raises:
            ConfigLoadError: If required env var not found

        Example:
            >>> os.environ['API_KEY'] = 'secret'
            >>> cls._substitute_env_var_in_string("key=${API_KEY}")
            'key=secret'

            >>> cls._substitute_env_var_in_string("key=${MISSING:-default}")
            'key=default'
        """

        def replace_match(match: re.Match) -> str:
            """Replace a single environment variable match."""
            var_expression = match.group(1)

            # Check for default value syntax: VAR_NAME:-default
            if ":-" in var_expression:
                var_name, default_value = var_expression.split(":-", 1)
                var_name = var_name.strip()
                default_value = default_value.strip()

                env_value = os.environ.get(var_name)
                if env_value is not None:
                    logger.debug(f"Substituted ${{{var_name}}} with env value")
                    return env_value
                else:
                    logger.debug(
                        f"Environment variable ${{{var_name}}} not found, "
                        f"using default: {default_value}"
                    )
                    return default_value
            else:
                var_name = var_expression.strip()
                env_value = os.environ.get(var_name)

                if env_value is not None:
                    logger.debug(f"Substituted ${{{var_name}}} with env value")
                    return env_value
                else:
                    raise ConfigLoadError(f"Required environment variable not found: {var_name}")

        return cls.ENV_VAR_PATTERN.sub(replace_match, value)

    @classmethod
    def validate_config_file(cls, config_path: str | Path) -> bool:
        """
        Validate a configuration file without fully loading it.

        Args:
            config_path: Path to configuration file

        Returns:
            True if valid, False otherwise

        Example:
            >>> is_valid = ConfigLoader.validate_config_file("codemode.yaml")
        """
        try:
            cls.load(config_path)
            return True
        except (ConfigLoadError, FileNotFoundError, Exception) as e:
            logger.error(f"Configuration validation failed: {e}")
            return False

    # ========================================================================
    # Client Configuration Loading
    # ========================================================================

    @classmethod
    def load_client_config(cls, config_path: str | Path) -> ClientConfig:
        """
        Load client configuration from a YAML file.

        This is the recommended way to configure client applications that
        connect to the codemode executor sidecar.

        Args:
            config_path: Path to codemode-client.yaml file

        Returns:
            Validated ClientConfig instance

        Raises:
            ConfigLoadError: If file not found or invalid
            FileNotFoundError: If config file doesn't exist

        Example:
            >>> config = ConfigLoader.load_client_config("codemode-client.yaml")
            >>> print(config.executor_url)
        """
        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"Client configuration file not found: {config_path}")

        logger.info(f"Loading client configuration from: {config_path}")

        try:
            with open(config_path) as f:
                raw_config = yaml.safe_load(f)

            if not raw_config:
                raise ConfigLoadError("Client configuration file is empty")

            processed_config = cls._substitute_env_vars(raw_config)
            config = ClientConfig(**processed_config)

            logger.info("Successfully loaded client configuration")
            return config

        except yaml.YAMLError as e:
            raise ConfigLoadError(f"Invalid YAML syntax in client config: {e}") from e
        except Exception as e:
            raise ConfigLoadError(f"Failed to load client configuration: {e}") from e

    @classmethod
    def load_client_config_from_dict(cls, config_dict: dict[str, Any]) -> ClientConfig:
        """
        Load client configuration from a dictionary.

        Args:
            config_dict: Configuration dictionary

        Returns:
            Validated ClientConfig instance

        Raises:
            ConfigLoadError: If configuration is invalid

        Example:
            >>> config = ConfigLoader.load_client_config_from_dict({
            ...     "executor_url": "http://executor:8001",
            ...     "executor_api_key": "secret-key",
            ... })
        """
        try:
            processed_config = cls._substitute_env_vars(config_dict)
            config = ClientConfig(**processed_config)
            logger.debug("Loaded client configuration from dictionary")
            return config
        except Exception as e:
            raise ConfigLoadError(f"Failed to load client configuration from dict: {e}") from e

    @classmethod
    def load_client_config_from_env(cls) -> ClientConfig:
        """
        Load client configuration from environment variables only.

        This is useful for containerized deployments where all configuration
        comes from environment variables.

        Returns:
            Validated ClientConfig instance

        Raises:
            ValueError: If required environment variables are missing

        Example:
            >>> import os
            >>> os.environ["CODEMODE_EXECUTOR_URL"] = "http://executor:8001"
            >>> os.environ["CODEMODE_EXECUTOR_API_KEY"] = "secret"
            >>> config = ConfigLoader.load_client_config_from_env()
        """
        logger.info("Loading client configuration from environment variables")
        return ClientConfig.from_env()

    # ========================================================================
    # Sidecar Configuration Loading
    # ========================================================================

    @classmethod
    def load_sidecar_config(cls, config_path: str | Path) -> SidecarConfig:
        """
        Load sidecar configuration from a YAML file.

        This is the recommended way to configure the executor sidecar service.

        Args:
            config_path: Path to codemode-sidecar.yaml file

        Returns:
            Validated SidecarConfig instance

        Raises:
            ConfigLoadError: If file not found or invalid
            FileNotFoundError: If config file doesn't exist

        Example:
            >>> config = ConfigLoader.load_sidecar_config("codemode-sidecar.yaml")
            >>> print(config.port)
        """
        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"Sidecar configuration file not found: {config_path}")

        logger.info(f"Loading sidecar configuration from: {config_path}")

        try:
            with open(config_path) as f:
                raw_config = yaml.safe_load(f)

            if not raw_config:
                raise ConfigLoadError("Sidecar configuration file is empty")

            processed_config = cls._substitute_env_vars(raw_config)
            config = SidecarConfig(**processed_config)

            logger.info("Successfully loaded sidecar configuration")
            return config

        except yaml.YAMLError as e:
            raise ConfigLoadError(f"Invalid YAML syntax in sidecar config: {e}") from e
        except Exception as e:
            raise ConfigLoadError(f"Failed to load sidecar configuration: {e}") from e

    @classmethod
    def load_sidecar_config_from_dict(cls, config_dict: dict[str, Any]) -> SidecarConfig:
        """
        Load sidecar configuration from a dictionary.

        Args:
            config_dict: Configuration dictionary

        Returns:
            Validated SidecarConfig instance

        Raises:
            ConfigLoadError: If configuration is invalid

        Example:
            >>> config = ConfigLoader.load_sidecar_config_from_dict({
            ...     "port": 8001,
            ...     "api_key": "secret-key",
            ... })
        """
        try:
            processed_config = cls._substitute_env_vars(config_dict)
            config = SidecarConfig(**processed_config)
            logger.debug("Loaded sidecar configuration from dictionary")
            return config
        except Exception as e:
            raise ConfigLoadError(f"Failed to load sidecar configuration from dict: {e}") from e

    @classmethod
    def load_sidecar_config_from_env(cls) -> SidecarConfig:
        """
        Load sidecar configuration from environment variables only.

        This is useful for containerized deployments where all configuration
        comes from environment variables.

        Returns:
            Validated SidecarConfig instance

        Example:
            >>> import os
            >>> os.environ["CODEMODE_API_KEY"] = "secret"
            >>> config = ConfigLoader.load_sidecar_config_from_env()
        """
        logger.info("Loading sidecar configuration from environment variables")
        return SidecarConfig.from_env()
