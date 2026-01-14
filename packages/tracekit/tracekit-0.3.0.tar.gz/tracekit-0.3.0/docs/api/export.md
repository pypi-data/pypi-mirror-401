# TraceKit Export API Documentation

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

Complete guide to exporting trace data and analysis results in multiple formats.

## Overview

TraceKit provides comprehensive export functionality for all data types:

- **CSV** - Time series data with metadata comments
- **JSON** - Structured data with full trace support
- **HDF5** - Efficient binary format for large datasets
- **MATLAB** - .mat files for MATLAB/Octave compatibility
- **NPZ** - NumPy compressed format for Python workflows
- **PWL** - SPICE piecewise linear format for circuit simulation
- **Markdown** - Human-readable reports with tables and plots

All export functions are accessible via top-level API: `tk.export_*()`

## Quick Start

```python
import tracekit as tk

# Load a trace
trace = tk.load("capture.wfm")

# Export to different formats
tk.export_csv(trace, "output.csv")
tk.export_json(trace, "output.json")
tk.export_hdf5(trace, "output.h5")
tk.export_mat(trace, "output.mat")
```

## CSV Export

Export trace data to CSV format with metadata as header comments.

### Basic Usage

```python
import tracekit as tk

trace = tk.load("signal.wfm")

# Simple export
tk.export_csv(trace, "signal.csv")

# With custom precision and delimiter
tk.export_csv(trace, "signal.tsv", precision=6, delimiter="\t")

# Without time column
tk.export_csv(trace, "data_only.csv", include_time=False)
```

### Features

- **Metadata Comments**: Sample rate, duration, acquisition info as `#` comments
- **Time Units**: Choose from seconds, milliseconds, microseconds, nanoseconds
- **Precision Control**: Configure decimal precision for floating point values
- **Custom Delimiters**: Comma, tab, or any delimiter
- **Header Control**: Optional header rows

### CSV Export Parameters

```python
tk.export_csv(
    data,              # WaveformTrace, DigitalTrace, dict, or ndarray
    path,              # Output file path
    include_time=True, # Include time column
    time_unit="s",     # "s", "ms", "us", "ns"
    precision=9,       # Decimal precision
    delimiter=",",     # Column delimiter
    header=True        # Include header and metadata
)
```

### CSV File Format

```csv
# TraceKit CSV Export
# Sample Rate: 1000000000.0 Hz
# Time Base: 1e-09 s
# Samples: 10000
# Duration: 9.999e-06 s
# Vertical Scale: 0.1 V/div
# Vertical Offset: 0.0 V
# Source File: capture.wfm
# Channel: CH1
#
Time (s),Voltage
0,0.0123456
1e-09,0.0234567
2e-09,0.0345678
...
```

### Multiple Traces

```python
from tracekit.exporters import export_multi_trace_csv

traces = [ch1, ch2, ch3]
export_multi_trace_csv(
    traces,
    "channels.csv",
    names=["CH1", "CH2", "CH3"],
    time_unit="us"
)
```

## JSON Export

Export structured data with full trace object support.

### Basic Usage

```python
import tracekit as tk

trace = tk.load("signal.wfm")

# Export full trace object
tk.export_json(trace, "trace.json")

# Export measurements
results = tk.measure(trace)
tk.export_json(results, "measurements.json")

# Compressed JSON
tk.export_json(trace, "trace.json.gz", compress=True)
```

### Features

- **Full Trace Support**: Exports complete WaveformTrace/DigitalTrace objects
- **Metadata Preservation**: All metadata included in structured format
- **Pretty Printing**: Human-readable or compact output
- **Compression**: Optional gzip compression for large files
- **Type Information**: Preserves data types with `_type` annotations

### JSON Export Parameters

```python
tk.export_json(
    data,                  # Trace, dict, or list
    path,                  # Output file path
    pretty=True,           # Pretty print with indentation
    include_metadata=True, # Include export metadata
    compress=False         # Compress with gzip
)
```

