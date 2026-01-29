"""
CrewAI integration for Codemode.

This module provides CrewAI-specific integration including:
- CodemodeTool: Tool for CrewAI agents to execute code
- CrewAIIntegration: Context management for crews/teams
- Wrapper functions for injecting context into crew execution

All CrewAI-specific logic is contained in this file.
"""

import logging
from typing import Any

try:
    from crewai import Agent, Crew, Task
    from crewai.tools import BaseTool
    from pydantic import BaseModel, ConfigDict, Field

    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    # Create dummy classes for type checking
    BaseTool = object
    BaseModel = object

    def Field(*args, **kwargs):
        return None

    def ConfigDict(*args, **kwargs):
        return None

    Crew = object
    Agent = object
    Task = object

from codemode.core.context import RuntimeContext
from codemode.core.executor_client import ExecutorClient, ExecutorClientError
from codemode.core.registry import ComponentRegistry
from codemode.executor.models import ExecutionResult

logger = logging.getLogger(__name__)


if not CREWAI_AVAILABLE:
    logger.warning("CrewAI not installed. Install with: pip install opencodemode[crewai]")


class CodemodeToolInput(BaseModel):
    """
    Input schema for Codemode tool.

    Attributes:
        code: Python code to execute
    """

    code: str = Field(
        ...,
        description=(
            "Python code to execute. Must define a 'result' variable with the output. "
            "Available: tools['tool_name'].run(**kwargs), agents['name'], "
            "teams['name'], config['key']"
        ),
        min_length=1,
    )

    if not CREWAI_AVAILABLE:
        model_config = ConfigDict(arbitrary_types_allowed=True)


