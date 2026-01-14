# Parallel Pipeline Examples

This directory contains examples demonstrating the use of `ParallelPipeline` for accelerated trace processing.

## Overview

`ParallelPipeline` extends the standard `Pipeline` with parallel execution capabilities. It automatically analyzes dependencies between stages and executes independent stages concurrently using thread or process pools.

## Files

- `basic_parallel_usage.py` - Comprehensive examples showing all ParallelPipeline features

## Running the Examples

```bash
# Run all examples
python examples/05_parallel_pipeline/basic_parallel_usage.py

# Or using uv
uv run python examples/05_parallel_pipeline/basic_parallel_usage.py
```

## Key Features Demonstrated

### 1. Executor Types

- **Thread Pool**: Best for I/O-bound tasks with low overhead
- **Process Pool**: Best for CPU-bound tasks with true parallelism

### 2. Worker Count Selection

- **Automatic**: `max_workers=None` selects optimal worker count
  - Thread pool: `min(32, cpu_count + 4)`
  - Process pool: `cpu_count`
- **Manual**: Specify exact worker count

### 3. API Compatibility

`ParallelPipeline` is fully API-compatible with `Pipeline`:

```python
from tracekit.pipeline import Pipeline, ParallelPipeline

# Drop-in replacement
sequential = Pipeline(steps)
parallel = ParallelPipeline(steps)  # Same interface, parallel execution
```

### 4. Dynamic Configuration

Change executor configuration at runtime:

```python
pipeline.set_parallel_config(executor_type='process', max_workers=4)
```

### 5. Intermediate Results

Access outputs from individual pipeline stages:

```python
result = pipeline.transform(trace)
intermediate = pipeline.get_intermediate('filter')
```

## Performance Characteristics

### Thread Pool (executor_type='thread')

**Use for**: I/O-bound tasks (file loading, network requests)

**Characteristics**:

- Low overhead (~10ms startup)
- Shared memory (no serialization)
- Limited by GIL for CPU-bound tasks

**Example**:

```python
pipeline = ParallelPipeline(
    steps,
    executor_type='thread',
    max_workers=4
)
```

### Process Pool (executor_type='process')

**Use for**: CPU-bound tasks (FFT, filtering, complex analysis)

**Characteristics**:

- Higher overhead (~50ms startup)
- True parallelism (bypasses GIL)
- Requires picklable transformers

**Example**:

```python
pipeline = ParallelPipeline(
    steps,
    executor_type='process',
    max_workers=None  # Auto: cpu_count
)
```

## Dependency Analysis

Current implementation uses conservative dependency analysis where each stage depends on the previous stage (sequential execution). This ensures correctness while providing the parallel execution infrastructure.

**Execution Order Example**:

```python
pipeline = ParallelPipeline([
    ('filter1', LowPassFilter()),
    ('filter2', HighPassFilter()),
    ('merge', MergeTransformer())
])

# Current: Sequential execution
# Generation 0: ['filter1']
# Generation 1: ['filter2']
# Generation 2: ['merge']
```

Future enhancement (FUTURE-002) will support advanced dependency analysis to automatically detect truly independent stages for parallel execution.

## Common Patterns

### Pattern 1: Simple Sequential Enhancement

```python
# Just change Pipeline to ParallelPipeline
pipeline = ParallelPipeline([
    ('preprocess', Normalize()),
    ('filter', LowPassFilter()),
    ('analyze', FFT())
])
```

### Pattern 2: CPU-Intensive Processing

```python
# Use process pool for heavy computation
pipeline = ParallelPipeline([
    ('fft', FFT(nfft=65536)),
    ('wavelet', WaveletTransform()),
    ('analyze', SpectralAnalysis())
], executor_type='process')
```

### Pattern 3: Switching Executors

```python
# Start with thread pool for development
pipeline = ParallelPipeline(steps, executor_type='thread')

# Switch to process pool for production
pipeline.set_parallel_config(executor_type='process')
```

## See Also

- `examples/01_basics/` - Basic Pipeline usage
- `src/tracekit/pipeline/pipeline.py` - Standard Pipeline implementation
- `src/tracekit/pipeline/parallel.py` - ParallelPipeline implementation
- `tests/unit/pipeline/test_parallel_pipeline.py` - Comprehensive tests
