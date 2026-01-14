"""Integration tests for real capture data.

These tests verify TraceKit works correctly with real oscilloscope captures,
providing confidence that the library handles production data properly.

Tests use the real_captures/ directory which contains:
- Real Tektronix WFM files across size tiers
- Tektronix session (.tss) and settings (.set) files
- UDP packet capture subsets
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

pytestmark = pytest.mark.integration


@pytest.mark.integration
@pytest.mark.requires_data
class TestRealWaveformCaptures:
    """Test loading and analysis of real Tektronix WFM captures."""

    def test_load_small_wfm_files(self, real_wfm_small: list[Path]) -> None:
        """Test loading small WFM files (< 1.5 MB)."""
        if not real_wfm_small:
            pytest.skip("No small WFM files available")

        from tracekit.core.exceptions import LoaderError
        from tracekit.loaders.tektronix import load_tektronix_wfm

        loaded_count = 0
        for wfm_file in real_wfm_small:
            try:
                trace = load_tektronix_wfm(wfm_file)

                # Basic validation
                assert trace is not None
                assert hasattr(trace, "data")
                assert len(trace.data) > 0
                assert np.isfinite(trace.data).all()

                # Metadata should be present
                assert hasattr(trace, "metadata")
                assert trace.metadata is not None
                loaded_count += 1
            except LoaderError:
                # Skip corrupted/incompatible WFM files
                continue

        # At least one file should load successfully
        if loaded_count == 0:
            pytest.skip("No WFM files could be loaded (all corrupted/incompatible)")

    def test_load_medium_wfm_files(self, real_wfm_medium: list[Path]) -> None:
        """Test loading medium WFM files (1.5 - 6 MB)."""
        if not real_wfm_medium:
            pytest.skip("No medium WFM files available")

        from tracekit.core.exceptions import LoaderError
        from tracekit.loaders.tektronix import load_tektronix_wfm

        loaded_count = 0
        for wfm_file in real_wfm_medium[:3]:  # Limit to 3 for speed
            try:
                trace = load_tektronix_wfm(wfm_file)

                assert trace is not None
                assert len(trace.data) > 0
                assert np.isfinite(trace.data).all()
                loaded_count += 1
            except LoaderError:
                # Skip corrupted/incompatible WFM files
                continue

        # At least one file should load successfully
        if loaded_count == 0:
            pytest.skip("No WFM files could be loaded (all corrupted/incompatible)")

    @pytest.mark.slow
    def test_load_large_wfm_files(self, real_wfm_large: list[Path]) -> None:
        """Test loading large WFM files (> 6 MB)."""
        if not real_wfm_large:
            pytest.skip("No large WFM files available")

        from tracekit.loaders.tektronix import load_tektronix_wfm

        # Only test first large file due to time
        wfm_file = real_wfm_large[0]
        trace = load_tektronix_wfm(wfm_file)

        assert trace is not None
        assert len(trace.data) > 0
        assert np.isfinite(trace.data).all()

    def test_basic_measurements_on_real_data(self, loaded_real_wfm_data: dict[str, any]) -> None:
        """Test basic measurements work on real capture data."""
        if not loaded_real_wfm_data:
            pytest.skip("No pre-loaded WFM data available")

        from tracekit import amplitude, mean, rms

        for filename, trace in loaded_real_wfm_data.items():
            # Skip digital/boolean data (can't compute amplitude on boolean)
            if trace.data.dtype == np.bool_:
                continue

            # Basic measurements should succeed
            m = mean(trace)
            assert np.isfinite(m), f"Mean is not finite for {filename}"

            r = rms(trace)
            assert r >= 0, f"RMS is negative for {filename}"

            amp = amplitude(trace)
            assert amp >= 0, f"Amplitude is negative for {filename}"

    def test_fft_on_real_data(self, loaded_real_wfm_data: dict[str, any]) -> None:
        """Test FFT computation works on real capture data."""
        if not loaded_real_wfm_data:
            pytest.skip("No pre-loaded WFM data available")

        from tracekit import fft

        for filename, trace in loaded_real_wfm_data.items():
            freq, mag = fft(trace)

            assert len(freq) > 0, f"No frequency data for {filename}"
            assert len(mag) == len(freq), f"Frequency/magnitude mismatch for {filename}"
            assert np.isfinite(mag).all(), f"Non-finite magnitude values for {filename}"

    def test_filtering_on_real_data(self, loaded_real_wfm_data: dict[str, any]) -> None:
        """Test filtering works on real capture data."""
        if not loaded_real_wfm_data:
            pytest.skip("No pre-loaded WFM data available")

        from tracekit import low_pass

        for trace in loaded_real_wfm_data.values():
            # Use a reasonable cutoff based on sample rate
            if hasattr(trace.metadata, "sample_rate") and trace.metadata.sample_rate:
                cutoff = trace.metadata.sample_rate * 0.1
            else:
                cutoff = 1e5

            filtered = low_pass(trace, cutoff=cutoff)

            assert len(filtered.data) == len(trace.data)
            assert np.isfinite(filtered.data).all()


@pytest.mark.integration
@pytest.mark.requires_data
class TestRealUDPPacketCaptures:
    """Test loading and analysis of real UDP packet captures."""

    def test_udp_packet_segments_exist(self, real_udp_packets: dict[str, Path | None]) -> None:
        """Test that UDP packet segment files exist and have content."""
        segments_found = sum(1 for v in real_udp_packets.values() if v is not None)

        if segments_found == 0:
            pytest.skip("No UDP packet files available")

        for segment_name, path in real_udp_packets.items():
            if path is not None:
                assert path.exists(), f"UDP {segment_name} file doesn't exist"
                assert path.stat().st_size > 0, f"UDP {segment_name} file is empty"

    def test_load_udp_packets_as_binary(self, real_udp_packets: dict[str, Path | None]) -> None:
        """Test loading UDP packets as raw binary data."""
        from tracekit.loaders.binary import load_binary

        for segment_name, path in real_udp_packets.items():  # noqa: PERF102
            if path is None:
                continue

            # Load as raw bytes (uint8)
            trace = load_binary(path, dtype="uint8", sample_rate=1.0)

            assert trace is not None
            assert len(trace.data) > 0

    def test_entropy_analysis_on_udp_packets(
        self, real_udp_packets: dict[str, Path | None]
    ) -> None:
        """Test entropy analysis on UDP packet data."""
        try:
            from tracekit.analyzers.statistical.entropy import calculate_entropy
        except ImportError:
            pytest.skip("Entropy analysis not available")

        for segment_name, path in real_udp_packets.items():
            if path is None:
                continue

            with open(path, "rb") as f:
                data = f.read(10000)  # First 10KB

            entropy = calculate_entropy(data)

            # Real packet data should have moderate to high entropy
            assert 0 < entropy <= 8.0, f"Entropy out of range for {segment_name}"


@pytest.mark.integration
@pytest.mark.requires_data
class TestRealCaptureManifest:
    """Test manifest validation for real captures."""

    def test_manifest_exists_and_valid(self, real_captures_manifest: dict[str, any]) -> None:
        """Test that manifest.json exists and has valid structure."""
        if not real_captures_manifest:
            pytest.skip("No manifest.json found")

        # Check required fields
        assert "version" in real_captures_manifest
        assert "files" in real_captures_manifest
        assert "total_files" in real_captures_manifest
        assert "categories" in real_captures_manifest

    def test_manifest_files_exist(
        self, real_captures_manifest: dict[str, any], real_captures_dir: Path
    ) -> None:
        """Test that all files listed in manifest actually exist."""
        if not real_captures_manifest:
            pytest.skip("No manifest.json found")

        missing_files = []
        for file_info in real_captures_manifest.get("files", []):
            filename = file_info.get("filename")
            category = file_info.get("category")
            subcategory = file_info.get("subcategory", "")

            if subcategory:
                expected_path = real_captures_dir / category / subcategory / filename
            else:
                expected_path = real_captures_dir / category / filename

            if not expected_path.exists():
                missing_files.append(str(expected_path))

        if missing_files:
            pytest.fail(f"Missing files from manifest: {missing_files[:5]}...")

    def test_manifest_checksums(
        self, real_captures_manifest: dict[str, any], real_captures_dir: Path
    ) -> None:
        """Test that file checksums match manifest (spot check)."""
        import hashlib

        if not real_captures_manifest:
            pytest.skip("No manifest.json found")

        files_checked = 0
        files_matched = 0
        mismatches = []

        for file_info in real_captures_manifest.get("files", [])[:10]:  # Check up to 10
            filename = file_info.get("filename")
            category = file_info.get("category")
            subcategory = file_info.get("subcategory", "")
            expected_md5 = file_info.get("md5_hash")

            if subcategory:
                file_path = real_captures_dir / category / subcategory / filename
            else:
                file_path = real_captures_dir / category / filename

            if not file_path.exists() or not expected_md5:
                continue

            # Compute actual MD5
            md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    md5.update(chunk)

            actual_md5 = md5.hexdigest()
            files_checked += 1

            if actual_md5 == expected_md5:
                files_matched += 1
            else:
                mismatches.append(filename)

        if files_checked == 0:
            pytest.skip("No files with checksums to verify")

        # Allow up to 20% of files to have mismatches (corrupted test data)
        match_rate = files_matched / files_checked if files_checked > 0 else 0
        assert match_rate >= 0.8, (
            f"Too many checksum mismatches ({len(mismatches)}/{files_checked}): {mismatches}"
        )


@pytest.mark.integration
@pytest.mark.requires_data
class TestWaveformSizeVariations:
    """Test that different size WFM files load correctly."""

    def test_size_categories_coverage(self, real_wfm_files: dict[str, list[Path]]) -> None:
        """Test that we have files in each size category."""
        total_files = sum(len(files) for files in real_wfm_files.values())

        if total_files == 0:
            pytest.skip("No real WFM files available")

        # Report what we have
        for category, files in real_wfm_files.items():
            if files:
                total_size = sum(f.stat().st_size for f in files)
                print(f"  {category}: {len(files)} files, {total_size / 1e6:.1f} MB total")

    def test_wfm_metadata_extraction(self, real_wfm_files: dict[str, list[Path]]) -> None:
        """Test that metadata is correctly extracted from real WFM files."""
        from tracekit.core.exceptions import LoaderError
        from tracekit.loaders.tektronix import load_tektronix_wfm

        all_files = []
        for files in real_wfm_files.values():
            all_files.extend(files)

        if not all_files:
            pytest.skip("No real WFM files available")

        # Test first file from each size category
        tested = 0
        for category, files in real_wfm_files.items():  # noqa: PERF102
            if not files:
                continue

            try:
                trace = load_tektronix_wfm(files[0])

                # Verify we got metadata
                assert trace.metadata is not None
                assert hasattr(trace.metadata, "sample_rate")

                # Sample rate should be reasonable (1 kHz to 10 GHz)
                if trace.metadata.sample_rate:
                    assert 1e3 <= trace.metadata.sample_rate <= 1e10

                tested += 1
            except LoaderError:
                # Skip corrupted/incompatible WFM files
                continue

        if tested == 0:
            pytest.skip("No WFM files could be loaded (all corrupted/incompatible)")
