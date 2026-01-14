#!/usr/bin/env python3
"""Example 01: Basic Power Measurements.

Demonstrates instantaneous power, average power, and energy
calculations from voltage and current waveforms.

Key Concepts:
- Instantaneous power: P(t) = V(t) x I(t)
- Average power: Mean of instantaneous power
- Energy: Integral of power over time
- Power statistics

Expected Output:
- Power calculations for resistive loads
- Energy consumption over time
- Power statistics summary

Run:
    uv run python examples/09_power/01_basic_power.py
"""

import numpy as np

import tracekit as tk
from tracekit.core.types import TraceMetadata, WaveformTrace


def main() -> None:
    """Demonstrate basic power measurements."""
    print("=" * 60)
    print("TraceKit Example: Basic Power Measurements")
    print("=" * 60)

    # Create common parameters
    sample_rate = 100e3  # 100 kHz
    duration = 100e-3  # 100 ms
    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate
    metadata = TraceMetadata(sample_rate=sample_rate)

    # --- DC Power (Resistive Load) ---
    print("\n--- DC Power: Resistive Load ---")
    print("P = V x I = V^2/R = I^2*R")

    resistance = 100  # 100 ohms
    dc_voltage = 5.0  # 5V DC
    dc_current = dc_voltage / resistance  # 50 mA

    # Create constant voltage and current traces
    v_dc = np.ones(n_samples) * dc_voltage
    i_dc = np.ones(n_samples) * dc_current

    trace_v_dc = WaveformTrace(data=v_dc, metadata=metadata)
    trace_i_dc = WaveformTrace(data=i_dc, metadata=metadata)

    # Instantaneous power
    p_inst = tk.instantaneous_power(trace_v_dc, trace_i_dc)

    # Average power
    p_avg = tk.average_power(voltage=trace_v_dc, current=trace_i_dc)

    # Energy
    total_energy = tk.energy(voltage=trace_v_dc, current=trace_i_dc)

    print(f"Voltage: {dc_voltage:.1f} V DC")
    print(f"Current: {dc_current * 1e3:.1f} mA")
    print(f"Resistance: {resistance} ohms")
    print(f"Instantaneous power: {p_inst.data[0] * 1e3:.2f} mW (constant)")
    print(f"Average power: {p_avg * 1e3:.2f} mW")
    print(f"Energy over {duration * 1e3:.0f} ms: {total_energy * 1e3:.2f} mJ")
    print(f"Expected: P = V^2/R = {dc_voltage**2 / resistance * 1e3:.2f} mW")

    # --- AC Power (Pure Resistive) ---
    print("\n--- AC Power: Pure Resistive Load ---")
    print("P_avg = V_rms x I_rms (when in phase)")

    frequency = 60  # 60 Hz
    v_peak = 170  # ~120V RMS
    v_ac = v_peak * np.sin(2 * np.pi * frequency * t)
    i_ac = v_ac / resistance  # Pure resistive, current in phase

    trace_v_ac = WaveformTrace(data=v_ac, metadata=metadata)
    trace_i_ac = WaveformTrace(data=i_ac, metadata=metadata)

    p_inst_ac = tk.instantaneous_power(trace_v_ac, trace_i_ac)
    p_avg_ac = tk.average_power(voltage=trace_v_ac, current=trace_i_ac)

    v_rms = v_peak / np.sqrt(2)
    i_rms = v_rms / resistance
    expected_power = v_rms * i_rms

    print(f"AC voltage: {v_peak:.0f} V peak ({v_rms:.1f} V RMS)")
    print(f"Load: {resistance} ohms (pure resistive)")
    print(f"Peak instantaneous power: {np.max(p_inst_ac.data):.2f} W")
    print(f"Average power: {p_avg_ac:.2f} W")
    print(f"Expected (V_rms x I_rms): {expected_power:.2f} W")

    # --- Pulsed Power ---
    print("\n--- Pulsed Power ---")

    # PWM-like power (50% duty cycle)
    duty_cycle = 0.5
    pwm_freq = 1e3  # 1 kHz PWM
    pwm = (np.sin(2 * np.pi * pwm_freq * t) > 0).astype(float)

    v_pwm = 12.0 * pwm  # 12V when on
    i_pwm = v_pwm / 10  # 10 ohm load

    trace_v_pwm = WaveformTrace(data=v_pwm, metadata=metadata)
    trace_i_pwm = WaveformTrace(data=i_pwm, metadata=metadata)

    p_inst_pwm = tk.instantaneous_power(trace_v_pwm, trace_i_pwm)
    p_avg_pwm = tk.average_power(voltage=trace_v_pwm, current=trace_i_pwm)

    print(f"PWM voltage: 12V at {pwm_freq / 1e3:.0f} kHz, {duty_cycle * 100:.0f}% duty")
    print(f"Peak power (when ON): {np.max(p_inst_pwm.data):.2f} W")
    print(f"Average power: {p_avg_pwm:.2f} W")
    print(f"Expected (duty x P_peak): {duty_cycle * 12**2 / 10:.2f} W")

    # --- Power Statistics ---
    print("\n--- Power Statistics ---")

    stats = tk.power_statistics(voltage=trace_v_ac, current=trace_i_ac)

    print("Power statistics for AC signal:")
    print(f"  Average: {stats['average']:.2f} W")
    print(f"  RMS: {stats['rms']:.2f} W")
    print(f"  Peak: {stats['peak']:.2f} W")
    print(f"  Min: {stats['min']:.2f} W")
    print(f"  Std Dev: {stats['std']:.2f} W")
    print(f"  Energy: {stats['energy'] * 1e3:.2f} mJ")

    # --- Energy Over Time ---
    print("\n--- Energy Accumulation ---")

    # Variable load simulation
    load_profile = np.ones(n_samples)
    load_profile[n_samples // 4 : n_samples // 2] = 2.0  # Double load
    load_profile[n_samples // 2 : 3 * n_samples // 4] = 0.5  # Half load

    v_const = np.ones(n_samples) * 12.0
    i_variable = v_const / (100 / load_profile)  # Variable current

    trace_v_load = WaveformTrace(data=v_const, metadata=metadata)
    trace_i_load = WaveformTrace(data=i_variable, metadata=metadata)

    energy_total = tk.energy(voltage=trace_v_load, current=trace_i_load)

    # Energy at different time points
    quarter = n_samples // 4
    print("Variable load power consumption:")
    print(f"  0-25%:   P = {np.mean(v_const[:quarter] * i_variable[:quarter]):.3f} W")
    print(
        f"  25-50%:  P = {np.mean(v_const[quarter : 2 * quarter] * i_variable[quarter : 2 * quarter]):.3f} W"
    )
    print(
        f"  50-75%:  P = {np.mean(v_const[2 * quarter : 3 * quarter] * i_variable[2 * quarter : 3 * quarter]):.3f} W"
    )
    print(f"  75-100%: P = {np.mean(v_const[3 * quarter :] * i_variable[3 * quarter :]):.3f} W")
    print(f"Total energy: {energy_total * 1e3:.2f} mJ")

    # --- Battery Discharge Example ---
    print("\n--- Practical: Battery Discharge ---")

    # Simulated battery discharge (voltage drops over time)
    battery_capacity = 2000e-3  # 2000 mAh
    discharge_current = 0.5  # 500 mA
    initial_voltage = 4.2
    final_voltage = 3.0

    # Linear voltage drop (simplified)
    v_battery = np.linspace(initial_voltage, final_voltage, n_samples)
    i_battery = np.ones(n_samples) * discharge_current

    trace_v_bat = WaveformTrace(data=v_battery, metadata=metadata)
    trace_i_bat = WaveformTrace(data=i_battery, metadata=metadata)

    p_battery = tk.instantaneous_power(trace_v_bat, trace_i_bat)
    energy_battery = tk.energy(voltage=trace_v_bat, current=trace_i_bat)

    print(f"Battery: {initial_voltage}V to {final_voltage}V")
    print(f"Discharge current: {discharge_current * 1e3:.0f} mA")
    print(f"Initial power: {p_battery.data[0]:.2f} W")
    print(f"Final power: {p_battery.data[-1]:.2f} W")
    print(f"Energy delivered in {duration * 1e3:.0f} ms: {energy_battery * 1e3:.2f} mJ")
    print(f"Average voltage: {np.mean(v_battery):.2f} V")
    print(f"Average power: {np.mean(p_battery.data):.2f} W")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. instantaneous_power() gives P(t) = V(t) x I(t)")
    print("  2. average_power() computes mean power over time")
    print("  3. energy() integrates power to get total energy")
    print("  4. power_statistics() gives comprehensive stats")
    print("  5. For DC: P = V x I = V^2/R = I^2*R")
    print("  6. For AC resistive: P_avg = V_rms x I_rms")
    print("=" * 60)


if __name__ == "__main__":
    main()
