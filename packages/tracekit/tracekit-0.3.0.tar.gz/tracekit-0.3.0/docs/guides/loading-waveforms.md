# Loading Waveforms Guide

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

This guide covers loading waveform data from various file formats, including
analog and digital waveforms, multi-channel files, and large file handling.

## Basic Loading

The primary entry point for loading trace data is the `load()` function:

```python
import tracekit as tk

# Auto-detect format from file extension
trace = tk.load("capture.wfm")

# Check what we loaded
print(f"Samples: {len(trace.data)}")
print(f"Sample rate: {trace.metadata.sample_rate} Hz")
print(f"Channel: {trace.metadata.channel_name}")
```

## Loading Digital Waveforms

TraceKit automatically detects whether a file contains analog or digital
waveform data. Digital waveforms from mixed-signal oscilloscopes (MSO) are
loaded as `DigitalTrace` objects with boolean sample data:

```python
import tracekit as tk
from tracekit import DigitalTrace, WaveformTrace

# Load any waveform file
trace = tk.load("digital_capture.wfm")

# Check if it's a digital trace
if isinstance(trace, DigitalTrace):
    print("Loaded digital waveform")
    print(f"Total samples: {len(trace.data)}")
    print(f"High samples: {trace.data.sum()}")
    print(f"Duty cycle: {trace.data.mean() * 100:.1f}%")

    # Access edge information if available
    if trace.edges:
        print(f"Detected edges: {len(trace.edges)}")
else:
    print("Loaded analog waveform")
    print(f"Mean value: {trace.data.mean():.4f}")
```

### Digital Trace Properties

Digital traces have these key properties:

- `data`: NumPy boolean array (True = high, False = low)
- `metadata`: TraceMetadata with sample_rate, source_file, channel_name
- `edges`: Optional list of (timestamp, is_rising) tuples

### Digital Channel Naming

Digital channels from Tektronix MSO scopes typically use D1, D2, etc. naming:

```python
trace = tk.load("mso_capture.wfm")
print(f"Channel: {trace.metadata.channel_name}")  # e.g., "D1"
```

## Multi-Channel Loading

For files containing multiple channels, use `load_all_channels()` to load
all channels with a single read:

```python
import tracekit as tk

# Load all channels from a multi-channel file
channels = tk.load_all_channels("multi_channel.wfm")

# Iterate through channels
for name, trace in channels.items():
    print(f"{name}: {len(trace.data)} samples")

    # Check trace type
    if isinstance(trace, tk.DigitalTrace):
        print(f"  Type: Digital")
        print(f"  Duty cycle: {trace.data.mean() * 100:.1f}%")
    else:
        print(f"  Type: Analog")
        print(f"  Mean: {trace.data.mean():.4f}")

# Access specific channels
ch1 = channels.get("ch1")  # Analog channel 1
d1 = channels.get("d1")    # Digital channel 1
```

### Channel Naming Convention

- Analog channels: `ch1`, `ch2`, `ch3`, `ch4`
- Digital channels: `d1`, `d2`, `d3`, ... `d16`

## Lazy Loading for Large Files

For very large files (>100MB), use lazy loading to avoid memory issues:

```python
import tracekit as tk

# Enable lazy loading
trace = tk.load("huge_capture.wfm", lazy=True)

# Metadata is available immediately
print(f"File: {trace.metadata.source_file}")

# Data is loaded on first access
chunk = trace.data[0:10000]  # Loads only what's needed
```

The `load()` function will warn you when loading large files without lazy mode:

```
UserWarning: File is large (250.5 MB).
Consider using lazy=True for better memory efficiency.
```

## Specifying File Format

By default, TraceKit auto-detects the format from the file extension. You can
override this with the `format` parameter:

```python
# Force Tektronix loader
trace = tk.load("unknown.dat", format="tektronix")

# Force Rigol loader
trace = tk.load("capture.bin", format="rigol")
```

## Supported Formats

Check supported formats programmatically:

```python
from tracekit import get_supported_formats

formats = get_supported_formats()
print(formats)
# ['.wfm', '.npz', '.csv', '.h5', '.hdf5', '.sr', '.pcap', ...]
```

## Error Handling

TraceKit provides informative error messages:

```python
import tracekit as tk
from tracekit import LoaderError, FormatError

try:
    trace = tk.load("problem.wfm")
except FormatError as e:
    print(f"Format issue: {e}")
    print(f"File: {e.file_path}")
    print(f"Fix hint: {e.fix_hint}")
except LoaderError as e:
    print(f"Load failed: {e}")
```

### Common Error Scenarios

| Error              | Cause                    | Solution             |
| ------------------ | ------------------------ | -------------------- |
| File too small     | Truncated/corrupted file | Check file integrity |
| No waveform data   | Empty acquisition        | Re-capture data      |
| Unsupported format | Unknown file type        | Use explicit format= |

## Debugging Loading Issues

Enable debug logging to troubleshoot loading problems:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

import tracekit as tk
trace = tk.load("problem.wfm")
```

This will show:

- WFM object type detected
- Available attributes
- Loading path chosen (analog_waveforms, digital, etc.)
- Sample rate and other metadata extraction

## Performance Tips

1. **Multi-channel files**: Use `load_all_channels()` instead of multiple
   `load()` calls - it reads the file once.

2. **Large files**: Use `lazy=True` to avoid loading entire file into memory.

3. **Batch processing**: Consider using chunked loading for very large datasets:

   ```python
   from tracekit import load_trace_chunks

   for chunk in load_trace_chunks("huge_file.wfm", chunk_size=1_000_000):
       process(chunk)
   ```

4. **Format detection**: If you know the format, use `format=` parameter
   to skip auto-detection overhead.
