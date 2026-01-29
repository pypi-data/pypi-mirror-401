"""
Code runner for safe execution with gRPC tool proxies.

This module provides the CodeRunner class for executing Python code in a sandboxed
environment with gRPC-based tool proxies, along with helper functions for error
classification and traceback parsing.
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
import sys
from typing import Any

from codemode.executor.models import ExecutionError, ExecutionResult
from codemode.executor.security import SecurityValidator

logger = logging.getLogger(__name__)


# =============================================================================
# Error Handling Helpers
# =============================================================================


def _parse_traceback(stderr: str, limit: int = 5) -> str | None:
    """
    Extract last N frames from Python traceback in stderr.

    Parses Python traceback format and returns a limited number of frames
    to avoid exposing too much internal implementation detail.

    Args:
        stderr: Standard error output containing potential traceback
        limit: Maximum number of frames to include (0 to disable)

    Returns:
        Limited traceback string or None if no traceback found

    Example:
        >>> stderr = '''Traceback (most recent call last):
        ...   File "test.py", line 10, in <module>
        ...     result = process_data()
        ...   File "test.py", line 5, in process_data
        ...     return int("not a number")
        ... ValueError: invalid literal for int()'''
        >>> tb = _parse_traceback(stderr, limit=2)
        >>> print(tb)
        Traceback (most recent call last):
          File "test.py", line 5, in process_data
            return int("not a number")
        ValueError: invalid literal for int()
    """
    if limit == 0 or not stderr:
        return None

    lines = stderr.split("\n")

    # Find traceback start
    tb_start = None
    for i, line in enumerate(lines):
        if line.startswith("Traceback (most recent call last):"):
            tb_start = i
            break

    if tb_start is None:
        return None

    # Extract lines from traceback start to end
    tb_lines = lines[tb_start:]

    # Parse frames (each frame typically has 2 lines: File... and code)
    frames: list[tuple[str, str]] = []
    i = 1  # Skip "Traceback (most recent call last):" line
    while i < len(tb_lines):
        line = tb_lines[i]
        stripped = line.strip()

        # Check if this is a "File ..." line (frame start)
        if stripped.startswith("File "):
            file_line = line
            code_line = ""

            # Next line might be the code (if it exists and is indented)
            if i + 1 < len(tb_lines):
                next_line = tb_lines[i + 1]
                # Code lines are indented but don't start with "File " or error type
                if next_line.startswith("    ") and not next_line.strip().startswith("File "):
                    # Check it's not the error line (which typically has a colon like "ValueError:")
                    if not re.match(r"^\s*\w+Error:", next_line) and not re.match(
                        r"^\s*\w+Exception:", next_line
                    ):
                        code_line = next_line
                        i += 1

            frames.append((file_line, code_line))
        elif stripped and not stripped.startswith("File "):
            # This might be the final error line - stop parsing frames
            break

        i += 1

    if not frames:
        return None

    # Take last N frames
    limited_frames = frames[-limit:] if len(frames) > limit else frames

    # Reconstruct traceback
    result_lines = ["Traceback (most recent call last):"]
    for file_line, code_line in limited_frames:
        result_lines.append(file_line)
        if code_line.strip():
            result_lines.append(code_line)

    # Add the final error line (last non-empty line in tb_lines)
    for line in reversed(tb_lines):
        stripped = line.strip()
        if stripped:
            # Check if this looks like an error line
            if re.match(r"^\w+(Error|Exception):", stripped) or re.match(
                r"^\w+(Error|Exception)$", stripped
            ):
                result_lines.append(stripped)
            break

    return "\n".join(result_lines)


def _classify_error(stderr: str, return_code: int) -> str:
    """
    Classify error type from stderr and return code.

    Analyzes the stderr output and return code to determine the category
    of error that occurred during code execution.

    Args:
        stderr: Standard error output from execution
        return_code: Process return code

    Returns:
        Error classification string, one of:
        - "SecurityViolation": Security policy was violated
        - "Timeout": Execution timed out
        - "SyntaxError": Python syntax error
        - "ImportError": Module import failed
        - "TypeError": Type mismatch error
        - "ValueError": Invalid value error
        - "KeyError": Dictionary key not found
        - "RuntimeError": General runtime error
        - "Unknown": Could not classify the error

    Example:
        >>> stderr = "TypeError: unsupported operand type(s)"
        >>> _classify_error(stderr, 1)
        'TypeError'
        >>> _classify_error("Security violation: import os forbidden", 1)
        'SecurityViolation'
    """
    if not stderr:
        if return_code != 0:
            return "RuntimeError"
        return "Unknown"

    stderr_lower = stderr.lower()

    # Check for security violations first (case-insensitive)
    if "security violation" in stderr_lower:
        return "SecurityViolation"

    # Check for timeout
    if "timeout" in stderr_lower:
        return "Timeout"

    # Check for specific Python exception types (case-sensitive)
    error_types = [
        "SyntaxError",
        "ImportError",
        "ModuleNotFoundError",
        "TypeError",
        "ValueError",
        "KeyError",
        "AttributeError",
        "NameError",
        "IndexError",
        "ZeroDivisionError",
    ]

    for error_type in error_types:
        if error_type in stderr:
            # Map ModuleNotFoundError to ImportError for consistency
            if error_type == "ModuleNotFoundError":
                return "ImportError"
            return error_type

    # Generic runtime error if process failed
    if return_code != 0:
        return "RuntimeError"

    return "Unknown"


class CodeExecutionError(Exception):
    """Raised when code execution fails."""


class CodeRunner:
    """Executes Python code with gRPC tool proxies in a safe environment."""

    def __init__(
        self,
        main_app_target: str | None = None,
        api_key: str | None = None,
        security_validator: SecurityValidator | None = None,
        allow_direct_execution: bool = False,
    ) -> None:
        target = main_app_target or "localhost:50051"
        # Strip both http:// and https:// prefixes for gRPC target normalization
        if target.startswith("https://"):
            target = target[len("https://") :]
        elif target.startswith("http://"):
            target = target[len("http://") :]
        self.main_app_target = target.rstrip("/")
        self.api_key = api_key
        self.allow_direct_execution = allow_direct_execution
        self.security_validator = security_validator or SecurityValidator(
            allow_direct_execution=allow_direct_execution
        )

        logger.info(
            "Initialized CodeRunner for %s (direct_execution=%s)",
            self.main_app_target,
            allow_direct_execution,
        )

    async def run(
        self,
        code: str,
        available_tools: list[str],
        config: dict[str, Any],
        timeout: int = 30,
        context: dict[str, Any] | None = None,
        tool_metadata: dict[str, dict] | None = None,
        correlation_id: str | None = None,
    ) -> ExecutionResult:
        """
        Execute Python code with tool proxies in a sandboxed environment.

        Args:
            code: Python code to execute
            available_tools: List of tool names to make available
            config: Configuration dictionary
            timeout: Execution timeout in seconds
            context: Optional runtime context for tools
            tool_metadata: Optional metadata about tools (async, has_context)
            correlation_id: Optional correlation ID for request tracing

        Returns:
            ExecutionResult with success status and output
        """
        log_extra = {"correlation_id": correlation_id} if correlation_id else {}
        logger.debug(
            "Running code (%s chars) with %s tools, timeout=%ss%s",
            len(code),
            len(available_tools),
            timeout,
            ", with context" if context else "",
            extra=log_extra,
        )

        if tool_metadata is None:
            raise ValueError("tool_metadata is required - call ListTools first")

        validation_result = self.security_validator.validate(code)
        if not validation_result.is_safe:
            logger.warning(
                "Security validation failed: %s", validation_result.reason, extra=log_extra
            )
            return ExecutionResult.error_result(
                error=f"Security violation: {validation_result.reason}",
                error_details=ExecutionError(
                    error_type="SecurityViolation",
                    message=validation_result.reason or "Security policy violated",
                    traceback=None,
                ),
                correlation_id=correlation_id,
            )

        wrapped_code = self._wrap_code_with_proxies(
            user_code=code,
            available_tools=available_tools,
            tool_metadata=tool_metadata,
            config=config,
            context=context,
        )

        try:
            result = await self._execute_code(
                wrapped_code=wrapped_code,
                timeout=timeout,
                correlation_id=correlation_id,
            )
            return result
        except Exception as e:  # Broad catch OK: catch all execution errors for safe fallback
            logger.error("Code execution failed: %s", e, exc_info=True, extra=log_extra)
            return ExecutionResult.error_result(
                error=f"Execution failed: {str(e)}",
                error_details=ExecutionError(
                    error_type="RuntimeError",
                    message=str(e),
                    traceback=None,
                ),
                correlation_id=correlation_id,
            )

    def _wrap_code_with_proxies(
        self,
        user_code: str,
        available_tools: list[str],
        tool_metadata: dict[str, dict],
        config: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> str:
        """Wrap user code with matched tool proxy infrastructure (gRPC -> main app)."""
        config_json = json.dumps(config)
        context_json = json.dumps(context) if context else "None"

        imports_section = """
