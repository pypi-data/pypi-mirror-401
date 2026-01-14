#!/usr/bin/env python3
"""Example 01: Edge-Based Triggering.

Demonstrates finding rising and falling edges in signals
for timing analysis and event detection.

Key Concepts:
- Rising edge detection
- Falling edge detection
- Threshold-based triggering
- Edge timing analysis

Expected Output:
- Edge locations and timestamps
- Edge timing statistics
- Frequency calculation from edges

Run:
    uv run python examples/08_triggering/01_edge_trigger.py
"""

import numpy as np

import tracekit as tk
from tracekit.core.types import TraceMetadata, WaveformTrace


def main() -> None:
    """Demonstrate edge-based triggering."""
    print("=" * 60)
    print("TraceKit Example: Edge-Based Triggering")
    print("=" * 60)

    # Create test signal
    sample_rate = 10e6  # 10 MHz
    duration = 1e-3  # 1 ms
    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate
    metadata = TraceMetadata(sample_rate=sample_rate)

    # --- Rising Edge Detection ---
    print("\n--- Rising Edge Detection ---")

    # Square wave
    frequency = 10e3  # 10 kHz
    square_wave = 3.3 * (np.sin(2 * np.pi * frequency * t) > 0).astype(float)
    trace = WaveformTrace(data=square_wave, metadata=metadata)

    # Find rising edges (return_indices=True to get sample indices)
    rising_edges = tk.find_rising_edges(trace, level=1.65, return_indices=True)

    print(f"Signal: {frequency / 1e3:.0f} kHz square wave, 0-3.3V")
    print("Threshold: 1.65V (50%)")
    print(f"Rising edges found: {len(rising_edges)}")

    if len(rising_edges) > 1:
        # Calculate period from edge spacing
        edge_times = rising_edges / sample_rate
        periods = np.diff(edge_times)
        avg_period = np.mean(periods)
        calc_freq = 1 / avg_period

        print(f"Average period: {avg_period * 1e6:.2f} us")
        print(f"Calculated frequency: {calc_freq / 1e3:.2f} kHz")
        print(f"Period jitter (std): {np.std(periods) * 1e9:.2f} ns")

    # First few edges
    print("\nFirst 5 rising edges (sample indices):")
    for i, edge in enumerate(rising_edges[:5]):
        print(f"  Edge {i + 1}: sample {edge}, time {edge / sample_rate * 1e6:.2f} us")

    # --- Falling Edge Detection ---
    print("\n--- Falling Edge Detection ---")

    falling_edges = tk.find_falling_edges(trace, level=1.65, return_indices=True)

    print(f"Falling edges found: {len(falling_edges)}")

    # Measure pulse widths (rising to falling)
    if len(rising_edges) > 0 and len(falling_edges) > 0:
        pulse_widths = []
        for rising in rising_edges:
            # Find next falling edge after this rising edge
            following = falling_edges[falling_edges > rising]
            if len(following) > 0:
                width = (following[0] - rising) / sample_rate
                pulse_widths.append(width)

        if pulse_widths:
            print("\nPulse width (high time):")
            print(f"  Average: {np.mean(pulse_widths) * 1e6:.2f} us")
            print(f"  Expected (50% duty): {1 / frequency / 2 * 1e6:.2f} us")

    # --- Threshold Sensitivity ---
    print("\n--- Threshold Sensitivity ---")

    # Add noise to signal
    noisy_square = square_wave + np.random.randn(n_samples) * 0.3
    noisy_trace = WaveformTrace(data=noisy_square, metadata=metadata)

    thresholds = [1.0, 1.65, 2.3]
    print("Testing different thresholds on noisy signal:")
    print(f"{'Threshold':<12} {'Rising':<10} {'Falling':<10}")
    print("-" * 35)

    for thresh in thresholds:
        rising = tk.find_rising_edges(noisy_trace, level=thresh, return_indices=True)
        falling = tk.find_falling_edges(noisy_trace, level=thresh, return_indices=True)
        print(f"{thresh:.2f}V{'':<7} {len(rising):<10} {len(falling):<10}")

    # --- Hysteresis Triggering ---
    print("\n--- Hysteresis Triggering ---")
    print("Using EdgeTrigger with high/low thresholds")

    trigger = tk.EdgeTrigger(
        level=1.65,
        edge="rising",
        hysteresis=0.5,  # 0.5V hysteresis band
    )

    # Use find_events for EdgeTrigger objects
    trigger_events = trigger.find_events(noisy_trace)
    trigger_points = [event.sample_index for event in trigger_events]

    print(
        f"Standard rising edges (1.65V): {len(tk.find_rising_edges(noisy_trace, level=1.65, return_indices=True))}"
    )
    print(f"With hysteresis (1.15V-2.15V): {len(trigger_points)}")
    print("Hysteresis reduces false triggers from noise")

    # --- Multi-Level Detection ---
    print("\n--- Multi-Level Signal ---")

    # Create 3-level signal (like RS-232)
    levels = np.array([0, 1.65, 3.3])
    multi_level = np.zeros(n_samples)
    segment_len = n_samples // 6
    multi_level[segment_len : 2 * segment_len] = 1.65
    multi_level[2 * segment_len : 3 * segment_len] = 3.3
    multi_level[3 * segment_len : 4 * segment_len] = 1.65
    multi_level[4 * segment_len : 5 * segment_len] = 0

    multi_trace = WaveformTrace(data=multi_level, metadata=metadata)

    # Detect transitions at different thresholds
    print("3-level signal (0V, 1.65V, 3.3V)")
    print(f"{'Threshold':<12} {'Rising':<10} {'Falling':<10}")
    print("-" * 35)

    for thresh in [0.8, 2.5]:
        rising = tk.find_rising_edges(multi_trace, level=thresh, return_indices=True)
        falling = tk.find_falling_edges(multi_trace, level=thresh, return_indices=True)
        print(f"{thresh:.1f}V{'':<8} {len(rising):<10} {len(falling):<10}")

    # --- Edge Timing Analysis ---
    print("\n--- Edge Timing Analysis ---")

    # Create signal with timing variations
    np.random.seed(42)
    jitter_ps = 100  # 100 ps RMS jitter
    jittery_edges = []
    edge_time = 0.0

    while edge_time < duration:
        jittery_edges.append(edge_time)
        # Add jitter to period
        period = (1 / frequency) + np.random.randn() * jitter_ps * 1e-12
        edge_time += period

    # Create signal from edges
    jittery_signal = np.zeros(n_samples)
    for i, edge in enumerate(jittery_edges):
        idx = int(edge * sample_rate)
        if idx < n_samples:
            # Alternate high/low
            end_idx = (
                int(jittery_edges[i + 1] * sample_rate) if i + 1 < len(jittery_edges) else n_samples
            )
            if i % 2 == 0:
                jittery_signal[idx:end_idx] = 3.3

    jittery_trace = WaveformTrace(data=jittery_signal, metadata=metadata)
    measured_edges = tk.find_rising_edges(jittery_trace, level=1.65, return_indices=True)

    if len(measured_edges) > 2:
        edge_times = measured_edges / sample_rate
        periods = np.diff(edge_times)

        print(f"Signal with {jitter_ps} ps RMS jitter:")
        print(f"  Measured period mean: {np.mean(periods) * 1e6:.4f} us")
        print(f"  Period jitter (std): {np.std(periods) * 1e12:.1f} ps")
        print(f"  Period jitter (p-p): {np.ptp(periods) * 1e12:.1f} ps")

    # --- Clock Recovery from Data ---
    print("\n--- Clock Recovery from Data ---")

    # Simulate data with embedded clock
    data_rate = 1e6  # 1 Mbps
    bit_period = 1 / data_rate
    n_bits = 100
    data_bits = np.random.randint(0, 2, n_bits)

    # Create NRZ data signal
    data_signal = np.zeros(n_samples)
    for i, bit in enumerate(data_bits):
        start = int(i * bit_period * sample_rate)
        end = int((i + 1) * bit_period * sample_rate)
        if end <= n_samples:
            data_signal[start:end] = 3.3 * bit

    data_trace = WaveformTrace(data=data_signal, metadata=metadata)

    # Find all transitions
    rising = tk.find_rising_edges(data_trace, level=1.65, return_indices=True)
    falling = tk.find_falling_edges(data_trace, level=1.65, return_indices=True)
    all_edges = np.sort(np.concatenate([rising, falling]))

    if len(all_edges) > 1:
        edge_intervals = np.diff(all_edges / sample_rate)
        min_interval = np.min(edge_intervals)
        estimated_bit_period = min_interval

        print(f"Data rate: {data_rate / 1e6:.0f} Mbps")
        print(f"Expected bit period: {bit_period * 1e6:.2f} us")
        print(f"Minimum edge interval: {min_interval * 1e6:.2f} us")
        print(f"Estimated data rate: {1 / estimated_bit_period / 1e6:.2f} Mbps")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. find_rising_edges() detects low-to-high transitions")
    print("  2. find_falling_edges() detects high-to-low transitions")
    print("  3. Threshold selection affects edge count")
    print("  4. Hysteresis reduces false triggers from noise")
    print("  5. Edge timing enables frequency and jitter measurement")
    print("  6. Minimum edge interval indicates data rate")
    print("=" * 60)


if __name__ == "__main__":
    main()
