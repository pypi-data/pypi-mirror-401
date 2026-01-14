# TraceKit Expert Guide

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

Advanced topics for power users: custom measurements, analysis pipelines, plugin development, and framework extension.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Creating Custom Measurements](#creating-custom-measurements)
3. [Building Analysis Pipelines](#building-analysis-pipelines)
4. [Developing TraceKit Plugins](#developing-tracekit-plugins)
5. [Extending the Framework](#extending-the-framework)
6. [Performance Optimization](#performance-optimization)
7. [Contributing to TraceKit](#contributing-to-tracekit)

---

## Introduction

### When to Use Advanced Features

This guide is for users who need to:

- **Define custom measurements** for domain-specific analysis
- **Build reusable pipelines** for repeated workflows
- **Develop plugins** to extend TraceKit's capabilities
- **Optimize performance** for large datasets or real-time processing
- **Contribute** to TraceKit's development

### Prerequisites

- Familiarity with TraceKit basics (see [Loading Waveforms Guide](loading-waveforms.md))
- Python 3.12+ programming experience
- Understanding of signal processing concepts
- Knowledge of NumPy and SciPy

### Expert API Overview

TraceKit provides 8 core Expert APIs:

| API                     | Purpose                                     | Reference |
| ----------------------- | ------------------------------------------- | --------- |
| **Pipeline**            | Composable trace transformations            | API-001   |
| **Composition**         | Functional operators (compose, pipe, curry) | API-002   |
| **Streaming**           | Process large files in chunks               | API-003   |
| **TraceTransformer**    | Base class for custom transformations       | API-004   |
| **Results**             | Access intermediate computation results     | API-005   |
| **Algorithm Registry**  | Register custom algorithms                  | API-006   |
| **Plugin Architecture** | Third-party extensions via entry points     | API-007   |
| **Custom Measurements** | Define and register measurements            | API-008   |

---

## Creating Custom Measurements

### Overview

Custom measurements extend TraceKit's built-in capabilities with domain-specific analysis functions. They integrate seamlessly with batch processing, reporting, and export.

### Defining Measurement Algorithms

Measurement functions accept a `WaveformTrace` and return a numeric value:

```python
import tracekit as tk
import numpy as np

def crest_factor(trace, **kwargs):
    """Calculate crest factor: peak / RMS.

    Args:
        trace: WaveformTrace to measure.
        **kwargs: Additional parameters (not used).

    Returns:
        Crest factor as ratio.
    """
    peak = np.abs(trace.data).max()
    rms = np.sqrt(np.mean(trace.data ** 2))

    if rms == 0:
        return 0.0

    return peak / rms
```

**Key points:**

- First parameter must be `WaveformTrace`
- Accept `**kwargs` for extensibility
- Return a single numeric value
- Handle edge cases (division by zero, empty data)
- Include clear docstrings

### Registering Custom Measurements

Register measurements globally for use throughout TraceKit:

```python
import tracekit as tk

# Register the measurement
tk.register_measurement(
    name='crest_factor',
    func=crest_factor,
    units='ratio',
    category='amplitude',
    description='Crest factor (peak/RMS ratio)',
    tags=['amplitude', 'quality', 'power']
)

# Use the measurement
trace = tk.load("signal.wfm")
cf = tk.measure_custom(trace, 'crest_factor')
print(f"Crest factor: {cf:.2f}")
```

**Registration parameters:**

- `name`: Unique identifier (lowercase, underscores)
- `func`: Callable measurement function
- `units`: Units of measurement (e.g., 'V', 'Hz', 's', 'ratio', 'dB')
- `category`: Category for organization ('amplitude', 'timing', 'frequency', 'quality')
- `description`: Human-readable description
- `tags`: List of tags for search and categorization

### Unit Testing Custom Code

Test custom measurements thoroughly:

```python
import pytest
import numpy as np
import tracekit as tk

def test_crest_factor_sine_wave():
    """Test crest factor on pure sine wave."""
    # Generate sine wave
    t = np.linspace(0, 1, 1000)
    data = np.sin(2 * np.pi * 10 * t)
    trace = tk.WaveformTrace(
        data=data,
        metadata=tk.TraceMetadata(sample_rate=1000.0)
    )

    # Calculate crest factor
    cf = crest_factor(trace)

    # Sine wave crest factor ≈ √2
    expected = np.sqrt(2)
    assert abs(cf - expected) < 0.01

def test_crest_factor_dc_signal():
    """Test crest factor on DC signal."""
    data = np.ones(1000) * 3.3
    trace = tk.WaveformTrace(
        data=data,
        metadata=tk.TraceMetadata(sample_rate=1e6)
    )

    cf = crest_factor(trace)

    # DC signal: peak = RMS, so CF = 1
    assert abs(cf - 1.0) < 0.01

def test_crest_factor_zero_signal():
    """Test crest factor handles zero signal."""
    data = np.zeros(1000)
    trace = tk.WaveformTrace(
        data=data,
        metadata=tk.TraceMetadata(sample_rate=1e6)
    )

    cf = crest_factor(trace)
    assert cf == 0.0  # Should handle division by zero
```

### Integration with TraceKit

Custom measurements work with all TraceKit features:

#### Batch Processing

```python
import tracekit as tk

# Register custom measurement
tk.register_measurement(
    name='snr_estimate',
    func=signal_to_noise_ratio,
    units='dB',
    category='quality'
)

# Batch process files
results = []
for file in ["capture1.wfm", "capture2.wfm", "capture3.wfm"]:
    trace = tk.load(file)
    snr = tk.measure_custom(trace, 'snr_estimate')
    results.append({'file': file, 'snr': snr})

# Export to CSV
import pandas as pd
df = pd.DataFrame(results)
df.to_csv('snr_results.csv', index=False)
```

#### Report Generation

```python
# Include custom measurements in reports
report = tk.Report()
report.add_measurement('crest_factor', cf)
report.add_measurement('snr_estimate', snr)
report.generate('analysis_report.pdf')
```

### Advanced Example: Adaptive Measurement

Measurements can accept configuration parameters:

```python
def adaptive_threshold(trace, percentile=95, **kwargs):
    """Calculate adaptive threshold based on percentile.

    Args:
        trace: WaveformTrace to measure.
        percentile: Percentile for threshold (0-100).
        **kwargs: Additional parameters.

    Returns:
        Threshold value in signal units.
    """
    return np.percentile(np.abs(trace.data), percentile)

# Register with default parameters
tk.register_measurement(
    name='adaptive_threshold_95',
    func=lambda trace: adaptive_threshold(trace, percentile=95),
    units='V',
    category='amplitude',
    description='95th percentile adaptive threshold'
)

# Use with custom percentile
def measure_with_params(trace, percentile):
    return adaptive_threshold(trace, percentile=percentile)
```

---

## Building Analysis Pipelines

### Pipeline Fundamentals

Pipelines chain trace transformations in a reusable, composable way:

```python
import tracekit as tk

# Create pipeline with multiple stages
pipeline = tk.Pipeline([
    ('lowpass', tk.LowPassFilter(cutoff=1e6)),
    ('normalize', tk.scale(factor=1.0)),  # Wrapped function
    ('remove_dc', lambda t: tk.subtract(t, tk.mean(t))),
])

# Process trace
trace = tk.load("noisy_signal.wfm")
result = pipeline.transform(trace)
```

**Pipeline features:**

- **Named stages** for identification and debugging
- **Sequential execution** with intermediate result caching
- **Reusable** across multiple traces
- **Serializable** for saving/loading workflows

### Creating Custom Transformers

Transformers implement the `TraceTransformer` interface:

```python
import tracekit as tk
import numpy as np

class OutlierClipper(tk.TraceTransformer):
    """Clip values beyond N standard deviations.

    Attributes:
        n_sigma: Number of standard deviations for clipping.
    """

    def __init__(self, n_sigma=3.0):
        """Initialize clipper.

        Args:
            n_sigma: Number of standard deviations (default: 3.0).
        """
        self.n_sigma = n_sigma

    def transform(self, trace):
        """Clip outliers in trace.

        Args:
            trace: Input WaveformTrace.

        Returns:
            WaveformTrace with clipped data.
        """
        mean = trace.data.mean()
        std = trace.data.std()

        lower = mean - self.n_sigma * std
        upper = mean + self.n_sigma * std

        clipped = np.clip(trace.data, lower, upper)

        # Cache intermediate results
        self._cache_intermediate('lower_bound', lower)
        self._cache_intermediate('upper_bound', upper)
        self._cache_intermediate('clipped_count',
                                np.sum((trace.data < lower) | (trace.data > upper)))

        return tk.WaveformTrace(
            data=clipped,
            metadata=trace.metadata
        )
```

### Stateful Transformers with Fit/Transform

Transformers can learn parameters from reference traces:

```python
class AdaptiveNormalizer(tk.TraceTransformer):
    """Normalize trace using statistics from reference."""

    def __init__(self):
        self.mean_ = None
        self.std_ = None

    def fit(self, trace):
        """Learn normalization parameters from reference trace.

        Args:
            trace: Reference WaveformTrace.

        Returns:
            Self for method chaining.
        """
        self.mean_ = trace.data.mean()
        self.std_ = trace.data.std()
        return self

    def transform(self, trace):
        """Normalize trace using learned parameters.

        Args:
            trace: Input WaveformTrace.

        Returns:
            Normalized WaveformTrace.

        Raises:
            ValueError: If fit() has not been called.
        """
        if self.mean_ is None or self.std_ is None:
            raise ValueError("Must call fit() before transform()")

        normalized = (trace.data - self.mean_) / self.std_

        return tk.WaveformTrace(
            data=normalized,
            metadata=trace.metadata
        )

# Usage
normalizer = AdaptiveNormalizer()
normalizer.fit(reference_trace)

# Apply to multiple traces
results = [normalizer.transform(trace) for trace in test_traces]
```

### Chaining Operations

#### Using Pipeline

```python
# Build complex pipeline
pipeline = tk.Pipeline([
    ('detrend', TrendRemover()),
    ('clip', OutlierClipper(n_sigma=3.0)),
    ('smooth', tk.LowPassFilter(cutoff=1e6)),
    ('normalize', AdaptiveNormalizer()),
])

# Fit stateful transformers
pipeline.fit(reference_trace)

# Transform multiple traces
processed = [pipeline.transform(t) for t in traces]
```

#### Accessing Intermediate Results

```python
# Transform with pipeline
result = pipeline.transform(trace)

# Access intermediate stages
detrended = pipeline.get_intermediate('detrend')
clipped = pipeline.get_intermediate('clip')
smoothed = pipeline.get_intermediate('smooth')

# Get transformer details
clipper = pipeline.get_transformer('clip')
print(f"Clipped {clipper.get_intermediate_result('clipped_count')} samples")
```

### Functional Composition Patterns

TraceKit supports functional programming patterns:

#### Compose (right-to-left)

```python
# Create composable functions
def double(t):
    return tk.WaveformTrace(data=t.data * 2, metadata=t.metadata)

def add_one(t):
    return tk.WaveformTrace(data=t.data + 1, metadata=t.metadata)

# Compose: add_one(double(trace))
composed = tk.compose(add_one, double)
result = composed(trace)
```

#### Pipe (left-to-right)

```python
# Pipe data through transformations (more readable)
result = tk.pipe(
    trace,
    double,
    add_one,
    lambda t: tk.scale(t, factor=0.5)
)
```

#### Curry (partial application)

```python
# Create specialized functions via currying
scale_by_2 = tk.curry(tk.scale, factor=2.0)
offset_by_1 = tk.curry(tk.offset, offset=1.0)

# Use curried functions
result = tk.pipe(trace, scale_by_2, offset_by_1)
```

#### Composable Decorator

```python
# Make any function composable
@tk.make_composable
def custom_transform(trace, gain=1.0, offset=0.0):
    data = trace.data * gain + offset
    return tk.WaveformTrace(data=data, metadata=trace.metadata)

# Chain with >> operator
result = (trace
          >> custom_transform(gain=2.0)
          >> tk.low_pass(cutoff=1e6))
```

### Performance Optimization

#### Lazy Evaluation

Defer computation until results are needed:

```python
from tracekit.streaming import load_trace_chunks

# Process file in chunks
analyzer = tk.StreamingAnalyzer()

for chunk in load_trace_chunks("large_file.wfm", chunk_size=10000):
    analyzer.accumulate_statistics(chunk)

# Get final statistics without loading entire file
stats = analyzer.get_statistics()
```

#### Parallel Processing

Process multiple files in parallel:

```python
from concurrent.futures import ProcessPoolExecutor

def process_file(filename):
    """Process single file through pipeline."""
    trace = tk.load(filename)
    return pipeline.transform(trace)

# Process files in parallel
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_file, filenames))
```

#### Pipeline Caching

Cache intermediate results to avoid recomputation:

```python
# Enable result caching
pipeline = tk.Pipeline([
    ('lowpass', tk.LowPassFilter(cutoff=1e6)),
    ('normalize', AdaptiveNormalizer()),
], cache_intermediates=True)

# First transform caches results
result1 = pipeline.transform(trace)

# Access cached intermediates without recomputation
filtered = pipeline.get_intermediate('lowpass')
```

---

## Developing TraceKit Plugins

### Plugin Architecture Overview

TraceKit uses Python entry points for plugin discovery:

```
Entry Point Groups:
- tracekit.decoders    → Protocol decoders
- tracekit.loaders     → File format loaders
- tracekit.exporters   → Export format handlers
- tracekit.analyzers   → Custom analyzers
```

Plugins are:

- **Auto-discovered** at import time
- **Lazily loaded** on first use
- **Isolated** (failures don't crash main app)
- **Versioned** for compatibility tracking

### Creating a Plugin from Scratch

Use the template generator:

```bash
# Generate plugin skeleton
python -c "
from pathlib import Path
import tracekit as tk

plugin_dir = tk.generate_plugin_template(
    name='my_custom_decoder',
    plugin_type='decoder',
    output_dir=Path('plugins/my_decoder'),
    author='Your Name',
    description='Custom protocol decoder for MyProtocol'
)
print(f'Plugin created at {plugin_dir}')
"
```

Generated structure:

```
plugins/my_decoder/
├── __init__.py                 # Plugin metadata
├── my_custom_decoder.py        # Main implementation
├── tests/
│   ├── __init__.py
│   └── test_my_custom_decoder.py
├── README.md                   # Usage documentation
└── pyproject.toml              # Packaging config
```

### Custom Protocol Decoders

Implement protocol decoding logic:

```python
"""Custom protocol decoder implementation."""

from __future__ import annotations
import numpy as np
from numpy.typing import NDArray

class MyCustomDecoder:
    """Decoder for MyProtocol.

    Protocol Specification:
    - Start bit: 0
    - Data: 8 bits
    - Parity: Even
    - Stop bit: 1

    Example:
        >>> decoder = MyCustomDecoder(sample_rate=1_000_000, baudrate=9600)
        >>> frames = decoder.decode(digital_signal)
        >>> for frame in frames:
        ...     print(f"Data: 0x{frame['data']:02X}")
    """

    def __init__(self, *, sample_rate: float, baudrate: int = 9600):
        """Initialize decoder.

        Args:
            sample_rate: Sample rate in Hz.
            baudrate: Baud rate in bits/second.
        """
        self.sample_rate = sample_rate
        self.baudrate = baudrate
        self.samples_per_bit = int(sample_rate / baudrate)

    def decode(self, signal: NDArray[np.uint8]) -> list[dict[str, object]]:
        """Decode protocol frames from digital signal.

        Args:
            signal: Digital signal (0/1 values).

        Returns:
            List of decoded frames.

        Raises:
            ValueError: If signal is empty or invalid.
        """
        if len(signal) == 0:
            raise ValueError("Signal cannot be empty")

        frames = []
        i = 0

        while i < len(signal):
            # Find start bit (falling edge)
            if signal[i] == 0:
                # Extract frame
                frame_start = i

                # Skip start bit
                i += self.samples_per_bit

                # Read 8 data bits
                data = 0
                for bit_idx in range(8):
                    if i >= len(signal):
                        break

                    # Sample middle of bit
                    bit_sample = i + self.samples_per_bit // 2
                    if bit_sample < len(signal):
                        bit = signal[bit_sample]
                        data |= (bit << bit_idx)

                    i += self.samples_per_bit

                # Read parity bit
                if i < len(signal):
                    parity_sample = i + self.samples_per_bit // 2
                    if parity_sample < len(signal):
                        parity = signal[parity_sample]
                    i += self.samples_per_bit

                # Read stop bit
                if i < len(signal):
                    stop_sample = i + self.samples_per_bit // 2
                    if stop_sample < len(signal):
                        stop = signal[stop_sample]
                    i += self.samples_per_bit

                # Validate frame
                expected_parity = bin(data).count('1') % 2  # Even parity
                if parity == expected_parity and stop == 1:
                    frames.append({
                        'timestamp': frame_start / self.sample_rate,
                        'data': data,
                        'parity_ok': True,
                    })
            else:
                i += 1

        return frames
```

### Custom File Format Loaders

Implement file format loading:

```python
"""Custom file format loader."""

from __future__ import annotations
import struct
from pathlib import Path
import numpy as np
from numpy.typing import NDArray

class CustomFormatLoader:
    """Loader for custom binary format.

    File Format:
    - Header: 16 bytes
        - Magic: 4 bytes ('CUST')
        - Version: 2 bytes
        - Channels: 2 bytes
        - Sample rate: 4 bytes (float)
        - Sample count: 4 bytes
    - Data: Interleaved channel samples (float32)

    Example:
        >>> loader = CustomFormatLoader()
        >>> data = loader.load(Path('capture.cust'))
        >>> print(f"Loaded {len(data)} channels")
    """

    MAGIC = b'CUST'
    VERSION = 1

    def load(self, file_path: Path) -> dict[str, NDArray[np.float64]]:
        """Load data from custom format file.

        Args:
            file_path: Path to file.

        Returns:
            Dictionary mapping channel names to data arrays.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If file format is invalid.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with file_path.open('rb') as f:
            # Read header
            magic = f.read(4)
            if magic != self.MAGIC:
                raise ValueError(f"Invalid magic bytes: {magic}")

            version = struct.unpack('<H', f.read(2))[0]
            if version != self.VERSION:
                raise ValueError(f"Unsupported version: {version}")

            num_channels = struct.unpack('<H', f.read(2))[0]
            sample_rate = struct.unpack('<f', f.read(4))[0]
            sample_count = struct.unpack('<I', f.read(4))[0]

            # Read interleaved data
            total_samples = num_channels * sample_count
            raw_data = struct.unpack(f'<{total_samples}f',
                                     f.read(total_samples * 4))

            # De-interleave channels
            data = {}
            for ch_idx in range(num_channels):
                channel_data = np.array(
                    raw_data[ch_idx::num_channels],
                    dtype=np.float64
                )
                data[f'CH{ch_idx + 1}'] = channel_data

        return data

    @staticmethod
    def can_load(file_path: Path) -> bool:
        """Check if this loader can handle the file.

        Args:
            file_path: Path to file.

        Returns:
            True if file has correct magic bytes.
        """
        if not file_path.exists():
            return False

        try:
            with file_path.open('rb') as f:
                magic = f.read(4)
                return magic == CustomFormatLoader.MAGIC
        except Exception:
            return False
```

### Publishing Plugins

#### Package Configuration (pyproject.toml)

```toml
[project]
name = "tracekit-my-decoder"
version = "0.1.0"
description = "Custom protocol decoder for TraceKit"
requires-python = ">=3.12"
dependencies = [
    "tracekit>=0.1.0",
    "numpy>=1.26.0",
]

# Entry point for plugin discovery
[project.entry-points."tracekit.decoders"]
my_custom_decoder = "my_custom_decoder:MyCustomDecoder"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

#### Publishing to PyPI

```bash
# Build package
uv build

# Test installation locally
uv pip install dist/tracekit_my_decoder-0.1.0-py3-none-any.whl

# Publish to PyPI
uv publish
```

#### Installing Plugin

```bash
# Install from PyPI
pip install tracekit-my-decoder

# Plugin is auto-discovered
python -c "
import tracekit as tk
plugins = tk.list_plugins()
print(plugins['tracekit.decoders'])
"
```

---

## Extending the Framework

### Custom Exporters

Create exporters for custom file formats:

```python
"""Custom CSV exporter with metadata."""

from pathlib import Path
import numpy as np
from numpy.typing import NDArray
import csv

class EnhancedCSVExporter:
    """Export to CSV with metadata header.

    Format:
    - Metadata section (# comments)
    - Column headers
    - Data rows

    Example:
        >>> exporter = EnhancedCSVExporter()
        >>> exporter.export(data, Path('output.csv'), metadata={'fs': 1e6})
    """

    def export(
        self,
        data: dict[str, NDArray[np.float64]],
        output_path: Path,
        *,
        metadata: dict[str, object] | None = None,
    ) -> None:
        """Export data to enhanced CSV.

        Args:
            data: Channel data dictionary.
            output_path: Output file path.
            metadata: Optional metadata to include in header.

        Raises:
            ValueError: If data is empty.
        """
        if not data:
            raise ValueError("Data cannot be empty")

        with output_path.open('w', newline='') as f:
            writer = csv.writer(f)

            # Write metadata header
            if metadata:
                for key, value in metadata.items():
                    writer.writerow([f'# {key}: {value}'])
                writer.writerow([])

            # Write column headers
            channels = sorted(data.keys())
            writer.writerow(['Sample'] + channels)

            # Write data rows
            num_samples = len(next(iter(data.values())))
            for i in range(num_samples):
                row = [i] + [data[ch][i] for ch in channels]
                writer.writerow(row)

# Register exporter
from tracekit.exporters import register_exporter

register_exporter('enhanced_csv', EnhancedCSVExporter())
```

### Custom Visualizations

Create specialized visualization functions:

```python
"""Custom visualization for eye diagrams."""

import matplotlib.pyplot as plt
import numpy as np
from tracekit.core.types import WaveformTrace

def plot_eye_diagram_advanced(
    trace: WaveformTrace,
    symbol_rate: float,
    *,
    num_symbols: int = 2,
    num_traces: int = 100,
    colormap: str = 'viridis',
    output_path: str | None = None,
) -> None:
    """Plot eye diagram with density coloring.

    Args:
        trace: Input waveform.
        symbol_rate: Symbol rate in Hz.
        num_symbols: Number of symbols per trace (default: 2).
        num_traces: Maximum traces to overlay (default: 100).
        colormap: Matplotlib colormap name.
        output_path: Optional path to save figure.

    Example:
        >>> trace = tk.load('digital_signal.wfm')
        >>> plot_eye_diagram_advanced(
        ...     trace,
        ...     symbol_rate=1e6,
        ...     num_symbols=2,
        ...     output_path='eye_diagram.png'
        ... )
    """
    samples_per_symbol = int(trace.metadata.sample_rate / symbol_rate)
    samples_per_trace = samples_per_symbol * num_symbols

    # Extract overlapping traces
    traces = []
    for i in range(0, len(trace.data) - samples_per_trace, samples_per_symbol):
        if len(traces) >= num_traces:
            break
        traces.append(trace.data[i:i + samples_per_trace])

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create time axis
    t = np.linspace(0, num_symbols / symbol_rate, samples_per_trace)

    # Plot traces with density-based coloring
    for idx, trace_seg in enumerate(traces):
        alpha = 0.3  # Semi-transparent for density effect
        ax.plot(t * 1e6, trace_seg,
                color=plt.cm.get_cmap(colormap)(idx / len(traces)),
                alpha=alpha,
                linewidth=0.5)

    ax.set_xlabel('Time (μs)')
    ax.set_ylabel('Amplitude (V)')
    ax.set_title(f'Eye Diagram ({symbol_rate / 1e6:.1f} MHz symbol rate)')
    ax.grid(True, alpha=0.3)

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()
```

### Algorithm Registry

Register custom algorithms for framework-wide use:

```python
"""Custom edge detection algorithm."""

import tracekit as tk
import numpy as np

def schmitt_trigger_edges(
    data: np.ndarray,
    *,
    low_threshold: float = 0.3,
    high_threshold: float = 0.7,
    **kwargs
) -> list[int]:
    """Detect edges using Schmitt trigger with hysteresis.

    Args:
        data: Input signal.
        low_threshold: Lower threshold (normalized).
        high_threshold: Upper threshold (normalized).
        **kwargs: Additional parameters.

    Returns:
        List of edge sample indices.
    """
    edges = []
    state = data[0] > high_threshold

    for i, val in enumerate(data):
        if state:
            # Currently high, check for falling edge
            if val < low_threshold:
                edges.append(i)
                state = False
        else:
            # Currently low, check for rising edge
            if val > high_threshold:
                edges.append(i)
                state = True

    return edges

# Register in algorithm registry
tk.register_algorithm(
    'schmitt_trigger',
    schmitt_trigger_edges,
    category='edge_detector',
    validate=True
)

# Use registered algorithm
trace = tk.load('digital_signal.wfm')
edges = tk.get_algorithm('edge_detector', 'schmitt_trigger')(
    trace.data,
    low_threshold=0.3,
    high_threshold=0.7
)
```

### Extension Points

TraceKit provides extension points throughout the framework:

#### Custom Window Functions

```python
"""Custom window function for FFT."""

import numpy as np

def custom_tukey_window(n: int, alpha: float = 0.5, **kwargs) -> np.ndarray:
    """Tukey (tapered cosine) window.

    Args:
        n: Window length.
        alpha: Taper fraction (0-1).
        **kwargs: Additional parameters.

    Returns:
        Window coefficients.
    """
    x = np.linspace(0, 1, n)
    window = np.ones(n)

    # Taper first alpha/2 samples
    taper_len = int(alpha * n / 2)
    window[:taper_len] = 0.5 * (
        1 + np.cos(np.pi * (2 * x[:taper_len] / alpha - 1))
    )

    # Taper last alpha/2 samples
    window[-taper_len:] = 0.5 * (
        1 + np.cos(np.pi * (2 * (1 - x[-taper_len:]) / alpha - 1))
    )

    return window

# Register window function
tk.register_algorithm('tukey', custom_tukey_window, category='window_func')

# Use in FFT
trace = tk.load('signal.wfm')
result = tk.fft(trace, window='tukey', alpha=0.3)
```

#### Custom Triggers

```python
"""Custom trigger condition."""

from tracekit.triggering.base import TriggerCondition

class PatternTrigger(TriggerCondition):
    """Trigger on specific bit pattern.

    Attributes:
        pattern: Expected bit pattern (list of 0/1).
        tolerance: Number of allowed bit errors.
    """

    def __init__(self, pattern: list[int], tolerance: int = 0):
        self.pattern = np.array(pattern, dtype=np.uint8)
        self.tolerance = tolerance

    def check(self, signal: np.ndarray, index: int) -> bool:
        """Check if pattern matches at index.

        Args:
            signal: Digital signal.
            index: Current sample index.

        Returns:
            True if pattern matches within tolerance.
        """
        if index + len(self.pattern) > len(signal):
            return False

        segment = signal[index:index + len(self.pattern)]
        errors = np.sum(segment != self.pattern)

        return errors <= self.tolerance

# Use custom trigger
trigger = PatternTrigger(pattern=[1, 0, 1, 0, 1, 1], tolerance=1)
trigger_indices = tk.find_triggers(digital_trace, trigger)
```

---

## Performance Optimization

### Profiling TraceKit Workflows

Identify performance bottlenecks:

```python
"""Profile analysis workflow."""

import tracekit as tk
import cProfile
import pstats
from io import StringIO

def analysis_workflow(filename):
    """Example workflow to profile."""
    trace = tk.load(filename)

    # Apply filters
    filtered = tk.low_pass(trace, cutoff=1e6)

    # Spectral analysis
    fft_result = tk.fft(filtered)
    thd = tk.thd(filtered)
    snr = tk.snr(filtered)

    # Time domain measurements
    rise_time = tk.rise_time(filtered)
    freq = tk.frequency(filtered)

    return {
        'thd': thd,
        'snr': snr,
        'rise_time': rise_time,
        'frequency': freq,
    }

# Profile the workflow
profiler = cProfile.Profile()
profiler.enable()

result = analysis_workflow('large_capture.wfm')

profiler.disable()

# Print statistics
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```

### Memory Management

Handle large datasets efficiently:

```python
"""Memory-efficient batch processing."""

import tracekit as tk
from tracekit.streaming import load_trace_chunks

def process_large_file(filename: str, chunk_size: int = 100000):
    """Process large file in chunks.

    Args:
        filename: File to process.
        chunk_size: Samples per chunk.

    Returns:
        Aggregated statistics.
    """
    analyzer = tk.StreamingAnalyzer()

    # Process in chunks
    for chunk in load_trace_chunks(filename, chunk_size=chunk_size):
        # Apply lightweight processing per chunk
        filtered = tk.low_pass(chunk, cutoff=1e6)

        # Accumulate statistics
        analyzer.accumulate_statistics(filtered)

    # Get final results without loading full file
    return analyzer.get_statistics()

# Check memory before processing
available = tk.get_available_memory()
file_size = estimate_file_size('large_capture.wfm')

if file_size > available * 0.8:  # Leave 20% headroom
    print("Using chunked processing")
    result = process_large_file('large_capture.wfm')
else:
    print("Using standard processing")
    trace = tk.load('large_capture.wfm')
    result = analyze_full_trace(trace)
```

### GPU Acceleration

Leverage GPU for compute-intensive operations:

```python
"""GPU-accelerated processing."""

from tracekit.core import gpu
import numpy as np

def gpu_accelerated_analysis(trace):
    """Use GPU for FFT and convolution.

    Args:
        trace: Input waveform.

    Returns:
        Analysis results.
    """
    # Check GPU availability
    if gpu.gpu_available:
        print("Using GPU acceleration")
    else:
        print("GPU not available, using NumPy fallback")

    # GPU-accelerated FFT (automatic fallback)
    spectrum = gpu.rfft(trace.data)

    # GPU-accelerated convolution
    kernel = np.ones(51) / 51  # Moving average kernel
    smoothed = gpu.convolve(trace.data, kernel, mode='same')

    # GPU-accelerated correlation
    template = create_template()
    correlation = gpu.correlate(trace.data, template, mode='valid')

    return {
        'spectrum': spectrum,
        'smoothed': smoothed,
        'correlation': correlation,
    }

# Enable GPU globally
import os
os.environ['TRACEKIT_USE_GPU'] = '1'

# Or disable for debugging
os.environ['TRACEKIT_USE_GPU'] = '0'
```

See [GPU Acceleration Guide](gpu-acceleration.md) for detailed configuration.

### Lazy Loading Strategies

Defer computation until needed:

```python
"""Lazy evaluation for analysis pipelines."""

from functools import lru_cache
import tracekit as tk

class LazyAnalysisPipeline:
    """Pipeline with lazy computation caching.

    Results are computed only when accessed and cached for reuse.
    """

    def __init__(self, trace):
        self.trace = trace
        self._cache = {}

    @property
    @lru_cache(maxsize=1)
    def filtered(self):
        """Lazily compute filtered trace."""
        print("Computing filtered trace...")
        return tk.low_pass(self.trace, cutoff=1e6)

    @property
    @lru_cache(maxsize=1)
    def spectrum(self):
        """Lazily compute FFT."""
        print("Computing FFT...")
        return tk.fft(self.filtered)

    @property
    @lru_cache(maxsize=1)
    def thd(self):
        """Lazily compute THD."""
        print("Computing THD...")
        return tk.thd(self.filtered)

    @property
    @lru_cache(maxsize=1)
    def measurements(self):
        """Lazily compute all measurements."""
        print("Computing measurements...")
        return {
            'rise_time': tk.rise_time(self.filtered),
            'frequency': tk.frequency(self.filtered),
            'amplitude': tk.amplitude(self.filtered),
        }

# Usage
trace = tk.load('signal.wfm')
pipeline = LazyAnalysisPipeline(trace)

# Only computes when accessed
print(f"THD: {pipeline.thd}")  # Triggers computation
print(f"THD: {pipeline.thd}")  # Uses cached result
```

### Parallel Processing

Process multiple files concurrently:

```python
"""Parallel batch processing."""

from concurrent.futures import ProcessPoolExecutor, as_completed
import tracekit as tk
from pathlib import Path

def process_single_file(filepath: Path) -> dict:
    """Process single file.

    Args:
        filepath: File to process.

    Returns:
        Analysis results.
    """
    try:
        trace = tk.load(str(filepath))

        return {
            'file': filepath.name,
            'frequency': tk.frequency(trace),
            'amplitude': tk.amplitude(trace),
            'thd': tk.thd(trace),
            'status': 'success',
        }
    except Exception as e:
        return {
            'file': filepath.name,
            'status': 'failed',
            'error': str(e),
        }

def batch_process_parallel(
    file_pattern: str,
    max_workers: int = 4
) -> list[dict]:
    """Process files in parallel.

    Args:
        file_pattern: Glob pattern for files.
        max_workers: Number of parallel workers.

    Returns:
        List of results.
    """
    files = list(Path('.').glob(file_pattern))
    results = []

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(process_single_file, f): f
            for f in files
        }

        # Collect results as they complete
        for future in as_completed(futures):
            filepath = futures[future]
            try:
                result = future.result()
                results.append(result)
                print(f"Completed: {filepath.name}")
            except Exception as e:
                print(f"Failed: {filepath.name} - {e}")

    return results

# Process all WFM files with 4 workers
results = batch_process_parallel('*.wfm', max_workers=4)

# Export to CSV
import pandas as pd
df = pd.DataFrame(results)
df.to_csv('batch_results.csv', index=False)
```

---

## Contributing to TraceKit

### Development Setup

Clone and set up the development environment:

```bash
# Clone repository
git clone https://github.com/lair-click-bats/tracekit.git
cd tracekit

# Install with development dependencies
uv pip install -e ".[dev]"

# Verify installation
uv run pytest tests/unit -x --maxfail=5
```

### Testing Guidelines

#### Running Tests

```bash
# Run unit tests (fast, isolated)
uv run pytest tests/unit -v

# Run with coverage
uv run pytest tests/unit --cov=src/tracekit --cov-report=term-missing

# Run specific test modules
uv run pytest tests/unit/analyzers -v
uv run pytest tests/unit/loaders -v

# Run compliance tests (IEEE/JEDEC standards)
uv run pytest tests/compliance -v

# Run in parallel (faster on multi-core)
uv run pytest tests/unit -n 4
```

#### Writing Tests

Use pytest with factory fixtures:

```python
"""Test custom measurement."""

import pytest
import numpy as np
import tracekit as tk

# Module-level markers (required)
pytestmark = [pytest.mark.unit, pytest.mark.analyzer]

def test_crest_factor_sine_wave(signal_factory):
    """Test crest factor on sine wave."""
    # Use factory to generate test signal
    signal, metadata = signal_factory(
        signal_type='sine',
        frequency=1000,
        amplitude=1.0,
        duration=1.0,
        sample_rate=10000
    )

    trace = tk.WaveformTrace(data=signal, metadata=metadata)
    cf = crest_factor(trace)

    # Sine wave CF = √2
    assert abs(cf - np.sqrt(2)) < 0.01

def test_crest_factor_edge_cases(signal_factory):
    """Test edge cases."""
    # Zero signal
    signal, metadata = signal_factory(
        signal_type='dc',
        amplitude=0.0,
        duration=1.0
    )
    trace = tk.WaveformTrace(data=signal, metadata=metadata)
    cf = crest_factor(trace)
    assert cf == 0.0

    # Single sample
    trace = tk.WaveformTrace(
        data=np.array([1.0]),
        metadata=tk.TraceMetadata(sample_rate=1e6)
    )
    cf = crest_factor(trace)
    assert cf == 1.0

@pytest.mark.parametrize('amplitude', [0.5, 1.0, 2.0, 5.0])
def test_crest_factor_amplitude_invariant(signal_factory, amplitude):
    """Test CF is amplitude-invariant for sine waves."""
    signal, metadata = signal_factory(
        signal_type='sine',
        frequency=1000,
        amplitude=amplitude
    )

    trace = tk.WaveformTrace(data=signal, metadata=metadata)
    cf = crest_factor(trace)

    # CF should be independent of amplitude
    expected = np.sqrt(2)
    assert abs(cf - expected) < 0.01
```

#### Test Markers

Required markers for test organization:

```python
# Module-level markers
pytestmark = [
    pytest.mark.unit,        # Test type
    pytest.mark.analyzer,    # Module
]

# Test-specific markers
@pytest.mark.slow
def test_large_dataset():
    """Test with large dataset (>1 second)."""
    pass

@pytest.mark.requires_data
def test_real_capture():
    """Test requires test_data directory."""
    pass
```

### Documentation Standards

#### Docstring Format

Use Google-style docstrings:

```python
def custom_measurement(trace: WaveformTrace, threshold: float = 0.5) -> float:
    """Calculate custom measurement.

    Brief description of what the measurement computes.

    Args:
        trace: Input WaveformTrace to measure.
        threshold: Detection threshold (default: 0.5).

    Returns:
        Measured value in appropriate units.

    Raises:
        ValueError: If trace is empty.

    Example:
        >>> trace = tk.load('signal.wfm')
        >>> value = custom_measurement(trace, threshold=0.7)
        >>> print(f"Result: {value:.3f}")

    References:
        IEEE 181-2011: Pulse measurement standard
        https://example.com/measurement-theory
    """
    if len(trace.data) == 0:
        raise ValueError("Trace cannot be empty")

    # Implementation
    return computed_value
```

#### Type Hints

Use comprehensive type hints:

```python
from __future__ import annotations
from typing import TYPE_CHECKING
from numpy.typing import NDArray
import numpy as np

if TYPE_CHECKING:
    from tracekit.core.types import WaveformTrace

def process_trace(
    trace: WaveformTrace,
    *,
    window_size: int = 10,
    mode: str = 'constant',
) -> NDArray[np.float64]:
    """Process trace with typed parameters."""
    pass
```

### Pull Request Process

1. **Create Feature Branch**

   ```bash
   git checkout -b feature/my-amazing-feature
   ```

2. **Make Changes**
   - Implement feature with tests
   - Follow code style (Ruff formatting)
   - Add docstrings and type hints
   - Update documentation if needed

3. **Run Quality Checks**

   ```bash
   # Run tests
   uv run pytest tests/unit -v

   # Check formatting
   uv run ruff check src/ tests/
   uv run ruff format src/ tests/ --check

   # Type check
   uv run mypy src/
   ```

4. **Commit Changes**

   Use [Conventional Commits](https://www.conventionalcommits.org/):

   ```bash
   git commit -m "feat: add crest factor measurement

   - Implement crest_factor() function
   - Add comprehensive test suite
   - Update measurement registry
   - Add documentation examples

   Closes #123"
   ```

   **Commit types:**
   - `feat`: New feature
   - `fix`: Bug fix
   - `docs`: Documentation only
   - `style`: Code style (formatting, no logic change)
   - `refactor`: Code refactoring
   - `test`: Adding/updating tests
   - `perf`: Performance improvement
   - `chore`: Maintenance tasks

5. **Push and Create PR**

   ```bash
   git push origin feature/my-amazing-feature
   ```

   Open pull request on GitHub with:
   - Clear title and description
   - Reference to related issues
   - Screenshots/examples if applicable
   - Test results summary

6. **Code Review**
   - Address review feedback
   - Keep PR focused and atomic
   - Maintain clean commit history

### Code Style Guidelines

#### Formatting

- **Line length**: 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes for strings
- **Imports**: Organized (stdlib, third-party, local)

#### Naming Conventions

```python
# Functions and variables: snake_case
def calculate_rise_time(trace):
    sample_count = len(trace.data)

# Classes: PascalCase
class CustomTransformer:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_ITERATIONS = 100
DEFAULT_THRESHOLD = 0.5

# Private members: leading underscore
def _internal_helper():
    pass
```

#### Error Handling

```python
def robust_measurement(trace: WaveformTrace) -> float:
    """Measurement with proper error handling."""
    # Input validation
    if not isinstance(trace, WaveformTrace):
        raise TypeError(f"Expected WaveformTrace, got {type(trace)}")

    if len(trace.data) == 0:
        raise ValueError("Trace data cannot be empty")

    # Computation with safety checks
    try:
        result = compute_value(trace)
    except ZeroDivisionError:
        raise AnalysisError("Division by zero in measurement") from None

    # Output validation
    if not np.isfinite(result):
        raise AnalysisError(f"Measurement produced non-finite result: {result}")

    return result
```

### Continuous Integration

TraceKit uses GitHub Actions for CI:

- **Unit tests** on Python 3.12, 3.13
- **Code formatting** (Ruff)
- **Type checking** (mypy)
- **Security scanning** (Bandit)
- **Coverage reporting** (pytest-cov)

Your PR must pass all CI checks before merging.

---

## Additional Resources

### Documentation

- [API Reference](../api/index.md) - Complete API documentation
- [Loading Waveforms](loading-waveforms.md) - File format guide
- [GPU Acceleration](gpu-acceleration.md) - Performance optimization
- [Testing Guidelines](../testing/index.md) - Comprehensive test guide

### Examples

- [`examples/06_expert_api/`](../../examples/06_expert_api/) - Expert API examples
- [`examples/05_advanced/`](../../examples/05_advanced/) - Advanced techniques

### Community

- **GitHub**: [github.com/lair-click-bats/tracekit](https://github.com/lair-click-bats/tracekit)
- **Issues**: [Report bugs and request features](https://github.com/lair-click-bats/tracekit/issues)
- **Discussions**: [Ask questions and share ideas](https://github.com/lair-click-bats/tracekit/discussions)

### Standards References

- **IEEE 181-2011**: Pulse measurement standard
- **IEEE 1057-2017**: Digitizer characterization
- **IEEE 1241-2010**: ADC testing standard
- **IEEE 2414-2020**: Jitter measurements

---

## Summary

This guide covered:

1. ✅ **Custom Measurements** - Define, register, test, and integrate
2. ✅ **Analysis Pipelines** - Build reusable, composable workflows
3. ✅ **Plugin Development** - Create and publish TraceKit extensions
4. ✅ **Framework Extension** - Custom exporters, visualizations, algorithms
5. ✅ **Performance Optimization** - Profiling, memory, GPU, parallelization
6. ✅ **Contributing** - Development setup, testing, documentation, PRs

**Next Steps:**

- Explore [examples/06_expert_api/](../../examples/06_expert_api/) for working code
- Read [API Reference](../api/index.md) for detailed documentation
- Join the community on GitHub to share your extensions
- Contribute improvements and help make TraceKit better!

---

_For questions or feedback, please [open an issue](https://github.com/lair-click-bats/tracekit/issues) on GitHub._
