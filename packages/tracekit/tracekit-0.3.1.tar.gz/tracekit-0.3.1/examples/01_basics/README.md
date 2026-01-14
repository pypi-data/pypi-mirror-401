# 01_basics - Getting Started with TraceKit

> **Prerequisites**: None
> **Time**: 30-45 minutes

Welcome to TraceKit basics! This section teaches fundamental concepts for
loading, analyzing, and visualizing waveform data.

## Learning Objectives

By completing these examples, you will learn how to:

1. **Load waveforms** - Load data from various file formats
2. **Basic measurements** - Measure frequency, amplitude, rise time
3. **Plot waveforms** - Visualize signals
4. **Export data** - Save results to CSV, HDF5
5. **Generate reports** - Create PDF/HTML reports

## Examples in This Section

### 01_load_waveform.py

**What it does**: Load waveform data from various file formats

**Concepts covered**:

- Auto-format detection
- WaveformTrace objects
- Accessing metadata
- Multi-channel loading

**Run it**:

```bash
uv run python examples/01_basics/01_load_waveform.py
```

**Expected output**: Console output showing loaded trace properties

---

### 02_basic_measurements.py

**What it does**: Perform time-domain measurements on waveforms

**Concepts covered**:

- Frequency measurement
- Rise/fall time measurement
- Amplitude statistics
- Duty cycle calculation

**Run it**:

```bash
uv run python examples/01_basics/02_basic_measurements.py
```

**Expected output**: Measurement results with units

---

### 03_plot_waveform.py

**What it does**: Create visualizations of waveform data

**Concepts covered**:

- Basic plotting
- Plot customization
- Multiple traces
- Saving plots to file

**Run it**:

```bash
uv run python examples/01_basics/03_plot_waveform.py
```

**Expected output**: Display window with waveform plot (or saved file)

---

### 04_export_data.py

**What it does**: Export waveform data to various formats

**Concepts covered**:

- CSV export
- HDF5 export
- NumPy NPZ export
- Export options

**Run it**:

```bash
uv run python examples/01_basics/04_export_data.py
```

**Expected output**: Exported files in working directory

---

### 05_generate_report.py

**What it does**: Generate analysis reports

**Concepts covered**:

- Report configuration
- PDF generation
- HTML generation
- Custom templates

**Run it**:

```bash
uv run python examples/01_basics/05_generate_report.py
```

**Expected output**: Generated report file(s)

---

## Quick Reference

### Loading Data

```python
import tracekit as tk

# Auto-detect format
trace = tk.load("capture.wfm")

# Specify format
trace = tk.load("data.bin", format="tektronix")

# Load all channels
channels = tk.load_all_channels("multi.wfm")

# Lazy loading for large files
trace = tk.load("huge.wfm", lazy=True)
```

### Basic Measurements

```python
# Frequency
freq = tk.measure_frequency(trace)

# Rise time (10-90%)
rise = tk.measure_rise_time(trace)

# Custom thresholds
rise_2080 = tk.measure_rise_time(trace, 0.2, 0.8)

# Amplitude
amp = tk.measure_amplitude(trace)
stats = tk.analyze_amplitude(trace)
```

### Plotting

```python
# Quick plot
tk.plot(trace)

# Save to file
tk.plot(trace, output="waveform.png")

# With title
tk.plot(trace, title="My Signal")
```

### Exporting

```python
# To CSV
tk.export(trace, "data.csv")

# To HDF5
tk.export(trace, "data.h5")

# To NumPy
tk.export(trace, "data.npz")
```

## Common Issues

**Issue**: File format not recognized

**Solution**: Specify format explicitly:

```python
trace = tk.load("file.dat", format="tektronix")
```

---

**Issue**: Measurement returns NaN

**Solution**: Check signal has required characteristics. See [NaN Handling Guide](../../docs/guides/nan-handling.md).

---

**Issue**: Plot window doesn't appear

**Solution**: Use `tk.plot(trace, output="file.png")` to save to file instead.

---

## Estimated Time

- **Quick review**: 15 minutes
- **Hands-on practice**: 30-45 minutes

## Next Steps

Once you're comfortable with basics, continue to:

**[02_digital_analysis](../02_digital_analysis/)** - Clock recovery, edge detection, bus decoding

Or explore specific topics:

- **[03_spectral_analysis](../03_spectral_analysis/)** - FFT and frequency domain
- **[04_protocol_decoding](../04_protocol_decoding/)** - Serial protocol decoding

## See Also

- [Getting Started Guide](../../docs/getting-started.md)
- [Loading Waveforms Guide](../../docs/guides/loading-waveforms.md)
- [API Reference: Loader](../../docs/api/loader.md)
