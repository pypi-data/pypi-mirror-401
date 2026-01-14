# Memory-Mapped Loading Guide

## Overview

TraceKit provides memory-mapped file loading for working with huge waveform files (GB+) that don't fit in RAM. Memory-mapped loading allows you to:

- **Access huge files** without loading all data into memory
- **Process data in chunks** to avoid out-of-memory (OOM) errors
- **Work with files larger than RAM** (10+ GB files on systems with 8 GB RAM)
- **Achieve fast random access** to any part of the file
- **Integrate seamlessly** with existing TraceKit loaders

## When to Use Memory-Mapped Loading

Use memory-mapped loading when:

- File size > 1 GB (automatic threshold)
- Available RAM < file size
- Processing data in chunks (FFT, statistics, protocol decoding)
- Need random access to subsets of huge files
- Working with long-duration recordings (hours/days)

Use regular loading when:

- File size < 100 MB
- Need to modify data frequently
- Working with network filesystems (performance may vary)

## Quick Start

### Basic Memory-Mapped Loading

```python
from tracekit.loaders import load_mmap

# Load huge .npy file (doesn't load data into RAM)
trace = load_mmap("10GB_capture.npy", sample_rate=1e9)

print(f"Length: {trace.length:,} samples")  # Metadata available immediately
print(f"Duration: {trace.duration:.2f} seconds")

# Access subset without loading entire file
subset = trace[1000:2000]
print(f"Mean: {np.mean(subset):.3f}")
```

### Chunked Processing

```python
from tracekit.loaders import load_mmap

# Load huge file
trace = load_mmap("huge_trace.npy", sample_rate=1e9)

# Process in chunks to avoid OOM
for chunk in trace.iter_chunks(chunk_size=1_000_000):
    # Process chunk (FFT, statistics, etc.)
    fft_result = compute_fft(chunk)
    # Only one chunk in memory at a time
```

### Overlapping Chunks (Windowed Processing)

```python
# For windowed operations (FFT with Hanning window, etc.)
for chunk in trace.iter_chunks(chunk_size=4096, overlap=2048):
    # Apply window and process
    windowed = chunk * np.hanning(len(chunk))
    spectrum = np.fft.fft(windowed)
```

## Supported File Formats

### NumPy Files (.npy)

**Recommended format** for memory-mapped loading. Auto-detects array format.

```python
from tracekit.loaders import load_mmap

# Auto-detects dtype, shape, and data offset
trace = load_mmap("waveform.npy", sample_rate=1e9)
```

### Raw Binary Files

For custom binary formats:

```python
# Load raw binary file (need to specify dtype and length)
trace = load_mmap(
    "data.f32",
    sample_rate=1e9,
    dtype=np.float32,
    length=1_000_000_000  # 1 billion samples
)
```

### CSV Files (with conversion)

Large CSV files are converted to .npy format for efficient access:

```python
from tracekit.loaders.csv_loader import load_csv

# Parses CSV once, then saves as .npy for mmap
trace = load_csv("huge_oscilloscope.csv", mmap=True)

# Returned trace is memory-mapped
for chunk in trace.iter_chunks(chunk_size=100_000):
    process(chunk)
```

### HDF5 Files

HDF5 datasets are already lazy by default via h5py:

```python
from tracekit.loaders.hdf5_loader import load_hdf5

# Uses h5py's native lazy loading
trace = load_hdf5("data.h5", mmap=True)

# HDF5 datasets are accessed on-demand
subset = trace[1000:2000]
```

## API Reference

### `load_mmap()`

Load waveform file with memory mapping.

```python
def load_mmap(
    file_path: str | Path,
    sample_rate: float | None = None,
    *,
    dtype: np.dtype | None = None,
    offset: int = 0,
    length: int | None = None,
    mode: str = "r",
    **metadata: Any,
) -> MmapWaveformTrace:
    """Load waveform file with memory mapping.

    Args:
        file_path: Path to waveform file (.npy or raw binary).
        sample_rate: Sample rate in Hz (required).
        dtype: Data type (auto-detected for .npy).
        offset: Byte offset to data start.
        length: Number of samples (auto-computed if possible).
        mode: File access mode ('r' or 'r+').
        **metadata: Additional metadata.

    Returns:
        MmapWaveformTrace for memory-mapped access.
    """
```

### `MmapWaveformTrace`

Memory-mapped waveform trace class.

**Properties:**

- `sample_rate`: Sample rate in Hz
- `length`: Number of samples
- `duration`: Duration in seconds
- `dtype`: Data type of samples
- `file_path`: Path to memory-mapped file
- `data`: Memory-mapped numpy array (lazy access)

**Methods:**

- `iter_chunks(chunk_size, overlap=0)`: Iterate in chunks
- `to_eager()`: Convert to eager WaveformTrace (loads all data)
- `close()`: Close file handle

**Example:**

```python
# Context manager ensures proper cleanup
with load_mmap("huge.npy", sample_rate=1e9) as trace:
    for chunk in trace.iter_chunks(chunk_size=1_000_000):
        process(chunk)
# File automatically closed
```

### `should_use_mmap()`

Check if file should use memory mapping based on size.

```python
from tracekit.loaders import should_use_mmap, load_mmap

if should_use_mmap("huge_file.npy"):
    trace = load_mmap("huge_file.npy", sample_rate=1e9)
else:
    trace = load("huge_file.npy", sample_rate=1e9)
```

Default threshold: 1 GB (configurable via `threshold` parameter).

## Integration with Existing Loaders

### CSV Loader

