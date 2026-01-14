#!/usr/bin/env python3
"""Example 01: Low-Pass Filtering Basics.

Demonstrates low-pass filtering to remove high-frequency noise while
preserving the signal of interest.

Key Concepts:
- Cutoff frequency selection
- Filter order and rolloff
- Butterworth vs other filter types
- Effect on time domain signal

Expected Output:
- Original vs filtered signal comparison
- Noise reduction metrics
- Frequency response visualization

Run:
    uv run python examples/05_filtering/01_low_pass.py
"""

import numpy as np

from tracekit.core.types import TraceMetadata, WaveformTrace
from tracekit.filtering import LowPassFilter, low_pass


def main() -> None:
    """Demonstrate low-pass filtering techniques."""
    print("=" * 60)
    print("TraceKit Example: Low-Pass Filtering")
    print("=" * 60)

    # --- Overview ---
    print("\n--- Low-Pass Filter Overview ---")
    print("Low-pass filters attenuate frequencies above the cutoff.")
    print("Use cases:")
    print("  - Remove high-frequency noise from measurements")
    print("  - Anti-aliasing before downsampling")
    print("  - Smooth noisy sensor data")
    print("  - Extract DC component or slow trends")

    # --- Create Test Signal ---
    print("\n--- Creating Test Signal ---")
    sample_rate = 10e6  # 10 MHz
    duration = 1e-3  # 1 ms
    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate

    # Signal: 10 kHz sine with high-frequency noise
    signal_freq = 10e3  # 10 kHz
    noise_freq = 500e3  # 500 kHz noise
    signal = np.sin(2 * np.pi * signal_freq * t)
    noise = 0.3 * np.sin(2 * np.pi * noise_freq * t)
    noisy_signal = signal + noise + np.random.randn(n_samples) * 0.1

    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="noisy_signal")
    trace = WaveformTrace(data=noisy_signal, metadata=metadata)

    print(f"Signal frequency: {signal_freq / 1e3:.0f} kHz")
    print(f"Noise frequency: {noise_freq / 1e3:.0f} kHz")
    print(f"Sample rate: {sample_rate / 1e6:.0f} MHz")
    print(f"Samples: {n_samples:,}")

    # --- Simple Low-Pass (Convenience Function) ---
    print("\n--- Method 1: Convenience Function ---")
    filtered_trace = low_pass(trace, cutoff=50e3)  # 50 kHz cutoff

    print("Cutoff frequency: 50 kHz")
    print(f"Original RMS: {np.sqrt(np.mean(noisy_signal**2)):.4f}")
    print(f"Filtered RMS: {np.sqrt(np.mean(filtered_trace.data**2)):.4f}")  # type: ignore[union-attr]

    # Calculate noise reduction
    noise_original = np.std(noisy_signal - signal)
    noise_filtered = np.std(filtered_trace.data - signal)  # type: ignore[union-attr]
    reduction_db = 20 * np.log10(noise_original / noise_filtered)
    print(f"Noise reduction: {reduction_db:.1f} dB")

    # --- Using Filter Object ---
    print("\n--- Method 2: Filter Object (More Control) ---")

    # Create Butterworth low-pass filter
    lpf = LowPassFilter(
        cutoff=50e3,
        sample_rate=sample_rate,
        order=4,  # 4th order = 24 dB/octave rolloff
        filter_type="butterworth",
    )

    # Apply filter
    filtered2 = lpf.apply(trace)

    print("Filter type: Butterworth")
    print("Order: 4 (24 dB/octave)")
    print("Cutoff: 50 kHz")

    # Get frequency response
    freqs, response = lpf.get_frequency_response(worN=1000)

    # Convert normalized frequency to Hz
    if lpf.sample_rate:
        freqs_hz = freqs * lpf.sample_rate / (2 * np.pi)
    else:
        freqs_hz = freqs

    # Find -3dB point
    response_db = 20 * np.log10(np.abs(response) + 1e-10)
    idx_3db = np.argmin(np.abs(response_db + 3))
    print(f"Actual -3dB frequency: {freqs_hz[idx_3db] / 1e3:.1f} kHz")

    # --- Different Filter Orders ---
    print("\n--- Effect of Filter Order ---")
    print(f"{'Order':<8} {'Rolloff':<15} {'Delay':<12} {'Noise Reduction'}")
    print("-" * 50)

    for order in [2, 4, 6, 8]:
        lpf_test = LowPassFilter(
            cutoff=50e3,
            sample_rate=sample_rate,
            order=order,
            filter_type="butterworth",
        )
        filtered_test = lpf_test.apply(trace)

        # Calculate metrics
        noise_test = np.std(filtered_test.data - signal)  # type: ignore[union-attr]
        reduction = 20 * np.log10(noise_original / noise_test)

        rolloff = f"{order * 6} dB/oct"
        delay = f"{order * 2} samples"  # Approximate

        print(f"{order:<8} {rolloff:<15} {delay:<12} {reduction:.1f} dB")

    # --- Different Filter Types ---
    print("\n--- Different Filter Types ---")
    print(f"{'Type':<15} {'Passband':<15} {'Transition':<15} {'Phase'}")
    print("-" * 60)

    filter_types = [
        ("butterworth", "Maximally flat", "Moderate", "Nonlinear"),
        ("chebyshev1", "Ripple", "Sharp", "Nonlinear"),
        ("chebyshev2", "Flat", "Sharp", "Nonlinear"),
        ("bessel", "Flat", "Gradual", "Linear-ish"),
    ]

    for ftype, passband, transition, phase in filter_types:
        print(f"{ftype:<15} {passband:<15} {transition:<15} {phase}")

    # --- Practical Example: Remove 60 Hz Harmonics ---
    print("\n--- Practical: Power Line Noise Removal ---")

    # Create signal with 60 Hz harmonics
    t2 = np.arange(10000) / 10e3  # 10 kHz sample rate
    clean = np.sin(2 * np.pi * 100 * t2)  # 100 Hz signal
    power_noise = 0.2 * np.sin(2 * np.pi * 60 * t2)  # 60 Hz
    power_noise += 0.1 * np.sin(2 * np.pi * 120 * t2)  # 120 Hz
    contaminated = clean + power_noise

    meta2 = TraceMetadata(sample_rate=10e3)
    trace2 = WaveformTrace(data=contaminated, metadata=meta2)

    # Use low-pass to remove content above 150 Hz
    filtered_power = low_pass(trace2, cutoff=150)

    noise_before = np.std(contaminated - clean)
    noise_after = np.std(filtered_power.data - clean)  # type: ignore[union-attr]

    print("Signal: 100 Hz, Noise: 60 Hz + 120 Hz")
    print("Low-pass cutoff: 150 Hz")
    print(f"Noise reduction: {20 * np.log10(noise_before / noise_after):.1f} dB")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. low_pass() is the simplest way to filter")
    print("  2. LowPassFilter provides more control (order, type)")
    print("  3. Higher order = sharper rolloff but more delay")
    print("  4. Butterworth is best for general use (flat passband)")
    print("  5. Bessel preserves pulse shape (linear phase)")
    print("=" * 60)


if __name__ == "__main__":
    main()
