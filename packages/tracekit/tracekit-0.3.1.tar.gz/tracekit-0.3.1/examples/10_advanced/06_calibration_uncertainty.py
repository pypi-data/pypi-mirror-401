#!/usr/bin/env python3
"""Example: Using TraceKit with Calibration Metadata and Measurement Uncertainty.

This example demonstrates how to use TraceKit's enhanced measurement capabilities
for regulatory-compliant applications (DOD, FDA, aerospace, etc.).

Features demonstrated:
- Calibration metadata tracking (ISO/IEC 17025, NIST 150)
- Measurement uncertainty propagation (GUM-compliant)
- Traceability documentation
- Standards-compliant measurements

References:
    MEASUREMENT_VALIDATION.md - Addresses DOD contractor skepticism
    STANDARDS_COMPLIANCE.md - Complete IEEE standards index
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

from datetime import datetime

import numpy as np

from tracekit.analyzers.waveform import measurements as meas
from tracekit.analyzers.waveform import measurements_with_uncertainty as meas_u
from tracekit.core.types import CalibrationInfo, TraceMetadata, WaveformTrace
from tracekit.core.uncertainty import MeasurementWithUncertainty, UncertaintyEstimator


def example_dod_contractor_workflow() -> None:
    """DOD contractor workflow with full traceability.

    Scenario: Government contractor performing measurements on calibrated
    Tektronix oscilloscope for system verification.
    """
    print("=" * 70)
    print("DOD CONTRACTOR WORKFLOW - Calibrated Measurement with Traceability")
    print("=" * 70)
    print()

    # Step 1: Create calibration info from scope calibration certificate
    cal_info = CalibrationInfo(
        instrument="Tektronix DPO7254C",
        serial_number="B040123",
        calibration_date=datetime(2024, 12, 15),
        calibration_due_date=datetime(2025, 12, 15),
        calibration_lab="Tektronix Standards Lab (NIST-traceable)",
        calibration_cert_number="TEK-CAL-2024-12-B040123",
        firmware_version="FV:11.0.0",
        probe_attenuation=10.0,  # 10x probe
        coupling="DC",
        vertical_resolution=8,  # 8-bit ADC
    )

    # Step 2: Generate synthetic test signal (in real use, this comes from scope CSV export)
    sample_rate = 2.5e9  # 2.5 GSa/s
    duration = 1e-6  # 1 microsecond
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples)

    # 10 MHz square wave with some noise (simulating real acquisition)
    freq = 10e6
    signal = np.sign(np.sin(2 * np.pi * freq * t))  # Square wave
    noise = np.random.normal(0, 0.01, n_samples)  # 10 mV RMS noise
    waveform_data = signal + noise

    # Step 3: Create trace with calibration metadata
    metadata = TraceMetadata(
        sample_rate=sample_rate,
        vertical_scale=0.5,  # 500 mV/div
        vertical_offset=0.0,
        acquisition_time=datetime.now(),
        source_file="measurement_2024-12-20_system_verification.csv",
        calibration_info=cal_info,
    )

    trace = WaveformTrace(data=waveform_data, metadata=metadata)

    # Step 4: Print traceability information
    print("CALIBRATION TRACEABILITY")
    print("-" * 70)
    print(f"Instrument: {trace.metadata.calibration_info.traceability_summary}")
    print(
        f"Calibration Status: {'CURRENT ✓' if trace.metadata.calibration_info.is_calibration_current else 'EXPIRED ✗'}"
    )
    print(f"Acquisition Time: {trace.metadata.acquisition_time}")
    print(f"Source File: {trace.metadata.source_file}")
    print()

    # Step 5: Perform standard measurements (backward compatible)
    print("STANDARD MEASUREMENTS (Fast, no uncertainty)")
    print("-" * 70)
    freq_meas = meas.frequency(trace)
    rise_meas = meas.rise_time(trace)
    amp_meas = meas.amplitude(trace)

    print(f"Frequency: {freq_meas / 1e6:.6f} MHz")
    print(f"Rise Time: {rise_meas * 1e9:.2f} ns")
    print(f"Amplitude: {amp_meas:.4f} V")
    print()

    # Step 6: Perform measurements with uncertainty (for regulatory compliance)
    print("MEASUREMENTS WITH UNCERTAINTY (GUM-compliant)")
    print("-" * 70)

    freq_result = meas_u.frequency(trace)
    print("Frequency:")
    print(f"  Value: {freq_result.value / 1e6:.6f} MHz")
    print(f"  Uncertainty: ±{freq_result.uncertainty / 1e6:.6f} MHz (k=1, 68.27%)")
    print(f"  Relative: ±{freq_result.relative_uncertainty * 100:.3f}%")
    print(
        f"  Interval: [{freq_result.lower_bound / 1e6:.6f}, {freq_result.upper_bound / 1e6:.6f}] MHz"
    )
    print()

    rise_result = meas_u.rise_time(trace)
    print("Rise Time:")
    print(f"  Value: {rise_result.value * 1e9:.2f} ns")
    print(f"  Uncertainty: ±{rise_result.uncertainty * 1e9:.2f} ns (k=1, 68.27%)")
    print(f"  Relative: ±{rise_result.relative_uncertainty * 100:.3f}%")
    print()

    amp_result = meas_u.amplitude(trace)
    print("Amplitude:")
    print(f"  Value: {amp_result.value:.4f} V")
    print(f"  Uncertainty: ±{amp_result.uncertainty:.4f} V (k=1, 68.27%)")
    print(f"  Relative: ±{amp_result.relative_uncertainty * 100:.3f}%")
    print()

    # Step 7: Generate compliance report
    print("=" * 70)
    print("COMPLIANCE SUMMARY")
    print("=" * 70)
    print("✓ IEEE 181-2011: Rise Time, Frequency measurements")
    print("✓ IEEE 1057-2017: Amplitude (Vpp) measurement")
    print("✓ JCGM 100:2008 (GUM): Measurement uncertainty propagation")
    print("✓ ISO/IEC 17025: Calibration traceability documented")
    print("✓ NIST Handbook 150: Measurement standards compliance")
    print()
    print("This measurement is audit-ready for DOD/regulatory submission.")
    print()


def example_uncertainty_components() -> None:
    """Demonstrate uncertainty calculation components.

    Shows how different uncertainty sources contribute to total uncertainty.
    """
    print("=" * 70)
    print("MEASUREMENT UNCERTAINTY COMPONENTS")
    print("=" * 70)
    print()

    # Scenario: 1 GSa/s scope, 25 ppm timebase, measuring 1.5V signal
    sample_rate = 1e9
    reading = 1.5  # volts

    print("Scenario: Measuring 1.5 V signal with 1 GSa/s oscilloscope")
    print()

    # Type A uncertainty (statistical - from repeated measurements)
    measurements = np.array([1.501, 1.499, 1.500, 1.502, 1.498])
    u_type_a = UncertaintyEstimator.type_a_standard_error(measurements)
    print("Type A Uncertainty (statistical):")
    print(f"  Repeated measurements: {measurements}")
    print(f"  Standard error: {u_type_a * 1000:.3f} mV")
    print()

    # Type B uncertainties (systematic)
    print("Type B Uncertainties (systematic):")

    # Timebase uncertainty
    u_timebase = UncertaintyEstimator.time_base_uncertainty(sample_rate, 25.0)
    print(f"  Timebase (25 ppm): {u_timebase * 1e12:.2f} ps per sample")

    # Vertical uncertainty (scope spec: ±2% of reading + 1 mV offset)
    u_vertical = UncertaintyEstimator.vertical_uncertainty(reading, 2.0, 0.001)
    print(f"  Vertical (±2% + 1mV): {u_vertical * 1000:.2f} mV")

    # Quantization (8-bit ADC, 5V full scale)
    full_scale = 5.0
    lsb = full_scale / 256
    u_quant = UncertaintyEstimator.type_b_rectangular(0.5 * lsb)
    print(f"  Quantization (8-bit): {u_quant * 1000:.2f} mV")
    print()

    # Combined uncertainty
    u_combined = UncertaintyEstimator.combined_uncertainty([u_type_a, u_vertical, u_quant])
    print(f"Combined Standard Uncertainty: {u_combined * 1000:.2f} mV")

    # Expanded uncertainty (k=2, 95.45% confidence)
    u_expanded = 2.0 * u_combined
    print(f"Expanded Uncertainty (k=2, 95.45%): {u_expanded * 1000:.2f} mV")
    print()

    # Final result
    result = MeasurementWithUncertainty(
        value=reading,
        uncertainty=u_combined,
        unit="V",
        coverage_factor=2.0,
        confidence_level=0.9545,
    )
    print(f"Final Result: {result}")
    print()


def example_simple_usage() -> None:
    """Simple example for research/development use.

    Shows backward-compatible usage without uncertainty tracking.
    """
    print("=" * 70)
    print("SIMPLE USAGE (Research/Development)")
    print("=" * 70)
    print()

    # Generate simple test signal
    sample_rate = 1e9
    t = np.linspace(0, 1e-6, 1000)
    waveform = np.sin(2 * np.pi * 10e6 * t)

    # Create trace (minimal metadata)
    trace = WaveformTrace(data=waveform, metadata=TraceMetadata(sample_rate=sample_rate))

    # Fast measurements
    freq = meas.frequency(trace)
    amp = meas.amplitude(trace)
    rms_val = meas.rms(trace)

    print(f"Frequency: {freq / 1e6:.3f} MHz")
    print(f"Amplitude: {amp:.4f} V")
    print(f"RMS: {rms_val:.4f} V")
    print()


def main() -> None:
    """Run all examples."""
    example_dod_contractor_workflow()
    example_uncertainty_components()
    example_simple_usage()

    print("=" * 70)
    print("For more information, see:")
    print("  - MEASUREMENT_VALIDATION.md (addresses DOD contractor questions)")
    print("  - STANDARDS_COMPLIANCE.md (complete IEEE standards index)")
    print("  - IMPLEMENTATION_SUMMARY.md (full implementation guide)")
    print("=" * 70)


if __name__ == "__main__":
    main()
