"""
Unit tests for security validator.
"""

from codemode.executor.security import SecurityValidationResult, SecurityValidator


class TestSecurityValidationResult:
    """Test SecurityValidationResult dataclass."""

    def test_safe_result(self):
        """Test creating a safe result."""
        result = SecurityValidationResult.safe()

        assert result.is_safe is True
        assert result.violations == []
        assert result.reason == ""

    def test_unsafe_result(self):
        """Test creating an unsafe result."""
        result = SecurityValidationResult.unsafe(
            violations=["eval", "exec"], reason="Dangerous patterns detected"
        )

        assert result.is_safe is False
        assert result.violations == ["eval", "exec"]
        assert result.reason == "Dangerous patterns detected"

    def test_result_with_custom_fields(self):
        """Test creating result with custom values."""
        result = SecurityValidationResult(is_safe=False, violations=["test"], reason="Test reason")

        assert result.is_safe is False
        assert result.violations == ["test"]
        assert result.reason == "Test reason"


class TestSecurityValidatorInit:
    """Test SecurityValidator initialization."""

    def test_default_initialization(self):
        """Test validator with default settings."""
        validator = SecurityValidator()

        assert validator.max_code_length == 10000
        assert validator.allow_direct_execution is False
        assert len(validator.blocked_patterns) > 0
        assert len(validator.blocked_imports) > 0
        assert validator.allowed_commands == set()
        assert validator.allowed_paths == {}

    def test_custom_max_code_length(self):
        """Test validator with custom max code length."""
        validator = SecurityValidator(max_code_length=5000)

        assert validator.max_code_length == 5000

    def test_additional_blocked_patterns(self):
        """Test validator with additional blocked patterns."""
        validator = SecurityValidator(additional_blocked_patterns=["dangerous_func"])

        assert "dangerous_func" in validator.blocked_patterns
        assert "eval(" in validator.blocked_patterns  # Original patterns still there

    def test_additional_blocked_imports(self):
        """Test validator with additional blocked imports."""
        validator = SecurityValidator(additional_blocked_imports=["custom_dangerous_module"])

        assert "custom_dangerous_module" in validator.blocked_imports
        assert "subprocess" in validator.blocked_imports  # Original imports still there

    def test_allow_direct_execution(self):
        """Test validator with direct execution enabled."""
        validator = SecurityValidator(
            allow_direct_execution=True,
            allowed_commands=["grep", "cat", "ls"],
            allowed_paths={"/workspace": "r", "/sandbox": "rw"},
        )

        assert validator.allow_direct_execution is True
        assert "grep" in validator.allowed_commands
        assert "/workspace" in validator.allowed_paths
        # When direct execution is enabled, some blocks are relaxed
        assert "open(" not in validator.blocked_patterns
        assert "subprocess" not in validator.blocked_imports

    def test_repr(self):
        """Test string representation."""
        validator = SecurityValidator()

        repr_str = repr(validator)

        assert "SecurityValidator" in repr_str
        assert "max_length=10000" in repr_str
        assert "direct_execution=False" in repr_str


class TestSecurityValidatorBasicChecks:
    """Test basic security validation."""

    def test_validate_safe_code(self):
        """Test validation of safe code."""
        validator = SecurityValidator()

        result = validator.validate("result = 2 + 2")

        assert result.is_safe is True
        assert result.violations == []

    def test_validate_max_length_exceeded(self):
        """Test code exceeding max length."""
        validator = SecurityValidator(max_code_length=100)

        code = "x = 1\n" * 100  # Definitely over 100 chars
        result = validator.validate(code)

        assert result.is_safe is False
        assert "max_length_exceeded" in result.violations
        assert "maximum length" in result.reason

    def test_validate_blocked_pattern(self):
        """Test code with blocked patterns."""
        validator = SecurityValidator()

        result = validator.validate("eval('2 + 2')")

        assert result.is_safe is False
        assert "eval(" in result.violations
        assert "Blocked pattern" in result.reason

    def test_validate_multiple_blocked_patterns(self):
        """Test code with multiple blocked patterns."""
        validator = SecurityValidator()

        result = validator.validate("eval('x'); exec('y')")

        assert result.is_safe is False
        assert "eval(" in result.violations
        assert "exec(" in result.violations