### JSON File Format

```json
{
  "_metadata": {
    "format": "tracekit_json",
    "version": "1.0",
    "exported_at": "2025-01-15T10:30:00"
  },
  "data": {
    "_type": "WaveformTrace",
    "data": [0.0, 0.1, 0.2, ...],
    "metadata": {
      "_type": "TraceMetadata",
      "sample_rate": 1000000000.0,
      "time_base": 1e-09,
      "vertical_scale": 0.1,
      "vertical_offset": 0.0,
      "acquisition_time": "2025-01-15T10:25:00",
      "source_file": "capture.wfm",
      "channel_name": "CH1"
    }
  }
}
```

### Specialized JSON Exports

```python
from tracekit.exporters import export_measurements, export_protocol_decode

# Export measurements with trace info
measurements = tk.measure(trace)
trace_info = {
    "source_file": "capture.wfm",
    "sample_rate": 1e9,
    "duration": 0.001
}
export_measurements(measurements, "results.json", trace_info=trace_info)

# Export protocol decode results
packets = tk.decode_uart(trace, baud_rate=115200)
export_protocol_decode(packets, "uart.json", protocol="uart")
```

## HDF5 Export

Export to HDF5 format for efficient storage of large datasets.

### Basic Usage

```python
import tracekit as tk

trace = tk.load("signal.wfm")

# Export single trace
tk.export_hdf5(trace, "trace.h5")

# Export multiple traces
tk.export_hdf5(
    {"ch1": ch1, "ch2": ch2, "ch3": ch3},
    "channels.h5"
)

# With compression
tk.export_hdf5(
    trace,
    "compressed.h5",
    compression="gzip",
    compression_opts=9
)
```

### Features

- **Efficient Binary Storage**: Compact storage for large datasets
- **Compression**: gzip or lzf compression
- **Metadata Attributes**: All metadata stored as HDF5 attributes
- **Multiple Traces**: Store multiple traces in single file
- **Chunked Storage**: Optimized for large file handling

### HDF5 Export Parameters

```python
tk.export_hdf5(
    data,                  # Trace or dict of traces
    path,                  # Output file path
    compression="gzip",    # "gzip", "lzf", or None
    compression_opts=4,    # Compression level (1-9 for gzip)
    include_metadata=True  # Include trace metadata as attributes
)
```

### HDF5 File Structure

```
waveform.h5
├── trace_data (dataset)
│   ├── @sample_rate: 1e9
│   ├── @time_base: 1e-9
│   ├── @vertical_scale: 0.1
│   ├── @vertical_offset: 0.0
│   ├── @acquisition_time: "2025-01-15T10:25:00"
│   ├── @source_file: "capture.wfm"
│   ├── @channel_name: "CH1"
│   └── @trace_type: "waveform"
└── @created: "2025-01-15T10:30:00"
```

### Appending Traces

```python
from tracekit.exporters import append_trace

# Create initial file
tk.export_hdf5(ch1, "data.h5")

# Append more traces
append_trace("data.h5", "ch2", ch2)
append_trace("data.h5", "ch3", ch3)
```

### Requirements

HDF5 export requires h5py:

```bash
pip install h5py
```

## MATLAB Export

Export to MATLAB .mat format for MATLAB/Octave compatibility.

### Basic Usage

```python
import tracekit as tk

trace = tk.load("signal.wfm")

# Export single trace
tk.export_mat(trace, "trace.mat")

# Export multiple traces
tk.export_mat(
    {"ch1": ch1, "ch2": ch2},
    "channels.mat"
)

# Use MATLAB v7.3 format (HDF5-based)
tk.export_mat(
    trace,
    "large_file.mat",
    version="7.3",
    compression=True
)
```

### Features

