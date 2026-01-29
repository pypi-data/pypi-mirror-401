"""
Codemode: Secure code execution for multi-agent AI systems.

This package provides a secure way to execute dynamically generated code
in isolated environments while maintaining access to tools and resources
through an RPC bridge pattern.
"""

__version__ = "0.2.3"

from codemode.core.codemode import Codemode
from codemode.core.registry import ComponentRegistry

__all__ = [
    "ComponentRegistry",
    "Codemode",
    "__version__",
]
