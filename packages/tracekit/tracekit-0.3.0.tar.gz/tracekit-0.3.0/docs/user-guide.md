# User Guide

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08 | **Applies to**: TraceKit 0.1.x

A comprehensive guide to using TraceKit for waveform analysis and protocol decoding.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Loading Waveforms](#loading-waveforms)
3. [Basic Measurements](#basic-measurements)
4. [Digital Signal Analysis](#digital-signal-analysis)
5. [Spectral Analysis](#spectral-analysis)
6. [Protocol Decoding](#protocol-decoding)
7. [Protocol Inference](#protocol-inference)
8. [Report Generation](#report-generation)
9. [Data Export](#data-export)
10. [Best Practices](#best-practices)

---

## Getting Started

### First Analysis

Create your first waveform analysis with a few lines of code:

```python
import tracekit as tk

# Load waveform
trace = tk.load("capture.wfm")

# Measure key parameters
print(f"Frequency: {tk.measure_frequency(trace):.2f} Hz")
print(f"Rise time: {tk.measure_rise_time(trace) * 1e9:.2f} ns")
print(f"Amplitude: {tk.measure_amplitude(trace):.3f} V")
```

### Using the CLI

For quick analyses, use the command line:

```bash
# Analyze a file
uv run tracekit analyze capture.wfm

# Decode a protocol
uv run tracekit decode capture.wfm -p uart --baud 115200

# Generate a report
uv run tracekit report capture.wfm -o report.pdf
```

---

## Loading Waveforms

### Basic Loading

TraceKit auto-detects file formats:

```python
import tracekit as tk

# Load any supported format
trace = tk.load("capture.wfm")       # Tektronix
trace = tk.load("data.sr")           # Sigrok
trace = tk.load("recording.csv")     # CSV

# Check what was loaded
print(f"Samples: {len(trace.data)}")
print(f"Sample rate: {trace.metadata.sample_rate}")
print(f"Duration: {trace.duration_seconds:.3f} s")
```

### Multi-Channel Files

Load all channels at once:

```python
# Load all channels
channels = tk.load_all_channels("multi_channel.wfm")

for name, trace in channels.items():
    print(f"{name}: {len(trace.data)} samples")

# Access specific channel
ch1 = channels["CH1"]
```

### Large Files

Use lazy loading for files over 100MB:

```python
# Enable lazy loading
trace = tk.load("huge_capture.wfm", lazy=True)

# Metadata available immediately
print(f"Sample rate: {trace.metadata.sample_rate}")

# Data loaded on demand
chunk = trace.data[0:10000]  # Only loads first 10k samples
```

### Format-Specific Options

```python
# Force specific loader
trace = tk.load("unknown.dat", format="tektronix")

# CSV with custom settings
trace = tk.load("data.csv", delimiter=";", skip_header=2)

# HDF5 with specific dataset
trace = tk.load("data.h5", dataset="/measurements/channel1")
```

### Supported Formats

Check supported formats programmatically:

```python
formats = tk.get_supported_formats()
# ['.wfm', '.csv', '.npz', '.h5', '.sr', '.pcap', ...]
```

---

## Basic Measurements

### Time-Domain Measurements

```python
import tracekit as tk

trace = tk.load("capture.wfm")

# Frequency and period
frequency = tk.measure_frequency(trace)
period = tk.measure_period(trace)

# Timing measurements
rise_time = tk.measure_rise_time(trace)           # 10-90%
rise_time_2080 = tk.measure_rise_time(trace, 0.2, 0.8)  # 20-80%
fall_time = tk.measure_fall_time(trace)

# Duty cycle
duty = tk.measure_duty_cycle(trace)

print(f"Frequency: {frequency/1e6:.2f} MHz")
print(f"Rise time: {rise_time*1e9:.2f} ns")
print(f"Duty cycle: {duty*100:.1f}%")
```

### Amplitude Measurements

```python
# Amplitude statistics
stats = tk.analyze_amplitude(trace)

print(f"Min: {stats.minimum:.3f} V")
print(f"Max: {stats.maximum:.3f} V")
print(f"Peak-to-peak: {stats.peak_to_peak:.3f} V")
print(f"Mean: {stats.mean:.3f} V")
print(f"RMS: {stats.rms:.3f} V")
print(f"Standard deviation: {stats.std:.3f} V")

# Or individual measurements
amplitude = tk.measure_amplitude(trace)
rms = tk.measure_rms(trace)
mean = tk.measure_mean(trace)
```

### Edge Detection

```python
# Find all edges
edges = tk.find_edges(trace, threshold=0.5)

for timestamp, is_rising in edges[:10]:
    edge_type = "rising" if is_rising else "falling"
    print(f"  {timestamp*1e6:.3f} us: {edge_type}")

# Count edges
rising_count = sum(1 for _, rising in edges if rising)
falling_count = len(edges) - rising_count
```

### Measurement with IEEE Compliance

TraceKit follows IEEE standards for measurements:

```python
# IEEE 181-2011 compliant pulse measurements
rise_time = tk.measure_rise_time(trace)  # Per IEEE 181-2011 Section 5.2

# IEEE 1241-2010 compliant ADC testing
sinad = tk.measure_sinad(trace)          # Per IEEE 1241-2010
enob = tk.measure_enob(trace)
```

---

## Digital Signal Analysis

### Clock Recovery

```python
from tracekit.analyzers.digital import recover_clock

# Recover clock from data signal
clock_info = recover_clock(trace)

print(f"Clock frequency: {clock_info.frequency/1e6:.2f} MHz")
print(f"Clock period: {clock_info.period*1e9:.2f} ns")
print(f"Jitter (RMS): {clock_info.jitter_rms*1e12:.2f} ps")
```

### Signal Quality Analysis

```python
from tracekit.analyzers.digital import analyze_signal_quality

# Comprehensive signal quality
quality = analyze_signal_quality(trace)

print(f"Rise time: {quality.rise_time*1e9:.2f} ns")
print(f"Fall time: {quality.fall_time*1e9:.2f} ns")
print(f"Overshoot: {quality.overshoot*100:.1f}%")
print(f"Undershoot: {quality.undershoot*100:.1f}%")
print(f"Ringing: {quality.ringing*100:.1f}%")
```

### Eye Diagram Analysis

```python
from tracekit.analyzers.eye import create_eye_diagram, analyze_eye

# Create eye diagram
eye = create_eye_diagram(trace, bit_rate=1e9)

# Analyze eye metrics
metrics = analyze_eye(eye)

print(f"Eye height: {metrics.eye_height*1e3:.2f} mV")
print(f"Eye width: {metrics.eye_width*1e12:.2f} ps")
print(f"Jitter (pk-pk): {metrics.jitter_pp*1e12:.2f} ps")
```

---

## Spectral Analysis

### FFT Analysis

```python
from tracekit.analyzers.spectral import compute_fft, compute_psd

# Compute FFT
spectrum = compute_fft(trace)

# Access frequency and magnitude data
frequencies = spectrum.frequencies
magnitudes_db = spectrum.magnitude_db

# Find peak
peak_idx = magnitudes_db.argmax()
print(f"Peak frequency: {frequencies[peak_idx]/1e6:.2f} MHz")
print(f"Peak magnitude: {magnitudes_db[peak_idx]:.1f} dB")
```

### Power Spectral Density

```python
# Compute PSD
psd = compute_psd(trace, window="hanning", nperseg=4096)

# Find dominant frequencies
peaks = tk.find_spectral_peaks(psd, threshold_db=-20)
for freq, power in peaks[:5]:
    print(f"  {freq/1e6:.2f} MHz: {power:.1f} dB")
```

### Harmonic Analysis

```python
from tracekit.analyzers.spectral import analyze_harmonics

# Find harmonics of fundamental
harmonics = analyze_harmonics(trace, fundamental=1e6)

print(f"Fundamental: {harmonics.fundamental/1e6:.2f} MHz @ {harmonics.fundamental_power:.1f} dB")
for i, (freq, power) in enumerate(harmonics.harmonics[:5], 2):
    print(f"H{i}: {freq/1e6:.2f} MHz @ {power:.1f} dB")

# Total Harmonic Distortion
thd = harmonics.thd
print(f"THD: {thd*100:.2f}%")
```

### SNR and SINAD

```python
from tracekit.analyzers.spectral import measure_snr, measure_sinad, measure_enob

# Signal-to-noise ratio
snr = measure_snr(trace, signal_freq=1e6)
print(f"SNR: {snr:.1f} dB")

# SINAD (includes distortion)
sinad = measure_sinad(trace, signal_freq=1e6)
print(f"SINAD: {sinad:.1f} dB")

# Effective number of bits
enob = measure_enob(trace)
print(f"ENOB: {enob:.2f} bits")
```

---

## Protocol Decoding

### UART Decoding

```python
from tracekit.protocols import UARTDecoder

# Create decoder
decoder = UARTDecoder(
    baud_rate=115200,
    data_bits=8,
    parity="none",
    stop_bits=1
)

# Decode trace
messages = decoder.decode(trace)

for msg in messages:
    print(f"[{msg.timestamp:.6f}s] {msg.data.hex()} '{msg.data.decode('ascii', errors='replace')}'")
```

### SPI Decoding

```python
from tracekit.protocols import SPIDecoder

# Load multi-channel capture
channels = tk.load_all_channels("spi_capture.wfm")

# Create decoder
decoder = SPIDecoder(
    clock=channels["D0"],
    mosi=channels["D1"],
    miso=channels["D2"],
    cs=channels["D3"],
    cpol=0,
    cpha=0
)

# Decode transactions
transactions = decoder.decode()

for txn in transactions:
    print(f"[{txn.timestamp:.6f}s] MOSI: {txn.mosi_data.hex()} MISO: {txn.miso_data.hex()}")
```

### I2C Decoding

```python
from tracekit.protocols import I2CDecoder

channels = tk.load_all_channels("i2c_capture.wfm")

decoder = I2CDecoder(
    sda=channels["SDA"],
    scl=channels["SCL"],
    address_bits=7
)

transactions = decoder.decode()

for txn in transactions:
    direction = "Write" if txn.is_write else "Read"
    print(f"[{txn.timestamp:.6f}s] Addr: 0x{txn.address:02X} {direction}: {txn.data.hex()}")
```

### CAN Decoding

```python
from tracekit.protocols import CANDecoder

decoder = CANDecoder(
    bitrate=500000,
    extended_ids=False
)

frames = decoder.decode(trace)

for frame in frames:
    print(f"ID: 0x{frame.arbitration_id:03X} Data: {frame.data.hex()} DLC: {frame.dlc}")
```

### Available Protocols

TraceKit supports 16+ protocols:

| Protocol   | Class               | Description                  |
| ---------- | ------------------- | ---------------------------- |
| UART       | `UARTDecoder`       | Async serial                 |
| SPI        | `SPIDecoder`        | Serial Peripheral Interface  |
| I2C        | `I2CDecoder`        | Inter-Integrated Circuit     |
| CAN        | `CANDecoder`        | Controller Area Network      |
| LIN        | `LINDecoder`        | Local Interconnect Network   |
| 1-Wire     | `OneWireDecoder`    | Dallas 1-Wire                |
| JTAG       | `JTAGDecoder`       | Joint Test Action Group      |
| SWD        | `SWDDecoder`        | Serial Wire Debug            |
| MDIO       | `MDIODecoder`       | Management Data I/O          |
| HDLC       | `HDLCDecoder`       | High-Level Data Link         |
| Manchester | `ManchesterDecoder` | Manchester encoding          |
| Miller     | `MillerDecoder`     | Miller encoding              |
| DMX512     | `DMX512Decoder`     | DMX lighting                 |
| DALI       | `DALIDecoder`       | Digital Addressable Lighting |
| Modbus     | `ModbusDecoder`     | Modbus RTU/ASCII             |
| NMEA       | `NMEADecoder`       | NMEA 0183 GPS                |

---

## Protocol Inference

### Automatic Detection

```python
from tracekit.inference import infer_protocol

# Automatically detect protocol
result = infer_protocol(trace)

print(f"Detected: {result.protocol_type}")
print(f"Confidence: {result.confidence:.1%}")
print(f"Parameters: {result.parameters}")
```

### Baud Rate Detection

```python
from tracekit.inference import detect_baud_rate

# Find baud rate
baud = detect_baud_rate(trace)
print(f"Detected baud rate: {baud}")
```

### Field Discovery

```python
from tracekit.inference import discover_fields

# Find message structure
fields = discover_fields(messages)

for field in fields:
    print(f"Field at offset {field.offset}: {field.type} ({field.bit_length} bits)")
```

---

## Report Generation

### PDF Reports

```python
from tracekit.reporting import generate_report, save_pdf_report

# Generate report
report = generate_report(
    trace,
    title="Signal Analysis Report",
    author="Engineering Team"
)

# Save as PDF
save_pdf_report(report, "analysis.pdf")
```

### HTML Reports

```python
from tracekit.reporting import save_html_report

# Generate interactive HTML
save_html_report(report, "analysis.html")
```

### Custom Reports

```python
from tracekit.reporting import ReportConfig, generate_report

config = ReportConfig(
    title="Custom Report",
    include_plots=True,
    include_raw_data=False,
    sections=["summary", "measurements", "spectral"]
)

report = generate_report(trace, config=config)
```

---

## Data Export

### CSV Export

```python
# Export to CSV
tk.export(trace, "data.csv")

# With options
tk.export(trace, "data.csv", include_time=True, precision=6)
```

### HDF5 Export

```python
# Export to HDF5 (recommended for large data)
tk.export(trace, "data.h5", compression="gzip")

# Multiple channels
tk.export_channels(channels, "multi.h5")
```

### NumPy Export

```python
# Export to NPZ
tk.export(trace, "data.npz")

# Load later
import numpy as np
data = np.load("data.npz")
samples = data["data"]
sample_rate = data["sample_rate"]
```

---

## Best Practices

### Memory Management

```python
# Use lazy loading for large files
trace = tk.load("huge.wfm", lazy=True)

# Process in chunks
for chunk in tk.iter_chunks(trace, chunk_size=100000):
    process(chunk)

# Explicit cleanup
del trace
```

### Error Handling

```python
from tracekit import LoaderError, DecodeError, MeasurementError

try:
    trace = tk.load("file.wfm")
except LoaderError as e:
    print(f"Load failed: {e}")
    print(f"Fix hint: {e.fix_hint}")

try:
    freq = tk.measure_frequency(trace)
except MeasurementError as e:
    print(f"Measurement failed: {e}")
    # freq may be NaN for certain signals
```

### NaN Handling

```python
import math

freq = tk.measure_frequency(trace)
if math.isnan(freq):
    print("Could not measure frequency - check signal type")
else:
    print(f"Frequency: {freq:.2f} Hz")
```

See [NaN Handling Guide](guides/nan-handling.md) for more details.

### Performance Tips

1. **Use lazy loading** for files over 100MB
2. **Process in chunks** for very large datasets
3. **Enable GPU** for FFT-heavy workloads
4. **Use appropriate precision** (float32 vs float64)

```python
# Enable GPU acceleration
import os
os.environ["TRACEKIT_GPU"] = "true"

# Or per-function
spectrum = compute_fft(trace, use_gpu=True)
```

---

## Troubleshooting

### Common Issues

**File won't load**

- Check file format is supported: `tk.get_supported_formats()`
- Verify file isn't corrupted
- Try specifying format explicitly: `tk.load("file", format="tektronix")`

**Measurements return NaN**

- Signal may not meet measurement requirements
- Check signal has sufficient transitions
- See [NaN Handling Guide](guides/nan-handling.md)

**Protocol decode errors**

- Verify protocol parameters (baud rate, polarity, etc.)
- Check signal quality and noise levels
- Use `infer_protocol()` to auto-detect settings

### Getting Help

- Check the [API Reference](api/index.md)
- Review [Examples](examples-reference.md)
- See [Troubleshooting Guide](guides/troubleshooting.md)

---

## See Also

- [Getting Started](getting-started.md) - Quick introduction
- [CLI Reference](cli.md) - Command-line interface
- [API Reference](api/index.md) - Complete API documentation
- [Examples](examples-reference.md) - Working code examples
