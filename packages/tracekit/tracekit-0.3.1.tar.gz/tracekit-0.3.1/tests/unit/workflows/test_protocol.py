"""Comprehensive unit tests for protocol debug workflow.

Requirements tested:

This test suite covers:
- Protocol auto-detection and decoding
- Error context extraction
- Protocol-specific decoding (UART, SPI, I2C, CAN)
- Configuration handling
- Statistics calculation
- Waveform to digital conversion
"""

from __future__ import annotations

from unittest.mock import Mock, patch

import numpy as np
import pytest

from tracekit.core.exceptions import AnalysisError
from tracekit.core.types import DigitalTrace, ProtocolPacket, TraceMetadata, WaveformTrace
from tracekit.workflows.protocol import (
    _decode_can,
    _decode_i2c,
    _decode_spi,
    _decode_uart,
    _extract_context,
    _get_default_protocol_config,
    _to_digital,
    debug_protocol,
)

pytestmark = pytest.mark.unit


@pytest.fixture
def waveform_trace():
    """Create a simple waveform trace for testing."""
    sample_rate = 1e6  # 1 MHz
    duration = 1e-3  # 1 ms
    n_samples = int(sample_rate * duration)

    # Create a square wave
    t = np.linspace(0, duration, n_samples)
    data = np.sin(2 * np.pi * 1000 * t)  # 1 kHz sine wave

    metadata = TraceMetadata(sample_rate=sample_rate)
    return WaveformTrace(data=data, metadata=metadata)


@pytest.fixture
def digital_trace():
    """Create a simple digital trace for testing."""
    sample_rate = 1e6  # 1 MHz
    n_samples = 1000

    # Create a digital pattern
    data = np.array([bool(i % 2) for i in range(n_samples)])

    metadata = TraceMetadata(sample_rate=sample_rate)
    return DigitalTrace(data=data, metadata=metadata)


@pytest.fixture
def protocol_packet():
    """Create a protocol packet with errors."""
    return ProtocolPacket(
        timestamp=1.5e-3,
        protocol="UART",
        data=b"\xaa",
        errors=["parity_error", "framing_error"],
        annotations={"address": 0x42},
    )


@pytest.mark.unit
class TestToDigital:
    """Test waveform to digital conversion."""

    def test_digital_trace_passthrough(self, digital_trace):
        """Test that digital traces are passed through unchanged."""
        result = _to_digital(digital_trace)

        assert result is digital_trace
        assert isinstance(result, DigitalTrace)

    def test_waveform_conversion(self, waveform_trace):
        """Test waveform to digital conversion."""
        result = _to_digital(waveform_trace)

        assert isinstance(result, DigitalTrace)
        assert len(result.data) == len(waveform_trace.data)
        assert result.data.dtype == np.bool_
        assert result.metadata == waveform_trace.metadata

    def test_threshold_calculation(self):
        """Test that threshold is calculated correctly."""
        data = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
        metadata = TraceMetadata(sample_rate=1e6)
        trace = WaveformTrace(data=data, metadata=metadata)

        result = _to_digital(trace)

        # Threshold should be (0 + 4) / 2 = 2.0
        # So values > 2.0 should be True
        expected = np.array([False, False, False, True, True])
        np.testing.assert_array_equal(result.data, expected)

    def test_preserves_metadata(self, waveform_trace):
        """Test that metadata is preserved during conversion."""
        result = _to_digital(waveform_trace)

        assert result.metadata.sample_rate == waveform_trace.metadata.sample_rate
        assert result.metadata.source_file == waveform_trace.metadata.source_file


