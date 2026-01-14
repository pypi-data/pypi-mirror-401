"""TraceKit exception hierarchy - DEPRECATED compatibility module.

.. deprecated:: 1.0.0
    This module is deprecated for backward compatibility only.
    New code MUST import from `tracekit.core.exceptions` directly.
    This module will be removed in a future major version.

This module re-exports exceptions from tracekit.core.exceptions.
The canonical location for all exception classes is `tracekit.core.exceptions`.

Why two files exist:
    - `tracekit/core/exceptions.py`: Canonical implementation of all exception classes
    - `tracekit/exceptions.py` (this file): Deprecated re-export for backward compatibility

Migration guide:
    Old (deprecated):
        from tracekit.exceptions import LoaderError

    New (preferred):
        from tracekit.core.exceptions import LoaderError
"""

import warnings

# Issue deprecation warning on import
warnings.warn(
    "tracekit.exceptions is deprecated. "
    "Import from tracekit.core.exceptions instead. "
    "This module will be removed in a future major version.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export all exceptions from core.exceptions
from tracekit.core.exceptions import (  # noqa: E402
    AnalysisError,
    ConfigurationError,
    ExportError,
    FormatError,
    InsufficientDataError,
    LoaderError,
    SampleRateError,
    TraceKitError,
    UnsupportedFormatError,
    ValidationError,
)

__all__ = [
    "AnalysisError",
    "ConfigurationError",
    "ExportError",
    "FormatError",
    "InsufficientDataError",
    "LoaderError",
    "SampleRateError",
    "TraceKitError",
    "UnsupportedFormatError",
    "ValidationError",
]
