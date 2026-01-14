#!/usr/bin/env python3
"""Example 05: Multi-Channel Digital Analysis.

This example demonstrates multi-channel correlation, time alignment,
and cross-channel analysis for digital signals.

Time: 25 minutes
Prerequisites: Edge detection, bus decoding basics

Run:
    uv run python examples/02_digital_analysis/05_multi_channel.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import numpy as np

from tracekit.analyzers.digital.correlation import (
    ChannelSkewResult,
    CrossCorrelationResult,
    align_by_trigger,
    correlate_channels,
    measure_channel_skew,
)
from tracekit.core.types import DigitalTrace, TraceMetadata


def main() -> None:
    """Demonstrate multi-channel digital analysis."""
    print("=" * 60)
    print("TraceKit Example: Multi-Channel Digital Analysis")
    print("=" * 60)

    # --- Cross-Channel Correlation ---
    print("\n--- Cross-Channel Correlation ---")

    demo_cross_correlation()

    # --- Time Alignment ---
    print("\n--- Trigger-Based Time Alignment ---")

    demo_time_alignment()

    # --- Channel Skew Measurement ---
    print("\n--- Channel Skew Measurement ---")

    demo_skew_measurement()

    # --- Multi-Channel Clock Analysis ---
    print("\n--- Multi-Channel Clock Analysis ---")

    demo_multi_clock_analysis()

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. correlate_channels() finds time delay between signals")
    print("  2. align_by_trigger() aligns channels to common trigger")
    print("  3. measure_channel_skew() quantifies timing differences")
    print("  4. Multi-channel analysis helps debug timing issues")
    print("  5. Cross-correlation works even with noise")
    print("=" * 60)


def demo_cross_correlation() -> None:
    """Demonstrate cross-channel correlation for delay measurement."""
    sample_rate = 1e9  # 1 GHz
    duration = 10e-6  # 10 microseconds

    # Generate reference channel (square wave)
    n_samples = int(sample_rate * duration)
    freq = 1e6  # 1 MHz

    t = np.arange(n_samples) / sample_rate
    reference = (np.sin(2 * np.pi * freq * t) > 0).astype(float)

    # Generate delayed channel (same signal, delayed by 50 ns)
    delay_ns = 50
    delay_samples = int(delay_ns * 1e-9 * sample_rate)

    delayed = np.zeros(n_samples)
    delayed[delay_samples:] = reference[:-delay_samples]

    # Add some noise
    reference += np.random.randn(n_samples) * 0.05
    delayed += np.random.randn(n_samples) * 0.05

    # Create traces
    ref_metadata = TraceMetadata(sample_rate=sample_rate, channel_name="CLK_REF")
    del_metadata = TraceMetadata(sample_rate=sample_rate, channel_name="CLK_DELAYED")

    ref_trace = DigitalTrace(data=(reference > 0.5), metadata=ref_metadata)
    del_trace = DigitalTrace(data=(delayed > 0.5), metadata=del_metadata)

    # Correlate channels
    result: CrossCorrelationResult = correlate_channels(ref_trace, del_trace)

    print("Reference channel: CLK_REF (1 MHz)")
    print(f"Delayed channel: CLK_DELAYED (+{delay_ns} ns delay)")
    print("\nCross-correlation results:")
    print(f"  Measured delay: {result.delay_seconds * 1e9:.1f} ns")
    print(f"  Expected delay: {delay_ns:.1f} ns")
    print(f"  Correlation peak: {result.correlation_peak:.3f}")
    print(f"  Error: {abs(result.delay_seconds * 1e9 - delay_ns):.2f} ns")


def demo_time_alignment() -> None:
    """Demonstrate trigger-based time alignment of multiple channels."""
    sample_rate = 500e6  # 500 MHz
    n_samples = 10000

    # Create multiple channels with different trigger positions
    # Simulate data capture with trigger jitter
    channels = {}

    base_trigger = 2000  # Base trigger position

    channel_names = ["DATA", "CLK", "ENABLE", "STATUS"]
    trigger_offsets = [0, 15, -8, 23]  # Sample offsets from ideal trigger

    for name, offset in zip(channel_names, trigger_offsets, strict=False):
        # Create a pattern with clear trigger point
        signal = np.zeros(n_samples)

        # Place trigger event (rising edge) at offset position
        trigger_pos = base_trigger + offset
        signal[trigger_pos:] = 1.0

        # Add some pre-trigger activity
        pre_activity = np.sin(2 * np.pi * 10e6 * np.arange(trigger_pos) / sample_rate)
        signal[:trigger_pos] = (pre_activity > 0).astype(float) * 0.3

        # Add noise
        signal += np.random.randn(n_samples) * 0.02

        metadata = TraceMetadata(sample_rate=sample_rate, channel_name=name)
        channels[name] = DigitalTrace(data=(signal > 0.5), metadata=metadata)

    print("Original trigger positions (samples from start):")
    for name, offset in zip(channel_names, trigger_offsets, strict=False):
        print(f"  {name}: {base_trigger + offset}")

    # Align all channels to DATA channel trigger
    reference_channel = "DATA"
    aligned = align_by_trigger(
        channels,
        reference=reference_channel,
        trigger_edge="rising",
        threshold=0.5,
    )

    print(f"\nAligned to {reference_channel} trigger:")
    print("  All channels now synchronized to common time base")
    print(f"  Alignment window: {aligned['window_start']} to {aligned['window_end']} samples")

    # Show alignment results
    print("\nAlignment offsets applied:")
    for name in channel_names:
        if name in aligned.get("offsets", {}):
            offset = aligned["offsets"][name]
            print(f"  {name}: {offset:+d} samples ({offset / sample_rate * 1e9:+.1f} ns)")


def demo_skew_measurement() -> None:
    """Demonstrate precise channel skew measurement."""
    sample_rate = 2e9  # 2 GHz for precise timing
    duration = 5e-6

    n_samples = int(sample_rate * duration)

    # Generate a clock signal
    clock_freq = 100e6  # 100 MHz
    t = np.arange(n_samples) / sample_rate
    clock = (np.sin(2 * np.pi * clock_freq * t) > 0).astype(float)

    # Create data signal with setup/hold relationship
    # Data changes just before clock edge
    setup_time_ns = 2.5  # 2.5 ns setup time
    setup_samples = int(setup_time_ns * 1e-9 * sample_rate)

    data = np.zeros(n_samples)
    # Data transitions setup_samples before clock rising edges
    clock_edges = np.where((clock[:-1] == 0) & (clock[1:] == 1))[0]

    for i, edge in enumerate(clock_edges):
        data_start = max(0, edge - setup_samples)
        data_end = min(n_samples, edge + int(sample_rate / clock_freq / 2))
        data[data_start:data_end] = i % 2  # Alternating pattern

    # Add small noise
    clock += np.random.randn(n_samples) * 0.02
    data += np.random.randn(n_samples) * 0.02

    # Create traces
    clock_meta = TraceMetadata(sample_rate=sample_rate, channel_name="CLK")
    data_meta = TraceMetadata(sample_rate=sample_rate, channel_name="DATA")

    clock_trace = DigitalTrace(data=(clock > 0.5), metadata=clock_meta)
    data_trace = DigitalTrace(data=(data > 0.5), metadata=data_meta)

    # Measure skew
    result: ChannelSkewResult = measure_channel_skew(
        clock_trace,
        data_trace,
        reference_edge="rising",
    )

    print(f"Clock frequency: {clock_freq / 1e6:.0f} MHz")
    print(f"Expected setup time: {setup_time_ns:.1f} ns")
    print("\nSkew measurement results:")
    print(f"  Mean skew: {result.mean_skew_seconds * 1e9:.2f} ns")
    print(f"  Std dev: {result.std_skew_seconds * 1e9:.2f} ns")
    print(f"  Min skew: {result.min_skew_seconds * 1e9:.2f} ns")
    print(f"  Max skew: {result.max_skew_seconds * 1e9:.2f} ns")
    print(f"  Measurements: {result.n_measurements}")

    # Setup/hold analysis
    setup_margin = setup_time_ns - result.mean_skew_seconds * 1e9
    print(f"\nSetup margin: {setup_margin:.2f} ns")


def demo_multi_clock_analysis() -> None:
    """Demonstrate multi-clock domain analysis."""
    sample_rate = 4e9  # 4 GHz
    duration = 2e-6

    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate

    # Create multiple clock domains
    clocks = {
        "CLK_100M": {"freq": 100e6, "phase": 0},
        "CLK_50M": {"freq": 50e6, "phase": 0},
        "CLK_33M": {"freq": 33.33e6, "phase": np.pi / 4},
    }

    traces = {}
    for name, params in clocks.items():
        signal = np.sin(2 * np.pi * params["freq"] * t + params["phase"]) > 0
        metadata = TraceMetadata(sample_rate=sample_rate, channel_name=name)
        traces[name] = DigitalTrace(data=signal, metadata=metadata)

    print("Multi-clock domain analysis:")
    print("-" * 40)

    # Analyze each clock
    for name, trace in traces.items():
        # Count rising edges
        data = trace.data.astype(int)
        rising_edges = np.where((data[:-1] == 0) & (data[1:] == 1))[0]

        if len(rising_edges) >= 2:
            periods = np.diff(rising_edges) / sample_rate
            mean_freq = 1.0 / np.mean(periods)
            freq_std = np.std(1.0 / periods)

            print(f"\n{name}:")
            print(f"  Expected frequency: {clocks[name]['freq'] / 1e6:.2f} MHz")
            print(f"  Measured frequency: {mean_freq / 1e6:.2f} MHz")
            print(f"  Frequency jitter: {freq_std / 1e3:.1f} kHz")
            print(f"  Rising edges detected: {len(rising_edges)}")

    # Cross-domain correlation
    print("\nCross-domain correlations:")
    print("-" * 40)

    pairs = [("CLK_100M", "CLK_50M"), ("CLK_100M", "CLK_33M"), ("CLK_50M", "CLK_33M")]

    for ch1, ch2 in pairs:
        result = correlate_channels(traces[ch1], traces[ch2])
        print(f"  {ch1} vs {ch2}:")
        print(f"    Correlation: {result.correlation_peak:.3f}")
        print(f"    Phase offset: {result.delay_seconds * 1e9:.1f} ns")


if __name__ == "__main__":
    main()