import grpc
import grpc.aio
import json
import asyncio
from google.protobuf import struct_pb2
from google.protobuf.json_format import MessageToDict
from codemode.protos import codemode_pb2, codemode_pb2_grpc
"""
        if self.allow_direct_execution:
            imports_section += """
import subprocess
import os
from pathlib import Path
"""

        helpers = """
def _dict_to_struct(data):
    struct = struct_pb2.Struct()
    if data:
        struct.update(data)
    return struct

def _struct_to_python(struct_msg):
    if not struct_msg:
        return None
    return MessageToDict(struct_msg, preserving_proto_field_name=True)

def _get_grpc_channel_credentials():
    '''Load TLS credentials from environment variables.'''
    import os
    tls_enabled = os.getenv("CODEMODE_GRPC_TLS_ENABLED", "false").lower() == "true"
    if not tls_enabled:
        return None

    mode = os.getenv("CODEMODE_GRPC_TLS_MODE", "system")
    if mode == "custom":
        ca_file = os.getenv("CODEMODE_GRPC_TLS_CA_FILE")
        if ca_file:
            with open(ca_file, 'rb') as f:
                ca_cert = f.read()
            # Optional: client cert for mTLS
            client_cert_file = os.getenv("CODEMODE_GRPC_TLS_CLIENT_CERT_FILE")
            client_key_file = os.getenv("CODEMODE_GRPC_TLS_CLIENT_KEY_FILE")
            if client_cert_file and client_key_file:
                with open(client_cert_file, 'rb') as f:
                    client_cert = f.read()
                with open(client_key_file, 'rb') as f:
                    client_key = f.read()
                return grpc.ssl_channel_credentials(ca_cert, client_key, client_cert)
            return grpc.ssl_channel_credentials(ca_cert)

    # System certificates
    return grpc.ssl_channel_credentials()
