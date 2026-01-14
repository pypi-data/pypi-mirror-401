# 02_digital_analysis - Digital Signal Processing

> **Prerequisites**: [01_basics](../01_basics/)
> **Time**: 45-60 minutes

Learn digital signal analysis techniques including edge detection, clock recovery,
and signal quality assessment.

## Learning Objectives

By completing these examples, you will learn how to:

1. **Detect edges** - Find rising/falling transitions
2. **Recover clocks** - Extract clock signals from data
3. **Decode buses** - Extract data from digital buses
4. **Assess quality** - Measure signal integrity
5. **Multi-channel** - Analyze multiple signals together

## Examples in This Section

### 01_edge_detection.py

**What it does**: Find and analyze edge transitions

**Concepts covered**:

- Threshold crossing detection
- Rising vs falling edges
- Edge timing extraction
- Transition statistics

**Run it**:

```bash
uv run python examples/02_digital_analysis/01_edge_detection.py
```

**Expected output**: Edge count, timing, and statistics

---

### 02_clock_recovery.py

**What it does**: Recover clock timing from a data signal

**Concepts covered**:

- Clock frequency detection
- Period measurement
- Jitter calculation
- Correlation-based recovery

**Run it**:

```bash
uv run python examples/02_digital_analysis/02_clock_recovery.py
```

**Expected output**: Recovered clock frequency and jitter measurements

---

### 03_bus_decoding.py

**What it does**: Decode parallel bus data

**Concepts covered**:

- Multi-channel synchronization
- Bit alignment
- Bus state extraction
- Timing diagrams

**Run it**:

```bash
uv run python examples/02_digital_analysis/03_bus_decoding.py
```

**Expected output**: Decoded bus values with timestamps

---

### 04_signal_quality.py

**What it does**: Assess digital signal quality metrics

**Concepts covered**:

- Rise/fall time measurement
- Overshoot and undershoot
- Ringing detection
- Signal integrity scoring

**Run it**:

```bash
uv run python examples/02_digital_analysis/04_signal_quality.py
```

**Expected output**: Signal quality metrics and pass/fail status

---

### 05_multi_channel.py

**What it does**: Analyze multiple channels together

**Concepts covered**:

- Loading multi-channel files
- Channel correlation
- Timing relationships
- Skew measurement

**Run it**:

```bash
uv run python examples/02_digital_analysis/05_multi_channel.py
```

**Expected output**: Multi-channel analysis results

---

## Quick Reference

### Edge Detection

```python
import tracekit as tk

edges = tk.detect_edges(trace, threshold=0.5)

for edge in edges[:10]:
    edge_type = "rising" if edge.is_rising else "falling"
    print(f"{edge.timestamp*1e6:.3f} us: {edge_type}")
```

### Clock Recovery

```python
from tracekit.analyzers.digital import recover_clock

clock_info = recover_clock(trace)
print(f"Frequency: {clock_info.frequency/1e6:.2f} MHz")
print(f"Jitter RMS: {clock_info.jitter_rms*1e12:.2f} ps")
```

### Signal Quality

```python
from tracekit.analyzers.digital import SignalQualityAnalyzer

analyzer = SignalQualityAnalyzer(sample_rate, logic_family="TTL")
quality = analyzer.analyze(signal)
print(f"Rise time: {quality.transitions.rise_time*1e9:.2f} ns")
print(f"Overshoot: {quality.transitions.overshoot:.1f}%")
```

### Multi-Channel

```python
import tracekit as tk

channels = tk.load_all_channels("capture.wfm")

for name, trace in channels.items():
    freq = tk.frequency(trace)
    print(f"{name}: {freq/1e6:.2f} MHz")
```

## Common Issues

**Issue**: Clock recovery fails

**Solution**: Ensure signal has regular transitions. Pure DC or random noise won't work.

---

**Issue**: Edge detection finds too many/few edges

**Solution**: Adjust threshold to match signal levels:

```python
edges = tk.detect_edges(trace, threshold=1.65)  # For 3.3V logic
```

---

**Issue**: Multi-channel timing is off

**Solution**: Verify channels are from same capture with same timebase.

---

## Estimated Time

- **Quick review**: 20 minutes
- **Hands-on practice**: 45-60 minutes

## Next Steps

Continue your learning path:

- **[03_spectral_analysis](../03_spectral_analysis/)** - Frequency domain analysis
- **[04_protocol_decoding](../04_protocol_decoding/)** - Decode serial protocols

## See Also

- [User Guide: Digital Analysis](../../docs/user-guide.md#digital-signal-analysis)
- [API Reference: Analysis](../../docs/api/analysis.md)
