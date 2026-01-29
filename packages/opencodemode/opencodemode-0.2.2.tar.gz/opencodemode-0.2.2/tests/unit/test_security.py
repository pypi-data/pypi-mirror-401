"""
Unit tests for SecurityValidator.
"""

import pytest

from codemode.executor.security import SecurityValidationResult, SecurityValidator


class TestSecurityValidator:
    """Test SecurityValidator class."""

    def test_init(self):
        """Test validator initialization."""
        validator = SecurityValidator()

        assert validator.max_code_length == SecurityValidator.MAX_CODE_LENGTH
        assert len(validator.blocked_patterns) > 0
        assert len(validator.blocked_imports) > 0

    def test_init_custom_max_length(self):
        """Test validator with custom max length."""
        validator = SecurityValidator(max_code_length=5000)

        assert validator.max_code_length == 5000

    def test_init_additional_patterns(self):
        """Test validator with additional blocked patterns."""
        validator = SecurityValidator(additional_blocked_patterns=["dangerous_func"])

        assert "dangerous_func" in validator.blocked_patterns

    def test_validate_safe_code(self):
        """Test validation of safe code."""
        validator = SecurityValidator()

        code = """
result = 2 + 2
print(result)
"""

        result = validator.validate(code)

        assert result.is_safe
        assert len(result.violations) == 0

    def test_validate_max_length_exceeded(self):
        """Test validation of code exceeding max length."""
        validator = SecurityValidator(max_code_length=100)

        code = "x = 1\n" * 1000  # Very long code

        result = validator.validate(code)

        assert not result.is_safe
        assert "max_length_exceeded" in result.violations
        assert "maximum length" in result.reason

    def test_validate_blocked_import(self):
        """Test validation of blocked imports."""
        validator = SecurityValidator()

        test_cases = [
            "import subprocess",
            "from subprocess import run",
            "import socket",
            "import os.system",  # Explicitly blocked submodule
            "from os import system",  # Explicitly blocked submodule
        ]

        for code in test_cases:
            result = validator.validate(code)
            assert not result.is_safe, f"Should block: {code}"
            assert len(result.violations) > 0

    def test_validate_allowed_parent_modules(self):
        """Test that parent modules are allowed when only submodules are blocked."""
        validator = SecurityValidator()

        # os itself is not blocked, only os.system, os.popen, etc.
        test_cases = [
            "import os",
            "from os import path",
            "from os import environ",
            "import asyncio",  # Not blocked, only asyncio.subprocess is blocked
            "from asyncio import sleep, gather",
        ]

        for code in test_cases:
            result = validator.validate(code)
            assert result.is_safe, f"Should allow: {code}, but got violations: {result.violations}"

    def test_validate_blocked_pattern_eval(self):
        """Test validation of eval pattern."""
        validator = SecurityValidator()

        code = "result = eval('2 + 2')"

        result = validator.validate(code)

        assert not result.is_safe
        assert "eval(" in result.violations
        assert "eval(" in result.reason

    def test_validate_blocked_pattern_exec(self):
        """Test validation of exec pattern."""
        validator = SecurityValidator()

        code = "exec('print(1)')"

        result = validator.validate(code)

        assert not result.is_safe
        assert "exec(" in result.violations

    def test_validate_blocked_pattern_import(self):
        """Test validation of __import__ pattern."""
        validator = SecurityValidator()

        code = "__import__('os').system('ls')"

        result = validator.validate(code)

        assert not result.is_safe
        assert "__import__" in result.violations

    def test_validate_blocked_pattern_open(self):
        """Test validation of open pattern."""
        validator = SecurityValidator()

        code = "f = open('/etc/passwd', 'r')"

        result = validator.validate(code)

        assert not result.is_safe
        assert "open(" in result.violations

    def test_validate_suspicious_infinite_loop(self):
        """Test validation of infinite loop."""
        validator = SecurityValidator()

        code = """
while True:
    pass
"""

        result = validator.validate(code)

        assert not result.is_safe
        assert "infinite_loop" in result.violations

    def test_validate_suspicious_unicode(self):
        """Test validation of unicode encoding tricks."""
        validator = SecurityValidator()

        code = "x = '\\x41\\x42\\x43'"

        result = validator.validate(code)

        assert not result.is_safe
        assert "unicode_encoding" in result.violations

    def test_validate_safe_requests_usage(self):
        """Test that requests import is allowed (network blocked at container level)."""
        validator = SecurityValidator()

        # requests import is allowed since network isolation is handled
        # at the container level (no-network mode in Docker)
        code = "import requests"

        result = validator.validate(code)

        # requests is not in BLOCKED_IMPORTS - network isolation via Docker
        assert result.is_safe

    def test_validate_multiple_violations(self):
        """Test code with multiple violations."""
        validator = SecurityValidator()

        code = """
import subprocess
eval('2 + 2')
exec('print(1)')
"""

        result = validator.validate(code)

        assert not result.is_safe
        # Should have multiple violations
        assert len(result.violations) >= 2

    def test_repr(self):
        """Test string representation."""
        validator = SecurityValidator()

        repr_str = repr(validator)

        assert "SecurityValidator" in repr_str
        assert "max_length" in repr_str


