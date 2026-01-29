"""
Optional base class for context-aware tools.

Tools can inherit from this to get explicit context support,
or they can just accept a 'context' parameter in their run() method.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

# Re-export for convenience
from codemode.core.context import RuntimeContext, ToolContextRequirements

logger = logging.getLogger(__name__)


class ContextAwareTool(ABC):
    """
    Optional base class for tools that use runtime context.

    Tools can either:
    1. Inherit from this class and implement run_with_context()
    2. Accept a 'context' parameter in their run() method
    3. Ignore context entirely (backward compatible)

    Example:
        >>> class MyTool(ContextAwareTool):
        ...     def run_with_context(self, context, query: str) -> str:
        ...         client_id = context.get("client_id")
        ...         return f"Query for {client_id}: {query}"
    """

    @abstractmethod
    def run_with_context(self, context: RuntimeContext, **kwargs) -> Any:
        """
        Execute tool with runtime context.

        Args:
            context: RuntimeContext with injected variables
            **kwargs: Tool-specific arguments

        Returns:
            Tool execution result
        """
        pass

    def run(self, **kwargs) -> Any:
        """
        Fallback run method (for backward compatibility).

        Override this if your tool can work without context.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} requires runtime context. "
            "Call run_with_context() or use via RPC with context."
        )


__all__ = ["ContextAwareTool", "RuntimeContext", "ToolContextRequirements"]
