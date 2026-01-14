# Tutorial 6: Report Generation

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08 | **Time**: 20 minutes

Learn to generate professional analysis reports in multiple formats.

## Prerequisites

- Completed previous tutorials
- Understanding of TraceKit measurements and analysis

## Learning Objectives

By the end of this tutorial, you will be able to:

- Generate analysis reports
- Customize report content and appearance
- Export to PDF, HTML, and JSON formats
- Create automated report workflows

## Quick Start

Generate a basic report in three lines:

```python
import tracekit as tk
from tracekit.reporting import generate_report, save_pdf_report

trace = tk.load("capture.wfm")
report = generate_report(trace, title="Signal Analysis")
save_pdf_report(report, "analysis_report.pdf")
```

## Report Components

A TraceKit report includes:

| Section      | Contents                              |
| ------------ | ------------------------------------- |
| Header       | Title, date, version                  |
| Summary      | Key findings, pass/fail status        |
| Measurements | Time/frequency/amplitude measurements |
| Spectral     | FFT, harmonics, SNR                   |
| Protocol     | Decoded messages (if applicable)      |
| Plots        | Waveform, spectrum, histogram         |
| Raw Data     | Optional data tables                  |

## Basic Report Generation

### From a Single Trace

```python
import tracekit as tk
from tracekit.reporting import generate_report

# Load data
trace = tk.load("capture.wfm")

# Generate report with default settings
report = generate_report(trace)

# Report object contains all analysis results
print(f"Report title: {report.title}")
print(f"Measurements: {len(report.measurements)}")
print(f"Plots: {len(report.plots)}")
```

### From Multiple Traces

```python
from tracekit.reporting import generate_comparative_report

# Load multiple captures
traces = {
    "Before": tk.load("before.wfm"),
    "After": tk.load("after.wfm"),
}

# Generate comparative report
report = generate_comparative_report(
    traces,
    title="Before/After Comparison"
)
```

## Customizing Report Content

### Using ReportConfig

```python
from tracekit.reporting import generate_report, ReportConfig

config = ReportConfig(
    # Content settings
    include_summary=True,
    include_measurements=True,
    include_spectral=True,
    include_protocol=False,  # Skip protocol section
    include_raw_data=False,  # Skip raw data tables

    # Plot settings
    include_plots=True,
    plot_dpi=150,
    plot_style="publication",  # or "presentation", "default"

    # Measurement selection
    measurements=[
        "frequency",
        "amplitude",
        "rise_time",
        "snr",
    ],
)

report = generate_report(trace, config=config)
```

### Selective Measurements

```python
# Only include specific measurements
config = ReportConfig(
    measurements=[
        "frequency",
        "period",
        "duty_cycle",
    ]
)

# Or exclude specific measurements
config = ReportConfig(
    exclude_measurements=[
        "thd",
        "sinad",
    ]
)
```

### Custom Title and Metadata

```python
report = generate_report(
    trace,
    title="Oscillator Characterization",
    author="Engineering Team",
    project="PROJ-001",
    device_under_test="Crystal Oscillator XO-100",
    test_conditions="25C, 3.3V supply",
)
```

## Export Formats

### PDF Export

```python
from tracekit.reporting import save_pdf_report

# Basic PDF
save_pdf_report(report, "report.pdf")

# With options
save_pdf_report(
    report,
    "report.pdf",
    paper_size="letter",  # or "a4"
    orientation="portrait",  # or "landscape"
    margins={"top": 1, "bottom": 1, "left": 1, "right": 1},
)
```

### HTML Export

```python
from tracekit.reporting import save_html_report

# Basic HTML
save_html_report(report, "report.html")

# Self-contained (images embedded)
save_html_report(
    report,
    "report.html",
    embed_images=True,
    include_css=True,
)

# With interactive plots
save_html_report(
    report,
    "report.html",
    interactive_plots=True,  # Uses Plotly
)
```

### JSON Export

For programmatic processing:

```python
from tracekit.reporting import save_json_report

save_json_report(report, "report.json")

# Load and process
import json
with open("report.json") as f:
    data = json.load(f)

print(f"Frequency: {data['measurements']['frequency']}")
```

### Markdown Export

For documentation systems:

```python
from tracekit.reporting import save_markdown_report

save_markdown_report(report, "report.md")
```

## Adding Custom Sections

### Custom Text Sections

```python
from tracekit.reporting import generate_report, TextSection

report = generate_report(trace)

# Add custom section
report.add_section(TextSection(
    title="Test Procedure",
    content="""
    1. Connect DUT to oscilloscope CH1
    2. Apply 3.3V power supply
    3. Capture 10ms of signal
    4. Verify frequency within spec
    """
))
```

### Custom Tables

```python
from tracekit.reporting import TableSection

# Add custom data table
report.add_section(TableSection(
    title="Specification Compliance",
    headers=["Parameter", "Spec", "Measured", "Status"],
    rows=[
        ["Frequency", "1 MHz +/- 100 ppm", "1.000005 MHz", "PASS"],
        ["Rise time", "< 10 ns", "8.5 ns", "PASS"],
        ["Jitter", "< 1 ns RMS", "0.8 ns", "PASS"],
    ]
))
```

### Custom Plots

```python
import matplotlib.pyplot as plt
from tracekit.reporting import PlotSection

# Create custom plot
fig, ax = plt.subplots()
ax.plot(trace.time_axis * 1e6, trace.data)
ax.set_xlabel("Time (us)")
ax.set_ylabel("Voltage (V)")
ax.set_title("Captured Waveform")

# Add to report
report.add_section(PlotSection(
    title="Custom Waveform View",
    figure=fig
))
```