- **MATLAB Variable Naming**: Automatic sanitization for MATLAB compatibility
- **Metadata Struct**: Metadata exported as MATLAB struct
- **Multiple Versions**: v5 (compatible) or v7.3 (HDF5-based, for large files)
- **Time Vectors**: Automatically generates time arrays
- **Compression**: Available with v7.3 format

### MATLAB Export Parameters

```python
tk.export_mat(
    data,                  # Trace, dict, or measurements
    path,                  # Output file path
    version="7.3",         # "5" or "7.3"
    compression=True,      # Compression (v7.3 only)
    include_metadata=True  # Include trace metadata
)
```

### MATLAB Variable Structure

For a trace named "trace":

- `trace_data` - Waveform data array
- `trace_time` - Time vector array
- `trace_metadata` - Metadata struct with fields:
  - `sample_rate`
  - `time_base`
  - `num_samples`
  - `duration`
  - `vertical_scale`
  - `vertical_offset`
  - `acquisition_time`
  - `source_file`
  - `channel_name`
  - `trace_type`

### Using in MATLAB

```matlab
% Load exported data
data = load('trace.mat');

% Access waveform
plot(data.trace_time, data.trace_data);
xlabel('Time (s)');
ylabel('Voltage (V)');

% Check metadata
fprintf('Sample Rate: %.2e Hz\n', data.trace_metadata.sample_rate);
fprintf('Duration: %.6f s\n', data.trace_metadata.duration);
```

### Multiple Traces

```python
from tracekit.exporters import export_multi_trace_mat

traces = [ch1, ch2, ch3]
export_multi_trace_mat(
    traces,
    "channels.mat",
    names=["ch1", "ch2", "ch3"],
    version="7.3"
)
```

### Version Comparison

| Feature         | Version 5         | Version 7.3    |
| --------------- | ----------------- | -------------- |
| File size limit | 2 GB              | Unlimited      |
| Compression     | No                | Yes            |
| Compatibility   | All MATLAB/Octave | MATLAB R2006b+ |
| Speed           | Fast              | Moderate       |
| Requirements    | scipy             | scipy + h5py   |

### Requirements

MATLAB export requires scipy:

```bash
pip install scipy

# For v7.3 format, also need h5py
pip install h5py
```

## Export Workflow Examples

### Complete Analysis Export

```python
import tracekit as tk

# Load and analyze
trace = tk.load("capture.wfm")
freq, mag = tk.fft(trace)
measurements = tk.measure(trace)

# Export raw data
tk.export_csv(trace, "raw_data.csv")
tk.export_hdf5(trace, "raw_data.h5")

# Export analysis results
tk.export_json(measurements, "measurements.json")
tk.export_mat({"freq": freq, "mag": mag}, "spectrum.mat")
```

### Multi-Channel Export

```python
import tracekit as tk

# Load multiple channels
ch1 = tk.load("ch1.wfm")
ch2 = tk.load("ch2.wfm")
ch3 = tk.load("ch3.wfm")

# Export all formats
channels = {"ch1": ch1, "ch2": ch2, "ch3": ch3}

tk.export_hdf5(channels, "all_channels.h5")
tk.export_mat(channels, "all_channels.mat", version="7.3")

# Or use specialized multi-trace functions
from tracekit.exporters import export_multi_trace_csv, export_multi_trace_mat

export_multi_trace_csv([ch1, ch2, ch3], "channels.csv", names=["CH1", "CH2", "CH3"])
export_multi_trace_mat([ch1, ch2, ch3], "channels.mat", names=["CH1", "CH2", "CH3"])
```

### Protocol Decode Export

```python
import tracekit as tk
from tracekit.exporters import export_protocol_decode

# Decode protocol
trace = tk.load("uart_capture.wfm")
packets = tk.decode_uart(trace, baud_rate=115200)

# Export decode results
export_protocol_decode(
    packets,
    "uart_decode.json",
    protocol="uart",
    trace_info={
        "source": "uart_capture.wfm",
        "baud_rate": 115200,
        "sample_rate": trace.metadata.sample_rate
    }
)
```