@pytest.mark.unit
class TestGetDefaultProtocolConfig:
    """Test default protocol configuration retrieval."""

    def test_uart_config(self):
        """Test UART default configuration."""
        config = _get_default_protocol_config("UART")

        assert config["baud_rate"] == 115200
        assert config["data_bits"] == 8
        assert config["parity"] == "none"
        assert config["stop_bits"] == 1

    def test_spi_config(self):
        """Test SPI default configuration."""
        config = _get_default_protocol_config("SPI")

        assert config["clock_polarity"] == 0
        assert config["clock_phase"] == 0
        assert config["bit_order"] == "MSB"

    def test_i2c_config(self):
        """Test I2C default configuration."""
        config = _get_default_protocol_config("I2C")

        assert config["clock_rate"] == 100000
        assert config["address_bits"] == 7

    def test_can_config(self):
        """Test CAN default configuration."""
        config = _get_default_protocol_config("CAN")

        assert config["baud_rate"] == 500000
        assert config["sample_point"] == 0.75

    def test_unknown_protocol(self):
        """Test that unknown protocol returns empty dict."""
        config = _get_default_protocol_config("UNKNOWN")

        assert config == {}

    def test_case_sensitive(self):
        """Test that protocol name must be uppercase."""
        config = _get_default_protocol_config("uart")

        assert config == {}


@pytest.mark.unit
class TestExtractContext:
    """Test context extraction around error points."""

    def test_context_extraction_waveform(self, waveform_trace):
        """Test extracting context from waveform trace."""
        sample_idx = 500
        context_samples = 100

        result = _extract_context(waveform_trace, sample_idx, context_samples)

        assert result is not None
        assert isinstance(result, WaveformTrace)
        assert len(result.data) == 200  # 100 before + 100 after
        assert result.metadata == waveform_trace.metadata

    def test_context_extraction_digital(self, digital_trace):
        """Test extracting context from digital trace."""
        sample_idx = 500
        context_samples = 50

        result = _extract_context(digital_trace, sample_idx, context_samples)

        assert result is not None
        assert isinstance(result, DigitalTrace)
        assert len(result.data) == 100  # 50 before + 50 after

    def test_context_at_start(self, waveform_trace):
        """Test context extraction at start of trace."""
        sample_idx = 10
        context_samples = 100

        result = _extract_context(waveform_trace, sample_idx, context_samples)

        assert result is not None
        # Should start at 0, not -90
        assert len(result.data) <= 110

    def test_context_at_end(self, waveform_trace):
        """Test context extraction at end of trace."""
        sample_idx = len(waveform_trace.data) - 10
        context_samples = 100

        result = _extract_context(waveform_trace, sample_idx, context_samples)

        assert result is not None
        # Should not go past end of data
        assert len(result.data) <= 110

    def test_invalid_sample_index(self, waveform_trace):
        """Test handling of invalid sample index."""
        # Context that would result in empty or invalid range
        sample_idx = 0
        context_samples = 0

        result = _extract_context(waveform_trace, sample_idx, context_samples)

        assert result is None

    def test_context_preserves_type(self, digital_trace):
        """Test that context preserves trace type."""
        result = _extract_context(digital_trace, 500, 100)

        assert isinstance(result, DigitalTrace)
        assert not isinstance(result, WaveformTrace)


