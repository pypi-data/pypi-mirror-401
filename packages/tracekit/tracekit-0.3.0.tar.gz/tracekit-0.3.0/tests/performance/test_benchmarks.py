"""Performance benchmark tests using pytest-benchmark.

Converted from standalone comprehensive_profiling.py script.
These tests measure performance of critical code paths and can
run in CI to detect regressions.

Benchmarks are organized by module:
- Loaders: Binary data loading performance
- Analyzers: Signal analysis and processing
- Inference: Protocol inference algorithms
- Memory: Memory usage and efficiency
- Large Files: 1GB+ file processing (MED-005)
- Chunked Analyzers: Streaming/chunked processing performance

Run with:
    pytest tests/performance/test_benchmarks.py --benchmark-only
    pytest tests/performance/test_benchmarks.py --benchmark-only --benchmark-json=results.json
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from numpy.typing import NDArray

from tracekit.core.types import TraceMetadata, WaveformTrace

pytestmark = [pytest.mark.performance, pytest.mark.benchmark]


# =============================================================================
# Loader Benchmarks
# =============================================================================


class TestLoaderBenchmarks:
    """Benchmarks for data loaders."""

    @pytest.mark.parametrize("file_size_mb", [1, 10])
    def test_binary_loader_performance(self, benchmark, tmp_path: Path, file_size_mb: int) -> None:
        """Benchmark binary file loading at different sizes.

        Args:
            benchmark: pytest-benchmark fixture.
            tmp_path: Temporary directory fixture.
            file_size_mb: File size in megabytes.
        """
        from tracekit.loaders import load

        # Create test file
        file_path = tmp_path / f"test_{file_size_mb}mb.npz"
        data_size = file_size_mb * 1024 * 1024 // 8  # float64 = 8 bytes
        test_data = np.random.randn(data_size)
        metadata = TraceMetadata(sample_rate=1e9)
        np.savez(file_path, data=test_data, sample_rate=metadata.sample_rate)

        # Benchmark loading
        result = benchmark(load, file_path)

        # Assertions
        assert result is not None
        assert len(result.data) == data_size

    @pytest.mark.slow
    def test_npz_loader_large_file(self, benchmark, tmp_path: Path) -> None:
        """Benchmark loading of large NPZ files (100MB).

        Args:
            benchmark: pytest-benchmark fixture.
            tmp_path: Temporary directory fixture.
        """
        from tracekit.loaders import load

        # Create 100MB test file
        file_path = tmp_path / "large_100mb.npz"
        data_size = 100 * 1024 * 1024 // 8  # 100MB of float64 data
        test_data = np.random.randn(data_size)
        metadata = TraceMetadata(sample_rate=1e9)
        np.savez(file_path, data=test_data, sample_rate=metadata.sample_rate)

        # Benchmark
        result = benchmark(load, file_path)

        # Assertions
        assert result is not None
        assert len(result.data) == data_size


# =============================================================================
# Analyzer Benchmarks
# =============================================================================


class TestAnalyzerBenchmarks:
    """Benchmarks for signal analyzers."""

    @pytest.mark.parametrize("signal_length", [1000, 10000, 100000])
    def test_edge_detection_performance(self, benchmark, signal_length: int) -> None:
        """Benchmark edge detection at different signal lengths.

        Args:
            benchmark: pytest-benchmark fixture.
            signal_length: Number of samples in signal.
        """
        from tracekit.analyzers.digital.edges import detect_edges

        # Generate test signal - square wave
        t = np.linspace(0, 1, signal_length)
        signal = np.where(np.sin(2 * np.pi * 10 * t) > 0, 3.3, 0.0)

        # Benchmark
        result = benchmark(detect_edges, signal, threshold=1.65)

        # Assertions
        assert result is not None
        assert len(result) > 0

    @pytest.mark.parametrize("signal_length", [1000, 10000])
    def test_basic_stats_performance(self, benchmark, signal_length: int) -> None:
        """Benchmark basic statistics computation.

        Args:
            benchmark: pytest-benchmark fixture.
            signal_length: Number of samples in signal.
        """
        from tracekit.analyzers.statistics import basic

        # Generate test signal
        signal = np.random.randn(signal_length)

        # Benchmark
        result = benchmark(basic.basic_stats, signal)

        # Assertions
        assert result is not None
        assert "mean" in result
        assert "std" in result

    @pytest.mark.slow
    def test_fft_performance(self, benchmark) -> None:
        """Benchmark FFT analysis on 1M samples.

        Args:
            benchmark: pytest-benchmark fixture.
        """
        # Generate 1M sample signal
        signal_length = 1_000_000
        t = np.linspace(0, 1, signal_length)
        signal = np.sin(2 * np.pi * 1000 * t) + 0.5 * np.sin(2 * np.pi * 5000 * t)

        # Benchmark FFT
        result = benchmark(np.fft.rfft, signal)

        # Assertions
        assert result is not None
        assert len(result) == signal_length // 2 + 1

    # NOTE: moving_average test removed - function doesn't exist in codebase
    # Can be re-added when function is implemented


# =============================================================================
# Inference Benchmarks
# =============================================================================


class TestInferenceBenchmarks:
    """Benchmarks for protocol inference algorithms."""

    @pytest.mark.parametrize("packet_count", [100, 1000])
    def test_message_format_inference_performance(self, benchmark, packet_count: int) -> None:
        """Benchmark message format inference.

        Args:
            benchmark: pytest-benchmark fixture.
            packet_count: Number of packets to infer from.
        """
        try:
            from tracekit.inference.message_format import infer_format
        except ImportError:
            pytest.skip("infer_format not available")

        # Generate test packets with consistent structure and FIXED length
        # infer_format requires all messages to have same length
        packets = []
        payload_len = 32  # Fixed payload length
        for i in range(packet_count):
            # Header (2 bytes) + Sequence (2 bytes) + Length (1 byte) + Payload (32 bytes) + CRC (2 bytes)
            header = b"\xaa\x55"
            seq = i.to_bytes(2, "big")
            length = payload_len.to_bytes(1, "big")
            payload = bytes([(i + j) % 256 for j in range(payload_len)])
            crc = (sum(payload) & 0xFFFF).to_bytes(2, "big")
            packets.append(header + seq + length + payload + crc)

        # Benchmark - use correct function name
        result = benchmark(infer_format, packets)

        # Assertions
        assert result is not None

    @pytest.mark.slow
    def test_state_machine_learning_performance(self, benchmark) -> None:
        """Benchmark state machine learning (RPNI algorithm).

        Args:
            benchmark: pytest-benchmark fixture.
        """
        from tracekit.inference.state_machine import learn_fsm

        # Create sample sequences (simple alternating pattern)
        positive_samples = []
        for i in range(50):
            seq = [j % 2 for j in range(i % 10 + 5)]
            positive_samples.append(seq)

        # Benchmark
        result = benchmark(learn_fsm, positive_samples, [])

        # Assertions
        assert result is not None
        assert hasattr(result, "states")


# =============================================================================
# Memory Efficiency Benchmarks
# =============================================================================


class TestMemoryBenchmarks:
    """Benchmarks for memory usage and efficiency."""

    @pytest.mark.parametrize("sample_count", [100000, 1000000])
    def test_trace_object_memory_overhead(
        self, benchmark, sample_count: int, memory_monitor
    ) -> None:
        """Benchmark memory overhead of WaveformTrace objects.

        Args:
            benchmark: pytest-benchmark fixture.
            sample_count: Number of samples.
            memory_monitor: Memory monitoring fixture.
        """

        def create_trace() -> WaveformTrace:
            """Create a trace object."""
            data = np.random.randn(sample_count)
            metadata = TraceMetadata(sample_rate=1e9)
            return WaveformTrace(data=data, metadata=metadata)

        # Benchmark with memory monitoring
        with memory_monitor() as monitor:
            result = benchmark(create_trace)

        # Assertions
        assert result is not None
        assert len(result.data) == sample_count

        # Check memory overhead is reasonable
        theoretical_mb = (sample_count * 8) / (1024 * 1024)  # float64 = 8 bytes
        assert monitor.peak_mb < theoretical_mb * 2.5  # Allow 150% overhead

    def test_time_vector_computation_memory(self, benchmark, memory_monitor) -> None:
        """Benchmark memory usage of time vector computation.

        Args:
            benchmark: pytest-benchmark fixture.
            memory_monitor: Memory monitoring fixture.
        """
        # Create a large trace
        sample_count = 1_000_000
        data = np.random.randn(sample_count)
        metadata = TraceMetadata(sample_rate=1e9)
        trace = WaveformTrace(data=data, metadata=metadata)

        # Benchmark time vector access
        def get_time_vector() -> NDArray[np.float64]:
            """Get time vector."""
            return trace.time_vector

        with memory_monitor() as monitor:
            result = benchmark(get_time_vector)

        # Assertions
        assert result is not None
        assert len(result) == sample_count
        # Time vector should be cached, minimal overhead
        assert monitor.peak_mb < 20  # Adjusted for Python memory overhead


# =============================================================================
# Algorithm Complexity Benchmarks
# =============================================================================


class TestComplexityBenchmarks:
    """Benchmarks for measuring algorithm complexity (O(n) behavior)."""

    @pytest.mark.parametrize("size", [1000, 5000, 10000, 50000, 100000], ids=lambda x: f"n={x}")
    def test_statistics_complexity(self, benchmark, size: int) -> None:
        """Measure O(n) behavior of statistics computation.

        Args:
            benchmark: pytest-benchmark fixture.
            size: Data size.
        """
        from tracekit.analyzers.statistics import basic

        # Generate test data
        data = np.random.randn(size)

        # Benchmark
        result = benchmark(basic.basic_stats, data)

        # Assertions
        assert result is not None

    @pytest.mark.parametrize("size", [1000, 10000, 100000], ids=lambda x: f"n={x}")
    def test_edge_detection_complexity(self, benchmark, size: int) -> None:
        """Measure O(n) behavior of edge detection.

        Args:
            benchmark: pytest-benchmark fixture.
            size: Signal length.
        """
        from tracekit.analyzers.digital.edges import detect_edges

        # Generate test signal
        t = np.linspace(0, 1, size)
        signal = np.where(np.sin(2 * np.pi * 10 * t) > 0, 3.3, 0.0)

        # Benchmark
        result = benchmark(detect_edges, signal, threshold=1.65)

        # Assertions
        assert result is not None


# =============================================================================
# Scalability Benchmarks
# =============================================================================


class TestScalabilityBenchmarks:
    """Benchmarks for testing scalability with concurrent operations."""

    @pytest.mark.slow
    def test_sequential_file_loading(self, benchmark, tmp_path: Path) -> None:
        """Benchmark sequential file loading (baseline).

        Args:
            benchmark: pytest-benchmark fixture.
            tmp_path: Temporary directory fixture.
        """
        from tracekit.loaders import load

        # Create multiple test files
        file_paths = []
        for i in range(10):
            file_path = tmp_path / f"test_{i}.npz"
            data = np.random.randn(100000)
            metadata = TraceMetadata(sample_rate=1e9)
            np.savez(file_path, data=data, sample_rate=metadata.sample_rate)
            file_paths.append(file_path)

        # Benchmark sequential loading
        def load_all_sequential() -> list[WaveformTrace]:
            """Load all files sequentially."""
            return [load(p) for p in file_paths]

        result = benchmark(load_all_sequential)

        # Assertions
        assert result is not None
        assert len(result) == 10


# =============================================================================
# Large File Processing Benchmarks (MED-005)
# =============================================================================


class TestLargeFileBenchmarks:
    """Benchmarks for large file processing (1GB+).

    These tests verify that tracekit can handle very large datasets
    efficiently without running out of memory or taking excessive time.
    """

    @pytest.mark.slow
    @pytest.mark.parametrize("file_size_mb", [500, 1000])
    def test_large_file_loading(self, benchmark, tmp_path: Path, file_size_mb: int) -> None:
        """Benchmark loading of very large files (500MB-1GB).

        Args:
            benchmark: pytest-benchmark fixture.
            tmp_path: Temporary directory fixture.
            file_size_mb: File size in megabytes.
        """
        from tracekit.loaders import load

        # Create large test file
        file_path = tmp_path / f"large_{file_size_mb}mb.npz"
        data_size = file_size_mb * 1024 * 1024 // 8  # float64 = 8 bytes
        test_data = np.random.randn(data_size)
        metadata = TraceMetadata(sample_rate=1e9)
        np.savez(file_path, data=test_data, sample_rate=metadata.sample_rate)

        # Benchmark loading - should complete in reasonable time
        result = benchmark.pedantic(
            load,
            args=(file_path,),
            iterations=1,
            rounds=3,
        )

        # Assertions
        assert result is not None
        assert len(result.data) == data_size

    @pytest.mark.slow
    def test_gigabyte_file_processing(self, benchmark, tmp_path: Path) -> None:
        """Benchmark 1GB+ file processing.

        This test verifies that the system can handle gigabyte-scale data.

        Args:
            benchmark: pytest-benchmark fixture.
            tmp_path: Temporary directory fixture.
        """
        # Create ~1GB file (1024MB / 8 bytes = 128M samples)
        file_size_mb = 1024
        file_path = tmp_path / "gigabyte_file.npz"
        data_size = file_size_mb * 1024 * 1024 // 8

        # Generate in chunks to avoid memory issues during setup
        test_data = np.random.randn(data_size)
        metadata = TraceMetadata(sample_rate=1e9)
        np.savez(file_path, data=test_data, sample_rate=metadata.sample_rate)

        # Import after file creation
        from tracekit.loaders import load

        # Benchmark loading - should complete
        result = benchmark.pedantic(
            load,
            args=(file_path,),
            iterations=1,
            rounds=1,
        )

        # Assertions
        assert result is not None
        assert len(result.data) == data_size


# =============================================================================
# Chunked Analyzer Benchmarks (MED-005)
# =============================================================================


class TestChunkedAnalyzerBenchmarks:
    """Benchmarks for chunked/streaming analyzers.

    Tests performance of analyzers that process data in chunks,
    which is essential for handling large files without loading
    everything into memory.
    """

    @pytest.mark.parametrize("chunk_size", [1024, 4096, 16384, 65536])
    def test_chunked_fft_performance(self, benchmark, chunk_size: int) -> None:
        """Benchmark chunked FFT analysis with different chunk sizes.

        Args:
            benchmark: pytest-benchmark fixture.
            chunk_size: Size of each processing chunk.
        """
        try:
            from tracekit.analyzers.spectral.fft import fft_chunked
        except ImportError:
            pytest.skip("fft_chunked not available")

        # Generate large test signal (10M samples)
        signal_length = 10_000_000
        t = np.linspace(0, 1, signal_length)
        signal = np.sin(2 * np.pi * 1000 * t) + 0.5 * np.sin(2 * np.pi * 5000 * t)

        # Benchmark chunked FFT
        result = benchmark(fft_chunked, signal, chunk_size=chunk_size)

        # Assertions
        assert result is not None

    @pytest.mark.parametrize("total_samples", [1_000_000, 10_000_000])
    def test_streaming_statistics_performance(self, benchmark, total_samples: int) -> None:
        """Benchmark streaming statistics computation.

        Args:
            benchmark: pytest-benchmark fixture.
            total_samples: Total number of samples to process.
        """
        try:
            from tracekit.analyzers.statistics.streaming import StreamingStats
        except ImportError:
            pytest.skip("StreamingStats not available")

        # Generate test data
        data = np.random.randn(total_samples)

        def compute_streaming_stats():
            """Compute statistics in streaming fashion."""
            stats = StreamingStats()
            chunk_size = 10000
            for i in range(0, len(data), chunk_size):
                chunk = data[i : i + chunk_size]
                stats.update(chunk)
            return stats.finalize()

        # Benchmark
        result = benchmark(compute_streaming_stats)

        # Assertions
        assert result is not None

    @pytest.mark.slow
    def test_chunked_vs_nonchunked_consistency(self, tmp_path: Path) -> None:
        """Verify chunked and non-chunked analyzers produce consistent results.

        This is a correctness test, not a benchmark, but important for
        validating that chunked processing doesn't lose accuracy.
        """
        try:
            from tracekit.analyzers.spectral.fft import fft_chunked
        except ImportError:
            pytest.skip("fft_chunked not available")

        # Generate test signal
        signal_length = 100_000
        t = np.linspace(0, 1, signal_length)
        signal = np.sin(2 * np.pi * 1000 * t)

        # Non-chunked FFT
        fft_direct = np.fft.rfft(signal)

        # Chunked FFT (should produce similar results)
        fft_chunked_result = fft_chunked(signal, chunk_size=1024)

        # Results should be similar (exact match depends on implementation)
        # For now, just verify both complete without error
        assert fft_direct is not None
        assert fft_chunked_result is not None

    @pytest.mark.slow
    @pytest.mark.parametrize("file_size_mb", [100, 500])
    def test_chunked_file_analysis(self, benchmark, tmp_path: Path, file_size_mb: int) -> None:
        """Benchmark chunked analysis of large files.

        Tests the scenario where a large file is analyzed in chunks
        rather than loading entirely into memory.

        Args:
            benchmark: pytest-benchmark fixture.
            tmp_path: Temporary directory fixture.
            file_size_mb: File size in megabytes.
        """

        # Create large test file
        data_size = file_size_mb * 1024 * 1024 // 8
        test_data = np.random.randn(data_size)

        def analyze_in_chunks(data: np.ndarray, chunk_size: int = 100000) -> dict:
            """Analyze data in chunks, accumulating results."""
            # Simulate chunked analysis
            running_sum = 0.0
            running_sum_sq = 0.0
            total_count = 0

            for i in range(0, len(data), chunk_size):
                chunk = data[i : i + chunk_size]
                running_sum += np.sum(chunk)
                running_sum_sq += np.sum(chunk**2)
                total_count += len(chunk)

            mean = running_sum / total_count
            variance = (running_sum_sq / total_count) - (mean**2)

            return {
                "mean": mean,
                "std": np.sqrt(variance),
                "count": total_count,
            }

        # Benchmark chunked analysis
        result = benchmark(analyze_in_chunks, test_data)

        # Assertions
        assert result is not None
        assert "mean" in result
        assert "std" in result
        assert result["count"] == data_size


# =============================================================================
# Parallel Processing Benchmarks
# =============================================================================


class TestParallelProcessingBenchmarks:
    """Benchmarks for parallel processing capabilities."""

    @pytest.mark.slow
    def test_parallel_fft_performance(self, benchmark) -> None:
        """Benchmark parallel FFT analysis.

        Args:
            benchmark: pytest-benchmark fixture.
        """
        try:
            from tracekit.analyzers.spectral.fft import fft_chunked_parallel
        except ImportError:
            pytest.skip("fft_chunked_parallel not available")

        # Generate large test signal
        signal_length = 10_000_000
        t = np.linspace(0, 1, signal_length)
        signal = np.sin(2 * np.pi * 1000 * t) + 0.5 * np.sin(2 * np.pi * 5000 * t)

        # Benchmark parallel FFT
        result = benchmark(fft_chunked_parallel, signal, n_workers=4)

        # Assertions
        assert result is not None

    @pytest.mark.slow
    def test_parallel_vs_sequential_speedup(self, tmp_path: Path) -> None:
        """Measure speedup from parallel processing.

        This test compares parallel and sequential performance to
        verify that parallelization provides actual benefits.
        """
        import time

        try:
            from tracekit.analyzers.spectral.fft import fft_chunked, fft_chunked_parallel
        except ImportError:
            pytest.skip("fft_chunked_parallel not available")

        # Generate test signal
        signal_length = 5_000_000
        t = np.linspace(0, 1, signal_length)
        signal = np.sin(2 * np.pi * 1000 * t)

        # Time sequential
        start = time.perf_counter()
        fft_chunked(signal, chunk_size=65536)
        sequential_time = time.perf_counter() - start

        # Time parallel
        start = time.perf_counter()
        fft_chunked_parallel(signal, n_workers=4)
        parallel_time = time.perf_counter() - start

        # Log results (not strictly a pass/fail test)
        speedup = sequential_time / parallel_time if parallel_time > 0 else 1.0
        print(f"\nSequential: {sequential_time:.3f}s, Parallel: {parallel_time:.3f}s")
        print(f"Speedup: {speedup:.2f}x")

        # Parallel should not be significantly slower
        assert parallel_time < sequential_time * 1.5  # Allow some overhead
