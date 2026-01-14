# Signal Intelligence & Classification Guide

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

TraceKit Phase 3 introduces intelligent signal classification and measurement suitability checking to help users understand their signals and avoid common measurement pitfalls.

## Overview

The signal intelligence features automatically analyze signals to:

- **Classify signal types** (DC, analog, digital, mixed)
- **Assess signal quality** (SNR, noise, clipping, saturation)
- **Check measurement suitability** (prevent NaN results, warn about unreliable measurements)
- **Suggest appropriate measurements** (ranked recommendations based on signal characteristics)

## Quick Start

```python
import tracekit as tk

# Load a signal
trace = tk.load("mystery_signal.wfm")

# Classify the signal
classification = tk.classify_signal(trace)
print(f"Signal type: {classification['type']}")
print(f"Characteristics: {classification['characteristics']}")
if classification['frequency_estimate']:
    print(f"Frequency: {classification['frequency_estimate']:.3e} Hz")

# Assess signal quality
quality = tk.assess_signal_quality(trace)
if quality['snr']:
    print(f"SNR: {quality['snr']:.1f} dB")
if quality['warnings']:
    print("Quality warnings:", quality['warnings'])

# Get measurement suggestions
suggestions = tk.suggest_measurements(trace)
print("\nRecommended measurements:")
for s in suggestions[:5]:
    print(f"  - {s['name']}: {s['rationale']}")
```

## Signal Classification

### classify_signal()

Automatically detects signal type and characteristics:

```python
classification = tk.classify_signal(trace)
```

**Returns:**

- `type`: "dc", "analog", "digital", or "mixed"
- `characteristics`: List like ["periodic", "clean", "digital_levels"]
- `dc_component`: True if significant DC offset
- `frequency_estimate`: Fundamental frequency in Hz (or None)
- `confidence`: Classification confidence (0.0-1.0)
- `noise_level`: Estimated noise in signal units
- `levels`: For digital signals, dict with "low" and "high" voltage levels

**Example - DC Signal:**

```python
# DC power rail measurement
dc_trace = tk.load("3v3_rail.wfm")
result = tk.classify_signal(dc_trace)
# result['type'] = 'dc'
# result['characteristics'] = ['constant']
# result['frequency_estimate'] = None
```

**Example - Digital Square Wave:**

```python
# Clock signal
clock_trace = tk.load("10mhz_clock.wfm")
result = tk.classify_signal(clock_trace)
# result['type'] = 'digital'
# result['characteristics'] = ['periodic', 'digital_levels', 'clean']
# result['frequency_estimate'] ≈ 10e6  # Hz
# result['levels'] = {'low': 0.0, 'high': 3.3}
```

**Example - Analog Sine Wave:**

```python
# Audio signal
audio_trace = tk.load("1khz_tone.wfm")
result = tk.classify_signal(audio_trace)
# result['type'] = 'analog'
# result['characteristics'] = ['periodic', 'clean']
# result['frequency_estimate'] ≈ 1000  # Hz
```

## Signal Quality Assessment

### assess_signal_quality()

Evaluates signal quality and detects issues:

```python
quality = tk.assess_signal_quality(trace)
```

**Returns:**

- `snr`: Signal-to-noise ratio in dB (or None)
- `noise_level`: RMS noise level
- `clipping`: True if signal is clipped
- `saturation`: True if signal is saturated
- `warnings`: List of quality warning strings
- `dynamic_range`: Signal dynamic range in dB
- `crest_factor`: Peak-to-RMS ratio

**Example - Detecting Clipping:**

```python
# Overdriven signal
clipped_trace = tk.load("overdriven_input.wfm")
quality = tk.assess_signal_quality(clipped_trace)

if quality['clipping']:
    print("WARNING: Signal clipping detected!")
    print("This will affect measurement accuracy.")
    print("Reduce input amplitude or increase scope vertical range.")
```

**Example - SNR Analysis:**

