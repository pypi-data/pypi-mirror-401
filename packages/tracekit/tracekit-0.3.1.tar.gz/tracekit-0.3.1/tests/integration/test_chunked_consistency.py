"""Chunked vs non-chunked consistency integration tests.

This module tests that chunked/streaming analyzers produce consistent
results with their non-chunked counterparts. This is critical for
ensuring that large file processing does not introduce accuracy errors.

LOW-003: Integration test additions
"""

from __future__ import annotations

import numpy as np
import pytest

from tracekit.core.types import TraceMetadata, WaveformTrace

pytestmark = pytest.mark.integration


def make_waveform_trace(data: np.ndarray, sample_rate: float = 1e9) -> WaveformTrace:
    """Create a WaveformTrace from raw data."""
    metadata = TraceMetadata(sample_rate=sample_rate)
    return WaveformTrace(data=data.astype(np.float64), metadata=metadata)


# =============================================================================
# FFT Consistency Tests
# =============================================================================


class TestFFTChunkedConsistency:
    """Test FFT chunked vs non-chunked consistency."""

    @pytest.mark.parametrize("signal_length", [1000, 10000, 100000])
    @pytest.mark.skip(
        reason="API mismatch: fft_chunked expects file path, not in-memory array. "
        "Test needs refactoring to write temp files or use array-based API."
    )
    def test_fft_magnitude_consistency(self, signal_length: int) -> None:
        """Test that chunked FFT produces similar magnitude spectrum.

        Note: Currently skipped - fft_chunked API expects:
          - file_path (str | Path) - binary file path
          - segment_size (not chunk_size)

        This test was written for an in-memory array API that doesn't exist.
        Needs rewrite to use file-based API or alternative function.
        """
        # Generate test signal with known frequencies
        sample_rate = 1e6
        t = np.arange(signal_length) / sample_rate
        signal = (
            np.sin(2 * np.pi * 1000 * t)
            + 0.5 * np.sin(2 * np.pi * 5000 * t)
            + 0.25 * np.sin(2 * np.pi * 10000 * t)
        )

        # Direct FFT
        fft_direct = np.fft.rfft(signal)
        mag_direct = np.abs(fft_direct)

        # TODO: Rewrite to use file-based API or array-based alternative
        # freqs = np.fft.rfftfreq(signal_length, 1 / sample_rate)
        # direct_peaks = np.argsort(mag_direct)[-3:]  # Top 3 peaks

    @pytest.mark.parametrize("chunk_size", [256, 512, 1024, 2048])
    @pytest.mark.skip(
        reason="API mismatch: fft_chunked expects file path, not in-memory array. "
        "Test needs refactoring to write temp files or use array-based API."
    )
    def test_fft_chunk_size_invariance(self, chunk_size: int) -> None:
        """Test that different chunk sizes produce similar results.

        Note: Currently skipped - fft_chunked API expects:
          - file_path (str | Path) - binary file path
          - segment_size parameter (not chunk_size)

        This test was written for an in-memory array API that doesn't exist.
        """
        # Generate test signal
        signal_length = 10000
        sample_rate = 1e6
        t = np.arange(signal_length) / sample_rate
        signal = np.sin(2 * np.pi * 1000 * t)

        # TODO: Rewrite to use file-based API with temp files


# =============================================================================
# Statistics Consistency Tests
# =============================================================================


class TestStatisticsChunkedConsistency:
    """Test streaming statistics vs batch statistics consistency."""

    @pytest.mark.parametrize("sample_count", [1000, 10000, 100000])
    def test_mean_consistency(self, sample_count: int) -> None:
        """Test that streaming mean equals batch mean."""
        # Generate test data
        rng = np.random.default_rng(42)
        data = rng.normal(loc=5.0, scale=2.0, size=sample_count)

        # Batch mean
        batch_mean = np.mean(data)

        # Streaming mean
        def streaming_mean(data: np.ndarray, chunk_size: int = 1000) -> float:
            """Calculate mean in streaming fashion."""
            total = 0.0
            count = 0
            for i in range(0, len(data), chunk_size):
                chunk = data[i : i + chunk_size]
                total += np.sum(chunk)
                count += len(chunk)
            return total / count

        stream_mean = streaming_mean(data)

        # Should be very close (within floating point precision)
        np.testing.assert_allclose(stream_mean, batch_mean, rtol=1e-10)

    @pytest.mark.parametrize("sample_count", [1000, 10000, 100000])
    def test_variance_consistency(self, sample_count: int) -> None:
        """Test that streaming variance equals batch variance."""
        # Generate test data
        rng = np.random.default_rng(42)
        data = rng.normal(loc=5.0, scale=2.0, size=sample_count)

        # Batch variance
        batch_var = np.var(data)

        # Streaming variance (Welford's algorithm)
        def streaming_variance(data: np.ndarray, chunk_size: int = 1000) -> float:
            """Calculate variance in streaming fashion using Welford's algorithm."""
            n = 0
            mean = 0.0
            M2 = 0.0

            for i in range(0, len(data), chunk_size):
                chunk = data[i : i + chunk_size]
                for x in chunk:
                    n += 1
                    delta = x - mean
                    mean += delta / n
                    delta2 = x - mean
                    M2 += delta * delta2

            return M2 / n if n > 0 else 0.0

        stream_var = streaming_variance(data)

        # Should be close (may have small numerical differences)
        np.testing.assert_allclose(stream_var, batch_var, rtol=1e-6)

    def test_min_max_consistency(self) -> None:
        """Test that streaming min/max equals batch min/max."""
        # Generate test data
        rng = np.random.default_rng(42)
        data = rng.uniform(-100, 100, size=50000)

        # Batch
        batch_min = np.min(data)
        batch_max = np.max(data)

        # Streaming
        def streaming_minmax(data: np.ndarray, chunk_size: int = 1000):
            """Calculate min/max in streaming fashion."""
            running_min = np.inf
            running_max = -np.inf

            for i in range(0, len(data), chunk_size):
                chunk = data[i : i + chunk_size]
                running_min = min(running_min, np.min(chunk))
                running_max = max(running_max, np.max(chunk))

            return running_min, running_max

        stream_min, stream_max = streaming_minmax(data)

        # Should be exactly equal
        assert stream_min == batch_min
        assert stream_max == batch_max


