# Supported File Formats

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

TraceKit supports loading waveform data from multiple oscilloscope vendors and generic formats.

## Quick Reference

| Format        | Extension      | Vendor/Standard | Status  | Notes                |
| ------------- | -------------- | --------------- | ------- | -------------------- |
| Tektronix WFM | `.wfm`         | Tektronix       | Full    | DPO/MSO series       |
| Rigol WFM     | `.wfm`         | Rigol           | Full    | DS/MSO series        |
| LeCroy TRC    | `.trc`         | LeCroy/Teledyne | Partial | Binary waveform      |
| Keysight BIN  | `.bin`         | Keysight        | Planned | InfiniiVision series |
| Sigrok        | `.sr`          | Sigrok          | Full    | PulseView captures   |
| VCD           | `.vcd`         | Standard        | Full    | Value Change Dump    |
| CSV           | `.csv`         | Generic         | Full    | Comma-separated      |
| NumPy         | `.npz`, `.npy` | NumPy           | Full    | Array format         |
| HDF5          | `.h5`, `.hdf5` | HDF Group       | Full    | Hierarchical data    |
| MATLAB        | `.mat`         | MathWorks       | Full    | v7.3 (HDF5-based)    |
| WAV           | `.wav`         | Audio           | Full    | Audio waveform       |
| JSON          | `.json`        | Generic         | Full    | With base64 data     |

## Oscilloscope Formats

### Tektronix WFM

**Extensions**: `.wfm`
**Status**: Full Support
**Supported Models**: DPO2000, DPO3000, DPO4000, MSO4000, DPO5000, DPO7000, MSO70000

```python
import tracekit as tk

# Auto-detect Tektronix format
trace = tk.load("capture.wfm")

# Explicitly specify vendor
trace = tk.load("capture.wfm", format="tektronix")
```

**Metadata Extracted**:

- Sample rate
- Vertical scale and offset
- Horizontal scale and position
- Channel information
- Acquisition mode
- Record length
- Trigger settings

**Multi-Channel**:

```python
# Load all channels from multi-channel capture
channels = tk.load_all_channels("multi.wfm")
for name, trace in channels.items():
    print(f"{name}: {len(trace.data)} samples")
```

### Rigol WFM

**Extensions**: `.wfm`
**Status**: Full Support
**Supported Models**: DS1000, DS2000, DS4000, MSO5000

```python
# Rigol WFM format (auto-detected by header)
trace = tk.load("rigol_capture.wfm")

# Force Rigol format
trace = tk.load("capture.wfm", format="rigol")
```

**Note**: Tektronix and Rigol both use `.wfm` extension. TraceKit auto-detects based on file header magic bytes.

### LeCroy TRC

**Extensions**: `.trc`
**Status**: Partial Support
**Supported Models**: WaveSurfer, WaveRunner, WavePro

```python
trace = tk.load("capture.trc")
```

**Limitations**:

- Segmented acquisitions not yet supported
- Some advanced trigger metadata not parsed

### Keysight (Planned)

**Extensions**: `.bin`, `.h5`
**Status**: Planned
**Target Models**: InfiniiVision 1000X, 2000X, 3000X, 4000X

## Logic Analyzer Formats

### Sigrok

**Extensions**: `.sr`
**Status**: Full Support
**Source**: PulseView, sigrok-cli

```python
# Load Sigrok capture (returns DigitalTrace)
trace = tk.load("logic_capture.sr")

# Access channel names
print(f"Channels: {trace.channel_names}")
```

**Multi-Channel Access**:

```python
channels = tk.load_all_channels("capture.sr")
for name, digital in channels.items():
    edges = tk.find_edges(digital)
    print(f"{name}: {len(edges)} edges")
```

### VCD (Value Change Dump)

**Extensions**: `.vcd`
**Status**: Full Support
**Standard**: IEEE 1364 (Verilog)

```python
# Load VCD file
trace = tk.load("simulation.vcd")

# VCD files can contain many signals
channels = tk.load_all_channels("simulation.vcd")
```

**Notes**:

- Supports 4-state logic (0, 1, X, Z)
- Variable-width signals
- Hierarchical signal names

### Saleae (Planned)

**Extensions**: `.logicdata`
**Status**: Planned
**Source**: Saleae Logic

## Generic Formats

### CSV

**Extensions**: `.csv`
**Status**: Full Support

```python
# Standard format: time,voltage columns
trace = tk.load("data.csv")

# Custom column names
trace = tk.load(
    "data.csv",
    time_column="Time_s",
    voltage_column="CH1_V"
)

# Multiple channels
trace = tk.load("data.csv", voltage_column="CH1")
trace2 = tk.load("data.csv", voltage_column="CH2")
```

