# Component Analysis Guide

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

Practical guide to component characterization and validation using Time Domain Reflectometry (TDR) and waveform analysis with TraceKit.

## Overview

This guide covers comprehensive component analysis techniques including:

- **TDR measurements** - Impedance profiling and discontinuity detection
- **Passive components** - Capacitor, inductor, and resistor characterization
- **Transmission lines** - PCB trace impedance and propagation delay
- **Connectors and cables** - Quality validation and testing
- **Parasitic extraction** - ESR, ESL, and self-resonant frequency
- **Signal integrity** - Crosstalk, differential impedance, and quality metrics

## Table of Contents

1. [Introduction to Component Characterization](#introduction)
2. [TDR Basics](#tdr-basics)
3. [Step-by-Step Tutorials](#tutorials)
4. [Advanced Techniques](#advanced-techniques)
5. [Real-World Applications](#real-world-applications)
6. [Troubleshooting](#troubleshooting)

---

## Introduction

### What is Component Characterization?

Component characterization is the process of measuring and validating the electrical properties of circuit elements, transmission lines, and interconnects. TraceKit provides tools for:

- **DC measurements** - Resistance, voltage, current
- **AC measurements** - Impedance, reactance, phase
- **TDR analysis** - Characteristic impedance, discontinuities
- **Parasitic extraction** - ESR, ESL, parasitic capacitance/inductance
- **Quality metrics** - Signal integrity, return loss, insertion loss

### When to Use This Guide

Use component analysis when you need to:

- Validate PCB trace impedance (50Ω, 75Ω, 100Ω differential)
- Characterize connectors and cables
- Measure capacitor ESR and self-resonant frequency
- Extract inductor parameters (L, DCR, Q-factor)
- Detect transmission line discontinuities
- Verify high-speed signal integrity

### Prerequisites

Basic understanding of:

- Oscilloscope operation and TDR mode
- Transmission line theory
- Circuit component behavior
- Signal integrity concepts

---

## TDR Basics

### What is Time Domain Reflectometry?

Time Domain Reflectometry (TDR) is a measurement technique that sends a fast step pulse down a transmission line and analyzes the reflections to determine:

- Characteristic impedance (Z₀)
- Impedance discontinuities
- Cable faults and breaks
- Propagation delay and velocity factor
- Connector quality

### TDR Theory

When a signal encounters an impedance discontinuity, part of the signal reflects back to the source. The reflection coefficient (ρ) is:

```
ρ = (Z₂ - Z₁) / (Z₂ + Z₁)
```

Where:

- Z₁ = Source impedance
- Z₂ = Load or discontinuity impedance

From the reflection coefficient, we can extract impedance:

```
Z = Z₀ × (1 + ρ) / (1 - ρ)
```

### Setting Up TDR Measurements

**Equipment needed:**

- Oscilloscope with TDR mode or fast step generator
- TDR probe or SMA cable
- Calibration standards (50Ω load, open, short)
- Device under test (DUT)

**Basic setup:**

1. Connect TDR source to oscilloscope
2. Set source impedance (typically 50Ω)
3. Calibrate with known standards
4. Connect device under test
5. Capture TDR waveform
6. Analyze with TraceKit

### Loading TDR Data

```python
import tracekit as tk

# Load TDR waveform from oscilloscope
tdr_trace = tk.load("tdr_capture.wfm")

# Check trace properties
print(f"Sample rate: {tdr_trace.metadata.sample_rate / 1e9:.2f} GS/s")
print(f"Record length: {len(tdr_trace.data)} samples")
print(f"Duration: {len(tdr_trace.data) / tdr_trace.metadata.sample_rate * 1e9:.2f} ns")
```

---

## Tutorials

### Tutorial 1: PCB Trace Impedance Measurement

**Goal:** Measure the characteristic impedance of a 50Ω microstrip trace on FR4.

#### Step 1: Capture TDR Waveform

Set up your oscilloscope in TDR mode with:

- Source impedance: 50Ω
- Rise time: < 100ps (for best resolution)
- Timebase: Adjust to show trace length
- Open-ended trace (no termination)

```python
import tracekit as tk
from tracekit.component import extract_impedance, characteristic_impedance

# Load TDR capture
tdr_trace = tk.load("pcb_trace_tdr.wfm")

# Quick impedance check
z0 = characteristic_impedance(tdr_trace, z0_source=50.0)
print(f"Characteristic impedance: {z0:.2f} Ω")
```

#### Step 2: Extract Full Impedance Profile

```python
from tracekit.component import extract_impedance

# Extract impedance profile
z0, profile = extract_impedance(
    tdr_trace,
    z0_source=50.0,           # Source impedance
    velocity_factor=0.66,      # FR4 typical value
    start_time=5e-9,          # Start after incident edge (5ns)
    end_time=20e-9            # End before open reflection (20ns)
)

# Display results
print(f"\n=== PCB Trace Impedance ===")
print(f"Characteristic impedance: {z0:.2f} Ω")
print(f"Mean impedance: {profile.mean_impedance:.2f} Ω")
print(f"Impedance range: {profile.min_impedance:.2f} - {profile.max_impedance:.2f} Ω")
print(f"Standard deviation: {profile.statistics['z0_std']:.2f} Ω")

# Check tolerance (±10% for typical PCB)
tolerance = 0.10
if abs(z0 - 50.0) / 50.0 <= tolerance:
    print(f"✓ Within {tolerance*100:.0f}% tolerance")
else:
    print(f"✗ Outside {tolerance*100:.0f}% tolerance")
```

#### Step 3: Visualize Impedance Profile

```python
import matplotlib.pyplot as plt

# Plot impedance vs. distance
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Impedance vs. distance
ax1.plot(profile.distance * 1000, profile.impedance, 'b-', linewidth=1)
ax1.axhline(y=50, color='r', linestyle='--', label='Target 50Ω')
ax1.axhline(y=55, color='orange', linestyle=':', alpha=0.5, label='±10% tolerance')
ax1.axhline(y=45, color='orange', linestyle=':', alpha=0.5)
ax1.set_xlabel('Distance (mm)')
ax1.set_ylabel('Impedance (Ω)')
ax1.set_title('PCB Trace Impedance Profile')
ax1.grid(True, alpha=0.3)
ax1.legend()
ax1.set_ylim([40, 60])

# Impedance vs. time
ax2.plot(profile.time * 1e9, profile.impedance, 'b-', linewidth=1)
ax2.axhline(y=50, color='r', linestyle='--')
ax2.set_xlabel('Time (ns)')
ax2.set_ylabel('Impedance (Ω)')
ax2.set_title('TDR Time Domain Response')
ax2.grid(True, alpha=0.3)
ax2.set_ylim([40, 60])

plt.tight_layout()
plt.savefig('pcb_trace_impedance.png', dpi=300)
plt.show()
```

**Expected Results:**

- Well-controlled trace: Z₀ = 48-52Ω, ±2Ω variation
- Manufacturing variation: Z₀ = 45-55Ω, up to ±5Ω
- Poor control: Z₀ outside ±10% or high variation

---

### Tutorial 2: Connector Characterization

**Goal:** Characterize an SMA connector for impedance match and discontinuities.

#### Step 1: Measure Connector Impedance

```python
import tracekit as tk
from tracekit.component import discontinuity_analysis, extract_impedance

# Load TDR data (cable + connector + cable)
connector_tdr = tk.load("sma_connector_tdr.wfm")

# Extract impedance profile
z0, profile = extract_impedance(
    connector_tdr,
    z0_source=50.0,
    velocity_factor=0.66
)

print(f"\n=== SMA Connector Analysis ===")
print(f"Average impedance: {z0:.2f} Ω")
```

#### Step 2: Detect Discontinuities

```python
# Analyze discontinuities
discontinuities = discontinuity_analysis(
    connector_tdr,
    z0_source=50.0,
    velocity_factor=0.66,
    threshold=2.0,              # Detect impedance changes > 2Ω
    min_separation=100e-12      # Minimum 100ps between discontinuities
)

print(f"\nDetected {len(discontinuities)} discontinuities:")
print("\nPosition | Impedance Change | Type | Reflection Coeff")
print("-" * 65)

for disc in discontinuities:
    print(f"{disc.position*1000:6.2f}mm | "
          f"{disc.impedance_before:5.1f}Ω → {disc.impedance_after:5.1f}Ω | "
          f"{disc.discontinuity_type:11s} | "
          f"ρ = {disc.reflection_coeff:+.4f}")
```

#### Step 3: Calculate Return Loss

```python
import numpy as np

# Calculate return loss for each discontinuity
print("\n=== Return Loss Analysis ===")

for i, disc in enumerate(discontinuities, 1):
    # Return loss (dB) = -20 × log₁₀(|ρ|)
    if abs(disc.reflection_coeff) > 1e-6:
        return_loss = -20 * np.log10(abs(disc.reflection_coeff))
        print(f"Discontinuity {i}: {return_loss:.1f} dB")

        # Quality assessment
        if return_loss > 30:
            quality = "Excellent"
        elif return_loss > 20:
            quality = "Good"
        elif return_loss > 15:
            quality = "Acceptable"
        else:
            quality = "Poor"

        print(f"  Quality: {quality}")
    else:
        print(f"Discontinuity {i}: >40 dB (excellent match)")
```

**Connector Quality Metrics:**

| Return Loss | Quality    | Typical Use Case        |
| ----------- | ---------- | ----------------------- |
| > 30 dB     | Excellent  | RF, high-speed digital  |
| 20-30 dB    | Good       | General high-speed      |
| 15-20 dB    | Acceptable | Standard digital        |
| < 15 dB     | Poor       | May cause signal issues |

---

### Tutorial 3: Cable Testing and Qualification

**Goal:** Test a coaxial cable for impedance, loss, and faults.

#### Step 1: Baseline Cable Characterization

```python
import tracekit as tk
from tracekit.component import transmission_line_analysis

# Load TDR measurement of cable
cable_tdr = tk.load("coax_cable_tdr.wfm")

# Analyze transmission line parameters
result = transmission_line_analysis(
    cable_tdr,
    z0_source=50.0,
    line_length=2.0,  # Known cable length: 2 meters
)

print(f"\n=== Cable Characterization ===")
print(f"Characteristic impedance: {result.z0:.2f} Ω")
print(f"Propagation delay: {result.propagation_delay * 1e9:.2f} ns")
print(f"Velocity factor: {result.velocity_factor:.3f}")
print(f"Propagation velocity: {result.velocity / 1e8:.2f} × 10⁸ m/s")
print(f"Estimated length: {result.length:.3f} m")

if result.loss is not None:
    print(f"Estimated loss: {result.loss:.2f} dB")
if result.return_loss is not None:
    print(f"Return loss: {result.return_loss:.2f} dB")
```

#### Step 2: Verify Velocity Factor

```python
from tracekit.component import velocity_factor

# Calculate velocity factor from known length
measured_vf = velocity_factor(cable_tdr, line_length=2.0)

print(f"\n=== Velocity Factor Verification ===")
print(f"Measured velocity factor: {measured_vf:.3f}")

# Common cable types
cable_types = {
    "RG-58": 0.66,
    "RG-174": 0.66,
    "RG-213": 0.66,
    "LMR-400": 0.85,
    "Precision coax": 0.70
}

print("\nComparison with standard cables:")
for cable_name, vf in cable_types.items():
    error = abs(measured_vf - vf) / vf * 100
    if error < 5:
        print(f"  {cable_name:15s}: {vf:.3f} (✓ match within 5%)")
```

#### Step 3: Detect Cable Faults

```python
from tracekit.component import discontinuity_analysis

# Look for faults (crimps, breaks, water ingress)
faults = discontinuity_analysis(
    cable_tdr,
    z0_source=50.0,
    velocity_factor=measured_vf,
    threshold=5.0,      # Higher threshold for fault detection
    min_separation=1e-9  # 1ns minimum separation
)

print(f"\n=== Fault Detection ===")
if len(faults) == 0:
    print("No faults detected. Cable is good.")
else:
    print(f"Found {len(faults)} potential fault(s):")

    for i, fault in enumerate(faults, 1):
        print(f"\nFault {i}:")
        print(f"  Location: {fault.position:.3f} m ({fault.position/result.length*100:.1f}% of cable)")
        print(f"  Impedance change: {fault.impedance_before:.1f}Ω → {fault.impedance_after:.1f}Ω")
        print(f"  Magnitude: {fault.magnitude:+.1f}Ω")

        # Fault type interpretation
        if fault.discontinuity_type == "capacitive":
            print(f"  Type: {fault.discontinuity_type} (possible crimp/pinch)")
        elif fault.discontinuity_type == "inductive":
            print(f"  Type: {fault.discontinuity_type} (possible break/gap)")
        else:
            print(f"  Type: {fault.discontinuity_type}")
```

---

### Tutorial 4: Capacitor ESR Measurement

**Goal:** Measure capacitor Equivalent Series Resistance (ESR) from step response.

#### Step 1: Generate Step Response

Set up a simple RC circuit with known resistor and capture the charging waveform:

```python
import tracekit as tk
from tracekit.component import measure_capacitance

# Load voltage waveform across capacitor
# Load current waveform through capacitor
voltage_trace = tk.load("capacitor_voltage.wfm")
current_trace = tk.load("capacitor_current.wfm")

# Measure capacitance using charge integration method
cap_result = measure_capacitance(
    voltage_trace,
    current_trace,
    method="charge"
)

print(f"\n=== Capacitor Characterization ===")
print(f"Capacitance: {cap_result.capacitance * 1e6:.2f} µF")
print(f"ESR: {cap_result.esr:.3f} Ω")
print(f"Measurement method: {cap_result.method}")
print(f"Confidence: {cap_result.confidence * 100:.1f}%")

# Additional statistics
stats = cap_result.statistics
print(f"\nMeasurement details:")
print(f"  Voltage change: {stats['delta_v']:.3f} V")
print(f"  Charge transferred: {stats['delta_q'] * 1e6:.2f} µC")
print(f"  Sample count: {stats['num_samples']}")
```

#### Step 2: Alternative Slope Method

```python
# Measure using slope method (I = C × dV/dt)
cap_slope = measure_capacitance(
    voltage_trace,
    current_trace,
    method="slope"
)

print(f"\n=== Slope Method Comparison ===")
print(f"Capacitance: {cap_slope.capacitance * 1e6:.2f} µF")
print(f"Confidence: {cap_slope.confidence * 100:.1f}%")
print(f"Standard deviation: {cap_slope.statistics['capacitance_std'] * 1e6:.3f} µF")

# Compare methods
diff = abs(cap_result.capacitance - cap_slope.capacitance)
diff_pct = diff / cap_result.capacitance * 100
print(f"\nMethod agreement: {diff_pct:.1f}% difference")
```

#### Step 3: Frequency-Dependent ESR

```python
import numpy as np
from scipy.fft import fft, fftfreq

# Analyze ESR vs. frequency from impedance sweep
voltage = voltage_trace.data
current = current_trace.data
sample_rate = voltage_trace.metadata.sample_rate

# Compute impedance spectrum
V_fft = fft(voltage)
I_fft = fft(current)
freqs = fftfreq(len(voltage), 1/sample_rate)

# Calculate impedance Z = V / I
Z = V_fft / (I_fft + 1e-20)
ESR_spectrum = np.real(Z)

# Plot ESR vs. frequency
import matplotlib.pyplot as plt

pos_freqs = freqs[:len(freqs)//2]
pos_esr = ESR_spectrum[:len(freqs)//2]

plt.figure(figsize=(10, 6))
plt.semilogx(pos_freqs[1:], pos_esr[1:], 'b-', linewidth=2)
plt.xlabel('Frequency (Hz)')
plt.ylabel('ESR (Ω)')
plt.title('Capacitor ESR vs. Frequency')
plt.grid(True, which='both', alpha=0.3)
plt.savefig('capacitor_esr_frequency.png', dpi=300)
plt.show()
```

**ESR Quality Guidelines:**

| Capacitor Type | ESR @ 100kHz | Quality               |
| -------------- | ------------ | --------------------- |
| Ceramic        | < 10 mΩ      | Excellent             |
| Polymer        | 10-50 mΩ     | Good                  |
| Electrolytic   | 50-500 mΩ    | Typical               |
| Tantalum       | 100-1000 mΩ  | Application dependent |

---

### Tutorial 5: Inductor Characterization

**Goal:** Measure inductance, DCR, and Q-factor of an inductor.

#### Step 1: Measure Inductance

```python
import tracekit as tk
from tracekit.component import measure_inductance

# Load voltage across inductor and current through it
voltage_trace = tk.load("inductor_voltage.wfm")
current_trace = tk.load("inductor_current.wfm")

# Measure using flux integration (V = L × dI/dt)
ind_result = measure_inductance(
    voltage_trace,
    current_trace,
    method="flux"
)

print(f"\n=== Inductor Characterization ===")
print(f"Inductance: {ind_result.inductance * 1e6:.2f} µH")
print(f"DC Resistance (DCR): {ind_result.dcr:.3f} Ω")
print(f"Measurement method: {ind_result.method}")
print(f"Confidence: {ind_result.confidence * 100:.1f}%")

# Measurement statistics
stats = ind_result.statistics
print(f"\nMeasurement details:")
print(f"  Current change: {stats['delta_i'] * 1e3:.2f} mA")
print(f"  Flux linkage: {stats['delta_flux'] * 1e6:.2f} µWb")
```

#### Step 2: Calculate Q-Factor

```python
import numpy as np
from scipy.fft import fft, fftfreq

# Calculate Q-factor from impedance spectrum
voltage = voltage_trace.data
current = current_trace.data
sample_rate = voltage_trace.metadata.sample_rate

# FFT analysis
V_fft = fft(voltage)
I_fft = fft(current)
freqs = fftfreq(len(voltage), 1/sample_rate)

# Impedance
Z = V_fft / (I_fft + 1e-20)

# Find resonant frequency (maximum impedance)
pos_idx = freqs > 0
pos_freqs = freqs[pos_idx]
pos_Z = np.abs(Z[pos_idx])

resonant_idx = np.argmax(pos_Z)
resonant_freq = pos_freqs[resonant_idx]

# Q-factor = X_L / R = (2πfL) / R
omega = 2 * np.pi * resonant_freq
X_L = omega * ind_result.inductance
Q_factor = X_L / ind_result.dcr if ind_result.dcr > 0 else 0

print(f"\n=== Q-Factor Analysis ===")
print(f"Resonant frequency: {resonant_freq / 1e6:.2f} MHz")
print(f"Inductive reactance: {X_L:.2f} Ω")
print(f"Q-factor: {Q_factor:.1f}")

# Quality assessment
if Q_factor > 100:
    quality = "Excellent (RF applications)"
elif Q_factor > 50:
    quality = "Good (general purpose)"
elif Q_factor > 20:
    quality = "Acceptable (power applications)"
else:
    quality = "Low (check for issues)"

print(f"Quality: {quality}")
```

#### Step 3: Self-Resonant Frequency

```python
# Plot impedance magnitude vs. frequency
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Impedance magnitude
ax1.semilogx(pos_freqs, pos_Z, 'b-', linewidth=2)
ax1.axvline(x=resonant_freq, color='r', linestyle='--',
            label=f'SRF = {resonant_freq/1e6:.2f} MHz')
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('|Z| (Ω)')
ax1.set_title('Inductor Impedance vs. Frequency')
ax1.grid(True, which='both', alpha=0.3)
ax1.legend()

# Phase
phase = np.angle(Z[pos_idx], deg=True)
ax2.semilogx(pos_freqs, phase, 'g-', linewidth=2)
ax2.axvline(x=resonant_freq, color='r', linestyle='--')
ax2.axhline(y=0, color='k', linestyle=':', alpha=0.5)
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Phase (degrees)')
ax2.set_title('Impedance Phase')
ax2.grid(True, which='both', alpha=0.3)

plt.tight_layout()
plt.savefig('inductor_characterization.png', dpi=300)
plt.show()

print(f"\nSelf-resonant frequency: {resonant_freq / 1e6:.2f} MHz")
print(f"Use inductor below {resonant_freq / 1e6 * 0.5:.2f} MHz for best performance")
```

---

### Tutorial 6: Parasitic Extraction

**Goal:** Extract parasitic R, L, C parameters from an interconnect or component.

#### Step 1: Capture Impedance Data

```python
import tracekit as tk
from tracekit.component import extract_parasitics

# Load voltage and current measurements
voltage_trace = tk.load("interconnect_voltage.wfm")
current_trace = tk.load("interconnect_current.wfm")

# Extract parasitic parameters using series RLC model
parasitics = extract_parasitics(
    voltage_trace,
    current_trace,
    model="series_RLC",
    frequency_range=(1e6, 1e9)  # Analyze 1 MHz to 1 GHz
)

print(f"\n=== Parasitic Extraction ===")
print(f"Model: {parasitics.model_type}")
print(f"Resistance: {parasitics.resistance:.3f} Ω")
print(f"Inductance: {parasitics.inductance * 1e9:.2f} nH")
print(f"Capacitance: {parasitics.capacitance * 1e12:.2f} pF")

if parasitics.resonant_freq is not None:
    print(f"Resonant frequency: {parasitics.resonant_freq / 1e9:.3f} GHz")

print(f"Model fit quality: {parasitics.fit_quality:.3f} (R²)")
```

#### Step 2: Validate Model Fit

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# Get measured impedance
voltage = voltage_trace.data
current = current_trace.data
sample_rate = voltage_trace.metadata.sample_rate

V_fft = fft(voltage)
I_fft = fft(current)
freqs = fftfreq(len(voltage), 1/sample_rate)

Z_measured = V_fft / (I_fft + 1e-20)

# Calculate model impedance
pos_idx = (freqs > 1e6) & (freqs < 1e9)
freqs_model = freqs[pos_idx]
omega = 2 * np.pi * freqs_model

# Series RLC: Z = R + j(ωL - 1/(ωC))
Z_model = (parasitics.resistance +
           1j * (omega * parasitics.inductance -
                 1 / (omega * parasitics.capacitance + 1e-20)))

# Plot comparison
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Magnitude
ax1.loglog(freqs_model, np.abs(Z_measured[pos_idx]), 'b-',
           linewidth=2, label='Measured')
ax1.loglog(freqs_model, np.abs(Z_model), 'r--',
           linewidth=2, label='Model')
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('|Z| (Ω)')
ax1.set_title('Impedance Magnitude: Measured vs. Model')
ax1.grid(True, which='both', alpha=0.3)
ax1.legend()

# Phase
ax2.semilogx(freqs_model, np.angle(Z_measured[pos_idx], deg=True), 'b-',
             linewidth=2, label='Measured')
ax2.semilogx(freqs_model, np.angle(Z_model, deg=True), 'r--',
             linewidth=2, label='Model')
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Phase (degrees)')
ax2.set_title('Impedance Phase')
ax2.grid(True, which='both', alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.savefig('parasitic_model_fit.png', dpi=300)
plt.show()
```

#### Step 3: Application-Specific Analysis

```python
# Analyze for specific frequency ranges
frequency_ranges = {
    "Audio": (20, 20e3),
    "USB 2.0": (1e6, 500e6),
    "DDR4": (100e6, 2.4e9),
    "PCIe Gen3": (100e6, 8e9),
}

print(f"\n=== Frequency Range Analysis ===")

for app_name, (f_min, f_max) in frequency_ranges.items():
    # Recalculate for specific range
    app_parasitics = extract_parasitics(
        voltage_trace,
        current_trace,
        model="series_RLC",
        frequency_range=(f_min, f_max)
    )

    print(f"\n{app_name} ({f_min/1e6:.1f}-{f_max/1e6:.1f} MHz):")
    print(f"  R = {app_parasitics.resistance:.3f} Ω")
    print(f"  L = {app_parasitics.inductance * 1e9:.2f} nH")
    print(f"  C = {app_parasitics.capacitance * 1e12:.2f} pF")
    print(f"  Fit: R² = {app_parasitics.fit_quality:.3f}")
```

---

## Advanced Techniques

### Differential Impedance Measurement

Measure differential impedance for high-speed differential pairs (USB, Ethernet, HDMI, etc.).

```python
import tracekit as tk
from tracekit.component import extract_impedance
import numpy as np

# Load TDR measurements for both traces
tdr_p = tk.load("diff_pair_positive_tdr.wfm")
tdr_n = tk.load("diff_pair_negative_tdr.wfm")

# Extract single-ended impedance
z0_p, profile_p = extract_impedance(tdr_p, z0_source=50.0, velocity_factor=0.66)
z0_n, profile_n = extract_impedance(tdr_n, z0_source=50.0, velocity_factor=0.66)

# Calculate differential impedance
# Z_diff = 2 × Z_0 × (1 - k)  where k is coupling coefficient
# Simplified: Z_diff ≈ 2 × Z_0 for weak coupling

z_diff = 2 * np.mean([z0_p, z0_n])

print(f"\n=== Differential Impedance ===")
print(f"Positive trace Z0: {z0_p:.2f} Ω")
print(f"Negative trace Z0: {z0_n:.2f} Ω")
print(f"Differential impedance: {z_diff:.2f} Ω")

# Check trace matching
mismatch = abs(z0_p - z0_n)
mismatch_pct = mismatch / np.mean([z0_p, z0_n]) * 100

print(f"Trace mismatch: {mismatch:.2f} Ω ({mismatch_pct:.1f}%)")

# Target specifications
targets = {
    "USB 2.0": 90,
    "USB 3.0": 90,
    "HDMI": 100,
    "Ethernet": 100,
    "PCIe": 85,
}

print("\nComparison with standards:")
for interface, target_z in targets.items():
    error = abs(z_diff - target_z) / target_z * 100
    status = "✓" if error < 10 else "✗"
    print(f"  {interface:10s}: {target_z}Ω  {status} ({error:.1f}% error)")
```

### Crosstalk Analysis

Analyze near-end and far-end crosstalk between adjacent traces.

```python
import tracekit as tk
import numpy as np

# Load victim and aggressor signals
victim = tk.load("crosstalk_victim.wfm")
aggressor = tk.load("crosstalk_aggressor.wfm")

# Calculate near-end crosstalk (NEXT)
victim_data = victim.data
aggressor_data = aggressor.data

# Align signals
min_len = min(len(victim_data), len(aggressor_data))
victim_data = victim_data[:min_len]
aggressor_data = aggressor_data[:min_len]

# NEXT coefficient (near-end coupling)
aggressor_peak = np.max(np.abs(aggressor_data))
victim_peak = np.max(np.abs(victim_data))

next_db = 20 * np.log10(victim_peak / aggressor_peak) if aggressor_peak > 0 else -np.inf

print(f"\n=== Crosstalk Analysis ===")
print(f"Aggressor peak: {aggressor_peak:.3f} V")
print(f"Victim peak: {victim_peak:.3f} V")
print(f"NEXT: {next_db:.1f} dB")

# Crosstalk quality assessment
if next_db < -40:
    quality = "Excellent"
elif next_db < -30:
    quality = "Good"
elif next_db < -20:
    quality = "Acceptable"
else:
    quality = "Poor - redesign recommended"

print(f"Crosstalk quality: {quality}")

# Frequency-dependent crosstalk
from scipy.fft import fft, fftfreq

V_vic = fft(victim_data)
V_agg = fft(aggressor_data)
freqs = fftfreq(min_len, 1/victim.metadata.sample_rate)

# Calculate transfer function
H_xt = V_vic / (V_agg + 1e-20)
xt_db = 20 * np.log10(np.abs(H_xt))

# Plot crosstalk vs. frequency
import matplotlib.pyplot as plt

pos_idx = (freqs > 0) & (freqs < victim.metadata.sample_rate / 2)
pos_freqs = freqs[pos_idx]
pos_xt = xt_db[pos_idx]

plt.figure(figsize=(10, 6))
plt.semilogx(pos_freqs, pos_xt, 'b-', linewidth=2)
plt.axhline(y=-20, color='orange', linestyle='--', label='Acceptable (-20 dB)')
plt.axhline(y=-30, color='green', linestyle='--', label='Good (-30 dB)')
plt.axhline(y=-40, color='darkgreen', linestyle='--', label='Excellent (-40 dB)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Crosstalk (dB)')
plt.title('Frequency-Dependent Crosstalk')
plt.grid(True, which='both', alpha=0.3)
plt.legend()
plt.savefig('crosstalk_frequency.png', dpi=300)
plt.show()
```

### Signal Integrity Validation

Comprehensive signal integrity analysis for high-speed interfaces.

```python
import tracekit as tk
import numpy as np

# Load high-speed signal capture
signal = tk.load("high_speed_signal.wfm")

# Basic signal quality metrics
from tracekit.analyzers.timing import (
    measure_rise_time,
    measure_fall_time,
    measure_overshoot,
    measure_jitter
)

rise_time = measure_rise_time(signal)
fall_time = measure_fall_time(signal)
overshoot = measure_overshoot(signal)

print(f"\n=== Signal Integrity Metrics ===")
print(f"Rise time: {rise_time * 1e9:.2f} ns")
print(f"Fall time: {fall_time * 1e9:.2f} ns")
print(f"Overshoot: {overshoot:.1f}%")

# Jitter analysis
jitter_result = measure_jitter(signal)
print(f"Peak-to-peak jitter: {jitter_result['pk_pk_jitter'] * 1e12:.2f} ps")
print(f"RMS jitter: {jitter_result['rms_jitter'] * 1e12:.2f} ps")

# Eye diagram analysis
from tracekit.visualization import plot_eye_diagram

fig = plot_eye_diagram(
    signal,
    bit_rate=10e9,  # 10 Gbps
    samples_per_bit=100
)
plt.savefig('signal_integrity_eye.png', dpi=300)

# Spectral purity
from tracekit.analyzers.spectral import compute_fft, measure_snr, measure_thd

spectrum = compute_fft(signal, window="hann")
snr = measure_snr(signal, signal_freq=10e9)
thd = measure_thd(signal)

print(f"\n=== Spectral Quality ===")
print(f"SNR: {snr:.1f} dB")
print(f"THD: {thd:.2f}%")

# Pass/fail criteria for common interfaces
interfaces = {
    "USB 2.0 (480 Mbps)": {
        "rise_time_max": 4e-9,
        "overshoot_max": 10,
        "jitter_max": 500e-12,
    },
    "USB 3.0 (5 Gbps)": {
        "rise_time_max": 100e-12,
        "overshoot_max": 15,
        "jitter_max": 5e-12,
    },
    "PCIe Gen3 (8 Gbps)": {
        "rise_time_max": 60e-12,
        "overshoot_max": 20,
        "jitter_max": 3e-12,
    },
}

print(f"\n=== Compliance Check ===")
for iface, limits in interfaces.items():
    print(f"\n{iface}:")

    rt_pass = rise_time <= limits["rise_time_max"]
    os_pass = overshoot <= limits["overshoot_max"]
    jit_pass = jitter_result['pk_pk_jitter'] <= limits["jitter_max"]

    print(f"  Rise time: {rise_time*1e9:.2f}ns {'✓' if rt_pass else '✗'} (< {limits['rise_time_max']*1e9:.2f}ns)")
    print(f"  Overshoot: {overshoot:.1f}% {'✓' if os_pass else '✗'} (< {limits['overshoot_max']}%)")
    print(f"  Jitter: {jitter_result['pk_pk_jitter']*1e12:.2f}ps {'✓' if jit_pass else '✗'} (< {limits['jitter_max']*1e12:.2f}ps)")

    if rt_pass and os_pass and jit_pass:
        print(f"  Overall: ✓ PASS")
    else:
        print(f"  Overall: ✗ FAIL")
```

### Component Model Extraction

Extract SPICE-compatible component models from measurements.

```python
import tracekit as tk
from tracekit.component import extract_parasitics
import numpy as np

# Load S-parameter or impedance measurement
voltage_trace = tk.load("component_voltage.wfm")
current_trace = tk.load("component_current.wfm")

# Extract full model
parasitics = extract_parasitics(
    voltage_trace,
    current_trace,
    model="series_RLC",
    frequency_range=(100e3, 1e9)
)

# Generate SPICE model
def generate_spice_model(name, R, L, C):
    """Generate SPICE subcircuit model."""
    spice = f"""
* Component model extracted by TraceKit
* Date: 2026-01-08
.SUBCKT {name} 1 2
R{name} 1 3 {R:.6e}
L{name} 3 4 {L:.6e}
C{name} 4 2 {C:.6e}
.ENDS {name}
"""
    return spice

model_text = generate_spice_model(
    "EXTRACTED_COMPONENT",
    parasitics.resistance,
    parasitics.inductance,
    parasitics.capacitance
)

print("\n=== SPICE Model ===")
print(model_text)

# Save to file
with open("extracted_component_model.sp", "w") as f:
    f.write(model_text)

print("SPICE model saved to: extracted_component_model.sp")

# Generate usage example
usage = f"""
* Example usage:
.INCLUDE extracted_component_model.sp
X1 node1 node2 EXTRACTED_COMPONENT

* Model parameters:
* R = {parasitics.resistance:.3f} Ω
* L = {parasitics.inductance*1e9:.2f} nH
* C = {parasitics.capacitance*1e12:.2f} pF
* SRF = {parasitics.resonant_freq/1e6:.2f} MHz
* Fit quality: R² = {parasitics.fit_quality:.3f}
"""

print(usage)
```

---

## Real-World Applications

### High-Speed PCB Validation

Complete workflow for validating high-speed PCB designs.

```python
import tracekit as tk
from tracekit.component import extract_impedance, discontinuity_analysis
import numpy as np

def validate_pcb_trace(tdr_file, trace_name, target_z0=50.0, tolerance=0.1):
    """Validate a PCB trace against specifications."""

    print(f"\n{'='*60}")
    print(f"Validating: {trace_name}")
    print(f"{'='*60}")

    # Load TDR measurement
    tdr = tk.load(tdr_file)

    # Extract impedance
    z0, profile = extract_impedance(
        tdr,
        z0_source=50.0,
        velocity_factor=0.66,
        start_time=2e-9,
        end_time=20e-9
    )

    # Calculate metrics
    z_mean = profile.mean_impedance
    z_std = profile.statistics['z0_std']
    z_min = profile.min_impedance
    z_max = profile.max_impedance

    print(f"\nImpedance Measurements:")
    print(f"  Target: {target_z0:.1f} ± {tolerance*100:.0f}%")
    print(f"  Measured: {z_mean:.2f} Ω")
    print(f"  Range: {z_min:.2f} - {z_max:.2f} Ω")
    print(f"  Std Dev: {z_std:.2f} Ω")

    # Check specifications
    z_error = abs(z_mean - target_z0) / target_z0
    z_variation = z_std / z_mean

    results = {
        'trace_name': trace_name,
        'z0_measured': z_mean,
        'z0_target': target_z0,
        'error_pct': z_error * 100,
        'variation_pct': z_variation * 100,
        'pass': True
    }

    # Impedance accuracy check
    if z_error <= tolerance:
        print(f"  ✓ Impedance within {tolerance*100:.0f}% tolerance")
    else:
        print(f"  ✗ Impedance outside {tolerance*100:.0f}% tolerance")
        results['pass'] = False

    # Variation check (should be < 5%)
    if z_variation < 0.05:
        print(f"  ✓ Low variation ({z_variation*100:.1f}%)")
    else:
        print(f"  ✗ High variation ({z_variation*100:.1f}%)")
        results['pass'] = False

    # Discontinuity analysis
    discontinuities = discontinuity_analysis(
        tdr,
        z0_source=50.0,
        velocity_factor=0.66,
        threshold=3.0,
        min_separation=500e-12
    )

    print(f"\nDiscontinuities: {len(discontinuities)}")
    if len(discontinuities) == 0:
        print(f"  ✓ No significant discontinuities")
    else:
        for i, disc in enumerate(discontinuities, 1):
            print(f"  {i}. @ {disc.position*1000:.2f}mm: "
                  f"{disc.magnitude:+.1f}Ω ({disc.discontinuity_type})")

        # Check if discontinuities are acceptable
        max_disc = max(abs(d.magnitude) for d in discontinuities)
        if max_disc < target_z0 * 0.15:  # < 15% impedance change
            print(f"  ✓ Discontinuities < 15% ({max_disc:.1f}Ω)")
        else:
            print(f"  ✗ Large discontinuities ({max_disc:.1f}Ω)")
            results['pass'] = False

    results['num_discontinuities'] = len(discontinuities)

    return results

# Validate multiple traces
traces = [
    ("usb_dp_tdr.wfm", "USB D+", 45, 0.1),
    ("usb_dn_tdr.wfm", "USB D-", 45, 0.1),
    ("eth_tx_p_tdr.wfm", "ETH TX+", 50, 0.1),
    ("eth_tx_n_tdr.wfm", "ETH TX-", 50, 0.1),
]

results = []
for tdr_file, name, target, tol in traces:
    try:
        result = validate_pcb_trace(tdr_file, name, target, tol)
        results.append(result)
    except FileNotFoundError:
        print(f"\nSkipping {name}: File not found")

# Summary report
print(f"\n{'='*60}")
print(f"VALIDATION SUMMARY")
print(f"{'='*60}")

passed = sum(1 for r in results if r['pass'])
failed = len(results) - passed

print(f"\nTraces tested: {len(results)}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")

if failed == 0:
    print(f"\n✓ All traces meet specifications")
else:
    print(f"\n✗ {failed} trace(s) failed validation")
    print(f"\nFailed traces:")
    for r in results:
        if not r['pass']:
            print(f"  - {r['trace_name']}: "
                  f"{r['error_pct']:.1f}% error, "
                  f"{r['num_discontinuities']} discontinuities")
```

### Component Quality Control

Automated quality control for incoming components.

```python
import tracekit as tk
from tracekit.component import measure_capacitance, measure_inductance
import numpy as np

def qc_capacitor(voltage_file, current_file, nominal_value, tolerance=0.2):
    """Quality control test for capacitors."""

    # Load measurements
    voltage = tk.load(voltage_file)
    current = tk.load(current_file)

    # Measure capacitance
    result = measure_capacitance(voltage, current, method="charge")

    # Calculate deviation
    deviation = abs(result.capacitance - nominal_value) / nominal_value

    print(f"\n=== Capacitor QC ===")
    print(f"Nominal: {nominal_value*1e6:.2f} µF")
    print(f"Measured: {result.capacitance*1e6:.2f} µF")
    print(f"ESR: {result.esr*1e3:.2f} mΩ")
    print(f"Deviation: {deviation*100:.1f}%")

    # Pass/fail
    if deviation <= tolerance:
        print(f"✓ PASS (within {tolerance*100:.0f}%)")
        return True
    else:
        print(f"✗ FAIL (outside {tolerance*100:.0f}%)")
        return False

def qc_inductor(voltage_file, current_file, nominal_value, max_dcr):
    """Quality control test for inductors."""

    # Load measurements
    voltage = tk.load(voltage_file)
    current = tk.load(current_file)

    # Measure inductance
    result = measure_inductance(voltage, current, method="flux")

    # Calculate deviation
    deviation = abs(result.inductance - nominal_value) / nominal_value

    print(f"\n=== Inductor QC ===")
    print(f"Nominal: {nominal_value*1e6:.2f} µH")
    print(f"Measured: {result.inductance*1e6:.2f} µH")
    print(f"DCR: {result.dcr:.3f} Ω")
    print(f"Deviation: {deviation*100:.1f}%")

    # Pass/fail criteria
    value_ok = deviation <= 0.2  # 20% tolerance
    dcr_ok = result.dcr <= max_dcr

    if value_ok and dcr_ok:
        print(f"✓ PASS")
        return True
    else:
        if not value_ok:
            print(f"✗ FAIL: Inductance out of spec")
        if not dcr_ok:
            print(f"✗ FAIL: DCR too high ({result.dcr:.3f}Ω > {max_dcr:.3f}Ω)")
        return False

# Batch testing
def batch_qc_test(components, test_func):
    """Run QC tests on batch of components."""

    passed = 0
    failed = 0

    for comp_id, *params in components:
        print(f"\nTesting component {comp_id}...")
        try:
            if test_func(*params):
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ ERROR: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Batch QC Summary")
    print(f"{'='*60}")
    print(f"Total tested: {passed + failed}")
    print(f"Passed: {passed} ({passed/(passed+failed)*100:.1f}%)")
    print(f"Failed: {failed} ({failed/(passed+failed)*100:.1f}%)")

    return passed, failed

# Example batch test
capacitors = [
    ("CAP001", "cap001_v.wfm", "cap001_i.wfm", 10e-6, 0.2),
    ("CAP002", "cap002_v.wfm", "cap002_i.wfm", 10e-6, 0.2),
    # ... more capacitors
]

# batch_qc_test(capacitors, qc_capacitor)
```

### Cable Qualification for Production

Qualify cables for production use with comprehensive testing.

```python
import tracekit as tk
from tracekit.component import transmission_line_analysis, discontinuity_analysis
import numpy as np

def qualify_cable(tdr_file, cable_id, spec):
    """
    Qualify a cable against specifications.

    spec: dict with keys:
        - nominal_z0: Target impedance
        - z0_tolerance: Impedance tolerance (fraction)
        - nominal_length: Target length (m)
        - length_tolerance: Length tolerance (fraction)
        - max_loss: Maximum loss (dB/m)
        - max_discontinuities: Maximum number of discontinuities
    """

    print(f"\n{'='*60}")
    print(f"Cable Qualification: {cable_id}")
    print(f"{'='*60}")

    # Load TDR
    tdr = tk.load(tdr_file)

    # Analyze transmission line
    result = transmission_line_analysis(
        tdr,
        z0_source=50.0,
        line_length=spec['nominal_length']
    )

    print(f"\nMeasurements:")
    print(f"  Impedance: {result.z0:.2f} Ω (target: {spec['nominal_z0']:.0f} ± {spec['z0_tolerance']*100:.0f}%)")
    print(f"  Length: {result.length:.3f} m (target: {spec['nominal_length']:.2f} ± {spec['length_tolerance']*100:.0f}%)")
    print(f"  Velocity factor: {result.velocity_factor:.3f}")

    if result.loss is not None:
        loss_per_m = result.loss / result.length
        print(f"  Loss: {result.loss:.2f} dB ({loss_per_m:.2f} dB/m)")

    if result.return_loss is not None:
        print(f"  Return loss: {result.return_loss:.2f} dB")

    # Check specifications
    tests_passed = []

    # Impedance check
    z_error = abs(result.z0 - spec['nominal_z0']) / spec['nominal_z0']
    if z_error <= spec['z0_tolerance']:
        print(f"  ✓ Impedance: {z_error*100:.1f}% error")
        tests_passed.append(True)
    else:
        print(f"  ✗ Impedance: {z_error*100:.1f}% error (> {spec['z0_tolerance']*100:.0f}%)")
        tests_passed.append(False)

    # Length check
    length_error = abs(result.length - spec['nominal_length']) / spec['nominal_length']
    if length_error <= spec['length_tolerance']:
        print(f"  ✓ Length: {length_error*100:.1f}% error")
        tests_passed.append(True)
    else:
        print(f"  ✗ Length: {length_error*100:.1f}% error (> {spec['length_tolerance']*100:.0f}%)")
        tests_passed.append(False)

    # Loss check
    if result.loss is not None and 'max_loss' in spec:
        loss_per_m = result.loss / result.length
        if loss_per_m <= spec['max_loss']:
            print(f"  ✓ Loss: {loss_per_m:.2f} dB/m (< {spec['max_loss']:.2f} dB/m)")
            tests_passed.append(True)
        else:
            print(f"  ✗ Loss: {loss_per_m:.2f} dB/m (> {spec['max_loss']:.2f} dB/m)")
            tests_passed.append(False)

    # Discontinuity check
    discontinuities = discontinuity_analysis(
        tdr,
        z0_source=50.0,
        velocity_factor=result.velocity_factor,
        threshold=5.0
    )

    num_disc = len(discontinuities)
    if num_disc <= spec.get('max_discontinuities', 0):
        print(f"  ✓ Discontinuities: {num_disc} (< {spec.get('max_discontinuities', 0)})")
        tests_passed.append(True)
    else:
        print(f"  ✗ Discontinuities: {num_disc} (> {spec.get('max_discontinuities', 0)})")
        tests_passed.append(False)

    # Overall result
    print(f"\n{'='*60}")
    if all(tests_passed):
        print(f"✓ CABLE QUALIFIED")
        return True
    else:
        print(f"✗ CABLE REJECTED")
        return False

# Cable specifications
coax_50ohm_spec = {
    'nominal_z0': 50.0,
    'z0_tolerance': 0.05,      # ±5%
    'nominal_length': 2.0,     # 2 meters
    'length_tolerance': 0.02,   # ±2%
    'max_loss': 0.5,           # 0.5 dB/m @ 1 GHz
    'max_discontinuities': 0    # No discontinuities allowed
}

# Test cable
# qualify_cable("cable_001_tdr.wfm", "CABLE-001", coax_50ohm_spec)
```

### Design Verification Workflow

Complete design verification for high-speed designs.

```python
import tracekit as tk
from tracekit.component import extract_impedance, discontinuity_analysis
import numpy as np
import json

class DesignVerification:
    """Complete design verification workflow."""

    def __init__(self, design_name, spec_file):
        self.design_name = design_name
        self.results = []

        # Load specifications
        with open(spec_file, 'r') as f:
            self.specs = json.load(f)

    def verify_trace(self, tdr_file, trace_name):
        """Verify a single trace."""

        print(f"\nVerifying: {trace_name}")

        # Get specification for this trace
        spec = self.specs['traces'].get(trace_name)
        if spec is None:
            print(f"  Warning: No specification found for {trace_name}")
            return None

        # Load and analyze
        tdr = tk.load(tdr_file)
        z0, profile = extract_impedance(
            tdr,
            z0_source=spec['source_impedance'],
            velocity_factor=spec['velocity_factor']
        )

        # Check against specs
        z_target = spec['target_impedance']
        z_tol = spec['impedance_tolerance']

        result = {
            'trace': trace_name,
            'z0_measured': z0,
            'z0_target': z_target,
            'z0_tolerance': z_tol,
            'pass': abs(z0 - z_target) / z_target <= z_tol
        }

        print(f"  Z0: {z0:.2f}Ω (target: {z_target}Ω ±{z_tol*100:.0f}%)")
        print(f"  Result: {'✓ PASS' if result['pass'] else '✗ FAIL'}")

        self.results.append(result)
        return result

    def generate_report(self, output_file):
        """Generate verification report."""

        passed = sum(1 for r in self.results if r['pass'])
        total = len(self.results)

        report = f"""
Design Verification Report
{'='*60}

Design: {self.design_name}
Date: 2026-01-08
Test Count: {total}
Passed: {passed} ({passed/total*100:.1f}%)
Failed: {total-passed} ({(total-passed)/total*100:.1f}%)

{'='*60}
Detailed Results:

"""

        for r in self.results:
            status = "PASS" if r['pass'] else "FAIL"
            error = abs(r['z0_measured'] - r['z0_target']) / r['z0_target'] * 100

            report += f"""
Trace: {r['trace']}
  Measured: {r['z0_measured']:.2f} Ω
  Target: {r['z0_target']:.2f} Ω
  Error: {error:.1f}%
  Status: {status}
"""

        report += f"""
{'='*60}
Overall Result: {'✓ DESIGN VERIFIED' if passed == total else '✗ DESIGN NEEDS REWORK'}
{'='*60}
"""

        # Save report
        with open(output_file, 'w') as f:
            f.write(report)

        print(f"\nReport saved to: {output_file}")
        return report

# Example usage
"""
# Create specification file (design_spec.json):
{
    "traces": {
        "USB_DP": {
            "target_impedance": 45,
            "impedance_tolerance": 0.1,
            "source_impedance": 50,
            "velocity_factor": 0.66
        },
        "USB_DN": {
            "target_impedance": 45,
            "impedance_tolerance": 0.1,
            "source_impedance": 50,
            "velocity_factor": 0.66
        }
    }
}

# Run verification
dv = DesignVerification("USB_HUB_Rev_A", "design_spec.json")
dv.verify_trace("usb_dp_tdr.wfm", "USB_DP")
dv.verify_trace("usb_dn_tdr.wfm", "USB_DN")
dv.generate_report("verification_report.txt")
"""
```

---

## Troubleshooting

### Common TDR Issues

#### Issue 1: Noisy TDR Waveform

**Symptom:** TDR waveform has excessive noise, making impedance extraction difficult.

**Causes:**

- Insufficient averaging
- Poor probe ground connection
- EMI/RFI interference
- Oscilloscope bandwidth too high

**Solutions:**

```python
import tracekit as tk
import numpy as np
from scipy.signal import savgol_filter

# Load noisy TDR
tdr = tk.load("noisy_tdr.wfm")

# Apply smoothing
from tracekit.component import impedance_profile

# Use built-in smoothing
profile = impedance_profile(
    tdr,
    z0_source=50.0,
    velocity_factor=0.66,
    smooth_window=11  # Use moving average smoothing
)

# Or apply custom filtering
smoothed_data = savgol_filter(tdr.data, window_length=11, polyorder=3)
tdr_smooth = tk.WaveformTrace(
    data=smoothed_data,
    metadata=tdr.metadata
)

# Extract impedance from smoothed data
z0, profile = extract_impedance(tdr_smooth, z0_source=50.0)

print(f"Impedance (smoothed): {z0:.2f} Ω")
```

**Prevention:**

- Increase oscilloscope averaging (16-64 averages)
- Use bandwidth limiting on oscilloscope
- Ensure good ground connection
- Shield setup from noise sources

#### Issue 2: Incorrect Velocity Factor

**Symptom:** Distance measurements don't match physical dimensions.

**Solution:**

```python
import tracekit as tk
from tracekit.component import velocity_factor

# Measure TDR with known physical length
tdr = tk.load("known_length_tdr.wfm")

# Calculate correct velocity factor
physical_length = 0.100  # 100mm = 0.1m
vf = velocity_factor(tdr, line_length=physical_length)

print(f"Calculated velocity factor: {vf:.3f}")

# Use corrected value for future measurements
from tracekit.component import extract_impedance

z0, profile = extract_impedance(
    tdr,
    z0_source=50.0,
    velocity_factor=vf  # Use measured value
)
```

**Common Velocity Factors:**

| Material/Cable  | Velocity Factor |
| --------------- | --------------- |
| FR4 PCB         | 0.60 - 0.70     |
| Polyimide PCB   | 0.55 - 0.65     |
| RG-58 Coax      | 0.66            |
| LMR-400 Coax    | 0.85            |
| PTFE Coax       | 0.70            |
| Air (stripline) | 1.00            |

#### Issue 3: Calibration Errors

**Symptom:** Measurements don't match known standards.

**Solution:**

```python
import tracekit as tk
from tracekit.component import characteristic_impedance
import numpy as np

# Measure calibration standards
print("=== TDR Calibration ===")

# 1. Measure 50Ω load
tdr_50ohm = tk.load("cal_50ohm_load.wfm")
z_50 = characteristic_impedance(tdr_50ohm, z0_source=50.0)
print(f"50Ω load: {z_50:.2f}Ω (error: {abs(z_50-50)/50*100:.1f}%)")

# 2. Measure open
tdr_open = tk.load("cal_open.wfm")
z_open = characteristic_impedance(tdr_open, z0_source=50.0)
print(f"Open: {z_open:.2f}Ω (should be >> 50Ω)")

# 3. Measure short
tdr_short = tk.load("cal_short.wfm")
z_short = characteristic_impedance(tdr_short, z0_source=50.0)
print(f"Short: {z_short:.2f}Ω (should be << 50Ω)")

# Calculate calibration factors
cal_factor = 50.0 / z_50 if abs(z_50) > 1 else 1.0

print(f"\nCalibration factor: {cal_factor:.4f}")
print("Apply this factor to future measurements:")
print(f"  z0_corrected = z0_measured × {cal_factor:.4f}")
```

### Calibration Tips

**Best Practices:**

1. **Daily calibration:** Calibrate at start of each measurement session
2. **Use quality standards:** Precision 50Ω loads, not terminators
3. **Check cables:** Verify test cables with known good reference
4. **Temperature:** Allow equipment to warm up (30 minutes minimum)
5. **Probe compensation:** Compensate probes before TDR measurements

**Calibration Workflow:**

```python
def calibration_workflow():
    """Complete TDR calibration procedure."""

    print("TDR Calibration Procedure")
    print("="*60)

    input("1. Connect 50Ω precision load. Press Enter...")
    # Measure and save 50Ω reference

    input("2. Connect OPEN standard. Press Enter...")
    # Measure and save open reference

    input("3. Connect SHORT standard. Press Enter...")
    # Measure and save short reference

    print("\nCalibration complete!")
    print("Save calibration data for today's measurements.")

# calibration_workflow()
```

### Measurement Accuracy

**Factors Affecting Accuracy:**

1. **Sample rate:** Higher is better
   - Minimum: 10× rise time frequency
   - Recommended: 100× rise time frequency

2. **Rise time:** Faster is better
   - <100ps for PCB traces
   - <50ps for high-speed interfaces

3. **Probe quality:** Use appropriate probes
   - TDR-specific probes for best results
   - High-bandwidth scope probes (>1GHz)

4. **Connection quality:** Minimize parasitics
   - Direct connection when possible
   - SMA or 2.92mm connectors for >6GHz
   - Short ground leads (<10mm)

**Accuracy Estimation:**

```python
import tracekit as tk
import numpy as np

def estimate_measurement_accuracy(tdr_file, num_measurements=10):
    """Estimate measurement accuracy through repeated measurements."""

    measurements = []

    print("Measuring impedance repeatability...")
    for i in range(num_measurements):
        tdr = tk.load(f"{tdr_file}_{i}.wfm")
        z0, _ = extract_impedance(tdr, z0_source=50.0)
        measurements.append(z0)

    mean_z = np.mean(measurements)
    std_z = np.std(measurements)

    print(f"\nMeasurement Statistics:")
    print(f"  Mean: {mean_z:.3f} Ω")
    print(f"  Std Dev: {std_z:.3f} Ω")
    print(f"  Repeatability: ±{std_z:.3f} Ω ({std_z/mean_z*100:.2f}%)")

    # 95% confidence interval (±2σ)
    ci_95 = 2 * std_z
    print(f"  95% CI: ±{ci_95:.3f} Ω")

    return mean_z, std_z

# Example: measure 10 times to assess accuracy
# estimate_measurement_accuracy("pcb_trace", num_measurements=10)
```

---

## Summary

This guide covered comprehensive component analysis techniques using TraceKit:

### Key Takeaways

1. **TDR Fundamentals**
   - Understanding reflection coefficients and impedance calculations
   - Proper calibration and measurement setup
   - Velocity factor importance

2. **Component Characterization**
   - PCB trace impedance measurement and validation
   - Connector and cable quality assessment
   - Capacitor ESR and inductor DCR measurements
   - Parasitic parameter extraction

3. **Advanced Techniques**
   - Differential impedance for high-speed interfaces
   - Crosstalk analysis and mitigation
   - Signal integrity validation and compliance
   - SPICE model extraction

4. **Practical Applications**
   - High-speed PCB validation workflows
   - Component quality control procedures
   - Cable qualification for production
   - Design verification processes

5. **Troubleshooting**
   - Handling noisy measurements
   - Calibration procedures
   - Accuracy estimation and improvement

### Additional Resources

- **TraceKit Documentation**: [docs/](../index.md)
- **API Reference**: [docs/api/](../api/index.md)
- **Examples**: [examples/](../../examples/)
- **Standards**:
  - IPC-TM-650 2.5.5.7: Characteristic Impedance
  - IEEE 370-2020: Interconnect Characterization
  - IEEE 181-2011: Pulse Measurements
  - JEDEC Standards: Signal integrity specifications

### Getting Help

- GitHub Issues: [github.com/lair-click-bats/tracekit/issues](https://github.com/lair-click-bats/tracekit/issues)
- Documentation: [docs/](../index.md)
- Examples: [examples/](../../examples/)

---

**Document Version**: 0.1.0
**Last Updated**: 2026-01-08
**TraceKit Version**: 0.1.0
