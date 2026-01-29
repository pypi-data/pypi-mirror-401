"""
Unit tests for CodeRunner.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from codemode.executor.models import ExecutionResult
from codemode.executor.runner import CodeExecutionError, CodeRunner
from codemode.executor.security import SecurityValidationResult, SecurityValidator


class TestCodeExecutionError:
    """Test CodeExecutionError exception."""

    def test_raise_error(self):
        """Test raising CodeExecutionError."""
        with pytest.raises(CodeExecutionError, match="Test error"):
            raise CodeExecutionError("Test error")


class TestCodeRunner:
    """Test CodeRunner class."""

    def test_init_default(self):
        """Test initialization with defaults."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        assert runner.main_app_target == "localhost:50051"
        assert runner.api_key == "test-key"
        assert runner.allow_direct_execution is False
        assert isinstance(runner.security_validator, SecurityValidator)

    def test_init_with_trailing_slash(self):
        """Test initialization strips trailing slash from URL."""
        runner = CodeRunner(main_app_target="http://localhost:50051/", api_key="test-key")

        assert runner.main_app_target == "localhost:50051"

    def test_init_with_custom_validator(self):
        """Test initialization with custom security validator."""
        custom_validator = SecurityValidator(max_code_length=5000)

        runner = CodeRunner(
            main_app_target="localhost:50051",
            api_key="test-key",
            security_validator=custom_validator,
        )

        assert runner.security_validator is custom_validator

    def test_init_with_direct_execution(self):
        """Test initialization with direct execution enabled."""
        runner = CodeRunner(
            main_app_target="localhost:50051", api_key="test-key", allow_direct_execution=True
        )

        assert runner.allow_direct_execution is True

    def test_repr(self):
        """Test string representation."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        repr_str = repr(runner)

        assert "CodeRunner" in repr_str
        assert "localhost:50051" in repr_str

    @pytest.mark.asyncio
    async def test_run_security_validation_failure(self):
        """Test run with security validation failure."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        # Mock security validator to fail
        runner.security_validator.validate = Mock(
            return_value=SecurityValidationResult(
                is_safe=False, violations=["eval()"], reason="Dangerous pattern detected: eval()"
            )
        )

        result = await runner.run(
            code="eval('malicious')", available_tools=[], tool_metadata={}, config={}, timeout=30
        )

        assert result.success is False
        assert "Security violation" in result.error
        assert "eval()" in result.error

    @pytest.mark.asyncio
    async def test_run_success_simple_code(self):
        """Test successful run with simple code."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        # Mock _execute_code to return success
        runner._execute_code = AsyncMock(
            return_value=ExecutionResult(
                success=True,
                result="4",
                stdout='__CODEMODE_RESULT__:{"result": "4"}\n',
                stderr="",
                error=None,
            )
        )

        result = await runner.run(
            code="result = 2 + 2", available_tools=[], tool_metadata={}, config={}, timeout=30
        )

        assert result.success is True
        assert result.result == "4"

    @pytest.mark.asyncio
    async def test_run_with_tools_and_context(self):
        """Test run with tools and context."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        # Mock _execute_code to return success
        runner._execute_code = AsyncMock(
            return_value=ExecutionResult.success_result(result="weather data", stdout="", stderr="")
        )

        result = await runner.run(
            code="result = tools['weather'].run(location='NYC')",
            available_tools=["weather"],
            tool_metadata={"weather": {"is_async": False, "has_context": False}},
            config={"env": "prod"},
            timeout=30,
            context={"client_id": "acme", "user_id": "user_123"},
        )

        assert result.success is True
        # Verify _execute_code was called
        runner._execute_code.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_execution_exception(self):
        """Test run when execution raises exception."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        # Mock _execute_code to raise exception
        runner._execute_code = AsyncMock(side_effect=RuntimeError("Subprocess failed"))

        result = await runner.run(
            code="result = 2 + 2", available_tools=[], tool_metadata={}, config={}, timeout=30
        )

        assert result.success is False
        assert "Execution failed" in result.error
        assert "Subprocess failed" in result.error

    def test_wrap_code_with_proxies_basic(self):
        """Test wrapping code with basic proxies."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        wrapped = runner._wrap_code_with_proxies(
            user_code="result = 2 + 2",
            available_tools=[],
            tool_metadata={},
            config={},
            context=None,
        )

        assert "ToolProxy" in wrapped
        assert "result = 2 + 2" in wrapped
        assert "__CODEMODE_RESULT__" in wrapped
        assert "grpc" in wrapped  # ensure gRPC tooling present

    def test_api_key_none_serialization(self):
        """Test that API key None is properly serialized as Python None, not string 'None'."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key=None)

        wrapped = runner._wrap_code_with_proxies(
            user_code="result = 'test'",
            available_tools=["weather"],
            tool_metadata={"weather": {"is_async": False}},
            config={},
            context=None,
        )

        # Should have API_KEY = None (Python null), not API_KEY = "None" (string)
        assert "API_KEY = None" in wrapped
        assert 'API_KEY = "None"' not in wrapped

        # Also test with an API key set
        runner_with_key = CodeRunner(main_app_target="localhost:50051", api_key="test-secret")
        wrapped_with_key = runner_with_key._wrap_code_with_proxies(
            user_code="result = 'test'",
            available_tools=[],
            tool_metadata={},
            config={},
            context=None,
        )

        # Should have API_KEY = 'test-secret' (string)
        assert "API_KEY = 'test-secret'" in wrapped_with_key

    def test_wrap_code_with_tools(self):
        """Test wrapping code with tool proxies."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        wrapped = runner._wrap_code_with_proxies(
            user_code="result = tools['weather'].run(location='NYC')",
            available_tools=["weather", "database"],
            tool_metadata={"weather": {"is_async": False}, "database": {"is_async": False}},
            config={"env": "prod"},
            context=None,
        )

        assert "ToolProxy" in wrapped
        assert "'weather': SyncToolProxy" in wrapped or "'weather': AsyncToolProxy" in wrapped
        assert "'database': SyncToolProxy" in wrapped or "'database': AsyncToolProxy" in wrapped
        assert '"env": "prod"' in wrapped
        assert "tools['weather']" in wrapped

    def test_wrap_code_with_context(self):
        """Test wrapping code with context."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        wrapped = runner._wrap_code_with_proxies(
            user_code="result = 'test'",
            available_tools=[],
            tool_metadata={},
            config={},
            context={"client_id": "acme", "user_id": "123"},
        )

        assert "CONTEXT" in wrapped
        assert '"client_id": "acme"' in wrapped
        assert '"user_id": "123"' in wrapped

    def test_wrap_code_with_direct_execution(self):
        """Test wrapping code with direct execution enabled."""
        runner = CodeRunner(
            main_app_target="localhost:50051", api_key="test-key", allow_direct_execution=True
        )

        wrapped = runner._wrap_code_with_proxies(
            user_code="result = 'test'",
            available_tools=[],
            tool_metadata={},
            config={},
            context=None,
        )

        assert "import subprocess" in wrapped
        assert "import os" in wrapped
        assert "from pathlib import Path" in wrapped

    def test_wrap_code_without_direct_execution(self):
        """Test wrapping code without direct execution."""
        runner = CodeRunner(
            main_app_target="localhost:50051", api_key="test-key", allow_direct_execution=False
        )

        wrapped = runner._wrap_code_with_proxies(
            user_code="result = 'test'",
            available_tools=[],
            tool_metadata={},
            config={},
            context=None,
        )

        # Should not include subprocess imports
        assert "import grpc" in wrapped
        assert "import json" in wrapped
        lines = wrapped.split("\n")
        subprocess_import_lines = [line for line in lines if line.strip() == "import subprocess"]
        assert len(subprocess_import_lines) == 0

    @pytest.mark.asyncio
    async def test_execute_code_success(self):
        """Test successful code execution."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        wrapped_code = """
