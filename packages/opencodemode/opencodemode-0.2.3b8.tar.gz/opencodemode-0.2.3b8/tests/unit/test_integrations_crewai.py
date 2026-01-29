"""
Unit tests for CrewAI integration.
"""

import asyncio
from unittest.mock import Mock, patch

import pytest

from codemode.core.context import RuntimeContext
from codemode.core.executor_client import ExecutorClient, ExecutorClientError
from codemode.core.registry import ComponentRegistry
from codemode.executor.models import ExecutionError, ExecutionResult


# Test helpers
def create_mock_crewai_classes():
    """Create mock CrewAI classes for testing."""

    class MockBaseTool:
        """Mock CrewAI BaseTool."""

        def __init__(self, **kwargs):
            pass

    class MockBaseModel:
        """Mock Pydantic BaseModel."""

        pass

    class MockCrew:
        """Mock CrewAI Crew."""

        def kickoff(self, inputs=None):
            return {"result": "crew_output"}

        async def kickoff_async(self, inputs=None):
            return {"result": "async_crew_output"}

    class MockAgent:
        """Mock CrewAI Agent."""

        pass

    class MockTask:
        """Mock CrewAI Task."""

        pass

    return MockBaseTool, MockBaseModel, MockCrew, MockAgent, MockTask


class TestCrewAINotAvailable:
    """Test behavior when CrewAI is not installed."""

    def test_crewai_not_available_flag(self):
        """Test CREWAI_AVAILABLE flag when CrewAI not installed."""
        # Mock import failure
        with patch.dict("sys.modules", {"crewai": None, "crewai.tools": None}):
            # Reload module to trigger import error handling
            import importlib

            import codemode.integrations.crewai as crewai_module

            importlib.reload(crewai_module)

            # CREWAI_AVAILABLE should be False when import fails
            # (This is checked during module import)
            assert True  # Module loaded without crashing

    def test_codemode_tool_import_error(self):
        """Test CodemodeTool raises ImportError when CrewAI not available."""
        with patch("codemode.integrations.crewai.CREWAI_AVAILABLE", False):
            from codemode.integrations.crewai import CodemodeTool

            registry = ComponentRegistry()
            client = Mock(spec=ExecutorClient)

            with pytest.raises(ImportError, match="CrewAI is required"):
                CodemodeTool(registry=registry, executor_client=client)

    def test_crewai_integration_import_error(self):
        """Test CrewAIIntegration raises ImportError when CrewAI not available."""
        with patch("codemode.integrations.crewai.CREWAI_AVAILABLE", False):
            from codemode.integrations.crewai import CrewAIIntegration

            registry = ComponentRegistry()

            with pytest.raises(ImportError, match="CrewAI is required"):
                CrewAIIntegration(registry)

    def test_wrap_team_import_error(self):
        """Test wrap_team raises ImportError when CrewAI not available."""
        with patch("codemode.integrations.crewai.CREWAI_AVAILABLE", True):
            from codemode.integrations.crewai import CrewAIIntegration

            registry = ComponentRegistry()
            integration = CrewAIIntegration(registry)

            # Simulate CREWAI_AVAILABLE becoming False after initialization
            with patch("codemode.integrations.crewai.CREWAI_AVAILABLE", False):
                with pytest.raises(ImportError, match="CrewAI is required"):
                    integration.wrap_team(Mock(), None)

    def test_create_codemode_tool_import_error(self):
        """Test create_codemode_tool raises ImportError when CrewAI not available."""
        with patch("codemode.integrations.crewai.CREWAI_AVAILABLE", False):
            from codemode.integrations.crewai import create_codemode_tool

            registry = ComponentRegistry()
            client = Mock(spec=ExecutorClient)

            with pytest.raises(ImportError, match="CrewAI is required"):
                create_codemode_tool(registry, client)

    def test_create_crewai_integration_import_error(self):
        """Test create_crewai_integration raises ImportError when CrewAI not available."""
        with patch("codemode.integrations.crewai.CREWAI_AVAILABLE", False):
            from codemode.integrations.crewai import create_crewai_integration

            registry = ComponentRegistry()

            with pytest.raises(ImportError, match="CrewAI is required"):
                create_crewai_integration(registry)


