# EMC Compliance Testing Guide

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

A practical guide for engineers performing EMC (Electromagnetic Compatibility) and EMI (Electromagnetic Interference) compliance testing using TraceKit.

## Overview

This guide covers:

- EMC test setup and equipment configuration
- Conducted and radiated emissions testing
- Automotive EMC (CISPR 25) procedures
- Immunity testing workflows
- Pre-compliance testing strategies
- Report generation and documentation

### Who This Guide Is For

- EMC test engineers performing compliance testing
- Hardware engineers doing pre-compliance debugging
- Test lab technicians conducting emissions and immunity tests
- Compliance managers preparing regulatory submissions

### Prerequisites

- TraceKit 0.1.0 or later installed
- Basic understanding of EMC concepts
- Familiarity with regulatory requirements (FCC, CE, CISPR)

## 1. Introduction to EMC Testing

### What is EMC Testing?

EMC testing verifies that electronic devices:

1. **Don't emit excessive electromagnetic interference** (emissions testing)
2. **Can operate in the presence of interference** (immunity testing)

### Regulatory Requirements

#### FCC (United States)

- **FCC Part 15** - Unintentional radiators (consumer electronics)
  - Class A: Commercial/industrial equipment
  - Class B: Residential equipment (stricter limits)
- **Test method**: ANSI C63.4

#### CE/CISPR (European Union)

- **CISPR 22/32** - Information technology equipment
  - Class A: Commercial/industrial
  - Class B: Residential
- **CISPR 25** - Automotive components
- **Test method**: CISPR 16-1-1

#### Military Standards

- **MIL-STD-461G** - Military equipment EMC requirements
  - CE101/CE102: Conducted emissions
  - RE102: Radiated emissions
  - CS101: Conducted susceptibility

### Test Types Overview

| Test Type           | Purpose                            | Standards                    |
| ------------------- | ---------------------------------- | ---------------------------- |
| Conducted Emissions | Measure AC/DC power line emissions | FCC Part 15, CISPR 22/32     |
| Radiated Emissions  | Measure electromagnetic field      | FCC Part 15, CISPR 22/32     |
| Conducted Immunity  | Test susceptibility to line noise  | IEC 61000-4-6, MIL-STD-461   |
| Radiated Immunity   | Test susceptibility to RF fields   | IEC 61000-4-3                |
| ESD Immunity        | Electrostatic discharge testing    | IEC 61000-4-2                |
| Surge/Burst         | Transient immunity                 | IEC 61000-4-4, IEC 61000-4-5 |
| Automotive EMC      | Vehicle component testing          | CISPR 25                     |

## 2. Test Setup and Equipment

### Required Equipment

#### Emissions Testing

**Conducted Emissions:**

- Line Impedance Stabilization Network (LISN)
- Spectrum analyzer or EMI receiver
- RF cables (50Ω, calibrated)
- Power supply (clean, stable)

**Radiated Emissions:**

- Semi-anechoic chamber or open area test site (OATS)
- Calibrated antennas (biconical, log-periodic, horn)
- Spectrum analyzer or EMI receiver
- Turntable for DUT positioning
- Antenna mast (adjustable 1m - 4m height)

#### Immunity Testing

- Signal generators (RF, pulse, ESD gun)
- Current injection probes
- Power amplifiers
- Coupling/decoupling networks (CDN)
- Field probes

### TraceKit Integration

TraceKit connects to test equipment via:

1. **Direct file import** - Load saved traces from spectrum analyzers
2. **SCPI control** - Automate measurements via LAN/USB
3. **Data logging** - Real-time acquisition during testing

```python
import tracekit as tk

# Load spectrum analyzer data
trace = tk.load("emissions_scan.wfm")

# Or control via SCPI (example)
from tracekit.instruments import SpectrumAnalyzer

analyzer = SpectrumAnalyzer("TCPIP::192.168.1.100::INSTR")
analyzer.configure(start_freq=30e6, stop_freq=1e9, rbw=120e3)
trace = analyzer.acquire()
```

### Antenna Selection

| Frequency Range  | Antenna Type   | Notes                       |
| ---------------- | -------------- | --------------------------- |
| 9 kHz - 30 MHz   | Rod / Loop     | Near-field measurements     |
| 30 MHz - 200 MHz | Biconical      | Omnidirectional, linear pol |
| 200 MHz - 1 GHz  | Log-Periodic   | Wideband, directional       |
| 1 GHz - 18 GHz   | Horn           | High gain, narrowband       |
| 18 GHz - 40 GHz  | Waveguide horn | Microwave testing           |

### Test Environment

#### Semi-Anechoic Chamber Requirements

- RF absorbers on walls and ceiling
- Conductive ground plane
- Ambient noise floor < limit - 6 dB
- Site attenuation verification (NSA check)

#### Open Area Test Site (OATS)

- Flat, open area (30m x 30m minimum)
- Low ambient RF noise
- Ground plane (wire mesh or metal)
- Weather protection for equipment

## 3. Conducted Emissions Testing

Conducted emissions testing measures unwanted RF energy coupled onto power and signal cables.

### 3.1 FCC Part 15 Conducted Emissions Setup

#### Test Configuration

```
┌─────────────┐         ┌──────┐         ┌────────────┐
│   AC Mains  │────────▶│ LISN │────────▶│  Spectrum  │
│   Source    │         │      │         │  Analyzer  │
└─────────────┘         └──┬───┘         └────────────┘
                           │
                        ┌──▼──┐
                        │ DUT │
                        └─────┘
```

#### Equipment Setup

1. **Connect LISN** between AC source and DUT
2. **Connect spectrum analyzer** to LISN RF output (50Ω)
3. **Set analyzer parameters**:
   - Frequency range: 150 kHz - 30 MHz
   - Resolution bandwidth (RBW): 9 kHz
   - Detector: Quasi-peak
   - Sweep time: Per CISPR 16-1-1

#### TraceKit Workflow

```python
import tracekit as tk
from tracekit.compliance import load_limit_mask, check_compliance, generate_compliance_report

# Load conducted emissions measurement
trace = tk.load("conducted_emissions_line1.wfm")

# Load FCC Part 15 Class B conducted limits
fcc_mask = load_limit_mask("FCC_Part15_ClassB_Conducted")

print(f"Testing conducted emissions: 150 kHz - 30 MHz")
print(f"Limit: {fcc_mask.description}")
print(f"Detector: {fcc_mask.detector}")

# Check compliance
result = check_compliance(
    trace,
    fcc_mask,
    detector="quasi-peak",
    frequency_range=(150e3, 30e6),
    unit_conversion="V_to_dBuV"
)

# Display results
print(f"\n{'='*60}")
print(f"FCC PART 15 CONDUCTED EMISSIONS TEST RESULTS")
print(f"{'='*60}")
print(f"Status: {result.status}")
print(f"Margin to limit: {result.margin_to_limit:+.1f} dB")

if result.passed:
    print(f"\n✓ PASS - Minimum margin: {result.margin_to_limit:.1f} dB")
    print(f"  Worst case at {result.worst_frequency / 1e6:.3f} MHz")
else:
    print(f"\n✗ FAIL - {result.violation_count} violations detected")
    print("\nTop 5 violations:")
    for i, v in enumerate(result.violations[:5], 1):
        print(f"{i}. {v.frequency / 1e6:7.3f} MHz: "
              f"{v.measured_level:5.1f} dBµV "
              f"(limit: {v.limit_level:5.1f} dBµV, "
              f"excess: +{v.excess_db:.1f} dB)")

# Generate report
generate_compliance_report(
    result,
    "fcc_conducted_emissions_report.html",
    title="FCC Part 15 Class B Conducted Emissions Test",
    company_name="Example Electronics Inc.",
    dut_info={
        "Product": "Switching Power Supply Model PS-100",
        "Model": "PS-100",
        "Serial Number": "SN123456",
        "Test Standard": "FCC Part 15 Subpart B",
        "Test Method": "ANSI C63.4-2014",
        "Test Date": "2026-01-08",
        "Test Engineer": "J. Smith",
        "LISN": "50µH + 5Ω || 50Ω",
        "Line": "Line 1 (L1)",
        "Measurement Distance": "N/A (conducted)",
    }
)
```

