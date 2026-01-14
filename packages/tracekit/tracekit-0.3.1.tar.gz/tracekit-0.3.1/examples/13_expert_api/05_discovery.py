#!/usr/bin/env python3
"""Demo of TraceKit auto-discovery features.

This script demonstrates the DISC-* auto-discovery capabilities:
"""

import numpy as np

from tracekit.core.confidence import ConfidenceScore
from tracekit.core.types import TraceMetadata, WaveformTrace
from tracekit.discovery import (
    assess_data_quality,
    characterize_signal,
    decode_protocol,
    find_anomalies,
)


def create_uart_signal(duration_ms: float = 1.0, baud_rate: int = 115200) -> WaveformTrace:
    """Create simulated UART signal.

    Args:
        duration_ms: Signal duration in milliseconds.
        baud_rate: UART baud rate.

    Returns:
        WaveformTrace with UART data.
    """
    sample_rate = 10e6  # 10 MS/s
    n_samples = int(duration_ms * 1e-3 * sample_rate)

    # Create simple UART pattern (idle high, start bit low, data bits, stop bit high)
    signal = np.ones(n_samples) * 3.3  # Idle high

    bit_period = int(sample_rate / baud_rate)

    # Transmit "Hello" (0x48 0x65 0x6C 0x6C 0x6F)
    data_bytes = [0x48, 0x65, 0x6C, 0x6C, 0x6F]

    idx = 1000  # Start position
    for byte_val in data_bytes:
        if idx + 10 * bit_period >= n_samples:
            break

        # Start bit (low)
        signal[idx : idx + bit_period] = 0.0
        idx += bit_period

        # Data bits (LSB first)
        for bit_num in range(8):
            bit_val = (byte_val >> bit_num) & 1
            signal[idx : idx + bit_period] = 3.3 if bit_val else 0.0
            idx += bit_period

        # Stop bit (high)
        signal[idx : idx + bit_period] = 3.3
        idx += bit_period

        # Inter-byte gap
        idx += bit_period * 2

    return WaveformTrace(data=signal, metadata=TraceMetadata(sample_rate=sample_rate))


def demo_confidence_scoring() -> None:
    """Demonstrate confidence scoring."""
    print("=" * 70)
    print("DEMO: Universal Confidence Scoring (DISC-007)")
    print("=" * 70)

    # Create confidence scores
    score1 = ConfidenceScore(0.95, factors={"snr": 0.98, "timing": 0.92})
    score2 = ConfidenceScore(0.72, factors={"pattern": 0.75, "amplitude": 0.69})
    score3 = ConfidenceScore(0.45, factors={"quality": 0.50, "consistency": 0.40})

    for i, score in enumerate([score1, score2, score3], 1):
        print(f"\nScore {i}:")
        print(f"  Value: {score.value:.2f}")
        print(f"  Level: {score.level}")
        print(f"  Interpretation: {score.interpretation}")
        print(f"  Factors: {score.factors}")

    # Combine scores
    combined = ConfidenceScore.combine(
        [score1.value, score2.value, score3.value], weights=[0.5, 0.3, 0.2]
    )
    print(f"\nCombined score (weighted): {combined:.2f}")
    print()


def demo_signal_characterization() -> None:
    """Demonstrate automatic signal characterization."""
    print("=" * 70)
    print("DEMO: Automatic Signal Characterization (DISC-001)")
    print("=" * 70)

    # Create UART signal
    trace = create_uart_signal(duration_ms=2.0, baud_rate=115200)

    print("\nTrace info:")
    print(f"  Samples: {len(trace.data)}")
    print(f"  Duration: {trace.duration * 1e3:.2f} ms")
    print(f"  Sample rate: {trace.metadata.sample_rate / 1e6:.1f} MS/s")

    # Characterize signal
    print("\nCharacterizing signal...")
    result = characterize_signal(trace, include_alternatives=True)

    print("\nResults:")
    print(f"  Signal type: {result.signal_type}")
    print(f"  Confidence: {result.confidence:.2f}")
    print(f"  Voltage levels: {result.voltage_low:.2f}V to {result.voltage_high:.2f}V")
    print(f"  Frequency: {result.frequency_hz:.1f} Hz")

    print("\nQuality metrics:")
    for metric, value in result.quality_metrics.items():
        print(f"  {metric}: {value:.2f}")

    print("\nParameters:")
    for param, value in result.parameters.items():
        print(f"  {param}: {value}")

    if result.alternatives:
        print("\nAlternative suggestions:")
        for alt_type, alt_conf in result.alternatives:
            print(f"  {alt_type}: {alt_conf:.2f}")
    print()


