"""Correlation ID management for distributed tracing.

This module provides correlation ID generation and propagation for
request tracing across TraceKit operations.


Example:
    >>> from tracekit.core.correlation import with_correlation_id, get_correlation_id
    >>> @with_correlation_id()
    ... def analyze_trace(data):
    ...     corr_id = get_correlation_id()
    ...     print(f"Processing with correlation ID: {corr_id}")

References:
    - Distributed tracing best practices
    - Thread-local and async-safe context management
"""

from __future__ import annotations

import contextvars
import functools
import uuid
from collections.abc import Callable
from typing import Any, TypeVar

# Context variable for correlation ID (thread-safe and async-safe)
_correlation_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "correlation_id", default=None
)


def get_correlation_id() -> str | None:
    """Get the current correlation ID for request tracing.

    Returns the correlation ID from the current context, or None if
    no correlation context is active.

    Returns:
        Current correlation ID (UUID string) or None.

    Example:
        >>> with CorrelationContext():
        ...     corr_id = get_correlation_id()
        ...     print(f"Correlation ID: {corr_id}")

    References:
        LOG-004: Correlation ID Injection
    """
    return _correlation_id.get()


def set_correlation_id(corr_id: str) -> None:
    """Set the correlation ID for the current context.

    Args:
        corr_id: Correlation ID to set (typically a UUID string).

    Example:
        >>> set_correlation_id("550e8400-e29b-41d4-a716-446655440000")
        >>> print(get_correlation_id())
        550e8400-e29b-41d4-a716-446655440000

    References:
        LOG-004: Correlation ID Injection
    """
    _correlation_id.set(corr_id)


class CorrelationContext:
    """Context manager for correlation ID scoping.

    Automatically generates a UUID correlation ID if not provided,
    and ensures proper cleanup when exiting the context.

    Thread-safe and async-safe using contextvars.

    Args:
        corr_id: Optional correlation ID. If None, generates a new UUID.

    Example:
        >>> # Auto-generate correlation ID
        >>> with CorrelationContext() as corr_id:
        ...     print(f"Generated ID: {corr_id}")
        ...     # All operations here have this correlation ID
        ...     result = some_analysis()

        >>> # Use explicit correlation ID
        >>> with CorrelationContext("my-custom-id") as corr_id:
        ...     print(f"Using ID: {corr_id}")

    References:
        LOG-004: Correlation ID Injection
    """

    def __init__(self, corr_id: str | None = None):
        """Initialize correlation context.

        Args:
            corr_id: Correlation ID to use, or None to auto-generate.
        """
        self.corr_id = corr_id or str(uuid.uuid4())
        self.token: contextvars.Token | None = None  # type: ignore[type-arg]

    def __enter__(self) -> str:
        """Enter the correlation context.

        Returns:
            The correlation ID for this context.
        """
        self.token = _correlation_id.set(self.corr_id)
        return self.corr_id

    def __exit__(self, *args: Any) -> None:
        """Exit the correlation context and restore previous value."""
        if self.token:
            _correlation_id.reset(self.token)


F = TypeVar("F", bound=Callable[..., Any])


def with_correlation_id(corr_id: str | None = None) -> Callable[[F], F]:
    """Decorator to set correlation ID for a function call.

    Automatically wraps the function in a CorrelationContext, ensuring
    all operations within the function are traced with the same ID.

    Args:
        corr_id: Correlation ID to use, or None to auto-generate.

    Returns:
        Decorator function.

    Note:
        This decorator currently only supports synchronous functions.
        For async functions, use CorrelationContext directly:

        >>> async def async_function():
        ...     with CorrelationContext("my-id"):
        ...         await some_async_operation()

    Example:
        >>> @with_correlation_id()
        ... def analyze_trace(trace_data):
        ...     logger.info("Starting analysis")
        ...     # All logs will include the correlation ID
        ...     result = compute_fft(trace_data)
        ...     return result

        >>> @with_correlation_id("batch-job-123")
        ... def process_batch(files):
        ...     for f in files:
        ...         load_and_analyze(f)

    References:
        LOG-004: Correlation ID Injection
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with CorrelationContext(corr_id):
                return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


def generate_correlation_id() -> str:
    """Generate a new correlation ID (UUID4).

    Returns:
        New correlation ID as string.

    Example:
        >>> corr_id = generate_correlation_id()
        >>> with CorrelationContext(corr_id):
        ...     process_data()

    References:
        LOG-004: Correlation ID Injection
    """
    return str(uuid.uuid4())
