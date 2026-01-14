"""Pattern search and anomaly detection for TraceKit.


This module enables efficient pattern matching, anomaly detection, and
context extraction for debugging and analysis workflows.
"""

from tracekit.search.anomaly import find_anomalies
from tracekit.search.context import extract_context
from tracekit.search.pattern import find_pattern

__all__ = [
    "extract_context",
    "find_anomalies",
    "find_pattern",
]