"""

        sync_proxy_class = """
class SyncToolProxy:
    '''Synchronous tool proxy - blocks until result.'''

    def __init__(self, tool_name, target, api_key, context=None):
        self.tool_name = tool_name
        self.target = target
        self.api_key = api_key
        self.context = context

    def run(self, **kwargs):
        metadata = []
        if self.api_key:
            metadata.append(("authorization", f"Bearer {self.api_key}"))

        # TLS support
        credentials = _get_grpc_channel_credentials()
        if credentials:
            channel = grpc.secure_channel(self.target, credentials)
        else:
            channel = grpc.insecure_channel(self.target)

        try:
            stub = codemode_pb2_grpc.ToolServiceStub(channel)
            request = codemode_pb2.ToolCallRequest(
                tool_name=self.tool_name,
                arguments=_dict_to_struct(kwargs),
                context=_dict_to_struct(self.context) if self.context else None,
            )
            response = stub.CallTool(request, timeout=30, metadata=metadata)
            if response.success:
                return _struct_to_python(response.result)
            raise RuntimeError(response.error or f"Tool {self.tool_name} failed")
        finally:
            channel.close()

    def run_with_context(self, context, **kwargs):
        old_context = self.context
        self.context = context
        try:
            return self.run(**kwargs)
        finally:
            self.context = old_context