### 3.2 CISPR 22/32 Conducted Emissions

CISPR standards use similar setup to FCC but with different limit masks.

```python
import tracekit as tk
from tracekit.compliance import load_limit_mask, check_compliance

# Load measurement
trace = tk.load("cispr32_conducted_emissions.wfm")

# Load CISPR 32 Class B conducted limits
cispr32_mask = load_limit_mask("CE_CISPR32_ClassB_Conducted")

# Check compliance
result = check_compliance(
    trace,
    cispr32_mask,
    detector="quasi-peak",  # CISPR requires quasi-peak
    frequency_range=(150e3, 30e6)
)

print(f"CISPR 32 Class B Conducted Emissions: {result.status}")
print(f"Margin: {result.margin_to_limit:+.1f} dB")

# Also check with average detector per CISPR 32
result_avg = check_compliance(
    trace,
    cispr32_mask,
    detector="average"
)

print(f"Average detector margin: {result_avg.margin_to_limit:+.1f} dB")
```

### 3.3 Multi-Line Testing

Test both power lines and generate combined report:

```python
import tracekit as tk
from tracekit.compliance import load_limit_mask, check_compliance
import matplotlib.pyplot as plt

# Test both lines
lines = {
    "Line 1 (L1)": "conducted_line1.wfm",
    "Line 2 (L2)": "conducted_line2.wfm",
}

mask = load_limit_mask("FCC_Part15_ClassB_Conducted")
results = {}

print("Testing conducted emissions on both power lines...")
print()

for line_name, filename in lines.items():
    trace = tk.load(filename)
    result = check_compliance(
        trace,
        mask,
        detector="quasi-peak",
        unit_conversion="V_to_dBuV"
    )
    results[line_name] = result

    status_symbol = "✓" if result.passed else "✗"
    print(f"{line_name}: {status_symbol} {result.status} "
          f"(margin: {result.margin_to_limit:+.1f} dB)")

# Plot both lines
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

for ax, (line_name, result) in zip([ax1, ax2], results.items()):
    ax.semilogx(result.spectrum_freq / 1e6, result.spectrum_level,
                'b-', linewidth=1.5, label=f'{line_name} Measured')
    ax.semilogx(result.spectrum_freq / 1e6, result.limit_level,
                'r--', linewidth=2, label='FCC Limit')

    if result.violations:
        viol_freq = [v.frequency / 1e6 for v in result.violations]
        viol_level = [v.measured_level for v in result.violations]
        ax.scatter(viol_freq, viol_level, c='red', s=50,
                   marker='x', zorder=5, label='Violations')

    ax.set_xlabel('Frequency (MHz)')
    ax.set_ylabel('Level (dBµV)')
    ax.set_title(f'Conducted Emissions - {line_name}')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()
    ax.set_xlim(0.15, 30)

plt.tight_layout()
plt.savefig('conducted_emissions_both_lines.png', dpi=150)
plt.show()

# Determine overall pass/fail
overall_pass = all(r.passed for r in results.values())
print(f"\nOverall result: {'PASS' if overall_pass else 'FAIL'}")
```

### 3.4 Data Acquisition Best Practices

**Measurement Settings:**

```python
# Recommended spectrum analyzer settings for conducted emissions
settings = {
    "frequency_range": (150e3, 30e6),
    "rbw": 9e3,              # 9 kHz per CISPR 16-1-1
    "vbw": 30e3,             # 3x RBW typical
    "detector": "quasi-peak", # CISPR requirement
    "sweep_time": "auto",    # Or calculate per standard
    "attenuation": 10,       # 10 dB typical
    "ref_level": 100,        # 100 dBµV
}
```

**Multiple Sweeps for Consistency:**

```python
import tracekit as tk
import numpy as np

# Take multiple sweeps and check repeatability
sweeps = []
for i in range(3):
    trace = tk.load(f"conducted_sweep_{i+1}.wfm")
    sweeps.append(trace)

# Check if measurements are consistent
from tracekit.analyzers.spectral import fft

spectra = [fft(sweep) for sweep in sweeps]
# Calculate standard deviation across sweeps
freq = spectra[0][0]
mags = np.array([np.abs(spec[1]) for spec in spectra])
std_dev = np.std(mags, axis=0)

# Flag if standard deviation exceeds 2 dB
problematic = std_dev > 2.0
if np.any(problematic):
    print("⚠ Warning: Measurement repeatability issue detected")
    print(f"Frequencies with high variation: "
          f"{freq[problematic] / 1e6} MHz")
else:
    print("✓ Measurements are repeatable")

# Use average of sweeps for final test
avg_magnitude = np.mean(mags, axis=0)
result = check_compliance((freq, avg_magnitude), mask)
```

## 4. Radiated Emissions Testing

Radiated emissions testing measures electromagnetic fields radiated from the DUT and cables.

### 4.1 Test Setup

#### FCC Part 15 Radiated Emissions Configuration

**Measurement Distance:**

- Class B: 3 meters
- Class A: 10 meters

**Frequency Range:**

- 30 MHz - 1000 MHz (or higher for devices with clock > 108 MHz)

**Test Procedure:**

1. Place DUT on turntable
2. Position antenna at specified distance
3. Adjust antenna height (1m - 4m scan)
4. Rotate DUT 360° to find maximum emission
5. Measure both horizontal and vertical polarization

```python
import tracekit as tk
from tracekit.compliance import load_limit_mask, check_compliance, generate_compliance_report
import numpy as np

# Load radiated emissions measurement (worst case from scan)
trace = tk.load("radiated_emissions_3m_horizontal.wfm")

# Load FCC Part 15 Class B radiated limits
fcc_mask = load_limit_mask("FCC_Part15_ClassB")

print(f"FCC Part 15 Class B Radiated Emissions Test")
print(f"Frequency range: {fcc_mask.frequency_range[0] / 1e6:.1f} - "
      f"{fcc_mask.frequency_range[1] / 1e6:.1f} MHz")
print(f"Measurement distance: {fcc_mask.distance}m")

# Check compliance
result = check_compliance(
    trace,
    fcc_mask,
    detector="quasi-peak",
    frequency_range=(30e6, 1000e6),
    unit_conversion="V_to_dBuV"
)

# Analyze results
print(f"\n{'='*60}")
print(f"TEST RESULTS - Horizontal Polarization")
print(f"{'='*60}")
print(f"Status: {result.status}")
print(f"Margin to limit: {result.margin_to_limit:+.1f} dB")
print(f"Worst frequency: {result.worst_frequency / 1e6:.3f} MHz")

if not result.passed:
    print(f"\nViolations: {result.violation_count}")
    print("\nViolation details:")
    for v in result.violations:
        print(f"  {v.frequency / 1e6:7.3f} MHz: "
              f"{v.measured_level:5.1f} dBµV/m "
              f"(limit: {v.limit_level:5.1f} dBµV/m, "
              f"excess: +{v.excess_db:.1f} dB, "
              f"severity: {v.severity})")
else:
    print(f"\n✓ PASS with {result.margin_to_limit:.1f} dB margin")

# Generate compliance report
generate_compliance_report(
    result,
    "fcc_radiated_emissions_report.html",
    title="FCC Part 15 Class B Radiated Emissions Test",
    company_name="Example Electronics Inc.",
    dut_info={
        "Product": "Wireless Router Model WR-5000",
        "Model": "WR-5000",
        "FCC ID": "ABC-WR5000",
        "Serial Number": "SN789012",
        "Test Standard": "FCC Part 15 Subpart B",
        "Test Method": "ANSI C63.4-2014",
        "Test Date": "2026-01-08",
        "Test Engineer": "J. Smith",
        "Test Lab": "EMC Testing Lab (FCC Listed)",
        "Chamber": "SAC-10 (10m semi-anechoic)",
        "Distance": "3 meters",
        "Polarization": "Horizontal",
        "Antenna": "Biconical (30-200 MHz) + Log Periodic (200-1000 MHz)",
        "Turntable": "2m diameter, wooden, motorized",
        "Ambient Temperature": "23°C",
        "Relative Humidity": "45%",
    }
)
```

