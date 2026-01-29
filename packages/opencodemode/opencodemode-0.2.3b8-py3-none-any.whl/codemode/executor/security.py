"""
Security validation for code execution.

This module provides security validation to block dangerous code patterns
before execution in the isolated executor container.
"""

import logging
import re
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class SecurityValidationResult:
    """
    Result of security validation.

    Attributes:
        is_safe: Whether the code is safe to execute
        violations: List of security violations found
        reason: Human-readable reason if unsafe

    Example:
        >>> result = SecurityValidationResult(
        ...     is_safe=False,
        ...     violations=["__import__"],
        ...     reason="Blocked pattern: __import__"
        ... )
    """

    is_safe: bool
    violations: list[str]
    reason: str = ""

    @classmethod
    def safe(cls) -> "SecurityValidationResult":
        """
        Create a result indicating code is safe.

        Returns:
            SecurityValidationResult with is_safe=True

        Example:
            >>> result = SecurityValidationResult.safe()
        """
        return cls(is_safe=True, violations=[], reason="")

    @classmethod
    def unsafe(cls, violations: list[str], reason: str) -> "SecurityValidationResult":
        """
        Create a result indicating code is unsafe.

        Args:
            violations: List of security violations
            reason: Human-readable reason

        Returns:
            SecurityValidationResult with is_safe=False

        Example:
            >>> result = SecurityValidationResult.unsafe(
            ...     violations=["eval"],
            ...     reason="Blocked pattern: eval"
            ... )
        """
        return cls(is_safe=False, violations=violations, reason=reason)