class TestSecurityValidationResult:
    """Test SecurityValidationResult dataclass."""

    def test_safe_result(self):
        """Test creating safe result."""
        result = SecurityValidationResult.safe()

        assert result.is_safe
        assert len(result.violations) == 0
        assert result.reason == ""

    def test_unsafe_result(self):
        """Test creating unsafe result."""
        result = SecurityValidationResult.unsafe(violations=["eval"], reason="eval is dangerous")

        assert not result.is_safe
        assert "eval" in result.violations
        assert result.reason == "eval is dangerous"


class TestSecurityValidatorEnhanced:
    """Test enhanced SecurityValidator with hybrid execution support."""

    def test_init_with_direct_execution(self):
        """Test validator initialization with direct execution."""
        validator = SecurityValidator(
            allow_direct_execution=True,
            allowed_commands=["grep", "cat"],
            allowed_paths={"/workspace": "r", "/sandbox": "rw"},
        )

        assert validator.allow_direct_execution is True
        assert "grep" in validator.allowed_commands
        assert "/workspace" in validator.allowed_paths

    def test_direct_execution_allows_subprocess(self):
        """Test that subprocess is allowed when direct execution is enabled."""
        validator = SecurityValidator(allow_direct_execution=True)

        code = "import subprocess"
        result = validator.validate(code)

        # Should be safe when direct execution is enabled
        assert result.is_safe

    def test_direct_execution_allows_open(self):
        """Test that open() is allowed when direct execution is enabled."""
        validator = SecurityValidator(
            allow_direct_execution=True, allowed_paths={"/workspace": "r"}
        )

        code = "f = open('/workspace/file.txt', 'r')"
        result = validator.validate(code)

        # Should be safe when direct execution is enabled with path validation
        assert result.is_safe

    def test_command_whitelist_blocks_unauthorized(self):
        """Test that unauthorized commands are blocked."""
        validator = SecurityValidator(allow_direct_execution=True, allowed_commands=["grep", "cat"])

        code = "subprocess.run(['rm', '-rf', '/'])"
        result = validator.validate(code)

        assert not result.is_safe
        assert any("unauthorized_command" in v for v in result.violations)

    def test_command_whitelist_allows_authorized(self):
        """Test that authorized commands are allowed."""
        validator = SecurityValidator(allow_direct_execution=True, allowed_commands=["grep", "cat"])

        code = "subprocess.run(['grep', 'ERROR', '/workspace/app.log'])"
        result = validator.validate(code)

        # Should pass command check
        assert result.is_safe

    def test_path_validation_blocks_unauthorized(self):
        """Test that unauthorized paths are blocked."""
        validator = SecurityValidator(
            allow_direct_execution=True, allowed_paths={"/workspace": "r", "/sandbox": "rw"}
        )

        code = "open('/etc/passwd', 'r')"
        result = validator.validate(code)

        assert not result.is_safe
        assert any("unauthorized_path" in v for v in result.violations)

    def test_path_validation_allows_authorized(self):
        """Test that authorized paths are allowed."""
        validator = SecurityValidator(
            allow_direct_execution=True, allowed_paths={"/workspace": "r"}
        )

        code = "open('/workspace/data.txt', 'r')"
        result = validator.validate(code)

        assert result.is_safe

    def test_is_path_allowed(self):
        """Test path checking logic."""
        validator = SecurityValidator(
            allow_direct_execution=True, allowed_paths={"/workspace": "r", "/sandbox": "rw"}
        )

        assert validator._is_path_allowed("/workspace/file.txt")
        assert validator._is_path_allowed("/sandbox/output.txt")
        assert not validator._is_path_allowed("/etc/passwd")
        assert not validator._is_path_allowed("/tmp/hack.sh")

    def test_no_direct_execution_blocks_subprocess(self):
        """Test that subprocess is blocked when direct execution is disabled."""
        validator = SecurityValidator(allow_direct_execution=False)

        code = "import subprocess"
        result = validator.validate(code)

        assert not result.is_safe
        assert len(result.violations) > 0

    def test_hybrid_execution_example(self):
        """Test realistic hybrid execution code."""
        validator = SecurityValidator(
            allow_direct_execution=True,
            allowed_commands=["grep", "cat", "wc"],
            allowed_paths={"/workspace": "r", "/sandbox": "rw"},
        )

        code = """
import subprocess

# Direct file operation
with open('/workspace/app.log', 'r') as f:
    logs = f.read()

# Direct command
result = subprocess.run(['grep', 'ERROR', '/workspace/app.log'],
                       capture_output=True, text=True)

# Write to sandbox
with open('/sandbox/analysis.txt', 'w') as f:
    f.write(result.stdout)

# Proxied tool call
alert = tools['alerting'].run(message='Found errors')
"""

        result = validator.validate(code)

        # Should be safe with proper configuration
        assert result.is_safe


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
