# API Reference

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

Complete API documentation for TraceKit.

## Quick Links

| Category            | Documentation                                        |
| ------------------- | ---------------------------------------------------- |
| Loading Data        | [loader.md](loader.md)                               |
| Analysis            | [analysis.md](analysis.md)                           |
| Pipelines           | [pipelines.md](pipelines.md)                         |
| Component Analysis  | [component-analysis.md](component-analysis.md)       |
| Comparison & Limits | [comparison-and-limits.md](comparison-and-limits.md) |
| EMC Compliance      | [emc-compliance.md](emc-compliance.md)               |
| Session Management  | [session-management.md](session-management.md)       |
| Export              | [export.md](export.md)                               |
| Reporting           | [reporting.md](reporting.md)                         |
| Visualization       | [visualization.md](visualization.md)                 |
| **Expert API**      | **[expert-api.md](expert-api.md)**                   |

## API Overview

### Loading Data

```python
import tracekit as tk

# Load waveform (auto-detect format)
trace = tk.load("capture.wfm")

# Load with options
trace = tk.load("capture.wfm", lazy=True)

# Load all channels
channels = tk.load_all_channels("multi_channel.wfm")

# Check supported formats
formats = tk.get_supported_formats()
```

**Full documentation**: [loader.md](loader.md)

### Measurements

```python
import tracekit as tk

# Time-domain
freq = tk.frequency(trace)
period = tk.period(trace)
rise_time = tk.rise_time(trace)
fall_time = tk.fall_time(trace)
duty_cycle = tk.duty_cycle(trace)

# Amplitude
amplitude = tk.amplitude(trace)
peak_to_peak = tk.peak_to_peak(trace)
rms = tk.rms(trace)

# Edges
edges = tk.find_edges(trace, threshold=0.5)
```

**Full documentation**: [analysis.md](analysis.md)

### Protocol Decoding

```python
import tracekit as tk
from tracekit.analyzers.protocols import (
    UARTDecoder,
    SPIDecoder,
    I2CDecoder,
    CANDecoder,
)

# UART (using convenience function)
messages = tk.decode_uart(trace, baud_rate=115200)

# Or use decoder class directly
decoder = UARTDecoder(baud_rate=115200)
messages = decoder.decode(trace)

# SPI (multi-channel)
decoder = SPIDecoder(clock=ch_clk, mosi=ch_mosi, miso=ch_miso, cs=ch_cs)
transactions = decoder.decode()

# I2C
decoder = I2CDecoder(sda=ch_sda, scl=ch_scl)
transactions = decoder.decode()
```

