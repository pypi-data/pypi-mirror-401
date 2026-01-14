# Tutorial 4: Spectral Analysis

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08 | **Time**: 30 minutes

Learn to analyze signals in the frequency domain using FFT, PSD, and spectral metrics.

## Prerequisites

- Completed [Tutorial 2: Basic Measurements](02-basic-measurements.md)
- Basic understanding of frequency domain concepts

## Learning Objectives

By the end of this tutorial, you will be able to:

- Compute and interpret FFT results
- Calculate power spectral density
- Measure THD, SNR, and SINAD
- Analyze harmonics

## The Frequency Domain

Time-domain analysis tells you "what happened when." Frequency-domain analysis tells you "what frequencies are present and how strong."

```python
import numpy as np
import tracekit as tk

# A pure 1 MHz sine wave
sample_rate = 100e6
duration = 100e-6
frequency = 1e6
t = np.arange(0, duration, 1/sample_rate)
data = np.sin(2 * np.pi * frequency * t)
sine = tk.WaveformTrace(data=data, metadata=tk.TraceMetadata(sample_rate=sample_rate))

# In time domain: we see oscillations
# In frequency domain: we see a single spike at 1 MHz
```

## Computing FFT

### Basic FFT

```python
from tracekit.analyzers.spectral import compute_fft

# Compute FFT
spectrum = compute_fft(sine)

# Spectrum contains:
# - frequencies: array of frequency bins (Hz)
# - magnitude: linear magnitude
# - magnitude_db: magnitude in dB
# - phase: phase in radians

print(f"Frequency bins: {len(spectrum.frequencies)}")
print(f"Frequency range: {spectrum.frequencies[0]:.0f} - {spectrum.frequencies[-1]/1e6:.1f} MHz")
```

### Finding the Peak Frequency

```python
import numpy as np

# Find the dominant frequency
peak_idx = np.argmax(spectrum.magnitude_db)
peak_freq = spectrum.frequencies[peak_idx]
peak_mag = spectrum.magnitude_db[peak_idx]

print(f"Peak frequency: {peak_freq / 1e6:.3f} MHz")
print(f"Peak magnitude: {peak_mag:.1f} dB")
```

### Windowing

Apply window functions to reduce spectral leakage:

```python
# Available windows: hanning, hamming, blackman, flattop, rectangular
spectrum_hann = compute_fft(sine, window="hanning")
spectrum_flat = compute_fft(sine, window="flattop")

# Hanning: Good frequency resolution
# Flattop: Good amplitude accuracy
# Rectangular: No windowing (fastest, but most leakage)
```

### FFT Size Control

```python
# Specify FFT size (must be power of 2 for efficiency)
spectrum = compute_fft(sine, nfft=4096)

# More points = better frequency resolution
# Resolution = sample_rate / nfft
resolution = 100e6 / 4096
print(f"Frequency resolution: {resolution / 1e3:.2f} kHz")
```

## Power Spectral Density

PSD shows power distribution across frequencies:

```python
from tracekit.analyzers.spectral import compute_psd

# Compute PSD using Welch's method
psd = compute_psd(sine)

print(f"PSD frequencies: {len(psd.frequencies)}")
print(f"Units: V^2/Hz (power density)")

# Find frequency with maximum power
peak_idx = np.argmax(psd.power)
print(f"Peak at: {psd.frequencies[peak_idx] / 1e6:.3f} MHz")
```

### PSD Parameters

```python
# Control averaging and resolution
psd = compute_psd(
    sine,
    nperseg=1024,      # Segment length
    noverlap=512,      # Overlap between segments
    window="hanning"   # Window function
)
```

## Signal Quality Metrics

### Total Harmonic Distortion (THD)

THD measures harmonic content relative to the fundamental:

```python
from tracekit.analyzers.spectral import measure_thd

# Generate signal with harmonics (distorted sine)
sample_rate = 100e6
duration = 100e-6
frequency = 1e6
t = np.arange(0, duration, 1/sample_rate)
# Add 2nd and 3rd harmonics for ~5% THD
data = np.sin(2 * np.pi * frequency * t) + \
       0.03 * np.sin(2 * np.pi * 2 * frequency * t) + \
       0.04 * np.sin(2 * np.pi * 3 * frequency * t)
distorted = tk.WaveformTrace(data=data, metadata=tk.TraceMetadata(sample_rate=sample_rate))

thd = measure_thd(distorted)
print(f"THD: {thd * 100:.2f}%")
```

### Signal-to-Noise Ratio (SNR)

```python
from tracekit.analyzers.spectral import measure_snr

# Generate noisy signal
sample_rate = 100e6
duration = 100e-6
frequency = 1e6
t = np.arange(0, duration, 1/sample_rate)
data = np.sin(2 * np.pi * frequency * t) + np.random.normal(0, 0.01, len(t))
noisy = tk.WaveformTrace(data=data, metadata=tk.TraceMetadata(sample_rate=sample_rate))

snr = measure_snr(noisy, signal_freq=1e6)
print(f"SNR: {snr:.1f} dB")
```

### SINAD (Signal-to-Noise and Distortion)

SINAD combines noise and distortion:

```python
from tracekit.analyzers.spectral import measure_sinad

sinad = measure_sinad(noisy, signal_freq=1e6)
print(f"SINAD: {sinad:.1f} dB")
```

### Effective Number of Bits (ENOB)

For ADC characterization:

```python
from tracekit.analyzers.spectral import measure_enob

enob = measure_enob(noisy, signal_freq=1e6)
print(f"ENOB: {enob:.2f} bits")

# ENOB relates to SINAD: ENOB = (SINAD - 1.76) / 6.02
```

## Harmonic Analysis

Find and analyze harmonics:

```python
from tracekit.analyzers.spectral import analyze_harmonics

harmonics = analyze_harmonics(distorted, fundamental=1e6, num_harmonics=5)

print("Harmonic analysis:")
print(f"  Fundamental: {harmonics.fundamental_freq / 1e6:.3f} MHz")
print(f"  Fundamental power: {harmonics.fundamental_power_db:.1f} dB")

for i, (freq, power) in enumerate(zip(harmonics.harmonic_freqs, harmonics.harmonic_powers_db)):
    print(f"  Harmonic {i+2}: {freq / 1e6:.3f} MHz, {power:.1f} dB")
```

## Multi-Tone Analysis

Analyze signals with multiple frequency components:

```python
# Create signal with multiple tones
sample_rate = 100e6
duration = 100e-6
frequencies = [1e6, 2.5e6, 4e6]
amplitudes = [1.0, 0.5, 0.25]
t = np.arange(0, duration, 1/sample_rate)
data = sum(amp * np.sin(2 * np.pi * freq * t)
           for freq, amp in zip(frequencies, amplitudes))
multi = tk.WaveformTrace(data=data, metadata=tk.TraceMetadata(sample_rate=sample_rate))

spectrum = compute_fft(multi)

# Find all peaks above threshold
from tracekit.analyzers.spectral import find_spectral_peaks

peaks = find_spectral_peaks(spectrum, threshold_db=-40)

print(f"Found {len(peaks)} spectral peaks:")
for freq, mag_db in peaks:
    print(f"  {freq / 1e6:.3f} MHz: {mag_db:.1f} dB")
```

## Spectrogram (Time-Frequency Analysis)

For signals that change over time:

```python
from tracekit.analyzers.spectral import compute_spectrogram

# Generate chirp signal (frequency sweep)
sample_rate = 100e6
duration = 1e-3
start_freq = 100e3
end_freq = 10e6
t = np.arange(0, duration, 1/sample_rate)
# Linear chirp
instantaneous_freq = start_freq + (end_freq - start_freq) * t / duration
phase = 2 * np.pi * np.cumsum(instantaneous_freq) / sample_rate
data = np.sin(phase)
chirp = tk.WaveformTrace(data=data, metadata=tk.TraceMetadata(sample_rate=sample_rate))

# Compute spectrogram
spectrogram = compute_spectrogram(
    chirp,
    nperseg=256,
    noverlap=128
)

print(f"Spectrogram shape: {spectrogram.Sxx.shape}")
print(f"Time bins: {len(spectrogram.times)}")
print(f"Frequency bins: {len(spectrogram.frequencies)}")
```

## GPU Acceleration

Speed up spectral analysis with GPU:

```python
# Check GPU availability
if tk.gpu_available():
    # GPU-accelerated FFT
    spectrum = compute_fft(sine, use_gpu=True)
    print("Using GPU acceleration")
else:
    spectrum = compute_fft(sine)
    print("Using CPU")
```

## Complete Analysis Example

```python
import numpy as np
import tracekit as tk
from tracekit.analyzers.spectral import (
    compute_fft,
    compute_psd,
    measure_snr,
    measure_thd,
    measure_sinad,
    measure_enob,
)

# Generate test signal
sample_rate = 100e6
duration = 1e-3
frequency = 1e6
amplitude = 1.0
t = np.arange(0, duration, 1/sample_rate)
data = amplitude * np.sin(2 * np.pi * frequency * t) + np.random.normal(0, 0.001, len(t))
signal = tk.WaveformTrace(data=data, metadata=tk.TraceMetadata(sample_rate=sample_rate))

print("=== Spectral Analysis Report ===\n")

# Time domain info
print(f"Signal duration: {signal.duration * 1e3:.2f} ms")
print(f"Sample rate: {signal.metadata.sample_rate / 1e6:.0f} MSa/s")
print(f"Samples: {len(signal.data)}")

# FFT analysis
spectrum = compute_fft(signal, window="hanning")
peak_idx = np.argmax(spectrum.magnitude_db)

print(f"\nFFT Analysis:")
print(f"  Dominant frequency: {spectrum.frequencies[peak_idx] / 1e6:.6f} MHz")
print(f"  Peak magnitude: {spectrum.magnitude_db[peak_idx]:.1f} dB")

# Quality metrics
print(f"\nSignal Quality:")
print(f"  SNR: {measure_snr(signal, signal_freq=1e6):.1f} dB")
print(f"  THD: {measure_thd(signal) * 100:.4f}%")
print(f"  SINAD: {measure_sinad(signal, signal_freq=1e6):.1f} dB")
print(f"  ENOB: {measure_enob(signal, signal_freq=1e6):.2f} bits")
```

## Exercise

Analyze a complex signal:

```python
# Generate AM modulated signal
sample_rate = 100e6
duration = 10e-3
carrier_freq = 10e6
modulation_freq = 1e3
modulation_depth = 0.8
t = np.arange(0, duration, 1/sample_rate)
# AM: (1 + m*cos(2*pi*fm*t)) * cos(2*pi*fc*t)
modulation = 1 + modulation_depth * np.cos(2 * np.pi * modulation_freq * t)
data = modulation * np.cos(2 * np.pi * carrier_freq * t)
am = tk.WaveformTrace(data=data, metadata=tk.TraceMetadata(sample_rate=sample_rate))

# Tasks:
# 1. Compute the FFT and identify the carrier frequency
# 2. Find the sidebands (carrier +/- modulation_freq)
# 3. Calculate the modulation depth from sideband amplitudes

# Your code here...
```

## Next Steps

- [Tutorial 5: Protocol Decoding](05-protocol-decoding.md)
- [Tutorial 6: Report Generation](06-report-generation.md)

## See Also

- [Spectral API Reference](../api/analysis.md#spectral-analysis)
- [GPU Acceleration Guide](../guides/gpu-acceleration.md)
- [IEEE 1241-2010 Compliance](../reference/standards-compliance.md)