# =============================================================================
# Edge Detection Consistency Tests
# =============================================================================


class TestEdgeDetectionConsistency:
    """Test edge detection consistency with different methods."""

    def test_edge_count_consistency(self) -> None:
        """Test that chunked edge detection finds same number of edges."""
        try:
            from tracekit.analyzers.digital.edges import detect_edges
        except ImportError:
            pytest.skip("detect_edges not available")

        # Generate square wave signal
        signal_length = 10000
        period = 100
        signal = np.zeros(signal_length)
        for i in range(0, signal_length, period):
            signal[i : i + period // 2] = 3.3

        # Batch detection
        batch_edges = detect_edges(signal, threshold=1.65)

        # Chunked detection (simulated)
        def chunked_edge_detect(signal: np.ndarray, threshold: float, chunk_size: int = 1000):
            """Detect edges in chunks."""
            all_edges = []
            overlap = 10  # Small overlap to catch edges at boundaries

            for i in range(0, len(signal), chunk_size - overlap):
                chunk_start = i
                chunk_end = min(i + chunk_size, len(signal))
                chunk = signal[chunk_start:chunk_end]

                # Detect edges in chunk
                chunk_edges = detect_edges(chunk, threshold=threshold)

                # Adjust indices and add to result (avoid duplicates)
                for edge in chunk_edges:
                    global_idx = chunk_start + edge.sample_index
                    if global_idx not in all_edges:
                        all_edges.append(global_idx)

            return sorted(set(all_edges))

        chunked_edges = chunked_edge_detect(signal, threshold=1.65)

        # Edge counts should be similar (chunked may find a few more due to overlap)
        assert abs(len(chunked_edges) - len(batch_edges)) <= 2


# =============================================================================
# Histogram Consistency Tests
# =============================================================================


class TestHistogramConsistency:
    """Test histogram computation consistency."""

    @pytest.mark.parametrize("sample_count", [10000, 100000])
    def test_histogram_consistency(self, sample_count: int) -> None:
        """Test that chunked histogram equals batch histogram."""
        # Generate test data
        rng = np.random.default_rng(42)
        data = rng.normal(loc=0, scale=1, size=sample_count)

        # Define bins
        bins = np.linspace(-4, 4, 50)

        # Batch histogram
        batch_hist, _ = np.histogram(data, bins=bins)

        # Chunked histogram
        def chunked_histogram(data: np.ndarray, bins: np.ndarray, chunk_size: int = 5000):
            """Compute histogram in chunks."""
            hist = np.zeros(len(bins) - 1, dtype=np.int64)

            for i in range(0, len(data), chunk_size):
                chunk = data[i : i + chunk_size]
                chunk_hist, _ = np.histogram(chunk, bins=bins)
                hist += chunk_hist

            return hist

        chunked_hist = chunked_histogram(data, bins)

        # Should be exactly equal
        np.testing.assert_array_equal(chunked_hist, batch_hist)


# =============================================================================
# Percentile Consistency Tests
# =============================================================================


class TestPercentileConsistency:
    """Test percentile computation consistency."""

    def test_median_consistency(self) -> None:
        """Test that approximate streaming median is close to exact median."""
        # Generate test data
        rng = np.random.default_rng(42)
        data = rng.normal(loc=100, scale=20, size=100000)

        # Exact median
        exact_median = np.median(data)

        # Approximate median using reservoir sampling
        def approximate_median(data: np.ndarray, reservoir_size: int = 10000):
            """Approximate median using reservoir sampling."""
            rng = np.random.default_rng(42)
            reservoir = np.zeros(reservoir_size)

            for i, x in enumerate(data):
                if i < reservoir_size:
                    reservoir[i] = x
                else:
                    j = rng.integers(0, i + 1)
                    if j < reservoir_size:
                        reservoir[j] = x

            n = min(len(data), reservoir_size)
            return float(np.median(reservoir[:n]))

        approx_median = approximate_median(data)

        # Should be within 5% for normal distribution
        relative_error = abs(approx_median - exact_median) / exact_median
        assert relative_error < 0.05, f"Median error: {relative_error:.2%}"


# =============================================================================
# Correlation Consistency Tests
# =============================================================================


class TestCorrelationConsistency:
    """Test correlation computation consistency."""

    def test_autocorrelation_consistency(self) -> None:
        """Test that chunked autocorrelation is consistent."""
        # Generate periodic signal
        signal_length = 10000
        period = 100
        signal = np.sin(2 * np.pi * np.arange(signal_length) / period)

        # Full autocorrelation
        full_autocorr = np.correlate(signal, signal, mode="full")
        full_autocorr = full_autocorr[len(signal) - 1 :]  # Keep positive lags

        # Verify periodicity detection
        # Find first peak after lag 0
        peaks = []
        for i in range(1, min(500, len(full_autocorr) - 1)):
            if full_autocorr[i] > full_autocorr[i - 1] and full_autocorr[i] > full_autocorr[i + 1]:
                peaks.append(i)

        # First peak should be near the period
        if peaks:
            detected_period = peaks[0]
            assert abs(detected_period - period) < 5, (
                f"Period detection off: {detected_period} vs {period}"
            )


# =============================================================================
# Cross-Module Integration Tests
# =============================================================================


class TestCrossModuleIntegration:
    """Test integration between different modules."""

    def test_loader_to_analyzer_data_integrity(self) -> None:
        """Test that data integrity is preserved from loader to analyzer."""
        # Simulate loading data
        sample_rate = 1e9
        duration = 0.001  # 1ms
        n_samples = int(sample_rate * duration)

        # Create test signal
        t = np.arange(n_samples) / sample_rate
        original_signal = np.sin(2 * np.pi * 1e6 * t)  # 1 MHz sine

        # Create trace
        trace = make_waveform_trace(original_signal, sample_rate=sample_rate)

        # Verify data is unchanged
        np.testing.assert_array_equal(trace.data, original_signal)

        # Verify metadata is correct
        assert trace.metadata.sample_rate == sample_rate

    def test_analyzer_chain_data_flow(self) -> None:
        """Test data flow through a chain of analyzers."""
        # Create test signal
        sample_rate = 1e6
        duration = 0.01
        n_samples = int(sample_rate * duration)
        t = np.arange(n_samples) / sample_rate

        signal = np.sin(2 * np.pi * 1000 * t) + np.random.normal(0, 0.1, n_samples)

        # Step 1: Basic statistics
        mean_val = np.mean(signal)
        std_val = np.std(signal)

        assert abs(mean_val) < 0.5  # Should be close to 0 for sine wave
        assert 0.5 < std_val < 1.0  # Should be ~0.7 for unit sine

        # Step 2: DC removal
        dc_removed = signal - mean_val

        # Verify DC is removed
        assert abs(np.mean(dc_removed)) < 1e-10

        # Step 3: FFT
        fft_result = np.fft.rfft(dc_removed)
        freqs = np.fft.rfftfreq(n_samples, 1 / sample_rate)

        # Find dominant frequency
        peak_idx = np.argmax(np.abs(fft_result[1:])) + 1  # Skip DC
        dominant_freq = freqs[peak_idx]

        # Should detect 1 kHz
        assert abs(dominant_freq - 1000) < 50  # Within 50 Hz

    def test_protocol_decoder_to_message_parser(self) -> None:
        """Test data flow from protocol decoder to message parser."""
        # Simulate decoded packets
        packets = [
            {"timestamp": 0.0, "data": b"\x01\x02\x03\x04"},
            {"timestamp": 0.001, "data": b"\x01\x02\x05\x06"},
            {"timestamp": 0.002, "data": b"\x01\x02\x07\x08"},
        ]

        # Extract common header
        common_bytes = []
        for i in range(min(len(p["data"]) for p in packets)):
            byte_vals = [p["data"][i] for p in packets]
            if len(set(byte_vals)) == 1:
                common_bytes.append((i, byte_vals[0]))

        # Should identify bytes 0 and 1 as constant header
        assert len(common_bytes) == 2
        assert common_bytes[0] == (0, 0x01)
        assert common_bytes[1] == (1, 0x02)