class CodemodeTool(BaseTool if CREWAI_AVAILABLE else object):
    """
    CrewAI tool for executing code in isolated environment.

    This tool enables CrewAI agents to generate and execute Python code
    that orchestrates other tools, agents, and teams through the secure
    executor service. Context (like client_id, user_id) is automatically
    injected from the registry.

    Attributes:
        name: Tool name ("codemode")
        description: Tool description for LLM
        args_schema: Pydantic model for input validation
        registry: Component registry
        executor_client: Client for executor service

    Example:
        >>> from codemode.core.registry import ComponentRegistry
        >>> from codemode.core.executor_client import ExecutorClient
        >>>
        >>> registry = ComponentRegistry()
        >>> registry.register_tool('weather', WeatherTool())
        >>>
        >>> client = ExecutorClient("http://executor:8001", "api_key")
        >>> tool = CodemodeTool(registry=registry, executor_client=client)
        >>>
        >>> # Use in CrewAI agent
        >>> agent = Agent(
        ...     role="Orchestrator",
        ...     tools=[tool],
        ...     backstory="You write Python code to coordinate tools"
        ... )
    """

    # Pydantic v2 configuration to allow arbitrary types
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = "codemode"

    description: str = """
Execute Python code to orchestrate tools in a secure sandbox.

<META_TOOLS>
tools['__list__'].run() - List all available tools with descriptions
tools['__schema__'].run(name='tool_name') - Get input/output schema for a tool
</META_TOOLS>

<EXECUTION_PATTERN>
Code MUST use async pattern with result variable:

```python
import asyncio

async def main():
    # Sequential calls
    data = await tools['database'].run(query='SELECT * FROM users')

    # Parallel calls (when inputs are independent)
    weather, stocks = await asyncio.gather(
        tools['weather'].run(location='NYC'),
        tools['stocks'].run(symbol='AAPL'),
    )

    # Tool chaining (output of one -> input of another)
    schema = await tools['__schema__'].run(name='analytics')
    analysis = await tools['analytics'].run(**build_params(schema, data))

    return {'data': data, 'analysis': analysis}

result = asyncio.run(main())
```
</EXECUTION_PATTERN>

<RULES>
- MUST set 'result' variable - this is extracted as output
- ALL tools are async: await tools['name'].run(**kwargs)
- Use asyncio.gather() for parallel independent calls
- Runtime context (client_id, user_id) auto-injected - never hardcode
- Only stdlib imports allowed (asyncio, json, datetime, re, math)
- FORBIDDEN: eval, exec, open, os.*, subprocess.*, __import__, locals, globals
</RULES>

<ERROR_HANDLING>
try:
    data = await tools['api'].run(endpoint='/users')
    result = {'success': True, 'data': data}
except Exception as e:
    result = {'success': False, 'error': str(e)}
</ERROR_HANDLING>
"""

    args_schema: type[BaseModel] = CodemodeToolInput

    # Conditionally declare fields only when CrewAI is available
    if CREWAI_AVAILABLE:
        registry: ComponentRegistry = Field(default=None, exclude=True)
        executor_client: ExecutorClient = Field(default=None, exclude=True)

    def __init__(
        self,
        registry: ComponentRegistry,
        executor_client: ExecutorClient,
        description: str | None = None,
        **kwargs,
    ):
        """
        Initialize CodemodeTool.

        Args:
            registry: Component registry with tools/agents/teams
            executor_client: Executor client for code execution
            description: Custom description to override the default. If provided,
                completely replaces the default. Useful for adding your specific
                tool signatures and business rules.
            **kwargs: Additional arguments passed to BaseTool
        """
        if not CREWAI_AVAILABLE:
            raise ImportError(
                "CrewAI is required for CodemodeTool. Install with: pip install opencodemode[crewai]"
            )

        # Initialize BaseTool - only pass kwargs if we're inheriting from BaseTool
        # (not object). This handles the case where tests mock CREWAI_AVAILABLE
        # but the class was already defined with object as base.
        if self.__class__.__bases__[0] is not object:
            # Inheriting from BaseTool (real or mocked) - let Pydantic handle fields
            super().__init__(registry=registry, executor_client=executor_client, **kwargs)
        else:
            # Inheriting from object - set attributes manually and don't pass to super()
            super().__init__()
            self.registry = registry
            self.executor_client = executor_client

        # Override description if custom one provided
        if description is not None:
            # Use object.__setattr__ to bypass Pydantic's frozen model check if applicable
            object.__setattr__(self, "description", description)

        logger.info("Initialized CodemodeTool for CrewAI")

    def _format_error(self, result: ExecutionResult) -> str:
        """
        Format a comprehensive error message from execution result.

        Includes error type, traceback, stderr, correlation ID, and duration
        for better debugging and error tracing.

        Args:
            result: ExecutionResult with failure details

        Returns:
            Formatted error string with all available diagnostic info
        """
        parts = [f"ERROR: {result.error}"]

        # Include structured error details if available
        if result.error_details:
            if result.error_details.error_type:
                parts.append(f"Type: {result.error_details.error_type}")
            if result.error_details.traceback:
                parts.append(f"Traceback:\n{result.error_details.traceback}")

        # Include stderr if it has additional info not already in error message
        if result.stderr and result.stderr.strip():
            stderr_content = result.stderr.strip()
            # Only add stderr if it contains info not in the error message
            if result.error and stderr_content not in result.error:
                parts.append(f"Stderr:\n{stderr_content}")

        # Add tracing info for debugging
        if result.correlation_id:
            parts.append(f"Correlation ID: {result.correlation_id}")

        if result.duration_ms is not None:
            parts.append(f"Duration: {result.duration_ms:.1f}ms")

        return "\n".join(parts)

    def _run(self, code: str) -> str:
        """
        Execute code via executor service with context injection (sync).

        This is the main method called by CrewAI when the agent uses this tool.
        Context from the registry (client_id, user_id, etc.) is automatically
        injected and passed to all tool calls.

        This method uses the synchronous gRPC channel which is thread-safe and
        works correctly across different event loops. This is essential for
        compatibility with CrewAI's `kickoff_async()` which uses `asyncio.to_thread`
        and can result in different event loops being used for each tool call.

        Thread Safety & Context Propagation:
            Runtime context is stored in a ``ContextVar`` which provides isolation
            across concurrent async tasks. When CrewAI uses ``asyncio.to_thread()``,
            the context is automatically copied to the worker thread (Python 3.9+).

            This means context set via ``registry.set_context()`` will be correctly
            available in this method when called from:
            - Direct sync calls
            - ``asyncio.to_thread()`` (used by CrewAI's ``kickoff_async()``)
            - Any async task that copies the current context

            **Important**: If you create threads manually using ``threading.Thread``
            or ``concurrent.futures.ThreadPoolExecutor``, the context will NOT be
            automatically propagated. In those cases, you must either:
            1. Use ``asyncio.to_thread()`` instead (recommended)
            2. Manually copy context using ``contextvars.copy_context()``

        Args:
            code: Python code to execute

        Returns:
            String representation of execution result, including comprehensive
            error information on failure (error type, traceback, correlation ID)

        Example:
            >>> result = tool._run("result = 2 + 2")
            >>> print(result)
            '4'
        """
        logger.debug(f"Executing code via CodemodeTool ({len(code)} chars)")

        # Get component names for execution context
        component_names = self.registry.get_component_names()

        # Get runtime context from registry (if set)
        context = self.registry.get_context()

        if context:
            logger.debug(f"Injecting context with variables: {list(context.variables.keys())}")

        try:
            # Execute code via sync executor with context
            # Using sync gRPC channel which is thread-safe and has no event loop binding
            result = self.executor_client.execute(
                code=code,
                available_tools=component_names["tools"],
                config=dict(self.registry.config),
                execution_timeout=30,
                context=context,  # Pass context for injection
            )

            if result.success:
                logger.info("Code execution via CodemodeTool successful")

                # Return result or success message
                if result.result:
                    return result.result
                else:
                    return "Code executed successfully (no result returned)"

            else:
                logger.warning(f"Code execution failed: {result.error}")
                return self._format_error(result)

        except ExecutorClientError as e:
            logger.error(f"Executor error: {e}")
            return f"EXECUTOR ERROR: {str(e)}"

        except Exception as e:
            logger.error(f"Unexpected error in CodemodeTool: {e}", exc_info=True)
            return f"UNEXPECTED ERROR: {str(e)}"

    async def _arun(self, code: str) -> str:
        """
        Async version of _run for native async CrewAI usage.

        This method uses the async gRPC channel with per-event-loop caching,
        making it safe for use with CrewAI's `akickoff()` method which provides
        true native async execution.

        Args:
            code: Python code to execute

        Returns:
            String representation of execution result

        Example:
            >>> result = await tool._arun("result = 2 + 2")
            >>> print(result)
            '4'
        """
        logger.debug(f"Executing code via CodemodeTool async ({len(code)} chars)")

        # Get component names for execution context
        component_names = self.registry.get_component_names()

        # Get runtime context from registry (if set)
        context = self.registry.get_context()

        if context:
            logger.debug(f"Injecting context with variables: {list(context.variables.keys())}")

        try:
            # Execute code via async executor with context
            result = await self.executor_client.execute_async(
                code=code,
                available_tools=component_names["tools"],
                config=dict(self.registry.config),
                execution_timeout=30,
                context=context,  # Pass context for injection
            )

            if result.success:
                logger.info("Async code execution via CodemodeTool successful")

                # Return result or success message
                if result.result:
                    return result.result
                else:
                    return "Code executed successfully (no result returned)"

            else:
                logger.warning(f"Async code execution failed: {result.error}")
                return self._format_error(result)

        except ExecutorClientError as e:
            logger.error(f"Executor error: {e}")
            return f"EXECUTOR ERROR: {str(e)}"

        except Exception as e:
            logger.error(f"Unexpected error in CodemodeTool: {e}", exc_info=True)
            return f"UNEXPECTED ERROR: {str(e)}"

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"CodemodeTool("
            f"tools={len(self.registry.tools)}, "
            f"agents={len(self.registry.agents)}, "
            f"teams={len(self.registry.teams)})"
        )