result = 2 + 2
import json
print("__CODEMODE_RESULT__:" + json.dumps({'result': str(result)}))
"""

        result = await runner._execute_code(wrapped_code, timeout=5)

        assert result.success is True
        assert result.result == "4"

    @pytest.mark.asyncio
    async def test_execute_code_with_error(self):
        """Test code execution with runtime error."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        wrapped_code = """
raise ValueError("Test error")
"""

        result = await runner._execute_code(wrapped_code, timeout=5)

        assert result.success is False
        assert result.error is not None
        assert "ValueError" in result.stderr

    @pytest.mark.asyncio
    async def test_subprocess_blocked_by_default(self):
        """Test that subprocess imports are blocked by default for security."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        # Try to run code that imports subprocess (should be blocked)
        result = await runner.run(
            code="import subprocess; result = 'should not reach here'",
            available_tools=[],
            tool_metadata={},
            config={},
            timeout=5,
        )

        assert result.success is False
        assert "Security violation" in result.error or "Blocked import" in result.error
        assert "subprocess" in result.error.lower()

    @pytest.mark.asyncio
    async def test_direct_execution_allows_subprocess(self):
        """Test that subprocess is allowed when direct execution is enabled."""
        runner = CodeRunner(
            main_app_target="localhost:50051", api_key="test-key", allow_direct_execution=True
        )

        # Now subprocess should be allowed (but may still fail in sandbox environment)
        # We're just testing that it passes security validation
        validation = runner.security_validator.validate("import subprocess\nresult = 'ok'")

        # Should pass security validation when direct execution is enabled
        assert validation.is_safe is True
        assert "subprocess" not in [v.lower() for v in validation.violations]

    @pytest.mark.asyncio
    async def test_execute_code_subprocess_error(self):
        """Test code execution with subprocess error."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        # Mock asyncio.create_subprocess_exec to raise
        with patch("asyncio.create_subprocess_exec", side_effect=OSError("Subprocess failed")):
            result = await runner._execute_code("result = 1", timeout=5)

            assert result.success is False
            assert "Subprocess error" in result.error

    def test_extract_result_success(self):
        """Test extracting result from stdout."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        stdout = """