### Large File Export

```python
import tracekit as tk

# Load large trace
trace = tk.load("large_capture.wfm")

# Use compressed formats for efficiency
tk.export_hdf5(
    trace,
    "large.h5",
    compression="gzip",
    compression_opts=9
)

tk.export_mat(
    trace,
    "large.mat",
    version="7.3",  # Required for >2GB
    compression=True
)

tk.export_json(
    trace,
    "large.json.gz",
    compress=True
)
```

## Format Selection Guide

Choose the right format for your use case:

| Format     | Best For                          | Pros                             | Cons                             |
| ---------- | --------------------------------- | -------------------------------- | -------------------------------- |
| **CSV**    | Human-readable data, Excel import | Universal, simple, text-based    | Large file size, no compression  |
| **JSON**   | Structured results, web APIs      | Flexible, hierarchical, readable | Large file size for arrays       |
| **HDF5**   | Large datasets, archival          | Efficient, compressed, fast      | Binary, needs h5py               |
| **MATLAB** | MATLAB/Octave analysis            | Native MATLAB format, metadata   | Needs scipy, limited to 2GB (v5) |

### Decision Tree

1. **Need human readability?** → CSV or JSON
2. **File size > 100 MB?** → HDF5 or MATLAB v7.3
3. **Using MATLAB/Octave?** → MATLAB
4. **Web/API integration?** → JSON
5. **Maximum compatibility?** → CSV
6. **Best performance?** → HDF5

## Advanced Topics

### Custom Metadata

```python
import tracekit as tk
from datetime import datetime

# Create trace with rich metadata
metadata = tk.TraceMetadata(
    sample_rate=1e9,
    vertical_scale=0.1,
    vertical_offset=0.0,
    acquisition_time=datetime.now(),
    source_file="scope_ch1.wfm",
    channel_name="CH1",
    trigger_info={
        "type": "edge",
        "level": 0.5,
        "slope": "rising"
    }
)

trace = tk.WaveformTrace(data=data, metadata=metadata)

# Metadata automatically included in all exports
tk.export_csv(trace, "with_metadata.csv")   # In comments
tk.export_json(trace, "with_metadata.json")  # In structure
tk.export_hdf5(trace, "with_metadata.h5")    # As attributes
tk.export_mat(trace, "with_metadata.mat")    # As struct
```

### Programmatic Format Selection

```python
import tracekit as tk

def export_trace(trace, base_path, formats=None):
    """Export trace to multiple formats."""
    if formats is None:
        formats = ["csv", "json", "hdf5", "mat"]

    results = {}

    for fmt in formats:
        path = f"{base_path}.{fmt}"

        try:
            if fmt == "csv":
                tk.export_csv(trace, path)
            elif fmt == "json":
                tk.export_json(trace, path)
            elif fmt == "hdf5":
                tk.export_hdf5(trace, path)
            elif fmt == "mat":
                tk.export_mat(trace, path)

            results[fmt] = path
        except ImportError as e:
            print(f"Skipping {fmt}: {e}")

    return results

# Use it
trace = tk.load("signal.wfm")
files = export_trace(trace, "output", formats=["csv", "json", "hdf5"])
```

## Error Handling

```python
import tracekit as tk

trace = tk.load("signal.wfm")

try:
    tk.export_mat(trace, "output.mat")
except ImportError:
    print("scipy not installed, using JSON instead")
    tk.export_json(trace, "output.json")

try:
    tk.export_hdf5(trace, "output.h5")
except ImportError:
    print("h5py not installed, using CSV instead")
    tk.export_csv(trace, "output.csv")
```

## NumPy NPZ Export

Export to NumPy's compressed NPZ format for Python-based workflows.

### Basic Usage

