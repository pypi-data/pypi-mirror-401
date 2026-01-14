#!/usr/bin/env python3
"""Example 02: Calculus Operations - Differentiate and Integrate.

Demonstrates differentiation and integration of waveform traces
for slew rate measurement, energy calculation, and signal analysis.

Key Concepts:
- Differentiation for rate of change (dV/dt)
- Integration for accumulated values
- Slew rate measurement
- Energy and charge calculation

Expected Output:
- Derivative of various waveforms
- Integral calculations
- Practical measurement examples

Run:
    uv run python examples/07_math/02_calculus.py
"""

import numpy as np

import tracekit as tk
from tracekit.core.types import TraceMetadata, WaveformTrace


def main() -> None:
    """Demonstrate differentiation and integration."""
    print("=" * 60)
    print("TraceKit Example: Differentiate and Integrate")
    print("=" * 60)

    # Create common parameters
    sample_rate = 10e6  # 10 MHz
    duration = 1e-3  # 1 ms
    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate
    metadata = TraceMetadata(sample_rate=sample_rate)

    # --- Differentiation Basics ---
    print("\n--- Differentiation: differentiate() ---")
    print("Computes rate of change: dV/dt")

    # Sine wave derivative
    frequency = 1e3  # 1 kHz
    amplitude = 1.0
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)
    trace_sine = WaveformTrace(data=sine_wave, metadata=metadata)

    derivative = tk.differentiate(trace_sine)

    # Expected: d/dt[A*sin(wt)] = A*w*cos(wt)
    expected_peak = amplitude * 2 * np.pi * frequency
    actual_peak = np.max(np.abs(derivative.data))

    print(f"\nSine wave: {frequency / 1e3:.0f} kHz, {amplitude:.1f}V amplitude")
    print("Derivative is cosine with peak = A * 2 * pi * f")
    print(f"Expected peak: {expected_peak:.2f} V/s")
    print(f"Measured peak: {actual_peak:.2f} V/s")
    print(f"Error: {abs(expected_peak - actual_peak) / expected_peak * 100:.2f}%")

    # --- Slew Rate Measurement ---
    print("\n--- Slew Rate Measurement ---")
    print("Maximum rate of change during transitions")

    # Create signal with fast edge
    edge_signal = np.zeros(n_samples)
    edge_start = n_samples // 4
    edge_samples = 100  # 10 us rise time at 10 MHz
    edge_signal[edge_start : edge_start + edge_samples] = np.linspace(0, 3.3, edge_samples)
    edge_signal[edge_start + edge_samples :] = 3.3

    trace_edge = WaveformTrace(data=edge_signal, metadata=metadata)
    edge_derivative = tk.differentiate(trace_edge)

    slew_rate = np.max(edge_derivative.data)
    rise_time = 3.3 / slew_rate

    print("Edge: 0V to 3.3V")
    print(f"Slew rate (max dV/dt): {slew_rate / 1e6:.2f} V/us")
    print(f"Calculated rise time: {rise_time * 1e6:.2f} us")
    print(f"Actual edge samples: {edge_samples} ({edge_samples / sample_rate * 1e6:.2f} us)")

    # --- Differentiation for Edge Detection ---
    print("\n--- Edge Detection via Differentiation ---")

    # Square wave with edges
    square = np.sign(np.sin(2 * np.pi * 5e3 * t))  # 5 kHz square
    trace_square = WaveformTrace(data=square, metadata=metadata)

    square_deriv = tk.differentiate(trace_square)

    # Find edge locations (derivative spikes)
    threshold = 0.5 * np.max(np.abs(square_deriv.data))
    rising_edges = np.where(square_deriv.data > threshold)[0]
    falling_edges = np.where(square_deriv.data < -threshold)[0]

    print("Square wave: 5 kHz")
    print(f"Rising edges detected: {len(np.unique(rising_edges // 100))}")
    print(f"Falling edges detected: {len(np.unique(falling_edges // 100))}")
    print(f"Expected edges in {duration * 1e3:.0f} ms: {int(2 * frequency * duration)} each")

    # --- Integration Basics ---
    print("\n--- Integration: integrate() ---")
    print("Computes accumulated value over time")

    # Integrate sine wave (should give -cosine)
    integral = tk.integrate(trace_sine)

    # Expected: integral of A*sin(wt) = -A/w * cos(wt)
    expected_amplitude = amplitude / (2 * np.pi * frequency)
    actual_amplitude = np.max(np.abs(integral.data - np.mean(integral.data)))

    print("\nSine wave integration:")
    print(f"Expected amplitude: {expected_amplitude * 1e6:.2f} uV*s")
    print(f"Measured amplitude: {actual_amplitude * 1e6:.2f} uV*s")

    # --- Energy Calculation ---
    print("\n--- Energy Calculation ---")
    print("Energy = integral of Power over time")

    # Power pulse
    power_trace = np.zeros(n_samples)
    pulse_start = n_samples // 4
    pulse_duration = n_samples // 2
    power_level = 10.0  # 10 Watts

    power_trace[pulse_start : pulse_start + pulse_duration] = power_level

    trace_power = WaveformTrace(data=power_trace, metadata=metadata)
    energy = tk.integrate(trace_power)

    total_energy = energy.data[-1] - energy.data[0]
    expected_energy = power_level * (pulse_duration / sample_rate)

    print(f"Power pulse: {power_level:.0f} W for {pulse_duration / sample_rate * 1e6:.0f} us")
    print(f"Total energy: {total_energy * 1e6:.2f} uJ")
    print(f"Expected: {expected_energy * 1e6:.2f} uJ")

    # --- Charge Calculation ---
    print("\n--- Charge Calculation ---")
    print("Charge = integral of Current over time")

    # Current pulse (capacitor charging)
    current = np.zeros(n_samples)
    tau = 50e-6  # 50 us time constant
    charge_start = n_samples // 4
    charge_t = np.arange(n_samples - charge_start) / sample_rate
    current[charge_start:] = 0.001 * np.exp(-charge_t / tau)  # 1mA initial

    trace_current = WaveformTrace(data=current, metadata=metadata)
    charge = tk.integrate(trace_current)

    total_charge = charge.data[-1]
    expected_charge = 0.001 * tau  # Q = I0 * tau for exponential decay

    print(f"Exponential current decay: I0=1mA, tau={tau * 1e6:.0f} us")
    print(f"Total charge: {total_charge * 1e9:.2f} nC")
    print(f"Expected (I0 * tau): {expected_charge * 1e9:.2f} nC")

    # --- RMS via Integration ---
    print("\n--- RMS Calculation via Integration ---")

    # RMS = sqrt(mean(V^2))
    squared = tk.multiply(trace_sine, trace_sine)
    mean_squared = tk.integrate(squared)
    rms_value = np.sqrt(mean_squared.data[-1] / duration)

    expected_rms = amplitude / np.sqrt(2)

    print(f"Sine wave amplitude: {amplitude:.1f} V")
    print(f"RMS via integration: {rms_value:.4f} V")
    print(f"Expected (A/sqrt(2)): {expected_rms:.4f} V")

    # --- Inverse Operations ---
    print("\n--- Verify Inverse Operations ---")

    # Differentiate then integrate should recover original (minus DC)
    deriv_then_int = tk.integrate(tk.differentiate(trace_sine))

    # Remove DC offset from result
    recovered = deriv_then_int.data - np.mean(deriv_then_int.data)
    original_centered = sine_wave - np.mean(sine_wave)

    correlation = np.corrcoef(recovered[1000:-1000], original_centered[1000:-1000])[0, 1]

    print("Original -> Differentiate -> Integrate -> Recovered")
    print(f"Correlation with original: {correlation:.6f}")
    print("(Edge effects cause minor differences)")

    # --- Practical Example: Inductor Voltage ---
    print("\n--- Practical: Inductor Voltage from Current ---")
    print("V = L * dI/dt")

    inductance = 100e-6  # 100 uH
    current_ramp = np.linspace(0, 0.5, n_samples)  # 0 to 500mA linear

    trace_i_ramp = WaveformTrace(data=current_ramp, metadata=metadata)
    di_dt = tk.differentiate(trace_i_ramp)

    # V = L * dI/dt
    inductor_voltage = tk.multiply(di_dt, inductance)

    di_dt_expected = 0.5 / duration  # A/s
    v_expected = inductance * di_dt_expected

    print(f"Inductance: {inductance * 1e6:.0f} uH")
    print(f"Current ramp: 0 to 500 mA in {duration * 1e3:.0f} ms")
    print(f"dI/dt: {np.mean(di_dt.data):.1f} A/s")
    print(f"Inductor voltage: {np.mean(inductor_voltage.data) * 1e3:.2f} mV")
    print(f"Expected: {v_expected * 1e3:.2f} mV")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. differentiate() computes dV/dt (rate of change)")
    print("  2. integrate() computes accumulated value over time")
    print("  3. Use differentiate for slew rate and edge detection")
    print("  4. Use integrate for energy, charge, RMS calculations")
    print("  5. V = L * dI/dt for inductor analysis")
    print("  6. Q = integral(I*dt) for charge calculation")
    print("=" * 60)


if __name__ == "__main__":
    main()