@pytest.mark.unit
class TestDecodeUART:
    """Test UART protocol decoding."""

    @patch("tracekit.analyzers.protocols.uart.UARTDecoder")
    def test_basic_decoding(self, mock_decoder_class, digital_trace):
        """Test basic UART decoding."""
        # Setup mock
        mock_decoder = Mock()
        mock_decoder_class.return_value = mock_decoder

        packet = ProtocolPacket(timestamp=1e-3, protocol="UART", data=b"A", errors=[])
        mock_decoder.decode.return_value = [packet]

        config = {"baud_rate": 115200, "data_bits": 8, "parity": "none", "stop_bits": 1}
        packets, errors = _decode_uart(digital_trace, config, 100, None, digital_trace)

        # Verify decoder was initialized correctly
        mock_decoder_class.assert_called_once_with(
            baudrate=115200, data_bits=8, parity="none", stop_bits=1
        )

        # Verify decoding was called
        mock_decoder.decode.assert_called_once_with(digital_trace)

        assert len(packets) == 1
        assert len(errors) == 0

    @patch("tracekit.analyzers.protocols.uart.UARTDecoder")
    def test_error_detection(self, mock_decoder_class, digital_trace):
        """Test UART error detection and context extraction."""
        mock_decoder = Mock()
        mock_decoder_class.return_value = mock_decoder

        # Create packet with errors
        packet = ProtocolPacket(
            timestamp=1e-3,
            protocol="UART",
            data=b"A",
            errors=["parity_error"],
        )
        mock_decoder.decode.return_value = [packet]

        config = {"baud_rate": 115200, "data_bits": 8, "parity": "none", "stop_bits": 1}
        packets, errors = _decode_uart(digital_trace, config, 100, None, digital_trace)

        assert len(errors) == 1
        error = errors[0]
        assert error["type"] == "parity_error"
        assert error["timestamp"] == 1e-3
        assert error["packet_index"] == 0
        assert error["data"] == b"A"
        assert "context" in error
        assert "context_trace" in error

    @patch("tracekit.analyzers.protocols.uart.UARTDecoder")
    def test_error_type_filtering(self, mock_decoder_class, digital_trace):
        """Test filtering errors by type."""
        mock_decoder = Mock()
        mock_decoder_class.return_value = mock_decoder

        packet = ProtocolPacket(
            timestamp=1e-3,
            protocol="UART",
            data=b"A",
            errors=["parity_error", "framing_error"],
        )
        mock_decoder.decode.return_value = [packet]

        config = {"baud_rate": 115200, "data_bits": 8, "parity": "none", "stop_bits": 1}

        # Filter to only parity errors
        packets, errors = _decode_uart(digital_trace, config, 100, ["parity"], digital_trace)

        assert len(errors) == 1
        assert errors[0]["type"] == "parity_error"

    @patch("tracekit.analyzers.protocols.uart.UARTDecoder")
    def test_multiple_packets_with_errors(self, mock_decoder_class, digital_trace):
        """Test handling multiple packets with errors."""
        mock_decoder = Mock()
        mock_decoder_class.return_value = mock_decoder

        packets_list = [
            ProtocolPacket(timestamp=1e-3, protocol="UART", data=b"A", errors=[]),
            ProtocolPacket(timestamp=2e-3, protocol="UART", data=b"B", errors=["parity_error"]),
            ProtocolPacket(timestamp=3e-3, protocol="UART", data=b"C", errors=["framing_error"]),
        ]
        mock_decoder.decode.return_value = packets_list

        config = {"baud_rate": 115200, "data_bits": 8, "parity": "none", "stop_bits": 1}
        packets, errors = _decode_uart(digital_trace, config, 100, None, digital_trace)

        assert len(packets) == 3
        assert len(errors) == 2
        assert errors[0]["packet_index"] == 1
        assert errors[1]["packet_index"] == 2


@pytest.mark.unit
class TestDecodeSPI:
    """Test SPI protocol decoding."""

    @patch("tracekit.analyzers.protocols.spi.SPIDecoder")
    def test_basic_decoding(self, mock_decoder_class, digital_trace):
        """Test basic SPI decoding."""
        mock_decoder = Mock()
        mock_decoder_class.return_value = mock_decoder

        packet = ProtocolPacket(timestamp=1e-3, protocol="SPI", data=b"\xff", errors=[])
        mock_decoder.decode.return_value = [packet]

        config = {"clock_polarity": 0, "clock_phase": 0, "bit_order": "msb"}
        packets, errors = _decode_spi(digital_trace, config, 100, None, digital_trace)

        # Verify decoder initialization
        mock_decoder_class.assert_called_once_with(cpol=0, cpha=0, word_size=8, bit_order="msb")

        assert len(packets) == 1
        assert len(errors) == 0

    @patch("tracekit.analyzers.protocols.spi.SPIDecoder")
    def test_error_handling(self, mock_decoder_class, digital_trace):
        """Test SPI error handling."""
        mock_decoder = Mock()
        mock_decoder_class.return_value = mock_decoder

        packet = ProtocolPacket(timestamp=1e-3, protocol="SPI", data=b"\xff", errors=["cs_error"])
        mock_decoder.decode.return_value = [packet]

        config = {"clock_polarity": 0, "clock_phase": 0, "bit_order": "msb"}
        packets, errors = _decode_spi(digital_trace, config, 100, None, digital_trace)

        assert len(errors) == 1
        assert errors[0]["type"] == "cs_error"
        assert "mosi_data" in errors[0]

    @patch("tracekit.analyzers.protocols.spi.SPIDecoder")
    def test_word_size_configuration(self, mock_decoder_class, digital_trace):
        """Test SPI with custom word size."""
        mock_decoder = Mock()
        mock_decoder_class.return_value = mock_decoder
        mock_decoder.decode.return_value = []

        config = {
            "clock_polarity": 1,
            "clock_phase": 1,
            "bit_order": "lsb",
            "word_size": 16,
        }
        _decode_spi(digital_trace, config, 100, None, digital_trace)

        mock_decoder_class.assert_called_once_with(cpol=1, cpha=1, word_size=16, bit_order="lsb")


