"""
Main Codemode API class.

This module provides the high-level Codemode class that users interact with.
It supports both the legacy CodemodeConfig and the new ClientConfig for
client-side configuration.

Example:
    Using ClientConfig (recommended):
        >>> from codemode.config import ClientConfig
        >>> config = ClientConfig(
        ...     executor_url="http://executor:8001",
        ...     executor_api_key="secret-key",
        ... )
        >>> codemode = Codemode.from_client_config(config)

    Using legacy config file:
        >>> codemode = Codemode.from_config("codemode.yaml")
"""

import logging
from pathlib import Path
from typing import Any

from codemode.config.client_config import ClientConfig
from codemode.config.loader import ConfigLoader
from codemode.config.models import CodemodeConfig
from codemode.core.executor_client import ExecutorClient
from codemode.core.registry import ComponentRegistry

logger = logging.getLogger(__name__)


class Codemode:
    """
    Main Codemode class for secure code execution.

    This is the primary interface for using Codemode. It manages configuration,
    component registry, and executor communication.

    Supports two configuration approaches:
    1. ClientConfig (recommended): Modern, clean configuration for client apps
    2. CodemodeConfig (legacy): Unified config from codemode.yaml

    Attributes:
        config: Loaded configuration (CodemodeConfig or None for ClientConfig)
        client_config: ClientConfig if using new config style
        registry: Component registry
        executor_client: Executor client for code execution

    Example:
        Using ClientConfig (recommended):
            >>> from codemode.config import ClientConfig
            >>> config = ClientConfig(
            ...     executor_url="http://executor:8001",
            ...     executor_api_key="secret-key",
            ... )
            >>> codemode = Codemode.from_client_config(config)

        Using legacy config file:
            >>> codemode = Codemode.from_config('codemode.yaml')

        Direct execution:
            >>> result = codemode.execute("result = 2 + 2")
    """

    def __init__(
        self,
        config: CodemodeConfig | None = None,
        registry: ComponentRegistry | None = None,
        client_config: ClientConfig | None = None,
        executor_client: ExecutorClient | None = None,
    ):
        """
        Initialize Codemode.

        Args:
            config: Legacy CodemodeConfig object (mutually exclusive with client_config)
            registry: Optional existing registry (creates new if None)
            client_config: New-style ClientConfig (recommended)
            executor_client: Optional pre-configured ExecutorClient

        Raises:
            ValueError: If neither config nor client_config is provided

        Example:
            >>> config = ConfigLoader.load('codemode.yaml')
            >>> codemode = Codemode(config=config)

            >>> # Or with ClientConfig
            >>> client_config = ClientConfig(...)
            >>> codemode = Codemode(client_config=client_config)
        """
        if config is None and client_config is None:
            raise ValueError("Either 'config' or 'client_config' must be provided")

        self.config = config
        self.client_config = client_config
        self.registry = registry or ComponentRegistry()

        # Initialize executor client
        if executor_client:
            self.executor_client = executor_client
        elif client_config:
            # Use new ClientConfig
            self.executor_client = ExecutorClient(
                executor_url=client_config.executor_url,
                api_key=client_config.executor_api_key,
                timeout=client_config.executor_timeout,
            )
            logger.info(
                f"Initialized Codemode with ClientConfig, executor: {client_config.executor_url}"
            )
        else:
            # Use legacy CodemodeConfig
            assert config is not None  # Type narrowing
            self.executor_client = ExecutorClient(
                executor_url=config.executor.url,
                api_key=config.executor.api_key,
                timeout=config.executor.timeout,
                tls_config=config.grpc.tls,
            )
            logger.info(
                f"Initialized Codemode for project: {config.project.name}, "
                f"framework: {config.framework.type}, "
                f"TLS: {'enabled' if config.grpc.tls.enabled else 'disabled'}"
            )

    @classmethod
    def from_client_config(
        cls,
        config: ClientConfig | None = None,
        registry: ComponentRegistry | None = None,
        config_path: str | Path | None = None,
    ) -> "Codemode":
        """
        Create Codemode instance from ClientConfig.

        This is the recommended way to create a Codemode instance for client
        applications. Supports loading from:
        1. Provided ClientConfig object
        2. YAML file path
        3. Environment variables (if no config or path provided)

        Args:
            config: ClientConfig object (optional)
            registry: Optional existing registry
            config_path: Path to codemode-client.yaml (optional)

        Returns:
            Configured Codemode instance

        Raises:
            ValueError: If environment variables are missing when loading from env

        Example:
            From explicit config:
                >>> config = ClientConfig(
                ...     executor_url="http://executor:8001",
                ...     executor_api_key="secret-key",
                ... )
                >>> codemode = Codemode.from_client_config(config)

            From YAML file:
                >>> codemode = Codemode.from_client_config(
                ...     config_path="codemode-client.yaml"
                ... )

            From environment variables:
                >>> codemode = Codemode.from_client_config()
        """
        if config is not None:
            logger.info("Creating Codemode from provided ClientConfig")
        elif config_path is not None:
            logger.info(f"Loading ClientConfig from: {config_path}")
            config = ConfigLoader.load_client_config(config_path)
        else:
            logger.info("Loading ClientConfig from environment variables")
            config = ClientConfig.from_env()

        return cls(client_config=config, registry=registry)

    @classmethod
    def from_env(cls, registry: ComponentRegistry | None = None) -> "Codemode":
        """
        Create Codemode instance from environment variables.

        Convenience method that loads ClientConfig from environment variables.

        Required environment variables:
            CODEMODE_EXECUTOR_URL: Executor service URL
            CODEMODE_EXECUTOR_API_KEY: API key for authentication

        Returns:
            Configured Codemode instance

        Example:
            >>> import os
            >>> os.environ["CODEMODE_EXECUTOR_URL"] = "http://executor:8001"
            >>> os.environ["CODEMODE_EXECUTOR_API_KEY"] = "secret"
            >>> codemode = Codemode.from_env()
        """
        return cls.from_client_config(registry=registry)

    @classmethod
    def from_config(
        cls, config_path: str | Path, registry: ComponentRegistry | None = None
    ) -> "Codemode":
        """
        Create Codemode instance from configuration file.

        Args:
            config_path: Path to codemode.yaml
            registry: Optional existing registry

        Returns:
            Configured Codemode instance

        Raises:
            FileNotFoundError: If config file not found
            ConfigLoadError: If config is invalid

        Example:
            >>> codemode = Codemode.from_config('codemode.yaml')
            >>> print(codemode.config.project.name)
        """
        logger.info(f"Loading configuration from: {config_path}")

        # Load configuration
        config = ConfigLoader.load(config_path)

        # Create instance
        return cls(config=config, registry=registry)

    @classmethod
    def from_dict(cls, config_dict: dict, registry: ComponentRegistry | None = None) -> "Codemode":
        """
        Create Codemode instance from configuration dictionary.

        Args:
            config_dict: Configuration dictionary
            registry: Optional existing registry

        Returns:
            Configured Codemode instance

        Example:
            >>> codemode = Codemode.from_dict({
            ...     "project": {"name": "test"},
            ...     "framework": {"type": "crewai"},
            ...     "executor": {
            ...         "url": "http://localhost:8001",
            ...         "api_key": "key"
            ...     }
            ... })
        """
        logger.info("Loading configuration from dictionary")

        # Load configuration
        config = ConfigLoader.load_dict(config_dict)

        # Create instance
        return cls(config=config, registry=registry)

    def with_context(self, **variables) -> "Codemode":
        """
        Set runtime context with variables (fluent API).

        Args:
            **variables: Dynamic variables (client_id, user_id, etc.)

        Returns:
            Self for method chaining

        Example:
            >>> codemode.with_context(
            ...     client_id="acme",
            ...     user_id="user_123",
            ...     session_id="sess_456"
            ... )
        """
        from codemode.core.context import RuntimeContext

        context = RuntimeContext(variables=variables)
        self.registry.set_context(context)

        logger.info(f"Set context with variables: {list(variables.keys())}")
        return self

    async def with_context_async(self, **variables) -> "Codemode":
        """Async version of with_context."""
        self.with_context(**variables)
        return self

    def with_config(self, **config) -> "Codemode":
        """
        Set static configuration (fluent API).

        Args:
            **config: Static config (timeouts, limits, etc.)

        Returns:
            Self for method chaining

        Example:
            >>> codemode.with_config(
            ...     execution_timeout=60,
            ...     max_memory_mb=1024
            ... )
        """
        self.registry.update_config(**config)
        logger.info(f"Set config: {list(config.keys())}")
        return self

    async def with_config_async(self, **config) -> "Codemode":
        """Async version of with_config."""
        self.with_config(**config)
        return self

    def execute(self, code: str, execution_timeout: int | None = None) -> str:
        """
        Execute code directly without using CrewAI agent.

        This is useful for direct code execution without the overhead
        of creating an agent.

        Args:
            code: Python code to execute
            execution_timeout: Optional custom timeout (uses config default if None)

        Returns:
            Execution result as string

        Raises:
            ExecutorClientError: If execution fails

        Example:
            >>> result = codemode.execute("result = 2 + 2")
            >>> print(result)
            '4'

            >>> code = '''
            ... weather = tools['weather'].run(location='NYC')
            ... result = {'weather': weather}
            ... '''
            >>> result = codemode.execute(code)
        """
        logger.debug(f"Direct code execution ({len(code)} chars)")

        # Use config timeout if not specified
        if execution_timeout is None:
            if self.client_config:
                execution_timeout = self.client_config.executor_timeout
            elif self.config:
                execution_timeout = self.config.executor.limits.code_timeout
            else:
                execution_timeout = 30  # Default timeout

        # Type assertion for static analysis
        assert execution_timeout is not None

        # Get component names
        component_names = self.registry.get_component_names()

        # Get runtime context (if set)
        context = self.registry.get_context()

        # Execute with context
        result = self.executor_client.execute(
            code=code,
            available_tools=component_names["tools"],
            config=dict(self.registry.config),
            execution_timeout=execution_timeout,
            context=context,  # Pass context to executor
        )

        if result.success:
            return result.result or "Execution successful"
        else:
            return f"ERROR: {result.error}"

    async def execute_async(self, code: str, execution_timeout: int | None = None) -> str:
        """
        Async version of execute.

        Example:
            >>> result = await codemode.execute_async(code)
        """
        # For now, wrap sync version
        # In future, make executor_client fully async
        return self.execute(code, execution_timeout)

    def as_crewai_tool(self) -> Any:
        """
        Get Codemode as a CrewAI tool.

        Returns:
            CodemodeTool instance for use with CrewAI agents

        Raises:
            ImportError: If CrewAI not installed

        Example:
            >>> tool = codemode.as_crewai_tool()
            >>>
            >>> from crewai import Agent
            >>> agent = Agent(
            ...     role="Orchestrator",
            ...     tools=[tool],
            ...     backstory="You write Python code"
            ... )
        """
        try:
            from codemode.integrations.crewai import create_codemode_tool

            tool = create_codemode_tool(
                registry=self.registry, executor_client=self.executor_client
            )

            logger.info("Created CodemodeTool for CrewAI")
            return tool

        except ImportError as e:
            logger.error(f"Failed to create CrewAI tool: {e}")
            raise ImportError(
                "CrewAI is required for as_crewai_tool(). "
                "Install with: pip install opencodemode[crewai]"
            ) from e

    def health_check(self) -> bool:
        """
        Check if executor service is healthy.

        Returns:
            True if executor is healthy, False otherwise

        Example:
            >>> if codemode.health_check():
            ...     print("Executor is healthy")
        """
        return self.executor_client.health_check()

    def ready_check(self) -> bool:
        """
        Check if executor is ready (can reach main app).

        Returns:
            True if executor is ready, False otherwise

        Example:
            >>> if codemode.ready_check():
            ...     print("Executor is ready")
        """
        return self.executor_client.ready_check()

    def close(self) -> None:
        """
        Close resources.

        Closes the executor client's HTTP session.

        Example:
            >>> codemode.close()
        """
        self.executor_client.close()
        logger.debug("Closed Codemode resources")

    def __enter__(self) -> "Codemode":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()

    def __repr__(self) -> str:
        """Return string representation."""
        if self.config:
            return (
                f"Codemode("
                f"project={self.config.project.name}, "
                f"framework={self.config.framework.type}, "
                f"tools={len(self.registry.tools)}, "
                f"agents={len(self.registry.agents)})"
            )
        elif self.client_config:
            return (
                f"Codemode("
                f"executor={self.client_config.executor_url}, "
                f"tools={len(self.registry.tools)}, "
                f"agents={len(self.registry.agents)})"
            )
        else:
            return f"Codemode(tools={len(self.registry.tools)})"
