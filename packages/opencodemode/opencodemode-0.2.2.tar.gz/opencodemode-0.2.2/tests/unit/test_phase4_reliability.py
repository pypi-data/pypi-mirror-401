"""
Unit tests for Phase 4 Reliability & Observability features.

Tests cover:
- Correlation ID generation
- Retry logic in ExecutorClient
- Structured error parsing (_parse_traceback, _classify_error)
- ExecutionResult with correlation_id, error_details, duration_ms
"""

import time
from unittest.mock import Mock, patch

import grpc
import pytest

from codemode.core.correlation import _to_base36, generate_correlation_id
from codemode.executor.models import ExecutionError, ExecutionResult
from codemode.executor.runner import _classify_error, _parse_traceback

# =============================================================================
# Correlation ID Tests
# =============================================================================


class TestCorrelationId:
    """Tests for correlation ID generation."""

    def test_generate_correlation_id_format(self):
        """Test correlation ID has expected format: prefix-timestamp-random."""
        cid = generate_correlation_id()

        parts = cid.split("-")
        assert len(parts) == 3, f"Expected 3 parts, got {len(parts)}: {cid}"
        assert parts[0] == "cm", f"Expected prefix 'cm', got '{parts[0]}'"
        assert len(parts[1]) == 6, f"Expected 6-char timestamp, got {len(parts[1])}: {parts[1]}"
        assert len(parts[2]) == 4, f"Expected 4-char suffix, got {len(parts[2])}: {parts[2]}"

    def test_generate_correlation_id_custom_prefix(self):
        """Test correlation ID with custom prefix."""
        cid = generate_correlation_id(prefix="myapp")

        assert cid.startswith("myapp-")

    def test_generate_correlation_id_unique(self):
        """Test that generated IDs are unique."""
        ids = [generate_correlation_id() for _ in range(100)]

        assert len(set(ids)) == 100, "Expected all IDs to be unique"

    def test_to_base36_zero(self):
        """Test base36 encoding of zero."""
        assert _to_base36(0) == "0"

    def test_to_base36_values(self):
        """Test base36 encoding of various values."""
        assert _to_base36(35) == "z"
        assert _to_base36(36) == "10"
        assert _to_base36(10) == "a"

    def test_to_base36_large_number(self):
        """Test base36 encoding of large numbers."""
        result = _to_base36(1234567890)
        assert result.isalnum()
        assert len(result) < 10  # Compact representation


# =============================================================================
# Error Parsing Tests
# =============================================================================


class TestParseTraceback:
    """Tests for _parse_traceback function."""

    def test_parse_simple_traceback(self):
        """Test parsing a simple Python traceback."""
        stderr = """Traceback (most recent call last):
  File "test.py", line 10, in <module>
    result = process_data()
  File "test.py", line 5, in process_data
    return int("not a number")
ValueError: invalid literal for int()"""

        tb = _parse_traceback(stderr, limit=5)

        assert tb is not None
        assert "Traceback (most recent call last):" in tb
        assert "File" in tb
        assert "ValueError" in tb

    def test_parse_traceback_limit(self):
        """Test traceback frame limiting."""
        stderr = """Traceback (most recent call last):
  File "a.py", line 1, in a
    b()
  File "b.py", line 2, in b
    c()
  File "c.py", line 3, in c
    d()
  File "d.py", line 4, in d
    raise ValueError("error")
ValueError: error"""

        tb = _parse_traceback(stderr, limit=2)

        assert tb is not None
        assert "Traceback (most recent call last):" in tb
        # Should only have last 2 frames (c.py and d.py)
        lines = tb.split("\n")
        file_lines = [line for line in lines if line.strip().startswith("File")]
        assert len(file_lines) <= 2

    def test_parse_traceback_no_traceback(self):
        """Test when there's no traceback in stderr."""
        stderr = "Some random error message without traceback"

        tb = _parse_traceback(stderr, limit=5)

        assert tb is None

    def test_parse_traceback_empty(self):
        """Test with empty stderr."""
        tb = _parse_traceback("", limit=5)
        assert tb is None

    def test_parse_traceback_disabled(self):
        """Test with limit=0 (disabled)."""
        stderr = """Traceback (most recent call last):
  File "test.py", line 1, in <module>
    raise ValueError("test")
ValueError: test"""

        tb = _parse_traceback(stderr, limit=0)

        assert tb is None


