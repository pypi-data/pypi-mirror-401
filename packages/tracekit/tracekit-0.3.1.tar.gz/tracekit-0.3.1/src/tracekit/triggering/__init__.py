"""Signal triggering and event detection module for TraceKit.

Provides oscilloscope-style triggering functionality including edge
triggering, pattern triggering, pulse width triggering, glitch detection,
runt pulse detection, and window/zone triggering.

Example:
    >>> from tracekit.triggering import EdgeTrigger, find_triggers
    >>> trigger = EdgeTrigger(level=1.5, edge="rising")
    >>> events = trigger.find_events(trace)
    >>> # Or use convenience function
    >>> events = find_triggers(trace, "edge", level=1.5, edge="rising")
"""

from tracekit.triggering.base import (
    Trigger,
    TriggerEvent,
    find_triggers,
)
from tracekit.triggering.edge import (
    EdgeTrigger,
    find_all_edges,
    find_falling_edges,
    find_rising_edges,
)
from tracekit.triggering.pattern import (
    PatternTrigger,
    find_pattern,
)
from tracekit.triggering.pulse import (
    PulseWidthTrigger,
    find_glitches,
    find_pulses,
    find_runt_pulses,
)
from tracekit.triggering.window import (
    WindowTrigger,
    ZoneTrigger,
    check_limits,
    find_window_violations,
    find_zone_events,
)

__all__ = [
    # Edge triggering
    "EdgeTrigger",
    # Pattern triggering
    "PatternTrigger",
    # Pulse triggering
    "PulseWidthTrigger",
    # Base
    "Trigger",
    "TriggerEvent",
    # Window triggering
    "WindowTrigger",
    "ZoneTrigger",
    "check_limits",
    "find_all_edges",
    "find_falling_edges",
    "find_glitches",
    "find_pattern",
    "find_pulses",
    "find_rising_edges",
    "find_runt_pulses",
    "find_triggers",
    "find_window_violations",
    "find_zone_events",
]