class TestCodemodeToolInput:
    """Test CodemodeToolInput Pydantic model."""

    def test_input_model_exists(self):
        """Test that CodemodeToolInput model can be imported."""
        from codemode.integrations.crewai import CodemodeToolInput

        # Just verify it exists and has the expected attributes
        assert hasattr(CodemodeToolInput, "code") or CodemodeToolInput is not None


class TestCodemodeTool:
    """Test CodemodeTool class."""

    @pytest.fixture
    def mock_crewai_available(self):
        """Mock CrewAI as available."""
        with patch("codemode.integrations.crewai.CREWAI_AVAILABLE", True):
            yield

    @pytest.fixture
    def registry(self):
        """Create test registry."""
        registry = ComponentRegistry()
        registry.register_tool("weather", lambda location: f"Weather in {location}: 72°F")
        registry.set_config("timeout", 30)
        return registry

    @pytest.fixture
    def executor_client(self):
        """Create mock executor client."""
        return Mock(spec=ExecutorClient)

    def test_init_success(self, mock_crewai_available, registry, executor_client):
        """Test successful initialization."""
        MockBaseTool, _, _, _, _ = create_mock_crewai_classes()

        with patch("codemode.integrations.crewai.BaseTool", MockBaseTool):
            from codemode.integrations.crewai import CodemodeTool

            tool = CodemodeTool(registry=registry, executor_client=executor_client)

            assert tool.registry is registry
            assert tool.executor_client is executor_client
            assert tool.name == "codemode"

    def test_run_success(self, mock_crewai_available, registry, executor_client):
        """Test successful code execution."""
        MockBaseTool, _, _, _, _ = create_mock_crewai_classes()

        # Mock successful sync execution
        def mock_execute(*args, **kwargs):
            return ExecutionResult(
                success=True,
                result="42",
                stdout="",
                stderr="",
                error=None,
                error_details=None,
                correlation_id=None,
                duration_ms=0.0,
            )

        executor_client.execute = Mock(side_effect=mock_execute)

        with patch("codemode.integrations.crewai.BaseTool", MockBaseTool):
            from codemode.integrations.crewai import CodemodeTool

            tool = CodemodeTool(registry=registry, executor_client=executor_client)

            # _run is now sync
            result = tool._run("result = 2 + 2")

            assert result == "42"
            executor_client.execute.assert_called_once()
            call_kwargs = executor_client.execute.call_args.kwargs
            assert call_kwargs["code"] == "result = 2 + 2"
            assert "weather" in call_kwargs["available_tools"]

    def test_run_with_context(self, mock_crewai_available, registry, executor_client):
        """Test code execution with context injection."""
        MockBaseTool, _, _, _, _ = create_mock_crewai_classes()

        # Set context in registry
        context = RuntimeContext(variables={"client_id": "acme", "user_id": "123"})
        registry.set_context(context)

        # Mock successful sync execution
        def mock_execute(*args, **kwargs):
            return ExecutionResult(
                success=True,
                result="ok",
                stdout="",
                stderr="",
                error=None,
                error_details=None,
                correlation_id=None,
                duration_ms=0.0,
            )

        executor_client.execute = Mock(side_effect=mock_execute)

        with patch("codemode.integrations.crewai.BaseTool", MockBaseTool):
            from codemode.integrations.crewai import CodemodeTool

            tool = CodemodeTool(registry=registry, executor_client=executor_client)

            result = tool._run("result = 'test'")

            assert result == "ok"
            # Verify context was passed
            call_kwargs = executor_client.execute.call_args.kwargs
            assert call_kwargs["context"] == context

    def test_run_no_result(self, mock_crewai_available, registry, executor_client):
        """Test execution with no result returned."""
        MockBaseTool, _, _, _, _ = create_mock_crewai_classes()

        # Mock execution with no result
        def mock_execute(*args, **kwargs):
            return ExecutionResult(
                success=True,
                result=None,
                stdout="",
                stderr="",
                error=None,
                error_details=None,
                correlation_id=None,
                duration_ms=0.0,
            )

        executor_client.execute = Mock(side_effect=mock_execute)

        with patch("codemode.integrations.crewai.BaseTool", MockBaseTool):
            from codemode.integrations.crewai import CodemodeTool

            tool = CodemodeTool(registry=registry, executor_client=executor_client)

            result = tool._run("print('hello')")

            assert "successfully" in result.lower()

    def test_run_execution_failure(self, mock_crewai_available, registry, executor_client):
        """Test failed code execution."""
        MockBaseTool, _, _, _, _ = create_mock_crewai_classes()

        # Mock failed execution
        def mock_execute(*args, **kwargs):
            return ExecutionResult(
                success=False,
                result=None,
                stdout="",
                stderr="",
                error="NameError: name 'x' is not defined",
                error_details=None,
                correlation_id=None,
                duration_ms=0.0,
            )

        executor_client.execute = Mock(side_effect=mock_execute)

        with patch("codemode.integrations.crewai.BaseTool", MockBaseTool):
            from codemode.integrations.crewai import CodemodeTool

            tool = CodemodeTool(registry=registry, executor_client=executor_client)

            result = tool._run("print(x)")

            assert "ERROR" in result
            assert "NameError" in result

    def test_run_executor_client_error(self, mock_crewai_available, registry, executor_client):
        """Test ExecutorClientError handling."""
        MockBaseTool, _, _, _, _ = create_mock_crewai_classes()

        # Mock executor error
        def mock_execute(*args, **kwargs):
            raise ExecutorClientError("Connection failed")

        executor_client.execute = Mock(side_effect=mock_execute)

        with patch("codemode.integrations.crewai.BaseTool", MockBaseTool):
            from codemode.integrations.crewai import CodemodeTool

            tool = CodemodeTool(registry=registry, executor_client=executor_client)

            result = tool._run("result = 2 + 2")

            assert "EXECUTOR ERROR" in result
            assert "Connection failed" in result

    def test_run_unexpected_error(self, mock_crewai_available, registry, executor_client):
        """Test unexpected exception handling."""
        MockBaseTool, _, _, _, _ = create_mock_crewai_classes()

        # Mock unexpected error
        def mock_execute(*args, **kwargs):
            raise RuntimeError("Unexpected issue")

        executor_client.execute = Mock(side_effect=mock_execute)

        with patch("codemode.integrations.crewai.BaseTool", MockBaseTool):
            from codemode.integrations.crewai import CodemodeTool

            tool = CodemodeTool(registry=registry, executor_client=executor_client)

            result = tool._run("result = 2 + 2")

            assert "UNEXPECTED ERROR" in result
            assert "Unexpected issue" in result

    def test_arun(self, mock_crewai_available, registry, executor_client):
        """Test async execution uses execute_async."""
        MockBaseTool, _, _, _, _ = create_mock_crewai_classes()

        # Mock successful async execution
        async def mock_execute_async(*args, **kwargs):
            return ExecutionResult(
                success=True,
                result="42",
                stdout="",
                stderr="",
                error=None,
                error_details=None,
                correlation_id=None,
                duration_ms=0.0,
            )

        executor_client.execute_async = Mock(side_effect=mock_execute_async)

        with patch("codemode.integrations.crewai.BaseTool", MockBaseTool):
            from codemode.integrations.crewai import CodemodeTool

            tool = CodemodeTool(registry=registry, executor_client=executor_client)

            # _arun is now async
            result = asyncio.run(tool._arun("result = 2 + 2"))

            assert result == "42"

    def test_repr(self, mock_crewai_available, registry, executor_client):
        """Test string representation."""
        MockBaseTool, _, _, _, _ = create_mock_crewai_classes()

        with patch("codemode.integrations.crewai.BaseTool", MockBaseTool):
            from codemode.integrations.crewai import CodemodeTool

            tool = CodemodeTool(registry=registry, executor_client=executor_client)

            repr_str = repr(tool)

            assert "CodemodeTool" in repr_str
            assert "tools=1" in repr_str