def demo_anomaly_detection() -> None:
    """Demonstrate anomaly detection."""
    print("=" * 70)
    print("DEMO: Anomaly Detection (DISC-002)")
    print("=" * 70)

    # Create signal with anomalies
    sample_rate = 10e6
    n_samples = 10000
    signal = np.zeros(n_samples)

    # Square wave base
    t = np.arange(n_samples) / sample_rate
    signal = np.where(np.sin(2 * np.pi * 1e3 * t) > 0, 3.3, 0.0)

    # Add anomalies
    signal[1000] = 3.8  # Noise spike
    signal[3000:3002] = 0.5  # Glitch
    signal[5000] = -0.2  # Undershoot

    trace = WaveformTrace(data=signal, metadata=TraceMetadata(sample_rate=sample_rate))

    print("\nDetecting anomalies in signal...")
    anomalies = find_anomalies(trace, min_confidence=0.7)

    print(f"\nFound {len(anomalies)} anomalies:")
    for i, anom in enumerate(anomalies[:10], 1):  # Show first 10
        print(f"\n{i}. {anom.type.upper()} at {anom.timestamp_us:.2f} us")
        print(f"   Severity: {anom.severity}")
        print(f"   Description: {anom.description}")
        print(f"   Duration: {anom.duration_ns:.1f} ns")
        print(f"   Confidence: {anom.confidence:.2f}")

    # Show severity breakdown
    critical = sum(1 for a in anomalies if a.severity == "CRITICAL")
    warning = sum(1 for a in anomalies if a.severity == "WARNING")
    info = sum(1 for a in anomalies if a.severity == "INFO")

    print("\nSeverity breakdown:")
    print(f"  CRITICAL: {critical}")
    print(f"  WARNING: {warning}")
    print(f"  INFO: {info}")
    print()


def demo_quality_assessment() -> None:
    """Demonstrate data quality assessment."""
    print("=" * 70)
    print("DEMO: Data Quality Assessment (DISC-009)")
    print("=" * 70)

    # Create signal
    trace = create_uart_signal(duration_ms=5.0, baud_rate=115200)

    print("\nAssessing data quality for protocol decode...")
    quality = assess_data_quality(
        trace,
        scenario="protocol_decode",
        protocol_params={"clock_freq_mhz": 0.115},  # 115 kHz
    )

    print(f"\nOverall status: {quality.status}")
    print(f"Confidence: {quality.confidence:.2f}")

    print("\nIndividual metrics:")
    for metric in quality.metrics:
        status_symbol = "[OK]" if metric.passed else "[!!]"
        print(f"\n{status_symbol} {metric.name}: {metric.status}")
        print(f"   Current: {metric.current_value:.2f} {metric.unit}")
        print(f"   Required: {metric.required_value:.2f} {metric.unit}")
        print(f"   Margin: {metric.margin_percent:+.1f}%")

        if not metric.passed:
            print(f"   Issue: {metric.explanation}")
            print(f"   Fix: {metric.recommendation}")

    if quality.improvement_suggestions:
        print("\nImprovement suggestions:")
        for i, suggestion in enumerate(quality.improvement_suggestions, 1):
            print(f"\n{i}. {suggestion['action']}")
            print(f"   Expected benefit: {suggestion['expected_benefit']}")
            print(f"   Difficulty: {suggestion['difficulty_level']}")
    print()


def demo_protocol_decode() -> None:
    """Demonstrate one-shot protocol decode."""
    print("=" * 70)
    print("DEMO: One-Shot Protocol Decode (DISC-010)")
    print("=" * 70)

    # Create UART signal
    trace = create_uart_signal(duration_ms=5.0, baud_rate=115200)

    print("\nAuto-decoding protocol (no configuration required)...")
    result = decode_protocol(trace)

    print("\nDecode results:")
    print(f"  Protocol: {result.protocol}")
    print(f"  Overall confidence: {result.overall_confidence:.2f}")
    print(f"  Frames decoded: {result.frame_count}")
    print(f"  Errors detected: {result.error_count}")

    print("\nDetected parameters:")
    for param, value in result.detected_params.items():
        print(f"  {param}: {value}")

    if result.data:
        print(f"\nDecoded data ({len(result.data)} bytes):")
        for i, byte_data in enumerate(result.data[:20]):  # Show first 20
            char = chr(byte_data.value) if 32 <= byte_data.value < 127 else "."
            conf_indicator = "[OK]" if byte_data.confidence >= 0.8 else "[??]"

            print(
                f"  [{i:3d}] {conf_indicator} 0x{byte_data.value:02X} '{char}' "
                f"(confidence: {byte_data.confidence:.2f})"
            )

            if byte_data.has_error:
                print(f"       ERROR: {byte_data.error_description}")
    print()


def main() -> None:
    """Run all demos."""
    print("\n" + "=" * 70)
    print("TraceKit Auto-Discovery Feature Demo")
    print("=" * 70)
    print()

    demo_confidence_scoring()
    demo_signal_characterization()
    demo_anomaly_detection()
    demo_quality_assessment()
    demo_protocol_decode()

    print("=" * 70)
    print("Demo complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