### 4.2 Antenna Calibration and Height Scan

```python
import tracekit as tk
from tracekit.compliance import check_compliance, load_limit_mask
import numpy as np
import matplotlib.pyplot as plt

# Load measurements at different antenna heights
heights = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]  # meters
traces = {}

for h in heights:
    filename = f"radiated_scan_height_{h:.1f}m.wfm"
    traces[h] = tk.load(filename)

# Find worst-case height
mask = load_limit_mask("FCC_Part15_ClassB")
margins = {}

for height, trace in traces.items():
    result = check_compliance(trace, mask, detector="quasi-peak")
    margins[height] = result.margin_to_limit

# Plot margin vs height
plt.figure(figsize=(10, 6))
plt.plot(list(margins.keys()), list(margins.values()),
         'o-', linewidth=2, markersize=8)
plt.axhline(y=0, color='r', linestyle='--', label='Compliance Threshold')
plt.xlabel('Antenna Height (m)')
plt.ylabel('Margin to Limit (dB)')
plt.title('Radiated Emissions Margin vs Antenna Height')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('antenna_height_scan.png', dpi=150)
plt.show()

# Find worst case
worst_height = min(margins, key=margins.get)
worst_margin = margins[worst_height]

print(f"Worst case antenna height: {worst_height:.1f}m")
print(f"Margin at worst height: {worst_margin:+.1f} dB")

# Use worst case for final compliance test
worst_trace = traces[worst_height]
final_result = check_compliance(worst_trace, mask, detector="quasi-peak")

generate_compliance_report(
    final_result,
    "radiated_emissions_worst_case.html",
    title="FCC Part 15 Class B - Worst Case Configuration",
    dut_info={
        "Antenna Height": f"{worst_height:.1f}m (worst case from 1-4m scan)",
        "Polarization": "Horizontal",
    }
)
```

### 4.3 Peak Detection and Refinement

For accurate quasi-peak measurements, first identify peaks:

```python
import tracekit as tk
from tracekit.analyzers.spectral import find_spectral_peaks
from tracekit.compliance import check_compliance, load_limit_mask

# Load peak detector sweep (fast)
trace_peak = tk.load("radiated_peak_sweep.wfm")

# Find peaks exceeding threshold
from tracekit.analyzers.spectral import fft
import numpy as np

freq, mag = fft(trace_peak)
mag_db = 20 * np.log10(np.abs(mag) + 1e-12)

# Find peaks within 6 dB of limit
mask = load_limit_mask("FCC_Part15_ClassB")
limit_at_freq = mask.interpolate(freq)

# Identify peaks of interest (within 10 dB of limit)
margin = limit_at_freq - mag_db
peaks_of_interest = np.where(margin < 10)[0]

print(f"Found {len(peaks_of_interest)} peaks within 10 dB of limit")
print("\nPeaks requiring quasi-peak measurement:")

for idx in peaks_of_interest:
    print(f"  {freq[idx] / 1e6:7.3f} MHz: "
          f"{mag_db[idx]:5.1f} dBµV/m "
          f"(margin: {margin[idx]:+.1f} dB)")

# Now measure these peaks with quasi-peak detector
# (In practice, reconfigure spectrum analyzer for quasi-peak at these frequencies)
print(f"\nConfigure spectrum analyzer for quasi-peak measurements at:")
print(f"  Frequencies: {freq[peaks_of_interest] / 1e6} MHz")
print(f"  RBW: 120 kHz")
print(f"  Detector: Quasi-peak")
print(f"  Sweep time: ≥ 1 second per point")
```

### 4.4 Margin Analysis

```python
import tracekit as tk
from tracekit.compliance import check_compliance, load_limit_mask
import matplotlib.pyplot as plt
import numpy as np

# Load final radiated emissions data
trace = tk.load("radiated_emissions_final.wfm")
mask = load_limit_mask("FCC_Part15_ClassB")

result = check_compliance(trace, mask, detector="quasi-peak")

# Calculate margin across entire frequency range
margin_db = result.limit_level - result.spectrum_level

# Plot spectrum with margin
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Top: Spectrum vs Limit
ax1.semilogx(result.spectrum_freq / 1e6, result.spectrum_level,
             'b-', linewidth=1.5, label='Measured Emissions')
ax1.semilogx(result.spectrum_freq / 1e6, result.limit_level,
             'r--', linewidth=2, label='FCC Class B Limit')

if result.violations:
    viol_freq = [v.frequency / 1e6 for v in result.violations]
    viol_level = [v.measured_level for v in result.violations]
    ax1.scatter(viol_freq, viol_level, c='red', s=100,
                marker='x', zorder=5, linewidths=3, label='Violations')

ax1.set_ylabel('Field Strength (dBµV/m)')
ax1.set_title('FCC Part 15 Class B Radiated Emissions @ 3m')
ax1.grid(True, which='both', alpha=0.3)
ax1.legend()

# Bottom: Margin plot
ax2.semilogx(result.spectrum_freq / 1e6, margin_db, 'g-', linewidth=1.5)
ax2.axhline(y=0, color='r', linestyle='--', linewidth=2, label='Compliance Threshold')
ax2.axhline(y=6, color='orange', linestyle=':', linewidth=2, label='6 dB Margin')
ax2.fill_between(result.spectrum_freq / 1e6, 0, margin_db,
                  where=(margin_db >= 0), alpha=0.3, color='green',
                  label='Passing Region')
ax2.fill_between(result.spectrum_freq / 1e6, 0, margin_db,
                  where=(margin_db < 0), alpha=0.3, color='red',
                  label='Failing Region')

ax2.set_xlabel('Frequency (MHz)')
ax2.set_ylabel('Margin to Limit (dB)')
ax2.set_title('Compliance Margin Analysis')
ax2.grid(True, which='both', alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.savefig('radiated_emissions_margin_analysis.png', dpi=150)
plt.show()

# Statistical analysis
print(f"Margin Statistics:")
print(f"  Minimum: {np.min(margin_db):+.1f} dB @ "
      f"{result.spectrum_freq[np.argmin(margin_db)] / 1e6:.3f} MHz")
print(f"  Maximum: {np.max(margin_db):+.1f} dB")
print(f"  Mean: {np.mean(margin_db):+.1f} dB")
print(f"  Median: {np.median(margin_db):+.1f} dB")

# Warning if margin < 6 dB
critical_margins = margin_db < 6
if np.any(critical_margins):
    print(f"\n⚠ Warning: {np.sum(critical_margins)} frequency points "
          f"have < 6 dB margin")
    critical_freq = result.spectrum_freq[critical_margins]
    print(f"  Critical frequencies: {critical_freq / 1e6} MHz")
```

## 5. Automotive EMC (CISPR 25)

CISPR 25 specifies EMC requirements for automotive components and subsystems.

### 5.1 Test Configuration

Automotive EMC testing uses specialized setups:

- **Measurement distance**: 1 meter (vertical antenna)
- **Frequency range**: 150 kHz - 2500 MHz
- **Detector**: Broadband (peak) and narrowband (quasi-peak)
- **Test methods**: Stripline, TEM cell, ALSE, absorber-lined chamber

### 5.2 CISPR 25 Limit Masks

