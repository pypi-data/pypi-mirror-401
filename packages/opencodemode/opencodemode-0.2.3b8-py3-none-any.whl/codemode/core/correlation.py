"""Correlation ID generation and management.

Correlation IDs are used to trace requests across the main app and executor.
They provide a way to correlate logs and debugging information between
distributed services.

Format: {prefix}-{base36_timestamp}-{random}
Example: 'cm-2x5f9k-a7b3' (~15 chars total)
"""

from __future__ import annotations

import random
import string
import time


def _to_base36(num: int) -> str:
    """Convert an integer to a base36 string representation.

    Base36 uses digits 0-9 and lowercase letters a-z, providing a compact
    alphanumeric representation of numbers.

    Args:
        num: Non-negative integer to convert.

    Returns:
        Base36 encoded string representation.

    Example:
        >>> _to_base36(0)
        '0'
        >>> _to_base36(35)
        'z'
        >>> _to_base36(36)
        '10'
        >>> _to_base36(1234567890)
        'kf12oi'
    """
    chars = string.digits + string.ascii_lowercase
    if num == 0:
        return "0"
    result: list[str] = []
    while num:
        result.append(chars[num % 36])
        num //= 36
    return "".join(reversed(result))


def generate_correlation_id(prefix: str = "cm") -> str:
    """Generate a unique correlation ID for request tracing.

    Creates a compact, unique identifier suitable for correlating logs and
    requests across distributed services. The ID combines a configurable
    prefix, a base36-encoded timestamp, and random characters.

    Format: {prefix}-{base36_timestamp}-{random}
    - prefix: Configurable string, default "cm" (codemode)
    - timestamp: Base36 encoded milliseconds (last 6 chars for compactness)
    - random: 4 random alphanumeric characters for uniqueness

    Args:
        prefix: ID prefix string. Defaults to "cm".

    Returns:
        Correlation ID string (~15 chars total with default prefix).

    Example:
        >>> generate_correlation_id()
        'cm-2x5f9k-a7b3'
        >>> generate_correlation_id(prefix="req")
        'req-2x5f9k-c8d2'
    """
    # Base36 encode current time in milliseconds
    timestamp = int(time.time() * 1000)
    ts_b36 = _to_base36(timestamp)[-6:]  # Last 6 chars for compactness

    # Random suffix for uniqueness
    chars = string.ascii_lowercase + string.digits
    suffix = "".join(random.choices(chars, k=4))

    return f"{prefix}-{ts_b36}-{suffix}"