class CrewAIIntegration:
    """
    CrewAI integration manager for context-aware crew execution.

    This class provides methods to wrap CrewAI crews with runtime context,
    enabling multi-tenancy and per-request variable injection.

    Attributes:
        registry: Component registry

    Example:
        >>> from codemode.core.registry import ComponentRegistry
        >>> registry = ComponentRegistry()
        >>> integration = CrewAIIntegration(registry)
        >>>
        >>> # Wrap crew with context
        >>> context_crew = integration.wrap_team(
        ...     crew=my_crew,
        ...     context=RuntimeContext(variables={"client_id": "acme"})
        ... )
        >>> result = context_crew.kickoff()
    """

    def __init__(self, registry: ComponentRegistry):
        """
        Initialize CrewAI integration.

        Args:
            registry: Component registry

        Example:
            >>> integration = CrewAIIntegration(registry)
        """
        if not CREWAI_AVAILABLE:
            raise ImportError("CrewAI is required. Install with: pip install opencodemode[crewai]")

        self.registry = registry
        logger.info("Initialized CrewAI integration")

    def wrap_team(self, crew: Crew, context: RuntimeContext | None = None) -> Crew:
        """
        Wrap a CrewAI crew with runtime context.

        This creates a new crew wrapper that sets the context in the registry
        before kickoff and clears it afterward.

        Args:
            crew: CrewAI crew to wrap
            context: Runtime context to inject

        Returns:
            Wrapped crew with context support

        Example:
            >>> context = RuntimeContext(variables={"client_id": "acme"})
            >>> wrapped_crew = integration.wrap_team(my_crew, context)
            >>> result = wrapped_crew.kickoff()
        """
        if not CREWAI_AVAILABLE:
            raise ImportError("CrewAI is required")

        # Create a wrapper class that preserves the original crew
        class ContextAwareCrew:
            """Wrapper that injects context before crew execution."""

            def __init__(
                self,
                original_crew: Crew,
                registry: ComponentRegistry,
                context: RuntimeContext | None,
            ):
                self._crew = original_crew
                self._registry = registry
                self._context = context

            def kickoff(self, inputs: dict[str, Any] | None = None) -> Any:
                """Execute crew with context injection."""
                try:
                    # Set context in registry before execution
                    if self._context:
                        self._registry.set_context(self._context)
                        logger.debug(
                            f"Set context for crew execution: "
                            f"{list(self._context.variables.keys())}"
                        )

                    # Execute crew
                    result = self._crew.kickoff(inputs=inputs)

                    return result

                finally:
                    # Always clear context after execution
                    if self._context:
                        self._registry.clear_context()
                        logger.debug("Cleared context after crew execution")

            async def kickoff_async(self, inputs: dict[str, Any] | None = None) -> Any:
                """Async version of kickoff with context injection."""
                try:
                    # Set context in registry before execution
                    if self._context:
                        await self._registry.set_context_async(self._context)
                        logger.debug(
                            f"Set context for async crew execution: "
                            f"{list(self._context.variables.keys())}"
                        )

                    # Execute crew
                    if hasattr(self._crew, "kickoff_async"):
                        result = await self._crew.kickoff_async(inputs=inputs)
                    else:
                        # Fallback to sync version
                        result = self._crew.kickoff(inputs=inputs)

                    return result

                finally:
                    # Always clear context after execution
                    if self._context:
                        await self._registry.clear_context_async()
                        logger.debug("Cleared context after async crew execution")

            def __getattr__(self, name: str) -> Any:
                """Delegate attribute access to original crew."""
                return getattr(self._crew, name)

            def __repr__(self) -> str:
                return f"ContextAwareCrew({self._crew})"

        return ContextAwareCrew(crew, self.registry, context)

    def wrap_crew(self, crew: Crew, context: RuntimeContext | None = None) -> Crew:
        """
        Backward-compatible alias for wrap_team().

        Args:
            crew: CrewAI crew to wrap
            context: Runtime context to inject

        Returns:
            Wrapped crew with context support

        Example:
            >>> wrapped_crew = integration.wrap_crew(my_crew, context)
        """
        return self.wrap_team(crew, context)

    def __repr__(self) -> str:
        """Return string representation."""
        return f"CrewAIIntegration(registry={self.registry})"


