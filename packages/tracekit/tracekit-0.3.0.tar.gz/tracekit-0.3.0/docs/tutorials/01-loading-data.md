# Tutorial 1: Loading Waveform Data

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08 | **Time**: 15 minutes

Learn how to load waveform data from various file formats into TraceKit.

## Prerequisites

- TraceKit installed (`uv pip install -e .`)
- Basic Python knowledge

## Learning Objectives

By the end of this tutorial, you will be able to:

- Load waveforms from common oscilloscope formats
- Understand the WaveformTrace data structure
- Access trace metadata
- Handle multiple channels

## What is a WaveformTrace?

A `WaveformTrace` is TraceKit's core data structure for analog waveform data:

```python
from tracekit import WaveformTrace

# A trace contains:
# - data: numpy array of samples
# - metadata: sample rate, units, channel info
# - time axis: computed from sample rate
```

## Loading Your First Waveform

### Step 1: Basic Loading

The simplest way to load a waveform:

```python
import tracekit as tk

# Auto-detect format from extension
trace = tk.load("capture.wfm")

# View basic info
print(f"Samples: {len(trace.data)}")
print(f"Sample rate: {trace.metadata.sample_rate} Hz")
print(f"Duration: {trace.duration * 1e6:.2f} us")
```

### Step 2: Check Supported Formats

Not sure what formats are supported?

```python
formats = tk.get_supported_formats()
print("Supported formats:")
for fmt in formats:
    print(f"  - {fmt}")
```

**Output:**

```
Supported formats:
  - tektronix (.wfm)
  - rigol (.wfm)
  - lecroy (.trc)
  - sigrok (.sr)
  - csv (.csv)
  - numpy (.npz)
  - hdf5 (.h5, .hdf5)
  - wav (.wav)
```

### Step 3: Specify Format Explicitly

When format cannot be auto-detected:

```python
# Explicitly specify format
trace = tk.load("ambiguous_file.bin", format="tektronix")
```

## Working with Metadata

Every trace includes rich metadata:

```python
trace = tk.load("capture.wfm")
meta = trace.metadata

print(f"Channel: {meta.channel}")
print(f"Sample rate: {meta.sample_rate / 1e6:.1f} MHz")
print(f"Vertical scale: {meta.vertical_scale}")
print(f"Vertical offset: {meta.vertical_offset}")
print(f"Units: {meta.units}")
```

## Loading Multiple Channels

Multi-channel captures can be loaded all at once:

```python
# Load all channels from a multi-channel file
channels = tk.load_all_channels("multichannel.wfm")

for name, trace in channels.items():
    print(f"Channel {name}: {len(trace.data)} samples")
```

Or load a specific channel:

```python
# Load only CH1
ch1 = tk.load("multichannel.wfm", channel="CH1")
```

## Handling Large Files

For very large waveform files, use lazy loading:

```python
# Don't load all data into memory immediately
trace = tk.load("huge_capture.wfm", lazy=True)

# Data is loaded on-demand when accessed
first_1000 = trace.data[:1000]  # Only loads first 1000 samples
```

Or process in chunks:

```python
for chunk in tk.iter_chunks("huge_capture.wfm", chunk_size=100_000):
    # Process each chunk
    peak = max(chunk.data)
    print(f"Chunk peak: {peak}")
```

## Loading from Different Sources

### CSV Files

```python
# CSV with time and voltage columns
trace = tk.load("data.csv")

# Specify column names if non-standard
trace = tk.load(
    "data.csv",
    time_column="Time_s",
    voltage_column="Voltage_V"
)
```

### NumPy Arrays

```python
import numpy as np

# Load from .npz file
trace = tk.load("data.npz")

# Or create from array
data = np.sin(2 * np.pi * 1e6 * np.linspace(0, 1e-3, 100000))
trace = tk.from_array(data, sample_rate=100e6)
```

### HDF5 Files

```python
# Standard HDF5 loading
trace = tk.load("data.h5")

# Specify dataset path
trace = tk.load("data.h5", dataset="/waveforms/channel1")
```

## Common Issues

### File Not Found

```python
from pathlib import Path

path = Path("data/capture.wfm")
if path.exists():
    trace = tk.load(path)
else:
    print(f"File not found: {path}")
```

### Unknown Format

```python
try:
    trace = tk.load("data.bin")
except tk.LoaderError as e:
    print(f"Error: {e}")
    print(f"Hint: {e.fix_hint}")
    # Try specifying format explicitly
    trace = tk.load("data.bin", format="tektronix")
```

## Exercise

Try loading one of TraceKit's sample files:

```python
import numpy as np
import tracekit as tk

# Generate test sine wave
sample_rate = 100e6
duration = 10e-6
frequency = 1e6
t = np.arange(0, duration, 1/sample_rate)
data = np.sin(2 * np.pi * frequency * t)
trace = tk.WaveformTrace(data=data, metadata=tk.TraceMetadata(sample_rate=sample_rate))

print(f"Generated {len(trace.data)} samples")
print(f"Duration: {trace.duration * 1e6:.1f} us")
```

## Next Steps

Now that you can load data, learn to analyze it:

- [Tutorial 2: Basic Measurements](02-basic-measurements.md)
- [Tutorial 3: Digital Signal Analysis](03-digital-signals.md)

## See Also

- [Loading Waveforms Guide](../guides/loading-waveforms.md)
- [Supported Formats Reference](../reference/supported-formats.md)
- [Synthetic Test Data Guide](../guides/synthetic-test-data.md)
