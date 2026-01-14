#!/usr/bin/env python3
"""Example 05: Generate Analysis Reports.

This example demonstrates generating professional analysis reports
from TraceKit measurements and analyses.

Time: 15 minutes
Prerequisites: Examples 01-04 (loading, measurements, plotting, export)

Run:
    uv run python examples/01_basics/05_generate_report.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import json
from datetime import datetime
from pathlib import Path

import tracekit as tk
from tracekit.testing import SyntheticDataGenerator, SyntheticSignalConfig


def main() -> None:
    """Demonstrate report generation capabilities."""
    print("=" * 60)
    print("TraceKit Example: Generate Analysis Reports")
    print("=" * 60)

    # --- Generate Test Data ---
    print("\n--- Generating Test Signals ---")

    generator = SyntheticDataGenerator(seed=42)

    # Generate a clean square wave signal
    config = SyntheticSignalConfig(
        pattern_type="square",
        sample_rate=100e6,
        duration_samples=100000,
        frequency=1e6,
        noise_snr_db=40,
    )

    signal_data, ground_truth = generator.generate_digital_signal(config)

    # Create a trace-like object for measurements
    from tracekit.core.types import TraceMetadata, WaveformTrace

    metadata = TraceMetadata(
        sample_rate=config.sample_rate,
        channel_name="test_signal",
        units="V",
    )
    trace = WaveformTrace(data=signal_data, metadata=metadata)

    print(f"Generated signal with {len(signal_data)} samples")
    print(f"Expected frequency: {ground_truth.frequency_hz / 1e6:.3f} MHz")

    # --- Collect Measurements ---
    print("\n--- Collecting Measurements ---")

    # Time domain measurements
    freq = tk.frequency(trace)
    amp = tk.amplitude(trace)
    rms_val = tk.rms(trace)
    dc_mean = tk.mean(trace)
    duty = tk.duty_cycle(trace)

    print(f"Frequency: {freq / 1e6:.6f} MHz")
    print(f"Amplitude: {amp:.3f} V")
    print(f"RMS: {rms_val:.3f} V")
    print(f"DC Mean: {dc_mean:.3f} V")
    print(f"Duty Cycle: {duty * 100:.1f}%")

    # Spectral measurements
    thd_db = tk.thd(trace)
    snr_db = tk.snr(trace)
    sinad_db = tk.sinad(trace)
    enob_bits = tk.enob(trace)

    print("\nSpectral Quality:")
    print(f"  THD: {thd_db:.1f} dB")
    print(f"  SNR: {snr_db:.1f} dB")
    print(f"  SINAD: {sinad_db:.1f} dB")
    print(f"  ENOB: {enob_bits:.2f} bits")

    # Statistical analysis
    stats = tk.basic_stats(trace)
    print("\nStatistics:")
    print(f"  Min: {stats.min:.3f} V")
    print(f"  Max: {stats.max:.3f} V")
    print(f"  Std Dev: {stats.std:.3f} V")

    # --- Build Report Data Structure ---
    print("\n--- Building Report ---")

    report = {
        "metadata": {
            "title": "Signal Analysis Report",
            "generated_at": datetime.now().isoformat(),
            "tracekit_version": tk.__version__,
            "source_file": "synthetic_test_signal",
        },
        "signal_info": {
            "sample_rate_hz": config.sample_rate,
            "duration_samples": config.duration_samples,
            "duration_seconds": config.duration_samples / config.sample_rate,
            "channel_name": metadata.channel_name,
            "units": metadata.units,
        },
        "time_domain": {
            "frequency_hz": freq,
            "frequency_mhz": freq / 1e6,
            "amplitude_vpp": amp,
            "rms_voltage": rms_val,
            "dc_offset": dc_mean,
            "duty_cycle_percent": duty * 100,
        },
        "spectral_quality": {
            "thd_db": thd_db,
            "snr_db": snr_db,
            "sinad_db": sinad_db,
            "enob_bits": enob_bits,
        },
        "statistics": {
            "minimum": stats.min,
            "maximum": stats.max,
            "mean": stats.mean,
            "std_dev": stats.std,
            "peak_to_peak": stats.max - stats.min,
        },
        "pass_fail": {
            "frequency_accuracy": abs(freq - ground_truth.frequency_hz) / ground_truth.frequency_hz
            < 0.01,
            "snr_acceptable": snr_db > 30,
            "duty_cycle_nominal": abs(duty - 0.5) < 0.1,
        },
    }

    # --- Output Report Formats ---
    print("\n--- Report Output Options ---")

    # 1. JSON Report
    print("\n1. JSON Format (machine-readable):")
    json_output = json.dumps(report, indent=2)
    print(json_output[:500] + "..." if len(json_output) > 500 else json_output)

    # 2. Text Report
    print("\n2. Text Format (human-readable):")
    text_report = generate_text_report(report)
    print(text_report)

    # 3. Markdown Report
    print("\n3. Markdown Format (documentation):")
    md_report = generate_markdown_report(report)
    print(md_report[:800] + "..." if len(md_report) > 800 else md_report)

    # --- Save Reports ---
    print("\n--- Saving Reports ---")

    output_dir = Path("/tmp/tracekit_reports")
    output_dir.mkdir(exist_ok=True)

    # Save JSON
    json_path = output_dir / "analysis_report.json"
    json_path.write_text(json.dumps(report, indent=2))
    print(f"Saved JSON: {json_path}")

    # Save Text
    text_path = output_dir / "analysis_report.txt"
    text_path.write_text(text_report)
    print(f"Saved Text: {text_path}")

    # Save Markdown
    md_path = output_dir / "analysis_report.md"
    md_path.write_text(md_report)
    print(f"Saved Markdown: {md_path}")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. Collect measurements using tk.measure() or individual functions")
    print("  2. Build structured report dictionary")
    print("  3. Export as JSON for programmatic use")
    print("  4. Export as text/markdown for documentation")
    print("  5. Include pass/fail criteria for automated testing")
    print("=" * 60)


def generate_text_report(report: dict) -> str:
    """Generate plain text report from report dictionary."""
    lines = [
        "=" * 60,
        f"  {report['metadata']['title']}",
        "=" * 60,
        f"Generated: {report['metadata']['generated_at']}",
        f"TraceKit Version: {report['metadata']['tracekit_version']}",
        "",
        "SIGNAL INFORMATION",
        "-" * 40,
        f"  Sample Rate: {report['signal_info']['sample_rate_hz'] / 1e6:.1f} MHz",
        f"  Duration: {report['signal_info']['duration_seconds'] * 1e6:.1f} us",
        f"  Samples: {report['signal_info']['duration_samples']}",
        "",
        "TIME DOMAIN MEASUREMENTS",
        "-" * 40,
        f"  Frequency: {report['time_domain']['frequency_mhz']:.6f} MHz",
        f"  Amplitude: {report['time_domain']['amplitude_vpp']:.3f} Vpp",
        f"  RMS: {report['time_domain']['rms_voltage']:.3f} V",
        f"  DC Offset: {report['time_domain']['dc_offset']:.3f} V",
        f"  Duty Cycle: {report['time_domain']['duty_cycle_percent']:.1f}%",
        "",
        "SPECTRAL QUALITY",
        "-" * 40,
        f"  THD: {report['spectral_quality']['thd_db']:.1f} dB",
        f"  SNR: {report['spectral_quality']['snr_db']:.1f} dB",
        f"  SINAD: {report['spectral_quality']['sinad_db']:.1f} dB",
        f"  ENOB: {report['spectral_quality']['enob_bits']:.2f} bits",
        "",
        "PASS/FAIL SUMMARY",
        "-" * 40,
    ]

    for test, passed in report["pass_fail"].items():
        status = "PASS" if passed else "FAIL"
        lines.append(f"  {test}: {status}")

    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)


def generate_markdown_report(report: dict) -> str:
    """Generate Markdown report from report dictionary."""
    lines = [
        f"# {report['metadata']['title']}",
        "",
        f"**Generated:** {report['metadata']['generated_at']}",
        f"**TraceKit Version:** {report['metadata']['tracekit_version']}",
        "",
        "## Signal Information",
        "",
        "| Parameter | Value |",
        "|-----------|-------|",
        f"| Sample Rate | {report['signal_info']['sample_rate_hz'] / 1e6:.1f} MHz |",
        f"| Duration | {report['signal_info']['duration_seconds'] * 1e6:.1f} us |",
        f"| Samples | {report['signal_info']['duration_samples']} |",
        "",
        "## Time Domain Measurements",
        "",
        "| Measurement | Value |",
        "|-------------|-------|",
        f"| Frequency | {report['time_domain']['frequency_mhz']:.6f} MHz |",
        f"| Amplitude | {report['time_domain']['amplitude_vpp']:.3f} Vpp |",
        f"| RMS | {report['time_domain']['rms_voltage']:.3f} V |",
        f"| DC Offset | {report['time_domain']['dc_offset']:.3f} V |",
        f"| Duty Cycle | {report['time_domain']['duty_cycle_percent']:.1f}% |",
        "",
        "## Spectral Quality",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| THD | {report['spectral_quality']['thd_db']:.1f} dB |",
        f"| SNR | {report['spectral_quality']['snr_db']:.1f} dB |",
        f"| SINAD | {report['spectral_quality']['sinad_db']:.1f} dB |",
        f"| ENOB | {report['spectral_quality']['enob_bits']:.2f} bits |",
        "",
        "## Pass/Fail Summary",
        "",
        "| Test | Result |",
        "|------|--------|",
    ]

    for test, passed in report["pass_fail"].items():
        status = "PASS" if passed else "FAIL"
        lines.append(f"| {test} | {status} |")

    return "\n".join(lines)


if __name__ == "__main__":
    main()
