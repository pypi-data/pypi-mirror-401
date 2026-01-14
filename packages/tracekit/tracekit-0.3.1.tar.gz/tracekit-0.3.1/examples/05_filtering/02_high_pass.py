#!/usr/bin/env python3
"""Example 02: High-Pass Filtering and DC Removal.

Demonstrates high-pass filtering to remove low-frequency content
including DC offset and slow drift.

Key Concepts:
- DC offset removal
- Drift elimination
- Baseline correction
- AC coupling emulation

Expected Output:
- DC removal demonstration
- Drift correction results
- High-pass filter characteristics

Run:
    uv run python examples/05_filtering/02_high_pass.py
"""

import numpy as np

from tracekit.core.types import TraceMetadata, WaveformTrace
from tracekit.filtering import HighPassFilter, high_pass


def main() -> None:
    """Demonstrate high-pass filtering techniques."""
    print("=" * 60)
    print("TraceKit Example: High-Pass Filtering")
    print("=" * 60)

    # --- Overview ---
    print("\n--- High-Pass Filter Overview ---")
    print("High-pass filters attenuate frequencies below the cutoff.")
    print("Use cases:")
    print("  - Remove DC offset from AC signals")
    print("  - Eliminate slow drift in measurements")
    print("  - Baseline correction")
    print("  - Emulate AC coupling")
    print("  - Extract fast transients from slow background")

    # --- DC Offset Removal ---
    print("\n--- Example 1: DC Offset Removal ---")
    sample_rate = 100e3  # 100 kHz (lower to avoid numerical issues with low cutoffs)
    duration = 100e-3  # 100 ms
    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate

    # Signal with DC offset
    dc_offset = 2.5  # 2.5V DC offset
    ac_signal = 0.5 * np.sin(2 * np.pi * 1e3 * t)  # 1 kHz AC
    signal_with_dc = ac_signal + dc_offset

    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="dc_coupled")
    trace = WaveformTrace(data=signal_with_dc, metadata=metadata)

    print(f"Original signal mean (DC): {np.mean(signal_with_dc):.3f} V")
    print(f"Original signal AC RMS: {np.std(signal_with_dc):.3f} V")

    # High-pass filter to remove DC
    filtered = high_pass(trace, cutoff=100)  # 100 Hz cutoff

    print("\nAfter high-pass (100 Hz cutoff):")
    print(f"  Mean (DC): {np.mean(filtered.data):.6f} V (removed)")  # type: ignore[union-attr]
    print(f"  AC RMS: {np.std(filtered.data):.3f} V (preserved)")  # type: ignore[union-attr]

    # --- Drift Elimination ---
    print("\n--- Example 2: Drift Elimination ---")

    # Create signal with slow drift
    drift = 0.01 * t * sample_rate / n_samples  # Linear drift
    ac_signal_2 = 0.3 * np.sin(2 * np.pi * 500 * t)  # 500 Hz
    drifting_signal = ac_signal_2 + drift

    trace_drift = WaveformTrace(
        data=drifting_signal, metadata=TraceMetadata(sample_rate=sample_rate)
    )

    print(f"Original: starts at {drifting_signal[0]:.3f}, ends at {drifting_signal[-1]:.3f}")

    # Remove drift with high-pass (use lower order to avoid instability)
    stable = high_pass(trace_drift, cutoff=50, order=2)  # 50 Hz removes drift

    print(f"Filtered: starts at {stable.data[100]:.3f}, ends at {stable.data[-100]:.3f}")
    print(f"Drift removed: {abs(drifting_signal[-1] - drifting_signal[0]):.3f} V")

    # --- Using Filter Object ---
    print("\n--- Using HighPassFilter Object ---")

    hpf = HighPassFilter(
        cutoff=100,
        sample_rate=sample_rate,
        order=4,
        filter_type="butterworth",
    )

    filtered_obj = hpf.apply(trace)

    print("Filter: Butterworth, 4th order")
    print("Cutoff: 100 Hz")
    print(
        f"DC attenuation: {-20 * np.log10(abs(np.mean(filtered_obj.data) / dc_offset + 1e-10)):.1f} dB"  # type: ignore[union-attr]
    )

    # --- Frequency Response ---
    print("\n--- Filter Frequency Response ---")
    freqs, response = hpf.get_frequency_response(worN=1000)
    response_db = 20 * np.log10(np.abs(response) + 1e-10)

    # Convert normalized frequency to Hz
    if hpf.sample_rate:
        freqs = freqs * hpf.sample_rate / (2 * np.pi)

    # Show attenuation at key frequencies
    key_freqs = [1, 10, 50, 100, 500, 1000]
    print(f"{'Frequency':<12} {'Attenuation'}")
    print("-" * 25)

    for f in key_freqs:
        idx = np.argmin(np.abs(freqs - f))
        print(f"{f:>8} Hz   {response_db[idx]:>6.1f} dB")

    # --- AC Coupling Emulation ---
    print("\n--- Example 3: AC Coupling Emulation ---")

    # Typical oscilloscope AC coupling: ~50 Hz cutoff (adjusted for sample rate)
    ac_coupled = high_pass(trace, cutoff=50, order=2)

    print("AC coupling settings:")
    print("  Cutoff: 50 Hz")
    print("  Order: 2 (simple RC equivalent)")
    print(f"  Original DC: {np.mean(signal_with_dc):.3f} V")
    print(f"  After AC coupling: {np.mean(ac_coupled.data):.4f} V")

    # --- Baseline Correction ---
    print("\n--- Example 4: Baseline Correction ---")

    # Create signal with wandering baseline
    np.random.seed(42)
    baseline_wander = 0.2 * np.sin(2 * np.pi * 0.5 * t)  # 0.5 Hz wander
    pulse_signal = np.zeros(n_samples)

    # Add pulses
    pulse_positions = np.random.randint(0, n_samples, 20)
    for pos in pulse_positions:
        if pos + 100 < n_samples:
            pulse_signal[pos : pos + 100] = 1.0

    contaminated_pulses = pulse_signal + baseline_wander

    trace_baseline = WaveformTrace(
        data=contaminated_pulses, metadata=TraceMetadata(sample_rate=sample_rate)
    )

    # Correct baseline
    corrected = high_pass(trace_baseline, cutoff=20, order=2)

    print("Baseline wander frequency: 0.5 Hz")
    print("High-pass cutoff: 20 Hz")
    print(f"Baseline variation before: {np.std(baseline_wander):.4f} V")
    print(f"After correction (first 1000): {np.std(corrected.data[:1000]):.4f} V")

    # --- Different Filter Orders ---
    print("\n--- Effect of Filter Order on Settling ---")
    print(f"{'Order':<8} {'Settling Time':<15} {'DC Attenuation'}")
    print("-" * 40)

    for order in [1, 2, 4, 6]:
        hpf_test = HighPassFilter(cutoff=100, sample_rate=sample_rate, order=order)
        filtered_test = hpf_test.apply(trace)

        # Estimate settling time (when signal is within 5% of final)
        final_mean = np.mean(filtered_test.data[-1000:])  # type: ignore[union-attr]
        threshold = 0.05 * np.std(filtered_test.data)  # type: ignore[union-attr]
        settling_idx = 0
        for i in range(len(filtered_test.data)):  # type: ignore[union-attr]
            if abs(filtered_test.data[i] - final_mean) < threshold + np.std(ac_signal):  # type: ignore[union-attr]
                settling_idx = i
                break

        settling_time = settling_idx / sample_rate * 1000  # ms
        dc_atten = -20 * np.log10(abs(np.mean(filtered_test.data[-1000:]) / dc_offset + 1e-10))  # type: ignore[union-attr]

        print(f"{order:<8} {settling_time:>8.2f} ms      {dc_atten:>6.1f} dB")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. high_pass() removes DC offset and low-frequency content")
    print("  2. Lower cutoff = preserves more low-frequency signal")
    print("  3. Higher order = sharper transition but longer settling")
    print("  4. Use lower order (2) for very low cutoffs to avoid instability")
    print("  5. Use for baseline correction and drift removal")
    print("  6. Sample rate vs cutoff ratio should be >1000 for stability")
    print("=" * 60)


if __name__ == "__main__":
    main()
