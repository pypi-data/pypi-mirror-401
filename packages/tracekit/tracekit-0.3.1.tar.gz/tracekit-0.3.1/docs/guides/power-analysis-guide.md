# Power Analysis with TraceKit

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08 | **Time**: 60 minutes

A comprehensive, practical guide to power analysis with TraceKit covering DC, AC, switching regulators, battery characterization, and motor analysis.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Basic Power Measurements](#basic-power-measurements)
4. [Advanced Topics](#advanced-topics)
5. [Best Practices](#best-practices)
6. [Real-World Examples](#real-world-examples)
7. [Troubleshooting](#troubleshooting)

## Introduction

### What is Power Analysis?

Power analysis is the measurement and characterization of electrical power consumption, efficiency, and quality in electronic systems. It encompasses:

- **DC Power Analysis** - Steady-state power consumption measurement
- **AC Power Analysis** - Voltage, current, phase relationships, and power factor
- **Efficiency Measurements** - Power conversion efficiency and losses
- **Power Quality** - Ripple, harmonics, and transient behavior
- **Energy Profiling** - Total energy consumption over time

### Why Power Analysis Matters

**Circuit Design & Optimization**

- Verify power supply specifications meet requirements
- Optimize efficiency to reduce heat and improve battery life
- Debug excessive power consumption issues

**Compliance & Standards**

- Meet power quality standards (IEEE 1459, IEC 61000)
- Verify efficiency ratings (80 PLUS, Energy Star)
- Ensure EMI/EMC compliance

**Battery-Powered Systems**

- Estimate battery runtime under various load conditions
- Optimize power modes (active, sleep, deep sleep)
- Characterize charge/discharge profiles

**Cost & Environmental Impact**

- Reduce energy costs in production systems
- Meet environmental regulations
- Optimize thermal management

### TraceKit Power Analysis Features

TraceKit provides IEEE-compliant power analysis functions:

- **Basic Power**: Instantaneous, average, peak, RMS, energy
- **AC Power**: Apparent power, reactive power, power factor
- **Efficiency**: Power conversion efficiency, multi-output analysis
- **Ripple Analysis**: Peak-to-peak, RMS, frequency content, harmonics
- **Switching Analysis**: Dead time, conduction loss, switching loss
- **Visualization**: Power waveforms, efficiency curves, Lissajous figures

## Prerequisites

### Hardware Setup

#### Required Equipment

1. **Oscilloscope** - Minimum 2 channels (4+ recommended)
   - Bandwidth: ≥10× highest frequency component
   - Sample rate: ≥100× signal frequency
   - Memory depth: Sufficient for analysis duration

2. **Voltage Probes**
   - Differential probe for isolated measurements
   - High voltage probe for mains measurements
   - Passive probe (10:1) for general use

3. **Current Probes**
   - Hall effect probe for DC + AC measurements
   - Current shunt resistor for high accuracy
   - Rogowski coil for high current AC measurements

#### Optional Equipment

- Power analyzer for comparison/validation
- Thermal camera for thermal profiling
- EMI probe for noise characterization

### Probe Selection and Placement

#### Voltage Measurement

**Grounding Considerations**

```
✓ GOOD: Differential probe across DUT
  Probe (+) ────┬──── DUT High
                │
  Probe (-) ────┴──── DUT Low
  (Isolated measurement)

✗ BAD: Ground-referenced probe on floating circuit
  Probe ────── DUT High
  Ground ──┬── DUT Low
           └── Earth (creates ground loop!)
```

**Best Practices**

- Use differential probes for floating measurements
- Keep probe ground leads short (<5 cm) to minimize inductance
- Probe directly at the device under test (DUT), not at connectors
- Use 1:1 probes for low voltage (<10V) for better noise immunity

#### Current Measurement

**Method 1: Current Probe (Non-invasive)**

```python
# Hall-effect or Rogowski probe clamps around conductor
# Advantages: Non-invasive, no voltage drop
# Disadvantages: Lower bandwidth, drift
```

**Method 2: Shunt Resistor (Invasive)**

```python
# Insert low-value resistor in current path
# Measure voltage across shunt: I = V_shunt / R_shunt
# Advantages: High accuracy, high bandwidth
# Disadvantages: Voltage drop, power dissipation
```

**Shunt Resistor Selection**

```python
import tracekit as tk

# Design parameters
max_current = 5.0      # A
max_voltage_drop = 0.1 # V (limit power loss)
min_voltage = 0.050    # V (oscilloscope noise floor)

# Calculate shunt resistance
r_shunt = min_voltage / max_current
print(f"Minimum shunt: {r_shunt*1000:.1f} mΩ")

# Check power rating
p_max = max_current**2 * r_shunt
print(f"Power dissipation: {p_max:.2f} W")
print(f"Recommended rating: ≥{p_max*2:.1f} W")

# Expected output:
# Minimum shunt: 10.0 mΩ
# Power dissipation: 0.25 W
# Recommended rating: ≥0.5 W
```

**Current Probe Calibration**

```python
import tracekit as tk
import numpy as np

# Measure known DC current
i_known = 1.0  # 1A from calibrated source
i_measured = tk.load("calibration_1A.wfm")

# Calculate scaling factor
scale_factor = i_known / np.mean(i_measured.data)
print(f"Current probe scale factor: {scale_factor:.4f}")

# Apply to measurements
i_actual = i_measured.data * scale_factor
```

### Grounding and Noise Reduction

#### Ground Loop Prevention

**Problem: Multiple Ground Paths**

```
Oscilloscope ────Ground───┐
                          ├─── Earth
DUT Power Supply ─Ground──┘
     ↑
   (Ground loop current flows, adds noise)
```

**Solution: Single-Point Grounding**

```python
# Use isolated/differential measurements
# Float oscilloscope (use battery power if available)
# Use isolated power supply for DUT
# Connect grounds at single point only
```

**Common Mode Rejection**

```python
import tracekit as tk

# Measure with differential probe
v_diff = tk.load("differential_measurement.wfm")

# Compare to single-ended (with ground loop)
v_single = tk.load("single_ended_measurement.wfm")

# Calculate common mode rejection ratio (CMRR)
noise_single = tk.rms(v_single - v_diff)
signal_rms = tk.rms(v_diff)
cmrr_db = 20 * np.log10(signal_rms / noise_single)
print(f"CMRR improvement: {cmrr_db:.1f} dB")
```

#### Shielding and Filtering

**Probe Shielding**

- Use shielded probes for low-level measurements
- Ground shields at oscilloscope end only
- Avoid ground loops through shield

**Hardware Filtering**

```python
# Use oscilloscope bandwidth limiting
# Typical: 20 MHz for power measurements
# Removes high-frequency switching noise

# Or apply digital filtering
import tracekit as tk

v_raw = tk.load("voltage_noisy.wfm")
v_filtered = tk.low_pass(v_raw, cutoff=1e6)  # 1 MHz cutoff

print(f"RMS before: {tk.rms(v_raw):.4f} V")
print(f"RMS after:  {tk.rms(v_filtered):.4f} V")
```

### Sample Rate Selection

#### Nyquist Criterion

For accurate power measurements:

```python
# Minimum sample rate
f_signal_max = 1e6  # Hz (highest frequency of interest)
f_sample_min = 2.5 * f_signal_max  # Nyquist + margin
print(f"Minimum sample rate: {f_sample_min/1e6:.1f} MS/s")

# Recommended sample rate
f_sample_rec = 10 * f_signal_max  # 10× for accurate waveform
print(f"Recommended sample rate: {f_sample_rec/1e6:.1f} MS/s")
```

#### Power Measurement Specific

**DC Power**: 100× switching frequency minimum

```python
f_switching = 100e3  # 100 kHz switching regulator
f_sample = 100 * f_switching
print(f"Sample rate: {f_sample/1e6:.1f} MS/s")
# Output: 10.0 MS/s
```

**AC Power (50/60 Hz)**: ≥10 kS/s for fundamental, ≥100 kS/s for harmonics

```python
f_line = 60  # Hz
f_harmonic_max = 50 * f_line  # Up to 50th harmonic
f_sample = 10 * f_harmonic_max
print(f"Sample rate for harmonic analysis: {f_sample/1e3:.1f} kS/s")
# Output: 30.0 kS/s
```

**Switching Regulator**: ≥100× switching frequency

```python
f_switching = 500e3  # 500 kHz buck converter
f_sample = 100 * f_switching
print(f"Sample rate: {f_sample/1e6:.1f} MS/s")
# Output: 50.0 MS/s
```

### Software Setup

#### Installing TraceKit

```bash
# Using uv (recommended)
uv pip install tracekit

# Or using pip
pip install tracekit

# Verify installation
python -c "import tracekit as tk; print(f'TraceKit version: {tk.__version__}')"
```

#### Required Imports

```python
import numpy as np
import tracekit as tk
import matplotlib.pyplot as plt

# Verify power analysis functions available
assert hasattr(tk, 'instantaneous_power')
assert hasattr(tk, 'power_factor')
assert hasattr(tk, 'efficiency')
print("TraceKit power analysis ready!")
```

## Basic Power Measurements

### DC Power Consumption

DC power is the product of voltage and current in purely DC circuits or the average power in pulsed DC systems.

#### Simple DC Measurement

**Scenario**: Measure power consumption of 5V microcontroller

```python
import tracekit as tk

# Load voltage and current traces
v_supply = tk.load("mcu_voltage.wfm")
i_supply = tk.load("mcu_current.wfm")

# Calculate instantaneous power
power = tk.instantaneous_power(v_supply, i_supply)

# Get DC power (average)
p_dc = tk.average_power(power)
print(f"DC Power: {p_dc*1000:.2f} mW")

# Calculate energy over measurement period
energy = tk.energy(power)
duration = len(power.data) / power.metadata.sample_rate
print(f"Energy: {energy*1e6:.2f} µJ over {duration*1e3:.2f} ms")
print(f"Average current: {p_dc/5.0*1e3:.2f} mA")
```

**Expected Output**:

```
DC Power: 125.50 mW
Energy: 1255.00 µJ over 10.00 ms
Average current: 25.10 mA
```

#### Statistical Analysis

```python
import tracekit as tk

# Get comprehensive power statistics
stats = tk.power_statistics(voltage=v_supply, current=i_supply)

print(f"Power Statistics:")
print(f"  Average:      {stats['average']*1000:.2f} mW")
print(f"  Peak:         {stats['peak']*1000:.2f} mW")
print(f"  Minimum:      {stats['min']*1000:.2f} mW")
print(f"  RMS:          {stats['rms']*1000:.2f} mW")
print(f"  Std Dev:      {stats['std']*1000:.2f} mW")
print(f"  Total Energy: {stats['energy']*1e6:.2f} µJ")
```

**Expected Output**:

```
Power Statistics:
  Average:      125.50 mW
  Peak:         250.00 mW
  Minimum:      50.00 mW
  RMS:          135.23 mW
  Std Dev:      45.67 mW
  Total Energy: 1255.00 µJ
```

#### Power vs. Time Visualization

```python
import tracekit as tk
import matplotlib.pyplot as plt

# Calculate power waveform
power = tk.instantaneous_power(v_supply, i_supply)

# Create time axis
sample_rate = power.metadata.sample_rate
time = np.arange(len(power.data)) / sample_rate

# Plot power over time
plt.figure(figsize=(12, 6))
plt.subplot(3, 1, 1)
plt.plot(time * 1e3, v_supply.data)
plt.ylabel('Voltage (V)')
plt.title('DC Power Analysis')
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(time * 1e3, i_supply.data * 1e3)
plt.ylabel('Current (mA)')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(time * 1e3, power.data * 1000)
plt.axhline(tk.average_power(power) * 1000, color='r',
            linestyle='--', label=f'Average: {tk.average_power(power)*1000:.2f} mW')
plt.ylabel('Power (mW)')
plt.xlabel('Time (ms)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('dc_power_analysis.png', dpi=300)
plt.show()
```

### AC Power Measurements

AC power analysis involves measuring real power (P), apparent power (S), reactive power (Q), and power factor (PF).

#### Single-Phase AC Power

**Scenario**: Measure power consumption of 120V AC resistive load

```python
import tracekit as tk
import numpy as np

# Load AC voltage and current
v_ac = tk.load("ac_voltage_120v.wfm")
i_ac = tk.load("ac_current.wfm")

# Calculate all AC power quantities
p_real = tk.average_power(voltage=v_ac, current=i_ac)
s_apparent = tk.apparent_power(v_ac, i_ac)
q_reactive = tk.reactive_power(v_ac, i_ac)
pf = tk.power_factor(v_ac, i_ac)

print(f"AC Power Analysis (Single Phase):")
print(f"  Real Power (P):      {p_real:.2f} W")
print(f"  Apparent Power (S):  {s_apparent:.2f} VA")
print(f"  Reactive Power (Q):  {q_reactive:.2f} VAR")
print(f"  Power Factor:        {pf:.3f}")
print(f"  Phase Angle:         {np.degrees(np.arccos(pf)):.1f}°")

# Verify power triangle: S² = P² + Q²
s_calculated = np.sqrt(p_real**2 + q_reactive**2)
print(f"\nVerification:")
print(f"  S (measured):    {s_apparent:.2f} VA")
print(f"  S (calculated):  {s_calculated:.2f} VA")
print(f"  Error:           {abs(s_apparent-s_calculated)/s_apparent*100:.2f}%")
```

**Expected Output**:

```
AC Power Analysis (Single Phase):
  Real Power (P):      100.00 W
  Apparent Power (S):  100.00 VA
  Reactive Power (Q):  0.00 VAR
  Power Factor:        1.000
  Phase Angle:         0.0°

Verification:
  S (measured):    100.00 VA
  S (calculated):  100.00 VA
  Error:           0.00%
```

#### Inductive Load (Motor)

```python
import tracekit as tk
import numpy as np

# Load motor measurements
v_motor = tk.load("motor_voltage.wfm")
i_motor = tk.load("motor_current.wfm")

# Calculate power quantities
p = tk.average_power(voltage=v_motor, current=i_motor)
s = tk.apparent_power(v_motor, i_motor)
q = tk.reactive_power(v_motor, i_motor)
pf = tk.power_factor(v_motor, i_motor)

print(f"Inductive Load (Motor) Analysis:")
print(f"  Real Power:      {p:.2f} W")
print(f"  Apparent Power:  {s:.2f} VA")
print(f"  Reactive Power:  {q:.2f} VAR (inductive)")
print(f"  Power Factor:    {pf:.3f} lagging")

# Determine load characteristics
if q > 0:
    print(f"  Load Type:       Inductive (current lags voltage)")
    phase_angle = np.degrees(np.arcsin(q/s))
    print(f"  Phase Angle:     {phase_angle:.1f}° lagging")

# Calculate reactive power compensation needed
target_pf = 0.95
if pf < target_pf:
    q_compensation = p * (np.tan(np.arccos(pf)) - np.tan(np.arccos(target_pf)))
    print(f"\nPower Factor Correction:")
    print(f"  Target PF:           {target_pf:.3f}")
    print(f"  Required correction: {q_compensation:.2f} VAR")

    # Calculate capacitor size (60 Hz)
    v_rms = tk.rms(v_motor)
    capacitance = q_compensation / (2 * np.pi * 60 * v_rms**2)
    print(f"  Capacitor size:      {capacitance*1e6:.1f} µF @ {v_rms:.0f}V RMS")
```

**Expected Output**:

```
Inductive Load (Motor) Analysis:
  Real Power:      500.00 W
  Apparent Power:  714.29 VA
  Reactive Power:  500.00 VAR (inductive)
  Power Factor:    0.700 lagging
  Load Type:       Inductive (current lags voltage)
  Phase Angle:     45.0° lagging

Power Factor Correction:
  Target PF:           0.950
  Required correction: 328.59 VAR
  Capacitor size:      45.6 µF @ 120V RMS
```

#### Visualizing AC Power - Lissajous Curve

```python
import tracekit as tk
import matplotlib.pyplot as plt

# Load AC measurements
v_ac = tk.load("ac_voltage.wfm")
i_ac = tk.load("ac_current.wfm")

# Create Lissajous figure (V-I curve)
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.plot(v_ac.data, i_ac.data, linewidth=0.5)
plt.xlabel('Voltage (V)')
plt.ylabel('Current (A)')
plt.title('Lissajous Curve (V-I)')
plt.grid(True)
plt.axis('equal')

# Interpret shape
pf = tk.power_factor(v_ac, i_ac)
if abs(pf - 1.0) < 0.05:
    shape = "Linear (Resistive)"
elif pf > 0.9:
    shape = "Narrow ellipse (Mostly resistive)"
else:
    shape = "Wide ellipse (Reactive)"
plt.text(0.05, 0.95, f'PF={pf:.3f}\n{shape}',
         transform=plt.gca().transAxes, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Plot V and I over time
sample_rate = v_ac.metadata.sample_rate
time = np.arange(len(v_ac.data)) / sample_rate

plt.subplot(1, 2, 2)
plt.plot(time * 1e3, v_ac.data, label='Voltage', alpha=0.7)
plt.plot(time * 1e3, i_ac.data * 50, label='Current (×50)', alpha=0.7)
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude')
plt.title('Voltage and Current Waveforms')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('ac_power_lissajous.png', dpi=300)
plt.show()
```

### Power Factor Analysis

Power factor indicates how effectively electrical power is being converted to useful work output.

#### Measuring Power Factor

```python
import tracekit as tk
import numpy as np

# Load measurements
v = tk.load("line_voltage.wfm")
i = tk.load("line_current.wfm")

# Calculate power factor
pf = tk.power_factor(v, i)
print(f"Power Factor: {pf:.3f}")

# Interpret results
if pf >= 0.95:
    rating = "Excellent"
elif pf >= 0.85:
    rating = "Good"
elif pf >= 0.70:
    rating = "Fair - consider correction"
else:
    rating = "Poor - correction recommended"

print(f"Rating: {rating}")

# Calculate displacement power factor (for sinusoidal waveforms)
p = tk.average_power(voltage=v, current=i)
s = tk.apparent_power(v, i)
dpf = p / s  # Displacement power factor
print(f"Displacement PF: {dpf:.3f}")

# Calculate distortion power factor (accounts for harmonics)
# DPF = PF / cos(φ)
# If DPF ≈ PF, waveforms are sinusoidal
# If DPF < PF, harmonics present

# Calculate true power factor
v_rms = tk.rms(v)
i_rms = tk.rms(i)
v_fund_rms = tk.rms(tk.bandpass(v, 55, 65))  # 60 Hz fundamental
i_fund_rms = tk.rms(tk.bandpass(i, 55, 65))

distortion_factor_v = v_fund_rms / v_rms
distortion_factor_i = i_fund_rms / i_rms
print(f"\nHarmonic Content:")
print(f"  Voltage distortion: {(1-distortion_factor_v)*100:.2f}%")
print(f"  Current distortion: {(1-distortion_factor_i)*100:.2f}%")
```

**Expected Output**:

```
Power Factor: 0.850
Rating: Good
Displacement PF: 0.850

Harmonic Content:
  Voltage distortion: 2.50%
  Current distortion: 15.30%
```

### Efficiency Calculations

Efficiency is the ratio of useful output power to input power, representing power conversion effectiveness.

#### Basic Efficiency Measurement

**Scenario**: DC-DC buck converter efficiency

```python
import tracekit as tk

# Load input and output measurements
v_in = tk.load("buck_input_voltage.wfm")
i_in = tk.load("buck_input_current.wfm")
v_out = tk.load("buck_output_voltage.wfm")
i_out = tk.load("buck_output_current.wfm")

# Calculate efficiency
eta = tk.efficiency(v_in, i_in, v_out, i_out)
print(f"Efficiency: {eta*100:.2f}%")

# Calculate power budget
p_in = tk.average_power(voltage=v_in, current=i_in)
p_out = tk.average_power(voltage=v_out, current=i_out)
p_loss = p_in - p_out

print(f"\nPower Budget:")
print(f"  Input Power:  {p_in:.3f} W")
print(f"  Output Power: {p_out:.3f} W")
print(f"  Losses:       {p_loss:.3f} W ({p_loss/p_in*100:.2f}%)")

# Calculate output voltage and current
v_out_avg = tk.mean(v_out)
i_out_avg = tk.mean(i_out)
print(f"\nOperating Point:")
print(f"  Input:  {tk.mean(v_in):.2f} V @ {tk.mean(i_in)*1e3:.2f} mA")
print(f"  Output: {v_out_avg:.2f} V @ {i_out_avg*1e3:.2f} mA")
```

**Expected Output**:

```
Efficiency: 92.50%

Power Budget:
  Input Power:  5.000 W
  Output Power: 4.625 W
  Losses:       0.375 W (7.50%)

Operating Point:
  Input:  12.00 V @ 416.67 mA
  Output: 5.00 V @ 925.00 mA
```

#### Efficiency vs. Load Curve

```python
import tracekit as tk
import matplotlib.pyplot as plt

# Test at different load currents
load_currents = [0.1, 0.2, 0.5, 1.0, 2.0, 3.0]  # Amperes
efficiencies = []
output_powers = []

for i_load in load_currents:
    # Load measurements at this current
    v_in = tk.load(f"measurements/vin_{i_load}A.wfm")
    i_in = tk.load(f"measurements/iin_{i_load}A.wfm")
    v_out = tk.load(f"measurements/vout_{i_load}A.wfm")
    i_out = tk.load(f"measurements/iout_{i_load}A.wfm")

    # Calculate efficiency
    eta = tk.efficiency(v_in, i_in, v_out, i_out)
    p_out = tk.average_power(voltage=v_out, current=i_out)

    efficiencies.append(eta * 100)
    output_powers.append(p_out)

    print(f"Load: {i_load:.1f} A, Efficiency: {eta*100:.2f}%, Output: {p_out:.2f} W")

# Plot efficiency curve
plt.figure(figsize=(10, 6))
plt.plot(output_powers, efficiencies, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Output Power (W)')
plt.ylabel('Efficiency (%)')
plt.title('DC-DC Converter Efficiency vs. Load')
plt.grid(True)
plt.axhline(80, color='r', linestyle='--', alpha=0.5, label='80% threshold')
plt.legend()
plt.tight_layout()
plt.savefig('efficiency_curve.png', dpi=300)
plt.show()

# Find peak efficiency
peak_idx = np.argmax(efficiencies)
print(f"\nPeak Efficiency: {efficiencies[peak_idx]:.2f}% at {output_powers[peak_idx]:.2f} W")
```

**Expected Output**:

```
Load: 0.1 A, Efficiency: 85.50%, Output: 0.50 W
Load: 0.2 A, Efficiency: 89.20%, Output: 1.00 W
Load: 0.5 A, Efficiency: 92.50%, Output: 2.50 W
Load: 1.0 A, Efficiency: 93.80%, Output: 5.00 W
Load: 2.0 A, Efficiency: 93.20%, Output: 10.00 W
Load: 3.0 A, Efficiency: 91.50%, Output: 15.00 W

Peak Efficiency: 93.80% at 5.00 W
```

## Advanced Topics

### Switching Regulator Analysis

Switching regulators (buck, boost, buck-boost) require specialized analysis due to their pulsed nature.

#### Complete Buck Converter Characterization

**Scenario**: Characterize 12V to 5V buck converter at 500 kHz switching frequency

```python
import tracekit as tk
import numpy as np
import matplotlib.pyplot as plt

# Load all measurement points
v_in = tk.load("buck_vin.wfm")
i_in = tk.load("buck_iin.wfm")
v_out = tk.load("buck_vout.wfm")
i_out = tk.load("buck_iout.wfm")
v_sw = tk.load("buck_switch_node.wfm")  # Switch node voltage

print("=== Buck Converter Analysis ===\n")

# 1. Input Power Analysis
p_in = tk.average_power(voltage=v_in, current=i_in)
print(f"Input Power: {p_in:.3f} W")

# Input current ripple
i_in_ripple_pp, i_in_ripple_rms = tk.ripple(i_in)
print(f"Input Current Ripple: {i_in_ripple_pp*1e3:.2f} mA pk-pk, {i_in_ripple_rms*1e3:.2f} mA RMS")

# 2. Output Power Analysis
p_out = tk.average_power(voltage=v_out, current=i_out)
print(f"\nOutput Power: {p_out:.3f} W")

# Output voltage ripple
v_out_stats = tk.ripple_statistics(v_out)
print(f"Output Voltage: {v_out_stats['dc_level']:.4f} V")
print(f"Output Ripple: {v_out_stats['ripple_pp']*1e3:.2f} mV pk-pk ({v_out_stats['ripple_pp_percent']:.3f}%)")
print(f"Output Ripple (RMS): {v_out_stats['ripple_rms']*1e3:.2f} mV")
print(f"Ripple Frequency: {v_out_stats['ripple_frequency']/1e3:.1f} kHz")

# 3. Efficiency
eta = tk.efficiency(v_in, i_in, v_out, i_out)
losses = p_in - p_out
print(f"\nEfficiency: {eta*100:.2f}%")
print(f"Power Loss: {losses:.3f} W ({losses/p_in*100:.2f}%)")

# 4. Switching Analysis
# Extract switching period and duty cycle from switch node
freq = tk.frequency(v_sw)
duty = tk.duty_cycle(v_sw)
print(f"\nSwitching Frequency: {freq/1e3:.1f} kHz")
print(f"Duty Cycle: {duty*100:.2f}%")

# Theoretical duty cycle for buck converter: D = V_out / V_in
duty_theoretical = v_out_stats['dc_level'] / tk.mean(v_in)
print(f"Theoretical Duty Cycle: {duty_theoretical*100:.2f}%")
print(f"Duty Cycle Error: {abs(duty-duty_theoretical)*100:.2f}%")

# 5. Ripple Current Analysis
i_out_ripple_pp, i_out_ripple_rms = tk.ripple(i_out)
print(f"\nOutput Current Ripple: {i_out_ripple_pp*1e3:.2f} mA pk-pk")

# Calculate theoretical ripple current
# ΔI_L = (V_in - V_out) × D / (L × f_sw)
# Assuming inductance L = 22 µH
L = 22e-6  # Henry
v_in_avg = tk.mean(v_in)
v_out_avg = v_out_stats['dc_level']
i_ripple_theoretical = (v_in_avg - v_out_avg) * duty / (L * freq)
print(f"Theoretical Ripple: {i_ripple_theoretical*1e3:.2f} mA pk-pk")
print(f"Measured/Theoretical: {i_out_ripple_pp/i_ripple_theoretical:.2f}")

# 6. Component Stress Analysis
print(f"\n=== Component Stress ===")
v_sw_max = np.max(v_sw.data)
v_sw_min = np.min(v_sw.data)
print(f"Switch Node Max: {v_sw_max:.2f} V")
print(f"Switch Node Min: {v_sw_min:.2f} V")

# Calculate switching losses (simplified)
# E_sw = 0.5 × V × I × (t_rise + t_fall)
rise_time = tk.rise_time(v_sw)
fall_time = tk.fall_time(v_sw)
i_out_avg = tk.mean(i_out)
e_switching = 0.5 * v_in_avg * i_out_avg * (rise_time + fall_time) * freq
p_switching = e_switching * freq
print(f"\nRise Time: {rise_time*1e9:.1f} ns")
print(f"Fall Time: {fall_time*1e9:.1f} ns")
print(f"Estimated Switching Loss: {p_switching:.3f} W")

# Conduction losses
# P_cond = I_rms² × R_ds_on (assume R_ds_on = 50 mΩ)
r_ds_on = 0.050  # Ohms
i_out_rms = tk.rms(i_out)
p_conduction = i_out_rms**2 * r_ds_on * duty
print(f"Estimated Conduction Loss: {p_conduction:.3f} W")
print(f"Total Estimated Loss: {p_switching + p_conduction:.3f} W")
print(f"Measured Loss: {losses:.3f} W")
```

**Expected Output**:

```
=== Buck Converter Analysis ===

Input Power: 5.405 W
Input Current Ripple: 125.30 mA pk-pk, 36.20 mA RMS

Output Power: 5.000 W
Output Voltage: 5.0000 V
Output Ripple: 50.00 mV pk-pk (1.000%)
Output Ripple (RMS): 14.43 mV
Ripple Frequency: 500.0 kHz

Efficiency: 92.50%
Power Loss: 0.405 W (7.50%)

Switching Frequency: 500.0 kHz
Duty Cycle: 41.67%
Theoretical Duty Cycle: 41.67%
Duty Cycle Error: 0.00%

Output Current Ripple: 450.00 mA pk-pk
Theoretical Ripple: 454.55 mA pk-pk
Measured/Theoretical: 0.99

=== Component Stress ===
Switch Node Max: 12.50 V
Switch Node Min: -0.80 V

Rise Time: 25.0 ns
Fall Time: 20.0 ns
Estimated Switching Loss: 0.225 W
Estimated Conduction Loss: 0.104 W
Total Estimated Loss: 0.329 W
Measured Loss: 0.405 W
```

#### Visualizing Switching Waveforms

```python
import tracekit as tk
import matplotlib.pyplot as plt

# Load measurements
v_in = tk.load("buck_vin.wfm")
v_out = tk.load("buck_vout.wfm")
i_out = tk.load("buck_iout.wfm")
v_sw = tk.load("buck_switch_node.wfm")

# Create time axis (zoom to a few switching cycles)
sample_rate = v_sw.metadata.sample_rate
time = np.arange(len(v_sw.data)) / sample_rate

# Find a few switching cycles to display
freq = tk.frequency(v_sw)
period = 1 / freq
n_periods = 3
start_idx = len(time) // 2  # Start from middle
end_idx = start_idx + int(n_periods * period * sample_rate)

time_zoom = time[start_idx:end_idx] * 1e6  # Convert to µs
time_zoom = time_zoom - time_zoom[0]  # Start from zero

# Plot switching waveforms
fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)

# Switch node voltage
axes[0].plot(time_zoom, v_sw.data[start_idx:end_idx], 'b-', linewidth=1.5)
axes[0].set_ylabel('V_SW (V)')
axes[0].set_title('Buck Converter Switching Waveforms')
axes[0].grid(True, alpha=0.3)
axes[0].axhline(0, color='k', linewidth=0.5)

# Input voltage
axes[1].plot(time_zoom, v_in.data[start_idx:end_idx], 'g-', linewidth=1.5)
axes[1].set_ylabel('V_IN (V)')
axes[1].grid(True, alpha=0.3)

# Output voltage (zoomed to show ripple)
v_out_mean = tk.mean(v_out)
axes[2].plot(time_zoom, (v_out.data[start_idx:end_idx] - v_out_mean) * 1000, 'r-', linewidth=1.5)
axes[2].set_ylabel('V_OUT ripple (mV)')
axes[2].grid(True, alpha=0.3)
axes[2].axhline(0, color='k', linewidth=0.5, linestyle='--')

# Output current
axes[3].plot(time_zoom, i_out.data[start_idx:end_idx] * 1000, 'm-', linewidth=1.5)
axes[3].set_ylabel('I_OUT (mA)')
axes[3].set_xlabel('Time (µs)')
axes[3].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('buck_converter_waveforms.png', dpi=300)
plt.show()
```

### Battery Discharge Characterization

Battery characterization involves measuring voltage, current, and energy over the discharge curve.

#### Complete Battery Discharge Profile

**Scenario**: Characterize 3.7V Li-ion battery discharge

```python
import tracekit as tk
import numpy as np
import matplotlib.pyplot as plt

# Load long-duration battery measurement
v_batt = tk.load("battery_voltage_discharge.wfm")
i_batt = tk.load("battery_current_discharge.wfm")

print("=== Battery Discharge Analysis ===\n")

# Calculate total energy discharged
e_total = tk.energy(voltage=v_batt, current=i_batt)
e_wh = e_total / 3600  # Convert J to Wh
print(f"Total Energy Discharged: {e_total:.2f} J ({e_wh:.3f} Wh)")

# Calculate capacity in mAh
# Q = ∫ I dt
sample_rate = i_batt.metadata.sample_rate
dt = 1 / sample_rate
capacity_as = np.trapz(i_batt.data, dx=dt)  # Ampere-seconds
capacity_ah = capacity_as / 3600
capacity_mah = capacity_ah * 1000
print(f"Capacity: {capacity_mah:.1f} mAh")

# Calculate average voltage during discharge
v_avg = tk.mean(v_batt)
print(f"Average Voltage: {v_avg:.3f} V")

# Calculate discharge duration
duration = len(v_batt.data) / sample_rate
print(f"Discharge Duration: {duration/3600:.2f} hours ({duration/60:.1f} minutes)")

# Calculate C-rate
# C-rate = I / Q (assuming 2000 mAh battery)
nominal_capacity = 2000  # mAh
i_avg = tk.mean(i_batt)
c_rate = (i_avg * 1000) / nominal_capacity
print(f"Average Current: {i_avg*1000:.2f} mA")
print(f"C-rate: {c_rate:.2f}C")

# Analyze voltage drop
v_initial = np.mean(v_batt.data[:100])  # First 100 samples
v_final = np.mean(v_batt.data[-100:])   # Last 100 samples
v_drop = v_initial - v_final
print(f"\nVoltage Drop:")
print(f"  Initial: {v_initial:.3f} V")
print(f"  Final:   {v_final:.3f} V")
print(f"  Drop:    {v_drop:.3f} V ({v_drop/v_initial*100:.1f}%)")

# Calculate internal resistance (from voltage sag)
# When load changes, ΔV = I × R_internal
# Simplified: use initial voltage drop
r_internal = v_drop / i_avg
print(f"Estimated Internal Resistance: {r_internal*1000:.0f} mΩ")

# Power analysis over discharge
power = tk.instantaneous_power(v_batt, i_batt)
power_stats = tk.power_statistics(power)
print(f"\nPower Statistics:")
print(f"  Average: {power_stats['average']:.3f} W")
print(f"  Peak:    {power_stats['peak']:.3f} W")
print(f"  Minimum: {power_stats['min']:.3f} W")

# Efficiency (energy delivered vs. theoretical)
# Theoretical energy at nominal voltage
e_theoretical = capacity_as * 3.7  # J
efficiency = (e_total / e_theoretical) * 100
print(f"\nEnergy Efficiency: {efficiency:.1f}%")
print(f"  (Compared to nominal 3.7V)")

# Plot discharge curve
time_hours = np.arange(len(v_batt.data)) / sample_rate / 3600

fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

# Voltage vs time
axes[0].plot(time_hours, v_batt.data, 'b-', linewidth=1.5)
axes[0].set_ylabel('Voltage (V)')
axes[0].set_title('Battery Discharge Profile')
axes[0].grid(True, alpha=0.3)
axes[0].axhline(3.0, color='r', linestyle='--', alpha=0.5, label='Cutoff voltage')
axes[0].legend()

# Current vs time
axes[1].plot(time_hours, i_batt.data * 1000, 'g-', linewidth=1.5)
axes[1].set_ylabel('Current (mA)')
axes[1].grid(True, alpha=0.3)

# Cumulative energy vs time
cumulative_energy = np.cumsum(power.data) * dt / 3600  # Wh
axes[2].plot(time_hours, cumulative_energy, 'r-', linewidth=1.5)
axes[2].set_ylabel('Cumulative Energy (Wh)')
axes[2].set_xlabel('Time (hours)')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('battery_discharge_profile.png', dpi=300)
plt.show()
```

**Expected Output**:

```
=== Battery Discharge Analysis ===

Total Energy Discharged: 25920.00 J (7.200 Wh)
Capacity: 2000.0 mAh
Average Voltage: 3.600 V
Discharge Duration: 2.00 hours (120.0 minutes)
Average Current: 1000.00 mA
C-rate: 0.50C

Voltage Drop:
  Initial: 4.100 V
  Final:   3.000 V
  Drop:    1.100 V (26.8%)

Estimated Internal Resistance: 1100 mΩ

Power Statistics:
  Average: 3.600 W
  Peak:    4.100 W
  Minimum: 3.000 W

Energy Efficiency: 95.1%
  (Compared to nominal 3.7V)
```

#### State of Charge (SOC) Estimation

```python
import tracekit as tk
import numpy as np
import matplotlib.pyplot as plt

# Load battery measurement
v_batt = tk.load("battery_voltage.wfm")
i_batt = tk.load("battery_current.wfm")

# Calculate coulomb counting (SOC estimation)
sample_rate = i_batt.metadata.sample_rate
dt = 1 / sample_rate

# Cumulative charge (Coulombs)
charge = np.cumsum(i_batt.data) * dt
charge_ah = charge / 3600  # Ampere-hours

# Assume starting SOC = 100%, capacity = 2000 mAh
initial_capacity_ah = 2.0  # Ah
soc = (1 - charge_ah / initial_capacity_ah) * 100

# Create time axis
time_hours = np.arange(len(soc)) / sample_rate / 3600

# Plot SOC curve
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(time_hours, v_batt.data, 'b-', linewidth=1.5)
plt.ylabel('Battery Voltage (V)')
plt.title('State of Charge (SOC) vs. Voltage')
plt.grid(True, alpha=0.3)

plt.subplot(2, 1, 2)
plt.plot(time_hours, soc, 'g-', linewidth=1.5)
plt.ylabel('SOC (%)')
plt.xlabel('Time (hours)')
plt.axhline(20, color='r', linestyle='--', alpha=0.5, label='Low battery (20%)')
plt.axhline(10, color='r', linestyle='--', alpha=0.7, label='Critical (10%)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(0, 100)

plt.tight_layout()
plt.savefig('battery_soc.png', dpi=300)
plt.show()

# Create voltage-SOC lookup table
# This can be used for voltage-based SOC estimation
soc_points = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
voltage_points = []

for soc_target in soc_points:
    # Find index closest to this SOC
    idx = np.argmin(np.abs(soc - soc_target))
    voltage_points.append(v_batt.data[idx])

print("\nVoltage-SOC Lookup Table:")
print("SOC (%) | Voltage (V)")
print("--------|------------")
for s, v in zip(soc_points, voltage_points):
    print(f"  {s:3d}   |   {v:.3f}")
```

**Expected Output**:

```
Voltage-SOC Lookup Table:
SOC (%) | Voltage (V)
--------|------------
  100   |   4.100
   90   |   3.950
   80   |   3.850
   70   |   3.770
   60   |   3.720
   50   |   3.680
   40   |   3.640
   30   |   3.590
   20   |   3.520
   10   |   3.400
    0   |   3.000
```

### Motor Power Analysis

Motor power analysis includes mechanical power, electrical power, efficiency, and power factor.

#### Three-Phase Motor Analysis

**Scenario**: Analyze 3-phase induction motor at 480V, 60 Hz

```python
import tracekit as tk
import numpy as np

# Load three-phase measurements
v_a = tk.load("motor_voltage_phase_a.wfm")
i_a = tk.load("motor_current_phase_a.wfm")
v_b = tk.load("motor_voltage_phase_b.wfm")
i_b = tk.load("motor_current_phase_b.wfm")
v_c = tk.load("motor_voltage_phase_c.wfm")
i_c = tk.load("motor_current_phase_c.wfm")

print("=== Three-Phase Motor Analysis ===\n")

# Calculate power per phase
p_a = tk.average_power(voltage=v_a, current=i_a)
p_b = tk.average_power(voltage=v_b, current=i_b)
p_c = tk.average_power(voltage=v_c, current=i_c)
p_total = p_a + p_b + p_c

print(f"Real Power (per phase):")
print(f"  Phase A: {p_a:.2f} W")
print(f"  Phase B: {p_b:.2f} W")
print(f"  Phase C: {p_c:.2f} W")
print(f"  Total:   {p_total:.2f} W ({p_total/1000:.2f} kW)")

# Calculate apparent power per phase
s_a = tk.apparent_power(v_a, i_a)
s_b = tk.apparent_power(v_b, i_b)
s_c = tk.apparent_power(v_c, i_c)
s_total = s_a + s_b + s_c

print(f"\nApparent Power (per phase):")
print(f"  Phase A: {s_a:.2f} VA")
print(f"  Phase B: {s_b:.2f} VA")
print(f"  Phase C: {s_c:.2f} VA")
print(f"  Total:   {s_total:.2f} VA ({s_total/1000:.2f} kVA)")

# Calculate reactive power per phase
q_a = tk.reactive_power(v_a, i_a, frequency=60)
q_b = tk.reactive_power(v_b, i_b, frequency=60)
q_c = tk.reactive_power(v_c, i_c, frequency=60)
q_total = q_a + q_b + q_c

print(f"\nReactive Power (per phase):")
print(f"  Phase A: {q_a:.2f} VAR")
print(f"  Phase B: {q_b:.2f} VAR")
print(f"  Phase C: {q_c:.2f} VAR")
print(f"  Total:   {q_total:.2f} VAR ({q_total/1000:.2f} kVAR)")

# Calculate power factor
pf_a = tk.power_factor(v_a, i_a)
pf_b = tk.power_factor(v_b, i_b)
pf_c = tk.power_factor(v_c, i_c)
pf_total = p_total / s_total

print(f"\nPower Factor:")
print(f"  Phase A: {pf_a:.3f}")
print(f"  Phase B: {pf_b:.3f}")
print(f"  Phase C: {pf_c:.3f}")
print(f"  Overall: {pf_total:.3f}")

# Phase imbalance check
p_avg = (p_a + p_b + p_c) / 3
p_imbalance = max(abs(p_a - p_avg), abs(p_b - p_avg), abs(p_c - p_avg)) / p_avg * 100
print(f"\nPhase Imbalance: {p_imbalance:.2f}%")

if p_imbalance > 10:
    print("WARNING: Phase imbalance exceeds 10% - check connections!")

# Calculate line voltages (for wye or delta connection)
v_ab = v_a.data - v_b.data
v_bc = v_b.data - v_c.data
v_ca = v_c.data - v_a.data

v_ab_rms = np.sqrt(np.mean(v_ab**2))
v_bc_rms = np.sqrt(np.mean(v_bc**2))
v_ca_rms = np.sqrt(np.mean(v_ca**2))

print(f"\nLine-to-Line Voltages:")
print(f"  V_AB: {v_ab_rms:.1f} V")
print(f"  V_BC: {v_bc_rms:.1f} V")
print(f"  V_CA: {v_ca_rms:.1f} V")

# Estimate motor efficiency (if mechanical power known)
# For this example, assume rated mechanical output = 5 HP = 3730 W
p_mechanical = 3730  # Watts (5 HP)
eta_motor = (p_mechanical / p_total) * 100
print(f"\nMotor Efficiency:")
print(f"  Electrical Input: {p_total:.0f} W")
print(f"  Mechanical Output: {p_mechanical:.0f} W")
print(f"  Efficiency: {eta_motor:.1f}%")
print(f"  Losses: {p_total - p_mechanical:.0f} W")
```

**Expected Output**:

```
=== Three-Phase Motor Analysis ===

Real Power (per phase):
  Phase A: 1400.00 W
  Phase B: 1390.00 W
  Phase C: 1410.00 W
  Total:   4200.00 W (4.20 kW)

Apparent Power (per phase):
  Phase A: 1750.00 VA
  Phase B: 1740.00 VA
  Phase C: 1760.00 VA
  Total:   5250.00 VA (5.25 kVA)

Reactive Power (per phase):
  Phase A: 1092.00 VAR
  Phase B: 1085.00 VAR
  Phase C: 1098.00 VAR
  Total:   3275.00 VAR (3.27 kVAR)

Power Factor:
  Phase A: 0.800
  Phase B: 0.799
  Phase C: 0.801
  Overall: 0.800

Phase Imbalance: 0.72%

Line-to-Line Voltages:
  V_AB: 480.0 V
  V_BC: 480.0 V
  V_CA: 480.0 V

Motor Efficiency:
  Electrical Input: 4200 W
  Mechanical Output: 3730 W
  Efficiency: 88.8%
  Losses: 470 W
```

### Solar Panel MPPT Analysis

Maximum Power Point Tracking (MPPT) analysis characterizes solar panel performance and MPPT algorithm effectiveness.

#### I-V Curve Characterization

**Scenario**: Sweep solar panel from short-circuit to open-circuit and find maximum power point

```python
import tracekit as tk
import numpy as np
import matplotlib.pyplot as plt

# Load voltage and current during I-V sweep
v_panel = tk.load("solar_panel_voltage.wfm")
i_panel = tk.load("solar_panel_current.wfm")

print("=== Solar Panel I-V Curve Analysis ===\n")

# Calculate power at each point
power = tk.instantaneous_power(v_panel, i_panel)

# Find maximum power point
mpp_idx = np.argmax(power.data)
v_mpp = v_panel.data[mpp_idx]
i_mpp = i_panel.data[mpp_idx]
p_mpp = power.data[mpp_idx]

print(f"Maximum Power Point (MPP):")
print(f"  Voltage:  {v_mpp:.3f} V")
print(f"  Current:  {i_mpp:.3f} A")
print(f"  Power:    {p_mpp:.3f} W")

# Find open-circuit voltage (V_oc)
v_oc = np.max(v_panel.data)
print(f"\nOpen-Circuit Voltage (V_oc): {v_oc:.3f} V")

# Find short-circuit current (I_sc)
i_sc = np.max(i_panel.data)
print(f"Short-Circuit Current (I_sc): {i_sc:.3f} A")

# Calculate fill factor
# FF = (V_mpp × I_mpp) / (V_oc × I_sc)
fill_factor = p_mpp / (v_oc * i_sc)
print(f"\nFill Factor: {fill_factor:.3f}")

# Typical FF for crystalline silicon: 0.75-0.85
if fill_factor > 0.75:
    print("Good fill factor (healthy panel)")
else:
    print("Low fill factor (possible degradation or shading)")

# Calculate panel efficiency (if area known)
# Efficiency = P_mpp / (Irradiance × Area)
# Assume: Irradiance = 1000 W/m² (STC), Area = 1.6 m²
irradiance = 1000  # W/m²
area = 1.6  # m²
efficiency = (p_mpp / (irradiance * area)) * 100
print(f"\nPanel Efficiency: {efficiency:.2f}%")
print(f"  (at 1000 W/m², {area} m²)")

# Plot I-V and P-V curves
fig, axes = plt.subplots(2, 1, figsize=(10, 10))

# I-V curve
axes[0].plot(v_panel.data, i_panel.data, 'b-', linewidth=2)
axes[0].plot(v_mpp, i_mpp, 'ro', markersize=10, label=f'MPP: {v_mpp:.2f}V, {i_mpp:.2f}A')
axes[0].axhline(i_sc, color='g', linestyle='--', alpha=0.5, label=f'I_sc = {i_sc:.2f}A')
axes[0].axvline(v_oc, color='r', linestyle='--', alpha=0.5, label=f'V_oc = {v_oc:.2f}V')
axes[0].set_xlabel('Voltage (V)')
axes[0].set_ylabel('Current (A)')
axes[0].set_title('Solar Panel I-V Curve')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# P-V curve
axes[1].plot(v_panel.data, power.data, 'r-', linewidth=2)
axes[1].plot(v_mpp, p_mpp, 'ro', markersize=10, label=f'MPP: {p_mpp:.2f}W')
axes[1].axvline(v_mpp, color='g', linestyle='--', alpha=0.5)
axes[1].set_xlabel('Voltage (V)')
axes[1].set_ylabel('Power (W)')
axes[1].set_title('Solar Panel P-V Curve')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('solar_panel_curves.png', dpi=300)
plt.show()
```

**Expected Output**:

```
=== Solar Panel I-V Curve Analysis ===

Maximum Power Point (MPP):
  Voltage:  30.500 V
  Current:  8.200 A
  Power:    250.100 W

Open-Circuit Voltage (V_oc): 37.200 V
Short-Circuit Current (I_sc): 8.900 A

Fill Factor: 0.755
Good fill factor (healthy panel)

Panel Efficiency: 15.63%
  (at 1000 W/m², 1.6 m²)
```

#### MPPT Algorithm Performance

```python
import tracekit as tk
import numpy as np
import matplotlib.pyplot as plt

# Load MPPT controller measurements over time
v_panel = tk.load("mppt_panel_voltage.wfm")
i_panel = tk.load("mppt_panel_current.wfm")
v_battery = tk.load("mppt_battery_voltage.wfm")
i_battery = tk.load("mppt_battery_current.wfm")

print("=== MPPT Controller Performance ===\n")

# Calculate input and output power
p_input = tk.instantaneous_power(v_panel, i_panel)
p_output = tk.instantaneous_power(v_battery, i_battery)

# Calculate MPPT efficiency
eta_mppt = tk.efficiency(v_panel, i_panel, v_battery, i_battery)
print(f"MPPT Efficiency: {eta_mppt*100:.2f}%")

# Calculate average powers
p_in_avg = tk.average_power(p_input)
p_out_avg = tk.average_power(p_output)
print(f"Average Input Power:  {p_in_avg:.2f} W")
print(f"Average Output Power: {p_out_avg:.2f} W")
print(f"Power Loss: {p_in_avg - p_out_avg:.2f} W")

# Analyze MPPT tracking
# Good MPPT should keep voltage near MPP voltage (typically ~80% of V_oc)
v_oc_estimated = 37.2  # From previous I-V curve
v_mpp_ideal = 0.80 * v_oc_estimated
v_panel_avg = tk.mean(v_panel)
v_tracking_error = abs(v_panel_avg - v_mpp_ideal)

print(f"\nMPPT Tracking:")
print(f"  Ideal MPP Voltage:   {v_mpp_ideal:.2f} V")
print(f"  Actual Avg Voltage:  {v_panel_avg:.2f} V")
print(f"  Tracking Error:      {v_tracking_error:.2f} V ({v_tracking_error/v_mpp_ideal*100:.1f}%)")

# Analyze MPPT oscillations
v_panel_ripple_pp, v_panel_ripple_rms = tk.ripple(v_panel)
print(f"  Voltage Ripple:      {v_panel_ripple_pp:.3f} V pk-pk")

# Calculate energy harvested
e_harvested = tk.energy(p_output)
sample_rate = p_output.metadata.sample_rate
duration = len(p_output.data) / sample_rate
print(f"\nEnergy Harvested: {e_harvested:.2f} J ({e_harvested/3600:.4f} Wh)")
print(f"Duration: {duration:.1f} s")

# Plot MPPT operation
time = np.arange(len(v_panel.data)) / sample_rate

fig, axes = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

axes[0].plot(time, v_panel.data, 'b-', linewidth=1)
axes[0].axhline(v_mpp_ideal, color='r', linestyle='--', label=f'Ideal MPP: {v_mpp_ideal:.1f}V')
axes[0].set_ylabel('Panel Voltage (V)')
axes[0].set_title('MPPT Controller Operation')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(time, i_panel.data, 'g-', linewidth=1)
axes[1].set_ylabel('Panel Current (A)')
axes[1].grid(True, alpha=0.3)

axes[2].plot(time, p_input.data, 'r-', linewidth=1, label='Input')
axes[2].plot(time, p_output.data, 'b-', linewidth=1, label='Output')
axes[2].set_ylabel('Power (W)')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

axes[3].plot(time, v_battery.data, 'm-', linewidth=1)
axes[3].set_ylabel('Battery Voltage (V)')
axes[3].set_xlabel('Time (s)')
axes[3].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('mppt_operation.png', dpi=300)
plt.show()
```

**Expected Output**:

```
=== MPPT Controller Performance ===

MPPT Efficiency: 96.50%
Average Input Power:  248.50 W
Average Output Power: 239.80 W
Power Loss: 8.70 W

MPPT Tracking:
  Ideal MPP Voltage:   29.76 V
  Actual Avg Voltage:  30.20 V
  Tracking Error:      0.44 V (1.5%)
  Voltage Ripple:      1.250 V pk-pk

Energy Harvested: 23980.00 J (6.6611 Wh)
Duration: 100.0 s
```

## Best Practices

### Probe Selection and Placement

#### Voltage Probe Guidelines

```python
# Bandwidth rule: 5× highest frequency
f_max = 1e6  # 1 MHz signal
bw_required = 5 * f_max
print(f"Minimum probe bandwidth: {bw_required/1e6:.1f} MHz")

# Attenuation selection
# 1:1 for low voltage (<10V), low noise
# 10:1 for general purpose (10-500V)
# 100:1 for high voltage (>500V)

# Input capacitance affects loading
# Lower is better for high-Z sources
c_probe = 10e-12  # 10 pF typical
r_source = 1e6    # 1 MΩ source
tau = r_source * c_probe
f_3db = 1 / (2 * np.pi * tau)
print(f"Probe loading -3dB point: {f_3db/1e3:.1f} kHz")
```

#### Current Probe Guidelines

**Hall Effect Probe**

- DC to ~100 MHz bandwidth
- Non-invasive (clamp-on)
- May have DC drift - periodically zero
- Lower accuracy than shunt (~1-3%)

**Shunt Resistor**

- DC to >1 GHz bandwidth
- Highest accuracy (~0.1%)
- Introduces voltage drop
- Power dissipation consideration

**Rogowski Coil**

- AC only (no DC response)
- Very high bandwidth
- Flexible, non-invasive
- Good for high current (kA range)

### Grounding and Noise Reduction

#### Single-Point Grounding

```python
"""
Best Practice: Connect all grounds at a single point

        Equipment 1      Equipment 2      Equipment 3
             |               |               |
        Ground Wire     Ground Wire     Ground Wire
             |               |               |
             └───────────────┴───────────────┘
                             |
                        Single Point
                             |
                         Earth Ground

Avoids multiple current paths and ground loops.
"""
```

#### Common Mode Noise Rejection

```python
import tracekit as tk
import numpy as np

# Use differential measurement for best noise rejection
v_diff = tk.load("differential_voltage.wfm")

# Compare to single-ended measurement
v_single = tk.load("single_ended_voltage.wfm")

# Calculate common mode rejection improvement
noise_single = np.std(v_single.data)
noise_diff = np.std(v_diff.data)
rejection_db = 20 * np.log10(noise_single / noise_diff)

print(f"Single-ended noise: {noise_single*1e3:.2f} mV RMS")
print(f"Differential noise: {noise_diff*1e3:.2f} mV RMS")
print(f"CMRR improvement: {rejection_db:.1f} dB")
```

### Sample Rate Selection

#### Determining Adequate Sample Rate

```python
import tracekit as tk
import numpy as np

def check_sample_rate(trace, f_signal):
    """Check if sample rate is adequate for signal frequency."""
    sample_rate = trace.metadata.sample_rate

    # Nyquist criterion: f_s > 2 × f_max
    nyquist_rate = 2 * f_signal

    # Recommended: 10× for accurate waveform reconstruction
    recommended_rate = 10 * f_signal

    print(f"Signal Frequency: {f_signal/1e6:.2f} MHz")
    print(f"Sample Rate: {sample_rate/1e6:.2f} MS/s")
    print(f"Nyquist Rate: {nyquist_rate/1e6:.2f} MS/s")
    print(f"Recommended Rate: {recommended_rate/1e6:.2f} MS/s")

    if sample_rate < nyquist_rate:
        print("❌ ALIASING RISK - Increase sample rate!")
        return False
    elif sample_rate < recommended_rate:
        print("⚠️  Sample rate adequate but not optimal")
        return True
    else:
        print("✓ Sample rate is adequate")
        return True

# Example usage
trace = tk.load("switching_regulator.wfm")
f_switching = 500e3  # 500 kHz
check_sample_rate(trace, f_switching)
```

### Common Pitfalls

#### 1. Ground Loops

**Problem**: Multiple ground connections create noise currents

**Solution**:

```python
# Use differential probes for floating measurements
# Connect oscilloscope and DUT grounds at single point
# Use isolated power supplies when possible
```

#### 2. Probe Loading

**Problem**: Probe input capacitance distorts signal

**Solution**:

```python
# Use active probes for high-impedance sources
# Keep probe ground leads short
# Use 10:1 probe to reduce loading by 10×
```

#### 3. Insufficient Sample Rate

**Problem**: Aliasing distorts high-frequency components

**Solution**:

```python
import tracekit as tk

# Always verify sample rate
trace = tk.load("signal.wfm")
f_signal = tk.frequency(trace)
f_sample = trace.metadata.sample_rate

if f_sample < 10 * f_signal:
    print(f"WARNING: Sample rate ({f_sample/1e6:.1f} MS/s) may be too low")
    print(f"Recommended: ≥{10*f_signal/1e6:.1f} MS/s")
```

#### 4. Inadequate Record Length

**Problem**: Can't capture both transient and steady-state

**Solution**:

```python
# Calculate required record length
f_sample = 100e6  # 100 MS/s
duration_needed = 1e-3  # 1 ms
points_needed = f_sample * duration_needed
print(f"Required memory depth: {points_needed/1e3:.0f} kpts")

# Use segmented memory for long captures
# Use roll mode for continuous monitoring
```

#### 5. Incorrect Probe Compensation

**Problem**: Uncompensated probes cause frequency response errors

**Solution**:

```python
# Always compensate probes before use
# Use oscilloscope's probe compensation output
# Adjust compensation capacitor for square corners
# Re-compensate when changing channels
```

## Real-World Examples

### IoT Device Power Profiling

**Scenario**: Profile power consumption of battery-powered IoT sensor with sleep modes

```python
import tracekit as tk
import numpy as np
import matplotlib.pyplot as plt

# Load power measurement over complete duty cycle
v_supply = tk.load("iot_device_voltage.wfm")
i_supply = tk.load("iot_device_current.wfm")

print("=== IoT Device Power Profile ===\n")

# Calculate power
power = tk.instantaneous_power(v_supply, i_supply)
sample_rate = power.metadata.sample_rate
time = np.arange(len(power.data)) / sample_rate

# Identify different power states using thresholds
i_data = i_supply.data * 1e6  # Convert to µA

# Define thresholds (example values)
i_deep_sleep = 10      # µA
i_sleep = 500          # µA
i_active = 5000        # µA
i_tx = 50000           # µA

# Classify each sample
states = np.zeros_like(i_data, dtype=int)
states[i_data < i_deep_sleep] = 0  # Deep sleep
states[(i_data >= i_deep_sleep) & (i_data < i_sleep)] = 1  # Sleep
states[(i_data >= i_sleep) & (i_data < i_active)] = 2  # Active
states[i_data >= i_active] = 3  # Transmit

state_names = ['Deep Sleep', 'Sleep', 'Active', 'Transmit']
state_colors = ['blue', 'green', 'yellow', 'red']

# Calculate time in each state
dt = 1 / sample_rate
total_time = len(states) * dt
time_in_state = []
power_in_state = []

for state in range(4):
    mask = states == state
    time_state = np.sum(mask) * dt
    time_in_state.append(time_state)

    if np.any(mask):
        power_state = np.mean(power.data[mask])
    else:
        power_state = 0
    power_in_state.append(power_state)

    print(f"{state_names[state]}:")
    print(f"  Duration: {time_state*1e3:.2f} ms ({time_state/total_time*100:.1f}%)")
    print(f"  Avg Current: {np.mean(i_data[mask]) if np.any(mask) else 0:.1f} µA")
    print(f"  Avg Power: {power_state*1e6:.2f} µW")

# Calculate average power over entire cycle
p_avg = tk.average_power(power)
print(f"\nAverage Power (over cycle): {p_avg*1e6:.2f} µW ({p_avg*1e3:.4f} mW)")

# Estimate battery life
# Assume 3.7V Li-ion, 2000 mAh
battery_capacity_mah = 2000
battery_voltage = 3.7
battery_capacity_j = battery_capacity_mah * 1e-3 * 3600 * battery_voltage  # Joules

# Calculate runtime
runtime_seconds = battery_capacity_j / p_avg
runtime_days = runtime_seconds / 86400

print(f"\nBattery Life Estimate (2000 mAh @ 3.7V):")
print(f"  Runtime: {runtime_days:.1f} days ({runtime_seconds/3600:.0f} hours)")
print(f"  Average current: {p_avg/battery_voltage*1e6:.1f} µA")

# Calculate energy per cycle
e_cycle = tk.energy(power)
print(f"  Energy per cycle: {e_cycle*1e6:.2f} µJ")

# Plot power profile
fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

# Current over time with state shading
axes[0].plot(time*1e3, i_data, 'k-', linewidth=0.5)
axes[0].set_ylabel('Current (µA)')
axes[0].set_yscale('log')
axes[0].set_title('IoT Device Power Profile')
axes[0].grid(True, alpha=0.3)

# Add state regions
for state in range(4):
    mask = states == state
    if np.any(mask):
        axes[0].fill_between(time*1e3, 0, i_data, where=mask,
                             alpha=0.3, label=state_names[state],
                             color=state_colors[state])
axes[0].legend(loc='upper right')

# Power over time
axes[1].plot(time*1e3, power.data*1e6, 'r-', linewidth=0.5)
axes[1].axhline(p_avg*1e6, color='b', linestyle='--',
                label=f'Average: {p_avg*1e6:.2f} µW')
axes[1].set_ylabel('Power (µW)')
axes[1].set_yscale('log')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Cumulative energy
cumulative_energy = np.cumsum(power.data) * dt * 1e6  # µJ
axes[2].plot(time*1e3, cumulative_energy, 'g-', linewidth=1)
axes[2].set_ylabel('Cumulative Energy (µJ)')
axes[2].set_xlabel('Time (ms)')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('iot_power_profile.png', dpi=300)
plt.show()

# Create power budget breakdown
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Time breakdown
axes[0].pie(time_in_state, labels=state_names, autopct='%1.1f%%',
           colors=state_colors, startangle=90)
axes[0].set_title('Time Distribution')

# Energy breakdown
energy_in_state = [t * p for t, p in zip(time_in_state, power_in_state)]
axes[1].pie(energy_in_state, labels=state_names, autopct='%1.1f%%',
           colors=state_colors, startangle=90)
axes[1].set_title('Energy Distribution')

plt.tight_layout()
plt.savefig('iot_power_budget.png', dpi=300)
plt.show()
```

**Expected Output**:

```
=== IoT Device Power Profile ===

Deep Sleep:
  Duration: 900.00 ms (90.0%)
  Avg Current: 5.0 µA
  Avg Power: 18.50 µW

Sleep:
  Duration: 0.00 ms (0.0%)
  Avg Current: 0.0 µA
  Avg Power: 0.00 µW

Active:
  Duration: 95.00 ms (9.5%)
  Avg Current: 2500.0 µA
  Avg Power: 9250.00 µW

Transmit:
  Duration: 5.00 ms (0.5%)
  Avg Current: 55000.0 µA
  Avg Power: 203500.00 µW

Average Power (over cycle): 1196.75 µW (1.1968 mW)

Battery Life Estimate (2000 mAh @ 3.7V):
  Runtime: 230.3 days (5528 hours)
  Average current: 323.4 µA
  Energy per cycle: 1196.75 µJ
```

### DC-DC Converter Characterization

**Scenario**: Complete characterization of synchronous buck converter

```python
import tracekit as tk
import numpy as np
import matplotlib.pyplot as plt

# Load measurements
v_in = tk.load("buck_vin.wfm")
i_in = tk.load("buck_iin.wfm")
v_out = tk.load("buck_vout.wfm")
i_out = tk.load("buck_iout.wfm")
v_sw = tk.load("buck_switch_node.wfm")

print("=== DC-DC Buck Converter Characterization ===\n")
print("Specifications: 12V→5V, 500kHz, 3A max\n")

# Calculate all power metrics
p_in = tk.average_power(voltage=v_in, current=i_in)
p_out = tk.average_power(voltage=v_out, current=i_out)
eta = tk.efficiency(v_in, i_in, v_out, i_out)
losses = p_in - p_out

print(f"Power Conversion:")
print(f"  Input:      {p_in:.3f} W")
print(f"  Output:     {p_out:.3f} W")
print(f"  Efficiency: {eta*100:.2f}%")
print(f"  Losses:     {losses:.3f} W")

# Output regulation
v_out_stats = tk.ripple_statistics(v_out)
print(f"\nOutput Voltage:")
print(f"  Nominal:    {v_out_stats['dc_level']:.4f} V")
print(f"  Ripple:     {v_out_stats['ripple_pp']*1e3:.2f} mV pk-pk ({v_out_stats['ripple_pp_percent']:.3f}%)")
print(f"  Ripple RMS: {v_out_stats['ripple_rms']*1e3:.2f} mV")
print(f"  Frequency:  {v_out_stats['ripple_frequency']/1e3:.1f} kHz")

# Verify against specs
v_nominal = 5.0
v_tolerance = 0.05  # ±5%
v_out_avg = v_out_stats['dc_level']
v_error = abs(v_out_avg - v_nominal) / v_nominal

if v_error > v_tolerance:
    print(f"  ❌ FAIL: Output voltage error {v_error*100:.2f}% exceeds ±{v_tolerance*100}%")
else:
    print(f"  ✓ PASS: Output voltage within ±{v_tolerance*100}% ({v_error*100:.2f}%)")

# Output current
i_out_avg = tk.mean(i_out)
i_out_ripple_pp, i_out_ripple_rms = tk.ripple(i_out)
print(f"\nOutput Current:")
print(f"  Average:    {i_out_avg:.3f} A")
print(f"  Ripple:     {i_out_ripple_pp*1e3:.0f} mA pk-pk")
print(f"  Ripple RMS: {i_out_ripple_rms*1e3:.0f} mA")

# Switching analysis
freq = tk.frequency(v_sw)
duty = tk.duty_cycle(v_sw)
print(f"\nSwitching Parameters:")
print(f"  Frequency:  {freq/1e3:.1f} kHz")
print(f"  Duty Cycle: {duty*100:.2f}%")

# Check switching frequency tolerance
f_nominal = 500e3
f_tolerance = 0.10  # ±10%
f_error = abs(freq - f_nominal) / f_nominal

if f_error > f_tolerance:
    print(f"  ❌ FAIL: Frequency error {f_error*100:.1f}% exceeds ±{f_tolerance*100}%")
else:
    print(f"  ✓ PASS: Frequency within ±{f_tolerance*100}% ({f_error*100:.1f}%)")

# Rise/fall time analysis
rise_time = tk.rise_time(v_sw)
fall_time = tk.fall_time(v_sw)
print(f"  Rise Time:  {rise_time*1e9:.1f} ns")
print(f"  Fall Time:  {fall_time*1e9:.1f} ns")

# Input ripple
i_in_ripple_pp, i_in_ripple_rms = tk.ripple(i_in)
print(f"\nInput Current Ripple:")
print(f"  Peak-Peak: {i_in_ripple_pp*1e3:.0f} mA")
print(f"  RMS:       {i_in_ripple_rms*1e3:.0f} mA")

# Generate comprehensive report plot
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(4, 2, hspace=0.3, wspace=0.3)

sample_rate = v_sw.metadata.sample_rate
time = np.arange(len(v_sw.data)) / sample_rate * 1e6  # µs

# Zoom to a few switching cycles
period = 1 / freq
n_periods = 5
start_idx = len(time) // 2
end_idx = start_idx + int(n_periods * period * sample_rate)
time_zoom = time[start_idx:end_idx]
time_zoom = time_zoom - time_zoom[0]

# Plot 1: Switch node voltage
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(time_zoom, v_sw.data[start_idx:end_idx], 'b-', linewidth=1)
ax1.set_ylabel('Switch Node (V)')
ax1.set_title('Switching Waveforms')
ax1.grid(True, alpha=0.3)

# Plot 2: Output voltage (AC-coupled to show ripple)
ax2 = fig.add_subplot(gs[1, 0])
v_out_ac = (v_out.data - v_out_avg) * 1000  # mV
ax2.plot(time_zoom, v_out_ac[start_idx:end_idx], 'r-', linewidth=1)
ax2.set_ylabel('V_OUT Ripple (mV)')
ax2.axhline(0, color='k', linewidth=0.5, linestyle='--')
ax2.grid(True, alpha=0.3)

# Plot 3: Output current
ax3 = fig.add_subplot(gs[2, 0])
ax3.plot(time_zoom, i_out.data[start_idx:end_idx]*1000, 'g-', linewidth=1)
ax3.set_ylabel('I_OUT (mA)')
ax3.grid(True, alpha=0.3)

# Plot 4: Instantaneous power
ax4 = fig.add_subplot(gs[3, 0])
power = tk.instantaneous_power(v_out, i_out)
ax4.plot(time_zoom, power.data[start_idx:end_idx], 'm-', linewidth=1)
ax4.axhline(p_out, color='r', linestyle='--', label=f'Avg: {p_out:.2f}W')
ax4.set_ylabel('Power (W)')
ax4.set_xlabel('Time (µs)')
ax4.legend()
ax4.grid(True, alpha=0.3)

# Plot 5: Efficiency vs Load (if multiple measurements available)
# This would require loading multiple test points
# For now, show single point
ax5 = fig.add_subplot(gs[0:2, 1])
ax5.text(0.5, 0.5, f"Efficiency: {eta*100:.2f}%\n\n"
                    f"Input Power: {p_in:.3f} W\n"
                    f"Output Power: {p_out:.3f} W\n"
                    f"Losses: {losses:.3f} W\n\n"
                    f"V_IN: {tk.mean(v_in):.2f} V\n"
                    f"V_OUT: {v_out_avg:.3f} V\n"
                    f"I_OUT: {i_out_avg:.3f} A\n\n"
                    f"Switching: {freq/1e3:.1f} kHz\n"
                    f"Duty Cycle: {duty*100:.2f}%",
         transform=ax5.transAxes, fontsize=14,
         verticalalignment='center', horizontalalignment='center',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
ax5.axis('off')
ax5.set_title('Performance Summary')

# Plot 6: Output voltage histogram
ax6 = fig.add_subplot(gs[2:4, 1])
ax6.hist(v_out.data*1000, bins=50, color='skyblue', edgecolor='black')
ax6.axvline(v_out_avg*1000, color='r', linestyle='--', linewidth=2,
            label=f'Mean: {v_out_avg*1000:.2f} mV')
ax6.set_xlabel('Output Voltage (mV)')
ax6.set_ylabel('Count')
ax6.set_title('Output Voltage Distribution')
ax6.legend()
ax6.grid(True, alpha=0.3, axis='y')

plt.suptitle('DC-DC Buck Converter Characterization Report',
             fontsize=16, fontweight='bold')
plt.savefig('buck_converter_characterization.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"\n✓ Characterization complete! Report saved to buck_converter_characterization.png")
```

**Expected Output**:

```
=== DC-DC Buck Converter Characterization ===

Specifications: 12V→5V, 500kHz, 3A max

Power Conversion:
  Input:      5.405 W
  Output:     5.000 W
  Efficiency: 92.50%
  Losses:     0.405 W

Output Voltage:
  Nominal:    5.0000 V
  Ripple:     50.00 mV pk-pk (1.000%)
  Ripple RMS: 14.43 mV
  Frequency:  500.0 kHz
  ✓ PASS: Output voltage within ±5% (0.00%)

Output Current:
  Average:    1.000 A
  Ripple:     450 mA pk-pk
  Ripple RMS: 130 mA

Switching Parameters:
  Frequency:  500.0 kHz
  Duty Cycle: 41.67%
  ✓ PASS: Frequency within ±10% (0.0%)
  Rise Time:  25.0 ns
  Fall Time:  20.0 ns

Input Current Ripple:
  Peak-Peak: 125 mA
  RMS:       36 mA

✓ Characterization complete! Report saved to buck_converter_characterization.png
```

### Power Amplifier Efficiency

**Scenario**: Measure efficiency of Class AB audio amplifier

```python
import tracekit as tk
import numpy as np
import matplotlib.pyplot as plt

# Load amplifier measurements
# Input: audio signal from source
# Output: amplified signal to 8Ω load
v_supply_pos = tk.load("amp_vcc.wfm")
v_supply_neg = tk.load("amp_vee.wfm")
i_supply = tk.load("amp_supply_current.wfm")
v_output = tk.load("amp_output_voltage.wfm")
v_input = tk.load("amp_input_voltage.wfm")

print("=== Power Amplifier Efficiency Analysis ===\n")

# Calculate supply power (assuming split supply ±15V)
# P_supply = (V+ - V-) × I
v_supply = v_supply_pos.data - v_supply_neg.data
i_supply_data = i_supply.data
p_supply_inst = v_supply * i_supply_data

# Average supply power
p_supply = np.mean(p_supply_inst)
print(f"Supply Power: {p_supply:.3f} W")

# Calculate output power into load
# P_out = V_rms² / R_load
r_load = 8.0  # Ohms (speaker impedance)
v_out_rms = tk.rms(v_output)
p_out = v_out_rms**2 / r_load

print(f"Output Power: {p_out:.3f} W")
print(f"Output RMS Voltage: {v_out_rms:.3f} V")

# Calculate efficiency
eta = (p_out / p_supply) * 100
print(f"Efficiency: {eta:.2f}%")

# Power dissipated as heat
p_dissipated = p_supply - p_out
print(f"Power Dissipated: {p_dissipated:.3f} W")

# Calculate voltage gain
v_in_rms = tk.rms(v_input)
gain_v = v_out_rms / v_in_rms
gain_db = 20 * np.log10(gain_v)
print(f"\nVoltage Gain: {gain_v:.2f} ({gain_db:.1f} dB)")

# Calculate power gain
p_in = v_in_rms**2 / 10e3  # Assuming 10kΩ input impedance
gain_p = p_out / p_in
gain_p_db = 10 * np.log10(gain_p)
print(f"Power Gain: {gain_p:.0f} ({gain_p_db:.1f} dB)")

# Analyze THD (Total Harmonic Distortion)
thd = tk.thd(v_output)
print(f"\nTotal Harmonic Distortion: {thd*100:.3f}%")

# Signal-to-noise ratio
snr = tk.snr(v_output)
print(f"Signal-to-Noise Ratio: {snr:.1f} dB")

# Calculate efficiency at different output levels
print(f"\n=== Efficiency vs. Output Power ===")
# This requires multiple measurements at different input levels
# For demonstration, show single point
print(f"Output: {p_out:.2f} W, Efficiency: {eta:.1f}%")

# Plot waveforms
sample_rate = v_output.metadata.sample_rate
time = np.arange(len(v_output.data)) / sample_rate * 1000  # ms

fig, axes = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

# Input signal
axes[0].plot(time, v_input.data, 'b-', linewidth=0.8)
axes[0].set_ylabel('Input (V)')
axes[0].set_title('Power Amplifier Analysis')
axes[0].grid(True, alpha=0.3)

# Output signal
axes[1].plot(time, v_output.data, 'r-', linewidth=0.8)
axes[1].set_ylabel('Output (V)')
axes[1].grid(True, alpha=0.3)

# Supply current
axes[2].plot(time, i_supply.data*1000, 'g-', linewidth=0.8)
axes[2].set_ylabel('Supply Current (mA)')
axes[2].grid(True, alpha=0.3)

# Instantaneous efficiency
# Avoid division by zero
p_out_inst = v_output.data**2 / r_load
eta_inst = np.zeros_like(p_supply_inst)
mask = p_supply_inst > 0.01  # Avoid near-zero denominators
eta_inst[mask] = (p_out_inst[mask] / p_supply_inst[mask]) * 100
eta_inst[~mask] = 0

axes[3].plot(time, eta_inst, 'm-', linewidth=0.5)
axes[3].axhline(eta, color='r', linestyle='--', label=f'Average: {eta:.1f}%')
axes[3].set_ylabel('Efficiency (%)')
axes[3].set_xlabel('Time (ms)')
axes[3].set_ylim(0, 100)
axes[3].legend()
axes[3].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('amplifier_efficiency.png', dpi=300)
plt.show()

# Class AB efficiency note
print(f"\n📝 Note: Class AB amplifier efficiency is typically 50-60% at full power.")
print(f"   Measured {eta:.1f}% is {'within' if 40 < eta < 70 else 'outside'} expected range.")
```

**Expected Output**:

```
=== Power Amplifier Efficiency Analysis ===

Supply Power: 15.750 W
Output Power: 8.000 W
Output RMS Voltage: 8.000 V
Efficiency: 50.79%
Power Dissipated: 7.750 W

Voltage Gain: 10.00 (20.0 dB)
Power Gain: 400 (26.0 dB)

Total Harmonic Distortion: 0.050%
Signal-to-Noise Ratio: 95.5 dB

=== Efficiency vs. Output Power ===
Output: 8.00 W, Efficiency: 50.8%

📝 Note: Class AB amplifier efficiency is typically 50-60% at full power.
   Measured 50.8% is within expected range.
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: Measurements Return NaN

**Causes**:

- Signal not periodic (for frequency measurements)
- Insufficient signal amplitude
- Too much noise
- Incorrect threshold settings

**Solutions**:

```python
import tracekit as tk
import math

# Load signal
signal = tk.load("signal.wfm")

# Check if measurement is NaN
freq = tk.frequency(signal)
if math.isnan(freq):
    print("Frequency measurement failed!")

    # Debug: Check signal properties
    print(f"Signal amplitude: {tk.vpp(signal):.3f} V")
    print(f"Signal mean: {tk.mean(signal):.3f} V")
    print(f"Signal RMS: {tk.rms(signal):.3f} V")

    # Try edge detection with custom threshold
    threshold = tk.mean(signal)
    edges = tk.find_edges(signal, threshold=threshold)

    if len(edges) >= 2:
        # Calculate frequency from edges
        period_samples = edges[1] - edges[0]
        period = period_samples / signal.metadata.sample_rate
        freq = 1 / period
        print(f"Frequency from edges: {freq:.2f} Hz")
    else:
        print("Not enough edges found - signal may not be periodic")
```

#### Issue: Noisy Power Measurements

**Causes**:

- Ground loops
- Insufficient probe bandwidth limiting
- Switching noise
- Aliasing

**Solutions**:

```python
import tracekit as tk

# Load noisy measurements
v = tk.load("voltage_noisy.wfm")
i = tk.load("current_noisy.wfm")

# Apply low-pass filter to remove high-frequency noise
v_filtered = tk.low_pass(v, cutoff=100e3)  # 100 kHz cutoff
i_filtered = tk.low_pass(i, cutoff=100e3)

# Calculate power with filtered signals
power_filtered = tk.instantaneous_power(v_filtered, i_filtered)
p_avg_filtered = tk.average_power(power_filtered)

# Compare to noisy measurement
power_noisy = tk.instantaneous_power(v, i)
p_avg_noisy = tk.average_power(power_noisy)

print(f"Average power (noisy):    {p_avg_noisy:.4f} W")
print(f"Average power (filtered): {p_avg_filtered:.4f} W")
print(f"Difference: {abs(p_avg_noisy - p_avg_filtered):.4f} W")
```

#### Issue: Incorrect Efficiency (>100% or <0%)

**Causes**:

- Probe polarity reversed
- Sample rate mismatch between channels
- Time misalignment
- Measurement error

**Solutions**:

```python
import tracekit as tk

v_in = tk.load("vin.wfm")
i_in = tk.load("iin.wfm")
v_out = tk.load("vout.wfm")
i_out = tk.load("iout.wfm")

# Check polarity
p_in = tk.average_power(voltage=v_in, current=i_in)
p_out = tk.average_power(voltage=v_out, current=i_out)

print(f"Input power:  {p_in:.3f} W")
print(f"Output power: {p_out:.3f} W")

if p_in < 0:
    print("ERROR: Negative input power - check current probe polarity")
if p_out < 0:
    print("ERROR: Negative output power - check current probe polarity")

eta = tk.efficiency(v_in, i_in, v_out, i_out)

if eta > 1.0:
    print(f"ERROR: Efficiency > 100% ({eta*100:.1f}%)")
    print("Possible causes:")
    print("  - Output current probe polarity reversed")
    print("  - Measurement time misalignment")
    print("  - Regenerative load")
elif eta < 0:
    print(f"ERROR: Efficiency < 0% ({eta*100:.1f}%)")
    print("Possible causes:")
    print("  - Input current probe polarity reversed")
    print("  - Both probes reversed")
else:
    print(f"Efficiency: {eta*100:.2f}% ✓")
```

#### Issue: Ripple Measurement Shows Unexpected Results

**Causes**:

- DC coupling enabled when AC ripple expected
- Insufficient sample rate for ripple frequency
- Multiple ripple frequencies present

**Solutions**:

```python
import tracekit as tk
import numpy as np

# Load DC output with ripple
dc_output = tk.load("dc_output.wfm")

# Method 1: Use ripple() function with DC removal
r_pp, r_rms = tk.ripple(dc_output, dc_coupling=False)
print(f"Ripple (AC-coupled): {r_pp*1e3:.2f} mV pk-pk")

# Method 2: Manually remove DC and measure
dc_level = tk.mean(dc_output)
ac_component = dc_output.data - dc_level
r_pp_manual = np.max(ac_component) - np.min(ac_component)
print(f"Ripple (manual):     {r_pp_manual*1e3:.2f} mV pk-pk")

# Get comprehensive ripple statistics
stats = tk.ripple_statistics(dc_output)
print(f"\nRipple Statistics:")
print(f"  DC level:         {stats['dc_level']:.4f} V")
print(f"  Ripple pk-pk:     {stats['ripple_pp']*1e3:.2f} mV")
print(f"  Ripple RMS:       {stats['ripple_rms']*1e3:.2f} mV")
print(f"  Ripple frequency: {stats['ripple_frequency']/1e3:.1f} kHz")
print(f"  Crest factor:     {stats['crest_factor']:.2f}")

# Check sample rate
sample_rate = dc_output.metadata.sample_rate
f_ripple = stats['ripple_frequency']
samples_per_cycle = sample_rate / f_ripple
print(f"\nSamples per ripple cycle: {samples_per_cycle:.1f}")

if samples_per_cycle < 10:
    print("⚠️  WARNING: Insufficient sample rate for accurate ripple measurement")
    print(f"   Recommended: ≥{f_ripple * 10 / 1e6:.1f} MS/s")
```

#### Issue: Power Factor Calculation Gives Unexpected Values

**Causes**:

- Non-sinusoidal waveforms (harmonics)
- Time misalignment between voltage and current
- Insufficient measurement duration

**Solutions**:

```python
import tracekit as tk
import numpy as np

v_ac = tk.load("ac_voltage.wfm")
i_ac = tk.load("ac_current.wfm")

# Calculate power factor
pf = tk.power_factor(v_ac, i_ac)
print(f"Power Factor: {pf:.3f}")

# Check for sinusoidal waveforms
# Calculate THD for both voltage and current
thd_v = tk.thd(v_ac)
thd_i = tk.thd(i_ac)
print(f"Voltage THD: {thd_v*100:.2f}%")
print(f"Current THD: {thd_i*100:.2f}%")

if thd_v > 0.05 or thd_i > 0.05:
    print("⚠️  High harmonic content detected")
    print("   True power factor includes distortion effects")

# Calculate displacement power factor (fundamental only)
p = tk.average_power(voltage=v_ac, current=i_ac)
s = tk.apparent_power(v_ac, i_ac)
dpf = p / s
print(f"Displacement PF: {dpf:.3f}")

# Check measurement duration
sample_rate = v_ac.metadata.sample_rate
duration = len(v_ac.data) / sample_rate
f_line = 60  # Hz
cycles = duration * f_line
print(f"\nMeasurement duration: {duration:.3f} s ({cycles:.1f} cycles)")

if cycles < 10:
    print("⚠️  WARNING: Measurement duration may be insufficient")
    print("   Recommended: ≥10 line cycles for accurate power factor")
```

---

## Summary

This guide covered comprehensive power analysis with TraceKit including:

**Basic Measurements**:

- DC power, AC power, power factor, efficiency

**Advanced Topics**:

- Switching regulator analysis (ripple, efficiency, switching waveforms)
- Battery discharge characterization (capacity, SOC, runtime)
- Motor power analysis (three-phase, reactive power, PF correction)
- Solar panel MPPT analysis (I-V curves, fill factor, tracking)

**Best Practices**:

- Probe selection and placement
- Grounding and noise reduction
- Sample rate selection
- Common pitfalls and solutions

**Real-World Examples**:

- IoT device power profiling with sleep modes
- DC-DC converter complete characterization
- Power amplifier efficiency measurement
- Solar MPPT performance evaluation

## Additional Resources

### Documentation

- [Power Analysis API Reference](../api/power-analysis.md)
- [Analysis API](../api/analysis.md)
- [Visualization API](../api/visualization.md)

### Standards Referenced

- IEEE 1459-2010: Power quality measurements
- IEEE 181-2011: Pulse measurements
- IEC 61000-4-7: Harmonics and power quality
- IEEE 1057-2017: Digitizer characterization

### Getting Help

- GitHub Issues: [github.com/lair-click-bats/tracekit/issues](https://github.com/lair-click-bats/tracekit/issues)
- Documentation: [docs/](https://github.com/lair-click-bats/tracekit/tree/main/docs)

---

_TraceKit Power Analysis Guide - Version 0.1.0 - Last Updated: 2026-01-08_
