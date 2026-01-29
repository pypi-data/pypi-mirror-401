"""
Unit tests for main Codemode class.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from codemode.config.models import CodemodeConfig, ExecutorConfig, FrameworkConfig, ProjectConfig
from codemode.core.codemode import Codemode
from codemode.core.registry import ComponentRegistry
from codemode.executor.models import ExecutionResult


@pytest.fixture
def sample_config():
    """Create sample configuration."""
    return CodemodeConfig(
        project=ProjectConfig(name="test-project"),
        framework=FrameworkConfig(type="crewai"),
        executor=ExecutorConfig(
            url="http://localhost:8001",
            api_key="test-key",
            timeout=30,
        ),
    )


@pytest.fixture
def mock_executor_client():
    """Mock executor client."""
    with patch("codemode.core.codemode.ExecutorClient") as mock:
        yield mock


class TestCodemodeInit:
    """Test Codemode initialization."""

    def test_init_with_config(self, sample_config, mock_executor_client):
        """Test initialization with config."""
        codemode = Codemode(sample_config)

        assert codemode.config == sample_config
        assert isinstance(codemode.registry, ComponentRegistry)
        assert codemode.executor_client is not None

    def test_init_with_existing_registry(self, sample_config, mock_executor_client):
        """Test initialization with existing registry."""
        registry = ComponentRegistry()
        registry.register_tool("test_tool", lambda: "result")

        codemode = Codemode(sample_config, registry=registry)

        assert codemode.registry is registry
        assert "test_tool" in codemode.registry.tools


class TestCodemodeFactoryMethods:
    """Test factory methods."""

    @patch("codemode.core.codemode.ConfigLoader")
    def test_from_config(self, mock_loader, sample_config, mock_executor_client):
        """Test creating Codemode from config file."""
        mock_loader.load.return_value = sample_config

        codemode = Codemode.from_config("codemode.yaml")

        mock_loader.load.assert_called_once_with("codemode.yaml")
        assert codemode.config == sample_config

    @patch("codemode.core.codemode.ConfigLoader")
    def test_from_config_with_path(self, mock_loader, sample_config, mock_executor_client):
        """Test creating Codemode from Path object."""
        mock_loader.load.return_value = sample_config
        path = Path("codemode.yaml")

        _codemode = Codemode.from_config(path)

        mock_loader.load.assert_called_once_with(path)

    @patch("codemode.core.codemode.ConfigLoader")
    def test_from_dict(self, mock_loader, sample_config, mock_executor_client):
        """Test creating Codemode from dictionary."""
        config_dict = {
            "project": {"name": "test"},
            "framework": {"type": "crewai"},
            "executor": {"url": "http://localhost:8001", "api_key": "key"},
        }
        mock_loader.load_dict.return_value = sample_config

        codemode = Codemode.from_dict(config_dict)

        mock_loader.load_dict.assert_called_once_with(config_dict)
        assert codemode.config == sample_config


class TestCodemodeContextAndConfig:
    """Test context and config methods."""

    def test_with_context(self, sample_config, mock_executor_client):
        """Test setting context."""
        codemode = Codemode(sample_config)

        result = codemode.with_context(client_id="acme", user_id="123")

        assert result is codemode  # Fluent API
        context = codemode.registry.get_context()
        assert context is not None
        assert context.get("client_id") == "acme"
        assert context.get("user_id") == "123"

    @pytest.mark.asyncio
    async def test_with_context_async(self, sample_config, mock_executor_client):
        """Test async context setting."""
        codemode = Codemode(sample_config)

        result = await codemode.with_context_async(client_id="acme")

        assert result is codemode
        context = codemode.registry.get_context()
        assert context.get("client_id") == "acme"

    def test_with_config(self, sample_config, mock_executor_client):
        """Test setting config."""
        codemode = Codemode(sample_config)

        result = codemode.with_config(timeout=60, max_retries=3)

        assert result is codemode  # Fluent API
        assert codemode.registry.config["timeout"] == 60
        assert codemode.registry.config["max_retries"] == 3

    @pytest.mark.asyncio
    async def test_with_config_async(self, sample_config, mock_executor_client):
        """Test async config setting."""
        codemode = Codemode(sample_config)

        result = await codemode.with_config_async(timeout=60)

        assert result is codemode
        assert codemode.registry.config["timeout"] == 60


class TestCodemodeExecution:
    """Test code execution."""

    def test_execute_success(self, sample_config):
        """Test successful code execution."""
        with patch("codemode.core.codemode.ExecutorClient") as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.execute.return_value = ExecutionResult(
                success=True, result="42", stdout="", stderr="", error=None
            )

            codemode = Codemode(sample_config)
            result = codemode.execute("result = 2 + 2")

            assert result == "42"
            mock_client_instance.execute.assert_called_once()

    def test_execute_with_custom_timeout(self, sample_config):
        """Test execution with custom timeout."""
        with patch("codemode.core.codemode.ExecutorClient") as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.execute.return_value = ExecutionResult(
                success=True, result="done", stdout="", stderr="", error=None
            )

            codemode = Codemode(sample_config)
            _result = codemode.execute("import time; time.sleep(1)", execution_timeout=10)

            call_kwargs = mock_client_instance.execute.call_args.kwargs
            assert call_kwargs["execution_timeout"] == 10

    def test_execute_failure(self, sample_config):
        """Test failed code execution."""
        with patch("codemode.core.codemode.ExecutorClient") as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.execute.return_value = ExecutionResult(
                success=False,
                result=None,
                stdout="",
                stderr="",
                error="NameError: name 'x' is not defined",
            )

            codemode = Codemode(sample_config)
            result = codemode.execute("print(x)")

            assert "ERROR:" in result
            assert "NameError" in result

    def test_execute_with_tools(self, sample_config):
        """Test execution with registered tools."""
        with patch("codemode.core.codemode.ExecutorClient") as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.execute.return_value = ExecutionResult(
                success=True, result="result", stdout="", stderr="", error=None
            )

            codemode = Codemode(sample_config)
            codemode.registry.register_tool("weather", lambda location: f"Weather in {location}")

            _result = codemode.execute("result = tools['weather']('NYC')")

            call_kwargs = mock_client_instance.execute.call_args.kwargs
            assert "weather" in call_kwargs["available_tools"]

    def test_execute_with_context(self, sample_config):
        """Test execution with context."""
        with patch("codemode.core.codemode.ExecutorClient") as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.execute.return_value = ExecutionResult(
                success=True, result="result", stdout="", stderr="", error=None
            )

            codemode = Codemode(sample_config)
            codemode.with_context(client_id="acme")

            _result = codemode.execute("print(context['client_id'])")

            call_kwargs = mock_client_instance.execute.call_args.kwargs
            assert call_kwargs["context"] is not None

    @pytest.mark.asyncio
    async def test_execute_async(self, sample_config):
        """Test async code execution."""
        with patch("codemode.core.codemode.ExecutorClient") as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.execute.return_value = ExecutionResult(
                success=True, result="42", stdout="", stderr="", error=None
            )

            codemode = Codemode(sample_config)
            result = await codemode.execute_async("result = 2 + 2")

            assert result == "42"


class TestCodemodeCrewAIIntegration:
    """Test CrewAI integration."""

    def test_as_crewai_tool_success(self, sample_config, mock_executor_client):
        """Test creating CrewAI tool."""
        with patch("codemode.integrations.crewai.create_codemode_tool") as mock_create:
            mock_tool = MagicMock()
            mock_create.return_value = mock_tool

            codemode = Codemode(sample_config)
            tool = codemode.as_crewai_tool()

            assert tool is mock_tool
            mock_create.assert_called_once()

    def test_as_crewai_tool_import_error(self, sample_config, mock_executor_client):
        """Test CrewAI tool creation when CrewAI not installed."""
        # Simulate ImportError when importing the module
        with patch.dict("sys.modules", {"codemode.integrations.crewai": None}):
            codemode = Codemode(sample_config)

            with pytest.raises(ImportError, match="CrewAI is required"):
                codemode.as_crewai_tool()


class TestCodemodeHealthChecks:
    """Test health check methods."""

    def test_health_check_healthy(self, sample_config):
        """Test health check when executor is healthy."""
        with patch("codemode.core.codemode.ExecutorClient") as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.health_check.return_value = True

            codemode = Codemode(sample_config)
            result = codemode.health_check()

            assert result is True
            mock_client_instance.health_check.assert_called_once()

    def test_health_check_unhealthy(self, sample_config):
        """Test health check when executor is unhealthy."""
        with patch("codemode.core.codemode.ExecutorClient") as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.health_check.return_value = False

            codemode = Codemode(sample_config)
            result = codemode.health_check()

            assert result is False

    def test_ready_check_ready(self, sample_config):
        """Test readiness check when executor is ready."""
        with patch("codemode.core.codemode.ExecutorClient") as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.ready_check.return_value = True

            codemode = Codemode(sample_config)
            result = codemode.ready_check()

            assert result is True

    def test_ready_check_not_ready(self, sample_config):
        """Test readiness check when executor is not ready."""
        with patch("codemode.core.codemode.ExecutorClient") as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.ready_check.return_value = False

            codemode = Codemode(sample_config)
            result = codemode.ready_check()

            assert result is False


class TestCodemodeLifecycle:
    """Test lifecycle methods."""

    def test_close(self, sample_config):
        """Test closing resources."""
        with patch("codemode.core.codemode.ExecutorClient") as MockClient:
            mock_client_instance = MockClient.return_value

            codemode = Codemode(sample_config)
            codemode.close()

            mock_client_instance.close.assert_called_once()

    def test_context_manager(self, sample_config):
        """Test using Codemode as context manager."""
        with patch("codemode.core.codemode.ExecutorClient") as MockClient:
            mock_client_instance = MockClient.return_value

            with Codemode(sample_config) as codemode:
                assert codemode is not None

            mock_client_instance.close.assert_called_once()

    def test_repr(self, sample_config, mock_executor_client):
        """Test string representation."""
        codemode = Codemode(sample_config)
        codemode.registry.register_tool("tool1", lambda: "result")
        codemode.registry.register_tool("tool2", lambda: "result")

        repr_str = repr(codemode)

        assert "Codemode" in repr_str
        assert "test-project" in repr_str
        assert "crewai" in repr_str
        assert "tools=2" in repr_str
