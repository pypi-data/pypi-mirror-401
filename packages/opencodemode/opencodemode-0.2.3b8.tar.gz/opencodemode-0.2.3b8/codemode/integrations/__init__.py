"""
Framework integrations for Codemode.

This module provides optional integrations with various AI frameworks
like CrewAI, LangChain, AutoGen, etc. Each integration is optional
and only loaded if the framework is installed.
"""

# Try to import CrewAI integration (optional)
try:
    from codemode.integrations.crewai import (
        CREWAI_AVAILABLE,
        CodemodeTool,
        CodemodeToolInput,
        CrewAIIntegration,
        create_codemode_tool,
        create_crewai_integration,
    )

    __all__ = [
        "CodemodeTool",
        "CodemodeToolInput",
        "CrewAIIntegration",
        "create_codemode_tool",
        "create_crewai_integration",
        "CREWAI_AVAILABLE",
    ]

except ImportError:
    # CrewAI not installed, that's fine
    __all__ = []