@pytest.mark.unit
class TestDecodeI2C:
    """Test I2C protocol decoding."""

    @patch("tracekit.analyzers.protocols.i2c.I2CDecoder")
    def test_basic_decoding(self, mock_decoder_class, digital_trace):
        """Test basic I2C decoding."""
        mock_decoder = Mock()
        mock_decoder_class.return_value = mock_decoder

        packet = ProtocolPacket(
            timestamp=1e-3,
            protocol="I2C",
            data=b"\x42",
            annotations={"address": 0x50},
        )
        mock_decoder.decode.return_value = [packet]

        config = {"address_format": "7bit"}
        packets, errors = _decode_i2c(digital_trace, config, 100, None, digital_trace)

        # Verify decoder initialization
        mock_decoder_class.assert_called_once_with(address_format="7bit")

        assert len(packets) == 1

    @patch("tracekit.analyzers.protocols.i2c.I2CDecoder")
    def test_error_with_address(self, mock_decoder_class, digital_trace):
        """Test I2C error includes address information."""
        mock_decoder = Mock()
        mock_decoder_class.return_value = mock_decoder

        packet = ProtocolPacket(
            timestamp=1e-3,
            protocol="I2C",
            data=b"\x42",
            errors=["nack"],
            annotations={"address": 0x50},
        )
        mock_decoder.decode.return_value = [packet]

        config = {"address_format": "auto"}
        packets, errors = _decode_i2c(digital_trace, config, 100, None, digital_trace)

        assert len(errors) == 1
        assert errors[0]["address"] == 0x50
        assert errors[0]["type"] == "nack"

    def test_insufficient_edges(self, digital_trace):
        """Test I2C with insufficient edges returns empty results."""
        # Create trace with very few transitions
        data = np.ones(100, dtype=bool)
        trace = DigitalTrace(data=data, metadata=TraceMetadata(sample_rate=1e6))

        config = {"address_format": "auto"}
        packets, errors = _decode_i2c(trace, config, 100, None, trace)

        assert len(packets) == 0
        assert len(errors) == 0


@pytest.mark.unit
class TestDecodeCAN:
    """Test CAN protocol decoding."""

    @patch("tracekit.analyzers.protocols.can.CANDecoder")
    def test_basic_decoding(self, mock_decoder_class, digital_trace):
        """Test basic CAN decoding."""
        mock_decoder = Mock()
        mock_decoder_class.return_value = mock_decoder

        packet = ProtocolPacket(
            timestamp=1e-3,
            protocol="CAN",
            data=b"\x01\x02\x03",
            annotations={"arbitration_id": 0x123},
        )
        mock_decoder.decode.return_value = [packet]

        config = {"baud_rate": 500000, "sample_point": 0.75}
        packets, errors = _decode_can(digital_trace, config, 100, None, digital_trace)

        # Verify decoder initialization
        mock_decoder_class.assert_called_once_with(bitrate=500000, sample_point=0.75)

        assert len(packets) == 1

    @patch("tracekit.analyzers.protocols.can.CANDecoder")
    def test_error_with_arbitration_id(self, mock_decoder_class, digital_trace):
        """Test CAN error includes arbitration ID."""
        mock_decoder = Mock()
        mock_decoder_class.return_value = mock_decoder

        packet = ProtocolPacket(
            timestamp=1e-3,
            protocol="CAN",
            data=b"\x01\x02",
            errors=["crc_error"],
            annotations={"arbitration_id": 0x7FF},
        )
        mock_decoder.decode.return_value = [packet]

        config = {"baud_rate": 1000000, "sample_point": 0.8}
        packets, errors = _decode_can(digital_trace, config, 100, None, digital_trace)

        assert len(errors) == 1
        assert errors[0]["arbitration_id"] == 0x7FF
        assert errors[0]["type"] == "crc_error"


