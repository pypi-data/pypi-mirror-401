# Examples

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

Code examples for common TraceKit use cases.

> **Note**: See the `examples/` directory in the repository for working code examples. Detailed example documentation pages are planned for a future release.

## Working Examples in Repository

The `examples/` directory contains fully functional demonstrations:

**Configuration Examples** (`examples/configs/`):

- `packet_format_example.yaml` - Packet structure definitions
- `device_mapping_example.yaml` - Device ID mappings
- `bus_config_example.yaml` - Bus protocol settings
- `protocol_definition_example.yaml` - Protocol DSL

**Code Examples** (`examples/`):

- Basic waveform loading and measurements
- Protocol decoding workflows
- Visualization and plotting
- Custom loader implementation

## Planned Example Documentation

### Basic Examples

- Loading and Plotting
- Rise/Fall Time Measurement
- FFT Analysis

### Protocol Decoding

- UART Decoding
- SPI Decoding
- I2C Decoding
- CAN Decoding

### Advanced Examples

- Jitter Analysis
- Eye Diagram Generation
- Batch Processing
- Custom Export Formats

## Quick Start Example

```python
import tracekit as tk

# Load waveform data
trace = tk.load("data.wfm")

# Perform measurements
rise = tk.rise_time(trace)
fall = tk.fall_time(trace)

# Visualize
tk.plot(trace)
```

## Related Documentation

- [LOADER_API.md](../api/loader.md) - Complete loading reference
- [ANALYSIS_API.md](../api/analysis.md) - All analysis functions
- [EXPORT_API.md](../api/export.md) - Export capabilities
- [visualization_api.md](../api/visualization.md) - Plotting reference
