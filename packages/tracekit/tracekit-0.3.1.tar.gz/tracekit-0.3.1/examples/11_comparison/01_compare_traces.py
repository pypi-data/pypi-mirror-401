#!/usr/bin/env python3
"""Example 01: Comparing Traces.

Demonstrates comparing two waveform traces to quantify their
similarity and identify differences.

Key Concepts:
- Correlation coefficient
- Difference trace
- Similarity score
- Point-by-point comparison

Expected Output:
- Correlation metrics
- Difference statistics
- Similarity assessment

Run:
    uv run python examples/11_comparison/01_compare_traces.py
"""

import numpy as np

import tracekit as tk
from tracekit.core.types import TraceMetadata, WaveformTrace


def main() -> None:
    """Demonstrate trace comparison capabilities."""
    print("=" * 60)
    print("TraceKit Example: Comparing Traces")
    print("=" * 60)

    # Create test signals
    sample_rate = 1e6
    duration = 10e-3
    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate
    metadata = TraceMetadata(sample_rate=sample_rate)

    # Reference signal
    freq = 1000
    reference = np.sin(2 * np.pi * freq * t)
    trace_ref = WaveformTrace(data=reference, metadata=metadata)

    # --- Identical Signals ---
    print("\n--- Identical Signals ---")

    identical = reference.copy()
    trace_identical = WaveformTrace(data=identical, metadata=metadata)

    # correlation returns (lags, correlation_values)
    lags, corr_values = tk.correlation(trace_ref, trace_identical)
    # Get peak correlation value
    peak_corr = np.max(np.abs(corr_values))
    sim = tk.similarity_score(trace_ref, trace_identical)

    print(f"Peak Correlation: {peak_corr:.6f}")
    print(f"Similarity: {sim:.6f}")
    print("(Both should be 1.0 for identical signals)")

    # --- Signal with Noise ---
    print("\n--- Signal with Added Noise ---")

    noise_levels = [0.01, 0.1, 0.5, 1.0]
    print(f"{'Noise RMS':<12} {'Correlation':<15} {'Similarity'}")
    print("-" * 45)

    for noise_rms in noise_levels:
        noisy = reference + np.random.randn(n_samples) * noise_rms
        trace_noisy = WaveformTrace(data=noisy, metadata=metadata)

        lags, corr_values = tk.correlation(trace_ref, trace_noisy)
        peak_corr = np.max(np.abs(corr_values))
        sim = tk.similarity_score(trace_ref, trace_noisy)

        print(f"{noise_rms:<12.2f} {peak_corr:<15.4f} {sim:.4f}")

    # --- Signal with Amplitude Change ---
    print("\n--- Amplitude Variations ---")

    print(f"{'Amplitude':<12} {'Correlation':<15} {'Similarity'}")
    print("-" * 45)

    for amp_factor in [0.5, 0.9, 1.0, 1.1, 2.0]:
        scaled = reference * amp_factor
        trace_scaled = WaveformTrace(data=scaled, metadata=metadata)

        lags, corr_values = tk.correlation(trace_ref, trace_scaled)
        peak_corr = np.max(np.abs(corr_values))
        sim = tk.similarity_score(trace_ref, trace_scaled)

        print(f"{amp_factor:<12.1f} {peak_corr:<15.4f} {sim:.4f}")

    print("Note: Correlation ignores amplitude, similarity considers it")

    # --- Signal with DC Offset ---
    print("\n--- DC Offset ---")

    print(f"{'DC Offset':<12} {'Correlation':<15} {'Similarity'}")
    print("-" * 45)

    for offset in [-1.0, -0.5, 0, 0.5, 1.0]:
        shifted = reference + offset
        trace_shifted = WaveformTrace(data=shifted, metadata=metadata)

        lags, corr_values = tk.correlation(trace_ref, trace_shifted)
        peak_corr = np.max(np.abs(corr_values))
        sim = tk.similarity_score(trace_ref, trace_shifted)

        print(f"{offset:<12.1f} {peak_corr:<15.4f} {sim:.4f}")

    print("Note: Correlation is invariant to DC offset")

    # --- Phase Shift ---
    print("\n--- Phase Shift ---")

    print(f"{'Phase (deg)':<12} {'Correlation':<15} {'Similarity'}")
    print("-" * 45)

    for phase_deg in [0, 15, 45, 90, 180]:
        phase_rad = np.deg2rad(phase_deg)
        shifted = np.sin(2 * np.pi * freq * t + phase_rad)
        trace_shifted = WaveformTrace(data=shifted, metadata=metadata)

        lags, corr_values = tk.correlation(trace_ref, trace_shifted)
        peak_corr = np.max(np.abs(corr_values))
        sim = tk.similarity_score(trace_ref, trace_shifted)

        print(f"{phase_deg:<12.0f} {peak_corr:<15.4f} {sim:.4f}")

    # --- Difference Trace ---
    print("\n--- Difference Trace ---")

    # Create two slightly different signals
    signal_a = reference
    signal_b = reference + 0.1 * np.sin(2 * np.pi * 3 * freq * t)  # Add harmonic

    trace_a = WaveformTrace(data=signal_a, metadata=metadata)
    trace_b = WaveformTrace(data=signal_b, metadata=metadata)

    diff = tk.difference(trace_a, trace_b)

    print("Signal A: Pure 1 kHz sine")
    print("Signal B: 1 kHz sine + 3rd harmonic (10%)")
    print("Difference trace statistics:")
    print(f"  Mean: {np.mean(diff.data):.6f}")
    print(f"  RMS: {np.sqrt(np.mean(diff.data**2)):.4f}")
    print(f"  Peak: {np.max(np.abs(diff.data)):.4f}")
    lags_ab, corr_ab = tk.correlation(trace_a, trace_b)
    peak_corr_ab = np.max(np.abs(corr_ab))
    print(f"  Correlation A-B: {peak_corr_ab:.4f}")

    # --- Compare Results ---
    print("\n--- Full Comparison ---")

    comparison = tk.compare_traces(trace_a, trace_b)

    print("Comparison results:")
    print(f"  Match: {comparison.match}")
    print(f"  Similarity: {comparison.similarity:.4f}")
    print(f"  Max difference: {comparison.max_difference:.4f}")
    print(f"  RMS difference: {comparison.rms_difference:.4f}")
    print(f"  Correlation: {comparison.correlation:.4f}")
    if comparison.violations is not None:
        print(f"  Violations: {len(comparison.violations)}")

    # --- Practical Example: Before/After Comparison ---
    print("\n--- Practical: Before/After Fix ---")

    # "Before" - signal with glitch
    before = reference.copy()
    glitch_start = n_samples // 3
    glitch_width = 50
    before[glitch_start : glitch_start + glitch_width] = 2.0  # Glitch

    # "After" - clean signal
    after = reference.copy()

    trace_before = WaveformTrace(data=before, metadata=metadata)
    trace_after = WaveformTrace(data=after, metadata=metadata)

    # Compare to reference
    print("Comparing to reference:")
    _, corr_before = tk.correlation(trace_ref, trace_before)
    _, corr_after = tk.correlation(trace_ref, trace_after)
    print(f"  Before fix - Correlation: {np.max(np.abs(corr_before)):.4f}")
    print(f"  After fix - Correlation: {np.max(np.abs(corr_after)):.4f}")

    # Compare before vs after
    print("\nBefore vs After:")
    _, corr_ba = tk.correlation(trace_before, trace_after)
    print(f"  Correlation: {np.max(np.abs(corr_ba)):.4f}")
    print(f"  Similarity: {tk.similarity_score(trace_before, trace_after):.4f}")

    # Find where they differ
    diff_ba = tk.difference(trace_before, trace_after)
    diff_threshold = 0.1
    diff_regions = np.where(np.abs(diff_ba.data) > diff_threshold)[0]

    if len(diff_regions) > 0:
        print(f"\nDifferences > {diff_threshold} found at:")
        print(f"  Sample range: {diff_regions[0]} to {diff_regions[-1]}")
        print(
            f"  Time range: {diff_regions[0] / sample_rate * 1e6:.1f} us to {diff_regions[-1] / sample_rate * 1e6:.1f} us"
        )
        print(f"  Max difference: {np.max(np.abs(diff_ba.data)):.2f}")

    # --- Batch Comparison ---
    print("\n--- Batch Comparison ---")
    print("Comparing multiple captures against reference")

    # Simulate multiple captures
    captures = []
    for i in range(5):
        noise = np.random.randn(n_samples) * 0.05
        drift = i * 0.02  # Progressive drift
        capture = reference + noise + drift
        captures.append(WaveformTrace(data=capture, metadata=metadata))

    print(f"{'Capture':<10} {'Correlation':<15} {'Similarity':<15} {'Status'}")
    print("-" * 55)

    for i, capture in enumerate(captures):
        _, corr_values = tk.correlation(trace_ref, capture)
        peak_corr = np.max(np.abs(corr_values))
        sim = tk.similarity_score(trace_ref, capture)
        status = "PASS" if peak_corr > 0.99 else "WARN" if peak_corr > 0.95 else "FAIL"
        print(f"#{i + 1:<9} {peak_corr:<15.4f} {sim:<15.4f} {status}")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. correlation() measures shape similarity (ignores amplitude)")
    print("  2. similarity_score() considers both shape and magnitude")
    print("  3. difference() computes point-by-point subtraction")
    print("  4. compare_traces() provides comprehensive comparison")
    print("  5. Use correlation for shape matching")
    print("  6. Use similarity for production testing")
    print("=" * 60)


if __name__ == "__main__":
    main()
