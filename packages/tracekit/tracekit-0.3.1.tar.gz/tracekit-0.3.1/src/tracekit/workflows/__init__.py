"""High-level workflow presets for TraceKit.

This module provides one-call analysis workflows for common signal
characterization tasks.
"""

from tracekit.workflows.compliance import emc_compliance_test
from tracekit.workflows.digital import characterize_buffer
from tracekit.workflows.multi_trace import (
    AlignmentMethod,
    MultiTraceResults,
    MultiTraceWorkflow,
    TraceStatistics,
    load_all,
)
from tracekit.workflows.power import power_analysis
from tracekit.workflows.protocol import debug_protocol
from tracekit.workflows.signal_integrity import signal_integrity_audit

__all__ = [
    "AlignmentMethod",
    "MultiTraceResults",
    "MultiTraceWorkflow",
    "TraceStatistics",
    "characterize_buffer",
    "debug_protocol",
    "emc_compliance_test",
    "load_all",
    "power_analysis",
    "signal_integrity_audit",
]
