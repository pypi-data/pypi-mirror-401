# Guides

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

Task-focused guides for common TraceKit operations.

## Available Guides

### Data Loading

- **[Loading Waveforms](loading-waveforms.md)** - Loading data from various file formats
- **[Synthetic Test Data](synthetic-test-data.md)** - Generating test signals
- **[Public Test Data Sources](public-test-data-sources.md)** - Finding sample data

### Analysis & Troubleshooting

- **[Power Analysis](power-analysis-guide.md)** - Comprehensive power analysis guide (DC, AC, switching, battery, motor)
- **[Component Analysis](component-analysis-guide.md)** - TDR and component characterization
- **[EMC Compliance Testing](emc-compliance-guide.md)** - EMC/EMI testing workflows and regulatory compliance
- **[NaN Handling](nan-handling.md)** - Understanding and handling NaN results
- **[Signal Intelligence](signal-intelligence.md)** - Automatic signal classification
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions

### Performance

- **[GPU Acceleration](gpu-acceleration.md)** - Using CUDA for faster analysis
- **[Best Practices](best-practices.md)** - Tips for optimal usage

### Advanced Topics

- **[Expert Guide](expert-guide.md)** - Advanced features for power users (custom measurements, pipelines, plugins, performance)

### Customization

- **[Report Customization](report-customization.md)** - Customizing report output

### Migration & Deployment

- **[Test Data Migration](test-data-migration.md)** - Migrating test data
- **[Deployment](deployment.md)** - Deployment guidelines

### Repository Maintenance

- **[GitHub Repository Setup](github-repository-setup.md)** - Configuring GitHub repository settings

## Guide by Task

### "I want to test..."

| Test Type                 | Guide                                             |
| ------------------------- | ------------------------------------------------- |
| EMC/EMI compliance        | [EMC Compliance Testing](emc-compliance-guide.md) |
| FCC Part 15               | [EMC Compliance Testing](emc-compliance-guide.md) |
| CISPR 22/32               | [EMC Compliance Testing](emc-compliance-guide.md) |
| Automotive EMC (CISPR 25) | [EMC Compliance Testing](emc-compliance-guide.md) |
| Radiated emissions        | [EMC Compliance Testing](emc-compliance-guide.md) |
| Conducted emissions       | [EMC Compliance Testing](emc-compliance-guide.md) |
| ESD immunity              | [EMC Compliance Testing](emc-compliance-guide.md) |

### "I want to measure..."

| Component/Property    | Guide                                             |
| --------------------- | ------------------------------------------------- |
| Power consumption     | [Power Analysis](power-analysis-guide.md)         |
| Efficiency            | [Power Analysis](power-analysis-guide.md)         |
| Power factor          | [Power Analysis](power-analysis-guide.md)         |
| Battery discharge     | [Power Analysis](power-analysis-guide.md)         |
| Switching regulator   | [Power Analysis](power-analysis-guide.md)         |
| Motor power           | [Power Analysis](power-analysis-guide.md)         |
| PCB trace impedance   | [Component Analysis](component-analysis-guide.md) |
| Capacitor ESR         | [Component Analysis](component-analysis-guide.md) |
| Inductor parameters   | [Component Analysis](component-analysis-guide.md) |
| Cable characteristics | [Component Analysis](component-analysis-guide.md) |
| Connector quality     | [Component Analysis](component-analysis-guide.md) |
| Parasitic extraction  | [Component Analysis](component-analysis-guide.md) |

### "I want to load data from..."

| Source                 | Guide                                         |
| ---------------------- | --------------------------------------------- |
| Tektronix oscilloscope | [Loading Waveforms](loading-waveforms.md)     |
| Rigol oscilloscope     | [Loading Waveforms](loading-waveforms.md)     |
| Sigrok capture         | [Loading Waveforms](loading-waveforms.md)     |
| CSV file               | [Loading Waveforms](loading-waveforms.md)     |
| HDF5 file              | [Loading Waveforms](loading-waveforms.md)     |
| Generate test signal   | [Synthetic Test Data](synthetic-test-data.md) |

### "I'm getting an error..."

| Error Type              | Guide                                 |
| ----------------------- | ------------------------------------- |
| Measurement returns NaN | [NaN Handling](nan-handling.md)       |
| File won't load         | [Troubleshooting](troubleshooting.md) |
| Protocol decode fails   | [Troubleshooting](troubleshooting.md) |
| Out of memory           | [Troubleshooting](troubleshooting.md) |

### "I want to improve performance..."

| Goal               | Guide                                   |
| ------------------ | --------------------------------------- |
| Speed up FFT       | [GPU Acceleration](gpu-acceleration.md) |
| Handle large files | [Best Practices](best-practices.md)     |
| Optimize memory    | [Best Practices](best-practices.md)     |

### "I want to customize..."

| Customization            | Guide                                           |
| ------------------------ | ----------------------------------------------- |
| Report appearance        | [Report Customization](report-customization.md) |
| Analysis parameters      | [Best Practices](best-practices.md)             |
| Custom measurements      | [Expert Guide](expert-guide.md)                 |
| Build analysis pipelines | [Expert Guide](expert-guide.md)                 |
| Create plugins           | [Expert Guide](expert-guide.md)                 |
| Extend framework         | [Expert Guide](expert-guide.md)                 |

## Quick Tips

### Loading Large Files

```python
# Use lazy loading
trace = tk.load("huge_file.wfm", lazy=True)

# Process in chunks
for chunk in tk.iter_chunks(trace, chunk_size=100000):
    process(chunk)
```

### Handling NaN

```python
import math

freq = tk.measure_frequency(trace)
if math.isnan(freq):
    # Signal may not be periodic
    edges = tk.find_edges(trace)
    if edges:
        period = edges[1][0] - edges[0][0]
        freq = 1.0 / period
```

### GPU Acceleration

```python
# Check availability
if tk.gpu_available():
    spectrum = compute_fft(trace, use_gpu=True)
else:
    spectrum = compute_fft(trace)
```

## See Also

- [Getting Started](../getting-started.md) - Introduction to TraceKit
- [User Guide](../user-guide.md) - Comprehensive usage guide
- [API Reference](../api/index.md) - Complete API documentation
- [Examples](../examples-reference.md) - Working code examples