```python
import tracekit as tk
from tracekit.compliance import create_custom_mask, check_compliance

# Create CISPR 25 Class 5 broadband limit (most stringent)
cispr25_class5 = create_custom_mask(
    name="CISPR_25_Class5_Broadband",
    frequencies=[
        150e3,    # 150 kHz
        5.9e6,    # 5.9 MHz
        6.2e6,    # 6.2 MHz
        30e6,     # 30 MHz
        54e6,     # 54 MHz (TV Band I)
        88e6,     # 88 MHz (FM start)
        108e6,    # 108 MHz (FM end)
        174e6,    # 174 MHz (TV Band III)
        230e6,    # 230 MHz
        470e6,    # 470 MHz (TV Band IV/V)
        1000e6,   # 1 GHz
        2500e6,   # 2.5 GHz
    ],
    limits=[
        24,  # 150 kHz: 24 dBµV (linear)
        24,  # 5.9 MHz: 24 dBµV
        10,  # 6.2 MHz: 10 dBµV (AM broadcast protection)
        4,   # 30 MHz: 4 dBµV
        0,   # 54 MHz: 0 dBµV (TV Band I)
        -2,  # 88 MHz: -2 dBµV (FM protection)
        -6,  # 108 MHz: -6 dBµV
        -6,  # 174 MHz: -6 dBµV
        -6,  # 230 MHz: -6 dBµV
        -6,  # 470 MHz: -6 dBµV
        -6,  # 1 GHz: -6 dBµV
        -6,  # 2.5 GHz: -6 dBµV
    ],
    unit="dBuV",
    description="CISPR 25 Class 5 Broadband Radiated Emissions (Peak)",
    detector="peak",
    distance=1.0,
    regulatory_body="ISO",
    document="CISPR 25:2021 Table A.1"
)

# Create CISPR 25 Class 5 narrowband limit (average detector)
cispr25_class5_nb = create_custom_mask(
    name="CISPR_25_Class5_Narrowband",
    frequencies=[
        150e3, 30e6, 54e6, 88e6, 108e6, 174e6,
        230e6, 470e6, 1000e6, 2500e6
    ],
    limits=[
        14, -6, -10, -12, -16, -16,
        -16, -16, -16, -16
    ],
    unit="dBuV",
    description="CISPR 25 Class 5 Narrowband Radiated Emissions (Average)",
    detector="average",
    distance=1.0,
    regulatory_body="ISO",
    document="CISPR 25:2021 Table A.1"
)

# Test automotive ECU
ecu_trace = tk.load("automotive_ecu_emissions.wfm")

# Test broadband (peak detector)
print("CISPR 25 Automotive EMC Test - Broadband")
print("="*60)
result_bb = check_compliance(
    ecu_trace,
    cispr25_class5,
    detector="peak",
    frequency_range=(150e3, 2500e6)
)

print(f"Broadband (Peak): {result_bb.status}")
print(f"  Margin: {result_bb.margin_to_limit:+.1f} dB")
print(f"  Worst frequency: {result_bb.worst_frequency / 1e6:.3f} MHz")

# Test narrowband (average detector)
result_nb = check_compliance(
    ecu_trace,
    cispr25_class5_nb,
    detector="average",
    frequency_range=(150e3, 2500e6)
)

print(f"\nNarrowband (Average): {result_nb.status}")
print(f"  Margin: {result_nb.margin_to_limit:+.1f} dB")

# Overall result
overall_pass = result_bb.passed and result_nb.passed
print(f"\n{'='*60}")
print(f"Overall CISPR 25 Class 5 Result: {'PASS' if overall_pass else 'FAIL'}")
print(f"{'='*60}")

if not overall_pass:
    print("\nFailed tests:")
    if not result_bb.passed:
        print(f"  - Broadband: {result_bb.violation_count} violations")
    if not result_nb.passed:
        print(f"  - Narrowband: {result_nb.violation_count} violations")
```

### 5.3 Automotive Component Testing Workflow

```python
import tracekit as tk
from tracekit.compliance import create_custom_mask, check_compliance, generate_compliance_report
import matplotlib.pyplot as plt

# Test multiple vehicle components
components = {
    "Engine ECU": "ecu_emissions.wfm",
    "Infotainment": "infotainment_emissions.wfm",
    "Body Control Module": "bcm_emissions.wfm",
    "Instrument Cluster": "cluster_emissions.wfm",
}

# Load mask
cispr25_mask = create_custom_mask(
    name="CISPR_25_Class5",
    frequencies=[150e3, 30e6, 54e6, 88e6, 108e6, 174e6, 1000e6, 2500e6],
    limits=[24, 4, 0, -2, -6, -6, -6, -6],
    unit="dBuV",
    description="CISPR 25 Class 5 Broadband",
    detector="peak"
)

# Test all components
results = {}
print("Testing automotive components per CISPR 25...")
print()

for component, filename in components.items():
    trace = tk.load(filename)
    result = check_compliance(trace, cispr25_mask, detector="peak")
    results[component] = result

    status_symbol = "✓" if result.passed else "✗"
    print(f"{component:25s}: {status_symbol} {result.status:4s} "
          f"(margin: {result.margin_to_limit:+6.1f} dB)")

# Generate summary report
print(f"\n{'='*70}")
print(f"AUTOMOTIVE EMC COMPLIANCE SUMMARY")
print(f"{'='*70}")

pass_count = sum(1 for r in results.values() if r.passed)
total_count = len(results)

print(f"Pass rate: {pass_count}/{total_count} "
      f"({pass_count/total_count*100:.1f}%)")

if pass_count == total_count:
    print("\n✓ All components meet CISPR 25 Class 5 requirements")
else:
    print(f"\n✗ {total_count - pass_count} component(s) failed")
    print("\nFailed components:")
    for component, result in results.items():
        if not result.passed:
            print(f"  - {component}: {result.violation_count} violations, "
                  f"worst at {result.worst_frequency / 1e6:.3f} MHz")

# Plot all components on one graph
plt.figure(figsize=(14, 8))

colors = ['blue', 'green', 'purple', 'orange']
for (component, result), color in zip(results.items(), colors):
    plt.semilogx(result.spectrum_freq / 1e6, result.spectrum_level,
                 linewidth=1.5, label=component, alpha=0.7, color=color)

# Plot limit
plt.semilogx(result.limit_level[:, 0] / 1e6, result.limit_level[:, 1],
             'r--', linewidth=2.5, label='CISPR 25 Class 5 Limit')

plt.xlabel('Frequency (MHz)')
plt.ylabel('Emission Level (dBµV)')
plt.title('Automotive Component Emissions - CISPR 25 Class 5')
plt.grid(True, which='both', alpha=0.3)
plt.legend()
plt.xlim(0.15, 2500)
plt.tight_layout()
plt.savefig('automotive_components_comparison.png', dpi=150)
plt.show()
```

### 5.4 Pass/Fail Determination

```python
import tracekit as tk
from tracekit.compliance import check_compliance, create_custom_mask

# CISPR 25 requires testing at multiple supply voltages
test_voltages = [9, 12, 16]  # Volts (low, nominal, high)
results_by_voltage = {}

cispr25_mask = create_custom_mask(
    name="CISPR_25_Class5",
    frequencies=[150e3, 30e6, 108e6, 1000e6, 2500e6],
    limits=[24, 4, -6, -6, -6],
    unit="dBuV",
    detector="peak"
)

print("CISPR 25 Testing at Multiple Supply Voltages")
print("="*60)

for voltage in test_voltages:
    filename = f"ecu_emissions_{voltage}V.wfm"
    trace = tk.load(filename)
    result = check_compliance(trace, cispr25_mask, detector="peak")
    results_by_voltage[voltage] = result

    status = "✓ PASS" if result.passed else "✗ FAIL"
    print(f"{voltage:2d}V: {status} (margin: {result.margin_to_limit:+.1f} dB)")

# Overall pass requires all voltages to pass
overall_pass = all(r.passed for r in results_by_voltage.values())

print(f"\n{'='*60}")
if overall_pass:
    print("✓ COMPONENT PASSES CISPR 25 at all supply voltages")
    min_margin = min(r.margin_to_limit for r in results_by_voltage.values())
    print(f"  Minimum margin across all tests: {min_margin:.1f} dB")
else:
    print("✗ COMPONENT FAILS CISPR 25")
    for voltage, result in results_by_voltage.items():
        if not result.passed:
            print(f"  Failed at {voltage}V: {result.violation_count} violations")
```

