#!/usr/bin/env python3
"""Example: FFT Basics.

This example demonstrates fundamental FFT (Fast Fourier Transform)
analysis for frequency-domain signal analysis.

Time: 10 minutes
Prerequisites: Basic measurements

Run:
    uv run python examples/03_spectral_analysis/01_fft_basics.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import numpy as np

import tracekit as tk
from tracekit.testing import generate_multi_tone, generate_sine_wave


def main() -> None:
    """Demonstrate FFT analysis basics."""
    print("=" * 60)
    print("TraceKit Example: FFT Basics")
    print("=" * 60)

    # --- Generate Test Signal ---
    print("\n--- Generating Test Signal ---")

    # Pure 1 MHz sine wave
    trace = generate_sine_wave(
        frequency=1e6,  # 1 MHz
        amplitude=1.0,
        sample_rate=100e6,  # 100 MSa/s
        duration=100e-6,  # 100 us for good frequency resolution
    )
    print("Generated 1 MHz sine wave")
    print(f"  Samples: {len(trace.data)}")
    print(f"  Sample rate: {trace.metadata.sample_rate / 1e6:.0f} MSa/s")
    print(f"  Duration: {trace.duration * 1e6:.0f} us")

    # --- Basic FFT ---
    print("\n--- Computing FFT ---")

    # tk.fft returns (frequencies, magnitudes_db) tuple
    freq, mag_db = tk.fft(trace)

    print("FFT computed:")
    print(f"  Frequency bins: {len(freq)}")
    print(f"  Frequency range: 0 to {freq[-1] / 1e6:.1f} MHz")
    print(f"  Resolution: {freq[1] / 1e3:.2f} kHz")

    # --- Find Peak Frequency ---
    print("\n--- Peak Frequency ---")

    peak_idx = np.argmax(mag_db)
    peak_freq = freq[peak_idx]
    peak_mag = mag_db[peak_idx]

    print(f"Peak frequency: {peak_freq / 1e6:.6f} MHz")
    print(f"Peak magnitude: {peak_mag:.1f} dB")
    print("(Expected: 1.000000 MHz)")

    # --- FFT with Windowing ---
    print("\n--- Windowing Effects ---")

    windows = ["rectangular", "hann", "hamming", "blackman", "flattop"]
    print("Window comparison (same signal):")

    for window in windows:
        f, m = tk.fft(trace, window=window)
        peak_idx = np.argmax(m)
        peak_freq = f[peak_idx]
        peak_mag = m[peak_idx]
        print(f"  {window:12s}: peak = {peak_mag:6.1f} dB at {peak_freq / 1e6:.6f} MHz")

    print("\nNote: Flattop has best amplitude accuracy, Hann has best frequency resolution")

    # --- FFT Size Control ---
    print("\n--- FFT Size Effects ---")

    for nfft in [256, 1024, 4096]:
        f, m = tk.fft(trace, nfft=nfft)
        resolution = trace.metadata.sample_rate / nfft
        print(f"  NFFT={nfft:4d}: resolution = {resolution / 1e3:.2f} kHz, bins = {len(f)}")

    # --- Multi-Tone Signal ---
    print("\n--- Multi-Tone Analysis ---")

    multi = generate_multi_tone(
        frequencies=[1e6, 2.5e6, 4e6],
        amplitudes=[1.0, 0.5, 0.25],
        sample_rate=100e6,
        duration=100e-6,
    )

    freq_multi, mag_multi = tk.fft(multi, window="hann")

    print("Finding peaks in multi-tone signal:")

    # Find peaks (local maxima above threshold)
    threshold_db = -40
    peaks = []
    for i in range(1, len(mag_multi) - 1):
        if (
            mag_multi[i] > threshold_db
            and mag_multi[i] > mag_multi[i - 1]
            and mag_multi[i] > mag_multi[i + 1]
        ):
            peaks.append((freq_multi[i], mag_multi[i]))

    # Sort by magnitude
    peaks.sort(key=lambda x: x[1], reverse=True)

    print(f"  Found {len(peaks)} peaks above {threshold_db} dB:")
    for f, m in peaks[:5]:
        print(f"    {f / 1e6:.3f} MHz: {m:.1f} dB")

    # --- Spectrum Data Access ---
    print("\n--- FFT Return Values ---")

    print("tk.fft(trace) returns a tuple:")
    print("  (frequencies, magnitudes_db)")
    print("    - frequencies: frequency axis in Hz")
    print("    - magnitudes_db: magnitude spectrum in dB")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. tk.fft(trace) returns (frequencies, magnitudes_db) tuple")
    print("  2. Window selection affects amplitude vs frequency accuracy")
    print("  3. Larger NFFT = better frequency resolution")
    print("  4. Frequency resolution = sample_rate / nfft")
    print("  5. magnitudes_db is typically most useful for analysis")
    print("=" * 60)


if __name__ == "__main__":
    main()