@pytest.mark.unit
class TestDebugProtocol:
    """Test the main debug_protocol workflow function."""

    @patch("tracekit.inference.protocol.detect_protocol")
    @patch("tracekit.workflows.protocol._decode_uart")
    def test_auto_detection(self, mock_decode_uart, mock_detect, waveform_trace):
        """Test protocol auto-detection."""
        # Mock detection result
        mock_detect.return_value = {
            "protocol": "UART",
            "confidence": 0.85,
            "config": {"baud_rate": 115200, "data_bits": 8, "parity": "none", "stop_bits": 1},
        }

        # Mock decoder result - packet with errors so it shows up in results
        packet = ProtocolPacket(timestamp=1e-3, protocol="UART", data=b"A", errors=["test_error"])
        mock_decode_uart.return_value = ([packet], [])

        result = debug_protocol(waveform_trace, protocol=None)

        # Verify detection was called
        mock_detect.assert_called_once()

        assert result["protocol"] == "UART"
        assert result["baud_rate"] == 115200
        assert len(result["packets"]) == 1
        assert result["statistics"]["confidence"] == 0.85

    @patch("tracekit.inference.protocol.detect_protocol")
    @patch("tracekit.workflows.protocol._decode_uart")
    def test_explicit_protocol(self, mock_decode_uart, mock_detect, waveform_trace):
        """Test with explicitly specified protocol."""
        packet = ProtocolPacket(timestamp=1e-3, protocol="UART", data=b"A")
        mock_decode_uart.return_value = ([packet], [])

        result = debug_protocol(waveform_trace, protocol="UART")

        # Detection should not be called
        mock_detect.assert_not_called()

        assert result["protocol"] == "UART"
        assert result["statistics"]["confidence"] == 1.0

    @patch("tracekit.workflows.protocol._decode_spi")
    def test_spi_protocol(self, mock_decode_spi, waveform_trace):
        """Test SPI protocol decoding."""
        packet = ProtocolPacket(timestamp=1e-3, protocol="SPI", data=b"\xff")
        mock_decode_spi.return_value = ([packet], [])

        result = debug_protocol(waveform_trace, protocol="SPI")

        assert result["protocol"] == "SPI"
        mock_decode_spi.assert_called_once()

    @patch("tracekit.workflows.protocol._decode_i2c")
    def test_i2c_protocol(self, mock_decode_i2c, waveform_trace):
        """Test I2C protocol decoding."""
        packet = ProtocolPacket(timestamp=1e-3, protocol="I2C", data=b"\x42")
        mock_decode_i2c.return_value = ([packet], [])

        result = debug_protocol(waveform_trace, protocol="I2C")

        assert result["protocol"] == "I2C"
        assert result["baud_rate"] == 100000  # clock_rate from I2C config

    @patch("tracekit.workflows.protocol._decode_can")
    def test_can_protocol(self, mock_decode_can, waveform_trace):
        """Test CAN protocol decoding."""
        packet = ProtocolPacket(timestamp=1e-3, protocol="CAN", data=b"\x01\x02")
        mock_decode_can.return_value = ([packet], [])

        result = debug_protocol(waveform_trace, protocol="CAN")

        assert result["protocol"] == "CAN"
        assert result["baud_rate"] == 500000

    def test_unsupported_protocol(self, waveform_trace):
        """Test error on unsupported protocol."""
        with pytest.raises(AnalysisError, match="Unsupported protocol"):
            debug_protocol(waveform_trace, protocol="UNKNOWN")

    @patch("tracekit.workflows.protocol._decode_uart")
    def test_decode_all_packets(self, mock_decode_uart, waveform_trace):
        """Test decoding all packets vs only error packets."""
        packets = [
            ProtocolPacket(timestamp=1e-3, protocol="UART", data=b"A", errors=[]),
            ProtocolPacket(timestamp=2e-3, protocol="UART", data=b"B", errors=["parity_error"]),
            ProtocolPacket(timestamp=3e-3, protocol="UART", data=b"C", errors=[]),
        ]
        mock_decode_uart.return_value = (packets, [{"type": "parity_error"}])

        # Test decode_all=True
        result = debug_protocol(waveform_trace, protocol="UART", decode_all=True)
        assert len(result["packets"]) == 3

        # Test decode_all=False (default)
        result = debug_protocol(waveform_trace, protocol="UART", decode_all=False)
        assert len(result["packets"]) == 1  # Only packet with errors

    @patch("tracekit.workflows.protocol._decode_uart")
    def test_statistics_calculation(self, mock_decode_uart, waveform_trace):
        """Test statistics calculation."""
        packets = [
            ProtocolPacket(timestamp=1e-3, protocol="UART", data=b"A", errors=["error1"]),
            ProtocolPacket(timestamp=2e-3, protocol="UART", data=b"B", errors=["error2"]),
        ]
        errors = [{"type": "error1"}, {"type": "error2"}]
        mock_decode_uart.return_value = (packets, errors)

        result = debug_protocol(waveform_trace, protocol="UART", decode_all=True)

        stats = result["statistics"]
        assert stats["total_packets"] == 2
        assert stats["error_count"] == 2
        assert stats["error_rate"] == 1.0  # 2/2
        assert stats["confidence"] == 1.0

    @patch("tracekit.workflows.protocol._decode_uart")
    def test_zero_packets(self, mock_decode_uart, waveform_trace):
        """Test handling of zero packets."""
        mock_decode_uart.return_value = ([], [])

        result = debug_protocol(waveform_trace, protocol="UART")

        stats = result["statistics"]
        assert stats["total_packets"] == 0
        assert stats["error_count"] == 0
        assert stats["error_rate"] == 0

    @patch("tracekit.workflows.protocol._decode_uart")
    def test_context_samples_parameter(self, mock_decode_uart, waveform_trace):
        """Test context_samples parameter is passed through."""
        mock_decode_uart.return_value = ([], [])

        debug_protocol(waveform_trace, protocol="UART", context_samples=200)

        # Verify context_samples was passed to decoder
        call_args = mock_decode_uart.call_args
        assert call_args[0][2] == 200  # Third positional argument

    @patch("tracekit.workflows.protocol._decode_uart")
    def test_error_types_parameter(self, mock_decode_uart, waveform_trace):
        """Test error_types parameter is passed through."""
        mock_decode_uart.return_value = ([], [])

        error_types = ["parity", "framing"]
        debug_protocol(waveform_trace, protocol="UART", error_types=error_types)

        # Verify error_types was passed to decoder
        call_args = mock_decode_uart.call_args
        assert call_args[0][3] == error_types

    def test_digital_trace_input(self, digital_trace):
        """Test that digital traces are handled correctly."""
        with patch("tracekit.workflows.protocol._decode_uart") as mock_decode:
            mock_decode.return_value = ([], [])

            debug_protocol(digital_trace, protocol="UART")

            # Should be passed directly without conversion
            call_args = mock_decode.call_args
            assert isinstance(call_args[0][0], DigitalTrace)

    @patch("tracekit.inference.protocol.detect_protocol")
    def test_auto_protocol_string(self, mock_detect, waveform_trace):
        """Test protocol='auto' triggers detection."""
        mock_detect.return_value = {
            "protocol": "UART",
            "confidence": 0.9,
            "config": {"baud_rate": 9600},
        }

        with patch("tracekit.workflows.protocol._decode_uart") as mock_decode:
            mock_decode.return_value = ([], [])

            result = debug_protocol(waveform_trace, protocol="auto")

            mock_detect.assert_called_once()
            assert result["protocol"] == "UART"

    @patch("tracekit.workflows.protocol._decode_uart")
    def test_config_in_result(self, mock_decode_uart, waveform_trace):
        """Test that config is included in result."""
        mock_decode_uart.return_value = ([], [])

        result = debug_protocol(waveform_trace, protocol="UART")

        assert "config" in result
        assert result["config"]["baud_rate"] == 115200
        assert result["config"]["data_bits"] == 8

    @patch("tracekit.workflows.protocol._decode_uart")
    def test_packets_in_result(self, mock_decode_uart, waveform_trace):
        """Test that packets are included in result."""
        packet = ProtocolPacket(timestamp=1e-3, protocol="UART", data=b"A")
        mock_decode_uart.return_value = ([packet], [])

        result = debug_protocol(waveform_trace, protocol="UART", decode_all=True)

        assert "packets" in result
        assert len(result["packets"]) == 1
        assert result["packets"][0] is packet

    @patch("tracekit.workflows.protocol._decode_uart")
    def test_errors_in_result(self, mock_decode_uart, waveform_trace):
        """Test that errors are included in result."""
        error = {"type": "parity_error", "timestamp": 1e-3}
        mock_decode_uart.return_value = ([], [error])

        result = debug_protocol(waveform_trace, protocol="UART")

        assert "errors" in result
        assert len(result["errors"]) == 1
        assert result["errors"][0] == error

    @patch("tracekit.workflows.protocol._decode_spi")
    def test_clock_rate_in_result(self, mock_decode_spi, waveform_trace):
        """Test that clock_rate is used for baud_rate when baud_rate not present."""
        mock_decode_spi.return_value = ([], [])

        # I2C uses clock_rate instead of baud_rate
        with patch("tracekit.workflows.protocol._decode_i2c") as mock_decode_i2c:
            mock_decode_i2c.return_value = ([], [])

            result = debug_protocol(waveform_trace, protocol="I2C")

            # Should use clock_rate as baud_rate
            assert result["baud_rate"] == 100000


