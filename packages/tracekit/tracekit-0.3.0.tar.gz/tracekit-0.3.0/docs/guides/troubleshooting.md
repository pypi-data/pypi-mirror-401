# Troubleshooting Guide

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

Solutions for common TraceKit issues.

## File Loading Issues

### File format not recognized

**Error**: `TK-FMT-201: Cannot determine file format`

**Solutions**:

1. Check supported formats:

   ```python
   import tracekit as tk
   print(tk.get_supported_formats())
   ```

2. Specify format explicitly:

   ```python
   trace = tk.load("data.bin", format="tektronix")
   ```

3. Verify file is not corrupted:

   ```bash
   file data.wfm  # Check file type
   ```

### File not found

**Error**: `TK-FILE-101: File not found`

**Solutions**:

1. Use absolute paths:

   ```python
   from pathlib import Path
   trace = tk.load(Path("/full/path/to/file.wfm"))
   ```

2. Verify file exists:

   ```python
   from pathlib import Path
   path = Path("file.wfm")
   if path.exists():
       trace = tk.load(path)
   ```

### Out of memory loading large file

**Error**: `TK-LOAD-304: Memory limit exceeded`

**Solutions**:

1. Use lazy loading:

   ```python
   trace = tk.load("huge_file.wfm", lazy=True)
   ```

2. Process in chunks:

   ```python
   for chunk in tk.iter_chunks("huge_file.wfm", chunk_size=1_000_000):
       process(chunk)
   ```

3. Load specific channel only:

   ```python
   trace = tk.load("multi.wfm", channel="CH1")
   ```

---

## Measurement Issues

### Measurement returns NaN

**Issue**: `tk.measure_frequency(trace)` returns `nan`

**Causes**:

- Signal doesn't meet measurement criteria
- DC signal (no transitions)
- Wrong threshold level

**Solutions**:

1. Check signal characteristics:

   ```python
   stats = tk.analyze_amplitude(trace)
   print(f"Min: {stats.minimum}, Max: {stats.maximum}")
   ```

2. Verify signal has transitions:

   ```python
   edges = tk.find_edges(trace)
   print(f"Found {len(edges)} edges")
   ```

3. Adjust threshold:

   ```python
   freq = tk.measure_frequency(trace, threshold=0.5)
   ```

See [NaN Handling Guide](nan-handling.md) for complete coverage.

### Unexpected measurement values

**Issue**: Measurements don't match expected values

**Solutions**:

1. Verify sample rate:

   ```python
   print(f"Sample rate: {trace.metadata.sample_rate}")
   ```

2. Check units:

   ```python
   print(f"Units: {trace.metadata.units}")
   ```

3. Inspect the signal:

   ```python
   tk.plot(trace)  # Visual inspection
   ```

### Rise time measurement fails

**Error**: Rise time returns NaN

**Causes**:

- Signal is not a pulse
- Incorrect threshold settings
- Noisy signal

**Solutions**:

1. Check signal type:

   ```python
   # Rise time needs a pulse, not a sine
   from tracekit.testing import generate_pulse
   pulse = generate_pulse()  # This will work
   ```

2. Adjust thresholds:

   ```python
   rise = tk.measure_rise_time(trace, low=0.2, high=0.8)
   ```

<a id="edge-detection"></a>

### Edge detection issues

**Issue**: `tk.find_edges()` returns too few or too many edges

**Causes**:

- Incorrect threshold level
- Noisy signal
- Signal not digital

**Solutions**:

1. Adjust threshold:

   ```python
   edges = tk.find_edges(trace, threshold=0.5)  # Adjust as needed
   ```

2. Filter noisy signals:

   ```python
   from scipy import signal
   filtered = signal.medfilt(trace.data, kernel_size=5)
   edges = tk.find_edges(filtered)
   ```

3. Verify signal quality:

   ```python
   stats = tk.analyze_amplitude(trace)
   print(f"Peak-to-peak: {stats.peak_to_peak}")
   ```

---

## Protocol Decoding Issues

### UART shows garbage data

**Issue**: Decoded UART messages are garbled

**Solutions**:

1. Verify baud rate:

   ```python
   from tracekit.inference import detect_baud_rate
   detected = detect_baud_rate(trace)
   print(f"Detected baud rate: {detected}")
   ```

