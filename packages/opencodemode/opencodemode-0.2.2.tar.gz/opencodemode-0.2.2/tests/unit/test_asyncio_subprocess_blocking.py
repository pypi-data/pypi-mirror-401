"""
Unit tests to verify asyncio.subprocess is blocked while asyncio is allowed.
"""

from codemode.executor.security import SecurityValidator


class TestAsyncioSubprocessBlocking:
    """Test suite for asyncio.subprocess blocking."""

    def test_import_asyncio_allowed(self):
        """Test that plain 'import asyncio' is allowed."""
        validator = SecurityValidator()
        violations = validator._check_imports("import asyncio")
        assert violations == [], f"Plain 'import asyncio' should be allowed, got {violations}"

    def test_import_asyncio_subprocess_blocked(self):
        """Test that 'import asyncio.subprocess' is blocked."""
        validator = SecurityValidator()
        violations = validator._check_imports("import asyncio.subprocess")
        assert (
            "asyncio.subprocess" in violations
        ), f"'import asyncio.subprocess' should be blocked, got {violations}"

    def test_from_asyncio_import_subprocess_blocked(self):
        """Test that 'from asyncio import subprocess' is blocked."""
        validator = SecurityValidator()
        violations = validator._check_imports("from asyncio import subprocess")
        assert (
            "asyncio.subprocess" in violations
        ), f"'from asyncio import subprocess' should be blocked, got {violations}"

    def test_from_asyncio_subprocess_import_blocked(self):
        """Test that 'from asyncio.subprocess import PIPE' is blocked."""
        validator = SecurityValidator()
        violations = validator._check_imports("from asyncio.subprocess import PIPE")
        assert (
            "asyncio.subprocess" in violations
        ), f"'from asyncio.subprocess import PIPE' should be blocked, got {violations}"

    def test_from_asyncio_import_others_allowed(self):
        """Test that 'from asyncio import sleep, gather' is allowed."""
        validator = SecurityValidator()
        violations = validator._check_imports("from asyncio import sleep, gather, create_task")
        assert (
            violations == []
        ), f"'from asyncio import sleep, gather' should be allowed, got {violations}"

    def test_asyncio_with_code_allowed(self):
        """Test that asyncio with actual async code is allowed."""
        validator = SecurityValidator()
        code = """
import asyncio

async def main():
    await asyncio.sleep(1)
    await asyncio.gather(task1(), task2())

asyncio.run(main())
"""
        violations = validator._check_imports(code)
        assert violations == [], f"Async code with asyncio should be allowed, got {violations}"

    def test_subprocess_module_still_blocked(self):
        """Test that regular subprocess module is still blocked."""
        validator = SecurityValidator()
        violations = validator._check_imports("import subprocess")
        assert (
            "subprocess" in violations
        ), f"'import subprocess' should be blocked, got {violations}"

    def test_threading_still_blocked(self):
        """Test that threading module is still blocked."""
        validator = SecurityValidator()
        violations = validator._check_imports("import threading")
        assert "threading" in violations, f"'import threading' should be blocked, got {violations}"
