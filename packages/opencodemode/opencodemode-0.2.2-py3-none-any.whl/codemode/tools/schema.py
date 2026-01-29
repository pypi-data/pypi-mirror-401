"""
Tool schema utilities for Pydantic-based schema registration.

This module provides utilities for converting Pydantic models to JSON Schema
for tool registration and discovery. This enables agents to understand the
expected input and output formats for tools.

Example:
    >>> from pydantic import BaseModel, Field
    >>> from codemode.tools.schema import pydantic_to_json_schema
    >>>
    >>> class WeatherInput(BaseModel):
    ...     location: str = Field(..., description="City name")
    ...     units: str = Field("celsius", description="Temperature units")
    ...
    >>> schema = pydantic_to_json_schema(WeatherInput)
    >>> print(schema["properties"]["location"]["description"])
    City name
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic import BaseModel

logger = logging.getLogger(__name__)


@dataclass
class ToolRegistration:
    """
    Container for registered tool with metadata.

    This dataclass holds all information about a registered tool,
    including the tool instance and optional schema information.

    Attributes:
        tool: The tool instance (callable, or object with run/run_with_context).
        input_schema: JSON Schema dict for input validation (optional).
        output_schema: JSON Schema dict for return type (optional).
        description: Tool description override (optional).

    Example:
        >>> registration = ToolRegistration(
        ...     tool=my_tool,
        ...     input_schema={"type": "object", "properties": {...}},
        ...     description="Get weather for a location"
        ... )
    """

    tool: Any
    input_schema: dict[str, Any] | None = None
    output_schema: dict[str, Any] | None = None
    description: str | None = None


def pydantic_to_json_schema(model: type[BaseModel]) -> dict[str, Any]:
    """
    Convert a Pydantic model to JSON Schema.

    Supports nested models, optional fields, defaults, and descriptions.
    Uses Pydantic's built-in model_json_schema() method.

    Args:
        model: Pydantic BaseModel class.

    Returns:
        JSON Schema dictionary.

    Raises:
        TypeError: If model is not a Pydantic BaseModel.

    Example:
        >>> from pydantic import BaseModel, Field
        >>>
        >>> class WeatherInput(BaseModel):
        ...     location: str = Field(..., description="City name")
        ...     units: str = Field("celsius", description="Temperature units")
        ...
        >>> schema = pydantic_to_json_schema(WeatherInput)
        >>> print(schema)
        {
            'type': 'object',
            'properties': {
                'location': {'type': 'string', 'description': 'City name'},
                'units': {'type': 'string', 'default': 'celsius', ...}
            },
            'required': ['location']
        }
    """
    # Import here to avoid hard dependency on Pydantic
    try:
        from pydantic import BaseModel as PydanticBaseModel
    except ImportError as e:
        raise ImportError("Pydantic is required for schema support") from e

    if not isinstance(model, type) or not issubclass(model, PydanticBaseModel):
        raise TypeError(f"Expected Pydantic BaseModel class, got {type(model)}")

    return model.model_json_schema()


def dict_to_json_schema(schema_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Validate and normalize a JSON Schema dictionary.

    This function ensures the provided dictionary is a valid structure
    for use as a JSON Schema. It performs basic validation.

    Args:
        schema_dict: Raw JSON Schema dictionary.

    Returns:
        Normalized JSON Schema dictionary.

    Raises:
        ValueError: If schema is not a valid dictionary.

    Example:
        >>> schema = dict_to_json_schema({
        ...     "type": "object",
        ...     "properties": {
        ...         "name": {"type": "string"}
        ...     }
        ... })
    """
    if not isinstance(schema_dict, dict):
        raise ValueError(f"Schema must be a dictionary, got {type(schema_dict)}")

    # Basic validation - ensure it has some schema-like structure
    if schema_dict and "type" not in schema_dict and "properties" not in schema_dict:
        logger.warning("Schema dict may be incomplete - missing 'type' or 'properties'")

    return schema_dict


def schema_to_json_string(schema: dict[str, Any] | None) -> str:
    """
    Convert schema dict to compact JSON string for proto transport.

    Args:
        schema: JSON Schema dictionary or None.

    Returns:
        Compact JSON string representation, or empty string if None.

    Example:
        >>> schema = {"type": "object", "properties": {"x": {"type": "integer"}}}
        >>> json_str = schema_to_json_string(schema)
        >>> print(json_str)
        {"type":"object","properties":{"x":{"type":"integer"}}}
    """
    if not schema:
        return ""
    return json.dumps(schema, separators=(",", ":"), ensure_ascii=False)


def json_string_to_schema(json_str: str) -> dict[str, Any]:
    """
    Parse JSON string back to schema dict.

    Args:
        json_str: JSON string representation of schema.

    Returns:
        Parsed JSON Schema dictionary, or empty dict for empty strings.

    Raises:
        json.JSONDecodeError: If json_str is not valid JSON.

    Example:
        >>> json_str = '{"type":"object"}'
        >>> schema = json_string_to_schema(json_str)
        >>> print(schema)
        {'type': 'object'}
    """
    if not json_str or not json_str.strip():
        return {}
    return json.loads(json_str)


def normalize_schema(
    schema: type[BaseModel] | dict[str, Any] | None,
) -> dict[str, Any] | None:
    """
    Normalize a schema to JSON Schema dict format.

    Accepts either a Pydantic model class or a dict and returns
    a JSON Schema dictionary.

    Args:
        schema: Pydantic model class, JSON Schema dict, or None.

    Returns:
        JSON Schema dictionary or None.

    Raises:
        TypeError: If schema is an unsupported type.

    Example:
        >>> from pydantic import BaseModel
        >>>
        >>> class Input(BaseModel):
        ...     x: int
        ...
        >>> # From Pydantic model
        >>> schema = normalize_schema(Input)
        >>>
        >>> # From dict
        >>> schema = normalize_schema({"type": "object"})
        >>>
        >>> # None passes through
        >>> schema = normalize_schema(None)  # Returns None
    """
    if schema is None:
        return None

    if isinstance(schema, dict):
        return dict_to_json_schema(schema)

    # Try to convert as Pydantic model
    try:
        from pydantic import BaseModel as PydanticBaseModel

        if isinstance(schema, type) and issubclass(schema, PydanticBaseModel):
            return pydantic_to_json_schema(schema)
    except ImportError:
        pass

    raise TypeError(f"Schema must be a Pydantic BaseModel class or dict, got {type(schema)}")


def extract_description(tool: Any, override: str | None = None) -> str:
    """
    Extract description from a tool.

    Priority:
        1. Override (if provided)
        2. tool.description attribute
        3. tool.__doc__ (docstring)
        4. Empty string

    Args:
        tool: Tool instance or callable.
        override: Optional description override.

    Returns:
        Description string (may be empty).

    Example:
        >>> class MyTool:
        ...     '''A helpful tool.'''
        ...     description = "My custom tool"
        ...
        >>> extract_description(MyTool())
        'My custom tool'
    """
    if override:
        return override

    # Try .description attribute
    description = getattr(tool, "description", None)
    if description:
        return str(description)

    # Try __doc__
    doc = getattr(tool, "__doc__", None)
    if doc:
        # Clean up docstring (take first line, strip whitespace)
        first_line = doc.strip().split("\n")[0].strip()
        return first_line

    return ""


__all__ = [
    "ToolRegistration",
    "pydantic_to_json_schema",
    "dict_to_json_schema",
    "schema_to_json_string",
    "json_string_to_schema",
    "normalize_schema",
    "extract_description",
]