```python
from tracekit.loaders.csv_loader import load_csv

# Add mmap=True to convert to memory-mapped format
trace = load_csv("huge.csv", mmap=True)

# Returns MmapWaveformTrace backed by temporary .npy file
assert isinstance(trace, MmapWaveformTrace)
```

### HDF5 Loader

```python
from tracekit.loaders.hdf5_loader import load_hdf5

# Add mmap=True for lazy loading
trace = load_hdf5("data.h5", dataset="/waveform", mmap=True)

# Returns HDF5MmapTrace (h5py's lazy loading)
assert isinstance(trace, HDF5MmapTrace)
```

## Performance Considerations

### Memory Usage

Memory-mapped files use minimal RAM:

- **Metadata**: ~1 KB (sample rate, length, dtype, etc.)
- **Accessed data**: Only pages accessed (OS manages via page cache)
- **Chunk processing**: Only current chunk in RAM

Example: 10 GB file with 1M sample chunks uses ~4 MB RAM per chunk.

### Access Patterns

**Fast:**

- Sequential access (forward iteration)
- Large chunk sizes (aligned with page size)
- Repeated access to same regions (page cache)

**Slower:**

- Random access across entire file
- Very small chunk sizes (<4 KB)
- Network filesystems (NFS, SMB)

**Best practice:** Use chunk sizes ≥ 1 MB for optimal performance.

### Disk I/O

Memory mapping relies on the OS page cache:

- **First access**: Loads from disk (slow)
- **Subsequent access**: Served from page cache (fast)
- **Memory pressure**: OS evicts pages as needed

For best performance on huge files:

1. Process data in sequential chunks
2. Use chunk sizes appropriate for available RAM
3. Avoid accessing same file from multiple processes simultaneously

## Common Use Cases

### Case 1: FFT on Huge Signal

```python
from tracekit.loaders import load_mmap
import numpy as np

# Load 10 GB signal
trace = load_mmap("10GB_capture.npy", sample_rate=1e9)

# Compute FFT on chunks with overlap
results = []
for chunk in trace.iter_chunks(chunk_size=8192, overlap=4096):
    # Apply window
    windowed = chunk * np.hanning(len(chunk))
    # Compute FFT
    spectrum = np.fft.fft(windowed)
    results.append(spectrum)

# Combine results (average, max-hold, etc.)
avg_spectrum = np.mean(results, axis=0)
```

### Case 2: Protocol Decoding

```python
from tracekit.loaders import load_mmap
from tracekit.protocol.uart import UARTDecoder

# Load huge digital capture
trace = load_mmap("uart_capture.npy", sample_rate=100e6)

# Decode in chunks
decoder = UARTDecoder(baud_rate=115200)
frames = []

for chunk in trace.iter_chunks(chunk_size=1_000_000):
    frames.extend(decoder.decode(chunk))

print(f"Decoded {len(frames)} UART frames")
```

### Case 3: Statistics on Long Recording

```python
from tracekit.loaders import load_mmap
import numpy as np

# Load 24-hour recording
trace = load_mmap("24hr_recording.npy", sample_rate=1e6)

# Compute statistics in chunks
results = {
    'mean': [],
    'std': [],
    'min': [],
    'max': [],
}

for chunk in trace.iter_chunks(chunk_size=10_000_000):
    results['mean'].append(np.mean(chunk))
    results['std'].append(np.std(chunk))
    results['min'].append(np.min(chunk))
    results['max'].append(np.max(chunk))

# Overall statistics
print(f"Overall mean: {np.mean(results['mean']):.3f}")
print(f"Overall std: {np.mean(results['std']):.3f}")
print(f"Global min: {np.min(results['min']):.3f}")
print(f"Global max: {np.max(results['max']):.3f}")
```

### Case 4: Exporting Subsets

```python
from tracekit.loaders import load_mmap
import numpy as np

# Load huge file
trace = load_mmap("huge.npy", sample_rate=1e9)

# Export interesting subset
start = 1_000_000
end = 2_000_000
subset = trace[start:end]

# Save subset
np.save("subset.npy", subset)
```

## Limitations

1. **Read-only by default**: Use `mode='r+'` for read-write (not recommended)
2. **NPZ files**: Not directly memory-mappable (extract array first)
3. **Fortran-ordered arrays**: Not supported (resave in C order)
4. **Network filesystems**: Performance may vary (local filesystems recommended)
5. **Multi-dimensional arrays**: Automatically flattened to 1D

## Troubleshooting

### "File too small for requested data"

**Cause:** Requested length exceeds actual file size.

**Solution:** Check file size or omit `length` parameter for auto-detection.

### "Cannot memory-map NPZ files"

**Cause:** NPZ is a compressed archive, not directly mappable.

**Solution:** Extract array first:

```python
data = np.load("file.npz")["array"]
np.save("file.npy", data)
trace = load_mmap("file.npy", sample_rate=1e9)
```

### Slow performance

**Causes:**

- Network filesystem (NFS, SMB)
- Very small chunk sizes
- Random access pattern

**Solutions:**

- Copy file to local disk
- Increase chunk size (≥1 MB)
- Use sequential access

## See Also

- Lazy Loading Guide - Alternative lazy loading approach (coming soon)
- Performance Tips - General performance optimization (coming soon)
- Example Scripts - Complete working examples (see `examples/` directory)
- API Reference: `tracekit.loaders.mmap_loader`

## References

- NumPy memmap: https://numpy.org/doc/stable/reference/generated/numpy.memmap.html
- Memory mapping: https://en.wikipedia.org/wiki/Memory-mapped_file
- API-017: Lazy Loading for Huge Files (internal spec)