```python
# Noisy measurement
noisy_trace = tk.load("low_level_signal.wfm")
quality = tk.assess_signal_quality(noisy_trace)

print(f"SNR: {quality['snr']:.1f} dB")
if quality['snr'] < 20:
    print("Low SNR detected. Consider:")
    print("  - Reducing measurement bandwidth")
    print("  - Averaging multiple captures")
    print("  - Improving signal conditioning")
```

## Measurement Suitability

### check_measurement_suitability()

Checks if a measurement will work on a signal:

```python
suitability = tk.check_measurement_suitability(trace, "frequency")
```

**Args:**

- `trace`: Input waveform
- `measurement_name`: Name like "frequency", "rise_time", "thd", etc.

**Returns:**

- `suitable`: True if measurement is appropriate
- `confidence`: Confidence in assessment (0.0-1.0)
- `warnings`: List of warning strings
- `suggestions`: List of suggestion strings
- `expected_result`: "valid", "nan", or "unreliable"

**Example - Preventing NaN Results:**

```python
# User wants to measure frequency on DC signal
dc_trace = tk.load("dc_voltage.wfm")

# Check before measuring
check = tk.check_measurement_suitability(dc_trace, "frequency")

if not check['suitable']:
    print("WARNING: Frequency measurement not suitable!")
    print("Reason:", check['warnings'][0])
    print("Suggestion:", check['suggestions'][0])
    # Output:
    # WARNING: Frequency measurement not suitable!
    # Reason: frequency measurement not suitable for DC signal
    # Suggestion: Use 'mean' or 'rms' measurements for DC signals
else:
    freq = tk.frequency(dc_trace)  # Would return NaN
```

**Example - Detecting Insufficient Sample Rate:**

```python
# High frequency signal with low sample rate
fast_signal = tk.load("100mhz_signal.wfm")  # Sampled at 500 MSa/s

check = tk.check_measurement_suitability(fast_signal, "frequency")

if check['expected_result'] == "unreliable":
    print("WARNING: Measurement may be unreliable")
    for warning in check['warnings']:
        print(f"  - {warning}")
    # Output:
    # WARNING: Measurement may be unreliable
    #   - Sample rate may be too low for accurate timing measurements
    #   - Recommend sample rate > 1.00e+09 Hz (10x signal frequency)
```

## Smart Measurement Suggestions

### suggest_measurements()

Recommends appropriate measurements for a signal:

```python
suggestions = tk.suggest_measurements(trace, max_suggestions=10)
```

**Returns:** List of dictionaries with:

- `name`: Measurement name
- `category`: "timing", "amplitude", "spectral", "statistical"
- `priority`: Priority ranking (1 = highest)
- `rationale`: Why this measurement is recommended
- `confidence`: Confidence in recommendation (0.0-1.0)

**Example - Digital Signal:**

```python
# Square wave
clock = tk.load("uart_tx.wfm")
suggestions = tk.suggest_measurements(clock)

for s in suggestions[:5]:
    print(f"{s['priority']}. {s['name']}: {s['rationale']}")

# Output:
# 1. mean: Basic DC level measurement, always applicable
# 2. rms: RMS voltage measurement, useful for all signal types
# 3. amplitude: Peak-to-peak amplitude for digital signal
# 4. frequency: Periodic signal detected, frequency measurement applicable
# 5. period: Period measurement for periodic signal
# 6. rise_time: Digital edges detected (127 edges)
# 7. fall_time: Digital edges detected (127 edges)
# 8. duty_cycle: Periodic pulse train detected
```

**Example - DC Signal:**

```python
# Power rail
power_rail = tk.load("5v_rail.wfm")
suggestions = tk.suggest_measurements(power_rail)

for s in suggestions:
    print(f"  {s['name']}: {s['rationale']}")

# Output:
#   mean: Basic DC level measurement, always applicable
#   rms: RMS voltage measurement, useful for all signal types
#   amplitude: Measure noise/variation level in DC signal
```

**Example - Clean Periodic Signal:**

```python
# Pure sine wave from signal generator
sine = tk.load("1khz_sine.wfm")
suggestions = tk.suggest_measurements(sine)

# Includes spectral measurements for clean signals:
# - thd: Clean periodic signal suitable for harmonic analysis
# - snr: Spectral SNR measurement for signal quality
```

