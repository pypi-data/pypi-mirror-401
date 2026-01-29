"""
Component registry for managing tools, agents, teams, and flows.

This module provides the ComponentRegistry class which serves as a central
repository for all components that can be accessed from dynamically executed code.

Standard naming (library-agnostic):
- tools: Individual functions/tools
- agents: Individual AI agents
- teams: Groups of agents (Crew, GroupChat, team graph)
- flows: Workflows/graphs (Flow, Graph, Workflow)

Thread Safety:
    The registry uses `contextvars.ContextVar` for runtime context management,
    ensuring that context is isolated across concurrent async tasks and threads.
    This prevents context leakage in multi-tenant or concurrent request scenarios.

    Tool registration operations are NOT thread-safe and should be performed
    at application startup before handling concurrent requests.
"""

from __future__ import annotations

import logging
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic import BaseModel

    from codemode.core.context import RuntimeContext
    from codemode.tools.schema import ToolRegistration

logger = logging.getLogger(__name__)

# Module-level ContextVar for async-safe runtime context storage.
# This ensures each async task/thread has its own isolated context,
# preventing race conditions in concurrent request handling.
# Note: Using string annotation since RuntimeContext is imported only for type checking
_runtime_context_var: ContextVar["RuntimeContext | None"] = ContextVar(  # noqa: UP037
    "codemode_runtime_context", default=None
)


class RegistryError(Exception):
    """Base exception for registry-related errors."""

    pass


class ComponentNotFoundError(RegistryError):
    """Raised when a component is not found in the registry."""

    pass


class ComponentAlreadyExistsError(RegistryError):
    """Raised when attempting to register a component that already exists."""

    pass


