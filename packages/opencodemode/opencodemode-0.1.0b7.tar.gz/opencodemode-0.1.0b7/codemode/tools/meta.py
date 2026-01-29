"""
Meta-tools for tool discovery and schema introspection.

These built-in tools allow dynamically executed code to discover
available tools and their schemas without prior knowledge.

Meta-tools are registered with reserved names (prefixed with __):
- __list__: List all available tools with descriptions
- __schema__: Get input/output schema for a specific tool
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from codemode.core.registry import ComponentRegistry


class ListToolsMetaTool:
    """
    Built-in tool for listing available tools with descriptions.

    This meta-tool allows dynamically executed code to discover
    what tools are available without prior knowledge.

    Attributes:
        description: Human-readable description for agents.

    Example:
        >>> # In dynamically executed code
        >>> tools = registry.get_tool("__list__").run()
        >>> print(tools)
        {
            "tools": [
                {"name": "weather", "description": "Get current weather"},
                {"name": "database", "description": "Query database"}
            ]
        }
    """

    description = (
        "List all available tools with their descriptions. "
        "Returns a dictionary with 'tools' key containing a list of tool info. "
        "Each tool has: name, description, is_async, has_context."
    )

    def __init__(self, registry: ComponentRegistry) -> None:
        """
        Initialize with reference to component registry.

        Args:
            registry: ComponentRegistry instance containing registered tools.
        """
        self._registry = registry

    def run(self) -> dict[str, Any]:
        """
        List all available tools with brief descriptions.

        Returns:
            Dictionary with 'tools' key containing list of tool info.
            Each tool has: name, description, is_async, has_context.

        Example:
            >>> result = list_tool.run()
            >>> for tool in result["tools"]:
            ...     print(f"{tool['name']}: {tool['description']}")
        """
        import inspect

        tools = []
        for name, registration in self._registry.get_tool_registrations().items():
            # Skip meta-tools in listing
            if name.startswith("__"):
                continue

            tool = registration.tool
            is_async = (
                inspect.iscoroutinefunction(tool)
                or inspect.iscoroutinefunction(getattr(tool, "run", None))
                or inspect.iscoroutinefunction(getattr(tool, "run_with_context", None))
            )

            tools.append(
                {
                    "name": name,
                    "description": registration.description or "",
                    "is_async": is_async,
                    "has_context": hasattr(tool, "run_with_context"),
                    "has_input_schema": registration.input_schema is not None,
                    "has_output_schema": registration.output_schema is not None,
                }
            )

        return {"tools": tools, "count": len(tools)}

    async def run_async(self) -> dict[str, Any]:
        """Async version of run."""
        return self.run()


class GetSchemaMetaTool:
    """
    Built-in tool for getting tool schemas.

    This meta-tool allows dynamically executed code to get the
    input and output schema for a specific tool.

    Attributes:
        description: Human-readable description for agents.

    Example:
        >>> # In dynamically executed code
        >>> schema = registry.get_tool("__schema__").run(name="weather")
        >>> print(schema["input_schema"]["properties"])
        {'location': {'type': 'string', 'description': 'City name'}}
    """

    description = (
        "Get input and output schema for a specific tool. "
        "Pass 'name' argument with the tool name. "
        "Returns dictionary with: tool_name, input_schema, output_schema, description."
    )

    def __init__(self, registry: ComponentRegistry) -> None:
        """
        Initialize with reference to component registry.

        Args:
            registry: ComponentRegistry instance containing registered tools.
        """
        self._registry = registry

    def run(self, name: str) -> dict[str, Any]:
        """
        Get schema for a specific tool.

        Args:
            name: Tool name to get schema for.

        Returns:
            Dictionary with tool_name, input_schema, output_schema, description.

        Raises:
            ValueError: If tool name not found.

        Example:
            >>> result = schema_tool.run(name="weather")
            >>> print(json.dumps(result["input_schema"], indent=2))
        """
        import inspect

        registration = self._registry.get_tool_registration(name)

        if registration is None:
            available = [
                n for n in self._registry.get_tool_registrations().keys() if not n.startswith("__")
            ]
            raise ValueError(f"Tool '{name}' not found. Available tools: {available}")

        tool = registration.tool
        is_async = (
            inspect.iscoroutinefunction(tool)
            or inspect.iscoroutinefunction(getattr(tool, "run", None))
            or inspect.iscoroutinefunction(getattr(tool, "run_with_context", None))
        )

        return {
            "tool_name": name,
            "input_schema": registration.input_schema,
            "output_schema": registration.output_schema,
            "description": registration.description or "",
            "is_async": is_async,
            "has_context": hasattr(tool, "run_with_context"),
        }

    async def run_async(self, name: str) -> dict[str, Any]:
        """Async version of run."""
        return self.run(name=name)


def register_meta_tools(registry: ComponentRegistry) -> None:
    """
    Register meta-tools in the registry.

    This should be called after the registry is created to add
    built-in discovery tools.

    Args:
        registry: ComponentRegistry to register meta-tools in.

    Example:
        >>> from codemode.core.registry import ComponentRegistry
        >>> from codemode.tools.meta import register_meta_tools
        >>>
        >>> registry = ComponentRegistry()
        >>> register_meta_tools(registry)
        >>>
        >>> # Now __list__ and __schema__ are available
        >>> list_tool = registry.get_tool("__list__")
    """
    from pydantic import BaseModel, Field

    # Input schema for __schema__ tool
    class GetSchemaInput(BaseModel):
        """Input for __schema__ meta-tool."""

        name: str = Field(..., description="Name of the tool to get schema for")

    # Output schema for __list__ tool
    class ToolInfoOutput(BaseModel):
        """Info about a single tool."""

        name: str = Field(..., description="Tool name")
        description: str = Field("", description="Tool description")
        is_async: bool = Field(False, description="Whether tool is async")
        has_context: bool = Field(False, description="Whether tool supports context")
        has_input_schema: bool = Field(False, description="Whether input schema is defined")
        has_output_schema: bool = Field(False, description="Whether output schema is defined")

    class ListToolsOutput(BaseModel):
        """Output from __list__ meta-tool."""

        tools: list[ToolInfoOutput] = Field(..., description="List of available tools")
        count: int = Field(..., description="Number of tools")

    # Output schema for __schema__ tool
    class GetSchemaOutput(BaseModel):
        """Output from __schema__ meta-tool."""

        tool_name: str = Field(..., description="Name of the tool")
        input_schema: dict[str, Any] | None = Field(
            None, description="JSON Schema for input parameters"
        )
        output_schema: dict[str, Any] | None = Field(
            None, description="JSON Schema for return type"
        )
        description: str = Field("", description="Tool description")
        is_async: bool = Field(False, description="Whether tool is async")
        has_context: bool = Field(False, description="Whether tool supports context")

    # Register __list__ tool
    registry.register_tool(
        name="__list__",
        tool=ListToolsMetaTool(registry),
        output_schema=ListToolsOutput,
        description=ListToolsMetaTool.description,
        overwrite=True,
    )

    # Register __schema__ tool
    registry.register_tool(
        name="__schema__",
        tool=GetSchemaMetaTool(registry),
        input_schema=GetSchemaInput,
        output_schema=GetSchemaOutput,
        description=GetSchemaMetaTool.description,
        overwrite=True,
    )
