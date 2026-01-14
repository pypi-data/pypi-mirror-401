"""Session management for TraceKit analysis sessions.

This module provides session save/restore, trace annotations, and
operation history tracking.


Example:
    >>> import tracekit as tk
    >>> session = tk.Session()
    >>> session.load_trace('capture.wfm')
    >>> session.annotate(time=1.5e-6, text='Glitch here')
    >>> session.save('debug_session.tks')
    >>>
    >>> # Later...
    >>> session = tk.load_session('debug_session.tks')
    >>> print(session.annotations)
"""

from tracekit.session.annotations import Annotation, AnnotationLayer, AnnotationType
from tracekit.session.history import HistoryEntry, OperationHistory
from tracekit.session.session import Session, load_session

__all__ = [
    # Annotations (SESS-002)
    "Annotation",
    "AnnotationLayer",
    "AnnotationType",
    # History (SESS-003)
    "HistoryEntry",
    "OperationHistory",
    # Session (SESS-001)
    "Session",
    "load_session",
]