**Full documentation**: [analysis.md](analysis.md#protocol-decoding)

### Spectral Analysis

```python
import tracekit as tk

# FFT and PSD
spectrum = tk.fft(trace, window="hanning")
psd = tk.psd(trace, window="hanning")

# Quality metrics
thd = tk.thd(trace, fundamental_freq=1e6)
snr = tk.snr(trace, signal_freq=1e6)
sinad = tk.sinad(trace, signal_freq=1e6)
sfdr = tk.sfdr(trace)
enob = tk.enob(trace, signal_freq=1e6)
```

**Full documentation**: [analysis.md](analysis.md#spectral-analysis)

### Pipelines & Composition

```python
import tracekit as tk
from functools import partial

# Create analysis pipeline
pipeline = tk.Pipeline([
    ('filter', tk.LowPassFilter(cutoff=1e6)),
    ('normalize', tk.Normalize(method='peak')),
    ('fft', tk.FFT(nfft=8192))
])

# Transform trace
result = pipeline.transform(trace)

# Access intermediate results
filtered = pipeline.get_intermediate('filter')
spectrum = pipeline.get_intermediate('fft', 'spectrum')

# Functional composition
result = tk.pipe(
    trace,
    partial(tk.low_pass, cutoff=1e6),
    partial(tk.normalize, method='peak'),
    partial(tk.fft, nfft=8192)
)

# Custom transformers
class CustomTransformer(tk.TraceTransformer):
    def transform(self, trace):
        # Custom processing
        return trace
```

**Full documentation**: [pipelines.md](pipelines.md)

### Component Analysis

```python
import tracekit as tk

# TDR impedance profiling
z0, profile = tk.extract_impedance(tdr_trace, z0_source=50.0)
discontinuities = tk.discontinuity_analysis(tdr_trace)

# Capacitance and inductance
C = tk.measure_capacitance(voltage, current, method="charge")
L = tk.measure_inductance(voltage, current, method="slope")

# Parasitic extraction
params = tk.extract_parasitics(voltage, current, model="series_RLC")

# Transmission line parameters
z0 = tk.characteristic_impedance(tdr_trace)
delay = tk.propagation_delay(tdr_trace)
vf = tk.velocity_factor(tdr_trace, line_length=0.1)
```

**Full documentation**: [component-analysis.md](component-analysis.md)

### Comparison & Limit Testing

```python
import tracekit as tk
from tracekit.comparison import (
    compare_traces,
    create_golden,
    compare_to_golden,
    create_limit_spec,
    check_limits,
    eye_mask,
    mask_test,
)

# Compare waveforms
result = compare_traces(measured, reference, tolerance=0.01)

# Golden reference testing
golden = create_golden(reference, tolerance_pct=5)
test_result = compare_to_golden(measured, golden)

# Limit testing
spec = create_limit_spec(upper=3.3, lower=2.7)
limit_result = check_limits(trace, spec)

# Eye diagram mask testing
mask = eye_mask(eye_width=0.5, eye_height=0.4)
mask_result = mask_test(eye_trace, mask)
```

**Full documentation**: [comparison-and-limits.md](comparison-and-limits.md)

### EMC Compliance Testing

```python
import tracekit as tk
from tracekit.compliance import (
    load_limit_mask,
    check_compliance,
    create_custom_mask,
    generate_compliance_report,
)

# Test against FCC/CE/MIL standards
mask = load_limit_mask("FCC_Part15_ClassB")
result = check_compliance(trace, mask, detector="quasi-peak")

# Create custom automotive EMC mask (CISPR 25)
cispr25 = create_custom_mask(
    name="CISPR_25_ClassB",
    frequencies=[150e3, 30e6, 108e6, 1000e6],
    limits=[74, 54, 44, 44],
    unit="dBuV",
    description="CISPR 25 Class B radiated emissions"
)

# Generate compliance report
generate_compliance_report(
    result,
    "emc_report.html",
    title="EMC Compliance Test",
    dut_info={"Model": "XYZ-100", "Serial": "12345"}
)
```

**Full documentation**: [emc-compliance.md](emc-compliance.md)

### Session Management & Audit Trail

```python
import tracekit as tk

# Create and manage analysis sessions
session = tk.Session(name="Power Supply Analysis")
trace = session.load_trace("capture.wfm")
session.annotate("Voltage spike", time=1.5e-6)
session.record_measurement("rise_time", 2.3e-9, unit="s")
session.save("analysis.tks")

# Resume saved session
session = tk.load_session("analysis.tks")
print(session.summary())

# Audit trail for compliance
audit = tk.AuditTrail(secret_key=b"your-secret-key")
audit.record_action("load_trace", {"file": "data.wfm"})
assert audit.verify_integrity()
audit.export_audit_log("audit.json", format="json")
```

**Full documentation**: [session-management.md](session-management.md)

### Report Generation

```python
from tracekit.reporting import (
    generate_report,
    save_pdf_report,
    save_html_report,
    ReportConfig,
)

# Generate and save
report = generate_report(trace, title="Analysis Report")
save_pdf_report(report, "report.pdf")
save_html_report(report, "report.html")
```

**Full documentation**: [reporting.md](reporting.md)

### Data Export

```python
import tracekit as tk

# Export to various formats
tk.export_csv(trace, "data.csv")
tk.export_hdf5(trace, "data.h5", compression="gzip")
tk.export_npz(trace, "data.npz")
tk.export_json(trace, "data.json")
tk.export_mat(trace, "data.mat")
tk.export_pwl(trace, "data.pwl")  # For SPICE
```

**Full documentation**: [export.md](export.md)

## Module Reference

### Core Modules

| Module                     | Description                                                  |
| -------------------------- | ------------------------------------------------------------ |
| `tracekit`                 | Main package with convenience functions                      |
| `tracekit.core`            | Core data types (WaveformTrace, DigitalTrace, TraceMetadata) |
| `tracekit.core.exceptions` | Exception hierarchy                                          |
| `tracekit.core.config`     | Configuration management                                     |

### Loaders

| Module                          | Description                 |
| ------------------------------- | --------------------------- |
| `tracekit.loaders`              | File format loaders         |
| `tracekit.loaders.tektronix`    | Tektronix WFM loader        |
| `tracekit.loaders.rigol`        | Rigol WFM loader            |
| `tracekit.loaders.sigrok`       | Sigrok SR loader            |
| `tracekit.loaders.csv`          | CSV loader                  |
| `tracekit.loaders.hdf5`         | HDF5 loader                 |
| `tracekit.loaders.configurable` | Schema-driven packet loader |

### Analyzers

| Module                           | Description                |
| -------------------------------- | -------------------------- |
| `tracekit.analyzers.waveform`    | Waveform measurements      |
| `tracekit.analyzers.digital`     | Digital signal analysis    |
| `tracekit.analyzers.spectral`    | FFT, PSD, spectral metrics |
| `tracekit.analyzers.jitter`      | Jitter measurements        |
| `tracekit.analyzers.eye`         | Eye diagram analysis       |
| `tracekit.analyzers.statistical` | Statistical analysis       |
| `tracekit.analyzers.patterns`    | Pattern detection          |

### Protocol Decoders

| Module                                    | Protocol            |
| ----------------------------------------- | ------------------- |
| `tracekit.analyzers.protocols.uart`       | UART/RS-232         |
| `tracekit.analyzers.protocols.spi`        | SPI                 |
| `tracekit.analyzers.protocols.i2c`        | I2C                 |
| `tracekit.analyzers.protocols.can`        | CAN/CAN-FD          |
| `tracekit.analyzers.protocols.lin`        | LIN                 |
| `tracekit.analyzers.protocols.flexray`    | FlexRay             |
| `tracekit.analyzers.protocols.onewire`    | 1-Wire              |
| `tracekit.analyzers.protocols.jtag`       | JTAG                |
| `tracekit.analyzers.protocols.swd`        | SWD                 |
| `tracekit.analyzers.protocols.i2s`        | I2S                 |
| `tracekit.analyzers.protocols.usb`        | USB                 |
| `tracekit.analyzers.protocols.hdlc`       | HDLC                |
| `tracekit.analyzers.protocols.manchester` | Manchester encoding |

### Inference

| Module                              | Description                 |
| ----------------------------------- | --------------------------- |
| `tracekit.inference`                | Protocol inference          |
| `tracekit.inference.message_format` | Message structure detection |
| `tracekit.inference.state_machine`  | State machine inference     |
| `tracekit.inference.alignment`      | Sequence alignment          |

### Comparison & Testing

| Module                        | Description                  |
| ----------------------------- | ---------------------------- |
| `tracekit.comparison`         | Waveform comparison          |
| `tracekit.comparison.compare` | Trace comparison functions   |
| `tracekit.comparison.golden`  | Golden reference testing     |
| `tracekit.comparison.limits`  | Specification limit testing  |
| `tracekit.comparison.mask`    | Mask-based pass/fail testing |

### EMC Compliance

| Module                          | Description                                    |
| ------------------------------- | ---------------------------------------------- |
| `tracekit.compliance`           | EMC/EMI compliance testing                     |
| `tracekit.compliance.masks`     | Regulatory limit masks (FCC, CISPR, MIL-STD)   |
| `tracekit.compliance.testing`   | Compliance test execution and result analysis  |
| `tracekit.compliance.reporting` | Compliance report generation (HTML, PDF, JSON) |
| `tracekit.compliance.advanced`  | Advanced detectors and interpolation methods   |

### Session Management & Audit

| Module                | Description                        |
| --------------------- | ---------------------------------- |
| `tracekit.session`    | Session management and annotations |
| `tracekit.core.audit` | Audit trail with HMAC verification |

### Export & Reporting

| Module                   | Description        |
| ------------------------ | ------------------ |
| `tracekit.exporters`     | Data exporters     |
| `tracekit.reporting`     | Report generation  |
| `tracekit.visualization` | Plotting utilities |

## Accessing Documentation

### Python Help

```python
import tracekit as tk

# Get help on any function
help(tk.load)
help(tk.frequency)

# Module documentation
help(tk.analyzers.spectral)
```

### Docstrings

All public functions include comprehensive docstrings with:

- Parameter descriptions
- Return value documentation
- Usage examples
- IEEE standard references (where applicable)

Example:

```python
def measure_rise_time(
    trace: WaveformTrace,
    low: float = 0.1,
    high: float = 0.9,
) -> float:
    """Calculate rise time per IEEE 181-2011 Section 5.2.

    Parameters
    ----------
    trace : WaveformTrace
        Input waveform trace.
    low : float, optional
        Low reference level (0-1). Default 10%.
    high : float, optional
        High reference level (0-1). Default 90%.

    Returns
    -------
    float
        Rise time in seconds. NaN if measurement not applicable.

    Examples
    --------
    >>> trace = tk.load("capture.wfm")
    >>> rise = tk.measure_rise_time(trace)
    >>> print(f"Rise time: {rise*1e9:.2f} ns")

    References
    ----------
    IEEE 181-2011 Section 5.2 "Rise Time and Fall Time"
    """
```

## Exception Handling

```python
from tracekit import LoaderError, DecodeError, MeasurementError

try:
    trace = tk.load("file.wfm")
except LoaderError as e:
    print(f"Load failed: {e}")
    print(f"Fix hint: {e.fix_hint}")

try:
    freq = tk.frequency(trace)
except MeasurementError as e:
    print(f"Measurement failed: {e}")
```

See [Error Codes](../error-codes.md) for complete error reference.

## Type Hints

TraceKit is fully type-annotated for IDE support:

```python
from tracekit import WaveformTrace, DigitalTrace, TraceMetadata
from tracekit.analyzers.spectral import Spectrum, PowerSpectralDensity

def analyze_signal(trace: WaveformTrace) -> dict[str, float]:
    ...
```

## See Also

- [Getting Started](../getting-started.md) - Quick introduction
- [User Guide](../user-guide.md) - Comprehensive usage guide
- [Examples](../examples-reference.md) - Working code examples
- [CLI Reference](../cli.md) - Command-line interface
