#!/usr/bin/env python3
"""Example 06: Eye Diagram Generation and Analysis.

This example demonstrates eye diagram generation for signal integrity
analysis of serial data links.

Time: 25 minutes
Prerequisites: Spectral analysis, jitter concepts

Run:
    uv run python examples/05_advanced/06_eye_diagram.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import numpy as np

from tracekit.analyzers.eye import (
    auto_center_eye_diagram,
    generate_eye,
)
from tracekit.analyzers.eye.metrics import (
    measure_eye_height,
    measure_eye_width,
    measure_jitter_from_eye,
)
from tracekit.core.types import TraceMetadata, WaveformTrace


def main() -> None:
    """Demonstrate eye diagram generation and analysis."""
    print("=" * 60)
    print("TraceKit Example: Eye Diagram Generation")
    print("=" * 60)

    # --- Eye Diagram Overview ---
    print("\n--- Eye Diagram Overview ---")

    print_eye_overview()

    # --- Basic Eye Diagram ---
    print("\n--- Basic Eye Diagram Generation ---")

    demo_basic_eye()

    # --- Eye Metrics ---
    print("\n--- Eye Diagram Metrics ---")

    demo_eye_metrics()

    # --- Jitter Effects ---
    print("\n--- Jitter Effects on Eye Diagram ---")

    demo_jitter_effects()

    # --- Auto-Centering ---
    print("\n--- Eye Diagram Auto-Centering ---")

    demo_auto_centering()

    # --- High-Speed Serial Analysis ---
    print("\n--- High-Speed Serial Link Analysis ---")

    demo_serial_analysis()

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. Eye diagrams visualize signal quality over many UI")
    print("  2. Eye height indicates noise margin")
    print("  3. Eye width indicates timing margin (jitter)")
    print("  4. Histogram shows transition density distribution")
    print("  5. Use auto-centering for optimal alignment")
    print("=" * 60)


def print_eye_overview() -> None:
    """Print eye diagram overview."""
    print("Eye Diagram Fundamentals:")
    print("-" * 40)
    print("  - Created by folding waveform at Unit Interval (UI)")
    print("  - UI = bit period (1/data_rate)")
    print("  - Eye opening indicates margin for sampling")
    print("\nKey measurements:")
    print("  - Eye Height: Vertical opening (noise margin)")
    print("  - Eye Width: Horizontal opening (timing margin)")
    print("  - Jitter: Variation in edge positions")
    print("  - Crossing Level: Where transitions intersect")
    print("\nTypical applications:")
    print("  - PCIe, USB, SATA, Ethernet validation")
    print("  - SerDes characterization")
    print("  - Channel quality assessment")


def demo_basic_eye() -> None:
    """Demonstrate basic eye diagram generation."""
    # Generate a serial data signal
    sample_rate = 10e9  # 10 GHz
    data_rate = 1e9  # 1 Gbps
    ui = 1.0 / data_rate  # Unit interval

    n_bits = 500
    samples_per_bit = int(sample_rate / data_rate)

    # Generate PRBS-like data pattern
    np.random.seed(42)
    bits = np.random.randint(0, 2, n_bits)

    # Create NRZ signal with realistic transitions
    signal = create_nrz_signal(
        bits,
        samples_per_bit=samples_per_bit,
        rise_time=ui * 0.2,  # 20% of UI
        sample_rate=sample_rate,
        amplitude=0.8,  # 800 mV swing
    )

    # Add noise
    signal += np.random.randn(len(signal)) * 0.02

    # Create trace
    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="serial_data")
    trace = WaveformTrace(data=signal, metadata=metadata)

    print("Serial data signal:")
    print(f"  Data rate: {data_rate / 1e9:.1f} Gbps")
    print(f"  Unit interval: {ui * 1e12:.0f} ps")
    print(f"  Sample rate: {sample_rate / 1e9:.0f} GHz")
    print(f"  Rise time: {ui * 0.2 * 1e12:.0f} ps")

    # Generate eye diagram
    eye = generate_eye(
        trace,
        unit_interval=ui,
        n_ui=2,  # 2-UI eye
        trigger_level=0.5,
        trigger_edge="rising",
        generate_histogram=True,
    )

    print("\nEye diagram generated:")
    print(f"  Traces overlaid: {eye.n_traces}")
    print(f"  Samples per UI: {eye.samples_per_ui}")
    print(f"  Time span: {eye.n_traces} UI")

    if eye.histogram is not None:
        print(f"  Histogram shape: {eye.histogram.shape}")


def demo_eye_metrics() -> None:
    """Demonstrate eye diagram metric measurements."""
    sample_rate = 20e9
    data_rate = 2.5e9  # 2.5 Gbps
    ui = 1.0 / data_rate

    n_bits = 1000
    samples_per_bit = int(sample_rate / data_rate)

    np.random.seed(123)
    bits = np.random.randint(0, 2, n_bits)

    signal = create_nrz_signal(
        bits,
        samples_per_bit=samples_per_bit,
        rise_time=ui * 0.15,
        sample_rate=sample_rate,
        amplitude=0.5,
    )

    # Add controlled noise and jitter
    signal += np.random.randn(len(signal)) * 0.015

    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="data")
    trace = WaveformTrace(data=signal, metadata=metadata)

    eye = generate_eye(trace, unit_interval=ui, n_ui=2)

    # Measure eye metrics
    eye_height = measure_eye_height(eye)
    eye_width = measure_eye_width(eye)
    jitter = measure_jitter_from_eye(eye)

    print(f"Eye Diagram Metrics ({data_rate / 1e9:.1f} Gbps):")
    print("-" * 40)
    print("\nEye Height:")
    print(f"  Opening: {eye_height.opening_volts * 1e3:.1f} mV")
    print(f"  High level: {eye_height.high_level * 1e3:.1f} mV")
    print(f"  Low level: {eye_height.low_level * 1e3:.1f} mV")
    print(f"  Margin: {eye_height.margin_percent:.1f}%")

    print("\nEye Width:")
    print(f"  Opening: {eye_width.opening_ui:.2f} UI ({eye_width.opening_seconds * 1e12:.1f} ps)")
    print(f"  Left crossing: {eye_width.left_crossing_ui:.2f} UI")
    print(f"  Right crossing: {eye_width.right_crossing_ui:.2f} UI")
    print(f"  Margin: {eye_width.margin_percent:.1f}%")

    print("\nJitter (from eye):")
    print(f"  RMS: {jitter.rms_seconds * 1e12:.1f} ps ({jitter.rms_ui:.3f} UI)")
    print(f"  Peak-to-peak: {jitter.pp_seconds * 1e12:.1f} ps ({jitter.pp_ui:.3f} UI)")


def demo_jitter_effects() -> None:
    """Demonstrate how jitter affects eye diagram."""
    sample_rate = 10e9
    data_rate = 1e9
    ui = 1.0 / data_rate

    n_bits = 500
    samples_per_bit = int(sample_rate / data_rate)

    np.random.seed(42)
    bits = np.random.randint(0, 2, n_bits)

    jitter_levels = [0, 0.05, 0.10, 0.20]  # UI

    print("Jitter impact on eye opening:")
    print("-" * 50)
    print(f"{'Jitter (UI)':>12} {'Eye Width (UI)':>15} {'Eye Height (mV)':>16}")
    print("-" * 50)

    for jitter_ui in jitter_levels:
        signal = create_nrz_signal_with_jitter(
            bits,
            samples_per_bit=samples_per_bit,
            rise_time=ui * 0.2,
            sample_rate=sample_rate,
            amplitude=0.5,
            jitter_rms=jitter_ui * ui,
        )

        # Add noise
        signal += np.random.randn(len(signal)) * 0.01

        metadata = TraceMetadata(sample_rate=sample_rate, channel_name="data")
        trace = WaveformTrace(data=signal, metadata=metadata)

        eye = generate_eye(trace, unit_interval=ui, n_ui=2)

        eye_height = measure_eye_height(eye)
        eye_width = measure_eye_width(eye)

        print(
            f"{jitter_ui:>12.2f} {eye_width.opening_ui:>15.2f} "
            f"{eye_height.opening_volts * 1e3:>16.1f}"
        )

    print("\nNote: Increasing jitter closes the eye horizontally")


def demo_auto_centering() -> None:
    """Demonstrate eye diagram auto-centering."""
    sample_rate = 10e9
    data_rate = 1e9
    ui = 1.0 / data_rate

    n_bits = 500
    samples_per_bit = int(sample_rate / data_rate)

    np.random.seed(42)
    bits = np.random.randint(0, 2, n_bits)

    signal = create_nrz_signal(
        bits,
        samples_per_bit=samples_per_bit,
        rise_time=ui * 0.2,
        sample_rate=sample_rate,
        amplitude=0.5,
    )
    signal += np.random.randn(len(signal)) * 0.01

    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="data")
    trace = WaveformTrace(data=signal, metadata=metadata)

    # Generate eye without centering
    eye_raw = generate_eye(trace, unit_interval=ui, n_ui=2)

    # Apply auto-centering
    eye_centered = auto_center_eye_diagram(eye_raw, trigger_fraction=0.5)

    # Measure both
    height_raw = measure_eye_height(eye_raw)
    height_centered = measure_eye_height(eye_centered)

    print("Auto-centering comparison:")
    print("-" * 40)
    print("\nRaw eye diagram:")
    print(f"  Eye height: {height_raw.opening_volts * 1e3:.1f} mV")

    print("\nCentered eye diagram:")
    print(f"  Eye height: {height_centered.opening_volts * 1e3:.1f} mV")

    if height_centered.opening_volts > height_raw.opening_volts:
        improvement = (
            (height_centered.opening_volts - height_raw.opening_volts)
            / height_raw.opening_volts
            * 100
        )
        print(f"\nCentering improved eye height by {improvement:.1f}%")


def demo_serial_analysis() -> None:
    """Demonstrate analysis of a high-speed serial link."""
    # Simulate a 5 Gbps link
    sample_rate = 50e9  # 50 GHz
    data_rate = 5e9  # 5 Gbps
    ui = 1.0 / data_rate  # 200 ps

    n_bits = 2000
    samples_per_bit = int(sample_rate / data_rate)

    np.random.seed(456)
    bits = np.random.randint(0, 2, n_bits)

    # Realistic link parameters
    amplitude = 0.4  # 400 mV swing (200 mV per level)
    rise_time = 40e-12  # 40 ps rise time
    jitter_rms = 5e-12  # 5 ps RMS jitter
    noise_rms = 0.010  # 10 mV noise

    signal = create_nrz_signal_with_jitter(
        bits,
        samples_per_bit=samples_per_bit,
        rise_time=rise_time,
        sample_rate=sample_rate,
        amplitude=amplitude,
        jitter_rms=jitter_rms,
    )
    signal += np.random.randn(len(signal)) * noise_rms

    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="serial_5g")
    trace = WaveformTrace(data=signal, metadata=metadata)

    print("5 Gbps Serial Link Analysis:")
    print("-" * 40)
    print("\nLink parameters:")
    print(f"  Data rate: {data_rate / 1e9:.0f} Gbps")
    print(f"  Unit interval: {ui * 1e12:.0f} ps")
    print(f"  Amplitude: {amplitude * 1e3:.0f} mV")
    print(f"  Rise time: {rise_time * 1e12:.0f} ps")
    print(f"  Jitter: {jitter_rms * 1e12:.0f} ps RMS")
    print(f"  Noise: {noise_rms * 1e3:.0f} mV RMS")

    # Generate and analyze eye
    eye = generate_eye(trace, unit_interval=ui, n_ui=2, max_traces=500)
    eye = auto_center_eye_diagram(eye)

    eye_height = measure_eye_height(eye)
    eye_width = measure_eye_width(eye)
    jitter_measured = measure_jitter_from_eye(eye)

    print("\nMeasured eye parameters:")
    print(f"  Eye height: {eye_height.opening_volts * 1e3:.1f} mV")
    print(f"  Eye width: {eye_width.opening_ui:.2f} UI ({eye_width.opening_seconds * 1e12:.1f} ps)")
    print(f"  Jitter RMS: {jitter_measured.rms_seconds * 1e12:.1f} ps")
    print(f"  Jitter P-P: {jitter_measured.pp_seconds * 1e12:.1f} ps")

    # Pass/fail against typical spec
    eye_height_spec = 0.1  # 100 mV minimum
    eye_width_spec = 0.3  # 0.3 UI minimum

    print("\nSpecification check:")
    print(
        f"  Eye height >= {eye_height_spec * 1e3:.0f} mV: "
        f"{'PASS' if eye_height.opening_volts >= eye_height_spec else 'FAIL'}"
    )
    print(
        f"  Eye width >= {eye_width_spec:.1f} UI: "
        f"{'PASS' if eye_width.opening_ui >= eye_width_spec else 'FAIL'}"
    )


# --- Signal Generation Helpers ---


def create_nrz_signal(
    bits: np.ndarray,
    samples_per_bit: int,
    rise_time: float,
    sample_rate: float,
    amplitude: float,
) -> np.ndarray:
    """Create NRZ signal with smooth transitions."""
    n_bits = len(bits)
    n_samples = n_bits * samples_per_bit

    signal = np.zeros(n_samples)
    rise_samples = int(rise_time * sample_rate)

    for i, bit in enumerate(bits):
        start = i * samples_per_bit
        end = start + samples_per_bit

        target_level = amplitude / 2 if bit else -amplitude / 2

        if i > 0 and bits[i] != bits[i - 1]:
            # Transition needed
            prev_level = amplitude / 2 if bits[i - 1] else -amplitude / 2
            transition_end = min(start + rise_samples, end)

            # S-curve transition
            t = np.linspace(0, 1, transition_end - start)
            sigmoid = 1 / (1 + np.exp(-6 * (t - 0.5)))
            signal[start:transition_end] = prev_level + (target_level - prev_level) * sigmoid
            signal[transition_end:end] = target_level
        else:
            signal[start:end] = target_level

    return signal


def create_nrz_signal_with_jitter(
    bits: np.ndarray,
    samples_per_bit: int,
    rise_time: float,
    sample_rate: float,
    amplitude: float,
    jitter_rms: float,
) -> np.ndarray:
    """Create NRZ signal with timing jitter on edges."""
    n_bits = len(bits)
    n_samples = n_bits * samples_per_bit

    signal = np.zeros(n_samples)
    rise_samples = int(rise_time * sample_rate)

    # Generate jitter for each bit edge
    np.random.seed()  # Different seed for jitter
    jitter_samples = (np.random.randn(n_bits) * jitter_rms * sample_rate).astype(int)

    cumulative_offset = 0

    for i, bit in enumerate(bits):
        start = i * samples_per_bit + cumulative_offset
        jitter = jitter_samples[i]
        cumulative_offset += jitter

        end = min(start + samples_per_bit, n_samples)
        if start < 0:
            start = 0

        if start >= n_samples:
            break

        target_level = amplitude / 2 if bit else -amplitude / 2

        if i > 0 and bits[i] != bits[i - 1]:
            prev_level = amplitude / 2 if bits[i - 1] else -amplitude / 2
            transition_end = min(start + rise_samples, end, n_samples)

            if transition_end > start:
                t = np.linspace(0, 1, transition_end - start)
                sigmoid = 1 / (1 + np.exp(-6 * (t - 0.5)))
                signal[start:transition_end] = prev_level + (target_level - prev_level) * sigmoid

            if end > transition_end:
                signal[transition_end:end] = target_level
        else:
            signal[start:end] = target_level

    return signal


if __name__ == "__main__":
    main()
