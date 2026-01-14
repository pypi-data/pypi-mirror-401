"""Expert API module for TraceKit.

This module provides advanced APIs for power users including DSL,
fluent interfaces, performance profiling, and advanced workflow control.
"""

from tracekit.api.dsl import (
    DSLExpression,
    DSLParser,
    analyze,
    parse_expression,
)
from tracekit.api.fluent import (
    FluentResult,
    FluentTrace,
    trace,
)
from tracekit.api.operators import (
    TimeIndex,
    UnitConverter,
    convert_units,
    make_pipeable,
)
from tracekit.api.optimization import (
    GridSearch,
    OptimizationResult,
    ParameterSpace,
    optimize_parameters,
)
from tracekit.api.profiling import (
    OperationProfile,
    Profiler,
    ProfileReport,
    profile,
)

__all__ = [
    # DSL (API-010)
    "DSLExpression",
    "DSLParser",
    # Fluent (API-019)
    "FluentResult",
    "FluentTrace",
    # Optimization (API-014)
    "GridSearch",
    # Profiling (API-012)
    "OperationProfile",
    "OptimizationResult",
    "ParameterSpace",
    "ProfileReport",
    "Profiler",
    # Operators (API-015, API-016, API-018)
    "TimeIndex",
    "UnitConverter",
    "analyze",
    "convert_units",
    "make_pipeable",
    "optimize_parameters",
    "parse_expression",
    "profile",
    "trace",
]
