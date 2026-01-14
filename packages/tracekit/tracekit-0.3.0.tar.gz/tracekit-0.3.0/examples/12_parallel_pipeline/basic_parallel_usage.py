"""Example: Basic ParallelPipeline usage for trace analysis.

This example demonstrates how to use ParallelPipeline to speed up
trace processing by executing independent stages in parallel.

ParallelPipeline is fully API-compatible with the standard Pipeline,
so you can use it as a drop-in replacement to get automatic parallelization.
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

from __future__ import annotations

import time

import numpy as np

from tracekit.core.types import TraceMetadata, WaveformTrace
from tracekit.pipeline import ParallelPipeline
from tracekit.pipeline.base import TraceTransformer

# ============================================================================
# Example Transformers
# ============================================================================


class LowPassFilter(TraceTransformer):
    """Simple low-pass filter (example implementation)."""

    def __init__(self, cutoff: float = 1e6) -> None:
        self.cutoff = cutoff

    def transform(self, trace: WaveformTrace) -> WaveformTrace:
        """Apply low-pass filter (simplified)."""
        # Simulate processing time
        time.sleep(0.1)

        # Simple moving average as mock low-pass filter
        window_size = 5
        filtered = np.convolve(trace.data, np.ones(window_size) / window_size, mode="same")

        return WaveformTrace(data=filtered, metadata=trace.metadata)


class HighPassFilter(TraceTransformer):
    """Simple high-pass filter (example implementation)."""

    def __init__(self, cutoff: float = 1e3) -> None:
        self.cutoff = cutoff

    def transform(self, trace: WaveformTrace) -> WaveformTrace:
        """Apply high-pass filter (simplified)."""
        # Simulate processing time
        time.sleep(0.1)

        # Simple derivative as mock high-pass filter
        filtered = np.diff(trace.data, prepend=trace.data[0])

        return WaveformTrace(data=filtered, metadata=trace.metadata)


class Normalize(TraceTransformer):
    """Normalize trace to [-1, 1] range."""

    def transform(self, trace: WaveformTrace) -> WaveformTrace:
        """Normalize trace data."""
        data_range = np.ptp(trace.data)
        if data_range == 0:
            normalized = trace.data
        else:
            normalized = 2 * (trace.data - np.min(trace.data)) / data_range - 1

        return WaveformTrace(data=normalized, metadata=trace.metadata)


# ============================================================================
# Example 1: Basic Sequential Pipeline
# ============================================================================


def example_sequential_pipeline() -> None:
    """Demonstrate sequential pipeline execution."""
    print("=" * 70)
    print("Example 1: Sequential Pipeline")
    print("=" * 70)

    # Create synthetic trace
    t = np.linspace(0, 1e-3, 10000)
    signal = np.sin(2 * np.pi * 1e3 * t) + 0.5 * np.sin(2 * np.pi * 5e3 * t)
    trace = WaveformTrace(data=signal, metadata=TraceMetadata(sample_rate=1e7))

    # Create pipeline with sequential stages
    pipeline = ParallelPipeline(
        [
            ("lowpass", LowPassFilter(cutoff=2e3)),
            ("normalize", Normalize()),
        ]
    )

    print(f"Pipeline configuration: {pipeline.executor_type} executor")
    print(f"Worker count: {pipeline.max_workers or 'auto'}")
    print()

    # Execute pipeline
    start = time.time()
    result = pipeline.transform(trace)
    duration = time.time() - start

    print(f"Pipeline execution time: {duration:.3f} seconds")
    print(f"Input shape: {trace.data.shape}")
    print(f"Output shape: {result.data.shape}")
    print(f"Output range: [{result.data.min():.3f}, {result.data.max():.3f}]")
    print()


# ============================================================================
# Example 2: Thread Pool Executor
# ============================================================================


def example_thread_pool() -> None:
    """Demonstrate thread pool executor for I/O-bound tasks."""
    print("=" * 70)
    print("Example 2: Thread Pool Executor")
    print("=" * 70)

    # Create synthetic trace
    t = np.linspace(0, 1e-3, 10000)
    signal = np.sin(2 * np.pi * 1e3 * t)
    trace = WaveformTrace(data=signal, metadata=TraceMetadata(sample_rate=1e7))

    # Create pipeline with thread pool
    pipeline = ParallelPipeline(
        [
            ("filter1", LowPassFilter(cutoff=2e3)),
            ("filter2", HighPassFilter(cutoff=500)),
            ("normalize", Normalize()),
        ],
        executor_type="thread",
        max_workers=4,
    )

    print(f"Pipeline: {pipeline}")
    print()

    # Check dependency graph
    print("Dependency graph:")
    for stage, deps in pipeline.get_dependency_graph().items():
        print(f"  {stage}: depends on {deps if deps else 'nothing'}")
    print()

    # Check execution order
    print("Execution order (parallel generations):")
    for i, generation in enumerate(pipeline.get_execution_order()):
        print(f"  Generation {i}: {generation}")
    print()

    # Execute pipeline
    start = time.time()
    result = pipeline.transform(trace)
    duration = time.time() - start

    print(f"Pipeline execution time: {duration:.3f} seconds")
    print(f"Result shape: {result.data.shape}")
    print()


# ============================================================================
# Example 3: Process Pool Executor
# ============================================================================


def example_process_pool() -> None:
    """Demonstrate process pool executor for CPU-bound tasks."""
    print("=" * 70)
    print("Example 3: Process Pool Executor")
    print("=" * 70)

    # Create synthetic trace
    t = np.linspace(0, 1e-3, 10000)
    signal = np.sin(2 * np.pi * 1e3 * t)
    trace = WaveformTrace(data=signal, metadata=TraceMetadata(sample_rate=1e7))

    # Create pipeline with process pool
    pipeline = ParallelPipeline(
        [
            ("filter", LowPassFilter(cutoff=2e3)),
            ("normalize", Normalize()),
        ],
        executor_type="process",
        max_workers=2,
    )

    print(f"Pipeline configuration: {pipeline.executor_type} executor")
    print(f"Worker count: {pipeline.max_workers}")
    print()

    # Execute pipeline
    start = time.time()
    result = pipeline.transform(trace)
    duration = time.time() - start

    print(f"Pipeline execution time: {duration:.3f} seconds")
    print(f"Result range: [{result.data.min():.3f}, {result.data.max():.3f}]")
    print()


# ============================================================================
# Example 4: Dynamic Configuration
# ============================================================================


def example_dynamic_config() -> None:
    """Demonstrate changing executor configuration at runtime."""
    print("=" * 70)
    print("Example 4: Dynamic Configuration")
    print("=" * 70)

    # Create synthetic trace
    t = np.linspace(0, 1e-3, 10000)
    signal = np.sin(2 * np.pi * 1e3 * t)
    trace = WaveformTrace(data=signal, metadata=TraceMetadata(sample_rate=1e7))

    # Create pipeline with default configuration
    pipeline = ParallelPipeline([("filter", LowPassFilter(cutoff=2e3)), ("normalize", Normalize())])

    print(
        f"Initial config: {pipeline.executor_type} executor, {pipeline.max_workers or 'auto'} workers"
    )

    # Test with thread pool
    pipeline.set_parallel_config(executor_type="thread", max_workers=2)
    print(f"Changed to: {pipeline.executor_type} executor, {pipeline.max_workers} workers")

    start = time.time()
    result1 = pipeline.transform(trace)
    duration1 = time.time() - start
    print(f"Thread pool execution time: {duration1:.3f} seconds")

    # Test with process pool
    pipeline.set_parallel_config(executor_type="process", max_workers=2)
    print(f"Changed to: {pipeline.executor_type} executor, {pipeline.max_workers} workers")

    start = time.time()
    result2 = pipeline.transform(trace)
    duration2 = time.time() - start
    print(f"Process pool execution time: {duration2:.3f} seconds")

    # Verify results are equivalent
    np.testing.assert_array_almost_equal(result1.data, result2.data)
    print("Results are numerically equivalent!")
    print()


# ============================================================================
# Example 5: Accessing Intermediate Results
# ============================================================================


def example_intermediate_results() -> None:
    """Demonstrate accessing intermediate results from pipeline stages."""
    print("=" * 70)
    print("Example 5: Intermediate Results")
    print("=" * 70)

    # Create synthetic trace
    t = np.linspace(0, 1e-3, 10000)
    signal = np.sin(2 * np.pi * 1e3 * t) + 0.5
    trace = WaveformTrace(data=signal, metadata=TraceMetadata(sample_rate=1e7))

    # Create pipeline
    pipeline = ParallelPipeline([("filter", LowPassFilter(cutoff=2e3)), ("normalize", Normalize())])

    # Execute pipeline
    result = pipeline.transform(trace)

    # Access intermediate results
    print("Accessing intermediate results:")

    # Get filtered trace (before normalization)
    filtered = pipeline.get_intermediate("filter")
    print(f"  After filter: range=[{filtered.data.min():.3f}, {filtered.data.max():.3f}]")

    # Get final normalized trace
    normalized = pipeline.get_intermediate("normalize")
    print(f"  After normalize: range=[{normalized.data.min():.3f}, {normalized.data.max():.3f}]")

    # List all available intermediates
    print("\nAvailable intermediates:")
    all_intermediates = pipeline.list_intermediates()
    for stage, intermediates in all_intermediates.items():
        print(f"  {stage}: {intermediates if intermediates else 'none'}")
    print()


# ============================================================================
# Main
# ============================================================================


def main() -> None:
    """Run all examples."""
    print("\n")
    print("=" * 70)
    print("ParallelPipeline Examples")
    print("=" * 70)
    print()

    example_sequential_pipeline()
    example_thread_pool()
    example_process_pool()
    example_dynamic_config()
    example_intermediate_results()

    print("=" * 70)
    print("All examples completed successfully!")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
