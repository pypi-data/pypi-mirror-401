# 05_advanced - Advanced Topics

> **Prerequisites**: [01_basics](../01_basics/) through [04_protocol_decoding](../04_protocol_decoding/)
> **Time**: 45-60 minutes

Advanced analysis techniques for handling complex scenarios,
optimizing performance, and working with challenging data.

## Learning Objectives

By completing these examples, you will learn how to:

1. **Handle NaN results** - Understand and manage invalid measurements
2. **Use lazy loading** - Process large files efficiently
3. **Enable GPU** - Accelerate computation with CUDA
4. **Ensemble analysis** - Combine multiple analysis methods
5. **Cross-domain correlation** - Link time and frequency analysis
6. **Eye diagrams** - Analyze serial link quality
7. **Batch processing** - Process multiple files efficiently

## Examples in This Section

### 01_nan_handling.py

**What it does**: Handle NaN (Not a Number) measurement results

**Concepts covered**:

- Why measurements return NaN
- Detecting NaN values
- Fallback strategies
- Signal characterization
- Error recovery

**Run it**:

```bash
uv run python examples/05_advanced/01_nan_handling.py
```

**Expected output**: Demonstrations of NaN handling strategies

---

### 02_lazy_evaluation.py

**What it does**: Process large files without loading into memory

**Concepts covered**:

- Lazy loading mode
- Chunked processing
- Memory-efficient analysis
- Streaming computations

**Run it**:

```bash
uv run python examples/05_advanced/02_lazy_evaluation.py
```

**Expected output**: Analysis of large file with minimal memory

---

### 03_gpu_acceleration.py

**What it does**: Accelerate analysis with GPU computing

**Concepts covered**:

- GPU availability detection
- CUDA-accelerated FFT
- Performance comparison
- Fallback to CPU

**Run it**:

```bash
uv run python examples/05_advanced/03_gpu_acceleration.py
```

**Expected output**: Performance comparison CPU vs GPU

---

### 04_ensemble_analysis.py

**What it does**: Combine multiple analysis methods

**Concepts covered**:

- Running multiple analyses
- Combining results
- Confidence scoring
- Voting strategies

**Run it**:

```bash
uv run python examples/05_advanced/04_ensemble_analysis.py
```

**Expected output**: Combined analysis results with confidence

---

### 05_cross_domain.py

**What it does**: Correlate time and frequency domain results

**Concepts covered**:

- Time-domain measurement
- Frequency-domain measurement
- Cross-correlation
- Feature linking

**Run it**:

```bash
uv run python examples/05_advanced/05_cross_domain.py
```

**Expected output**: Correlated analysis results

---

### 06_eye_diagram.py

**What it does**: Create and analyze eye diagrams

**Concepts covered**:

- Eye diagram generation
- Eye opening measurements
- Jitter analysis
- Mask testing

**Run it**:

```bash
uv run python examples/05_advanced/06_eye_diagram.py
```

**Expected output**: Eye diagram plot and metrics

---

### 07_batch_processing.py

**What it does**: Process multiple waveform files

**Concepts covered**:

- File discovery
- Parallel processing
- Result aggregation
- Progress reporting

**Run it**:

```bash
uv run python examples/05_advanced/07_batch_processing.py
```

**Expected output**: Summary of batch processing results

---

## Quick Reference

### NaN Handling

```python
import math
import tracekit as tk

freq = tk.measure_frequency(trace)

if math.isnan(freq):
    print("Measurement not applicable to this signal")
    # Try alternative approach
    edges = tk.find_edges(trace)
    if len(edges) >= 2:
        period = edges[1][0] - edges[0][0]
        freq = 1.0 / period
```

### Lazy Loading

```python
import tracekit as tk

# Enable lazy loading
trace = tk.load("huge_file.wfm", lazy=True)

# Metadata available immediately
print(f"Samples: {trace.metadata.num_samples}")

# Data loaded on demand
chunk = trace.data[0:10000]

# Process in chunks
for chunk in tk.iter_chunks(trace, chunk_size=100000):
    process(chunk)
```

### GPU Acceleration

```python
from tracekit.analyzers.spectral import compute_fft

# Check GPU availability
import tracekit as tk
if tk.gpu_available():
    print("GPU acceleration available")

# Use GPU for FFT
spectrum = compute_fft(trace, use_gpu=True)

# Or set environment variable
import os
os.environ["TRACEKIT_GPU"] = "true"
```

### Eye Diagram

```python
from tracekit.analyzers.eye import create_eye_diagram, analyze_eye

# Create eye diagram at specified bit rate
eye = create_eye_diagram(trace, bit_rate=1e9)

# Analyze eye metrics
metrics = analyze_eye(eye)

print(f"Eye height: {metrics.eye_height*1e3:.2f} mV")
print(f"Eye width: {metrics.eye_width*1e12:.2f} ps")
print(f"Jitter: {metrics.jitter_pp*1e12:.2f} ps pk-pk")
```

### Batch Processing

```python
from pathlib import Path
import tracekit as tk

# Find all waveform files
files = list(Path("data/").glob("*.wfm"))

results = []
for file in files:
    trace = tk.load(file)
    freq = tk.measure_frequency(trace)
    results.append({"file": file.name, "frequency": freq})

# Aggregate
import statistics
frequencies = [r["frequency"] for r in results if not math.isnan(r["frequency"])]
print(f"Mean frequency: {statistics.mean(frequencies):.2f} Hz")
print(f"Std dev: {statistics.stdev(frequencies):.2f} Hz")
```

## Common Issues

**Issue**: NaN results on valid-looking signal

**Solution**: Check signal characteristics. Some measurements need specific signal types (e.g., rise time needs pulse, not sine).

---

**Issue**: Lazy loading is slow

**Solution**: Access data sequentially when possible. Random access patterns defeat caching.

---

**Issue**: GPU not detected

**Solution**: Verify CUDA installation:

```bash
nvidia-smi  # Check GPU
python -c "import cupy"  # Check cupy
```

---

**Issue**: Eye diagram looks wrong

**Solution**: Verify bit rate matches signal. Try auto-detection:

```python
eye = create_eye_diagram(trace)  # Auto-detect bit rate
```

---

## Estimated Time

- **Quick review**: 20 minutes
- **Hands-on practice**: 45-60 minutes

## Next Steps

Continue to advanced features:

- **[06_expert_api](../06_expert_api/)** - Expert mode and discovery

Or revisit specific topics:

- **[NaN Handling Guide](../../docs/guides/nan-handling.md)** - Complete NaN reference
- **[GPU Acceleration Guide](../../docs/guides/gpu-acceleration.md)** - GPU setup

## See Also

- [User Guide: Best Practices](../../docs/user-guide.md#best-practices)
- [API Reference](../../docs/api/index.md)