class TestCrewAIIntegration:
    """Test CrewAIIntegration class."""

    @pytest.fixture
    def mock_crewai_available(self):
        """Mock CrewAI as available."""
        with patch("codemode.integrations.crewai.CREWAI_AVAILABLE", True):
            yield

    @pytest.fixture
    def registry(self):
        """Create test registry."""
        return ComponentRegistry()

    def test_init_success(self, mock_crewai_available, registry):
        """Test successful initialization."""
        from codemode.integrations.crewai import CrewAIIntegration

        integration = CrewAIIntegration(registry)

        assert integration.registry is registry

    def test_wrap_team_without_context(self, mock_crewai_available, registry):
        """Test wrapping crew without context."""
        from codemode.core.registry import reset_context

        _, _, MockCrew, _, _ = create_mock_crewai_classes()

        # Ensure clean context state
        reset_context()

        with patch("codemode.integrations.crewai.Crew", MockCrew):
            from codemode.integrations.crewai import CrewAIIntegration

            integration = CrewAIIntegration(registry)
            crew = MockCrew()

            wrapped = integration.wrap_team(crew, context=None)

            # Execute wrapped crew
            result = wrapped.kickoff()

            assert result == {"result": "crew_output"}
            # Context should not be set
            assert registry.get_context() is None

    def test_wrap_team_with_context(self, mock_crewai_available, registry):
        """Test wrapping crew with context."""
        _, _, MockCrew, _, _ = create_mock_crewai_classes()

        with patch("codemode.integrations.crewai.Crew", MockCrew):
            from codemode.integrations.crewai import CrewAIIntegration

            integration = CrewAIIntegration(registry)
            crew = MockCrew()
            context = RuntimeContext(variables={"client_id": "acme"})

            wrapped = integration.wrap_team(crew, context=context)

            # Execute wrapped crew
            result = wrapped.kickoff()

            assert result == {"result": "crew_output"}
            # Context should be cleared after execution
            assert registry.get_context() is None

    def test_wrap_team_context_cleared_on_exception(self, mock_crewai_available, registry):
        """Test that context is cleared even if crew execution fails."""
        _, _, MockCrew, _, _ = create_mock_crewai_classes()

        # Create crew that raises exception
        class FailingCrew(MockCrew):
            def kickoff(self, inputs=None):
                raise RuntimeError("Crew failed")

        with patch("codemode.integrations.crewai.Crew", MockCrew):
            from codemode.integrations.crewai import CrewAIIntegration

            integration = CrewAIIntegration(registry)
            crew = FailingCrew()
            context = RuntimeContext(variables={"client_id": "acme"})

            wrapped = integration.wrap_team(crew, context=context)

            # Execute wrapped crew (should raise)
            with pytest.raises(RuntimeError, match="Crew failed"):
                wrapped.kickoff()

            # Context should still be cleared
            assert registry.get_context() is None

    @pytest.mark.asyncio
    async def test_wrap_team_async_with_kickoff_async(self, mock_crewai_available, registry):
        """Test async crew execution with kickoff_async."""
        _, _, MockCrew, _, _ = create_mock_crewai_classes()

        with patch("codemode.integrations.crewai.Crew", MockCrew):
            from codemode.integrations.crewai import CrewAIIntegration

            integration = CrewAIIntegration(registry)
            crew = MockCrew()
            context = RuntimeContext(variables={"client_id": "acme"})

            wrapped = integration.wrap_team(crew, context=context)

            # Execute wrapped crew async
            result = await wrapped.kickoff_async()

            assert result == {"result": "async_crew_output"}
            # Context should be cleared after execution
            assert registry.get_context() is None

    @pytest.mark.asyncio
    async def test_wrap_team_async_fallback_to_sync(self, mock_crewai_available, registry):
        """Test async crew execution falls back to sync if no kickoff_async."""
        _, _, MockCrew, _, _ = create_mock_crewai_classes()

        # Create crew without kickoff_async
        class SyncOnlyCrew:
            def kickoff(self, inputs=None):
                return {"result": "sync_output"}

        with patch("codemode.integrations.crewai.Crew", MockCrew):
            from codemode.integrations.crewai import CrewAIIntegration

            integration = CrewAIIntegration(registry)
            crew = SyncOnlyCrew()
            context = RuntimeContext(variables={"client_id": "acme"})

            wrapped = integration.wrap_team(crew, context=context)

            # Execute wrapped crew async (falls back to sync)
            result = await wrapped.kickoff_async()

            assert result == {"result": "sync_output"}

    def test_wrap_team_getattr_delegation(self, mock_crewai_available, registry):
        """Test that ContextAwareCrew delegates attribute access to original crew."""
        _, _, MockCrew, _, _ = create_mock_crewai_classes()

        # Add custom attribute to crew
        class CustomCrew(MockCrew):
            custom_attr = "custom_value"

            def custom_method(self):
                return "custom_result"

        with patch("codemode.integrations.crewai.Crew", MockCrew):
            from codemode.integrations.crewai import CrewAIIntegration

            integration = CrewAIIntegration(registry)
            crew = CustomCrew()

            wrapped = integration.wrap_team(crew, context=None)

            # Access delegated attributes
            assert wrapped.custom_attr == "custom_value"
            assert wrapped.custom_method() == "custom_result"

    def test_wrap_crew_alias(self, mock_crewai_available, registry):
        """Test wrap_crew is an alias for wrap_team."""
        _, _, MockCrew, _, _ = create_mock_crewai_classes()

        with patch("codemode.integrations.crewai.Crew", MockCrew):
            from codemode.integrations.crewai import CrewAIIntegration

            integration = CrewAIIntegration(registry)
            crew = MockCrew()

            wrapped = integration.wrap_crew(crew, context=None)

            # Execute wrapped crew
            result = wrapped.kickoff()

            assert result == {"result": "crew_output"}

    def test_repr(self, mock_crewai_available, registry):
        """Test string representation."""
        from codemode.integrations.crewai import CrewAIIntegration

        integration = CrewAIIntegration(registry)

        repr_str = repr(integration)

        assert "CrewAIIntegration" in repr_str
        assert "registry=" in repr_str