## 6. Immunity Testing

Immunity testing verifies that devices can operate correctly in the presence of electromagnetic disturbances.

### 6.1 ESD Testing (IEC 61000-4-2)

Electrostatic discharge testing simulates ESD events.

**Test Levels:**

| Level | Contact Discharge | Air Discharge |
| ----- | ----------------- | ------------- |
| 1     | ±2 kV             | ±2 kV         |
| 2     | ±4 kV             | ±4 kV         |
| 3     | ±6 kV             | ±8 kV         |
| 4     | ±8 kV             | ±15 kV        |

**Test Procedure:**

1. Apply ESD to specified points (direct contact)
2. Apply ESD to horizontal/vertical coupling planes (indirect)
3. Monitor DUT for malfunctions during and after test
4. Record Pass/Fail per IEC 61000-4-2 criteria

```python
import tracekit as tk
from tracekit.compliance import create_custom_mask, check_compliance
import numpy as np

# Create ESD pulse envelope mask per IEC 61000-4-2
# Standard ESD pulse: ~0.7-1ns rise time, 30-60ns first peak
esd_level3_mask = create_custom_mask(
    name="IEC_61000_4_2_Level3_Contact",
    frequencies=[  # Time points for envelope
        0,       # Start
        0.7e-9,  # 0.7 ns rise to first peak
        30e-9,   # 30 ns first peak
        60e-9,   # 60 ns decay
        100e-9,  # Ringing
        200e-9,  # Further decay
    ],
    limits=[  # Voltage envelope
        0,     # 0V
        6000,  # 6 kV peak (Level 3 contact)
        4000,  # Current decay
        2000,  # Ringing envelope
        500,   # Decay continues
        0,     # Return to baseline
    ],
    unit="V",
    description="IEC 61000-4-2 ESD Level 3 Contact Discharge Envelope",
    detector="peak",
    regulatory_body="IEC",
    document="IEC 61000-4-2:2008"
)

# Load ESD pulse measurement
esd_pulse = tk.load("esd_6kv_contact.wfm")

# For time-domain immunity, check if pulse is within spec
time = np.arange(len(esd_pulse.data)) / esd_pulse.metadata.sample_rate
voltage = np.abs(esd_pulse.data)

result = check_compliance(
    (time, voltage),
    esd_level3_mask,
    detector="peak"
)

print("IEC 61000-4-2 ESD Immunity Test - Level 3 (±6 kV)")
print("="*60)
print(f"ESD Generator Verification: {result.status}")

if result.passed:
    print(f"✓ ESD generator produces proper Level 3 pulse")
    print(f"  Peak voltage: {np.max(voltage):.0f} V")
    print(f"  Rise time: {esd_pulse.metadata.get('rise_time', 'N/A')}")
else:
    print(f"✗ ESD generator pulse out of specification")
    print(f"  Peak exceeded by: {-result.worst_margin:.1f} dB")

# Immunity test results
# (Typically logged manually or via automated test system)
print("\nESD Immunity Test Results:")
print("  Contact discharge: ±6 kV to all accessible points")
print("  Number of discharges: 10 per polarity per point")

# Example immunity results
test_points = {
    "USB Port": "PASS",
    "Power Jack": "PASS",
    "Reset Button": "FAIL - System reset occurred",
    "Ethernet Port": "PASS",
    "Display Bezel": "PASS",
}

print("\nTest Point Results:")
for point, result in test_points.items():
    symbol = "✓" if "PASS" in result else "✗"
    print(f"  {symbol} {point:20s}: {result}")

# Overall determination per IEC 61000-4-2 criteria
# Criteria A: Normal operation
# Criteria B: Temporary loss of function, self-recoverable
# Criteria C: Temporary loss, operator intervention needed
# Criteria D: Non-recoverable (failure)

overall_result = "FAIL" if any("FAIL" in r for r in test_points.values()) else "PASS"
print(f"\nOverall ESD Immunity: {overall_result}")
```

### 6.2 Surge Testing (IEC 61000-4-5)

Surge immunity testing for AC/DC power lines.

```python
import tracekit as tk
from tracekit.compliance import create_custom_mask, check_compliance

# IEC 61000-4-5 surge pulse (1.2/50 µs voltage wave)
surge_level3_mask = create_custom_mask(
    name="IEC_61000_4_5_Level3",
    frequencies=[  # Time points
        0,        # Start
        1.2e-6,   # 1.2 µs to 90% peak (front time)
        1.67e-6,  # Peak
        50e-6,    # 50 µs to 50% (time to half value)
        100e-6,   # Decay tail
    ],
    limits=[  # Voltage levels for Level 3
        0,     # 0V
        1800,  # 90% of 2 kV
        2000,  # 2 kV peak
        1000,  # 50% at 50 µs
        0,     # Decay complete
    ],
    unit="V",
    description="IEC 61000-4-5 Surge Level 3 (2kV line-to-earth)",
    detector="peak",
    regulatory_body="IEC",
    document="IEC 61000-4-5:2014"
)

# Load surge pulse
surge_trace = tk.load("surge_2kv_line_to_earth.wfm")

# Verify surge generator
time = np.arange(len(surge_trace.data)) / surge_trace.metadata.sample_rate
voltage = np.abs(surge_trace.data)

result = check_compliance((time, voltage), surge_level3_mask)

print("IEC 61000-4-5 Surge Immunity Test - Level 3 (2 kV)")
print("="*60)
print(f"Surge Generator: {result.status}")

# Log immunity test results
print("\nSurge Immunity Results (2 kV line-to-earth):")
print("  Configuration: Line to Earth")
print("  Repetition rate: 1 surge per minute")
print("  Number of surges: 5 positive + 5 negative")
print("  Phase angle: 0°, 90°, 180°, 270°")

immunity_results = {
    "0°": "PASS - Criteria A",
    "90°": "PASS - Criteria A",
    "180°": "PASS - Criteria B (temporary glitch, self-recovered)",
    "270°": "PASS - Criteria A",
}

for phase, result in immunity_results.items():
    print(f"    {phase:5s}: {result}")

print("\nOverall: PASS per IEC 61000-4-5")
```

### 6.3 Bulk Current Injection (BCI) - ISO 11452-4

```python
import tracekit as tk
from tracekit.compliance import create_custom_mask, check_compliance
import numpy as np

# ISO 11452-4 BCI testing for automotive
# Typical requirement: 60 mA injected current, 1 MHz - 400 MHz

bci_mask = create_custom_mask(
    name="ISO_11452_4_Level3",
    frequencies=[1e6, 400e6],  # 1 MHz - 400 MHz
    limits=[60, 60],            # 60 mA constant across band
    unit="mA",
    description="ISO 11452-4 BCI Level 3",
    detector="rms",
    regulatory_body="ISO",
    document="ISO 11452-4:2020"
)

# Load BCI calibration data
bci_cal = tk.load("bci_calibration.wfm")

# Verify injected current level
result = check_compliance(
    bci_cal,
    bci_mask,
    detector="rms",
    frequency_range=(1e6, 400e6)
)

print("ISO 11452-4 Bulk Current Injection Immunity Test")
print("="*60)
print(f"Injected Current Verification: {result.status}")
print(f"Target current: 60 mA RMS")

# Monitor DUT during BCI sweep
print("\nBCI Immunity Test Results:")
print("  Frequency sweep: 1 MHz - 400 MHz")
print("  Dwell time: 1 second per frequency")
print("  Step size: 1% (logarithmic)")
print("  Injected current: 60 mA")

# Example: Frequencies where DUT showed susceptibility
susceptible_freqs = [
    (27.3e6, "Criteria B - Display flicker"),
    (156.8e6, "Criteria C - Communication loss, required reset"),
]

if susceptible_freqs:
    print("\n⚠ Susceptible frequencies detected:")
    for freq, description in susceptible_freqs:
        print(f"    {freq / 1e6:.1f} MHz: {description}")
    print("\nOverall: FAIL - Requires design improvement")
else:
    print("\n✓ No susceptibility detected across full frequency range")
    print("Overall: PASS")
```

