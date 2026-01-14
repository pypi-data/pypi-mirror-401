# 06_expert_api - Expert Mode Features

> **Prerequisites**: All previous sections (01-05)
> **Time**: 60+ minutes

Power user features for advanced analysis, customization,
and protocol discovery.

## Learning Objectives

By completing these examples, you will learn how to:

1. **Use Expert API** - Access low-level analysis controls
2. **Advanced configuration** - Fine-tune analysis parameters
3. **Adaptive tuning** - Auto-optimize parameters
4. **Audit trails** - Track analysis history
5. **Discovery mode** - Explore unknown signals

## Examples in This Section

### 01_expert_basics.py

**What it does**: Introduction to Expert API

**Concepts covered**:

- Expert API entry points
- Configuration options
- Result inspection
- Debug output

**Run it**:

```bash
uv run python examples/06_expert_api/01_expert_basics.py
```

**Expected output**: Detailed analysis with expert controls

---

### 02_expert_advanced.py

**What it does**: Advanced Expert API usage

**Concepts covered**:

- Custom analysis pipelines
- Intermediate results
- Algorithm selection
- Performance tuning

**Run it**:

```bash
uv run python examples/06_expert_api/02_expert_advanced.py
```

**Expected output**: Advanced analysis with custom configuration

---

### 03_adaptive_tuning.py

**What it does**: Automatically optimize analysis parameters

**Concepts covered**:

- Parameter search
- Quality metrics
- Optimization strategies
- Convergence detection

**Run it**:

```bash
uv run python examples/06_expert_api/03_adaptive_tuning.py
```

**Expected output**: Optimized parameters and improvement metrics

---

### 04_audit_trail.py

**What it does**: Track and log analysis operations

**Concepts covered**:

- Operation logging
- Parameter recording
- Result versioning
- Reproducibility

**Run it**:

```bash
uv run python examples/06_expert_api/04_audit_trail.py
```

**Expected output**: Audit trail report

---

### 05_discovery.py

**What it does**: Explore unknown signals and protocols

**Concepts covered**:

- Signal characterization
- Pattern discovery
- Protocol inference
- Hypothesis generation

**Run it**:

```bash
uv run python examples/06_expert_api/05_discovery.py
```

**Expected output**: Discovery report with findings

---

## Quick Reference

### Expert API Basics

```python
from tracekit.api import ExpertAPI

# Create expert API instance
expert = ExpertAPI(trace)

# Configure analysis
expert.configure(
    threshold_method="adaptive",
    edge_filter="median",
    min_pulse_width=1e-9
)

# Run with full results
results = expert.analyze(return_intermediates=True)

# Access detailed results
print(f"Edges found: {results.edge_count}")
print(f"Threshold used: {results.computed_threshold}")
print(f"Confidence: {results.confidence}")
```

### Advanced Configuration

```python
from tracekit.api import AnalysisConfig

config = AnalysisConfig(
    # Threshold settings
    threshold_method="histogram",
    threshold_levels=2,

    # Edge detection
    edge_hysteresis=0.1,
    min_edge_separation=1e-9,

    # Filtering
    pre_filter="lowpass",
    filter_cutoff=100e6,

    # Performance
    use_gpu=True,
    chunk_size=1_000_000
)

results = expert.analyze(config=config)
```

### Adaptive Tuning

```python
from tracekit.api import AdaptiveTuner

tuner = AdaptiveTuner(trace)

# Define parameter ranges
tuner.set_range("threshold", 0.1, 0.9, steps=10)
tuner.set_range("filter_cutoff", 1e6, 100e6, log_scale=True)

# Define quality metric
def quality(results):
    return results.confidence * (1 - results.error_rate)

# Run optimization
best_params = tuner.optimize(quality, max_iterations=50)

print(f"Best parameters: {best_params}")
print(f"Quality score: {tuner.best_score:.3f}")
```

### Audit Trail

```python
from tracekit.api import AuditTrail

# Enable audit trail
audit = AuditTrail()
audit.start()

# Perform analysis (automatically logged)
trace = tk.load("capture.wfm")
freq = tk.measure_frequency(trace)
report = tk.generate_report(trace)

# Get audit log
audit.stop()

for entry in audit.entries:
    print(f"[{entry.timestamp}] {entry.operation}: {entry.parameters}")

# Save audit trail
audit.save("analysis_audit.json")
```

### Discovery Mode

```python
from tracekit.discovery import discover_signal

# Run discovery on unknown signal
findings = discover_signal(trace)

print("Signal Characteristics:")
print(f"  Type: {findings.signal_type}")
print(f"  Frequency: {findings.estimated_frequency}")
print(f"  Modulation: {findings.modulation_type}")

print("\nProtocol Candidates:")
for proto in findings.protocol_candidates:
    print(f"  {proto.name}: {proto.confidence:.1%}")

print("\nPattern Findings:")
for pattern in findings.patterns:
    print(f"  {pattern.description}")
```

## Common Issues

**Issue**: Expert API too complex

**Solution**: Start with defaults, then customize:

```python
# Start simple
results = expert.analyze()

# Then add customization
expert.configure(threshold_method="adaptive")
results = expert.analyze()
```

---

**Issue**: Adaptive tuning takes too long

**Solution**: Reduce search space or iterations:

```python
tuner.set_range("threshold", 0.4, 0.6, steps=5)  # Narrower range
best = tuner.optimize(quality, max_iterations=20)  # Fewer iterations
```

---

**Issue**: Discovery mode doesn't find protocol

**Solution**: Ensure sufficient data captured. Discovery needs representative samples.

---

## Estimated Time

- **Quick review**: 25 minutes
- **Hands-on practice**: 60+ minutes
- **Full exploration**: 2+ hours

## Further Learning

You've completed the structured learning path! Next steps:

- **Real projects**: Apply to your own waveform data
- **Custom plugins**: Extend TraceKit with your own analyzers
- **Contributing**: Share your improvements with the community

## See Also

- [API Reference: Expert API](../../docs/api/index.md)
- [User Guide](../../docs/user-guide.md)
- [Contributing Guide](../../CONTRIBUTING.md)