## Practical Workflows

### Workflow 1: Troubleshooting NaN Results

```python
import tracekit as tk

# User gets NaN from frequency measurement
trace = tk.load("problem_signal.wfm")
freq = tk.frequency(trace)
print(f"Frequency: {freq}")  # NaN!

# Diagnose the problem
classification = tk.classify_signal(trace)
print(f"\nSignal type: {classification['type']}")
print(f"Characteristics: {classification['characteristics']}")

if classification['type'] == 'dc':
    print("\nProblem: DC signal has no frequency!")
    print("The signal is constant - frequency measurement returns NaN.")

# Check what went wrong
suitability = tk.check_measurement_suitability(trace, "frequency")
print(f"\nMeasurement suitable: {suitability['suitable']}")
print(f"Expected result: {suitability['expected_result']}")
print(f"Warnings: {suitability['warnings']}")

# Get better suggestions
print("\nRecommended measurements instead:")
suggestions = tk.suggest_measurements(trace)
for s in suggestions[:3]:
    print(f"  - {s['name']}: {s['rationale']}")
```

### Workflow 2: Automatic Signal Characterization

```python
import tracekit as tk

def characterize_unknown_signal(filename):
    """Automatically characterize an unknown signal."""
    trace = tk.load(filename)

    # Classify
    classification = tk.classify_signal(trace)
    print(f"=== Signal Classification ===")
    print(f"Type: {classification['type']}")
    print(f"Characteristics: {', '.join(classification['characteristics'])}")

    if classification['frequency_estimate']:
        print(f"Frequency: {classification['frequency_estimate']:.3e} Hz")

    if classification['levels']:
        print(f"Logic levels: {classification['levels']['low']:.2f} V to "
              f"{classification['levels']['high']:.2f} V")

    print(f"Confidence: {classification['confidence']*100:.0f}%")

    # Assess quality
    print(f"\n=== Signal Quality ===")
    quality = tk.assess_signal_quality(trace)

    if quality['snr']:
        print(f"SNR: {quality['snr']:.1f} dB")
    print(f"Noise level: {quality['noise_level']:.3e}")

    if quality['clipping']:
        print("WARNING: Signal clipping detected!")
    if quality['saturation']:
        print("WARNING: Signal saturation detected!")

    if quality['warnings']:
        print("\nQuality warnings:")
        for w in quality['warnings']:
            print(f"  - {w}")

    # Suggest measurements
    print(f"\n=== Recommended Measurements ===")
    suggestions = tk.suggest_measurements(trace, max_suggestions=5)

    for i, s in enumerate(suggestions, 1):
        print(f"{i}. {s['name']} ({s['category']})")
        print(f"   {s['rationale']}")
        print(f"   Confidence: {s['confidence']*100:.0f}%")

    return classification, quality, suggestions

# Use it
classification, quality, suggestions = characterize_unknown_signal("mystery.wfm")
```

### Workflow 3: Validating Measurement Setup

```python
import tracekit as tk

def validate_measurement_setup(trace, desired_measurements):
    """Check if desired measurements will work on this signal."""
    print("=== Measurement Validation ===\n")

    valid_measurements = []
    problematic_measurements = []

    for meas_name in desired_measurements:
        check = tk.check_measurement_suitability(trace, meas_name)

        if check['suitable'] and check['expected_result'] == 'valid':
            valid_measurements.append(meas_name)
            print(f"✓ {meas_name}: OK")
        else:
            problematic_measurements.append((meas_name, check))
            print(f"✗ {meas_name}: {check['expected_result'].upper()}")

            for warning in check['warnings']:
                print(f"    Warning: {warning}")
            for suggestion in check['suggestions']:
                print(f"    Suggestion: {suggestion}")
            print()

    return valid_measurements, problematic_measurements

# Example usage
trace = tk.load("uart_signal.wfm")
desired = ["frequency", "rise_time", "duty_cycle", "thd"]

valid, problematic = validate_measurement_setup(trace, desired)

print(f"\nValid measurements: {len(valid)}/{len(desired)}")
print(f"Proceed with: {', '.join(valid)}")
```