Some output
__CODEMODE_RESULT__:{"result": "42"}
More output
"""

        result = runner._extract_result(stdout)

        assert result == "42"

    def test_extract_result_no_marker(self):
        """Test extracting result when no marker present."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        stdout = """
Some output
No result marker here
"""

        result = runner._extract_result(stdout)

        assert result is None

    def test_extract_result_invalid_json(self):
        """Test extracting result with invalid JSON."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        stdout = """
__CODEMODE_RESULT__:{ invalid json }
"""

        result = runner._extract_result(stdout)

        assert result is None

    def test_extract_result_with_null(self):
        """Test extracting result with null value."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        stdout = '__CODEMODE_RESULT__:{"result": null}'

        result = runner._extract_result(stdout)

        assert result is None

    def test_extract_result_multiple_lines(self):
        """Test extracting result from multiple output lines."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        stdout = """
Line 1
Line 2
__CODEMODE_RESULT__:{"result": "success"}
Line 3
"""

        result = runner._extract_result(stdout)

        assert result == "success"

    @pytest.mark.asyncio
    async def test_execute_code_with_stdout_and_stderr(self):
        """Test code execution captures both stdout and stderr."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        wrapped_code = """
import sys
print("stdout message")
print("stderr message", file=sys.stderr)
import json
result = "done"
print("__CODEMODE_RESULT__:" + json.dumps({'result': str(result)}))
"""

        result = await runner._execute_code(wrapped_code, timeout=5)

        assert result.success is True
        assert "stdout message" in result.stdout
        assert "stderr message" in result.stderr
        assert result.result == "done"

    @pytest.mark.asyncio
    async def test_run_integration(self):
        """Test full integration run."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        # Real integration test - execute simple code
        result = await runner.run(
            code="result = 10 * 5", available_tools=[], tool_metadata={}, config={}, timeout=5
        )

        assert result.success is True
        assert result.result == "50"

    @pytest.mark.asyncio
    async def test_run_with_config_access(self):
        """Test code can access config dictionary."""
        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        result = await runner.run(
            code="result = config.get('test_key', 'default')",
            available_tools=[],
            tool_metadata={},
            config={"test_key": "test_value"},
            timeout=5,
        )

        assert result.success is True
        assert result.result == "test_value"
