# TraceKit Import Path Guidelines

This document clarifies the canonical import paths for TraceKit modules.

## Protocol Decoders

**Both singular and plural forms are supported and equivalent:**

```python
# Both of these are equivalent - use either
from tracekit.analyzers.protocol import UARTDecoder
from tracekit.analyzers.protocols import UARTDecoder
```

**Recommendation:** Use the plural form `protocols` as it's more explicit:

```python
from tracekit.analyzers.protocols import UARTDecoder, SPIDecoder, I2CDecoder
```

**Note:** As of v0.1.0, both modules export all 16+ protocol decoders. The singular `protocol` module is a convenience re-export of `protocols`.

## Statistical Analysis

**These modules serve different purposes:**

### `statistics` - General Signal Statistics

Use for standard statistical analysis of signal data:

```python
from tracekit.analyzers.statistics import (
    basic_stats,
    percentiles,
    detect_outliers,
    correlation_coefficient,
)
```

Provides:

- Basic statistics (mean, std, quartiles, percentiles)
- Outlier detection (z-score, IQR, isolation forest, LOF)
- Correlation analysis (autocorrelation, cross-correlation)
- Trend detection (change points, drift, seasonal decomposition)
- Distribution analysis

### `statistical` - Statistical + Binary Analysis

Use for reverse engineering and binary data analysis:

```python
from tracekit.analyzers.statistical import (
    shannon_entropy,
    byte_frequency_distribution,
    detect_checksum_fields,
    classify_data_type,
)
```

Provides:

- Everything from `statistics` (re-exported)
- **Plus** entropy analysis (Shannon entropy, bit entropy, sliding entropy)
- **Plus** checksum detection (CRC, XOR, sum checksums)
- **Plus** data classification (text, compressed, encrypted, padding)
- **Plus** n-gram analysis

**Recommendation:**

- For signal analysis → use `statistics`
- For binary/protocol reverse engineering → use `statistical`

## Top-Level API

Most commonly-used functions are exported at the top level:

```python
import tracekit as tk

# Waveform measurements
freq = tk.frequency(trace)
rise = tk.rise_time(trace)

# Protocol decoding (use full path for decoders)
from tracekit.protocols import UARTDecoder
decoder = UARTDecoder(baud_rate=115200)

# Statistics (use full path for advanced features)
from tracekit.analyzers.statistics import detect_outliers
outliers = detect_outliers(data)
```

See [API Reference](../api/index.md) for the complete list of top-level exports.

## Summary

| Module            | Use Case            | Canonical Path                                    |
| ----------------- | ------------------- | ------------------------------------------------- |
| Protocol decoders | All cases           | `tracekit.analyzers.protocols` (plural preferred) |
| Signal statistics | Signal analysis     | `tracekit.analyzers.statistics`                   |
| Binary analysis   | Reverse engineering | `tracekit.analyzers.statistical`                  |
| Common functions  | Quick access        | `import tracekit as tk`                           |
