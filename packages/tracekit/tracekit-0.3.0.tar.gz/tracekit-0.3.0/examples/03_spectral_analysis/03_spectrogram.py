#!/usr/bin/env python3
"""Example 03: Spectrogram Analysis.

This example demonstrates time-frequency analysis using spectrograms
(Short-Time Fourier Transform) for non-stationary signals.

Time: 20 minutes
Prerequisites: FFT basics

Run:
    uv run python examples/03_spectral_analysis/03_spectrogram.py
"""

import numpy as np

from tracekit.analyzers.waveform.spectral import spectrogram, spectrogram_chunked
from tracekit.core.types import TraceMetadata, WaveformTrace


def main() -> None:
    """Demonstrate spectrogram analysis capabilities."""
    print("=" * 60)
    print("TraceKit Example: Spectrogram Analysis")
    print("=" * 60)

    # --- Basic Spectrogram ---
    print("\n--- Basic Spectrogram ---")

    demo_basic_spectrogram()

    # --- Chirp Signal Analysis ---
    print("\n--- Chirp Signal (Frequency Sweep) ---")

    demo_chirp_analysis()

    # --- Modulated Signal ---
    print("\n--- Amplitude Modulated Signal ---")

    demo_am_signal()

    # --- Multi-Tone Switching ---
    print("\n--- Multi-Tone Switching Analysis ---")

    demo_switching_tones()

    # --- Chunked Spectrogram (Large Files) ---
    print("\n--- Chunked Processing for Large Files ---")

    demo_chunked_spectrogram()

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. Spectrograms show frequency content over time")
    print("  2. nperseg controls frequency vs time resolution tradeoff")
    print("  3. noverlap improves time resolution")
    print("  4. Use chunked processing for very large files")
    print("  5. Window function affects spectral leakage")
    print("=" * 60)


def demo_basic_spectrogram() -> None:
    """Demonstrate basic spectrogram generation."""
    # Generate a simple signal with two frequencies
    sample_rate = 10e6  # 10 MHz
    duration = 1e-3  # 1 ms
    n_samples = int(sample_rate * duration)

    t = np.arange(n_samples) / sample_rate

    # Two-tone signal
    f1, f2 = 100e3, 250e3  # 100 kHz and 250 kHz
    signal = np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t)

    # Add noise
    signal += np.random.randn(n_samples) * 0.1

    # Create trace
    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="two_tone")
    trace = WaveformTrace(data=signal, metadata=metadata)

    # Compute spectrogram
    times, freqs, Sxx_db = spectrogram(trace, window="hann", nperseg=1024, noverlap=768)

    print(f"Signal: Two tones at {f1 / 1e3:.0f} kHz and {f2 / 1e3:.0f} kHz")
    print(f"Duration: {duration * 1e3:.1f} ms, Sample rate: {sample_rate / 1e6:.0f} MHz")
    print("\nSpectrogram dimensions:")
    print(f"  Time bins: {len(times)}")
    print(f"  Frequency bins: {len(freqs)}")
    print(f"  Frequency range: 0 to {freqs[-1] / 1e3:.0f} kHz")
    print(f"  Time range: 0 to {times[-1] * 1e3:.2f} ms")

    # Find peak frequencies
    avg_spectrum = np.mean(10 ** (Sxx_db / 10), axis=1)
    avg_spectrum_db = 10 * np.log10(avg_spectrum + 1e-20)

    # Find peaks
    peak_indices = np.argsort(avg_spectrum_db)[-5:][::-1]
    print("\nTop frequencies in spectrogram:")
    for idx in peak_indices:
        if freqs[idx] > 0:  # Skip DC
            print(f"  {freqs[idx] / 1e3:.1f} kHz: {avg_spectrum_db[idx]:.1f} dB")


