"""Batch processing functionality for TraceKit.


This module enables efficient batch analysis of multiple signal files
with parallel execution support and comprehensive result aggregation.
"""

from tracekit.batch.advanced import (
    AdvancedBatchProcessor,
    BatchCheckpoint,
    BatchConfig,
    FileResult,
    resume_batch,
)
from tracekit.batch.aggregate import aggregate_results
from tracekit.batch.analyze import batch_analyze
from tracekit.batch.logging import (
    BatchLogger,
    BatchSummary,
    FileLogEntry,
    FileLogger,
    aggregate_batch_logs,
)
from tracekit.batch.metrics import (
    BatchMetrics,
    BatchMetricsSummary,
    ErrorBreakdown,
    FileMetrics,
    ThroughputStats,
    TimingStats,
    get_batch_stats,
)

__all__ = [
    # Advanced batch processing (API-012)
    "AdvancedBatchProcessor",
    "BatchCheckpoint",
    "BatchConfig",
    "BatchLogger",
    "BatchMetrics",
    "BatchMetricsSummary",
    "BatchSummary",
    "ErrorBreakdown",
    "FileLogEntry",
    "FileLogger",
    "FileMetrics",
    "FileResult",
    "ThroughputStats",
    "TimingStats",
    "aggregate_batch_logs",
    "aggregate_results",
    "batch_analyze",
    "get_batch_stats",
    "resume_batch",
]
