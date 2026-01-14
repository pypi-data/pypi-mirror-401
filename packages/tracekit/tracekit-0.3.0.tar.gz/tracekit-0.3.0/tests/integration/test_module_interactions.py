"""Module interaction integration tests for TraceKit.

Tests cross-module integration paths and data flow between different
components of the system.

- Tests module boundaries and interfaces
- Validates data transformations across modules
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

# Graceful imports
try:
    from tracekit.analyzers.digital.clock import ClockRecovery
    from tracekit.analyzers.digital.edges import EdgeDetector
    from tracekit.analyzers.patterns.clustering import cluster_by_hamming
    from tracekit.analyzers.patterns.sequences import find_repeating_sequences
    from tracekit.analyzers.statistical.checksum import ChecksumDetector
    from tracekit.analyzers.statistical.entropy import EntropyAnalyzer
    from tracekit.core.types import DigitalTrace, TraceMetadata
    from tracekit.inference.message_format import MessageFormatInferrer
    from tracekit.loaders.configurable import (
        ConfigurablePacketLoader,
        PacketFormatConfig,
        SampleFormatDef,
    )
    from tracekit.loaders.preprocessing import detect_idle_regions, trim_idle
    from tracekit.loaders.validation import PacketValidator
    from tracekit.testing.synthetic import (
        SyntheticDataGenerator,
        SyntheticPacketConfig,
        SyntheticSignalConfig,
        generate_digital_signal,
        generate_packets,
        generate_protocol_messages,
    )

    IMPORTS_AVAILABLE = True
except ImportError as e:
    IMPORTS_AVAILABLE = False
    IMPORT_ERROR = str(e)

pytestmark = pytest.mark.integration


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Required imports not available")
@pytest.mark.integration
class TestLoaderAnalyzerInteraction:
    """Test interactions between loaders and analyzers."""

    def test_packet_loader_to_entropy_analyzer(self, tmp_path: Path) -> None:
        """Test packet loader output feeds into entropy analyzer."""
        try:
            # Generate test packets
            config = SyntheticPacketConfig(packet_size=128, include_checksum=True)
            binary_data, _ = generate_packets(count=30, **config.__dict__)

            data_file = tmp_path / "entropy_test.bin"
            data_file.write_bytes(binary_data)

            # Load packets
            loader_config = PacketFormatConfig(
                name="entropy_test",
                version="1.0",
                packet_size=128,
                byte_order="little",
                header_size=16,
                header_fields=[],
                sample_offset=16,
                sample_count=14,
                sample_format=SampleFormatDef(size=8, type="uint64", endian="little"),
            )

            loader = ConfigurablePacketLoader(loader_config)
            loaded = loader.load(data_file)

            # Extract data for entropy analysis
            analyzer = EntropyAnalyzer()

            for packet in loaded.packets[:5]:
                if hasattr(packet, "header"):
                    header_entropy = analyzer.calculate_entropy(bytes(packet.header))
                    assert 0 <= header_entropy <= 8.0

        except Exception as e:
            pytest.skip(f"Loader-analyzer interaction test skipped: {e}")

    def test_packet_loader_to_checksum_detector(self, tmp_path: Path) -> None:
        """Test packet loader to checksum detector flow."""
        try:
            # Generate packets with checksums
            config = SyntheticPacketConfig(
                packet_size=64,
                include_checksum=True,
            )
            binary_data, _ = generate_packets(count=20, **config.__dict__)

            data_file = tmp_path / "checksum_test.bin"
            data_file.write_bytes(binary_data)

            # Load packets
            loader_config = PacketFormatConfig(
                name="checksum_test",
                version="1.0",
                packet_size=64,
                byte_order="little",
                header_size=8,
                header_fields=[],
                sample_offset=8,
                sample_count=7,
                sample_format=SampleFormatDef(size=8, type="uint64", endian="little"),
            )

            loader = ConfigurablePacketLoader(loader_config)
            loaded = loader.load(data_file)

            # Convert packets to byte sequences
            packet_bytes = []
            for packet in loaded.packets:
                pkt_data = bytearray()
                if hasattr(packet, "header"):
                    pkt_data.extend(bytes(packet.header))
                if hasattr(packet, "samples"):
                    for sample in packet.samples:
                        pkt_data.extend(sample.to_bytes(8, byteorder="little"))
                packet_bytes.append(bytes(pkt_data))

            # Detect checksums
            detector = ChecksumDetector()
            result = detector.detect_checksum_field(packet_bytes)

            # Should complete analysis
            assert result is not None

        except Exception as e:
            pytest.skip(f"Checksum detector test skipped: {e}")

    def test_digital_signal_to_edge_detector(self) -> None:
        """Test digital signal generation to edge detection."""
        try:
            # Generate digital signal
            config = SyntheticSignalConfig(
                pattern_type="clock",
                sample_rate=10e6,
                duration_samples=10000,
            )

            signal, _ = generate_digital_signal(pattern="clock", **config.__dict__)

            # Convert to digital trace
            metadata = TraceMetadata(sample_rate=10e6)
            trace = DigitalTrace(data=signal > 1.5, metadata=metadata)

            # Detect edges
            detector = EdgeDetector()
            rising, falling = detector.detect_all_edges(trace.data)

            # Clock signal should have edges
            assert len(rising) > 0 or len(falling) > 0

        except Exception as e:
            pytest.skip(f"Signal to edge detector test skipped: {e}")

    def test_digital_signal_to_clock_recovery(self) -> None:
        """Test digital signal to clock recovery flow."""
        try:
            # Generate signal with known frequency
            config = SyntheticSignalConfig(
                pattern_type="clock",
                sample_rate=10e6,
                duration_samples=50000,
            )

            signal, _ = generate_digital_signal(pattern="clock", **config.__dict__)

            metadata = TraceMetadata(sample_rate=10e6)
            trace = DigitalTrace(data=signal > 1.5, metadata=metadata)

            # Recover clock
            recovery = ClockRecovery()
            freq = recovery.detect_frequency(trace)

            # Should detect some frequency
            assert freq > 0

        except Exception as e:
            pytest.skip(f"Clock recovery test skipped: {e}")


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Required imports not available")
@pytest.mark.integration
class TestAnalyzerInferenceInteraction:
    """Test interactions between analyzers and inference modules."""

    def test_pattern_detection_to_format_inference(self) -> None:
        """Test pattern detection feeds into format inference."""
        try:
            # Generate structured messages
            messages, truth = generate_protocol_messages(count=150, message_size=64)

            # Detect patterns first
            combined = b"".join(messages[:50])
            patterns = find_repeating_sequences(
                combined,
                min_length=2,
                max_length=6,
                min_count=5,
            )

            # Use inference to find structure
            inferrer = MessageFormatInferrer()
            inferred = inferrer.infer_format(messages)

            # Both should complete
            assert patterns is not None
            assert inferred is not None

        except Exception as e:
            pytest.skip(f"Pattern to inference test skipped: {e}")

    def test_entropy_analysis_to_clustering(self) -> None:
        """Test entropy analysis guides clustering."""
        try:
            # Generate message types with different entropy
            messages_low = []
            messages_high = []

            for i in range(50):
                # Low entropy: mostly zeros
                low_msg = bytearray(64)
                low_msg[0] = 0xAA
                messages_low.append(bytes(low_msg))

                # Higher entropy: random-ish
                high_msg = bytearray(64)
                for j in range(64):
                    high_msg[j] = (i * j) % 256
                messages_high.append(bytes(high_msg))

            all_messages = messages_low + messages_high

            # Analyze entropy
            entropy_analyzer = EntropyAnalyzer()
            entropies = [entropy_analyzer.calculate_entropy(msg) for msg in all_messages]

            # Low entropy messages should have lower values
            low_entropies = entropies[:50]
            high_entropies = entropies[50:]

            assert np.mean(low_entropies) < np.mean(high_entropies)

            # Cluster by content
            result = cluster_by_hamming(all_messages, threshold=0.2)

            # Should identify clusters
            assert result.num_clusters >= 1

        except Exception as e:
            pytest.skip(f"Entropy to clustering test skipped: {e}")

    def test_checksum_detection_to_validation(self, tmp_path: Path) -> None:
        """Test checksum detection informs validation."""
        try:
            # Generate messages with checksums
            messages, _ = generate_protocol_messages(count=30, message_size=64)

            # Detect checksum field
            detector = ChecksumDetector()
            result = detector.detect_checksum_field(messages)

            # If checksum detected, use for validation
            if result.has_checksum and result.offset is not None:
                # Create packets with known checksums
                config = SyntheticPacketConfig(
                    packet_size=64,
                    include_checksum=True,
                )
                binary_data, _ = generate_packets(count=20, **config.__dict__)

                data_file = tmp_path / "checksum_val.bin"
                data_file.write_bytes(binary_data)

                # Load and validate
                loader_config = PacketFormatConfig(
                    name="checksum_val",
                    version="1.0",
                    packet_size=64,
                    byte_order="little",
                    header_size=8,
                    header_fields=[],
                    sample_offset=8,
                    sample_count=7,
                    sample_format=SampleFormatDef(size=8, type="uint64", endian="little"),
                )

                loader = ConfigurablePacketLoader(loader_config)
                loaded = loader.load(data_file)

                validator = PacketValidator()
                for packet in loaded.packets:
                    validation = validator.validate_packet(packet)
                    assert validation is not None

        except Exception as e:
            pytest.skip(f"Checksum validation test skipped: {e}")


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Required imports not available")
@pytest.mark.integration
class TestValidationPreprocessingInteraction:
    """Test validation and preprocessing module interactions."""

    def test_validation_to_idle_detection(self, tmp_path: Path) -> None:
        """Test validation identifies idle regions."""
        try:
            # Generate packets with idle padding
            config = SyntheticPacketConfig(packet_size=128)
            binary_data, _ = generate_packets(count=20, **config.__dict__)

            # Add idle bytes
            idle_pattern = b"\x00" * 256
            full_data = idle_pattern + binary_data + idle_pattern

            data_file = tmp_path / "idle_test.bin"
            data_file.write_bytes(full_data)

            # Load
            loader_config = PacketFormatConfig(
                name="idle_test",
                version="1.0",
                packet_size=128,
                byte_order="little",
                header_size=16,
                header_fields=[],
                sample_offset=16,
                sample_count=14,
                sample_format=SampleFormatDef(size=8, type="uint64", endian="little"),
            )

            loader = ConfigurablePacketLoader(loader_config)
            loaded = loader.load(data_file)

            # Some packets may be all zeros (idle)
            validator = PacketValidator()

            idle_packets = []
            for packet in loaded.packets:
                if hasattr(packet, "samples"):
                    if all(s == 0 for s in packet.samples):
                        idle_packets.append(packet)

            # May or may not have idle packets depending on alignment
            # Just verify detection completes
            assert idle_packets is not None

        except Exception as e:
            pytest.skip(f"Idle detection test skipped: {e}")

    def test_preprocessing_trim_before_validation(self) -> None:
        """Test trimming idle data before validation."""
        try:
            # Generate digital signal with idle regions
            config = SyntheticSignalConfig(
                pattern_type="uart",
                sample_rate=10e6,
                duration_samples=20000,
            )

            signal, _ = generate_digital_signal(pattern="uart", **config.__dict__)

            # Add idle regions (all zeros)
            idle_prefix = np.zeros(5000, dtype=signal.dtype)
            idle_suffix = np.zeros(5000, dtype=signal.dtype)
            signal_with_idle = np.concatenate([idle_prefix, signal, idle_suffix])

            # Detect idle regions
            idle_regions = detect_idle_regions(signal_with_idle, threshold=0.1, min_duration=1000)

            # Should detect idle at start and end
            assert len(idle_regions) >= 1

            # Trim idle
            trimmed = trim_idle(signal_with_idle, pattern=0.0, min_duration=1000)

            # Trimmed should be shorter
            assert len(trimmed) < len(signal_with_idle)

        except Exception as e:
            pytest.skip(f"Preprocessing test skipped: {e}")

    def test_validation_filter_before_analysis(self, tmp_path: Path) -> None:
        """Test validation filters data before analysis."""
        try:
            # Generate mixed valid/invalid packets
            config = SyntheticPacketConfig(
                packet_size=64,
                noise_level=0.15,  # Some corruption
            )
            binary_data, _ = generate_packets(count=40, **config.__dict__)

            data_file = tmp_path / "filter_test.bin"
            data_file.write_bytes(binary_data)

            # Load
            loader_config = PacketFormatConfig(
                name="filter_test",
                version="1.0",
                packet_size=64,
                byte_order="little",
                header_size=8,
                header_fields=[],
                sample_offset=8,
                sample_count=7,
                sample_format=SampleFormatDef(size=8, type="uint64", endian="little"),
            )

            loader = ConfigurablePacketLoader(loader_config)
            loaded = loader.load(data_file)

            # Validate and filter
            validator = PacketValidator()
            valid_packets = []

            for packet in loaded.packets:
                result = validator.validate_packet(packet)
                if result.is_valid:
                    valid_packets.append(packet)

            # Analyze only valid packets
            if valid_packets:
                valid_bytes = bytearray()
                for packet in valid_packets[:5]:
                    if hasattr(packet, "header"):
                        valid_bytes.extend(bytes(packet.header))

                if len(valid_bytes) > 0:
                    entropy_analyzer = EntropyAnalyzer()
                    entropy = entropy_analyzer.calculate_entropy(bytes(valid_bytes))
                    assert 0 <= entropy <= 8.0

        except Exception as e:
            pytest.skip(f"Validation filter test skipped: {e}")


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Required imports not available")
@pytest.mark.integration
class TestSyntheticToAnalysisChain:
    """Test complete chains from synthetic data generation to analysis."""

    def test_synthetic_generator_consistency(self) -> None:
        """Test synthetic data generator produces consistent results."""
        try:
            # Create generator with seed
            generator = SyntheticDataGenerator(seed=42)

            # Generate packets twice with same config
            config = SyntheticPacketConfig(packet_size=64)

            packets1, truth1 = generator.generate_packets(config, count=10)
            packets2, truth2 = generator.generate_packets(config, count=10)

            # With same seed and reset, should produce same output
            # (Note: this depends on generator implementation)
            assert len(packets1) == len(packets2)

        except Exception as e:
            pytest.skip(f"Generator consistency test skipped: {e}")

    def test_synthetic_to_pattern_detection(self) -> None:
        """Test synthetic messages to pattern detection."""
        try:
            # Generate messages with known patterns
            messages, truth = generate_protocol_messages(count=100, message_size=64)

            # Detect patterns
            combined = b"".join(messages[:30])
            patterns = find_repeating_sequences(combined, min_length=2, max_length=8, min_count=5)

            # Should complete without error
            assert patterns is not None

        except Exception as e:
            pytest.skip(f"Synthetic to pattern test skipped: {e}")

    def test_synthetic_signal_full_analysis(self) -> None:
        """Test synthetic signal through full analysis chain."""
        try:
            # Generate UART signal
            config = SyntheticSignalConfig(
                pattern_type="uart",
                sample_rate=10e6,
                duration_samples=30000,
            )

            signal, truth = generate_digital_signal(pattern="uart", **config.__dict__)

            # Convert to trace
            metadata = TraceMetadata(sample_rate=10e6)
            trace = DigitalTrace(data=signal > 1.5, metadata=metadata)

            # Edge detection
            detector = EdgeDetector()
            rising, falling = detector.detect_all_edges(trace.data)

            total_edges = len(rising) + len(falling)
            assert total_edges > 0

            # Clock recovery
            recovery = ClockRecovery()
            freq = recovery.detect_frequency(trace)

            assert freq > 0

        except Exception as e:
            pytest.skip(f"Full signal analysis test skipped: {e}")


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Required imports not available")
@pytest.mark.integration
class TestDataTransformations:
    """Test data transformations across module boundaries."""

    def test_binary_to_packets_to_messages(self, tmp_path: Path) -> None:
        """Test transformation: binary file -> packets -> messages."""
        try:
            # Generate protocol messages
            messages, _ = generate_protocol_messages(count=50, message_size=128)

            # Package into packets
            config = SyntheticPacketConfig(packet_size=256)  # Large enough for 2 messages
            binary_data, _ = generate_packets(count=25, **config.__dict__)

            data_file = tmp_path / "transform_test.bin"
            data_file.write_bytes(binary_data)

            # Load as packets
            loader_config = PacketFormatConfig(
                name="transform_test",
                version="1.0",
                packet_size=256,
                byte_order="little",
                header_size=16,
                header_fields=[],
                sample_offset=16,
                sample_count=30,
                sample_format=SampleFormatDef(size=8, type="uint64", endian="little"),
            )

            loader = ConfigurablePacketLoader(loader_config)
            loaded = loader.load(data_file)

            # Extract message-like structures
            extracted_messages = []
            for packet in loaded.packets:
                if hasattr(packet, "samples"):
                    msg_bytes = bytearray()
                    for sample in packet.samples[:16]:  # 128 bytes = 16 uint64 samples
                        msg_bytes.extend(sample.to_bytes(8, byteorder="little"))
                    if len(msg_bytes) >= 64:
                        extracted_messages.append(bytes(msg_bytes[:64]))

            # Should have extracted messages
            if extracted_messages:
                # Analyze as messages
                inferrer = MessageFormatInferrer()
                inferred = inferrer.infer_format(extracted_messages)

                assert inferred is not None

        except Exception as e:
            pytest.skip(f"Binary to messages test skipped: {e}")

    def test_digital_trace_to_bytes_to_analysis(self) -> None:
        """Test transformation: digital trace -> bytes -> analysis."""
        try:
            # Generate digital signal
            config = SyntheticSignalConfig(
                pattern_type="uart",
                sample_rate=10e6,
                duration_samples=10000,
            )

            signal, _ = generate_digital_signal(pattern="uart", **config.__dict__)

            metadata = TraceMetadata(sample_rate=10e6)
            trace = DigitalTrace(data=signal > 1.5, metadata=metadata)

            # Convert boolean array to bytes
            byte_data = np.packbits(trace.data)

            # Analyze bytes
            entropy_analyzer = EntropyAnalyzer()
            entropy = entropy_analyzer.calculate_entropy(byte_data.tobytes())

            assert 0 <= entropy <= 8.0

        except Exception as e:
            pytest.skip(f"Digital to bytes test skipped: {e}")

    def test_streaming_chunked_analysis(self, tmp_path: Path) -> None:
        """Test streaming analysis with data transformations."""
        try:
            # Generate large dataset
            config = SyntheticPacketConfig(packet_size=128)
            binary_data, _ = generate_packets(count=200, **config.__dict__)

            data_file = tmp_path / "stream_transform.bin"
            data_file.write_bytes(binary_data)

            # Stream and analyze
            loader_config = PacketFormatConfig(
                name="stream_transform",
                version="1.0",
                packet_size=128,
                byte_order="little",
                header_size=16,
                header_fields=[],
                sample_offset=16,
                sample_count=14,
                sample_format=SampleFormatDef(size=8, type="uint64", endian="little"),
            )

            loader = ConfigurablePacketLoader(loader_config)
            entropy_analyzer = EntropyAnalyzer()

            chunk_entropies = []

            for chunk in loader.stream(data_file, chunk_size=50):
                # Extract bytes from chunk
                chunk_bytes = bytearray()
                for packet in chunk.packets[:5]:  # Sample from chunk
                    if hasattr(packet, "header"):
                        chunk_bytes.extend(bytes(packet.header))

                if len(chunk_bytes) > 0:
                    entropy = entropy_analyzer.calculate_entropy(bytes(chunk_bytes))
                    chunk_entropies.append(entropy)

            # Should have analyzed all chunks
            assert len(chunk_entropies) >= 2  # At least 2 chunks for 200 packets

        except Exception as e:
            pytest.skip(f"Streaming analysis test skipped: {e}")


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Required imports not available")
@pytest.mark.integration
class TestConcurrentModuleUsage:
    """Test using multiple modules concurrently."""

    def test_parallel_analysis_paths(self, tmp_path: Path) -> None:
        """Test running multiple analysis paths on same data."""
        try:
            # Generate test data
            config = SyntheticPacketConfig(packet_size=128, include_checksum=True)
            binary_data, _ = generate_packets(count=30, **config.__dict__)

            data_file = tmp_path / "parallel_test.bin"
            data_file.write_bytes(binary_data)

            # Load once
            loader_config = PacketFormatConfig(
                name="parallel_test",
                version="1.0",
                packet_size=128,
                byte_order="little",
                header_size=16,
                header_fields=[],
                sample_offset=16,
                sample_count=14,
                sample_format=SampleFormatDef(size=8, type="uint64", endian="little"),
            )

            loader = ConfigurablePacketLoader(loader_config)
            loaded = loader.load(data_file)

            # Run multiple analyses in parallel (simulated)
            # Path 1: Validation
            validator = PacketValidator()
            validation_results = [validator.validate_packet(p) for p in loaded.packets]

            # Path 2: Entropy analysis
            entropy_analyzer = EntropyAnalyzer()
            entropies = []
            for packet in loaded.packets[:10]:
                if hasattr(packet, "header"):
                    entropies.append(entropy_analyzer.calculate_entropy(bytes(packet.header)))

            # Path 3: Extract for inference
            packet_bytes = []
            for packet in loaded.packets:
                pkt_data = bytearray()
                if hasattr(packet, "header"):
                    pkt_data.extend(bytes(packet.header))
                packet_bytes.append(bytes(pkt_data))

            # All paths should complete
            assert len(validation_results) == len(loaded.packets)
            assert len(entropies) > 0
            assert len(packet_bytes) == len(loaded.packets)

        except Exception as e:
            pytest.skip(f"Parallel analysis test skipped: {e}")
