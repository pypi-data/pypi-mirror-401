#!/usr/bin/env python3
"""Example 01: Arithmetic Operations on Traces.

Demonstrates adding, subtracting, multiplying, and dividing waveform
traces for signal combination and analysis.

Key Concepts:
- Adding traces (signal combination, averaging)
- Subtracting traces (difference, baseline removal)
- Multiplying traces (power calculation, modulation)
- Dividing traces (impedance, gain measurement)

Expected Output:
- Combined signal examples
- Power calculation from V and I
- Impedance calculation

Run:
    uv run python examples/07_math/01_arithmetic.py
"""

import numpy as np

import tracekit as tk
from tracekit.core.types import TraceMetadata, WaveformTrace


def main() -> None:
    """Demonstrate arithmetic operations on traces."""
    print("=" * 60)
    print("TraceKit Example: Arithmetic Operations")
    print("=" * 60)

    # Create common time base
    sample_rate = 1e6  # 1 MHz
    duration = 10e-3  # 10 ms
    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate
    metadata = TraceMetadata(sample_rate=sample_rate)

    # --- Addition ---
    print("\n--- Addition: add() ---")
    print("Combining two signals or averaging measurements")

    # Two sine waves at different frequencies
    signal_1k = np.sin(2 * np.pi * 1000 * t)
    signal_3k = 0.5 * np.sin(2 * np.pi * 3000 * t)

    trace1 = WaveformTrace(data=signal_1k, metadata=metadata)
    trace2 = WaveformTrace(data=signal_3k, metadata=metadata)

    combined = tk.add(trace1, trace2)

    print("Signal 1: 1 kHz sine, amplitude 1.0")
    print("Signal 2: 3 kHz sine, amplitude 0.5")
    print(f"Combined peak-to-peak: {np.ptp(combined.data):.2f} V")
    print(f"Combined RMS: {np.sqrt(np.mean(combined.data**2)):.3f} V")

    # Adding scalar (offset)
    offset_trace = tk.add(trace1, 2.5)  # Add DC offset
    print(f"\nOriginal mean: {np.mean(trace1.data):.4f} V")
    print(f"After +2.5V offset: {np.mean(offset_trace.data):.4f} V")

    # --- Subtraction ---
    print("\n--- Subtraction: subtract() ---")
    print("Computing difference or removing baseline")

    # Create signal with baseline drift
    baseline = 0.1 * t * sample_rate / n_samples  # Linear drift
    signal_with_drift = signal_1k + baseline

    trace_drifted = WaveformTrace(data=signal_with_drift, metadata=metadata)
    trace_baseline = WaveformTrace(data=baseline, metadata=metadata)

    corrected = tk.subtract(trace_drifted, trace_baseline)

    print(f"Original signal range: {np.ptp(signal_with_drift):.3f} V")
    print(f"Corrected signal range: {np.ptp(corrected.data):.3f} V")
    print(f"Drift removed: {baseline[-1]:.3f} V")

    # Common-mode rejection (differential measurement)
    print("\n--- Differential Measurement ---")
    common_mode = 0.2 * np.sin(2 * np.pi * 60 * t)  # 60 Hz noise
    signal_pos = signal_1k + common_mode
    signal_neg = -signal_1k + common_mode

    trace_pos = WaveformTrace(data=signal_pos, metadata=metadata)
    trace_neg = WaveformTrace(data=signal_neg, metadata=metadata)

    differential = tk.subtract(trace_pos, trace_neg)

    print(f"Single-ended 60 Hz component: {0.2:.2f} V")
    print(f"Differential signal amplitude: {np.ptp(differential.data) / 2:.2f} V")
    print("Common-mode rejection achieved!")

    # --- Multiplication ---
    print("\n--- Multiplication: multiply() ---")
    print("Power calculation: P = V x I")

    # Voltage and current waveforms
    voltage = 5.0 * np.sin(2 * np.pi * 1000 * t)  # 5V peak
    current = 0.1 * np.sin(2 * np.pi * 1000 * t)  # 100mA peak, in phase

    trace_v = WaveformTrace(data=voltage, metadata=metadata)
    trace_i = WaveformTrace(data=current, metadata=metadata)

    power = tk.multiply(trace_v, trace_i)

    print("Voltage: 5V peak, 1 kHz")
    print("Current: 100mA peak, 1 kHz")
    print(f"Instantaneous power peak: {np.max(power.data):.3f} W")
    print(f"Average power: {np.mean(power.data):.3f} W")
    print(f"Expected (V_rms x I_rms): {5 / np.sqrt(2) * 0.1 / np.sqrt(2):.3f} W")

    # Power with phase shift
    print("\n--- Power with Phase Shift ---")
    current_lagging = 0.1 * np.sin(2 * np.pi * 1000 * t - np.pi / 4)  # 45 deg lag

    trace_i_lag = WaveformTrace(data=current_lagging, metadata=metadata)
    power_reactive = tk.multiply(trace_v, trace_i_lag)

    pf = np.cos(np.pi / 4)  # Power factor
    print("Current lagging by 45 degrees")
    print(f"Average power: {np.mean(power_reactive.data):.3f} W")
    print(f"Expected (with PF={pf:.3f}): {5 / np.sqrt(2) * 0.1 / np.sqrt(2) * pf:.3f} W")

    # Scaling by constant
    doubled = tk.multiply(trace1, 2.0)
    print(
        f"\nScaling by 2x: original peak {np.max(trace1.data):.2f}, scaled {np.max(doubled.data):.2f}"
    )

    # --- Division ---
    print("\n--- Division: divide() ---")
    print("Impedance calculation: Z = V / I")

    # Impedance measurement
    impedance = tk.divide(trace_v, trace_i)

    print(f"V/I at in-phase: {np.mean(np.abs(impedance.data)):.1f} ohms")
    print("Expected (5V / 0.1A): 50.0 ohms")

    # Gain measurement
    print("\n--- Gain Measurement ---")
    input_signal = 0.1 * np.sin(2 * np.pi * 1000 * t)
    output_signal = 2.0 * np.sin(2 * np.pi * 1000 * t)  # Amplified

    trace_in = WaveformTrace(data=input_signal, metadata=metadata)
    trace_out = WaveformTrace(data=output_signal, metadata=metadata)

    gain = tk.divide(trace_out, trace_in)

    # Avoid division by zero at zero crossings
    valid_idx = np.abs(input_signal) > 0.01
    print(f"Gain (Vout/Vin): {np.mean(gain.data[valid_idx]):.1f}x")
    print(f"Gain in dB: {20 * np.log10(np.mean(np.abs(gain.data[valid_idx]))):.1f} dB")

    # --- Combined Operations ---
    print("\n--- Combined Operations ---")
    print("Creating math channel: (Ch1 + Ch2) / 2")

    ch1 = WaveformTrace(data=signal_1k + np.random.randn(n_samples) * 0.1, metadata=metadata)
    ch2 = WaveformTrace(data=signal_1k + np.random.randn(n_samples) * 0.1, metadata=metadata)

    # Average of two channels
    summed = tk.add(ch1, ch2)
    averaged = tk.divide(summed, 2.0)

    noise_ch1 = np.std(ch1.data - signal_1k)
    noise_averaged = np.std(averaged.data - signal_1k)

    print(f"Single channel noise: {noise_ch1:.4f} V RMS")
    print(f"Averaged noise: {noise_averaged:.4f} V RMS")
    print(f"Improvement: {20 * np.log10(noise_ch1 / noise_averaged):.1f} dB")
    print(f"Expected (sqrt(2)): {20 * np.log10(np.sqrt(2)):.1f} dB")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. add() combines signals or adds offset")
    print("  2. subtract() computes difference or removes baseline")
    print("  3. multiply() calculates power (V x I) or scales")
    print("  4. divide() computes impedance (V/I) or gain")
    print("  5. Operations work with trace + trace or trace + scalar")
    print("  6. Averaging reduces noise by sqrt(N)")
    print("=" * 60)


if __name__ == "__main__":
    main()