## Pass/Fail Testing

### Define Specifications

```python
from tracekit.reporting import generate_report, Specification

specs = [
    Specification("frequency", min=999e3, max=1001e3, units="Hz"),
    Specification("amplitude", min=1.9, max=2.1, units="V"),
    Specification("rise_time", max=10e-9, units="s"),
    Specification("snr", min=40, units="dB"),
]

report = generate_report(trace, specifications=specs)

# Report includes pass/fail for each spec
for result in report.spec_results:
    status = "PASS" if result.passed else "FAIL"
    print(f"{result.name}: {result.measured} [{status}]")
```

### Overall Status

```python
if report.all_passed:
    print("All specifications PASSED")
else:
    print("Some specifications FAILED")
    for result in report.failed_specs:
        print(f"  FAIL: {result.name}")
```

## Batch Report Generation

### Multiple Files

```python
from pathlib import Path
from tracekit.reporting import generate_report, save_pdf_report

capture_dir = Path("captures/")
output_dir = Path("reports/")
output_dir.mkdir(exist_ok=True)

for wfm_file in capture_dir.glob("*.wfm"):
    trace = tk.load(wfm_file)
    report = generate_report(trace, title=wfm_file.stem)
    save_pdf_report(report, output_dir / f"{wfm_file.stem}_report.pdf")
    print(f"Generated report for {wfm_file.name}")
```

### Summary Report

```python
from tracekit.reporting import generate_summary_report

# Generate individual reports
reports = []
for wfm_file in capture_dir.glob("*.wfm"):
    trace = tk.load(wfm_file)
    reports.append(generate_report(trace, title=wfm_file.stem))

# Generate summary of all reports
summary = generate_summary_report(
    reports,
    title="Test Campaign Summary"
)

save_pdf_report(summary, "campaign_summary.pdf")
```

## Report Templates

### Using Templates

```python
from tracekit.reporting import load_template, generate_report

# Load custom template
template = load_template("templates/company_template.yaml")

report = generate_report(
    trace,
    template=template,
    title="Analysis Report"
)
```

### Template Configuration (YAML)

```yaml
# templates/company_template.yaml
header:
  logo: 'assets/logo.png'
  company: 'Acme Electronics'

sections:
  - summary
  - measurements
  - plots:
      - waveform
      - spectrum

style:
  font_family: 'Helvetica'
  primary_color: '#003366'

footer:
  text: 'Confidential - Internal Use Only'
```

## Complete Example

```python
import tracekit as tk
from tracekit.reporting import (
    generate_report,
    save_pdf_report,
    save_html_report,
    ReportConfig,
    Specification,
)

# Load and analyze
trace = tk.load("oscillator_capture.wfm")

# Define specifications
specs = [
    Specification("frequency", min=9.99e6, max=10.01e6, units="Hz"),
    Specification("amplitude", min=2.7, max=3.3, units="V"),
    Specification("thd", max=0.01, units="%"),
]

# Configure report
config = ReportConfig(
    include_summary=True,
    include_measurements=True,
    include_spectral=True,
    include_plots=True,
    plot_dpi=200,
    measurements=["frequency", "amplitude", "thd", "snr", "rise_time"],
)

# Generate report
report = generate_report(
    trace,
    config=config,
    specifications=specs,
    title="10 MHz Oscillator Characterization",
    author="Test Engineering",
    project="OSC-QUAL-001",
)

# Export multiple formats
save_pdf_report(report, "oscillator_report.pdf")
save_html_report(report, "oscillator_report.html", interactive_plots=True)

# Print summary
print(f"\n{'='*50}")
print(f"Report: {report.title}")
print(f"{'='*50}")
print(f"Status: {'PASS' if report.all_passed else 'FAIL'}")
print(f"\nMeasurements:")
for name, value in report.measurements.items():
    print(f"  {name}: {value}")
```

## Exercise

Create a custom report workflow:

```python
import numpy as np
import tracekit as tk

# Generate test data
sample_rate = 100e6
duration = 100e-6
frequency = 1e6
amplitude = 2.0
t = np.arange(0, duration, 1/sample_rate)
data = amplitude * np.sin(2 * np.pi * frequency * t) + np.random.normal(0, 0.01, len(t))
test_signal = tk.WaveformTrace(data=data, metadata=tk.TraceMetadata(sample_rate=sample_rate))

# Tasks:
# 1. Define specifications for frequency, amplitude, and SNR
# 2. Generate a report with pass/fail testing
# 3. Add a custom section with test notes
# 4. Export to both PDF and HTML

# Your code here...
```

## CLI Report Generation

Generate reports from the command line:

```bash
# Basic report
tracekit report capture.wfm -o report.pdf

# With options
tracekit report capture.wfm \
    --format html \
    --title "Signal Analysis" \
    --include-spectral \
    -o report.html

# Batch reports
tracekit report captures/*.wfm --output-dir reports/
```

## Next Steps

You've completed the tutorial series. Explore more:

- [Examples Directory](../examples-reference.md)
- [API Reference](../api/index.md)
- [User Guide](../user-guide.md)

## See Also

- [Report Customization Guide](../guides/report-customization.md)
- [Reporting API Reference](../api/reporting.md)
- [CLI Reference](../cli.md)