2. Check data bits, parity, stop bits:

   ```python
   decoder = UARTDecoder(
       baud_rate=115200,
       data_bits=8,
       parity="none",
       stop_bits=1
   )
   ```

3. Check signal polarity:

   ```python
   decoder = UARTDecoder(baud_rate=115200, inverted=True)
   ```

### SPI decoding fails

**Issue**: No transactions decoded

**Solutions**:

1. Verify CPOL/CPHA settings:

   ```python
   # Try all combinations
   for cpol in [0, 1]:
       for cpha in [0, 1]:
           decoder = SPIDecoder(clock=clk, mosi=mosi, cpol=cpol, cpha=cpha)
           txns = decoder.decode()
           if txns:
               print(f"Works with CPOL={cpol}, CPHA={cpha}")
   ```

2. Check channel assignments:

   ```python
   channels = tk.load_all_channels("capture.wfm")
   print(f"Available channels: {list(channels.keys())}")
   ```

### I2C misses transactions

**Issue**: Some I2C transactions not decoded

**Solutions**:

1. Check threshold levels:

   ```python
   decoder = I2CDecoder(sda=sda, scl=scl, threshold=1.5)
   ```

2. Verify signal quality:

   ```python
   # Check for clean edges
   scl_edges = tk.find_edges(scl)
   sda_edges = tk.find_edges(sda)
   ```

---

## Performance Issues

### Analysis is slow

**Solutions**:

1. Enable GPU acceleration:

   ```python
   import os
   os.environ["TRACEKIT_GPU"] = "true"

   # Or per-function
   spectrum = compute_fft(trace, use_gpu=True)
   ```

2. Use appropriate FFT size:

   ```python
   # Smaller = faster
   spectrum = compute_fft(trace, nfft=1024)
   ```

3. Reduce data size:

   ```python
   # Downsample if high resolution not needed
   trace_downsampled = tk.downsample(trace, factor=10)
   ```

### GPU not detected

**Issue**: `tk.gpu_available()` returns `False`

**Solutions**:

1. Check CUDA installation:

   ```bash
   nvidia-smi
   nvcc --version
   ```

2. Install cupy:

   ```bash
   uv pip install cupy-cuda12x  # For CUDA 12.x
   ```

3. Verify cupy works:

   ```python
   import cupy
   print(cupy.cuda.runtime.getDeviceCount())
   ```

---

## Report Generation Issues

### PDF generation fails

**Error**: `TK-RPT-803: Export format error`

**Solutions**:

1. Install dependencies:

   ```bash
   uv pip install reportlab
   ```

2. Use HTML instead:

   ```python
   save_html_report(report, "report.html")
   ```

### Report missing plots

**Issue**: Report has empty plot areas

**Solutions**:

1. Install matplotlib:

   ```bash
   uv pip install matplotlib
   ```

2. Check plot generation:

   ```python
   config = ReportConfig(include_plots=True, plot_dpi=150)
   report = generate_report(trace, config=config)
   ```

---

## Installation Issues

### Import error

**Error**: `ModuleNotFoundError: No module named 'tracekit'`

**Solutions**:

1. Install in development mode:

   ```bash
   uv pip install -e .
   ```

2. Verify installation:

   ```bash
   uv run python -c "import tracekit; print(tracekit.__version__)"
   ```

### Missing dependency

**Error**: `ImportError: No module named 'xxx'`

**Solutions**:

1. Sync dependencies:

   ```bash
   uv sync
   ```

2. Install specific extras:

   ```bash
   uv sync --extra viz  # For visualization
   uv sync --extra gpu  # For GPU support
   ```

---

## Getting More Help

### Enable debug logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

import tracekit as tk
trace = tk.load("file.wfm")  # Will show detailed logs
```

### Get system information

```bash
uv run tracekit version --verbose
```

### Check error codes

See [Error Codes Reference](../error-codes.md) for complete error documentation.

### Report issues

When reporting issues, include:

- TraceKit version
- Python version
- Operating system
- Complete error message
- Minimal reproducing example

## See Also

- [Error Codes](../error-codes.md) - Complete error reference
- [NaN Handling Guide](nan-handling.md) - NaN-specific troubleshooting
- [GPU Acceleration](gpu-acceleration.md) - GPU setup guide
