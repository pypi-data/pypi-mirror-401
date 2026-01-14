"""CAN bus analysis and reverse engineering.

This submodule provides CAN-specific analysis tools for reverse engineering
automotive protocols from captured CAN bus data.
"""

from __future__ import annotations

__all__ = [
    "ByteChange",
    "CANMessage",
    "CANMessageList",
    "CANSession",
    "CANStateMachine",
    "DecodedSignal",
    "FrequencyChange",
    "MessageAnalysis",
    "MessagePair",
    "MessageSequence",
    "PatternAnalyzer",
    "SequenceExtraction",
    "SignalDefinition",
    "StimulusResponseAnalyzer",
    "StimulusResponseReport",
    "TemporalCorrelation",
]

try:
    from tracekit.automotive.can.models import (
        CANMessage,
        CANMessageList,
        DecodedSignal,
        MessageAnalysis,
        SignalDefinition,
    )
    from tracekit.automotive.can.patterns import (
        MessagePair,
        MessageSequence,
        PatternAnalyzer,
        TemporalCorrelation,
    )
    from tracekit.automotive.can.session import CANSession
    from tracekit.automotive.can.state_machine import CANStateMachine, SequenceExtraction
    from tracekit.automotive.can.stimulus_response import (
        ByteChange,
        FrequencyChange,
        StimulusResponseAnalyzer,
        StimulusResponseReport,
    )
except ImportError:
    # Optional dependencies not installed
    pass
