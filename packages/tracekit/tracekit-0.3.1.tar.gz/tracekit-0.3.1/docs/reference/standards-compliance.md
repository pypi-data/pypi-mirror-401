# Standards Compliance

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

TraceKit implements measurements according to industry standards for accurate, reproducible results.

## IEEE Standards

### IEEE 181-2011 - Pulse Measurements

**Standard**: IEEE Standard for Transitions, Pulses, and Related Waveforms

**Coverage**: Full

| Measurement   | Section | TraceKit Function         | Notes                     |
| ------------- | ------- | ------------------------- | ------------------------- |
| Rise Time     | 5.2     | `measure_rise_time()`     | 10-90% default            |
| Fall Time     | 5.2     | `measure_fall_time()`     | 90-10% default            |
| Pulse Width   | 5.3     | `measure_pulse_width()`   | At 50% reference          |
| Overshoot     | 5.4     | `measure_overshoot()`     | As percentage             |
| Undershoot    | 5.4     | `measure_undershoot()`    | As percentage             |
| Preshoot      | 5.4     | `measure_preshoot()`      | Pre-transition aberration |
| Settling Time | 5.5     | `measure_settling_time()` | To specified band         |

#### Reference Levels

TraceKit uses IEEE 181-2011 Section 4 definitions:

- **Low Reference (0%)**: Minimum stable level before transition
- **High Reference (100%)**: Maximum stable level after transition
- **Proximal (10%)**: Default low threshold
- **Distal (90%)**: Default high threshold
- **Mesial (50%)**: Mid-reference for timing

```python
import tracekit as tk

# IEEE 181 compliant measurement (10-90%)
rise_time = tk.measure_rise_time(trace)

# Custom thresholds (20-80%)
rise_time_20_80 = tk.measure_rise_time(trace, low=0.2, high=0.8)
```

### IEEE 1057-2017 - Digitizer Characterization

**Standard**: IEEE Standard for Digitizing Waveform Recorders

**Coverage**: Partial

| Measurement     | Section | TraceKit Function | Notes        |
| --------------- | ------- | ----------------- | ------------ |
| Effective Bits  | 4.5     | `measure_enob()`  | Full support |
| Noise Floor     | 4.3     | `measure_noise()` | Full support |
| Linearity (INL) | 4.6     | -                 | Planned      |
| Linearity (DNL) | 4.6     | -                 | Planned      |

### IEEE 1241-2010 - ADC Testing

**Standard**: IEEE Standard for Terminology and Test Methods for Analog-to-Digital Converters

**Coverage**: Full

| Measurement | Section | TraceKit Function | Notes        |
| ----------- | ------- | ----------------- | ------------ |
| SNR         | 4.1.4.4 | `measure_snr()`   | Full support |
| SINAD       | 4.1.4.5 | `measure_sinad()` | Full support |
| THD         | 4.1.4.6 | `measure_thd()`   | Full support |
| SFDR        | 4.1.4.7 | `measure_sfdr()`  | Full support |
| ENOB        | 4.1.4.8 | `measure_enob()`  | Full support |

#### ENOB Calculation

```python
from tracekit.analyzers.spectral import measure_sinad, measure_enob

# ENOB from SINAD per IEEE 1241-2010
sinad = measure_sinad(trace, signal_freq=1e6)
enob = (sinad - 1.76) / 6.02

# Or use direct function
enob = measure_enob(trace, signal_freq=1e6)
```

### IEEE 2414-2020 - Jitter Measurements

**Standard**: IEEE Standard for Jitter and Phase Noise

**Coverage**: Partial

| Measurement        | Section | TraceKit Function          | Notes      |
| ------------------ | ------- | -------------------------- | ---------- |
| Period Jitter      | 5.2     | `measure_period_jitter()`  | RMS, pk-pk |
| Cycle-to-Cycle     | 5.3     | `measure_cycle_to_cycle()` | Full       |
| TIE                | 5.4     | `measure_tie()`            | Full       |
| Phase Noise        | 6.0     | -                          | Planned    |
| Random Jitter (RJ) | 7.1     | `decompose_jitter()`       | Partial    |
| Deterministic (DJ) | 7.2     | `decompose_jitter()`       | Partial    |