## 7. Pre-Compliance Testing

Pre-compliance testing helps identify and fix EMC issues early in development, before expensive formal testing.

### 7.1 Desktop Testing Strategies

Desktop EMC testing uses simplified setups:

**Equipment:**

- Near-field probes (E-field and H-field)
- Portable spectrum analyzer
- Current probes
- RF generator for immunity checks

```python
import tracekit as tk
from tracekit.compliance import load_limit_mask, check_compliance
import numpy as np
import matplotlib.pyplot as plt

# Pre-compliance radiated emissions with near-field probe
# Results won't match formal test but help identify issues

print("Pre-Compliance EMC Testing - Desktop Setup")
print("="*60)

# Load near-field measurement
trace = tk.load("nearfield_probe_scan.wfm")

# Use FCC mask as reference (expect higher readings in near-field)
fcc_mask = load_limit_mask("FCC_Part15_ClassB")

# Add offset for near-field to far-field estimation
# Rough approximation: near-field ~30 dB higher than far-field
NEARFIELD_OFFSET = 30  # dB

# Check against limit + offset
from tracekit.analyzers.spectral import fft
freq, mag = fft(trace)
mag_db = 20 * np.log10(np.abs(mag) + 1e-12) - NEARFIELD_OFFSET

result = check_compliance(
    (freq, mag_db),
    fcc_mask,
    detector="peak"
)

print(f"Near-field scan (with {NEARFIELD_OFFSET} dB offset): {result.status}")
print(f"Margin to limit: {result.margin_to_limit:+.1f} dB")

if result.margin_to_limit < 10:
    print(f"\n⚠ Warning: Margin < 10 dB")
    print(f"   Recommend formal testing to verify compliance")
    print(f"   Consider design improvements before proceeding")
else:
    print(f"\n✓ Good margin - likely to pass formal testing")

# Identify problem frequencies
from tracekit.analyzers.spectral import find_spectral_peaks

peaks = find_spectral_peaks(
    trace,
    min_height_db=-20,
    min_distance_hz=1e6,
    threshold_db=10
)

print(f"\nIdentified emission peaks:")
for peak in peaks[:10]:  # Top 10
    print(f"  {peak.frequency / 1e6:7.3f} MHz: {peak.magnitude_db:5.1f} dB")

# Suggest improvements
print("\nDesign iteration recommendations:")
if any(p.frequency > 100e6 for p in peaks):
    print("  - High frequency emissions present")
    print("    → Check cable shielding and connectors")
    print("    → Verify PCB ground planes")
if any(p.frequency < 50e6 for p in peaks):
    print("  - Low frequency emissions present")
    print("    → Check power supply filtering")
    print("    → Verify switching frequency and harmonics")
```

### 7.2 Issue Debugging Workflow

```python
import tracekit as tk
from tracekit.compliance import check_compliance, load_limit_mask
from tracekit.analyzers.spectral import fft, find_spectral_peaks
import numpy as np
import matplotlib.pyplot as plt

# Iterative debugging workflow
iterations = [
    ("Baseline", "prototype_v1_emissions.wfm"),
    ("Added ferrites", "prototype_v2_ferrites.wfm"),
    ("Improved grounding", "prototype_v3_grounding.wfm"),
    ("Final design", "prototype_v4_final.wfm"),
]

mask = load_limit_mask("FCC_Part15_ClassB")

print("Pre-Compliance Design Iteration")
print("="*60)

margins = []
results = {}

for iteration, filename in iterations:
    trace = tk.load(filename)
    result = check_compliance(trace, mask, detector="peak")
    results[iteration] = result
    margins.append(result.margin_to_limit)

    status = "✓ PASS" if result.passed else "✗ FAIL"
    print(f"{iteration:20s}: {status} (margin: {result.margin_to_limit:+6.1f} dB)")

# Plot improvement over iterations
plt.figure(figsize=(12, 8))

# Plot all iterations
for (iteration, _), result in zip(iterations, results.values()):
    plt.semilogx(result.spectrum_freq / 1e6, result.spectrum_level,
                 linewidth=1.5, label=iteration, alpha=0.8)

# Plot limit
plt.semilogx(result.spectrum_freq / 1e6, result.limit_level,
             'r--', linewidth=2.5, label='FCC Limit')

plt.xlabel('Frequency (MHz)')
plt.ylabel('Emission Level (dBµV/m)')
plt.title('EMC Pre-Compliance Design Iterations')
plt.grid(True, which='both', alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('design_iteration_progress.png', dpi=150)
plt.show()

# Show margin improvement
plt.figure(figsize=(10, 6))
plt.plot(range(len(margins)), margins, 'o-', linewidth=2, markersize=10)
plt.axhline(y=0, color='r', linestyle='--', label='Compliance Threshold')
plt.axhline(y=6, color='orange', linestyle=':', label='6 dB Margin Goal')
plt.xticks(range(len(margins)), [it[0] for it in iterations], rotation=15)
plt.ylabel('Margin to Limit (dB)')
plt.title('EMC Margin Improvement Through Design Iterations')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('margin_improvement.png', dpi=150)
plt.show()

print(f"\nMargin improvement: {margins[-1] - margins[0]:+.1f} dB")
print(f"Status changed: {iterations[0][0]} → {iterations[-1][0]}")

if margins[-1] >= 6:
    print("\n✓ Ready for formal compliance testing")
else:
    print(f"\n⚠ Margin still < 6 dB - recommend further improvements")
```

### 7.3 Clock Harmonic Analysis

```python
import tracekit as tk
from tracekit.analyzers.spectral import fft, find_spectral_peaks
import numpy as np
import matplotlib.pyplot as plt

# Analyze clock harmonics - common emission source
trace = tk.load("emissions_scan.wfm")

# Find fundamental clock frequency
peaks = find_spectral_peaks(trace, min_height_db=-40)

# Sort by magnitude
peaks_sorted = sorted(peaks, key=lambda p: p.magnitude_db, reverse=True)

print("Clock Harmonic Analysis")
print("="*60)

# Estimate fundamental frequency
# Often the strongest peak below 100 MHz is the clock or its first harmonic
fundamental_candidates = [p for p in peaks_sorted if p.frequency < 100e6]

if fundamental_candidates:
    fundamental = fundamental_candidates[0].frequency
    print(f"Estimated clock fundamental: {fundamental / 1e6:.3f} MHz")

    # Find harmonics
    print(f"\nHarmonics found:")
    print(f"{'Harmonic':<10s} {'Frequency (MHz)':<20s} {'Level (dBµV/m)':<15s} {'Note'}")
    print("-"*70)

    for i, peak in enumerate(peaks_sorted[:20], 1):
        # Check if peak is a harmonic (within 5% tolerance)
        harmonic_num = round(peak.frequency / fundamental)
        expected_freq = harmonic_num * fundamental
        error = abs(peak.frequency - expected_freq) / expected_freq

        if error < 0.05 and harmonic_num <= 50:  # Within 5%
            note = f"✓ {harmonic_num}th harmonic"
            if harmonic_num % 2 == 0:
                note += " (even - should be suppressed)"
        else:
            note = "Other emission"

        print(f"  {i:<8d} {peak.frequency / 1e6:>8.3f}  "
              f"{peak.magnitude_db:>15.1f}  {note}")

    # Check critical harmonics in sensitive bands
    fm_band = (88e6, 108e6)
    critical_harmonics = []

    for n in range(1, 100):
        harm_freq = n * fundamental
        if fm_band[0] <= harm_freq <= fm_band[1]:
            critical_harmonics.append((n, harm_freq))

    if critical_harmonics:
        print(f"\n⚠ Critical harmonics in FM broadcast band (88-108 MHz):")
        for n, freq in critical_harmonics:
            print(f"   {n}th harmonic at {freq / 1e6:.3f} MHz")
        print(f"   Recommendation: Consider changing clock frequency")

        # Suggest alternative clock frequencies
        # Find clock frequencies that avoid FM band
        print(f"\n   Alternative clock frequencies to avoid FM band:")
        for test_freq in np.arange(20e6, 50e6, 1e6):
            has_conflict = False
            for n in range(1, 10):
                if fm_band[0] <= n * test_freq <= fm_band[1]:
                    has_conflict = True
                    break
            if not has_conflict:
                print(f"     {test_freq / 1e6:.1f} MHz")

else:
    print("Could not identify fundamental clock frequency")

# Plot spectrum with harmonics marked
freq, mag = fft(trace)
mag_db = 20 * np.log10(np.abs(mag) + 1e-12)

plt.figure(figsize=(14, 6))
plt.semilogx(freq / 1e6, mag_db, 'b-', linewidth=1, alpha=0.7)

# Mark harmonics
if fundamental_candidates:
    for n in range(1, 20):
        harm_freq = n * fundamental
        if harm_freq < np.max(freq):
            plt.axvline(x=harm_freq / 1e6, color='r', linestyle='--',
                        alpha=0.3, linewidth=1)
            plt.text(harm_freq / 1e6, np.max(mag_db) - 5, f'{n}',
                     fontsize=8, ha='center')

# Mark sensitive bands
plt.axvspan(88, 108, alpha=0.2, color='yellow', label='FM Band (88-108 MHz)')
plt.axvspan(0.535, 1.705, alpha=0.2, color='orange', label='AM Band')

plt.xlabel('Frequency (MHz)')
plt.ylabel('Level (dBµV/m)')
plt.title('Spectrum with Clock Harmonics Identified')
plt.grid(True, which='both', alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('clock_harmonic_analysis.png', dpi=150)
plt.show()
```