class TestClassifyError:
    """Tests for _classify_error function."""

    def test_classify_security_violation(self):
        """Test classification of security violations."""
        assert _classify_error("Security violation: import os forbidden", 1) == "SecurityViolation"
        assert _classify_error("security violation detected", 1) == "SecurityViolation"

    def test_classify_timeout(self):
        """Test classification of timeout errors."""
        assert _classify_error("timeout after 30 seconds", 1) == "Timeout"
        assert _classify_error("Execution Timeout", 1) == "Timeout"

    def test_classify_python_errors(self):
        """Test classification of Python exception types."""
        assert _classify_error("TypeError: unsupported operand", 1) == "TypeError"
        assert _classify_error("ValueError: invalid literal", 1) == "ValueError"
        assert _classify_error("KeyError: 'missing_key'", 1) == "KeyError"
        assert _classify_error("SyntaxError: invalid syntax", 1) == "SyntaxError"
        assert _classify_error("AttributeError: no attribute", 1) == "AttributeError"
        assert _classify_error("NameError: name not defined", 1) == "NameError"
        assert _classify_error("IndexError: list index out of range", 1) == "IndexError"
        assert _classify_error("ZeroDivisionError: division by zero", 1) == "ZeroDivisionError"

    def test_classify_import_error(self):
        """Test classification of import errors."""
        assert _classify_error("ImportError: No module named 'foo'", 1) == "ImportError"
        assert _classify_error("ModuleNotFoundError: No module named 'bar'", 1) == "ImportError"

    def test_classify_runtime_error_on_failure(self):
        """Test RuntimeError classification when process fails without specific error."""
        assert _classify_error("", 1) == "RuntimeError"
        assert _classify_error("some unknown error", 1) == "RuntimeError"

    def test_classify_unknown_on_success(self):
        """Test Unknown classification when no error and success."""
        assert _classify_error("", 0) == "Unknown"


# =============================================================================
# ExecutionResult Tests
# =============================================================================


class TestExecutionResult:
    """Tests for ExecutionResult with Phase 4 fields."""

    def test_success_result_with_correlation_id(self):
        """Test creating success result with correlation ID."""
        result = ExecutionResult.success_result(
            result="42",
            stdout="output",
            stderr="",
            correlation_id="cm-abc123-xyz1",
            duration_ms=150.5,
        )

        assert result.success is True
        assert result.result == "42"
        assert result.correlation_id == "cm-abc123-xyz1"
        assert result.duration_ms == 150.5
        assert result.error_details is None

    def test_error_result_with_details(self):
        """Test creating error result with structured error details."""
        error_details = ExecutionError(
            error_type="TypeError",
            message="unsupported operand type(s)",
            traceback="File 'test.py', line 5...",
        )

        result = ExecutionResult.error_result(
            error="TypeError: unsupported operand type(s)",
            stdout="",
            stderr="TypeError: unsupported operand type(s)",
            error_details=error_details,
            correlation_id="cm-err456-def2",
            duration_ms=25.3,
        )

        assert result.success is False
        assert result.error_details is not None
        assert result.error_details.error_type == "TypeError"
        assert result.error_details.message == "unsupported operand type(s)"
        assert result.correlation_id == "cm-err456-def2"
        assert result.duration_ms == 25.3

    def test_error_result_without_details(self):
        """Test creating error result without structured details."""
        result = ExecutionResult.error_result(
            error="Unknown error",
            correlation_id="cm-xyz789-abc3",
        )

        assert result.success is False
        assert result.error_details is None
        assert result.correlation_id == "cm-xyz789-abc3"

    def test_execution_result_repr(self):
        """Test string representation includes correlation ID."""
        result = ExecutionResult(
            success=True,
            result="ok",
            stdout="",
            stderr="",
            error=None,
            error_details=None,
            correlation_id="cm-test-1234",
            duration_ms=None,
        )

        repr_str = repr(result)
        assert "success=True" in repr_str
        assert "cm-test-1234" in repr_str


# =============================================================================
# ExecutorClient Retry Logic Tests
# =============================================================================


class FakeChannel:
    """Fake gRPC channel for testing."""

    def close(self):
        pass


