# TraceKit Report Customization Guide

This guide shows you how to customize TraceKit analysis reports using the reporting API.

## Quick Start Example

See `examples/01_basics/05_generate_report.py` for a complete working example of report generation.

## 📝 Method 1: Using the Reporting API

TraceKit provides a comprehensive reporting API for creating custom analysis reports.

### Basic Report Generation

```python
from tracekit.reporting import generate_report, save_pdf_report, save_html_report
import tracekit as tk

# Load and analyze your data
trace = tk.load("capture.wfm")

# Generate a report with default settings
report = generate_report(
    trace,
    title="Signal Analysis Report",
    include_plots=True
)

# Save in different formats
save_pdf_report(report, "report.pdf")
save_html_report(report, "report.html")
```

### Custom Report with Sections

```python
from tracekit.reporting import Report, Section

# Create a custom report
report = Report(
    title="XYZ-2000 Communication System Analysis",
    subtitle="Signal Integrity Testing",
    author="John Doe, ABC Corporation",
    date="2025-12-30"
)

# Add custom sections
report.add_section(Section(
    title="Executive Summary",
    content="""
    This report presents the results of signal integrity analysis for the
    XYZ-2000 communication system. Testing was conducted on December 30, 2025
    at the ABC Laboratory. All measurements meet the required specifications
    outlined in standard IEEE 1234-2024.
    """
))

# Add measurement results
measurements = {
    "Frequency": tk.frequency(trace),
    "Rise Time": tk.rise_time(trace),
    "Fall Time": tk.fall_time(trace),
    "Amplitude": tk.amplitude(trace)
}

report.add_section(Section(
    title="Measurements",
    data=measurements
))

# Generate PDF
save_pdf_report(report, "custom_report.pdf")
```

---

## 🎨 Method 2: Configuration-Based Reports

Create a configuration file to control report generation.

### Create `report_config.yaml`:

```yaml
report:
  title: 'Signal Analysis Report - Project XYZ'
  subtitle: 'Digital Waveform and Protocol Analysis'
  author: 'John Doe, ABC Corporation'
  project_name: 'XYZ-2000 Communication System'
  test_date: '2025-12-30'
  laboratory: 'ABC Testing Laboratory'
  standard: 'IEEE 1234-2024'

sections:
  - digital_signal_analysis: true
  - spectral_analysis: true
  - protocol_decoding: true

styling:
  primary_color: '#3498DB'
  secondary_color: '#E74C3C'
  font_size_title: 24
  font_size_heading: 16

branding:
  logo_path: 'assets/company_logo.png'
```

### Use Configuration in Code:

```python
from tracekit.reporting import generate_report
import yaml

# Load configuration
with open("report_config.yaml") as f:
    config = yaml.safe_load(f)

# Generate report using configuration
report = generate_report(
    trace,
    title=config['report']['title'],
    subtitle=config['report']['subtitle'],
    author=config['report']['author'],
    config=config
)

save_pdf_report(report, "configured_report.pdf")
```

---

## 🔧 Method 3: Advanced Customization

For advanced use cases, you can customize report styles and layouts.

### Custom Styling

```python
from tracekit.reporting import ReportStyle

# Define custom style
style = ReportStyle(
    primary_color="#FF6B35",  # Orange
    secondary_color="#004E89",  # Navy
    font_family="Arial",
    font_size_title=26,
    font_size_heading=18,
    page_margins=(0.75, 0.75, 0.75, 0.75)  # inches
)

# Generate report with custom style
report = generate_report(trace, title="Custom Styled Report", style=style)
save_pdf_report(report, "styled_report.pdf")
```

### Adding Company Logo

```python
from reportlab.lib.units import inch

# Add logo to report
report = Report(title="Analysis Report")
report.add_logo("path/to/logo.png", width=2*inch, height=1*inch)
report.add_section(Section(title="Analysis Results", data=measurements))

save_pdf_report(report, "branded_report.pdf")
```

### Custom Plots

```python
import matplotlib.pyplot as plt

# Create custom plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(trace.time, trace.data)
ax.set_title("Signal Waveform")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude (V)")

# Add plot to report
report.add_plot(fig, caption="Measured waveform")
```

---

## 🎯 Common Customizations

### 1. Change Report Title and Metadata

```python
report = Report(
    title="YOUR CUSTOM TITLE",
    subtitle="Project specific subtitle",
    author="Your Name",
    date="2025-12-30",
    project_id="XYZ-2000"
)
```

### 2. Add Project Information Section

```python
project_info = {
    "Project": "XYZ-2000 Communication System",
    "Client": "ABC Corporation",
    "Test Engineer": "John Doe",
    "Laboratory": "ABC Testing Lab",
    "Standard": "IEEE 1234-2024"
}

report.add_section(Section(
    title="Project Information",
    data=project_info,
    layout="table"
))
```

### 3. Customize Color Scheme

```python
style = ReportStyle(
    primary_color="#1E88E5",  # Blue
    secondary_color="#FFC107",  # Amber
    accent_color="#4CAF50"  # Green
)

report = generate_report(trace, style=style)
```

### 4. Add Executive Summary

```python
report.add_section(Section(
    title="Executive Summary",
    content="""
    Testing was performed in accordance with IEEE 1234-2024 requirements.
    All measurements were taken using TraceKit automated analysis tools
    with 100 MHz sampling rate and calibrated probes.

    Key findings:
    - Signal integrity: PASS
    - Protocol compliance: PASS
    - Spectral purity: PASS
    """
))
```

---

## 💡 Best Practices

1. **Use Configuration Files** for project-specific settings
2. **Reuse Report Templates** for consistent formatting
3. **Version Control** your report configurations
4. **Test with Sample Data** before generating production reports
5. **Include Context** - add project info, standards, and test conditions

---

## 📚 API Reference

### Core Functions

- `generate_report()` - Generate a report from trace data
- `save_pdf_report()` - Save report as PDF
- `save_html_report()` - Save report as HTML
- `save_json_report()` - Save report data as JSON

### Classes

- `Report` - Main report container
- `Section` - Report section with title and content
- `ReportStyle` - Styling configuration
- `ReportConfig` - Report generation configuration

See `docs/api/reporting.md` for complete API documentation.

---

## 📖 Examples

### Complete Working Examples

1. **Basic Report**: `examples/01_basics/05_generate_report.py`
   - Simple report generation workflow
   - Measurements and plots
   - Multiple export formats

2. **Configuration File**: `examples/configs/universal_report_config.yaml`
   - Example configuration structure
   - Styling options
   - Section templates

### More Examples

```bash
# Run the basic example
uv run python examples/01_basics/05_generate_report.py

# See all available examples
ls examples/01_basics/
```

---

## 🔍 Troubleshooting

### Missing Dependencies

If PDF generation fails, ensure ReportLab is installed:

```bash
uv pip install tracekit[reporting]
```

### Custom Fonts

To use custom fonts in reports:

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register custom font
pdfmetrics.registerFont(TTFont('CustomFont', 'path/to/font.ttf'))

# Use in style
style = ReportStyle(font_family='CustomFont')
```

### Large Reports

For reports with many plots, consider:

- Reducing plot DPI: `save_pdf_report(report, "file.pdf", dpi=150)`
- Splitting into multiple reports
- Using HTML format instead of PDF

---

## Need Help?

- **API Documentation**: See `docs/api/reporting.md`
- **Examples**: Check `examples/01_basics/05_generate_report.py`
- **Source Code**: See `src/tracekit/reporting/` for implementation details