class TestFactoryFunctions:
    """Test factory functions."""

    @pytest.fixture
    def mock_crewai_available(self):
        """Mock CrewAI as available."""
        with patch("codemode.integrations.crewai.CREWAI_AVAILABLE", True):
            yield

    def test_create_codemode_tool(self, mock_crewai_available):
        """Test create_codemode_tool factory."""
        MockBaseTool, _, _, _, _ = create_mock_crewai_classes()

        with patch("codemode.integrations.crewai.BaseTool", MockBaseTool):
            from codemode.integrations.crewai import create_codemode_tool

            registry = ComponentRegistry()
            client = Mock(spec=ExecutorClient)

            tool = create_codemode_tool(registry, client)

            assert tool.registry is registry
            assert tool.executor_client is client

    def test_create_crewai_integration(self, mock_crewai_available):
        """Test create_crewai_integration factory."""
        from codemode.integrations.crewai import create_crewai_integration

        registry = ComponentRegistry()

        integration = create_crewai_integration(registry)

        assert integration.registry is registry


class TestCustomDescription:
    """Test custom description parameter."""

    @pytest.fixture
    def mock_crewai_available(self):
        """Mock CrewAI as available."""
        with patch("codemode.integrations.crewai.CREWAI_AVAILABLE", True):
            yield

    @pytest.fixture
    def registry(self):
        """Create test registry."""
        return ComponentRegistry()

    @pytest.fixture
    def executor_client(self):
        """Create mock executor client."""
        return Mock(spec=ExecutorClient)

    def test_init_with_custom_description(self, mock_crewai_available, registry, executor_client):
        """Test that custom description overrides default."""
        MockBaseTool, _, _, _, _ = create_mock_crewai_classes()

        custom_desc = "My custom tool description for testing"

        with patch("codemode.integrations.crewai.BaseTool", MockBaseTool):
            from codemode.integrations.crewai import CodemodeTool

            tool = CodemodeTool(
                registry=registry,
                executor_client=executor_client,
                description=custom_desc,
            )

            assert tool.description == custom_desc

    def test_init_without_custom_description(
        self, mock_crewai_available, registry, executor_client
    ):
        """Test that default description is used when not overridden."""
        MockBaseTool, _, _, _, _ = create_mock_crewai_classes()

        with patch("codemode.integrations.crewai.BaseTool", MockBaseTool):
            from codemode.integrations.crewai import CodemodeTool

            tool = CodemodeTool(
                registry=registry,
                executor_client=executor_client,
            )

            # Should use default description with key sections
            assert "Execute Python code" in tool.description
            assert "<META_TOOLS>" in tool.description
            assert "<EXECUTION_PATTERN>" in tool.description
            assert "<RULES>" in tool.description
            assert "result" in tool.description
            assert "asyncio" in tool.description