## Configuration Options

All signal intelligence functions support optional parameters to tune detection:

```python
# Classify with custom thresholds
classification = tk.classify_signal(
    trace,
    digital_threshold_ratio=0.8,  # Require 80% of samples at two levels for digital
    dc_threshold_percent=90.0,    # DC component if > 90% of amplitude
    periodicity_threshold=0.7     # Correlation threshold for periodic detection
)

# Assess quality with bandwidth consideration
quality = tk.assess_signal_quality(
    trace,
    bandwidth_hz=1e6  # Consider 1 MHz bandwidth for SNR calculation
)

# Limit number of suggestions
suggestions = tk.suggest_measurements(trace, max_suggestions=5)
```

## Integration with Existing Measurements

The signal intelligence features work seamlessly with TraceKit's existing measurement functions:

```python
import tracekit as tk

trace = tk.load("signal.wfm")

# Get smart suggestions
suggestions = tk.suggest_measurements(trace)

# Execute suggested measurements
results = {}
for s in suggestions[:5]:
    meas_name = s['name']

    # Check suitability before measuring
    check = tk.check_measurement_suitability(trace, meas_name)

    if check['expected_result'] == 'valid':
        # Safe to measure
        if meas_name == 'frequency':
            results[meas_name] = tk.frequency(trace)
        elif meas_name == 'rise_time':
            results[meas_name] = tk.rise_time(trace)
        elif meas_name == 'amplitude':
            results[meas_name] = tk.amplitude(trace)
        # ... etc

# Display results
print("Measurement Results:")
for name, value in results.items():
    if not np.isnan(value):
        print(f"  {name}: {value:.3e}")
```

## Best Practices

1. **Always classify unknown signals first** - Understanding signal type prevents inappropriate measurements

2. **Check suitability before measuring** - Avoid NaN results and wasted computation

3. **Heed quality warnings** - Clipping, low SNR, and saturation affect accuracy

4. **Use suggestions as a starting point** - They're ranked by relevance but you know your application best

5. **Consider sample rate warnings** - Insufficient sample rate is a common source of measurement errors

6. **Validate automated decisions** - The intelligence features are helpers, not replacements for domain knowledge

## API Reference

See the full API documentation:

- `classify_signal()` - [ANALYSIS_API.md](../api/analysis.md#classify_signal)
- `assess_signal_quality()` - [ANALYSIS_API.md](../api/analysis.md#assess_signal_quality)
- `check_measurement_suitability()` - [ANALYSIS_API.md](../api/analysis.md#check_measurement_suitability)
- `suggest_measurements()` - [ANALYSIS_API.md](../api/analysis.md#suggest_measurements)

## Related Documentation

- [NAN_RESULTS_GUIDE.md](nan-handling.md) - Why measurements return NaN
- [TROUBLESHOOTING_NAN_RESULTS.md](nan-handling.md) - Quick NaN troubleshooting

## Troubleshooting

**Q: Why is my signal classified as "unknown"?**
A: Likely insufficient data (<10 samples). Capture more samples.

**Q: Periodicity detection seems wrong**
A: Ensure you have at least 3-5 full periods in your capture. Single periods cannot be reliably detected as periodic.

**Q: Why doesn't it detect my digital signal?**
A: If signal has slow transitions or significant noise, it may appear analog. Check that samples spend most time at two distinct levels.

**Q: Frequency estimate is inaccurate**
A: Autocorrelation-based frequency estimation works best with 5+ periods and clean signals. For noisy or short captures, use `tk.frequency()` which uses edge detection.

## Future Enhancements

Planned features:

- Machine learning-based classification
- Protocol auto-detection (detect UART/SPI/I2C automatically)
- Signal source identification (generator vs real-world)
- Automatic filter recommendations
- Measurement uncertainty estimation

## Conclusion

The signal intelligence features make TraceKit more user-friendly by:

- Preventing common mistakes
- Explaining why measurements fail
- Guiding users to appropriate analysis techniques
- Reducing trial-and-error

Start using these features today to make your signal analysis workflow more efficient and robust!