@pytest.mark.unit
class TestProtocolWorkflowIntegration:
    """Integration tests for the protocol workflow."""

    def test_full_workflow_with_errors(self, waveform_trace):
        """Test complete workflow from trace to error reporting."""
        with patch("tracekit.inference.protocol.detect_protocol") as mock_detect:
            mock_detect.return_value = {
                "protocol": "UART",
                "confidence": 0.9,
                "config": {"baud_rate": 115200, "data_bits": 8, "parity": "none", "stop_bits": 1},
            }

            with patch("tracekit.workflows.protocol._decode_uart") as mock_decode:
                # Create packets with and without errors
                packets = [
                    ProtocolPacket(timestamp=1e-3, protocol="UART", data=b"A", errors=[]),
                    ProtocolPacket(
                        timestamp=2e-3,
                        protocol="UART",
                        data=b"B",
                        errors=["parity_error"],
                    ),
                ]
                errors = [
                    {
                        "type": "parity_error",
                        "timestamp": 2e-3,
                        "packet_index": 1,
                        "data": b"B",
                        "context": "Samples 1900 to 2100",
                    }
                ]
                mock_decode.return_value = (packets, errors)

                result = debug_protocol(waveform_trace)

                # Verify complete result structure
                assert result["protocol"] == "UART"
                assert result["baud_rate"] == 115200
                assert len(result["packets"]) == 1  # Only error packets by default
                assert len(result["errors"]) == 1
                assert result["statistics"]["total_packets"] == 1
                assert result["statistics"]["error_count"] == 1
                assert result["statistics"]["error_rate"] == 1.0
                assert result["statistics"]["confidence"] == 0.9

    def test_case_insensitive_protocol(self, waveform_trace):
        """Test that protocol names are case-insensitive."""
        with patch("tracekit.workflows.protocol._decode_uart") as mock_decode:
            mock_decode.return_value = ([], [])

            # Try lowercase
            result = debug_protocol(waveform_trace, protocol="uart")
            assert result["protocol"] == "UART"

            # Try mixed case
            result = debug_protocol(waveform_trace, protocol="UaRt")
            assert result["protocol"] == "UART"