**Supported Formats**:

```csv
# Format 1: Time and voltage
time,voltage
0.0,0.1
1e-9,0.15
...

# Format 2: Time in first column, multiple channels
time,CH1,CH2,CH3
0.0,0.1,0.2,0.3
...

# Format 3: Sample index and voltage
sample,voltage
0,0.1
1,0.15
...
```

**Options**:

```python
trace = tk.load(
    "data.csv",
    delimiter=",",           # or "\t" for TSV
    skip_rows=1,             # Skip header rows
    time_column="time",      # Column name or index
    voltage_column="voltage",
    sample_rate=100e6,       # If no time column
)
```

### NumPy

**Extensions**: `.npz`, `.npy`
**Status**: Full Support

```python
# Single array (.npy) - requires sample_rate
trace = tk.load("data.npy", sample_rate=100e6)

# Compressed archive (.npz)
trace = tk.load("data.npz")
```

**NPZ Format Expected**:

```python
import numpy as np

# Save in expected format
np.savez(
    "data.npz",
    data=waveform_array,
    sample_rate=100e6,
    # Optional metadata
    channel="CH1",
    units="V",
)
```

### HDF5

**Extensions**: `.h5`, `.hdf5`
**Status**: Full Support

```python
# Load from default dataset
trace = tk.load("data.h5")

# Specify dataset path
trace = tk.load("data.h5", dataset="/waveforms/ch1")

# List available datasets
datasets = tk.list_hdf5_datasets("data.h5")
print(datasets)
```

**Expected Structure**:

```
/
├── data           # Waveform samples (required)
├── sample_rate    # Sample rate in Hz (required)
├── channel        # Channel name (optional)
├── units          # Voltage units (optional)
└── metadata/      # Additional metadata group (optional)
```

### MATLAB

**Extensions**: `.mat`
**Status**: Full Support (v7.3 HDF5-based)

```python
trace = tk.load("data.mat")

# Specify variable name
trace = tk.load("data.mat", variable="waveform")
```

**Expected Variables**:

- `data` or `waveform`: Sample array
- `sample_rate` or `fs`: Sample rate
- `t` (optional): Time axis

### WAV Audio

**Extensions**: `.wav`
**Status**: Full Support

```python
# Load audio waveform
trace = tk.load("audio.wav")

# Multi-channel audio
channels = tk.load_all_channels("stereo.wav")
left = channels["Left"]
right = channels["Right"]
```

**Notes**:

- Sample rate from WAV header
- Supports 8/16/24/32-bit samples
- Stereo and multi-channel

### JSON

**Extensions**: `.json`
**Status**: Full Support

```python
trace = tk.load("data.json")
```

**Expected Format**:

```json
{
    "data": [0.1, 0.15, 0.2, ...],
    "sample_rate": 100000000,
    "channel": "CH1",
    "units": "V"
}
```

For large data, use base64 encoding:

```json
{
  "data_base64": "QUJDREVGRw==",
  "dtype": "float64",
  "sample_rate": 100000000
}
```

## Format Detection

### Auto-Detection

TraceKit automatically detects format by:

1. File extension
2. Magic bytes (file header)
3. Content structure

```python
# Auto-detect works for most files
trace = tk.load("unknown.wfm")  # Detects Tek vs Rigol from header
```

### Check Supported Formats

```python
# List all supported formats
formats = tk.get_supported_formats()
for fmt in formats:
    print(f"{fmt.name}: {fmt.extensions} - {fmt.status}")
```

### Force Format

```python
# Override auto-detection
trace = tk.load("file.bin", format="tektronix")
```

## Writing/Export

TraceKit can export to most formats:

```python
import tracekit as tk

trace = tk.load("capture.wfm")

# Export to various formats
tk.export(trace, "output.csv")
tk.export(trace, "output.h5")
tk.export(trace, "output.npz")
tk.export(trace, "output.mat")
tk.export(trace, "output.json")

# With options
tk.export(trace, "output.h5", compression="gzip")
tk.export(trace, "output.csv", include_time=True)
```

## Adding Custom Loaders

Extend TraceKit with custom format support:

```python
from tracekit.loaders import register_loader, BaseLoader

class MyFormatLoader(BaseLoader):
    extensions = [".myf"]
    magic_bytes = b"MYF\x00"

    def load(self, path, **kwargs):
        # Parse file and return WaveformTrace
        ...

# Register the loader
register_loader(MyFormatLoader)

# Now .myf files work automatically
trace = tk.load("data.myf")
```

## See Also

- [Loading Waveforms Guide](../guides/loading-waveforms.md)
- [Export API Reference](../api/export.md)
- [Loader API Reference](../api/loader.md)