def demo_chirp_analysis() -> None:
    """Demonstrate spectrogram of a frequency chirp."""
    sample_rate = 20e6  # 20 MHz
    duration = 2e-3  # 2 ms
    n_samples = int(sample_rate * duration)

    t = np.arange(n_samples) / sample_rate

    # Linear chirp from 100 kHz to 1 MHz over duration
    f0 = 100e3  # Start frequency
    f1 = 1e6  # End frequency

    # Chirp formula: f(t) = f0 + (f1-f0)*t/T
    # Phase: phi(t) = 2*pi * (f0*t + (f1-f0)*t^2/(2*T))
    phase = 2 * np.pi * (f0 * t + (f1 - f0) * t**2 / (2 * duration))
    signal = np.sin(phase)

    # Add noise
    signal += np.random.randn(n_samples) * 0.05

    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="chirp")
    trace = WaveformTrace(data=signal, metadata=metadata)

    # Compute spectrogram with good time resolution
    times, freqs, Sxx_db = spectrogram(trace, window="hann", nperseg=512, noverlap=480)

    print(f"Chirp signal: {f0 / 1e3:.0f} kHz to {f1 / 1e6:.1f} MHz")
    print(f"Duration: {duration * 1e3:.1f} ms")

    # Track frequency over time
    print("\nFrequency tracking (from spectrogram):")

    time_points = [0.0, 0.5e-3, 1.0e-3, 1.5e-3, 2.0e-3]
    for target_time in time_points:
        if target_time > times[-1]:
            continue

        # Find nearest time bin
        time_idx = np.argmin(np.abs(times - target_time))

        # Find peak frequency at this time
        spectrum_slice = Sxx_db[:, time_idx]
        peak_idx = np.argmax(spectrum_slice)
        peak_freq = freqs[peak_idx]

        # Expected frequency
        expected_freq = f0 + (f1 - f0) * target_time / duration

        error_pct = abs(peak_freq - expected_freq) / expected_freq * 100

        print(
            f"  t={target_time * 1e3:.1f}ms: measured={peak_freq / 1e3:.0f}kHz, "
            f"expected={expected_freq / 1e3:.0f}kHz, error={error_pct:.1f}%"
        )


def demo_am_signal() -> None:
    """Demonstrate spectrogram of amplitude modulated signal."""
    sample_rate = 10e6  # 10 MHz
    duration = 5e-3  # 5 ms
    n_samples = int(sample_rate * duration)

    t = np.arange(n_samples) / sample_rate

    # AM signal: carrier with modulating envelope
    fc = 500e3  # 500 kHz carrier
    fm = 1e3  # 1 kHz modulation frequency
    m = 0.8  # Modulation depth

    carrier = np.sin(2 * np.pi * fc * t)
    modulation = 1 + m * np.sin(2 * np.pi * fm * t)
    signal = modulation * carrier

    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="am_signal")
    trace = WaveformTrace(data=signal, metadata=metadata)

    # Compute spectrogram
    times, freqs, Sxx_db = spectrogram(trace, window="hann", nperseg=2048, noverlap=1920)

    print("AM Signal:")
    print(f"  Carrier frequency: {fc / 1e3:.0f} kHz")
    print(f"  Modulation frequency: {fm / 1e3:.1f} kHz")
    print(f"  Modulation depth: {m * 100:.0f}%")

    # Find carrier and sidebands in average spectrum
    avg_spectrum = np.mean(10 ** (Sxx_db / 10), axis=1)
    avg_spectrum_db = 10 * np.log10(avg_spectrum + 1e-20)

    # Look for carrier and sidebands
    carrier_idx = np.argmin(np.abs(freqs - fc))
    lower_sb_idx = np.argmin(np.abs(freqs - (fc - fm)))
    upper_sb_idx = np.argmin(np.abs(freqs - (fc + fm)))

    print("\nSpectral components:")
    print(f"  Carrier ({fc / 1e3:.0f} kHz): {avg_spectrum_db[carrier_idx]:.1f} dB")
    print(f"  Lower sideband ({(fc - fm) / 1e3:.1f} kHz): {avg_spectrum_db[lower_sb_idx]:.1f} dB")
    print(f"  Upper sideband ({(fc + fm) / 1e3:.1f} kHz): {avg_spectrum_db[upper_sb_idx]:.1f} dB")

    # Calculate modulation depth from sidebands
    carrier_power = 10 ** (avg_spectrum_db[carrier_idx] / 10)
    sideband_power = (
        10 ** (avg_spectrum_db[lower_sb_idx] / 10) + 10 ** (avg_spectrum_db[upper_sb_idx] / 10)
    ) / 2
    measured_m = 2 * np.sqrt(sideband_power / carrier_power)

    print(f"\nMeasured modulation depth: {measured_m * 100:.1f}% (expected {m * 100:.0f}%)")


