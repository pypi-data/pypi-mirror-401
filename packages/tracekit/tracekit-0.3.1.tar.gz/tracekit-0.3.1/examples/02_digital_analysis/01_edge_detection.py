#!/usr/bin/env python3
"""Example: Edge Detection and Digital Analysis.

This example demonstrates detecting edges in digital signals
and performing timing analysis.

Time: 15 minutes
Prerequisites: Basic measurements

Run:
    uv run python examples/02_digital_analysis/01_edge_detection.py
"""

import statistics

import tracekit as tk
from tracekit.testing import generate_square_wave


def main() -> None:
    """Demonstrate edge detection and digital analysis."""
    print("=" * 60)
    print("TraceKit Example: Edge Detection and Digital Analysis")
    print("=" * 60)

    # --- Generate Test Signal ---
    print("\n--- Generating Test Signal ---")

    # Generate a square wave with known characteristics
    square = generate_square_wave(
        frequency=1e6,  # 1 MHz
        duty_cycle=0.4,  # 40% duty cycle
        sample_rate=100e6,  # 100 MSa/s
        duration=10e-6,  # 10 us
        low=0.0,  # 0V low level
        high=3.3,  # 3.3V high level
    )

    print("Generated 1 MHz square wave:")
    print("  Duty cycle: 40%")
    print("  Levels: 0V to 3.3V")
    print(f"  Samples: {len(square.data)}")
    print(f"  Duration: {square.duration * 1e6:.1f} us")

    # --- Basic Edge Detection ---
    print("\n--- Basic Edge Detection ---")

    # Find rising and falling edges separately
    rising_times = tk.find_rising_edges(square)
    falling_times = tk.find_falling_edges(square)

    print("Detected edges:")
    print(f"  Total: {len(rising_times) + len(falling_times)}")
    print(f"  Rising: {len(rising_times)}")
    print(f"  Falling: {len(falling_times)}")

    # --- Edge Timing ---
    print("\n--- Edge Timing ---")

    # Combine and sort edges for sequential analysis
    all_edges = []
    for t in rising_times:
        all_edges.append((t, "rising"))
    for t in falling_times:
        all_edges.append((t, "falling"))
    all_edges.sort(key=lambda x: x[0])

    print("\nFirst 6 edges:")
    for i, (time, edge_type) in enumerate(all_edges[:6]):
        print(f"  {i + 1}. {time * 1e9:8.1f} ns: {edge_type}")

    # Calculate period from rising edges
    if len(rising_times) >= 2:
        period = rising_times[1] - rising_times[0]
        frequency = 1.0 / period
        print("\nCalculated from rising edges:")
        print(f"  Period: {period * 1e9:.1f} ns")
        print(f"  Frequency: {frequency / 1e6:.3f} MHz")

    # --- Custom Threshold ---
    print("\n--- Custom Threshold ---")

    # Use different thresholds (levels)
    levels = [0.5, 1.65, 2.5]  # Different voltage levels
    for level in levels:
        edges = tk.find_rising_edges(square, level=level)
        print(f"  Level {level:.2f}V: {len(edges)} rising edges")

    # --- Pulse Width Analysis ---
    print("\n--- Pulse Width Analysis ---")

    # Calculate high and low pulse widths
    high_widths = []
    low_widths = []

    for i in range(len(all_edges) - 1):
        t1, type1 = all_edges[i]
        t2, type2 = all_edges[i + 1]
        width = t2 - t1

        if type1 == "rising":  # Rising to falling = high time
            high_widths.append(width)
        else:  # Falling to rising = low time
            low_widths.append(width)

    if high_widths and low_widths:
        avg_high = statistics.mean(high_widths)
        avg_low = statistics.mean(low_widths)
        calc_duty = avg_high / (avg_high + avg_low)

        print("Pulse width analysis:")
        print(f"  Average high time: {avg_high * 1e9:.1f} ns")
        print(f"  Average low time: {avg_low * 1e9:.1f} ns")
        print(f"  Calculated duty cycle: {calc_duty * 100:.1f}%")
        print("  Expected duty cycle: 40.0%")

    # --- Jitter Analysis ---
    print("\n--- Simple Jitter Analysis ---")

    if len(rising_times) >= 3:
        periods = []
        for i in range(len(rising_times) - 1):
            period = rising_times[i + 1] - rising_times[i]
            periods.append(period)

        mean_period = statistics.mean(periods)
        if len(periods) > 1:
            std_period = statistics.stdev(periods)
            jitter_percent = (std_period / mean_period) * 100

            print(f"Period jitter (from {len(periods)} periods):")
            print(f"  Mean period: {mean_period * 1e9:.2f} ns")
            print(f"  Std deviation: {std_period * 1e12:.2f} ps")
            print(f"  Jitter: {jitter_percent:.4f}%")
        else:
            print(f"  Mean period: {mean_period * 1e9:.2f} ns")
            print("  (Need more periods for jitter calculation)")

    # --- Glitch Detection ---
    print("\n--- Glitch Detection ---")

    # A glitch is a pulse shorter than expected
    expected_min_pulse = 100e-9  # 100 ns minimum expected

    print(f"Looking for pulses shorter than {expected_min_pulse * 1e9:.0f} ns:")

    all_widths = high_widths + low_widths
    glitches = [w for w in all_widths if w < expected_min_pulse]

    if glitches:
        print(f"  Found {len(glitches)} glitches!")
        for g in glitches[:5]:
            print(f"    Pulse width: {g * 1e9:.1f} ns")
    else:
        print("  No glitches found (all pulses >= expected minimum)")

    # --- Frequency Stability ---
    print("\n--- Frequency Stability ---")

    if len(rising_times) >= 2:
        periods = [rising_times[i + 1] - rising_times[i] for i in range(len(rising_times) - 1)]
        freqs = [1.0 / p for p in periods]

        min_freq = min(freqs)
        max_freq = max(freqs)
        avg_freq = statistics.mean(freqs)

        print("Frequency stability:")
        print(f"  Minimum: {min_freq / 1e6:.6f} MHz")
        print(f"  Maximum: {max_freq / 1e6:.6f} MHz")
        print(f"  Average: {avg_freq / 1e6:.6f} MHz")
        print(f"  Spread: {(max_freq - min_freq) / 1e3:.2f} kHz")

    # --- Edge with Hysteresis ---
    print("\n--- Edge Detection with Hysteresis ---")
    print("Hysteresis prevents false triggers on noisy signals")

    # Compare edge counts with and without hysteresis
    edges_no_hyst = tk.find_rising_edges(square, hysteresis=0.0)
    edges_with_hyst = tk.find_rising_edges(square, hysteresis=0.1)  # 100mV hysteresis

    print(f"  Without hysteresis: {len(edges_no_hyst)} rising edges")
    print(f"  With 0.1V hysteresis: {len(edges_with_hyst)} rising edges")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. tk.find_rising_edges() returns edge times in seconds")
    print("  2. tk.find_falling_edges() returns falling edge times")
    print("  3. Use 'level' parameter for custom threshold")
    print("  4. Use 'hysteresis' for noisy signals")
    print("  5. Period = time between consecutive rising edges")
    print("  6. Duty cycle = high_time / (high_time + low_time)")
    print("=" * 60)


if __name__ == "__main__":
    main()
