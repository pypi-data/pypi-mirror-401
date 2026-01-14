# 03_spectral_analysis - Frequency Domain Analysis

> **Prerequisites**: [01_basics](../01_basics/)
> **Time**: 30-45 minutes

Learn spectral analysis techniques including FFT, harmonic analysis,
and signal quality measurements in the frequency domain.

## Learning Objectives

By completing these examples, you will learn how to:

1. **Compute FFT** - Transform time to frequency domain
2. **Measure THD/SNR** - Quantify signal quality
3. **Analyze harmonics** - Find and measure harmonic content
4. **Create spectrograms** - Time-frequency analysis
5. **Measure jitter** - Timing uncertainty analysis

## Examples in This Section

### 01_fft_basics.py

**What it does**: Compute and visualize FFT spectra

**Concepts covered**:

- FFT computation
- Window functions
- Frequency axis scaling
- dB conversion
- Peak finding

**Run it**:

```bash
uv run python examples/03_spectral_analysis/01_fft_basics.py
```

**Expected output**: FFT plot and peak frequencies

---

### 02_thd_snr_measurements.py

**What it does**: Measure signal quality metrics

**Concepts covered**:

- Total Harmonic Distortion (THD)
- Signal-to-Noise Ratio (SNR)
- SINAD measurement
- Effective Number of Bits (ENOB)

**Run it**:

```bash
uv run python examples/03_spectral_analysis/02_thd_snr_measurements.py
```

**Expected output**: THD, SNR, SINAD, ENOB values

---

### 03_spectrogram.py

**What it does**: Create time-frequency spectrograms

**Concepts covered**:

- Short-time FFT
- Spectrogram visualization
- Frequency drift detection
- Transient analysis

**Run it**:

```bash
uv run python examples/03_spectral_analysis/03_spectrogram.py
```

**Expected output**: Spectrogram plot

---

### 04_jitter_analysis.py

**What it does**: Analyze timing jitter

**Concepts covered**:

- Period jitter
- Cycle-to-cycle jitter
- Time Interval Error (TIE)
- Jitter histogram
- RMS and peak-to-peak jitter

**Run it**:

```bash
uv run python examples/03_spectral_analysis/04_jitter_analysis.py
```

**Expected output**: Jitter measurements and histogram

---

## Quick Reference

### FFT Computation

```python
from tracekit.analyzers.spectral import compute_fft

spectrum = compute_fft(trace, window="hanning")

# Access results
frequencies = spectrum.frequencies
magnitudes_db = spectrum.magnitude_db

# Find peak
peak_idx = magnitudes_db.argmax()
print(f"Peak: {frequencies[peak_idx]/1e6:.2f} MHz")
```

### THD and SNR

```python
from tracekit.analyzers.spectral import measure_thd, measure_snr, measure_sinad

thd = measure_thd(trace, fundamental_freq=1e6)
snr = measure_snr(trace, signal_freq=1e6)
sinad = measure_sinad(trace, signal_freq=1e6)

print(f"THD: {thd*100:.2f}%")
print(f"SNR: {snr:.1f} dB")
print(f"SINAD: {sinad:.1f} dB")
```

### Harmonic Analysis

```python
from tracekit.analyzers.spectral import analyze_harmonics

harmonics = analyze_harmonics(trace, fundamental=1e6)

print(f"Fundamental: {harmonics.fundamental_power:.1f} dB")
for i, (freq, power) in enumerate(harmonics.harmonics[:5], 2):
    print(f"H{i}: {freq/1e6:.2f} MHz @ {power:.1f} dB")
```

### Spectrogram

```python
from tracekit.analyzers.spectral import compute_spectrogram

spec = compute_spectrogram(trace, nperseg=1024, noverlap=512)

# Visualize
import matplotlib.pyplot as plt
plt.pcolormesh(spec.times, spec.frequencies, spec.power_db)
plt.ylabel("Frequency (Hz)")
plt.xlabel("Time (s)")
plt.show()
```

### Jitter Analysis

```python
from tracekit.analyzers.jitter import analyze_jitter

jitter = analyze_jitter(trace, clock_freq=100e6)

print(f"Period jitter RMS: {jitter.period_rms*1e12:.2f} ps")
print(f"Period jitter pk-pk: {jitter.period_pp*1e12:.2f} ps")
print(f"Cycle-to-cycle: {jitter.cycle_to_cycle*1e12:.2f} ps")
```

## Common Issues

**Issue**: FFT shows unexpected peaks

**Solution**: Use appropriate window function. Default "hanning" reduces spectral leakage.

---

**Issue**: THD measurement seems wrong

**Solution**: Ensure fundamental frequency is accurate. Use auto-detection:

```python
thd = measure_thd(trace)  # Auto-detects fundamental
```

---

**Issue**: Spectrogram resolution is poor

**Solution**: Adjust segment size and overlap:

```python
# More frequency resolution
spec = compute_spectrogram(trace, nperseg=4096)

# More time resolution
spec = compute_spectrogram(trace, nperseg=256)
```

---

## Estimated Time

- **Quick review**: 15 minutes
- **Hands-on practice**: 30-45 minutes

## Next Steps

Continue your learning path:

- **[04_protocol_decoding](../04_protocol_decoding/)** - Decode serial protocols
- **[05_advanced](../05_advanced/)** - Advanced topics

## See Also

- [User Guide: Spectral Analysis](../../docs/user-guide.md#spectral-analysis)
- [API Reference: Analysis](../../docs/api/analysis.md)