## 8. Report Generation and Documentation

### 8.1 Comprehensive Test Report

```python
import tracekit as tk
from tracekit.compliance import (
    load_limit_mask, check_compliance,
    generate_compliance_report, ComplianceReportFormat
)
from datetime import datetime

# Complete test report for regulatory submission

# Device information
dut_info = {
    "Manufacturer": "Example Electronics Inc.",
    "Product Name": "Wireless IoT Gateway",
    "Model Number": "WIG-2000",
    "FCC ID": "ABC-WIG2000",
    "Hardware Version": "Rev B",
    "Firmware Version": "v2.1.4",
    "Serial Number": "TEST-001",

    # Test information
    "Test Standard": "FCC Part 15 Subpart B, Class B",
    "Test Method": "ANSI C63.4-2014",
    "Test Date": "2026-01-08",
    "Test Engineer": "John Smith, EMC Engineer",
    "Reviewed By": "Jane Doe, Senior Engineer",

    # Test facility
    "Test Lab": "EMC Test Laboratory Inc.",
    "Lab Accreditation": "FCC Registration Number: 123456",
    "Lab Address": "123 Test Street, City, ST 12345",

    # Test environment
    "Chamber": "10m Semi-Anechoic Chamber (SAC-10)",
    "Ambient Temperature": "23°C ± 2°C",
    "Relative Humidity": "45% ± 5%",
    "Chamber Validation": "Site attenuation per ANSI C63.4 Annex C",

    # Test equipment
    "Spectrum Analyzer": "Keysight N9020B MXA",
    "Antenna - Biconical": "EMCO 3104B (30-300 MHz)",
    "Antenna - Log Periodic": "EMCO 3146 (200-2000 MHz)",
    "LISN": "Rohde & Schwarz ENV216",
    "Cable Calibration": "Performed 2026-01-06",

    # DUT configuration
    "Operating Mode": "Normal operation with WiFi and Ethernet active",
    "Supply Voltage": "12V DC nominal (± 10% tested)",
    "Load Condition": "Maximum operating load",
    "Connected Cables": "Ethernet (1.5m), USB (0.5m), Power (2m)",

    # Additional notes
    "Notes": "All measurements performed with device in worst-case configuration",
}

# Radiated emissions test
print("Generating comprehensive EMC compliance report...")

trace_radiated = tk.load("radiated_emissions_final.wfm")
mask_radiated = load_limit_mask("FCC_Part15_ClassB")

result_radiated = check_compliance(
    trace_radiated,
    mask_radiated,
    detector="quasi-peak",
    frequency_range=(30e6, 1000e6),
    unit_conversion="V_to_dBuV"
)

# Generate HTML report
report_path = generate_compliance_report(
    result_radiated,
    "FCC_Part15_Radiated_Emissions_Report.html",
    format=ComplianceReportFormat.HTML,
    include_plot=True,
    title="FCC Part 15 Class B Radiated Emissions Compliance Test Report",
    company_name="Example Electronics Inc.",
    dut_info=dut_info
)

print(f"✓ Report generated: {report_path}")

# Generate PDF for submission
pdf_path = generate_compliance_report(
    result_radiated,
    "FCC_Part15_Radiated_Emissions_Report.pdf",
    format=ComplianceReportFormat.PDF,
    include_plot=True,
    title="FCC Part 15 Class B Radiated Emissions Compliance Test Report",
    company_name="Example Electronics Inc.",
    dut_info=dut_info
)

print(f"✓ PDF report generated: {pdf_path}")

# Generate JSON data for records
json_path = generate_compliance_report(
    result_radiated,
    "FCC_Part15_Radiated_Emissions_Data.json",
    format=ComplianceReportFormat.JSON,
    title="FCC Part 15 Class B Radiated Emissions Test Data",
    dut_info=dut_info
)

print(f"✓ JSON data exported: {json_path}")

print("\n" + "="*60)
print("EMC COMPLIANCE REPORT SUMMARY")
print("="*60)
print(f"DUT: {dut_info['Product Name']} ({dut_info['Model Number']})")
print(f"Standard: {dut_info['Test Standard']}")
print(f"Test Date: {dut_info['Test Date']}")
print(f"Result: {result_radiated.status}")
print(f"Margin: {result_radiated.margin_to_limit:+.1f} dB")

if result_radiated.passed:
    print("\n✓ Device complies with FCC Part 15 Class B requirements")
else:
    print(f"\n✗ Device FAILS - {result_radiated.violation_count} violations")
```

### 8.2 Multi-Test Summary Report