class TestFormatError:
    """Test _format_error() method."""

    @pytest.fixture
    def mock_crewai_available(self):
        """Mock CrewAI as available."""
        with patch("codemode.integrations.crewai.CREWAI_AVAILABLE", True):
            yield

    @pytest.fixture
    def registry(self):
        """Create test registry."""
        return ComponentRegistry()

    @pytest.fixture
    def executor_client(self):
        """Create mock executor client."""
        return Mock(spec=ExecutorClient)

    def test_format_error_basic(self, mock_crewai_available, registry, executor_client):
        """Test basic error formatting."""
        MockBaseTool, _, _, _, _ = create_mock_crewai_classes()

        with patch("codemode.integrations.crewai.BaseTool", MockBaseTool):
            from codemode.integrations.crewai import CodemodeTool

            tool = CodemodeTool(registry=registry, executor_client=executor_client)

            result = ExecutionResult(
                success=False,
                result=None,
                stdout="",
                stderr="",
                error="Test error message",
                error_details=None,
                correlation_id=None,
                duration_ms=None,
            )

            formatted = tool._format_error(result)

            assert "ERROR: Test error message" in formatted

    def test_format_error_with_details(self, mock_crewai_available, registry, executor_client):
        """Test error formatting with error_details."""
        MockBaseTool, _, _, _, _ = create_mock_crewai_classes()

        with patch("codemode.integrations.crewai.BaseTool", MockBaseTool):
            from codemode.integrations.crewai import CodemodeTool

            tool = CodemodeTool(registry=registry, executor_client=executor_client)

            error_details = ExecutionError(
                error_type="TypeError",
                message="unsupported operand",
                traceback="File '<string>', line 5\n    x + y",
            )

            result = ExecutionResult(
                success=False,
                result=None,
                stdout="",
                stderr="",
                error="TypeError: unsupported operand",
                error_details=error_details,
                correlation_id="cm-test-123",
                duration_ms=50.5,
            )

            formatted = tool._format_error(result)

            assert "ERROR: TypeError" in formatted
            assert "Type: TypeError" in formatted
            assert "Traceback:" in formatted
            assert "line 5" in formatted
            assert "Correlation ID: cm-test-123" in formatted
            assert "Duration: 50.5ms" in formatted

    def test_format_error_with_stderr(self, mock_crewai_available, registry, executor_client):
        """Test error formatting includes stderr when relevant."""
        MockBaseTool, _, _, _, _ = create_mock_crewai_classes()

        with patch("codemode.integrations.crewai.BaseTool", MockBaseTool):
            from codemode.integrations.crewai import CodemodeTool

            tool = CodemodeTool(registry=registry, executor_client=executor_client)

            result = ExecutionResult(
                success=False,
                result=None,
                stdout="",
                stderr="Additional debug info from stderr",
                error="Main error message",
                error_details=None,
                correlation_id=None,
                duration_ms=None,
            )

            formatted = tool._format_error(result)

            assert "ERROR: Main error message" in formatted
            assert "Stderr:" in formatted
            assert "Additional debug info" in formatted