class TestSecurityValidatorImportChecks:
    """Test import validation."""

    def test_validate_blocked_import(self):
        """Test code with blocked import."""
        validator = SecurityValidator()

        result = validator.validate("import subprocess")

        assert result.is_safe is False
        assert "subprocess" in result.violations
        assert "Blocked import" in result.reason

    def test_validate_blocked_from_import(self):
        """Test code with blocked from import."""
        validator = SecurityValidator()

        result = validator.validate("from os import system")

        assert result.is_safe is False
        assert "os" in result.violations

    def test_validate_safe_import(self):
        """Test code with safe import."""
        validator = SecurityValidator()

        result = validator.validate("import json")

        assert result.is_safe is True

    def test_validate_nested_import(self):
        """Test code with nested module import."""
        validator = SecurityValidator()

        result = validator.validate("from http.client import HTTPConnection")

        assert result.is_safe is False
        assert "http" in result.violations


class TestSecurityValidatorSuspiciousPatterns:
    """Test suspicious pattern detection."""

    def test_infinite_loop_detection(self):
        """Test detection of infinite loops."""
        validator = SecurityValidator()

        result = validator.validate("while True: pass")

        assert result.is_safe is False
        assert "infinite_loop" in result.violations
        assert "Suspicious pattern" in result.reason

    def test_excessive_functions_detection(self):
        """Test detection of excessive function definitions."""
        validator = SecurityValidator()

        # Create code with more than 10 function definitions
        code = "\n".join([f"def func{i}(): pass" for i in range(15)])
        result = validator.validate(code)

        assert result.is_safe is False
        assert "excessive_functions" in result.violations

    def test_unicode_encoding_detection(self):
        """Test detection of unicode encoding tricks."""
        validator = SecurityValidator()

        result = validator.validate("x = '\\x41\\x42\\x43'")

        assert result.is_safe is False
        assert "unicode_encoding" in result.violations

    def test_long_embedded_string_detection(self):
        """Test detection of long embedded strings."""
        validator = SecurityValidator()

        # Create a string longer than 1000 characters
        long_string = "x" * 1500
        code = f'data = "{long_string}"'
        result = validator.validate(code)

        assert result.is_safe is False
        assert "long_embedded_string" in result.violations