class SecurityValidator:
    """
    Validates code for security issues before execution.

    This class checks code for dangerous patterns that could compromise
    security even in an isolated environment.

    Attributes:
        BLOCKED_PATTERNS: Set of dangerous code patterns to block
        BLOCKED_IMPORTS: Set of dangerous modules to block
        MAX_CODE_LENGTH: Maximum allowed code length

    Example:
        >>> validator = SecurityValidator()
        >>> result = validator.validate("import os")
        >>> print(result.is_safe)
        False
    """

    # Dangerous patterns that should be blocked
    BLOCKED_PATTERNS: set[str] = {
        "__import__",
        "eval(",
        "exec(",
        "compile(",
        "open(",
        "file(",
        "input(",
        "raw_input(",
        "execfile(",
        "__builtins__",
        "reload(",
        "vars(",
        "dir(",
        "globals(",
        "locals(",
        "delattr(",
        "setattr(",
        "getattr(",  # Can be used to access __import__
    }

    # Dangerous imports that should be blocked
    BLOCKED_IMPORTS: set[str] = {
        "subprocess",
        "os.system",
        "os.popen",
        "os.spawn",
        "os.exec",
        "socket",
        "urllib",
        "urllib2",
        "urllib3",
        "httplib",
        "http.client",
        "ftplib",
        "telnetlib",
        "smtplib",
        "ssl",
        "ctypes",
        "multiprocessing",
        "threading",
        "asyncio.subprocess",  # Blocks process spawning, not cooperative concurrency
        "pty",
        "pwd",
        "grp",
        "resource",
        "signal",
        "sys.exit",
    }

    # Maximum code length (10KB)
    MAX_CODE_LENGTH = 10000

    def __init__(
        self,
        max_code_length: int = MAX_CODE_LENGTH,
        additional_blocked_patterns: list[str] = None,
        additional_blocked_imports: list[str] = None,
        allow_direct_execution: bool = False,
        allowed_commands: list[str] | None = None,
        allowed_paths: dict[str, str] | None = None,
    ) -> None:
        """
        Initialize security validator.

        Args:
            max_code_length: Maximum code length in characters
            additional_blocked_patterns: Additional patterns to block
            additional_blocked_imports: Additional imports to block
            allow_direct_execution: Whether to allow direct system commands
            allowed_commands: List of allowed system commands
                (e.g., ['grep', 'cat', 'ls'])
            allowed_paths: Dict of path->permission mapping
                (e.g., {'/workspace': 'r', '/sandbox': 'rw'})

        Example:
            >>> validator = SecurityValidator(
            ...     max_code_length=5000,
            ...     additional_blocked_patterns=["dangerous_func"],
            ...     allow_direct_execution=True,
            ...     allowed_commands=['grep', 'cat', 'ls'],
            ...     allowed_paths={'/workspace': 'r', '/sandbox': 'rw'}
            ... )
        """
        self.max_code_length = max_code_length
        self.allow_direct_execution = allow_direct_execution
        self.allowed_commands = set(allowed_commands) if allowed_commands else set()
        self.allowed_paths = allowed_paths or {}

        # Copy class-level sets and add custom ones
        self.blocked_patterns = self.BLOCKED_PATTERNS.copy()
        self.blocked_imports = self.BLOCKED_IMPORTS.copy()

        # If direct execution is allowed, we need to adjust blocking rules
        if self.allow_direct_execution:
            # Allow subprocess and os modules when direct execution is enabled
            self.blocked_imports = {
                imp
                for imp in self.blocked_imports
                if not imp.startswith("subprocess") and not imp.startswith("os.")
            }
            # Allow open() for file operations within allowed paths
            self.blocked_patterns = {pat for pat in self.blocked_patterns if pat not in ["open("]}

        if additional_blocked_patterns:
            self.blocked_patterns.update(additional_blocked_patterns)

        if additional_blocked_imports:
            self.blocked_imports.update(additional_blocked_imports)

        logger.debug(
            "Initialized SecurityValidator with %s blocked patterns and %s "
            "blocked imports, direct_execution=%s",
            len(self.blocked_patterns),
            len(self.blocked_imports),
            self.allow_direct_execution,
        )

    def validate(self, code: str) -> SecurityValidationResult:
        """
        Validate code for security issues.

        Performs multiple security checks:
        1. Code length check
        2. Blocked pattern check
        3. Blocked import check
        4. Suspicious pattern check

        Args:
            code: Python code to validate

        Returns:
            SecurityValidationResult indicating if code is safe

        Example:
            >>> validator = SecurityValidator()
            >>> result = validator.validate("result = 2 + 2")
            >>> print(result.is_safe)
            True

            >>> result = validator.validate("import subprocess")
            >>> print(result.is_safe)
            False
        """
        violations = []

        # Check 1: Code length
        if len(code) > self.max_code_length:
            logger.warning("Code exceeds max length: %s > %s", len(code), self.max_code_length)
            return SecurityValidationResult.unsafe(
                violations=["max_length_exceeded"],
                reason=f"Code exceeds maximum length of {self.max_code_length} characters",
            )

        # Check 2: Blocked patterns
        for pattern in self.blocked_patterns:
            if pattern in code:
                logger.warning("Blocked pattern found: %s", pattern)
                violations.append(pattern)

        if violations:
            return SecurityValidationResult.unsafe(
                violations=violations,
                reason=f"Blocked pattern(s) detected: {', '.join(violations)}",
            )

        # Check 3: Blocked imports
        import_violations = self._check_imports(code)
        if import_violations:
            logger.warning("Blocked imports found: %s", import_violations)
            return SecurityValidationResult.unsafe(
                violations=import_violations,
                reason=f"Blocked import(s) detected: {', '.join(import_violations)}",
            )

        # Check 4: Suspicious patterns
        suspicious_violations = self._check_suspicious_patterns(code)
        if suspicious_violations:
            logger.warning("Suspicious patterns found: %s", suspicious_violations)
            return SecurityValidationResult.unsafe(
                violations=suspicious_violations,
                reason=f"Suspicious pattern(s) detected: {', '.join(suspicious_violations)}",
            )

        # Check 5: Command usage (if direct execution is enabled)
        if self.allow_direct_execution:
            command_violations = self._check_command_usage(code)
            if command_violations:
                logger.warning("Unauthorized commands found: %s", command_violations)
                return SecurityValidationResult.unsafe(
                    violations=command_violations,
                    reason=f"Unauthorized command(s) detected: {', '.join(command_violations)}",
                )

            # Check 6: Path access (if direct execution is enabled)
            path_violations = self._check_path_access(code)
            if path_violations:
                logger.warning("Unauthorized path access found:%s", path_violations)
                return SecurityValidationResult.unsafe(
                    violations=path_violations,
                    reason=f"Unauthorized path access detected: {', '.join(path_violations)}",
                )

        # All checks passed
        logger.debug("Code passed security validation")
        return SecurityValidationResult.safe()

    def _check_imports(self, code: str) -> list[str]:
        """
        Check for blocked imports with proper submodule handling.

        Args:
            code: Python code

        Returns:
            List of blocked imports found

        Example:
            >>> validator = SecurityValidator()
            >>> violations = validator._check_imports("import subprocess")
            >>> print(violations)
            ['subprocess']
            >>> violations = validator._check_imports("import asyncio")
            >>> print(violations)
            []
            >>> violations = validator._check_imports("import asyncio.subprocess")
            >>> print(violations)
            ['asyncio.subprocess']
        """
        violations = []

        # Pattern 1: import X or import X.Y.Z
        import_pattern = r"import\s+([\w.]+)"
        matches = re.findall(import_pattern, code)
        for match in matches:
            for blocked in self.blocked_imports:
                # Exact match or importing a submodule of blocked
                if match == blocked or match.startswith(blocked + "."):
                    if match not in violations:
                        violations.append(match)

        # Pattern 2: from X import Y, Z (or from X.Y import Z)
        from_import_pattern = r"from\s+([\w.]+)\s+import\s+([\w\s,*]+)"
        matches = re.findall(from_import_pattern, code)
        for module, imports in matches:
            # Clean up the imports list
            import_list = [i.strip() for i in imports.replace("*", "").split(",") if i.strip()]

            # Check if module itself is blocked
            for blocked in self.blocked_imports:
                if module == blocked or module.startswith(blocked + "."):
                    # Add the blocked base module to violations for backward compat
                    if blocked not in violations:
                        violations.append(blocked)
                    # Also add the specific module path if different
                    if module != blocked and module not in violations:
                        violations.append(module)
                    break

            # Check if any import forms a blocked submodule path
            for imp in import_list:
                full_path = f"{module}.{imp}"
                for blocked in self.blocked_imports:
                    if full_path == blocked or full_path.startswith(blocked + "."):
                        # Add the top-level module for user-friendly error messages
                        top_level = module.split(".")[0]
                        if top_level not in violations:
                            violations.append(top_level)
                        # Add the specific blocked module
                        if blocked != top_level and blocked not in violations:
                            violations.append(blocked)
                        # Also add the full path if different from both
                        if (
                            full_path != blocked
                            and full_path != top_level
                            and full_path not in violations
                        ):
                            violations.append(full_path)

        return violations

    def _check_suspicious_patterns(self, code: str) -> list[str]:
        """
        Check for suspicious patterns that might indicate malicious intent.

        Args:
            code: Python code

        Returns:
            List of suspicious patterns found

        Example:
            >>> validator = SecurityValidator()
            >>> violations = validator._check_suspicious_patterns("while True: pass")
            >>> print(violations)
            ['infinite_loop']
        """
        violations = []

        # Check for infinite loops
        if re.search(r"while\s+True\s*:", code):
            violations.append("infinite_loop")

        # Check for excessive recursion attempts
        if code.count("def ") > 10:
            # Too many function definitions might indicate obfuscation
            violations.append("excessive_functions")

        # Check for unicode or encoding tricks
        if "\\x" in code or "\\u" in code:
            violations.append("unicode_encoding")

        # Check for very long strings (might be embedded payloads)
        long_string_pattern = r'["\']([^"\']{1000,})["\']'
        if re.search(long_string_pattern, code):
            violations.append("long_embedded_string")

        return violations

    def _check_command_usage(self, code: str) -> list[str]:
        """
        Check if code uses only allowed commands (when direct execution is enabled).

        Args:
            code: Python code

        Returns:
            List of unauthorized commands found

        Example:
            >>> validator = SecurityValidator(
            ...     allow_direct_execution=True,
            ...     allowed_commands=['grep', 'cat']
            ... )
            >>> violations = validator._check_command_usage("subprocess.run(['rm', '-rf', '/'])")
            >>> print(violations)
            ['rm']
        """
        if not self.allow_direct_execution:
            # If direct execution is not enabled, subprocess usage is already blocked
            return []

        if not self.allowed_commands:
            # No command whitelist, allow all (risky, but user's choice)
            return []

        violations = []

        # Look for subprocess.run, subprocess.call, subprocess.Popen patterns
        subprocess_patterns = [
            r'subprocess\.run\(\s*\[?\s*[\'"]([^\'"\]]+)[\'"]',
            r'subprocess\.call\(\s*\[?\s*[\'"]([^\'"\]]+)[\'"]',
            r'subprocess\.Popen\(\s*\[?\s*[\'"]([^\'"\]]+)[\'"]',
            r'subprocess\.check_output\(\s*\[?\s*[\'"]([^\'"\]]+)[\'"]',
        ]

        for pattern in subprocess_patterns:
            matches = re.findall(pattern, code)
            for match in matches:
                # Extract command name (first word)
                cmd = match.strip().split()[0] if match.strip() else match
                if cmd not in self.allowed_commands:
                    if cmd not in violations:
                        violations.append(f"unauthorized_command:{cmd}")

        return violations

    def _check_path_access(self, code: str) -> list[str]:
        """
        Check if code accesses only allowed paths (when direct execution is enabled).

        Args:
            code: Python code

        Returns:
            List of unauthorized path accesses found

        Example:
            >>> validator = SecurityValidator(
            ...     allow_direct_execution=True,
            ...     allowed_paths={'/workspace': 'r', '/sandbox': 'rw'}
            ... )
            >>> violations = validator._check_path_access("open('/etc/passwd', 'r')")
            >>> print(violations)
            ['unauthorized_path:/etc/passwd']
        """
        if not self.allow_direct_execution:
            # If direct execution is not enabled, open() is already blocked
            return []

        if not self.allowed_paths:
            # No path restrictions, allow all (risky, but user's choice)
            return []

        violations = []

        # Look for open() calls and file path usage
        open_patterns = [
            r'open\(\s*[\'"]([^\'"\)]+)[\'"]',  # open('path', ...)
            r'Path\(\s*[\'"]([^\'"\)]+)[\'"]',  # Path('path')
            r'with\s+open\(\s*[\'"]([^\'"\)]+)[\'"]',  # with open('path', ...)
        ]

        for pattern in open_patterns:
            matches = re.findall(pattern, code)
            for match in matches:
                path = match.strip()
                # Check if path is within allowed paths
                if not self._is_path_allowed(path):
                    if f"unauthorized_path:{path}" not in violations:
                        violations.append(f"unauthorized_path:{path}")

        return violations

    def _is_path_allowed(self, path: str) -> bool:
        """
        Check if a path is within allowed paths.

        Args:
            path: File path to check

        Returns:
            True if path is allowed, False otherwise

        Example:
            >>> validator = SecurityValidator(
            ...     allow_direct_execution=True,
            ...     allowed_paths={'/workspace': 'r', '/sandbox': 'rw'}
            ... )
            >>> validator._is_path_allowed('/workspace/file.txt')
            True
            >>> validator._is_path_allowed('/etc/passwd')
            False
        """
        try:
            # Normalize path
            normalized_path = str(Path(path).resolve())

            # Check against each allowed path
            for allowed_path in self.allowed_paths.keys():
                normalized_allowed = str(Path(allowed_path).resolve())
                if normalized_path.startswith(normalized_allowed):
                    return True

            return False
        except Exception as e:  # Broad catch OK: safe fallback for path validation
            logger.warning("Error checking path %s: %s", path, e)
            return False

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"SecurityValidator("
            f"max_length={self.max_code_length}, "
            f"patterns={len(self.blocked_patterns)}, "
            f"imports={len(self.blocked_imports)}, "
            f"direct_execution={self.allow_direct_execution})"
        )
