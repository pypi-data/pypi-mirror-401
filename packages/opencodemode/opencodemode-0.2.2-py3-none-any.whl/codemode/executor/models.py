"""
Models for code execution in the executor.

This module defines the request/response models used by the executor
for code execution results, including structured error handling.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ExecutionError(BaseModel):
    """
    Structured error information from code execution.

    This model provides detailed error classification and traceback information
    for failed code executions, enabling better error handling and debugging.

    Attributes:
        error_type: Classification of the error (e.g., "SecurityViolation", "Timeout")
        message: Human-readable error message
        traceback: Limited traceback information (configurable frames)

    Example:
        >>> error = ExecutionError(
        ...     error_type="TypeError",
        ...     message="unsupported operand type(s) for +: 'int' and 'str'",
        ...     traceback="File '<string>', line 5, in <module>\\n    result = x + y"
        ... )
    """

    error_type: str = Field(..., description="Error classification type")
    message: str = Field(..., description="Error message")
    traceback: str | None = Field(None, description="Limited traceback (configurable frames)")


class ExecutionResult(BaseModel):
    """
    Result of code execution in the executor.

    This model is returned by the executor service after executing code,
    including success/failure status, outputs, and structured error details.

    Attributes:
        success: Whether execution succeeded
        result: Execution result (if successful)
        stdout: Standard output from execution
        stderr: Standard error from execution
        error: Error message (if failed)
        error_details: Structured error information (if failed)
        correlation_id: Request correlation ID for tracing
        duration_ms: Execution duration in milliseconds

    Example:
        >>> result = ExecutionResult(
        ...     success=True,
        ...     result="{'weather': '72°F'}",
        ...     stdout="Execution completed\\n",
        ...     stderr="",
        ...     correlation_id="cm-2x5f9k-a7b3",
        ...     duration_ms=150.5
        ... )
    """

    success: bool = Field(..., description="Whether execution succeeded")
    result: str | None = Field(None, description="Execution result")
    stdout: str = Field("", description="Standard output")
    stderr: str = Field("", description="Standard error")
    error: str | None = Field(None, description="Error message if failed")
    error_details: ExecutionError | None = Field(None, description="Structured error information")
    correlation_id: str | None = Field(None, description="Request correlation ID for tracing")
    duration_ms: float | None = Field(None, description="Execution duration in milliseconds")

    @classmethod
    def success_result(
        cls,
        result: str | None,
        stdout: str = "",
        stderr: str = "",
        correlation_id: str | None = None,
        duration_ms: float | None = None,
    ) -> ExecutionResult:
        """
        Create a successful execution result.

        Args:
            result: Execution result value
            stdout: Standard output from execution
            stderr: Standard error from execution
            correlation_id: Request correlation ID for tracing
            duration_ms: Execution duration in milliseconds

        Returns:
            ExecutionResult with success=True

        Example:
            >>> result = ExecutionResult.success_result(
            ...     result="Done",
            ...     stdout="OK\\n",
            ...     correlation_id="cm-2x5f9k-a7b3",
            ...     duration_ms=50.2
            ... )
        """
        return cls(
            success=True,
            result=result,
            stdout=stdout,
            stderr=stderr,
            correlation_id=correlation_id,
            duration_ms=duration_ms,
        )

    @classmethod
    def error_result(
        cls,
        error: str,
        stdout: str = "",
        stderr: str = "",
        error_details: ExecutionError | None = None,
        correlation_id: str | None = None,
        duration_ms: float | None = None,
    ) -> ExecutionResult:
        """
        Create an error execution result.

        Args:
            error: Error message
            stdout: Standard output before error
            stderr: Standard error from execution
            error_details: Structured error information
            correlation_id: Request correlation ID for tracing
            duration_ms: Execution duration in milliseconds

        Returns:
            ExecutionResult with success=False

        Example:
            >>> error_info = ExecutionError(
            ...     error_type="Timeout",
            ...     message="Execution timeout after 30 seconds"
            ... )
            >>> result = ExecutionResult.error_result(
            ...     error="Timeout",
            ...     stderr="...",
            ...     error_details=error_info,
            ...     correlation_id="cm-2x5f9k-a7b3",
            ...     duration_ms=30000.0
            ... )
        """
        return cls(
            success=False,
            error=error,
            stdout=stdout,
            stderr=stderr,
            error_details=error_details,
            correlation_id=correlation_id,
            duration_ms=duration_ms,
        )

    def __repr__(self) -> str:
        """Return string representation."""
        if self.success:
            return f"ExecutionResult(success=True, correlation_id={self.correlation_id})"
        return f"ExecutionResult(success=False, error={self.error}, correlation_id={self.correlation_id})"
