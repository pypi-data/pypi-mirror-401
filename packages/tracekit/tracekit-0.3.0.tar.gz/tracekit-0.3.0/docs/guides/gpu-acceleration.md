# GPU Acceleration in TraceKit

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

TraceKit provides optional GPU acceleration for computationally intensive operations using CuPy, with automatic fallback to NumPy when GPU is unavailable.

## Features

- **Transparent Fallback**: Automatically uses NumPy if CuPy is not installed
- **Lazy Initialization**: GPU resources allocated only when first needed
- **Memory Safe**: Automatic data transfer between CPU and GPU
- **Configurable**: Control GPU usage via environment variable
- **Zero Breaking Changes**: Existing code works without modification

## Supported Operations

### FFT/IFFT

- `gpu.fft()` - Fast Fourier Transform
- `gpu.ifft()` - Inverse FFT
- `gpu.rfft()` - Real FFT (memory efficient)
- `gpu.irfft()` - Inverse real FFT

**Use cases**: Spectral analysis, frequency domain filtering, signal decomposition

### Convolution

- `gpu.convolve()` - 1D convolution with configurable modes

**Use cases**: Signal filtering, smoothing, feature detection

### Correlation

- `gpu.correlate()` - Cross-correlation for pattern matching

**Use cases**: Pattern detection, template matching, signal alignment

### Matrix Operations

- `gpu.dot()` - Dot product
- `gpu.matmul()` - Matrix multiplication

**Use cases**: Linear algebra, pattern matching, dimensionality reduction

### Statistical Analysis

- `gpu.histogram()` - Fast histogram computation

**Use cases**: Distribution analysis, signal quality metrics, statistical profiling

## Installation

### Basic Installation (CPU-only)

```bash
pip install tracekit
```

### With GPU Acceleration

For NVIDIA GPUs with CUDA 11.x:

```bash
pip install tracekit cupy-cuda11x
```

For NVIDIA GPUs with CUDA 12.x:

```bash
pip install tracekit cupy-cuda12x
```

