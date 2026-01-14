#!/usr/bin/env python3
"""Demonstration of TraceKit Expert API features.

This script demonstrates all 8 CRITICAL Tier 1 Expert API requirements:


Usage:
    uv run python examples/expert_api_demo.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import numpy as np

import tracekit as tk


def demo_pipeline_api() -> None:
    """Demonstrate API-001: Pipeline Architecture."""
    print("\n" + "=" * 60)
    print("API-001: Pipeline Architecture Demo")
    print("=" * 60)

    # Create sample trace
    t = np.linspace(0, 1e-3, 1000)
    data = np.sin(2 * np.pi * 1000 * t) + 0.1 * np.random.randn(1000)
    trace = tk.WaveformTrace(data=data, metadata=tk.TraceMetadata(sample_rate=1e6))

    # Create custom transformer
    class ScaleTransformer(tk.TraceTransformer):
        def __init__(self, factor=2.0) -> None:
            self.factor = factor

        def transform(self, trace) -> None:
            scaled_data = trace.data * self.factor
            return tk.WaveformTrace(data=scaled_data, metadata=trace.metadata)

    # Build pipeline
    pipeline = tk.Pipeline(
        [
            ("scale", ScaleTransformer(factor=2.0)),
        ]
    )

    result = pipeline.transform(trace)
    print(f"[OK] Pipeline created with {len(pipeline)} steps")
    print(f"[OK] Original mean: {trace.data.mean():.3f}")
    print(f"[OK] Scaled mean: {result.data.mean():.3f}")
    print(f"[OK] Scale factor: {result.data.mean() / trace.data.mean():.1f}x")


def demo_composition_api() -> None:
    """Demonstrate API-002: Function Composition."""
    print("\n" + "=" * 60)
    print("API-002: Function Composition Demo")
    print("=" * 60)

    # Create sample trace
    data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    trace = tk.WaveformTrace(data=data, metadata=tk.TraceMetadata(sample_rate=1e6))

    # Define simple transformations
    def double(t) -> None:
        return tk.WaveformTrace(data=t.data * 2, metadata=t.metadata)

    def add_one(t) -> None:
        return tk.WaveformTrace(data=t.data + 1, metadata=t.metadata)

    # Test compose (right-to-left)
    composed = tk.compose(add_one, double)
    result1 = composed(trace)
    print(f"[OK] compose(add_one, double): {result1.data[:3]} ...")

    # Test pipe (left-to-right)
    result2 = tk.pipe(trace, double, add_one)
    print(f"[OK] pipe(trace, double, add_one): {result2.data[:3]} ...")

    # Verify both produce same result
    assert np.allclose(result1.data, result2.data)
    print("[OK] Composition functions work correctly")


def demo_streaming_api() -> None:
    """Demonstrate API-003: Streaming API."""
    print("\n" + "=" * 60)
    print("API-003: Streaming API Demo")
    print("=" * 60)

    # Create streaming analyzer
    analyzer = tk.StreamingAnalyzer()

    # Simulate processing chunks
    num_chunks = 5
    for i in range(num_chunks):
        # Create chunk
        chunk_data = np.random.randn(1000) + i * 0.1
        chunk = tk.WaveformTrace(data=chunk_data, metadata=tk.TraceMetadata(sample_rate=1e6))

        # Accumulate statistics
        analyzer.accumulate_statistics(chunk)

    # Get results
    stats = analyzer.get_statistics()
    print(f"[OK] Processed {num_chunks} chunks")
    print(f"[OK] Total samples: {stats['n_samples']}")
    print(f"[OK] Mean: {stats['mean']:.3f}")
    print(f"[OK] Std: {stats['std']:.3f}")
    print(f"[OK] Range: [{stats['min']:.3f}, {stats['max']:.3f}]")


def demo_transformer_base() -> None:
    """Demonstrate API-004: TraceTransformer Base Class."""
    print("\n" + "=" * 60)
    print("API-004: TraceTransformer Base Class Demo")
    print("=" * 60)

    # Create stateful transformer with fit/transform
    class MeanSubtractor(tk.TraceTransformer):
        def __init__(self) -> None:
            self.mean_ = None

        def fit(self, trace) -> None:
            self.mean_ = trace.data.mean()
            return self

        def transform(self, trace) -> None:
            if self.mean_ is None:
                raise ValueError("Must call fit() first")
            centered = trace.data - self.mean_
            return tk.WaveformTrace(data=centered, metadata=trace.metadata)

    # Test fit/transform pattern
    data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    trace = tk.WaveformTrace(data=data, metadata=tk.TraceMetadata(sample_rate=1e6))

    subtractor = MeanSubtractor()
    subtractor.fit(trace)
    result = subtractor.transform(trace)

    print(f"[OK] Original mean: {trace.data.mean():.3f}")
    print(f"[OK] Fitted mean: {subtractor.mean_:.3f}")
    print(f"[OK] Centered mean: {result.data.mean():.6f}")
    print(f"[OK] get_params(): {subtractor.get_params()}")


def demo_results_api() -> None:
    """Demonstrate API-005: Intermediate Results."""
    print("\n" + "=" * 60)
    print("API-005: Intermediate Results Demo")
    print("=" * 60)

    # Create FFT result
    spectrum = np.array([1.0 + 1.0j, 2.0 + 0.5j, 3.0 + 0.1j])
    frequencies = np.array([0.0, 1000.0, 2000.0])

    fft_result = tk.FFTResult(
        value=spectrum,
        spectrum=spectrum,
        frequencies=frequencies,
        power=np.abs(spectrum) ** 2,
        phase=np.angle(spectrum),
    )

    print("[OK] FFTResult created")
    print(f"[OK] Spectrum shape: {fft_result.spectrum.shape}")
    print(f"[OK] Peak frequency: {fft_result.peak_frequency:.0f} Hz")
    print(f"[OK] Available intermediates: {fft_result.list_intermediates()}")

    # Test intermediate access
    power = fft_result.get_intermediate("power")
    print(f"[OK] Retrieved power intermediate: {power.shape}")

    # Create measurement result
    measurement = tk.MeasurementResult(value=3.3, units="V", method="peak_to_peak")
    print(f"[OK] MeasurementResult: {measurement}")


def demo_algorithm_registry() -> None:
    """Demonstrate API-006: Algorithm Registry."""
    print("\n" + "=" * 60)
    print("API-006: Algorithm Registry Demo")
    print("=" * 60)

    # Register custom algorithm
    def custom_peak_finder(data, threshold=0.5) -> None:
        """Simple peak finder."""
        peaks = []
        for i in range(1, len(data) - 1):
            if data[i] > threshold and data[i] > data[i - 1] and data[i] > data[i + 1]:
                peaks.append(i)
        return peaks

    tk.register_algorithm("simple_peaks", custom_peak_finder, category="peak_finder")

    print("[OK] Registered 'simple_peaks' algorithm")

    # Retrieve and use algorithm
    peak_finder = tk.get_algorithm("peak_finder", "simple_peaks")
    data = np.array([0, 1, 0, 2, 0, 3, 0])
    peaks = peak_finder(data, threshold=0.5)
    print(f"[OK] Found peaks at indices: {peaks}")

    # List algorithms
    available = tk.get_algorithms("peak_finder")
    print(f"[OK] Available peak finders: {available}")


def demo_plugin_architecture() -> None:
    """Demonstrate API-007: Plugin Architecture."""
    print("\n" + "=" * 60)
    print("API-007: Plugin Architecture Demo")
    print("=" * 60)

    # List available plugins
    plugins = tk.list_plugins()
    print(f"[OK] Plugin groups: {list(plugins.keys())}")

    for group, plugin_list in plugins.items():
        if plugin_list:
            print(f"[OK] {group}: {plugin_list}")
        else:
            print(f"[OK] {group}: (no plugins installed)")

    # Get plugin manager
    manager = tk.get_plugin_manager()
    print(f"[OK] Plugin manager: {manager}")


def demo_custom_measurements() -> None:
    """Demonstrate API-008: Custom Measurements."""
    print("\n" + "=" * 60)
    print("API-008: Custom Measurements Demo")
    print("=" * 60)

    # Register custom measurement
    def crest_factor(trace, **kwargs) -> None:
        """Calculate crest factor: peak / RMS."""
        peak = abs(trace.data).max()
        rms = np.sqrt((trace.data**2).mean())
        return peak / rms

    tk.register_measurement(
        name="crest_factor",
        func=crest_factor,
        units="ratio",
        category="amplitude",
        description="Crest factor (peak/RMS)",
        tags=["amplitude", "quality"],
    )

    print("[OK] Registered 'crest_factor' measurement")

    # Use custom measurement
    data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    trace = tk.WaveformTrace(data=data, metadata=tk.TraceMetadata(sample_rate=1e6))

    cf = tk.measure_custom(trace, "crest_factor")
    print(f"[OK] Crest factor: {cf:.3f}")

    # List measurements
    measurements = tk.list_measurements()
    print(f"[OK] Total registered measurements: {len(measurements)}")

    # Get metadata
    registry = tk.get_measurement_registry()
    metadata = registry.get_metadata("crest_factor")
    print(f"[OK] Metadata: {metadata}")


def main() -> None:
    """Run all Expert API demonstrations."""
    print("\n" + "=" * 60)
    print("TraceKit Expert API Demonstration")
    print("Demonstrating all 8 CRITICAL Tier 1 APIs")
    print("=" * 60)

    try:
        demo_pipeline_api()
        demo_composition_api()
        demo_streaming_api()
        demo_transformer_base()
        demo_results_api()
        demo_algorithm_registry()
        demo_plugin_architecture()
        demo_custom_measurements()

        print("\n" + "=" * 60)
        print("[OK] All Expert API demonstrations completed successfully!")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n[!!] Error during demonstration: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