class TestSecurityValidatorDirectExecution:
    """Test direct execution security features."""

    def test_command_usage_when_direct_execution_disabled(self):
        """Test that _check_command_usage returns empty when direct execution is disabled."""
        validator = SecurityValidator(allow_direct_execution=False)

        # Even though code has subprocess, it's blocked earlier
        code = "subprocess.run(['ls', '-la'])"
        violations = validator._check_command_usage(code)

        # Should return empty because direct execution is not enabled
        assert violations == []

    def test_command_usage_with_allowed_commands(self):
        """Test command usage validation with allowed commands."""
        validator = SecurityValidator(
            allow_direct_execution=True, allowed_commands=["grep", "cat", "ls"]
        )

        # Allowed command
        code = "subprocess.run(['ls', '-la'])"
        violations = validator._check_command_usage(code)
        assert violations == []

        # Unauthorized command
        code = "subprocess.run(['rm', '-rf', '/'])"
        violations = validator._check_command_usage(code)
        assert len(violations) > 0
        assert any("rm" in v for v in violations)

    def test_command_usage_no_whitelist(self):
        """Test command usage when no whitelist is provided."""
        validator = SecurityValidator(allow_direct_execution=True, allowed_commands=None)

        code = "subprocess.run(['rm', '-rf', '/'])"
        violations = validator._check_command_usage(code)

        # No whitelist, so all commands allowed (risky but user's choice)
        assert violations == []

    def test_path_access_when_direct_execution_disabled(self):
        """Test that _check_path_access returns empty when direct execution is disabled."""
        validator = SecurityValidator(allow_direct_execution=False)

        code = "open('/etc/passwd', 'r')"
        violations = validator._check_path_access(code)

        # Should return empty because direct execution is not enabled
        assert violations == []

    def test_path_access_with_allowed_paths(self):
        """Test path access validation with allowed paths."""
        validator = SecurityValidator(
            allow_direct_execution=True, allowed_paths={"/workspace": "r", "/sandbox": "rw"}
        )

        # Allowed path
        code = "open('/workspace/file.txt', 'r')"
        violations = validator._check_path_access(code)
        assert violations == []

        # Unauthorized path
        code = "open('/etc/passwd', 'r')"
        violations = validator._check_path_access(code)
        assert len(violations) > 0
        assert any("/etc/passwd" in v for v in violations)

    def test_path_access_no_restrictions(self):
        """Test path access when no restrictions are provided."""
        validator = SecurityValidator(allow_direct_execution=True, allowed_paths=None)

        code = "open('/etc/passwd', 'r')"
        violations = validator._check_path_access(code)

        # No restrictions, so all paths allowed (risky but user's choice)
        assert violations == []

    def test_is_path_allowed(self):
        """Test path checking logic."""
        validator = SecurityValidator(
            allow_direct_execution=True, allowed_paths={"/workspace": "r", "/sandbox": "rw"}
        )

        # Allowed paths
        assert validator._is_path_allowed("/workspace/file.txt") is True
        assert validator._is_path_allowed("/sandbox/output.txt") is True

        # Disallowed paths
        assert validator._is_path_allowed("/etc/passwd") is False
        assert validator._is_path_allowed("/home/user/secret.txt") is False

    def test_is_path_allowed_with_exception(self):
        """Test path checking with invalid path that raises exception."""
        from pathlib import Path
        from unittest.mock import patch

        validator = SecurityValidator(
            allow_direct_execution=True, allowed_paths={"/workspace": "r"}
        )

        # Mock Path.resolve() to raise an exception
        with patch.object(Path, "resolve", side_effect=OSError("Path resolution failed")):
            result = validator._is_path_allowed("/workspace/test.txt")

        # Should return False when exception occurs
        assert result is False


class TestSecurityValidatorIntegration:
    """Test complete validation flows."""

    def test_validate_with_context_injection(self):
        """Test validation of code with context usage (should be safe)."""
        validator = SecurityValidator()

        code = """
result = context.get('user_id', 'default')
tools['weather'].run(location='NYC')
"""
        result = validator.validate(code)

        assert result.is_safe is True

    def test_validate_with_multiple_violations(self):
        """Test code with multiple security issues."""
        validator = SecurityValidator()

        code = """
import subprocess
eval('dangerous')
while True: pass
"""
        result = validator.validate(code)

        assert result.is_safe is False
        # Should catch at least one violation (they're checked in order)
        assert len(result.violations) > 0

    def test_validate_realistic_safe_code(self):
        """Test validation of realistic safe code."""
        validator = SecurityValidator()

        code = """
import json

def get_weather(location):
    # Use tool to fetch weather
    result = tools['weather'].run(location=location)
    return json.loads(result)

# Execute
weather_data = get_weather(context.get('location', 'NYC'))
result = f"Weather: {weather_data}"
"""
        result = validator.validate(code)

        # Should pass - this is safe code using tools
        assert result.is_safe is True

    def test_validate_with_direct_execution_full_flow(self):
        """Test full validation flow with direct execution enabled."""
        validator = SecurityValidator(
            allow_direct_execution=True,
            allowed_commands=["grep", "cat", "ls"],
            allowed_paths={"/workspace": "r"},
        )

        # Safe code with allowed command and path
        safe_code = """
import subprocess
subprocess.run(['cat', '/workspace/data.txt'])
"""
        result = validator.validate(safe_code)
        assert result.is_safe is True

        # Unsafe code with unauthorized command
        unsafe_code = """
import subprocess
subprocess.run(['rm', '-rf', '/'])
"""
        result = validator.validate(unsafe_code)
        assert result.is_safe is False
        assert any("unauthorized_command" in v for v in result.violations)

        # Unsafe code with unauthorized path
        unsafe_code = """
with open('/etc/passwd', 'r') as f:
    data = f.read()
"""
        result = validator.validate(unsafe_code)
        assert result.is_safe is False
        assert any("unauthorized_path" in v for v in result.violations)
