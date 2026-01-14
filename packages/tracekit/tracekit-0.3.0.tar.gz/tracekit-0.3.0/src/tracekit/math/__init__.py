"""Math and arithmetic operations module for TraceKit.

This module provides waveform math operations including arithmetic,
interpolation, and mathematical transformations.
"""

from tracekit.math.arithmetic import (
    absolute,
    add,
    differentiate,
    divide,
    integrate,
    invert,
    math_expression,
    multiply,
    offset,
    scale,
    subtract,
)
from tracekit.math.interpolation import (
    align_traces,
    downsample,
    interpolate,
    resample,
)

__all__ = [
    "absolute",
    # Arithmetic operations
    "add",
    "align_traces",
    "differentiate",
    "divide",
    "downsample",
    "integrate",
    # Interpolation
    "interpolate",
    "invert",
    "math_expression",
    "multiply",
    "offset",
    "resample",
    "scale",
    "subtract",
]