```python
from tracekit.analyzers.jitter import (
    measure_period_jitter,
    measure_cycle_to_cycle,
    measure_tie,
)

# Period jitter (RMS and peak-to-peak)
jitter = measure_period_jitter(trace)
print(f"Period jitter RMS: {jitter.rms * 1e12:.1f} ps")
print(f"Period jitter pk-pk: {jitter.peak_to_peak * 1e12:.1f} ps")

# Cycle-to-cycle jitter
c2c = measure_cycle_to_cycle(trace)
print(f"Cycle-to-cycle: {c2c * 1e12:.1f} ps")

# Time Interval Error
tie = measure_tie(trace, ideal_period=1e-6)
```

## JEDEC Standards

### JEDEC JESD65B - Timing Specifications

**Standard**: Definition of Skew Specifications for Standard Logic Devices

**Coverage**: Partial

| Measurement       | TraceKit Function      | Notes        |
| ----------------- | ---------------------- | ------------ |
| Propagation Delay | `measure_prop_delay()` | Full support |
| Skew              | `measure_skew()`       | Full support |
| Setup Time        | `measure_setup_time()` | Multi-signal |
| Hold Time         | `measure_hold_time()`  | Multi-signal |

```python
from tracekit.analyzers.digital import measure_setup_hold

# Measure setup and hold time between data and clock
timing = measure_setup_hold(data_trace, clock_trace)
print(f"Setup time: {timing.setup * 1e9:.1f} ns")
print(f"Hold time: {timing.hold * 1e9:.1f} ns")
```

## Compliance Verification

### Self-Test Mode

```python
import tracekit as tk

# Run compliance verification with known reference signals
from tracekit.testing import generate_ieee181_reference

# Generate reference pulse per IEEE 181-2011 Annex A
ref_pulse = generate_ieee181_reference(
    rise_time=10e-9,  # Known 10 ns rise time
    sample_rate=10e9,  # 10 GSa/s
)

# Measure and verify
measured = tk.measure_rise_time(ref_pulse)
error = abs(measured - 10e-9) / 10e-9 * 100
print(f"Rise time: {measured * 1e9:.2f} ns (error: {error:.2f}%)")
```

### Reference Signals

TraceKit includes reference signal generators per IEEE standards:

| Function                       | Standard       | Purpose                   |
| ------------------------------ | -------------- | ------------------------- |
| `generate_ieee181_reference()` | IEEE 181-2011  | Pulse timing verification |
| `generate_ieee1241_test()`     | IEEE 1241-2010 | ADC characterization      |
| `generate_ieee2414_clock()`    | IEEE 2414-2020 | Jitter measurement        |

## Implementation Notes

### Measurement Uncertainty

TraceKit reports measurement uncertainty when calculable:

```python
result = tk.measure_frequency(trace, return_uncertainty=True)
print(f"Frequency: {result.value / 1e6:.6f} MHz")
print(f"Uncertainty: +/- {result.uncertainty / 1e3:.1f} kHz")
```

### Sample Rate Requirements

For accurate measurements, sample rate must be sufficient:

| Measurement | Minimum Sample Rate            |
| ----------- | ------------------------------ |
| Rise Time   | 5x / rise_time (10x preferred) |
| Frequency   | 2x signal frequency (Nyquist)  |
| Jitter      | 10x / jitter_amount            |
| THD         | 10x highest harmonic           |

### Algorithm Selection

Some measurements have multiple algorithm options:

```python
# Rise time algorithms
rise = tk.measure_rise_time(trace, algorithm="histogram")  # Better for noisy signals
rise = tk.measure_rise_time(trace, algorithm="linear")     # Faster
rise = tk.measure_rise_time(trace, algorithm="filtered")   # Pre-filters noise

# Frequency algorithms
freq = tk.measure_frequency(trace, algorithm="zero_crossing")  # Standard
freq = tk.measure_frequency(trace, algorithm="fft")            # For noisy signals
freq = tk.measure_frequency(trace, algorithm="autocorr")       # For periodic signals
```

## References

- IEEE 181-2011: https://standards.ieee.org/standard/181-2011.html
- IEEE 1057-2017: https://standards.ieee.org/standard/1057-2017.html
- IEEE 1241-2010: https://standards.ieee.org/standard/1241-2010.html
- IEEE 2414-2020: https://standards.ieee.org/standard/2414-2020.html
- JEDEC JESD65B: https://www.jedec.org/standards-documents/docs/jesd-65b

## See Also

- [API Reference: Measurements](../api/analysis.md)
- [Measurement Functions](index.md#measurement-functions)
- [Troubleshooting](../guides/troubleshooting.md)