def demo_switching_tones() -> None:
    """Demonstrate spectrogram of frequency-hopping signal."""
    sample_rate = 20e6  # 20 MHz
    duration = 4e-3  # 4 ms
    n_samples = int(sample_rate * duration)

    t = np.arange(n_samples) / sample_rate

    # Frequency hopping sequence
    hop_duration = 1e-3  # 1 ms per frequency
    frequencies = [200e3, 500e3, 800e3, 300e3]  # 4 frequencies

    signal = np.zeros(n_samples)

    for i, freq in enumerate(frequencies):
        start_sample = int(i * hop_duration * sample_rate)
        end_sample = int((i + 1) * hop_duration * sample_rate)
        end_sample = min(end_sample, n_samples)

        t_segment = t[start_sample:end_sample] - t[start_sample]
        signal[start_sample:end_sample] = np.sin(2 * np.pi * freq * t_segment)

    # Add noise
    signal += np.random.randn(n_samples) * 0.1

    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="freq_hop")
    trace = WaveformTrace(data=signal, metadata=metadata)

    # Compute spectrogram with good time resolution
    times, freqs, Sxx_db = spectrogram(trace, window="hann", nperseg=512, noverlap=480)

    print("Frequency hopping signal:")
    print(f"  Hop duration: {hop_duration * 1e3:.0f} ms")
    print(f"  Frequencies: {[f / 1e3 for f in frequencies]} kHz")

    print("\nDetected frequency hops:")

    # Detect frequency at each hop interval
    for i in range(len(frequencies)):
        target_time = (i + 0.5) * hop_duration  # Middle of each hop

        # Find nearest time bin
        time_idx = np.argmin(np.abs(times - target_time))

        # Find peak frequency at this time
        spectrum_slice = Sxx_db[:, time_idx]
        peak_idx = np.argmax(spectrum_slice)
        detected_freq = freqs[peak_idx]

        expected_freq = frequencies[i]
        match = "OK" if abs(detected_freq - expected_freq) < 50e3 else "MISMATCH"

        print(
            f"  Hop {i + 1} (t={target_time * 1e3:.1f}ms): "
            f"detected={detected_freq / 1e3:.0f}kHz, expected={expected_freq / 1e3:.0f}kHz [{match}]"
        )


def demo_chunked_spectrogram() -> None:
    """Demonstrate chunked spectrogram for large files."""
    # Simulate a large file scenario
    sample_rate = 100e6  # 100 MHz
    duration = 10e-3  # 10 ms (1M samples - simulate large file)
    n_samples = int(sample_rate * duration)

    t = np.arange(n_samples) / sample_rate

    # Generate complex signal with multiple components
    signal = np.zeros(n_samples)

    # Component 1: Constant 1 MHz
    signal += np.sin(2 * np.pi * 1e6 * t)

    # Component 2: 5 MHz appearing halfway through
    halfway = n_samples // 2
    signal[halfway:] += 0.5 * np.sin(2 * np.pi * 5e6 * t[halfway:])

    # Add noise
    signal += np.random.randn(n_samples) * 0.1

    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="large_signal")
    trace = WaveformTrace(data=signal, metadata=metadata)

    print("Large signal analysis:")
    print(f"  Samples: {n_samples:,}")
    print(f"  Duration: {duration * 1e3:.1f} ms")
    print(f"  Sample rate: {sample_rate / 1e6:.0f} MHz")

    # Standard spectrogram
    times_std, freqs_std, Sxx_std = spectrogram(trace, nperseg=4096, noverlap=3072)

    print("\nStandard spectrogram:")
    print(f"  Time bins: {len(times_std)}")
    print(f"  Frequency bins: {len(freqs_std)}")

    # Chunked spectrogram (for demonstration - works same as standard for this size)
    chunk_size = n_samples // 4  # Process in 4 chunks
    times_chunked, freqs_chunked, Sxx_chunked = spectrogram_chunked(
        trace,
        chunk_size=chunk_size,
        nperseg=4096,
        noverlap=3072,
    )

    print("\nChunked spectrogram (4 chunks):")
    print(f"  Time bins: {len(times_chunked)}")
    print(f"  Frequency bins: {len(freqs_chunked)}")

    # Verify consistency
    if len(times_std) == len(times_chunked):
        max_diff = np.max(np.abs(Sxx_std - Sxx_chunked))
        print("\nConsistency check:")
        print(f"  Max difference: {max_diff:.2f} dB")
        print(f"  Chunked processing: {'Verified' if max_diff < 0.1 else 'Check required'}")

    print("\nTip: Use spectrogram_chunked() for files larger than available RAM.")
    print("     Memory usage scales with chunk_size, not file size.")


if __name__ == "__main__":
    main()
