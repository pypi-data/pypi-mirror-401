#!/usr/bin/env python3
"""Export API demonstration.

This example demonstrates exporting trace data to multiple formats.

Requirements demonstrated:

Usage:
    uv run python examples/export_demo.py
"""

from pathlib import Path

import numpy as np

import tracekit as tk


def main() -> None:
    """Demonstrate export functionality."""
    print("TraceKit Export API Demo")
    print("=" * 50)

    # Create a temporary directory for output files
    output_dir = Path("/tmp/tracekit_export_demo")
    output_dir.mkdir(exist_ok=True)

    # Track created files for cleanup
    created_files = []

    try:
        # Create a sample waveform (sine wave)
        sample_rate = 1e6  # 1 MHz
        duration = 1e-3  # 1 ms
        frequency = 1e3  # 1 kHz
        n_samples = int(sample_rate * duration)

        t = np.linspace(0, duration, n_samples)
        data = np.sin(2 * np.pi * frequency * t)

        # Create trace with metadata
        metadata = tk.TraceMetadata(
            sample_rate=sample_rate,
            vertical_scale=0.1,
            vertical_offset=0.0,
            channel_name="CH1",
            source_file="demo_signal.wfm",
        )

        trace = tk.WaveformTrace(data=data, metadata=metadata)

        print("\nCreated waveform:")
        print(f"  Samples: {len(trace.data)}")
        print(f"  Duration: {trace.duration * 1e3:.3f} ms")
        print(f"  Sample Rate: {trace.metadata.sample_rate / 1e6:.1f} MHz")

        # Export to CSV
        print("\n1. Exporting to CSV...")
        csv_file = output_dir / "demo_export.csv"
        tk.export_csv(trace, str(csv_file))
        created_files.append(csv_file)
        print(f"   Saved to {csv_file}")

        # Export with custom options
        csv_us_file = output_dir / "demo_export_us.csv"
        tk.export_csv(trace, str(csv_us_file), time_unit="us", precision=6)
        created_files.append(csv_us_file)
        print(f"   Saved to {csv_us_file} (microseconds, 6 decimals)")

        # Export to JSON
        print("\n2. Exporting to JSON...")
        json_file = output_dir / "demo_export.json"
        tk.export_json(trace, str(json_file), pretty=True)
        created_files.append(json_file)
        print(f"   Saved to {json_file}")

        # Export compressed JSON
        json_gz_file = output_dir / "demo_export.json.gz"
        tk.export_json(trace, str(json_gz_file), compress=True)
        created_files.append(json_gz_file)
        print(f"   Saved to {json_gz_file} (compressed)")

        # Export to HDF5 (if h5py available)
        print("\n3. Exporting to HDF5...")
        try:
            h5_file = output_dir / "demo_export.h5"
            tk.export_hdf5(trace, str(h5_file), compression="gzip")
            created_files.append(h5_file)
            print(f"   Saved to {h5_file}")
        except ImportError as e:
            print(f"   Skipped (h5py not installed): {e}")

        # Export to MATLAB (if scipy available)
        print("\n4. Exporting to MATLAB...")
        try:
            mat_file = output_dir / "demo_export.mat"
            tk.export_mat(trace, str(mat_file), version="5")
            created_files.append(mat_file)
            print(f"   Saved to {mat_file} (v5 format)")
        except ImportError as e:
            print(f"   Skipped (scipy not installed): {e}")

        # Try MATLAB v7.3 (if scipy and h5py available)
        try:
            mat_v73_file = output_dir / "demo_export_v73.mat"
            tk.export_mat(trace, str(mat_v73_file), version="7.3", compression=True)
            created_files.append(mat_v73_file)
            print(f"   Saved to {mat_v73_file} (v7.3 format, compressed)")
        except ImportError as e:
            print(f"   Skipped v7.3 (h5py not installed): {e}")

        # Create multiple channels
        print("\n5. Multi-channel export...")
        ch1 = trace
        ch2_data = np.cos(2 * np.pi * frequency * t)
        ch2 = tk.WaveformTrace(
            data=ch2_data,
            metadata=tk.TraceMetadata(
                sample_rate=sample_rate, channel_name="CH2", source_file="demo_signal.wfm"
            ),
        )
        ch3_data = np.sin(2 * np.pi * frequency * 2 * t)
        ch3 = tk.WaveformTrace(
            data=ch3_data,
            metadata=tk.TraceMetadata(
                sample_rate=sample_rate, channel_name="CH3", source_file="demo_signal.wfm"
            ),
        )

        # Export multiple traces to one file
        try:
            from tracekit.exporters import export_multi_trace_csv

            multi_csv_file = output_dir / "demo_multi.csv"
            export_multi_trace_csv(
                [ch1, ch2, ch3], str(multi_csv_file), names=["CH1", "CH2", "CH3"]
            )
            created_files.append(multi_csv_file)
            print(f"   Saved to {multi_csv_file} (3 channels)")
        except Exception as e:
            print(f"   Multi-trace CSV failed: {e}")

        try:
            multi_h5_file = output_dir / "demo_multi.h5"
            tk.export_hdf5({"ch1": ch1, "ch2": ch2, "ch3": ch3}, str(multi_h5_file))
            created_files.append(multi_h5_file)
            print(f"   Saved to {multi_h5_file} (3 channels)")
        except ImportError:
            print("   Skipped (h5py not installed)")

        try:
            multi_mat_file = output_dir / "demo_multi.mat"
            tk.export_mat({"ch1": ch1, "ch2": ch2, "ch3": ch3}, str(multi_mat_file))
            created_files.append(multi_mat_file)
            print(f"   Saved to {multi_mat_file} (3 channels)")
        except ImportError:
            print("   Skipped (scipy not installed)")

        # Export measurements
        print("\n6. Exporting analysis results...")
        measurements = {
            "frequency": frequency,
            "amplitude": 1.0,
            "rms": np.sqrt(0.5),
            "mean": np.mean(data),
            "peak_to_peak": 2.0,
        }

        measurements_file = output_dir / "demo_measurements.json"
        tk.export_json(measurements, str(measurements_file))
        created_files.append(measurements_file)
        print(f"   Saved to {measurements_file}")

        print("\n" + "=" * 50)
        print("Export demo complete!")
        print(f"\nGenerated files in {output_dir}:")
        for f in created_files:
            if f.exists():
                print(f"  - {f.name}")

    finally:
        # Cleanup temporary files
        print("\nCleaning up temporary files...")
        for f in created_files:
            try:
                if f.exists():
                    f.unlink()
            except OSError:
                pass  # Ignore cleanup errors

        # Try to remove the directory if empty
        try:
            output_dir.rmdir()
        except OSError:
            pass  # Directory not empty or other error

        print("Cleanup complete.")


if __name__ == "__main__":
    main()