```python
import tracekit as tk
from tracekit.compliance import load_limit_mask, check_compliance
import json
from pathlib import Path

# Generate summary report for all tests performed

test_suite = {
    "Conducted Emissions - Line 1": {
        "file": "conducted_line1.wfm",
        "mask": "FCC_Part15_ClassB_Conducted",
        "detector": "quasi-peak",
    },
    "Conducted Emissions - Line 2": {
        "file": "conducted_line2.wfm",
        "mask": "FCC_Part15_ClassB_Conducted",
        "detector": "quasi-peak",
    },
    "Radiated Emissions - Horizontal": {
        "file": "radiated_horizontal.wfm",
        "mask": "FCC_Part15_ClassB",
        "detector": "quasi-peak",
    },
    "Radiated Emissions - Vertical": {
        "file": "radiated_vertical.wfm",
        "mask": "FCC_Part15_ClassB",
        "detector": "quasi-peak",
    },
}

# Run all tests
results_summary = []

print("="*70)
print("FCC PART 15 CLASS B COMPLIANCE TEST SUITE")
print("="*70)
print()

for test_name, test_config in test_suite.items():
    trace = tk.load(test_config["file"])
    mask = load_limit_mask(test_config["mask"])

    result = check_compliance(
        trace,
        mask,
        detector=test_config["detector"]
    )

    results_summary.append({
        "test": test_name,
        "status": result.status,
        "passed": result.passed,
        "margin_db": result.margin_to_limit,
        "violations": result.violation_count,
        "worst_freq_mhz": result.worst_frequency / 1e6,
    })

    status_symbol = "✓" if result.passed else "✗"
    print(f"{status_symbol} {test_name:40s}: {result.status:4s} "
          f"(margin: {result.margin_to_limit:+6.1f} dB)")

# Overall determination
overall_pass = all(r["passed"] for r in results_summary)

print()
print("="*70)
print(f"OVERALL RESULT: {'PASS' if overall_pass else 'FAIL'}")
print("="*70)

if overall_pass:
    min_margin = min(r["margin_db"] for r in results_summary)
    print(f"\n✓ All tests passed")
    print(f"  Minimum margin across all tests: {min_margin:.1f} dB")
    print(f"\n  Device complies with FCC Part 15 Class B requirements")
else:
    failed_tests = [r for r in results_summary if not r["passed"]]
    print(f"\n✗ {len(failed_tests)} test(s) failed:")
    for r in failed_tests:
        print(f"  - {r['test']}: {r['violations']} violations, "
              f"worst at {r['worst_freq_mhz']:.3f} MHz")

# Export summary to JSON
summary_data = {
    "test_date": "2026-01-08",
    "standard": "FCC Part 15 Class B",
    "overall_result": "PASS" if overall_pass else "FAIL",
    "tests": results_summary,
}

with open("test_summary.json", "w") as f:
    json.dump(summary_data, f, indent=2)

print(f"\nTest summary exported to: test_summary.json")
```

### 8.3 Compliance Checklists

#### Pre-Test Checklist

```
EMC COMPLIANCE TEST - PRE-TEST CHECKLIST
========================================

Date: ________________    Engineer: ________________

□ DUT Configuration
  □ DUT fully assembled and functional
  □ Firmware version documented: __________
  □ Serial number recorded: __________
  □ Operating mode configured: __________
  □ All cables connected per normal use
  □ Power supply: nominal voltage verified

□ Test Equipment
  □ Spectrum analyzer calibrated (date: ______)
  □ Antennas calibrated (date: ______)
  □ Cables calibrated (date: ______)
  □ LISN verified operational
  □ All connections secure and proper impedance

□ Test Environment
  □ Chamber ambient noise floor checked
  □ Temperature in range: 20-30°C
  □ Humidity in range: 40-60%
  □ Site attenuation verification current
  □ Safety procedures reviewed

□ Documentation
  □ Test plan reviewed
  □ DUT information sheet completed
  □ Photo documentation prepared
  □ Data logging configured

□ Software/Analysis
  □ TraceKit installed and tested
  □ Limit masks verified
  □ Report templates prepared
  □ Data backup configured

Engineer Signature: ________________  Date: ________
```

#### Post-Test Checklist

```
EMC COMPLIANCE TEST - POST-TEST CHECKLIST
=========================================

Date: ________________    Engineer: ________________

□ Test Execution
  □ All test procedures completed
  □ Data files saved and backed up
  □ Photos/videos captured
  □ DUT condition verified after test
  □ Anomalies documented

□ Data Analysis
  □ All measurements analyzed with TraceKit
  □ Compliance status determined
  □ Margins calculated
  □ Violations identified (if any)

□ Reporting
  □ Test report generated
  □ Plots and graphs included
  □ DUT information complete
  □ Test equipment list complete
  □ Pass/fail determination clear

□ Follow-up Actions
  □ If FAIL: Issues documented
  □ If FAIL: Corrective actions identified
  □ If PASS: Report ready for submission
  □ Data archived appropriately

Engineer Signature: ________________  Date: ________
Reviewer Signature: ________________  Date: ________
```

## Best Practices and Tips

### Measurement Settings

**Resolution Bandwidth (RBW):**

- CISPR standards: 9 kHz (150 kHz - 30 MHz), 120 kHz (30 MHz - 1 GHz)
- Smaller RBW = better frequency resolution but longer sweep time
- Use appropriate RBW per standard

**Detector Types:**

- **Peak**: Fast, conservative, use for initial scans
- **Quasi-peak**: Required for CISPR, weights by repetition rate
- **Average**: Some conducted tests, good for comparison

**Sweep Time:**

- Must be sufficient for detector settling
- CISPR quasi-peak: typically 1-2 seconds per point
- Use "auto" setting if available

### Common Pitfalls

1. **Ambient Noise**: Always verify chamber ambient noise is at least 6 dB below limit
2. **Cable Routing**: Keep test cables > 40 cm from chamber walls
3. **Turntable Position**: Ensure DUT centered on turntable
4. **Antenna Polarization**: Test both horizontal and vertical
5. **Distance**: Verify measurement distance matches limit mask

### Cost-Saving Tips

**Pre-compliance testing:**

- Use near-field probes for desktop debugging
- Fix obvious issues before formal testing
- Iterate design in-house

**Optimize formal testing:**

- Come prepared with well-tested design
- Have backup units ready
- Schedule follow-up testing if needed

**Automated testing:**

```python
# Use TraceKit to automate repetitive analysis
import tracekit as tk
from tracekit.compliance import check_compliance, load_limit_mask

# Batch process multiple test files
import glob

mask = load_limit_mask("FCC_Part15_ClassB")

for filename in glob.glob("test_data/*.wfm"):
    trace = tk.load(filename)
    result = check_compliance(trace, mask)
    print(f"{filename}: {result.status} ({result.margin_to_limit:+.1f} dB)")
```

## Troubleshooting

### High Emissions Issues

**Radiated emissions too high:**

1. Check cable routing and shielding
2. Add ferrite beads on cables
3. Improve PCB ground plane
4. Add shielding to enclosure
5. Reduce clock frequency or use spread-spectrum clocking

**Conducted emissions too high:**

1. Improve power supply filtering
2. Add common-mode chokes
3. Check switching frequencies
4. Add X2Y or feedthrough capacitors
5. Improve PCB layout (power/ground planes)

### Immunity Test Failures

**ESD failures:**

1. Improve grounding
2. Add transient protection diodes
3. Increase trace spacing
4. Add shielding to sensitive circuits

**RF immunity failures:**

1. Add filtering on cables/connectors
2. Improve shielding
3. Reduce antenna effects (cable length resonances)
4. Add RF bypass capacitors

## See Also

- [EMC Compliance API Reference](../api/emc-compliance.md) - Complete API documentation
- [Standards Compliance](../reference/standards-compliance.md) - IEEE/IEC standards
- [Best Practices](best-practices.md) - General TraceKit best practices
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

## References

### Standards Documents

- **FCC Part 15** - Code of Federal Regulations Title 47 Part 15
- **ANSI C63.4-2014** - American National Standard for Methods of Measurement of Radio-Noise Emissions
- **CISPR 16-1-1** - Specification for radio disturbance and immunity measuring apparatus
- **CISPR 22** - Information technology equipment - Radio disturbance characteristics
- **CISPR 25:2021** - Vehicles, boats and internal combustion engines - Radio disturbance characteristics
- **CISPR 32** - Electromagnetic compatibility of multimedia equipment - Emission requirements
- **IEC 61000-4-2** - Electrostatic discharge immunity test
- **IEC 61000-4-3** - Radiated RF electromagnetic field immunity test
- **IEC 61000-4-4** - Electrical fast transient/burst immunity test
- **IEC 61000-4-5** - Surge immunity test
- **IEC 61000-4-6** - Immunity to conducted disturbances, induced by RF fields
- **ISO 11452-4** - Road vehicles - Component test methods for electrical disturbances - Bulk current injection
- **MIL-STD-461G** - Requirements for the control of electromagnetic interference characteristics

### Online Resources

- FCC Equipment Authorization: https://www.fcc.gov/oet/ea
- CISPR Standards: https://www.iec.ch/
- ANSI Standards: https://www.ansi.org/
- EMC Testing Equipment: https://www.emcompliance.com/