def create_codemode_tool(
    registry: ComponentRegistry, executor_client: ExecutorClient
) -> CodemodeTool:
    """
    Factory function to create a CodemodeTool.

    This is a convenience function for creating the tool with proper
    configuration.

    Args:
        registry: Component registry
        executor_client: Executor client

    Returns:
        Configured CodemodeTool instance

    Example:
        >>> tool = create_codemode_tool(registry, client)
        >>> agent = Agent(role="Orchestrator", tools=[tool])
    """
    if not CREWAI_AVAILABLE:
        raise ImportError("CrewAI is required. Install with: pip install opencodemode[crewai]")

    return CodemodeTool(registry=registry, executor_client=executor_client)


def create_crewai_integration(registry: ComponentRegistry) -> CrewAIIntegration:
    """
    Factory function to create CrewAI integration.

    Args:
        registry: Component registry

    Returns:
        CrewAI integration instance

    Example:
        >>> integration = create_crewai_integration(registry)
        >>> wrapped_crew = integration.wrap_team(crew, context)
    """
    if not CREWAI_AVAILABLE:
        raise ImportError("CrewAI is required. Install with: pip install opencodemode[crewai]")

    return CrewAIIntegration(registry)


__all__ = [
    "CodemodeTool",
    "CodemodeToolInput",
    "CrewAIIntegration",
    "create_codemode_tool",
    "create_crewai_integration",
    "CREWAI_AVAILABLE",
]