"""

        async_proxy_class = """
class AsyncToolProxy:
    '''Asynchronous tool proxy - returns coroutine.'''

    def __init__(self, tool_name, target, api_key, context=None):
        self.tool_name = tool_name
        self.target = target
        self.api_key = api_key
        self.context = context

    async def run(self, **kwargs):
        metadata = []
        if self.api_key:
            metadata.append(("authorization", f"Bearer {self.api_key}"))

        # TLS support
        credentials = _get_grpc_channel_credentials()
        if credentials:
            channel = grpc.aio.secure_channel(self.target, credentials)
        else:
            channel = grpc.aio.insecure_channel(self.target)

        async with channel:
            stub = codemode_pb2_grpc.ToolServiceStub(channel)
            request = codemode_pb2.ToolCallRequest(
                tool_name=self.tool_name,
                arguments=_dict_to_struct(kwargs),
                context=_dict_to_struct(self.context) if self.context else None,
            )
            response = await stub.CallTool(request, timeout=30, metadata=metadata)
            if response.success:
                return _struct_to_python(response.result)
            raise RuntimeError(response.error or f"Tool {self.tool_name} failed")

    async def run_with_context(self, context, **kwargs):
        old_context = self.context
        self.context = context
        try:
            return await self.run(**kwargs)
        finally:
            self.context = old_context
"""

        # Generate tool initialization based on metadata (matched to actual tool signatures)
        tool_init_lines = []
        for tool_name in available_tools:
            meta = tool_metadata.get(tool_name)
            if meta is None:
                raise ValueError(
                    f"Tool '{tool_name}' not found in metadata. "
                    f"Available tools: {list(tool_metadata.keys())}"
                )
            is_async = meta.get("is_async", False)
            proxy_class = "AsyncToolProxy" if is_async else "SyncToolProxy"
            tool_init_lines.append(
                f"    '{tool_name}': {proxy_class}('{tool_name}', GRPC_TARGET, API_KEY, CONTEXT),"
            )

        tools_init = f"""
# Initialize tool proxies (matched to actual tool signatures)
GRPC_TARGET = "{self.main_app_target}"
API_KEY = {repr(self.api_key)}  # Use repr() to properly serialize None
CONTEXT = {context_json}

tools = {{
{chr(10).join(tool_init_lines)}
}}

# Make context available to user code
context = CONTEXT
"""

        config_init = f"""
# Configuration
config = {config_json}
"""

        wrapped_code = f"""
{imports_section}
{helpers}
{sync_proxy_class}
{async_proxy_class}
{tools_init}
{config_init}

# User code starts here
{user_code}

# Extract result
if 'result' in locals():
    import json
    print("__CODEMODE_RESULT__:" + json.dumps({{'result': str(result)}}))
else:
    print(
        "__CODEMODE_RESULT__:"
        + json.dumps({{'result': None, 'warning': 'No result variable defined'}})
    )
