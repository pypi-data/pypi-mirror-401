#!/usr/bin/env python3
"""Advanced Expert API example combining multiple features.

This example demonstrates a real-world workflow combining:
- Custom TraceTransformer (API-004)
- Pipeline composition (API-001)
- Custom measurements (API-008)
- Intermediate results (API-005)
- Algorithm registry (API-006)

Use case: Build a custom analysis pipeline with domain-specific measurements.

Usage:
    uv run python examples/expert_api_advanced.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import numpy as np

import tracekit as tk

# ==============================================================================
# Custom Transformers (API-004)
# ==============================================================================


class NoiseReducer(tk.TraceTransformer):
    """Custom transformer that reduces noise using moving average."""

    def __init__(self, window_size=5) -> None:
        self.window_size = window_size

    def transform(self, trace) -> None:
        """Apply moving average to reduce noise."""
        # Simple moving average
        kernel = np.ones(self.window_size) / self.window_size
        smoothed = np.convolve(trace.data, kernel, mode="same")
        return tk.WaveformTrace(data=smoothed, metadata=trace.metadata)


class TrendRemover(tk.TraceTransformer):
    """Remove linear trend from signal."""

    def __init__(self) -> None:
        self.slope_ = None
        self.intercept_ = None

    def fit(self, trace) -> None:
        """Fit linear trend to trace."""
        x = np.arange(len(trace.data))
        coeffs = np.polyfit(x, trace.data, 1)
        self.slope_ = coeffs[0]
        self.intercept_ = coeffs[1]
        return self

    def transform(self, trace) -> None:
        """Remove fitted linear trend."""
        if self.slope_ is None:
            # No fit, just remove mean
            trend = trace.data.mean()
        else:
            x = np.arange(len(trace.data))
            trend = self.slope_ * x + self.intercept_

        detrended = trace.data - trend
        return tk.WaveformTrace(data=detrended, metadata=trace.metadata)


class OutlierClipper(tk.TraceTransformer):
    """Clip outliers beyond N standard deviations."""

    def __init__(self, n_sigma=3.0) -> None:
        self.n_sigma = n_sigma

    def transform(self, trace) -> None:
        """Clip values beyond n_sigma standard deviations."""
        mean = trace.data.mean()
        std = trace.data.std()
        lower = mean - self.n_sigma * std
        upper = mean + self.n_sigma * std
        clipped = np.clip(trace.data, lower, upper)
        return tk.WaveformTrace(data=clipped, metadata=trace.metadata)


# ==============================================================================
# Custom Measurements (API-008)
# ==============================================================================


def signal_to_noise_ratio(trace, **kwargs) -> None:
    """Calculate SNR as ratio of signal RMS to noise estimate."""
    # Estimate noise from high-frequency components
    diff = np.diff(trace.data)
    noise_rms = np.sqrt(np.mean(diff**2)) / np.sqrt(2)
    signal_rms = np.sqrt(np.mean(trace.data**2))
    if noise_rms == 0:
        return float("inf")
    return 20 * np.log10(signal_rms / noise_rms)


def zero_crossing_rate(trace, **kwargs) -> None:
    """Calculate rate of zero crossings per second."""
    # Count zero crossings
    signs = np.sign(trace.data)
    crossings = np.sum(np.abs(np.diff(signs)) > 0)
    duration = len(trace.data) / trace.metadata.sample_rate
    return crossings / duration


def peak_to_rms_ratio(trace, **kwargs) -> None:
    """Calculate peak-to-RMS ratio (crest factor)."""
    peak = np.abs(trace.data).max()
    rms = np.sqrt(np.mean(trace.data**2))
    if rms == 0:
        return 0.0
    return peak / rms


# ==============================================================================
# Custom Algorithm (API-006)
# ==============================================================================


def adaptive_threshold_detector(data, percentile=90, **kwargs) -> None:
    """Detect peaks using adaptive threshold based on percentile."""
    threshold = np.percentile(np.abs(data), percentile)
    peaks = []
    for i in range(1, len(data) - 1):
        if abs(data[i]) > threshold:
            if abs(data[i]) > abs(data[i - 1]) and abs(data[i]) > abs(data[i + 1]):
                peaks.append(i)
    return peaks


# ==============================================================================
# Registration and Pipeline Setup
# ==============================================================================


def register_custom_components() -> None:
    """Register custom measurements and algorithms with TraceKit.

    This function handles the registration that must happen before
    the custom components can be used.
    """
    # Register custom measurements
    tk.register_measurement(
        name="snr_estimate",
        func=signal_to_noise_ratio,
        units="dB",
        category="quality",
        description="Signal-to-noise ratio estimate",
        tags=["quality", "noise"],
    )

    tk.register_measurement(
        name="zero_crossing_rate",
        func=zero_crossing_rate,
        units="Hz",
        category="timing",
        description="Rate of zero crossings",
        tags=["timing", "frequency"],
    )

    tk.register_measurement(
        name="peak_to_rms",
        func=peak_to_rms_ratio,
        units="ratio",
        category="amplitude",
        description="Peak-to-RMS ratio",
        tags=["amplitude", "quality"],
    )

    # Register custom algorithm
    tk.register_algorithm(
        "adaptive_percentile", adaptive_threshold_detector, category="peak_finder"
    )


# ==============================================================================
# Build Analysis Pipeline (API-001)
# ==============================================================================


def create_analysis_pipeline() -> None:
    """Create a complete analysis pipeline."""
    return tk.Pipeline(
        [
            ("noise_reduce", NoiseReducer(window_size=5)),
            ("remove_trend", TrendRemover()),
            ("clip_outliers", OutlierClipper(n_sigma=3.0)),
        ]
    )


# ==============================================================================
# Main Analysis Workflow
# ==============================================================================


def analyze_signal(trace, verbose=True) -> None:
    """Complete signal analysis workflow combining all Expert APIs."""
    if verbose:
        print("\n" + "=" * 70)
        print("Advanced Expert API Analysis Workflow")
        print("=" * 70)

    # Create and fit pipeline
    pipeline = create_analysis_pipeline()

    if verbose:
        print("\n1. Processing through pipeline...")

    # Fit on trace (for trend removal)
    pipeline.fit(trace)

    # Transform
    processed = pipeline.transform(trace)

    if verbose:
        print(f"   Original signal: mean={trace.data.mean():.3f}, std={trace.data.std():.3f}")
        print(
            f"   Processed signal: mean={processed.data.mean():.3f}, std={processed.data.std():.3f}"
        )

        # Access intermediate results
        print("\n2. Accessing intermediate results...")
        after_noise = pipeline.get_intermediate("noise_reduce")
        after_trend = pipeline.get_intermediate("remove_trend")
        print(f"   After noise reduction: std={after_noise.data.std():.3f}")
        print(f"   After trend removal: mean={after_trend.data.mean():.3f}")

    # Apply custom measurements
    if verbose:
        print("\n3. Computing custom measurements...")

    snr = tk.measure_custom(processed, "snr_estimate")
    zcr = tk.measure_custom(processed, "zero_crossing_rate")
    ptr = tk.measure_custom(processed, "peak_to_rms")

    if verbose:
        print(f"   SNR estimate: {snr:.1f} dB")
        print(f"   Zero crossing rate: {zcr:.1f} Hz")
        print(f"   Peak-to-RMS ratio: {ptr:.2f}")

    # Use custom algorithm
    if verbose:
        print("\n4. Detecting peaks with custom algorithm...")

    peak_finder = tk.get_algorithm("peak_finder", "adaptive_percentile")
    peaks = peak_finder(processed.data, percentile=90)

    if verbose:
        print(f"   Found {len(peaks)} peaks using adaptive threshold")
        if len(peaks) > 0:
            print(f"   Peak locations: {peaks[:5]}{'...' if len(peaks) > 5 else ''}")

    # Create comprehensive result
    result = tk.AnalysisResult(
        value=processed,
        intermediates={
            "original": trace,
            "processed": processed,
            "peaks": peaks,
        },
        metadata={
            "snr_db": snr,
            "zero_crossing_rate_hz": zcr,
            "peak_to_rms": ptr,
            "num_peaks": len(peaks),
            "pipeline_steps": [name for name, _ in pipeline.steps],
        },
    )

    if verbose:
        print("\n5. Analysis complete!")
        print("   Results stored in AnalysisResult object")
        print(f"   Intermediates: {result.list_intermediates()}")
        print(f"   Metadata keys: {list(result.metadata.keys())}")

    return result


def main() -> None:
    """Demonstrate advanced Expert API workflow."""
    print("\n" + "=" * 70)
    print("Expert API Advanced Example")
    print("Combining: Pipeline + Custom Transformers + Measurements + Algorithms")
    print("=" * 70)

    # Register custom components before use
    register_custom_components()

    # Generate test signal: sine wave + noise + trend
    np.random.seed(42)
    t = np.linspace(0, 1.0, 1000)
    signal = (
        np.sin(2 * np.pi * 10 * t)  # 10 Hz sine
        + 0.2 * np.sin(2 * np.pi * 50 * t)  # 50 Hz harmonic
        + 0.1 * np.random.randn(1000)  # Noise
        + 0.5 * t  # Linear trend
    )

    trace = tk.WaveformTrace(data=signal, metadata=tk.TraceMetadata(sample_rate=1000.0))

    # Run complete analysis
    result = analyze_signal(trace, verbose=True)

    # Show final statistics
    print("\n" + "=" * 70)
    print("Final Results Summary")
    print("=" * 70)
    print(f"SNR: {result.metadata['snr_db']:.1f} dB")
    print(f"Zero Crossing Rate: {result.metadata['zero_crossing_rate_hz']:.1f} Hz")
    print(f"Peak-to-RMS: {result.metadata['peak_to_rms']:.2f}")
    print(f"Detected Peaks: {result.metadata['num_peaks']}")
    print(f"Pipeline: {' -> '.join(result.metadata['pipeline_steps'])}")

    print("\n" + "=" * 70)
    print("Advanced Expert API demonstration complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
