#!/usr/bin/env python3
"""Example 03: Band-Pass and Band-Stop Filtering.

Demonstrates band-pass filtering to isolate specific frequency ranges
and band-stop (notch) filtering to remove interference.

Key Concepts:
- Band-pass for frequency isolation
- Band-stop for interference removal
- Notch filters for narrow bands
- Center frequency and bandwidth

Expected Output:
- Frequency band isolation
- Interference removal examples
- Filter characteristics comparison

Run:
    uv run python examples/05_filtering/03_band_filters.py
"""

import numpy as np

from tracekit.core.types import TraceMetadata, WaveformTrace
from tracekit.filtering import BandPassFilter, band_pass, band_stop, notch_filter


def main() -> None:
    """Demonstrate band-pass and band-stop filtering."""
    print("=" * 60)
    print("TraceKit Example: Band-Pass and Band-Stop Filtering")
    print("=" * 60)

    # --- Overview ---
    print("\n--- Band Filter Overview ---")
    print("Band-pass: Passes frequencies within a range, attenuates others")
    print("Band-stop: Blocks frequencies within a range, passes others")
    print("Notch: Narrow band-stop for specific frequency removal")
    print("\nUse cases:")
    print("  Band-pass: Isolate signal of interest")
    print("  Band-stop: Remove interference band")
    print("  Notch: Remove power line hum (50/60 Hz)")

    # Create test signal
    sample_rate = 100e3  # 100 kHz
    duration = 100e-3  # 100 ms
    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate

    # --- Band-Pass Filtering ---
    print("\n--- Band-Pass Filtering ---")

    # Signal: Multiple frequency components
    signal_1k = 1.0 * np.sin(2 * np.pi * 1000 * t)  # 1 kHz (target)
    signal_100 = 0.5 * np.sin(2 * np.pi * 100 * t)  # 100 Hz (low)
    signal_10k = 0.3 * np.sin(2 * np.pi * 10000 * t)  # 10 kHz (high)
    composite = signal_1k + signal_100 + signal_10k

    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="composite")
    trace = WaveformTrace(data=composite, metadata=metadata)

    print("Input signal components:")
    print("  100 Hz: 0.5 V amplitude")
    print("  1 kHz:  1.0 V amplitude (target)")
    print("  10 kHz: 0.3 V amplitude")

    # Band-pass to isolate 1 kHz
    filtered = band_pass(trace, low=500, high=2000)

    # Measure component magnitudes after filtering
    from numpy.fft import rfft, rfftfreq

    freqs = rfftfreq(n_samples, 1 / sample_rate)
    fft_original = np.abs(rfft(composite))
    fft_filtered = np.abs(rfft(filtered.data))

    # Find peaks at component frequencies
    idx_100 = np.argmin(np.abs(freqs - 100))
    idx_1k = np.argmin(np.abs(freqs - 1000))
    idx_10k = np.argmin(np.abs(freqs - 10000))

    print("\nBand-pass: 500 Hz - 2 kHz")
    print(f"{'Component':<12} {'Before':<12} {'After':<12} {'Attenuation'}")
    print("-" * 48)
    print(
        f"{'100 Hz':<12} {fft_original[idx_100]:.1f}{'':>6} {fft_filtered[idx_100]:.1f}{'':>6} {20 * np.log10(fft_filtered[idx_100] / fft_original[idx_100] + 1e-10):.1f} dB"
    )
    print(
        f"{'1 kHz':<12} {fft_original[idx_1k]:.1f}{'':>6} {fft_filtered[idx_1k]:.1f}{'':>6} {20 * np.log10(fft_filtered[idx_1k] / fft_original[idx_1k] + 1e-10):.1f} dB"
    )
    print(
        f"{'10 kHz':<12} {fft_original[idx_10k]:.1f}{'':>6} {fft_filtered[idx_10k]:.1f}{'':>6} {20 * np.log10(fft_filtered[idx_10k] / fft_original[idx_10k] + 1e-10):.1f} dB"
    )

    # --- Using BandPassFilter Object ---
    print("\n--- BandPassFilter Object ---")

    bpf = BandPassFilter(
        low=500,
        high=2000,
        sample_rate=sample_rate,
        order=4,
    )

    low_freq, high_freq = bpf.passband
    center_freq = (low_freq + high_freq) / 2
    bandwidth = high_freq - low_freq
    q_factor = center_freq / bandwidth if bandwidth > 0 else 0

    print(f"Center frequency: {center_freq:.0f} Hz")
    print(f"Bandwidth: {bandwidth:.0f} Hz")
    print(f"Q factor: {q_factor:.2f}")

    # --- Band-Stop Filtering ---
    print("\n--- Band-Stop Filtering ---")

    # Scenario: Remove interference band
    signal = 1.0 * np.sin(2 * np.pi * 1000 * t)  # Desired signal
    interference = 0.8 * np.sin(2 * np.pi * 5000 * t)  # Interference
    contaminated = signal + interference

    trace_bs = WaveformTrace(data=contaminated, metadata=TraceMetadata(sample_rate=sample_rate))

    print("Input: 1 kHz signal + 5 kHz interference")

    # Band-stop to remove 5 kHz
    cleaned = band_stop(trace_bs, low=4000, high=6000)

    # Measure effectiveness
    fft_contam = np.abs(rfft(contaminated))
    fft_cleaned = np.abs(rfft(cleaned.data))
    idx_5k = np.argmin(np.abs(freqs - 5000))

    print("\nBand-stop: 4 kHz - 6 kHz")
    print("Interference at 5 kHz:")
    print(f"  Before: {fft_contam[idx_5k]:.1f}")
    print(f"  After:  {fft_cleaned[idx_5k]:.1f}")
    print(f"  Reduction: {20 * np.log10(fft_cleaned[idx_5k] / fft_contam[idx_5k] + 1e-10):.1f} dB")

    # --- Notch Filter ---
    print("\n--- Notch Filter (Narrow Band-Stop) ---")

    # Scenario: Remove 60 Hz power line hum
    sample_rate_2 = 10e3  # 10 kHz
    n_2 = int(sample_rate_2 * 0.5)  # 0.5 seconds
    t2 = np.arange(n_2) / sample_rate_2

    ecg_like = np.sin(2 * np.pi * 1.5 * t2)  # 1.5 Hz heartbeat
    hum_60 = 0.3 * np.sin(2 * np.pi * 60 * t2)  # 60 Hz hum
    hum_120 = 0.15 * np.sin(2 * np.pi * 120 * t2)  # 120 Hz harmonic
    noisy_ecg = ecg_like + hum_60 + hum_120

    trace_ecg = WaveformTrace(data=noisy_ecg, metadata=TraceMetadata(sample_rate=sample_rate_2))

    print("Input: ECG-like signal with 60 Hz + 120 Hz hum")

    # Apply notch filters
    cleaned_60 = notch_filter(trace_ecg, freq=60, q_factor=30)
    cleaned_both = notch_filter(cleaned_60, freq=120, q_factor=30)

    # Measure hum reduction
    freqs_2 = rfftfreq(n_2, 1 / sample_rate_2)
    fft_noisy = np.abs(rfft(noisy_ecg))
    fft_clean = np.abs(rfft(cleaned_both.data))

    idx_60 = np.argmin(np.abs(freqs_2 - 60))
    idx_120 = np.argmin(np.abs(freqs_2 - 120))

    print("\nNotch filters: 60 Hz (Q=30), 120 Hz (Q=30)")
    print(f"{'Frequency':<12} {'Before':<10} {'After':<10} {'Reduction'}")
    print("-" * 45)
    print(
        f"{'60 Hz':<12} {fft_noisy[idx_60]:.2f}{'':>4} {fft_clean[idx_60]:.2f}{'':>4} {20 * np.log10(fft_clean[idx_60] / fft_noisy[idx_60] + 1e-10):.1f} dB"
    )
    print(
        f"{'120 Hz':<12} {fft_noisy[idx_120]:.2f}{'':>4} {fft_clean[idx_120]:.2f}{'':>4} {20 * np.log10(fft_clean[idx_120] / fft_noisy[idx_120] + 1e-10):.1f} dB"
    )

    # --- Q Factor Effect ---
    print("\n--- Notch Filter Q Factor ---")
    print("Q = center_freq / bandwidth")
    print("Higher Q = narrower notch, less signal distortion")
    print()
    print(f"{'Q Factor':<10} {'Bandwidth':<12} {'60 Hz Atten':<15} {'50 Hz Atten'}")
    print("-" * 55)

    for q in [5, 10, 30, 50]:
        notched = notch_filter(trace_ecg, freq=60, q_factor=q)
        fft_n = np.abs(rfft(notched.data))
        bandwidth = 60 / q

        idx_50 = np.argmin(np.abs(freqs_2 - 50))
        atten_60 = 20 * np.log10(fft_n[idx_60] / fft_noisy[idx_60] + 1e-10)
        atten_50 = 20 * np.log10(fft_n[idx_50] / fft_noisy[idx_50] + 1e-10)

        print(f"Q={q:<8} {bandwidth:>6.1f} Hz     {atten_60:>6.1f} dB       {atten_50:>6.1f} dB")

    # --- Radio Frequency Isolation ---
    print("\n--- Example: RF Signal Isolation ---")

    # Simulate baseband signal extraction
    sample_rate_rf = 1e6  # 1 MHz
    n_rf = int(sample_rate_rf * 10e-3)  # 10 ms
    t_rf = np.arange(n_rf) / sample_rate_rf

    # Multiple radio signals
    signal_100k = np.sin(2 * np.pi * 100e3 * t_rf)  # 100 kHz
    signal_150k = 0.7 * np.sin(2 * np.pi * 150e3 * t_rf)  # 150 kHz (target)
    signal_200k = 0.5 * np.sin(2 * np.pi * 200e3 * t_rf)  # 200 kHz
    rf_composite = signal_100k + signal_150k + signal_200k

    trace_rf = WaveformTrace(data=rf_composite, metadata=TraceMetadata(sample_rate=sample_rate_rf))

    # Isolate 150 kHz with narrow band-pass
    isolated = band_pass(trace_rf, low=140e3, high=160e3, order=6)

    freqs_rf = rfftfreq(n_rf, 1 / sample_rate_rf)
    fft_rf = np.abs(rfft(rf_composite))
    fft_iso = np.abs(rfft(isolated.data))

    idx_100k = np.argmin(np.abs(freqs_rf - 100e3))
    idx_150k = np.argmin(np.abs(freqs_rf - 150e3))
    idx_200k = np.argmin(np.abs(freqs_rf - 200e3))

    print("RF composite: 100 kHz + 150 kHz + 200 kHz")
    print("Band-pass: 140-160 kHz (isolate 150 kHz)")
    print()
    print(f"{'Channel':<12} {'Isolation'}")
    print("-" * 25)
    print(f"{'100 kHz':<12} {20 * np.log10(fft_iso[idx_100k] / fft_rf[idx_100k] + 1e-10):.1f} dB")
    print(f"{'150 kHz':<12} {20 * np.log10(fft_iso[idx_150k] / fft_rf[idx_150k] + 1e-10):.1f} dB")
    print(f"{'200 kHz':<12} {20 * np.log10(fft_iso[idx_200k] / fft_rf[idx_200k] + 1e-10):.1f} dB")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. Band-pass isolates frequency range of interest")
    print("  2. Band-stop removes interference band")
    print("  3. Notch filter removes single frequency (narrow band-stop)")
    print("  4. Q factor controls notch width (higher = narrower)")
    print("  5. Higher order = sharper transition, more ringing")
    print("  6. Use cascaded notches for harmonics (60 Hz, 120 Hz, etc.)")
    print("=" * 60)


if __name__ == "__main__":
    main()