```python
import tracekit as tk

trace = tk.load("signal.wfm")

# Export single trace
tk.export_npz(trace, "trace.npz")

# Export multiple arrays
tk.export_npz(
    {
        "trace_data": trace.data,
        "time": trace.time_axis,
        "sample_rate": trace.metadata.sample_rate
    },
    "data.npz"
)
```

### Features

- **Compressed Storage**: Uses np.savez_compressed for efficient storage
- **Multiple Arrays**: Store multiple NumPy arrays in one file
- **Fast Loading**: Quick load times with np.load()
- **Python Native**: Seamless integration with NumPy workflows

### Loading NPZ Files

```python
import numpy as np

# Load exported data
data = np.load("trace.npz")

# Access arrays
trace_data = data["trace_data"]
time = data["time"]
sample_rate = data["sample_rate"]
```

## SPICE PWL Export

Export waveforms as SPICE piecewise linear (PWL) sources for circuit simulation.

### Basic Usage

```python
import tracekit as tk

trace = tk.load("signal.wfm")

# Export for SPICE
tk.export_pwl(trace, "stimulus.pwl")

# Downsample for faster simulation
tk.export_pwl(trace, "stimulus.pwl", max_points=1000)
```

### Features

- **SPICE Compatible**: Direct use in SPICE simulators (LTspice, ngspice, etc.)
- **Time-Voltage Pairs**: Standard PWL format
- **Downsampling**: Reduce points while preserving waveform shape
- **Header Comments**: Includes metadata as SPICE comments

### PWL File Format

```
* TraceKit PWL Export
* Sample Rate: 1e9 Hz
* Duration: 1e-6 s
* Samples: 1000
PWL(
  0.000000e+00 0.000000e+00
  1.000000e-09 1.234567e-01
  2.000000e-09 2.345678e-01
  ...
)
```

### Using in SPICE

```spice
* LTspice example
.include stimulus.pwl
V1 input 0 PWL FILE=stimulus.pwl
```

## Markdown Export

Export analysis results as Markdown reports with tables and embedded plots.

### Basic Usage

```python
import tracekit as tk

trace = tk.load("signal.wfm")

# Generate measurements
measurements = tk.measure(trace)

# Export as Markdown
tk.export_markdown(measurements, "report.md", title="Signal Analysis")
```

### Features

- **Human Readable**: Clean, formatted Markdown
- **Tables**: Measurement results in markdown tables
- **Plot Embedding**: Include plots as images
- **GitHub Compatible**: Renders perfectly on GitHub

## API Reference

### Top-Level Functions

- `tk.export_csv(data, path, **options)` - Export to CSV
- `tk.export_json(data, path, **options)` - Export to JSON
- `tk.export_hdf5(data, path, **options)` - Export to HDF5
- `tk.export_mat(data, path, **options)` - Export to MATLAB
- `tk.export_npz(data, path)` - Export to NumPy NPZ
- `tk.export_pwl(trace, path, **options)` - Export to SPICE PWL
- `tk.export_markdown(data, path, **options)` - Export to Markdown

### Specialized Functions

Available via `from tracekit.exporters import ...`:

- `export_multi_trace_csv(traces, path, ...)` - Multi-trace CSV
- `export_multi_trace_mat(traces, path, ...)` - Multi-trace MATLAB
- `export_measurements(measurements, path, ...)` - Measurement results
- `export_protocol_decode(packets, path, ...)` - Protocol decode results
- `append_trace(path, name, trace)` - Append to HDF5 file

## Dependencies

- **CSV Export**: No dependencies (uses stdlib)
- **JSON Export**: No dependencies (uses stdlib)
- **HDF5 Export**: Requires `h5py` (`pip install h5py`)
- **MATLAB Export**: Requires `scipy` (`pip install scipy`)
- **MATLAB v7.3**: Requires `scipy` + `h5py`

## See Also

- [Loader API](loader.md) - Loading trace files
- [Analysis API](analysis.md) - Analyzing traces
- [Reporting API](reporting.md) - Generating reports