"""

        return wrapped_code

    async def _execute_code(
        self,
        wrapped_code: str,
        timeout: int,
        correlation_id: str | None = None,
    ) -> ExecutionResult:
        """
        Execute wrapped code in a subprocess.

        Args:
            wrapped_code: Python code with tool proxies injected
            timeout: Execution timeout in seconds
            correlation_id: Optional correlation ID for request tracing

        Returns:
            ExecutionResult with execution outcome and structured error details
        """
        import time

        start_time = time.perf_counter()
        log_extra = {"correlation_id": correlation_id} if correlation_id else {}

        try:
            process = await asyncio.create_subprocess_exec(
                sys.executable,
                "-u",
                "-c",
                wrapped_code,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    process.communicate(), timeout=timeout
                )

                stdout = stdout_bytes.decode("utf-8", errors="replace")
                stderr = stderr_bytes.decode("utf-8", errors="replace")
                duration_ms = (time.perf_counter() - start_time) * 1000

                result_value = self._extract_result(stdout)

                if process.returncode == 0:
                    logger.info("Code executed successfully", extra=log_extra)
                    return ExecutionResult.success_result(
                        result=result_value,
                        stdout=stdout,
                        stderr=stderr,
                        correlation_id=correlation_id,
                        duration_ms=duration_ms,
                    )

                # Execution failed - classify error and parse traceback
                error_type = _classify_error(stderr, process.returncode)
                traceback_str = _parse_traceback(stderr, limit=5)

                logger.warning(
                    "Code execution failed with code %s (%s)",
                    process.returncode,
                    error_type,
                    extra=log_extra,
                )

                return ExecutionResult.error_result(
                    error=f"Execution failed with return code {process.returncode}",
                    stdout=stdout,
                    stderr=stderr,
                    error_details=ExecutionError(
                        error_type=error_type,
                        message=self._extract_error_message(stderr) or "Unknown error",
                        traceback=traceback_str,
                    ),
                    correlation_id=correlation_id,
                    duration_ms=duration_ms,
                )

            except TimeoutError:
                process.kill()
                await process.wait()
                duration_ms = (time.perf_counter() - start_time) * 1000
                logger.warning("Code execution timeout after %ss", timeout, extra=log_extra)
                return ExecutionResult.error_result(
                    error=f"Execution timeout after {timeout} seconds",
                    error_details=ExecutionError(
                        error_type="Timeout",
                        message=f"Code execution timed out after {timeout} seconds",
                        traceback=None,
                    ),
                    correlation_id=correlation_id,
                    duration_ms=duration_ms,
                )

        except Exception as e:  # Broad catch OK: catch all subprocess errors for safe fallback
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.error("Subprocess execution error: %s", e, extra=log_extra)
            return ExecutionResult.error_result(
                error=f"Subprocess error: {str(e)}",
                error_details=ExecutionError(
                    error_type="RuntimeError",
                    message=str(e),
                    traceback=None,
                ),
                correlation_id=correlation_id,
                duration_ms=duration_ms,
            )

    def _extract_error_message(self, stderr: str) -> str | None:
        """
        Extract the error message from stderr.

        Looks for common Python error patterns like "ErrorType: message".

        Args:
            stderr: Standard error output

        Returns:
            Error message string or None if not found
        """
        if not stderr:
            return None

        # Look for the last line that matches error pattern
        for line in reversed(stderr.strip().split("\n")):
            line = line.strip()
            # Match patterns like "ValueError: invalid literal" or "TypeError: ..."
            if re.match(r"^\w+(Error|Exception):", line):
                # Return the message part after the colon
                parts = line.split(":", 1)
                if len(parts) == 2:
                    return parts[1].strip()
                return line

        return None

    def _extract_result(self, stdout: str) -> str | None:
        marker = "__CODEMODE_RESULT__:"
        for line in stdout.split("\n"):
            if marker in line:
                try:
                    json_str = line.split(marker, 1)[1]
                    result_data = json.loads(json_str)
                    return result_data.get("result")
                except (json.JSONDecodeError, IndexError) as e:
                    logger.warning("Failed to parse result: %s", e)
                    return None
        return None

    def __repr__(self) -> str:
        return f"CodeRunner(main_app={self.main_app_target})"