class ComponentRegistry:
    """
    Central registry for managing AI components (library-agnostic).

    Component Types:
        tools: Individual functions/tools (with optional input/output schemas)
        agents: Individual AI agents
        teams: Groups of agents (Crew, GroupChat, etc.)
        flows: Workflows/graphs (Flow, Graph, Workflow)
        config: Static configuration

    This class maintains dictionaries of tools, agents, teams, flows, and
    configuration that can be accessed from dynamically executed code.

    Attributes:
        tools: Dictionary mapping tool names to tool instances (for backward compat)
        agents: Dictionary mapping agent names to agent instances
        teams: Dictionary mapping team names to team instances
        flows: Dictionary mapping flow names to flow instances
        config: Dictionary of configuration key-value pairs

    Example:
        >>> from pydantic import BaseModel, Field
        >>>
        >>> class WeatherInput(BaseModel):
        ...     location: str = Field(..., description="City name")
        ...
        >>> registry = ComponentRegistry()
        >>> registry.register_tool(
        ...     'weather',
        ...     WeatherTool(),
        ...     input_schema=WeatherInput,
        ...     description="Get current weather"
        ... )
    """

    def __init__(self) -> None:
        """Initialize an empty registry."""
        # Component storage
        self._tool_registrations: dict[str, ToolRegistration] = {}
        self.agents: dict[str, Any] = {}
        self.teams: dict[str, Any] = {}  # Changed from crews
        self.flows: dict[str, Any] = {}

        # Static configuration (set at startup)
        self.config: dict[str, Any] = {}

        # Note: Runtime context is stored in module-level ContextVar
        # (_runtime_context_var) for thread/async safety. The instance
        # variable below is kept for backward compatibility but is not used.
        self._runtime_context: RuntimeContext | None = None

        logger.debug("Initialized ComponentRegistry")

    @property
    def tools(self) -> dict[str, Any]:
        """
        Get dictionary of tool name to tool instance (backward compatibility).

        For full metadata, use get_tool_registration() or get_tool_registrations().
        """
        return {name: reg.tool for name, reg in self._tool_registrations.items()}

    # ========================================
    # TOOL REGISTRATION
    # ========================================

    def register_tool(
        self,
        name: str,
        tool: Any,
        input_schema: type[BaseModel] | dict[str, Any] | None = None,
        output_schema: type[BaseModel] | dict[str, Any] | None = None,
        description: str | None = None,
        overwrite: bool = False,
    ) -> None:
        """
        Register a tool in the registry with optional schema information.

        Args:
            name: Unique identifier for the tool.
            tool: Tool instance to register.
            input_schema: Pydantic model or JSON Schema dict for input validation.
            output_schema: Pydantic model or JSON Schema dict for return type.
            description: Optional description override (uses tool.description or __doc__).
            overwrite: If True, overwrite existing tool with same name.

        Raises:
            ComponentAlreadyExistsError: If tool exists and overwrite=False.
            ValueError: If name or tool is invalid.

        Example:
            >>> from pydantic import BaseModel, Field
            >>>
            >>> class WeatherInput(BaseModel):
            ...     location: str = Field(..., description="City name")
            ...     units: str = Field("celsius", description="Temperature units")
            ...
            >>> class WeatherOutput(BaseModel):
            ...     temperature: float = Field(..., description="Temperature value")
            ...     conditions: str = Field(..., description="Weather conditions")
            ...
            >>> registry.register_tool(
            ...     name='weather',
            ...     tool=weather_tool,
            ...     input_schema=WeatherInput,
            ...     output_schema=WeatherOutput,
            ...     description="Get current weather for a location"
            ... )
        """
        from codemode.tools.schema import ToolRegistration, extract_description, normalize_schema

        if not name:
            raise ValueError("Tool name cannot be empty")

        if not tool:
            raise ValueError("Tool instance cannot be None")

        if name in self._tool_registrations and not overwrite:
            raise ComponentAlreadyExistsError(
                f"Tool '{name}' already exists. Use overwrite=True to replace."
            )

        # Normalize schemas
        input_schema_dict = normalize_schema(input_schema)
        output_schema_dict = normalize_schema(output_schema)

        # Extract description
        tool_description = extract_description(tool, description)

        # Create registration
        registration = ToolRegistration(
            tool=tool,
            input_schema=input_schema_dict,
            output_schema=output_schema_dict,
            description=tool_description,
        )

        self._tool_registrations[name] = registration
        logger.info(f"Registered tool: {name}")

    async def register_tool_async(
        self,
        name: str,
        tool: Any,
        input_schema: type[BaseModel] | dict[str, Any] | None = None,
        output_schema: type[BaseModel] | dict[str, Any] | None = None,
        description: str | None = None,
        overwrite: bool = False,
    ) -> None:
        """Async version of register_tool."""
        self.register_tool(name, tool, input_schema, output_schema, description, overwrite)

    def get_tool_registration(self, name: str) -> ToolRegistration | None:
        """
        Get the full registration for a tool, including schemas.

        Args:
            name: Tool name.

        Returns:
            ToolRegistration or None if not found.
        """
        return self._tool_registrations.get(name)

    def get_tool_registrations(self) -> dict[str, ToolRegistration]:
        """
        Get all tool registrations.

        Returns:
            Dictionary mapping tool names to ToolRegistration objects.
        """
        return self._tool_registrations.copy()

    # ========================================
    # AGENT REGISTRATION
    # ========================================

    def register_agent(self, name: str, agent: Any, overwrite: bool = False) -> None:
        """
        Register an agent in the registry.

        Args:
            name: Unique identifier for the agent
            agent: Agent instance to register
            overwrite: If True, overwrite existing agent with same name

        Raises:
            ComponentAlreadyExistsError: If agent exists and overwrite=False
            ValueError: If name or agent is invalid

        Example:
            >>> registry.register_agent('researcher', researcher_agent)
        """
        if not name:
            raise ValueError("Agent name cannot be empty")

        if not agent:
            raise ValueError("Agent instance cannot be None")

        if name in self.agents and not overwrite:
            raise ComponentAlreadyExistsError(
                f"Agent '{name}' already exists. Use overwrite=True to replace."
            )

        self.agents[name] = agent
        logger.info(f"Registered agent: {name}")

    async def register_agent_async(self, name: str, agent: Any, overwrite: bool = False) -> None:
        """Async version of register_agent."""
        self.register_agent(name, agent, overwrite)

    # ========================================
    # TEAM REGISTRATION (library-agnostic)
    # ========================================

    def register_team(self, name: str, team: Any, overwrite: bool = False) -> None:
        """
        Register a team (group of agents).

        Works with:
        - CrewAI Crew
        - AutoGen GroupChat
        - LangGraph team structure
        - Any multi-agent group

        Args:
            name: Team identifier
            team: Team instance (Crew, GroupChat, etc.)
            overwrite: Whether to overwrite existing

        Example:
            >>> # CrewAI
            >>> registry.register_team('research', crew)
            >>>
            >>> # AutoGen
            >>> registry.register_team('analysts', group_chat)
        """
        if not name:
            raise ValueError("Team name cannot be empty")

        if not team:
            raise ValueError("Team instance cannot be None")

        if name in self.teams and not overwrite:
            raise ComponentAlreadyExistsError(
                f"Team '{name}' already exists. Use overwrite=True to replace."
            )

        self.teams[name] = team
        logger.info(f"Registered team: {name}")

    async def register_team_async(self, name: str, team: Any, overwrite: bool = False) -> None:
        """Async version of register_team."""
        self.register_team(name, team, overwrite)

    # ========================================
    # FLOW REGISTRATION (library-agnostic)
    # ========================================

    def register_flow(self, name: str, flow: Any, overwrite: bool = False) -> None:
        """
        Register a flow/workflow/graph.

        Works with:
        - CrewAI Flow
        - LangGraph StateGraph
        - LlamaIndex Workflow
        - Any workflow structure

        Args:
            name: Flow identifier
            flow: Flow instance
            overwrite: Whether to overwrite existing

        Example:
            >>> # CrewAI
            >>> registry.register_flow('data_pipeline', crewai_flow)
            >>>
            >>> # LangGraph
            >>> registry.register_flow('agent_graph', state_graph)
        """
        if not name:
            raise ValueError("Flow name cannot be empty")

        if not flow:
            raise ValueError("Flow instance cannot be None")

        if name in self.flows and not overwrite:
            raise ComponentAlreadyExistsError(
                f"Flow '{name}' already exists. Use overwrite=True to replace."
            )

        self.flows[name] = flow
        logger.info(f"Registered flow: {name}")

    async def register_flow_async(self, name: str, flow: Any, overwrite: bool = False) -> None:
        """Async version of register_flow."""
        self.register_flow(name, flow, overwrite)

    # ========================================
    # CONTEXT MANAGEMENT (dynamic, per-request)
    # ========================================

    def set_context(self, context: RuntimeContext) -> None:
        """
        Set runtime context for current request/task.

        Context is DYNAMIC (per-request) and contains variables like:
        - client_id, user_id, session_id
        - Request-specific data
        - Feature flags

        Thread Safety:
            This method uses ContextVar for storage, ensuring that context
            is isolated across concurrent async tasks and threads. Each
            async task or thread will have its own independent context.

        Args:
            context: RuntimeContext instance

        Example:
            >>> from codemode.core.context import RuntimeContext
            >>> context = RuntimeContext(variables={
            ...     "client_id": "acme",
            ...     "user_id": "user_123"
            ... })
            >>> registry.set_context(context)
        """
        from codemode.core.context import RuntimeContext

        if not isinstance(context, RuntimeContext):
            raise TypeError("context must be a RuntimeContext instance")

        _runtime_context_var.set(context)
        logger.debug(f"Set runtime context: {context}")

    async def set_context_async(self, context: RuntimeContext) -> None:
        """
        Async version of set_context.

        Note:
            ContextVar is natively async-safe, so this method simply
            delegates to the sync version. Both are safe to use in
            async contexts.
        """
        self.set_context(context)

    def get_context(self) -> RuntimeContext | None:
        """
        Get current runtime context (or None).

        Thread Safety:
            Returns the context for the current async task or thread.
            Each concurrent request has its own isolated context.

        Returns:
            RuntimeContext for the current task, or None if not set.
        """
        return _runtime_context_var.get()

    async def get_context_async(self) -> RuntimeContext | None:
        """
        Async version of get_context.

        Note:
            ContextVar is natively async-safe, so this method simply
            delegates to the sync version.
        """
        return self.get_context()

    def clear_context(self) -> None:
        """
        Clear runtime context for the current request/task.

        Thread Safety:
            Only clears the context for the current async task or thread.
            Other concurrent requests are not affected.
        """
        _runtime_context_var.set(None)
        logger.debug("Cleared runtime context")

    async def clear_context_async(self) -> None:
        """
        Async version of clear_context.

        Note:
            ContextVar is natively async-safe, so this method simply
            delegates to the sync version.
        """
        self.clear_context()

    # ========================================
    # CONFIG MANAGEMENT (static, startup)
    # ========================================

    def set_config(self, key: str, value: Any) -> None:
        """
        Set static configuration value.

        Config is STATIC (set at startup) and contains settings like:
        - Execution timeouts
        - Resource limits
        - Environment settings

        Args:
            key: Configuration key
            value: Configuration value

        Raises:
            ValueError: If key is invalid

        Example:
            >>> registry.set_config('execution_timeout', 30)
            >>> registry.set_config('max_memory_mb', 512)
        """
        if not key:
            raise ValueError("Config key cannot be empty")

        self.config[key] = value
        logger.debug(f"Set config: {key}={value}")

    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default

        Example:
            >>> api_key = registry.get_config('api_key')
            >>> env = registry.get_config('environment', 'development')
        """
        return self.config.get(key, default)

    def update_config(self, **kwargs) -> None:
        """Update multiple config values."""
        self.config.update(kwargs)
        logger.debug(f"Updated config with {len(kwargs)} values")

    # ========================================
    # COMPONENT RETRIEVAL
    # ========================================

    def get_tool(self, name: str) -> Any:
        """
        Get a registered tool.

        Args:
            name: Tool name

        Returns:
            Tool instance

        Raises:
            ComponentNotFoundError: If tool not found

        Example:
            >>> tool = registry.get_tool('weather')
        """
        if name not in self.tools:
            raise ComponentNotFoundError(
                f"Tool '{name}' not found. Available tools: {list(self.tools.keys())}"
            )
        return self.tools[name]

    def get_agent(self, name: str) -> Any:
        """
        Get a registered agent.

        Args:
            name: Agent name

        Returns:
            Agent instance

        Raises:
            ComponentNotFoundError: If agent not found

        Example:
            >>> agent = registry.get_agent('researcher')
        """
        if name not in self.agents:
            raise ComponentNotFoundError(
                f"Agent '{name}' not found. Available agents: {list(self.agents.keys())}"
            )
        return self.agents[name]

    def get_team(self, name: str) -> Any:
        """
        Get a registered team.

        Args:
            name: Team name

        Returns:
            Team instance

        Raises:
            ComponentNotFoundError: If team not found

        Example:
            >>> team = registry.get_team('research_team')
        """
        if name not in self.teams:
            raise ComponentNotFoundError(
                f"Team '{name}' not found. Available teams: {list(self.teams.keys())}"
            )
        return self.teams[name]

    def get_flow(self, name: str) -> Any:
        """
        Get a registered flow.

        Args:
            name: Flow name

        Returns:
            Flow instance

        Raises:
            ComponentNotFoundError: If flow not found

        Example:
            >>> flow = registry.get_flow('onboarding')
        """
        if name not in self.flows:
            raise ComponentNotFoundError(
                f"Flow '{name}' not found. Available flows: {list(self.flows.keys())}"
            )
        return self.flows[name]

    def get_component_names(self) -> dict[str, list[str]]:
        """
        Get names of all registered components.

        Returns:
            Dictionary with component type as key and list of names as value

        Example:
            >>> names = registry.get_component_names()
            >>> print(names['tools'])
            ['weather', 'database']
        """
        return {
            "tools": list(self.tools.keys()),
            "agents": list(self.agents.keys()),
            "teams": list(self.teams.keys()),  # Changed from crews
            "flows": list(self.flows.keys()),
        }

    def clear(self) -> None:
        """
        Clear all registered components and configuration.

        Warning:
            This will remove all registered components. Use with caution.
            Also clears the runtime context for the current task.

        Example:
            >>> registry.clear()
        """
        self._tool_registrations.clear()
        self.agents.clear()
        self.teams.clear()
        self.flows.clear()
        self.config.clear()
        _runtime_context_var.set(None)
        logger.info("Cleared all registry components")

    def __repr__(self) -> str:
        """Return string representation of registry."""
        return (
            f"ComponentRegistry("
            f"tools={len(self.tools)}, "
            f"agents={len(self.agents)}, "
            f"teams={len(self.teams)}, "  # Changed from crews
            f"flows={len(self.flows)})"
        )


def get_current_context() -> "RuntimeContext | None":  # noqa: UP037
    """
    Get the current runtime context from the ContextVar.

    This is a module-level function for accessing the context outside
    of a ComponentRegistry instance. Useful for tools that need to
    access context directly.

    Returns:
        Current RuntimeContext or None if not set.

    Example:
        >>> from codemode.core.registry import get_current_context
        >>> context = get_current_context()
        >>> if context:
        ...     client_id = context.get("client_id")
    """
    return _runtime_context_var.get()


def reset_context() -> None:
    """
    Reset the runtime context ContextVar.

    This is primarily for testing purposes to ensure clean state
    between tests. Should not be used in production code.

    Example:
        >>> from codemode.core.registry import reset_context
        >>> reset_context()  # Clears context for current task
    """
    _runtime_context_var.set(None)
