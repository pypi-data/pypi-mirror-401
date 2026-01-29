"""
Tools module for Codemode.

Provides base classes for creating context-aware tools, schema utilities,
and built-in meta-tools for tool discovery.
"""

from codemode.tools.base import ContextAwareTool, ToolContextRequirements
from codemode.tools.meta import GetSchemaMetaTool, ListToolsMetaTool, register_meta_tools
from codemode.tools.schema import (
    ToolRegistration,
    dict_to_json_schema,
    extract_description,
    json_string_to_schema,
    normalize_schema,
    pydantic_to_json_schema,
    schema_to_json_string,
)

__all__ = [
    # Base classes
    "ContextAwareTool",
    "ToolContextRequirements",
    # Schema utilities
    "ToolRegistration",
    "pydantic_to_json_schema",
    "dict_to_json_schema",
    "schema_to_json_string",
    "json_string_to_schema",
    "normalize_schema",
    "extract_description",
    # Meta-tools
    "ListToolsMetaTool",
    "GetSchemaMetaTool",
    "register_meta_tools",
]