class FakeResponse:
    """Fake gRPC response for testing."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class FakeRpcError(grpc.RpcError):
    """Fake gRPC error for testing."""

    def __init__(self, code, details="error"):
        self._code = code
        self._details = details

    def code(self):
        return self._code

    def details(self):
        return self._details


class TestExecutorClientRetry:
    """Tests for ExecutorClient retry logic."""

    @pytest.fixture(autouse=True)
    def patch_grpc(self, monkeypatch):
        """Patch gRPC channel creation for all tests."""
        import codemode.core.executor_client as executor_client

        monkeypatch.setattr(
            executor_client.grpc, "insecure_channel", lambda *_args, **_kwargs: FakeChannel()
        )

    def test_retry_disabled(self, monkeypatch):
        """Test that retry can be disabled."""
        import codemode.core.executor_client as executor_client
        from codemode.core.executor_client import ExecutorClient, ExecutorConnectionError

        call_count = 0

        class FailingStub:
            def __init__(self, *args, **kwargs):
                pass

            def Execute(self, request, timeout=None, metadata=None):
                nonlocal call_count
                call_count += 1
                raise FakeRpcError(grpc.StatusCode.UNAVAILABLE)

            def Health(self, request, timeout=None):
                return FakeResponse(status="healthy")

            def Ready(self, request, timeout=None):
                return FakeResponse(status="ready")

        monkeypatch.setattr(executor_client.codemode_pb2_grpc, "ExecutorServiceStub", FailingStub)

        client = ExecutorClient(
            "localhost:8001",
            "key",
            retry_enabled=False,  # Disable retry
        )

        with pytest.raises(ExecutorConnectionError):
            client.execute(code="x", available_tools=[], config={})

        assert call_count == 1, "Should only call once when retry is disabled"
        client.close()

    def test_retry_on_unavailable(self, monkeypatch):
        """Test retry on UNAVAILABLE error."""
        import codemode.core.executor_client as executor_client
        from codemode.core.executor_client import ExecutorClient

        call_count = 0

        class RetryThenSucceedStub:
            def __init__(self, *args, **kwargs):
                pass

            def Execute(self, request, timeout=None, metadata=None):
                nonlocal call_count
                call_count += 1
                if call_count < 3:
                    raise FakeRpcError(grpc.StatusCode.UNAVAILABLE)
                return FakeResponse(success=True, result="ok", stdout="", stderr="", error="")

            def Health(self, request, timeout=None):
                return FakeResponse(status="healthy")

            def Ready(self, request, timeout=None):
                return FakeResponse(status="ready")

        monkeypatch.setattr(
            executor_client.codemode_pb2_grpc, "ExecutorServiceStub", RetryThenSucceedStub
        )

        # Use very short backoff for fast test
        client = ExecutorClient(
            "localhost:8001",
            "key",
            retry_enabled=True,
            retry_max_attempts=3,
            retry_backoff_base_ms=1,  # Very short for tests
            retry_backoff_max_ms=10,
        )

        result = client.execute(code="x", available_tools=[], config={})

        assert result.success is True
        assert call_count == 3, "Should retry until success"
        client.close()

    def test_no_retry_on_non_transient_error(self, monkeypatch):
        """Test that non-transient errors are not retried."""
        import codemode.core.executor_client as executor_client
        from codemode.core.executor_client import ExecutorClient, ExecutorClientError

        call_count = 0

        class InternalErrorStub:
            def __init__(self, *args, **kwargs):
                pass

            def Execute(self, request, timeout=None, metadata=None):
                nonlocal call_count
                call_count += 1
                raise FakeRpcError(grpc.StatusCode.INTERNAL, "internal error")

            def Health(self, request, timeout=None):
                return FakeResponse(status="healthy")

            def Ready(self, request, timeout=None):
                return FakeResponse(status="ready")

        monkeypatch.setattr(
            executor_client.codemode_pb2_grpc, "ExecutorServiceStub", InternalErrorStub
        )

        client = ExecutorClient("localhost:8001", "key", retry_max_attempts=3)

        with pytest.raises(ExecutorClientError):
            client.execute(code="x", available_tools=[], config={})

        assert call_count == 1, "Should not retry non-transient errors"
        client.close()

    def test_correlation_id_auto_generated(self, monkeypatch):
        """Test that correlation ID is auto-generated."""
        import codemode.core.executor_client as executor_client
        from codemode.core.executor_client import ExecutorClient

        captured_metadata = None

        class CapturingStub:
            def __init__(self, *args, **kwargs):
                pass

            def Execute(self, request, timeout=None, metadata=None):
                nonlocal captured_metadata
                captured_metadata = metadata
                return FakeResponse(success=True, result="ok", stdout="", stderr="", error="")

            def Health(self, request, timeout=None):
                return FakeResponse(status="healthy")

            def Ready(self, request, timeout=None):
                return FakeResponse(status="ready")

        monkeypatch.setattr(executor_client.codemode_pb2_grpc, "ExecutorServiceStub", CapturingStub)

        client = ExecutorClient(
            "localhost:8001",
            "key",
            include_correlation_id=True,  # Default
        )

        result = client.execute(code="x", available_tools=[], config={})

        assert result.success is True
        assert result.correlation_id is not None
        assert result.correlation_id.startswith("cm-")

        # Check metadata contains correlation ID
        assert captured_metadata is not None
        metadata_dict = dict(captured_metadata)
        assert "x-correlation-id" in metadata_dict
        assert metadata_dict["x-correlation-id"] == result.correlation_id

        client.close()

    def test_correlation_id_custom_prefix(self, monkeypatch):
        """Test correlation ID with custom prefix."""
        import codemode.core.executor_client as executor_client
        from codemode.core.executor_client import ExecutorClient

        class SuccessStub:
            def __init__(self, *args, **kwargs):
                pass

            def Execute(self, request, timeout=None, metadata=None):
                return FakeResponse(success=True, result="ok", stdout="", stderr="", error="")

            def Health(self, request, timeout=None):
                return FakeResponse(status="healthy")

            def Ready(self, request, timeout=None):
                return FakeResponse(status="ready")

        monkeypatch.setattr(executor_client.codemode_pb2_grpc, "ExecutorServiceStub", SuccessStub)

        client = ExecutorClient(
            "localhost:8001",
            "key",
            correlation_id_prefix="myapp",
        )

        result = client.execute(code="x", available_tools=[], config={})

        assert result.correlation_id is not None
        assert result.correlation_id.startswith("myapp-")
        client.close()

    def test_correlation_id_provided(self, monkeypatch):
        """Test that provided correlation ID is used."""
        import codemode.core.executor_client as executor_client
        from codemode.core.executor_client import ExecutorClient

        class SuccessStub:
            def __init__(self, *args, **kwargs):
                pass

            def Execute(self, request, timeout=None, metadata=None):
                return FakeResponse(success=True, result="ok", stdout="", stderr="", error="")

            def Health(self, request, timeout=None):
                return FakeResponse(status="healthy")

            def Ready(self, request, timeout=None):
                return FakeResponse(status="ready")

        monkeypatch.setattr(executor_client.codemode_pb2_grpc, "ExecutorServiceStub", SuccessStub)

        client = ExecutorClient("localhost:8001", "key")

        result = client.execute(
            code="x",
            available_tools=[],
            config={},
            correlation_id="custom-id-12345",
        )

        assert result.correlation_id == "custom-id-12345"
        client.close()

    def test_duration_ms_recorded(self, monkeypatch):
        """Test that execution duration is recorded."""
        import codemode.core.executor_client as executor_client
        from codemode.core.executor_client import ExecutorClient

        class SlowStub:
            def __init__(self, *args, **kwargs):
                pass

            def Execute(self, request, timeout=None, metadata=None):
                time.sleep(0.05)  # 50ms delay
                return FakeResponse(success=True, result="ok", stdout="", stderr="", error="")

            def Health(self, request, timeout=None):
                return FakeResponse(status="healthy")

            def Ready(self, request, timeout=None):
                return FakeResponse(status="ready")

        monkeypatch.setattr(executor_client.codemode_pb2_grpc, "ExecutorServiceStub", SlowStub)

        client = ExecutorClient("localhost:8001", "key")

        result = client.execute(code="x", available_tools=[], config={})

        assert result.duration_ms is not None
        assert result.duration_ms >= 50  # At least 50ms
        client.close()

    def test_calculate_backoff(self):
        """Test exponential backoff calculation."""
        from codemode.core.executor_client import ExecutorClient

        # Create client with known backoff parameters
        with patch(
            "codemode.core.executor_client.grpc.insecure_channel", return_value=FakeChannel()
        ):
            with patch("codemode.core.executor_client.codemode_pb2_grpc.ExecutorServiceStub"):
                client = ExecutorClient(
                    "localhost:8001",
                    "key",
                    retry_backoff_base_ms=100,
                    retry_backoff_max_ms=5000,
                )

        # Test exponential growth with some jitter tolerance
        backoff_0 = client._calculate_backoff(0)
        backoff_1 = client._calculate_backoff(1)
        backoff_2 = client._calculate_backoff(2)

        # Backoff should roughly double each attempt (with jitter 0.8-1.2x)
        assert 0.08 <= backoff_0 <= 0.12  # ~100ms
        assert 0.16 <= backoff_1 <= 0.24  # ~200ms
        assert 0.32 <= backoff_2 <= 0.48  # ~400ms

        # Should cap at max
        backoff_high = client._calculate_backoff(10)  # Would be 100 * 2^10 = 102400ms
        assert backoff_high <= 5.0  # Capped at 5000ms = 5s


# =============================================================================
# CodeRunner with Correlation ID Tests
# =============================================================================


class TestCodeRunnerCorrelation:
    """Tests for CodeRunner correlation ID support."""

    @pytest.mark.asyncio
    async def test_run_with_correlation_id(self):
        """Test that correlation ID is passed through runner."""
        from codemode.executor.runner import CodeRunner

        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        # Mock _execute_code to capture correlation_id
        captured_correlation_id = None

        async def mock_execute(wrapped_code, timeout, correlation_id=None):
            nonlocal captured_correlation_id
            captured_correlation_id = correlation_id
            return ExecutionResult.success_result(
                result="ok",
                stdout="",
                stderr="",
                correlation_id=correlation_id,
            )

        runner._execute_code = mock_execute

        result = await runner.run(
            code="result = 1",
            available_tools=[],
            tool_metadata={},
            config={},
            correlation_id="test-corr-id",
        )

        assert result.success is True
        assert captured_correlation_id == "test-corr-id"
        assert result.correlation_id == "test-corr-id"

    @pytest.mark.asyncio
    async def test_security_violation_includes_error_details(self):
        """Test that security violations include structured error details."""
        from codemode.executor.runner import CodeRunner
        from codemode.executor.security import SecurityValidationResult

        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        # Mock security validator to fail
        runner.security_validator.validate = Mock(
            return_value=SecurityValidationResult(
                is_safe=False,
                violations=["eval()"],
                reason="Dangerous pattern detected: eval()",
            )
        )

        result = await runner.run(
            code="eval('bad')",
            available_tools=[],
            tool_metadata={},
            config={},
            correlation_id="sec-test-123",
        )

        assert result.success is False
        assert result.error_details is not None
        assert result.error_details.error_type == "SecurityViolation"
        assert result.correlation_id == "sec-test-123"

    @pytest.mark.asyncio
    async def test_execute_code_error_details(self):
        """Test that code execution errors include structured details."""
        from codemode.executor.runner import CodeRunner

        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        # Execute code that raises ValueError
        result = await runner._execute_code(
            wrapped_code='raise ValueError("test error")',
            timeout=5,
            correlation_id="val-err-123",
        )

        assert result.success is False
        assert result.error_details is not None
        assert result.error_details.error_type == "ValueError"
        assert result.correlation_id == "val-err-123"
        assert result.duration_ms is not None
        assert result.duration_ms > 0

    @pytest.mark.asyncio
    async def test_execute_code_timeout_error_details(self):
        """Test that timeout errors include structured details."""
        from codemode.executor.runner import CodeRunner

        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        # Execute code that times out
        result = await runner._execute_code(
            wrapped_code="import time; time.sleep(10)",
            timeout=1,  # 1 second timeout
            correlation_id="timeout-123",
        )

        assert result.success is False
        assert result.error_details is not None
        assert result.error_details.error_type == "Timeout"
        assert "timed out" in result.error_details.message.lower()
        assert result.correlation_id == "timeout-123"

    @pytest.mark.asyncio
    async def test_execute_code_success_with_duration(self):
        """Test successful execution includes duration."""
        from codemode.executor.runner import CodeRunner

        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        result = await runner._execute_code(
            wrapped_code='import json; print("__CODEMODE_RESULT__:" + json.dumps({"result": "ok"}))',
            timeout=5,
            correlation_id="success-123",
        )

        assert result.success is True
        assert result.correlation_id == "success-123"
        assert result.duration_ms is not None
        assert result.duration_ms > 0


class TestCodeRunnerErrorMessageExtraction:
    """Tests for error message extraction from stderr."""

    def test_extract_error_message_value_error(self):
        """Test extracting ValueError message."""
        from codemode.executor.runner import CodeRunner

        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        stderr = """Traceback (most recent call last):
  File "test.py", line 1, in <module>
    int("not a number")
ValueError: invalid literal for int() with base 10: 'not a number'"""

        message = runner._extract_error_message(stderr)
        assert message == "invalid literal for int() with base 10: 'not a number'"

    def test_extract_error_message_type_error(self):
        """Test extracting TypeError message."""
        from codemode.executor.runner import CodeRunner

        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        stderr = "TypeError: unsupported operand type(s) for +: 'int' and 'str'"

        message = runner._extract_error_message(stderr)
        assert message is not None
        assert "unsupported operand" in message

    def test_extract_error_message_none(self):
        """Test with no error message."""
        from codemode.executor.runner import CodeRunner

        runner = CodeRunner(main_app_target="localhost:50051", api_key="test-key")

        assert runner._extract_error_message("") is None
        assert runner._extract_error_message("no error pattern here") is None
