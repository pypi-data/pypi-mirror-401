"""
Runtime context for dynamic variable injection.

This module provides a framework-agnostic way to pass runtime variables
(like client_id, user_id, or any custom data) through the execution pipeline.

## Config vs Context

**Config** (static, set at startup):
- Execution timeouts
- Resource limits
- Allowed imports
- Environment settings

**Context** (dynamic, set per request):
- client_id, user_id, session_id
- Request-specific data
- Feature flags per tenant

## Standards

1. Context is always optional (backward compatible)
2. Context access via .get() with defaults
3. Context serializes to/from dict for RPC
4. Tools declare context requirements (optional)
"""

import json
import logging
from dataclasses import asdict, dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class RuntimeContext:
    """
    Runtime context for dynamic variables.

    Use this for variables that:
    - Change per request (client_id, user_id)
    - Should NOT be controlled by LLM
    - Are request-specific (not global config)

    DO NOT use for:
    - Static configuration (use config dict instead)
    - Global settings (use config)
    - Execution limits (use config)

    Attributes:
        variables: Dynamic variables (client_id, user_id, etc.)
        metadata: Optional metadata for logging/auditing

    Example:
        >>> # Multi-tenant SaaS
        >>> context = RuntimeContext(variables={
        ...     "client_id": "acme_corp",
        ...     "user_id": "user_123",
        ...     "session_id": "sess_456",
        ...     "subscription_tier": "premium"
        ... })
        >>>
        >>> # Feature flags
        >>> context = RuntimeContext(variables={
        ...     "features": {"new_ui": True, "beta_search": False}
        ... })
    """

    variables: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate context."""
        if not isinstance(self.variables, dict):
            raise TypeError("variables must be a dictionary")
        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

    # ========================================
    # STANDARD 1: .get() with defaults
    # ========================================

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get variable value with default.

        Args:
            key: Variable name
            default: Default if not found

        Returns:
            Variable value or default

        Example:
            >>> context.get("client_id")
            'acme_corp'
            >>> context.get("missing", "default")
            'default'
        """
        return self.variables.get(key, default)

    def require(self, key: str) -> Any:
        """
        Get required variable (raises if missing).

        Args:
            key: Variable name

        Returns:
            Variable value

        Raises:
            KeyError: If variable not found

        Example:
            >>> context.require("client_id")  # OK
            >>> context.require("missing")    # Raises KeyError
        """
        if key not in self.variables:
            raise KeyError(f"Required context variable '{key}' not found")
        return self.variables[key]

    def has(self, key: str) -> bool:
        """Check if variable exists."""
        return key in self.variables

    # ========================================
    # STANDARD 2: Serialization for RPC
    # ========================================

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict for RPC transmission."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RuntimeContext":
        """Deserialize from dict."""
        return cls(variables=data.get("variables", {}), metadata=data.get("metadata", {}))

    def to_json(self) -> str:
        """Serialize to JSON for RPC."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "RuntimeContext":
        """Deserialize from JSON."""
        return cls.from_dict(json.loads(json_str))

    # ========================================
    # Utility methods
    # ========================================

    def set(self, key: str, value: Any) -> None:
        """Set variable value."""
        self.variables[key] = value

    def update(self, **kwargs) -> None:
        """Update multiple variables."""
        self.variables.update(kwargs)

    def keys(self) -> list[str]:
        """Get all variable keys."""
        return list(self.variables.keys())

    def __repr__(self) -> str:
        return f"RuntimeContext(variables={list(self.variables.keys())})"

    def __bool__(self) -> bool:
        """Context is truthy if it has variables."""
        return bool(self.variables)

    def __len__(self) -> int:
        """Number of variables."""
        return len(self.variables)


# ========================================
# STANDARD 3: Tool Context Requirements
# ========================================


@dataclass
class ToolContextRequirements:
    """
    Optional metadata for tools that require context.

    Tools can declare what context variables they need.
    This is for documentation and validation only.

    Example:
        >>> requirements = ToolContextRequirements(
        ...     requires_context=True,
        ...     required_keys=["client_id"],
        ...     optional_keys=["user_id", "session_id"]
        ... )
    """

    requires_context: bool = False
    required_keys: list[str] = field(default_factory=list)
    optional_keys: list[str] = field(default_factory=list)

    def validate(self, context: RuntimeContext | None) -> None:
        """
        Validate that context meets requirements.

        Args:
            context: Runtime context to validate

        Raises:
            ValueError: If requirements not met
        """
        if self.requires_context and not context:
            raise ValueError("Tool requires context but none provided")

        if context and self.required_keys:
            missing = [k for k in self.required_keys if not context.has(k)]
            if missing:
                raise ValueError(f"Tool requires context keys: {missing}")
