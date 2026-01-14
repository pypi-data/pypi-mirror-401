#!/usr/bin/env python3
"""Example 05: Automatic Protocol Detection.

This example demonstrates automatic protocol detection and parameter
inference for unknown serial communications.

Time: 20 minutes
Prerequisites: Basic protocol concepts

Run:
    uv run python examples/04_protocol_decoding/05_auto_detection.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import numpy as np

from tracekit.core.types import DigitalTrace, TraceMetadata, WaveformTrace
from tracekit.inference import (
    assess_signal_quality,
    classify_signal,
    detect_logic_family,
    detect_protocol,
    recommend_analyses,
)


def main() -> None:
    """Demonstrate automatic protocol detection."""
    print("=" * 60)
    print("TraceKit Example: Automatic Protocol Detection")
    print("=" * 60)

    # --- Signal Classification ---
    print("\n--- Signal Classification ---")

    demo_signal_classification()

    # --- Logic Family Detection ---
    print("\n--- Logic Family Detection ---")

    demo_logic_family()

    # --- Protocol Detection ---
    print("\n--- Protocol Detection ---")

    demo_protocol_detection()

    # --- Analysis Recommendations ---
    print("\n--- Analysis Recommendations ---")

    demo_analysis_recommendations()

    # --- Complete Auto-Analysis Workflow ---
    print("\n--- Complete Auto-Analysis Workflow ---")

    demo_auto_workflow()

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. classify_signal() determines signal type (digital/analog)")
    print("  2. detect_logic_family() identifies voltage levels")
    print("  3. detect_protocol() identifies serial protocols")
    print("  4. recommend_analyses() suggests appropriate measurements")
    print("  5. Auto-detection enables rapid initial analysis")
    print("=" * 60)


def demo_signal_classification() -> None:
    """Demonstrate automatic signal classification."""
    sample_rate = 100e6  # 100 MHz
    duration = 10e-6
    n_samples = int(sample_rate * duration)

    t = np.arange(n_samples) / sample_rate

    signals = {
        "Digital Square": (np.sin(2 * np.pi * 1e6 * t) > 0).astype(float) * 3.3,
        "Analog Sine": 1.65 + 1.65 * np.sin(2 * np.pi * 500e3 * t),
        "Digital PWM": (np.sin(2 * np.pi * 100e3 * t) > 0.7).astype(float) * 5.0,
        "Noisy Digital": (
            (np.sin(2 * np.pi * 1e6 * t) > 0).astype(float) * 3.3 + np.random.randn(n_samples) * 0.3
        ),
    }

    print("Signal classification results:")
    print("-" * 50)

    for name, signal_data in signals.items():
        metadata = TraceMetadata(sample_rate=sample_rate, channel_name=name)
        trace = WaveformTrace(data=signal_data, metadata=metadata)

        classification = classify_signal(trace)

        print(f"\n{name}:")
        print(f"  Signal type: {classification.signal_type}")
        print(f"  Confidence: {classification.confidence:.1%}")
        if hasattr(classification, "characteristics"):
            for key, value in classification.characteristics.items():
                print(f"  {key}: {value}")


def demo_logic_family() -> None:
    """Demonstrate logic family detection."""
    sample_rate = 100e6
    duration = 10e-6
    n_samples = int(sample_rate * duration)

    t = np.arange(n_samples) / sample_rate

    logic_levels = {
        "TTL": {"low": 0.0, "high": 5.0, "threshold": 1.4},
        "CMOS 3.3V": {"low": 0.0, "high": 3.3, "threshold": 1.65},
        "LVTTL": {"low": 0.0, "high": 3.3, "threshold": 1.5},
        "LVCMOS 1.8V": {"low": 0.0, "high": 1.8, "threshold": 0.9},
    }

    print("Logic family detection:")
    print("-" * 50)

    for family_name, levels in logic_levels.items():
        # Generate digital signal with appropriate levels
        digital = (np.sin(2 * np.pi * 1e6 * t) > 0).astype(float)
        signal_data = digital * levels["high"] + (1 - digital) * levels["low"]

        # Add small noise
        signal_data += np.random.randn(n_samples) * 0.02

        metadata = TraceMetadata(sample_rate=sample_rate, channel_name=family_name)
        trace = WaveformTrace(data=signal_data, metadata=metadata)

        detected = detect_logic_family(trace)

        print(f"\n{family_name} signal:")
        print(f"  Detected family: {detected.family}")
        print(f"  High level: {detected.high_level:.2f}V")
        print(f"  Low level: {detected.low_level:.2f}V")
        print(f"  Threshold: {detected.threshold:.2f}V")
        print(f"  Confidence: {detected.confidence:.1%}")


def demo_protocol_detection() -> None:
    """Demonstrate automatic protocol detection."""
    sample_rate = 10e6  # 10 MHz

    protocols = {
        "UART 115200": generate_uart_like(sample_rate, 115200),
        "UART 9600": generate_uart_like(sample_rate, 9600),
        "SPI-like": generate_spi_like(sample_rate),
        "I2C-like": generate_i2c_like(sample_rate),
    }

    print("Protocol detection:")
    print("-" * 50)

    for name, signal_data in protocols.items():
        metadata = TraceMetadata(sample_rate=sample_rate, channel_name=name)
        trace = DigitalTrace(data=signal_data, metadata=metadata)

        detected = detect_protocol(trace)

        print(f"\n{name}:")
        print(f"  Detected protocol: {detected.protocol}")
        print(f"  Confidence: {detected.confidence:.1%}")
        if detected.parameters:
            print("  Parameters:")
            for param, value in detected.parameters.items():
                if isinstance(value, float):
                    print(f"    {param}: {value:.0f}")
                else:
                    print(f"    {param}: {value}")


def demo_analysis_recommendations() -> None:
    """Demonstrate analysis recommendations based on signal type."""
    sample_rate = 100e6
    n_samples = 100000

    t = np.arange(n_samples) / sample_rate

    # Different signal types
    test_signals = {
        "Clock Signal": (np.sin(2 * np.pi * 10e6 * t) > 0).astype(float) * 3.3,
        "Data Bus": generate_random_digital(n_samples) * 3.3,
        "PWM Control": (np.sin(2 * np.pi * 100e3 * t) > 0.3).astype(float) * 5.0,
        "Analog Sensor": 2.5
        + 0.5 * np.sin(2 * np.pi * 1e3 * t)
        + np.random.randn(n_samples) * 0.05,
    }

    print("Analysis recommendations:")
    print("-" * 50)

    for name, signal_data in test_signals.items():
        metadata = TraceMetadata(sample_rate=sample_rate, channel_name=name)
        trace = WaveformTrace(data=signal_data, metadata=metadata)

        recommendations = recommend_analyses(trace)

        print(f"\n{name}:")
        print("  Recommended analyses:")
        for rec in recommendations[:5]:  # Top 5
            print(f"    - {rec.analysis}: {rec.reason}")
            if rec.parameters:
                print(f"      Parameters: {rec.parameters}")


def demo_auto_workflow() -> None:
    """Demonstrate complete auto-analysis workflow."""
    print("Complete Auto-Analysis Workflow")
    print("-" * 50)

    # Generate an unknown signal
    sample_rate = 50e6
    signal_data = generate_uart_like(sample_rate, 115200)

    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="UNKNOWN")
    trace = DigitalTrace(data=signal_data, metadata=metadata)

    print("\nStep 1: Signal Quality Assessment")
    quality = assess_signal_quality(trace)
    print(f"  Overall quality: {quality.overall_quality}")
    print(f"  SNR: {quality.snr_db:.1f} dB")
    print(f"  Issues: {quality.issues if quality.issues else 'None'}")

    print("\nStep 2: Signal Classification")
    classification = classify_signal(trace)
    print(f"  Type: {classification.signal_type}")
    print(f"  Confidence: {classification.confidence:.1%}")

    print("\nStep 3: Logic Family Detection")
    logic = detect_logic_family(trace)
    print(f"  Family: {logic.family}")
    print(f"  Levels: {logic.low_level:.2f}V to {logic.high_level:.2f}V")

    print("\nStep 4: Protocol Detection")
    protocol = detect_protocol(trace)
    print(f"  Protocol: {protocol.protocol}")
    print(f"  Confidence: {protocol.confidence:.1%}")
    if protocol.parameters:
        print(f"  Parameters: {protocol.parameters}")

    print("\nStep 5: Analysis Recommendations")
    recommendations = recommend_analyses(trace)
    print("  Top recommendations:")
    for rec in recommendations[:3]:
        print(f"    - {rec.analysis}")

    print("\n" + "=" * 50)
    print("Auto-analysis complete!")
    print("Next steps: Apply recommended analyses or decode with detected protocol")


# --- Signal Generation Helpers ---


def generate_uart_like(sample_rate: float, baud_rate: float) -> np.ndarray:
    """Generate UART-like signal for testing."""
    bit_duration = 1.0 / baud_rate
    samples_per_bit = int(sample_rate * bit_duration)

    # Generate some UART frames (8N1)
    data_bytes = [0x55, 0xAA, 0x48, 0x65, 0x6C, 0x6C, 0x6F]  # Hello pattern

    signal = []

    # Idle before
    signal.extend([1] * (samples_per_bit * 10))

    for byte in data_bytes:
        # Start bit (low)
        signal.extend([0] * samples_per_bit)

        # Data bits (LSB first)
        for bit in range(8):
            bit_value = (byte >> bit) & 1
            signal.extend([bit_value] * samples_per_bit)

        # Stop bit (high)
        signal.extend([1] * samples_per_bit)

        # Inter-byte gap
        signal.extend([1] * (samples_per_bit * 2))

    # Idle after
    signal.extend([1] * (samples_per_bit * 10))

    return np.array(signal, dtype=bool)


def generate_spi_like(sample_rate: float) -> np.ndarray:
    """Generate SPI-like signal (clock pattern)."""
    clock_freq = 1e6
    samples_per_period = int(sample_rate / clock_freq)
    n_periods = 50

    # Generate clock pattern
    signal = []

    # Idle (CS high equivalent)
    signal.extend([1] * (samples_per_period * 5))

    # Active transmission
    for _ in range(n_periods):
        signal.extend([0] * (samples_per_period // 2))
        signal.extend([1] * (samples_per_period // 2))

    # Idle after
    signal.extend([1] * (samples_per_period * 5))

    return np.array(signal, dtype=bool)


def generate_i2c_like(sample_rate: float) -> np.ndarray:
    """Generate I2C-like signal (with START/STOP conditions)."""
    bit_samples = int(sample_rate / 100e3)  # 100 kHz

    signal = []

    # Idle (high)
    signal.extend([1] * (bit_samples * 10))

    # START-like (falling while clock high)
    signal.extend([0] * bit_samples)

    # Some data pattern
    pattern = [0, 1, 0, 1, 1, 0, 0, 1]
    for bit in pattern * 3:
        signal.extend([bit] * bit_samples)

    # STOP-like (rising while clock high)
    signal.extend([1] * bit_samples)

    # Idle after
    signal.extend([1] * (bit_samples * 10))

    return np.array(signal, dtype=bool)


def generate_random_digital(n_samples: int) -> np.ndarray:
    """Generate random digital pattern."""
    # Generate random data with some structure (like a data bus)
    np.random.seed(42)

    # Create pattern with variable pulse widths
    signal = np.zeros(n_samples)
    pos = 0

    while pos < n_samples:
        # Random pulse width (10-100 samples)
        width = np.random.randint(10, 100)
        value = np.random.randint(0, 2)

        end = min(pos + width, n_samples)
        signal[pos:end] = value
        pos = end

    return signal


if __name__ == "__main__":
    main()