**Note**: CuPy requires NVIDIA GPU with CUDA toolkit installed. See [CuPy installation guide](https://docs.cupy.dev/en/stable/install.html) for details.

## Usage

### Basic Usage

```python
from tracekit.core import gpu
import numpy as np

# Create signal
signal = np.random.randn(100000)

# GPU-accelerated FFT (automatic fallback to NumPy if no GPU)
spectrum = gpu.rfft(signal)

# GPU-accelerated convolution
kernel = np.ones(5) / 5
smoothed = gpu.convolve(signal, kernel, mode='same')

# Check if GPU is being used
if gpu.gpu_available:
    print("Using GPU acceleration")
else:
    print("Using CPU (NumPy) fallback")
```

### Force CPU-Only Mode

```python
from tracekit.core import GPUBackend

# Create CPU-only backend
cpu_backend = GPUBackend(force_cpu=True)

# All operations use NumPy
result = cpu_backend.fft(signal)
```

### Environment Variable Control

Disable GPU globally via environment variable:

```bash
# Disable GPU
export TRACEKIT_USE_GPU=0
python your_script.py

# Enable GPU (default)
export TRACEKIT_USE_GPU=1
python your_script.py
```

## Performance Guidelines

### When GPU Acceleration Helps

GPU acceleration provides significant speedup for:

1. **Large Arrays**: Operations on arrays with >10,000 elements
2. **Batch Processing**: Repeated operations on multiple signals
3. **FFT Operations**: Especially for lengths >100,000 samples
4. **Convolution**: With large kernels (>100 elements)

### When CPU May Be Faster

For small arrays (<1,000 elements), CPU may be faster due to:

- GPU memory transfer overhead
- Kernel launch latency
- CPU cache efficiency for small data

### Benchmark Example

```python
import time
import numpy as np
from tracekit.core import GPUBackend, gpu

# Create backends
cpu_backend = GPUBackend(force_cpu=True)
gpu_backend = gpu

# Large signal
signal = np.random.randn(1_000_000)

# CPU benchmark
start = time.perf_counter()
cpu_result = cpu_backend.rfft(signal)
cpu_time = time.perf_counter() - start

# GPU benchmark
start = time.perf_counter()
gpu_result = gpu_backend.rfft(signal)
gpu_time = time.perf_counter() - start

print(f"CPU: {cpu_time*1000:.1f}ms")
print(f"GPU: {gpu_time*1000:.1f}ms")
print(f"Speedup: {cpu_time/gpu_time:.1f}x")
```

## API Reference

### GPUBackend Class

```python
class GPUBackend:
    """GPU acceleration backend with automatic NumPy fallback."""
    def __init__(self, force_cpu: bool = False):
        """Initialize GPU backend.

        Args:
            force_cpu: If True, always use CPU even if GPU available.
        """
    @property
    def gpu_available(self) -> bool:
        """Check if GPU acceleration is available."""
    def fft(self, data, n=None, axis=-1, norm=None):
        """Compute FFT with GPU acceleration."""
    def ifft(self, data, n=None, axis=-1, norm=None):
        """Compute inverse FFT with GPU acceleration."""
    def rfft(self, data, n=None, axis=-1, norm=None):
        """Compute real FFT with GPU acceleration."""
    def irfft(self, data, n=None, axis=-1, norm=None):
        """Compute inverse real FFT with GPU acceleration."""
    def convolve(self, data, kernel, mode='full'):
        """Compute convolution with GPU acceleration."""
    def correlate(self, a, v, mode='full'):
        """Compute correlation with GPU acceleration."""
    def histogram(self, data, bins=10, range=None, density=False):
        """Compute histogram with GPU acceleration."""
    def dot(self, a, b):
        """Compute dot product with GPU acceleration."""
    def matmul(self, a, b):
        """Compute matrix multiplication with GPU acceleration."""
```

### Module-Level Singleton

```python
from tracekit.core import gpu

# Pre-configured singleton for convenient access
gpu.fft(signal)
gpu.gpu_available  # Check availability
```

## Troubleshooting

### CuPy Import Errors

**Error**: `ImportError: No module named 'cupy'`

**Solution**: Install CuPy for your CUDA version:

```bash
pip install cupy-cuda11x  # CUDA 11.x
pip install cupy-cuda12x  # CUDA 12.x
```

### CUDA Not Found

**Error**: `RuntimeError: CUDA not available`

**Solution**: Install NVIDIA CUDA toolkit or use CPU-only mode:

```python
export TRACEKIT_USE_GPU=0
```

### GPU Memory Errors

**Error**: `cupy.cuda.memory.OutOfMemoryError`

**Solution**:

1. Reduce array sizes or use chunked processing
2. Force CPU mode for memory-intensive operations
3. Clear GPU cache: `gpu._cp.get_default_memory_pool().free_all_blocks()`

### Version Compatibility

**Error**: `RuntimeError: CuPy version mismatch`

**Solution**: Ensure CuPy version matches CUDA version:

```bash
# Check CUDA version
nvidia-smi

# Install matching CuPy
pip install cupy-cuda11x  # For CUDA 11.x
pip install cupy-cuda12x  # For CUDA 12.x
```

## Best Practices

1. **Check Availability First**: Always check `gpu.gpu_available` before relying on GPU speedup
2. **Batch Operations**: Process multiple signals in sequence to amortize GPU initialization
3. **Array Size Matters**: Use GPU for arrays >10,000 elements for best results
4. **Profile Your Code**: Benchmark CPU vs GPU for your specific use case
5. **Graceful Degradation**: Write code that works with both CPU and GPU backends

## Examples

See `examples/gpu_acceleration_example.py` for comprehensive usage examples including:

- Basic FFT operations
- Signal smoothing with convolution
- Pattern matching with correlation
- Statistical analysis with histograms
- Performance benchmarking

## Integration with TraceKit

The GPU backend integrates seamlessly with TraceKit's analysis modules:

```python
from tracekit.core import gpu
from tracekit.analyzers.spectral import fft
from tracekit import WaveformTrace

# Load trace
trace = WaveformTrace.load("signal.csv")

# Use GPU-accelerated analysis
# (Future integration planned)
```

## Future Enhancements

Planned features for future releases:

- Direct integration with `tracekit.analyzers.spectral`
- GPU-accelerated filtering operations
- Multi-GPU support for parallel processing
- Automatic optimal backend selection based on array size

## See Also

- [ANALYSIS_API.md](../api/analysis.md) - Analysis functions (benefit from GPU)
- [visualization_api.md](../api/visualization.md) - Visualization (uses NumPy arrays)

## References

- [CuPy Documentation](https://docs.cupy.dev/)
- [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)
- [NumPy API Reference](https://numpy.org/doc/stable/reference/)
