#!/usr/bin/env python3
"""Example 04: CAN Bus Protocol Decoding.

This example demonstrates CAN (Controller Area Network) bus decoding
including standard and extended frames, bitrate detection, and
error frame analysis.

Time: 25 minutes
Prerequisites: Digital signal concepts

Run:
    uv run python examples/04_protocol_decoding/04_can_decoding.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import numpy as np

from tracekit.analyzers.protocols.can import CAN_BITRATES, CANDecoder, CANFrame, decode_can
from tracekit.core.types import DigitalTrace, TraceMetadata


def main() -> None:
    """Demonstrate CAN bus decoding capabilities."""
    print("=" * 60)
    print("TraceKit Example: CAN Bus Protocol Decoding")
    print("=" * 60)

    # --- CAN Overview ---
    print("\n--- CAN Protocol Overview ---")

    print_can_overview()

    # --- Basic CAN Decoding ---
    print("\n--- Basic CAN Frame Decoding ---")

    demo_basic_can()

    # --- Extended CAN Frames ---
    print("\n--- Extended (29-bit) CAN Frames ---")

    demo_extended_frames()

    # --- Multiple Frames ---
    print("\n--- Multiple CAN Frames ---")

    demo_multiple_frames()

    # --- CAN Frame Analysis ---
    print("\n--- CAN Frame Analysis ---")

    demo_frame_analysis()

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. CAN uses differential signaling (CAN_H - CAN_L)")
    print("  2. Standard frames: 11-bit ID, Extended: 29-bit ID")
    print("  3. Dominant (0) overwrites recessive (1) for arbitration")
    print("  4. Bit stuffing after 5 consecutive same bits")
    print("  5. CRC-15 provides error detection")
    print("=" * 60)


def print_can_overview() -> None:
    """Print CAN protocol overview."""
    print("CAN Protocol Basics:")
    print("-" * 40)
    print("  - Differential bus (CAN_H - CAN_L)")
    print("  - Dominant bit (0): CAN_H > CAN_L")
    print("  - Recessive bit (1): CAN_H = CAN_L")
    print("\nSupported bitrates:")
    for bitrate, name in CAN_BITRATES.items():
        print(f"  {name:12s} ({bitrate:,} bps)")

    print("\nCAN frame structure:")
    print("  [SOF][Arbitration][Control][Data][CRC][ACK][EOF]")
    print("  - SOF: Start of Frame (1 dominant bit)")
    print("  - Arbitration: ID + RTR/IDE bits")
    print("  - Control: DLC (data length code)")
    print("  - Data: 0-8 bytes")
    print("  - CRC: 15-bit CRC + delimiter")
    print("  - ACK: Acknowledgment slot")
    print("  - EOF: End of Frame (7 recessive bits)")


def demo_basic_can() -> None:
    """Demonstrate basic CAN frame decoding."""
    sample_rate = 20e6  # 20 MHz
    bitrate = 500000  # 500 kbps

    # Generate a simple CAN frame
    frame = CANFrame(
        arbitration_id=0x123,
        is_extended=False,
        is_remote=False,
        dlc=8,
        data=bytes([0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]),
        crc=0,
        crc_computed=0,
        timestamp=0,
        end_timestamp=0,
        errors=[],
    )

    signal = generate_can_frame(frame, sample_rate=sample_rate, bitrate=bitrate)

    # Create trace
    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="CAN")
    trace = DigitalTrace(data=signal, metadata=metadata)

    print("CAN Frame to decode:")
    print(f"  Arbitration ID: 0x{frame.arbitration_id:03X}")
    print(f"  Data: {frame.data.hex()}")
    print(f"  Bitrate: {bitrate / 1000:.0f} kbps")

    # Decode
    decoder = CANDecoder(bitrate=bitrate)
    decoded_frames = list(decoder.decode(trace))

    print(f"\nDecoded {len(decoded_frames)} frame(s):")
    for i, pkt in enumerate(decoded_frames):
        print(f"\n  Frame {i + 1}:")
        print(f"    ID: 0x{pkt.annotations['arbitration_id']:03X}")
        print(f"    Extended: {pkt.annotations['is_extended']}")
        print(f"    Remote: {pkt.annotations['is_remote']}")
        print(f"    DLC: {pkt.annotations['dlc']}")
        print(f"    Data: {pkt.data.hex()}")
        print(f"    CRC valid: {pkt.annotations['crc_valid']}")


def demo_extended_frames() -> None:
    """Demonstrate extended (29-bit) CAN frames."""
    sample_rate = 20e6
    bitrate = 250000  # 250 kbps

    # Extended frame with 29-bit ID
    frame = CANFrame(
        arbitration_id=0x18DAF110,  # J1939-style extended ID
        is_extended=True,
        is_remote=False,
        dlc=8,
        data=bytes([0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10]),
        crc=0,
        crc_computed=0,
        timestamp=0,
        end_timestamp=0,
        errors=[],
    )

    signal = generate_can_frame(frame, sample_rate=sample_rate, bitrate=bitrate)

    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="CAN")
    trace = DigitalTrace(data=signal, metadata=metadata)

    print("Extended CAN Frame:")
    print(f"  29-bit ID: 0x{frame.arbitration_id:08X}")
    print(f"  Bitrate: {bitrate / 1000:.0f} kbps")

    decoder = CANDecoder(bitrate=bitrate)
    decoded = list(decoder.decode(trace))

    if decoded:
        pkt = decoded[0]
        print("\nDecoded:")
        print(f"  ID: 0x{pkt.annotations['arbitration_id']:08X}")
        print(f"  Extended frame: {pkt.annotations['is_extended']}")
        print(f"  Data: {pkt.data.hex()}")

        # Parse J1939-style ID
        ext_id = pkt.annotations["arbitration_id"]
        priority = (ext_id >> 26) & 0x7
        pgn = (ext_id >> 8) & 0x3FFFF
        source = ext_id & 0xFF

        print("\nJ1939 parsing:")
        print(f"  Priority: {priority}")
        print(f"  PGN: 0x{pgn:04X} ({pgn})")
        print(f"  Source Address: 0x{source:02X}")


def demo_multiple_frames() -> None:
    """Demonstrate decoding multiple CAN frames."""
    sample_rate = 50e6  # 50 MHz for higher resolution
    bitrate = 500000

    # Generate multiple frames
    frames_data = [
        {"id": 0x100, "data": bytes([0x01, 0x02])},
        {"id": 0x200, "data": bytes([0x10, 0x20, 0x30, 0x40])},
        {"id": 0x300, "data": bytes([0xFF, 0xEE, 0xDD, 0xCC, 0xBB, 0xAA, 0x99, 0x88])},
        {"id": 0x7DF, "data": bytes([0x02, 0x01, 0x00])},  # OBD-II request
    ]

    print(f"Generating {len(frames_data)} CAN frames:")
    for fd in frames_data:
        print(f"  ID: 0x{fd['id']:03X}, Data: {fd['data'].hex()}")

    # Generate combined signal
    all_bits = []
    idle_bits = 20  # Inter-frame spacing

    for fd in frames_data:
        frame = CANFrame(
            arbitration_id=fd["id"],
            is_extended=False,
            is_remote=False,
            dlc=len(fd["data"]),
            data=fd["data"],
            crc=0,
            crc_computed=0,
            timestamp=0,
            end_timestamp=0,
            errors=[],
        )
        frame_signal = generate_can_frame(frame, sample_rate=sample_rate, bitrate=bitrate)
        all_bits.extend(frame_signal.tolist())

        # Add idle time between frames
        samples_per_bit = int(sample_rate / bitrate)
        all_bits.extend([True] * (idle_bits * samples_per_bit))

    signal = np.array(all_bits, dtype=bool)
    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="CAN")
    trace = DigitalTrace(data=signal, metadata=metadata)

    # Decode all frames
    decoded = decode_can(trace, bitrate=bitrate)

    print(f"\nDecoded {len(decoded)} frames:")
    for i, frame in enumerate(decoded):
        print(f"\n  Frame {i + 1}:")
        print(f"    ID: 0x{frame.arbitration_id:03X}")
        print(f"    DLC: {frame.dlc}")
        print(f"    Data: {frame.data.hex()}")
        print(f"    Timestamp: {frame.timestamp * 1e6:.1f} us")
        if frame.errors:
            print(f"    Errors: {frame.errors}")


def demo_frame_analysis() -> None:
    """Demonstrate CAN frame analysis and statistics."""
    sample_rate = 50e6
    bitrate = 500000

    # Generate traffic pattern
    # Simulating periodic messages from different ECUs
    frames_data = []

    # Engine ECU (ID 0x100-0x10F)
    for i in range(5):
        frames_data.append(
            {
                "id": 0x100 + (i % 4),
                "data": bytes([i, (i * 10) & 0xFF, 0x00, 0x00]),
            }
        )

    # Transmission ECU (ID 0x200-0x20F)
    for i in range(3):
        frames_data.append(
            {
                "id": 0x200 + i,
                "data": bytes([0xA0 + i, 0xB0 + i]),
            }
        )

    # Generate signals
    all_bits = []
    samples_per_bit = int(sample_rate / bitrate)

    for fd in frames_data:
        frame = CANFrame(
            arbitration_id=fd["id"],
            is_extended=False,
            is_remote=False,
            dlc=len(fd["data"]),
            data=fd["data"],
            crc=0,
            crc_computed=0,
            timestamp=0,
            end_timestamp=0,
            errors=[],
        )
        frame_signal = generate_can_frame(frame, sample_rate=sample_rate, bitrate=bitrate)
        all_bits.extend(frame_signal.tolist())
        all_bits.extend([True] * (10 * samples_per_bit))

    signal = np.array(all_bits, dtype=bool)
    metadata = TraceMetadata(sample_rate=sample_rate, channel_name="CAN")
    trace = DigitalTrace(data=signal, metadata=metadata)

    decoded = decode_can(trace, bitrate=bitrate)

    # Analyze traffic
    print("CAN Bus Traffic Analysis:")
    print("-" * 40)

    # Count frames by ID
    id_counts: dict[int, int] = {}
    id_bytes: dict[int, int] = {}

    for frame in decoded:
        fid = frame.arbitration_id
        id_counts[fid] = id_counts.get(fid, 0) + 1
        id_bytes[fid] = id_bytes.get(fid, 0) + len(frame.data)

    print(f"\nTotal frames: {len(decoded)}")
    print(f"Unique IDs: {len(id_counts)}")

    print("\nFrame distribution by ID:")
    for fid in sorted(id_counts.keys()):
        count = id_counts[fid]
        total_bytes = id_bytes[fid]
        print(f"  0x{fid:03X}: {count} frames, {total_bytes} bytes")

    # Calculate bus load
    total_time = decoded[-1].end_timestamp - decoded[0].timestamp if decoded else 0
    total_bits = sum(
        (
            1  # SOF
            + 11  # ID
            + 1  # RTR
            + 1  # IDE
            + 1  # r0
            + 4  # DLC
            + f.dlc * 8  # Data
            + 15  # CRC
            + 1  # CRC delimiter
            + 1  # ACK
            + 1  # ACK delimiter
            + 7  # EOF
        )
        for f in decoded
    )

    if total_time > 0:
        bus_utilization = (total_bits / bitrate) / total_time * 100
        print(f"\nBus utilization: ~{bus_utilization:.1f}%")

    # Error statistics
    error_frames = [f for f in decoded if f.errors]
    print(f"Error frames: {len(error_frames)}")
    if error_frames:
        for f in error_frames:
            print(f"  ID 0x{f.arbitration_id:03X}: {f.errors}")


# --- Signal Generation Helper ---


def generate_can_frame(
    frame: CANFrame,
    sample_rate: float,
    bitrate: int,
) -> np.ndarray:
    """Generate CAN frame signal.

    This is a simplified generator for demonstration purposes.
    Real CAN signals have bit stuffing and more complex timing.

    Args:
        frame: CANFrame to encode
        sample_rate: Sample rate in Hz
        bitrate: CAN bitrate in bps

    Returns:
        Boolean array representing CAN signal (True=recessive, False=dominant)
    """
    samples_per_bit = int(sample_rate / bitrate)

    bits = []

    # SOF (dominant)
    bits.append(0)

    # Arbitration field
    if frame.is_extended:
        # Extended frame: 11-bit base ID + SRR + IDE + 18-bit extension
        base_id = (frame.arbitration_id >> 18) & 0x7FF
        ext_id = frame.arbitration_id & 0x3FFFF

        # Base ID (11 bits, MSB first)
        for i in range(11):
            bits.append((base_id >> (10 - i)) & 1)

        # SRR (recessive)
        bits.append(1)

        # IDE (recessive for extended)
        bits.append(1)

        # Extended ID (18 bits)
        for i in range(18):
            bits.append((ext_id >> (17 - i)) & 1)

        # RTR
        bits.append(1 if frame.is_remote else 0)

        # r1, r0 (reserved, dominant)
        bits.extend([0, 0])
    else:
        # Standard frame: 11-bit ID
        for i in range(11):
            bits.append((frame.arbitration_id >> (10 - i)) & 1)

        # RTR
        bits.append(1 if frame.is_remote else 0)

        # IDE (dominant for standard)
        bits.append(0)

        # r0 (reserved, dominant)
        bits.append(0)

    # DLC (4 bits)
    for i in range(4):
        bits.append((frame.dlc >> (3 - i)) & 1)

    # Data field
    if not frame.is_remote:
        for byte in frame.data[: frame.dlc]:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)

    # CRC (simplified - just use placeholder)
    crc = _calculate_can_crc(bits)
    for i in range(15):
        bits.append((crc >> (14 - i)) & 1)

    # CRC delimiter (recessive)
    bits.append(1)

    # ACK slot (dominant - assuming acknowledged)
    bits.append(0)

    # ACK delimiter (recessive)
    bits.append(1)

    # EOF (7 recessive bits)
    bits.extend([1] * 7)

    # Add bit stuffing (simplified)
    stuffed_bits = _apply_bit_stuffing(bits)

    # Convert to samples
    signal = np.zeros(len(stuffed_bits) * samples_per_bit, dtype=bool)

    for i, bit in enumerate(stuffed_bits):
        start = i * samples_per_bit
        end = start + samples_per_bit
        signal[start:end] = bit  # 1 = recessive (True), 0 = dominant (False)

    # Add some idle before and after
    idle = np.ones(samples_per_bit * 10, dtype=bool)
    signal = np.concatenate([idle, signal, idle])

    return signal


def _calculate_can_crc(bits: list[int]) -> int:
    """Calculate CAN CRC-15."""
    crc = 0
    poly = 0x4599

    for bit in bits:
        crc_next = (crc >> 14) & 1
        crc = (crc << 1) & 0x7FFF

        if bit ^ crc_next:
            crc ^= poly

    return crc


def _apply_bit_stuffing(bits: list[int]) -> list[int]:
    """Apply CAN bit stuffing (insert opposite bit after 5 same bits)."""
    stuffed = []
    consecutive = 0
    last_bit = None

    # Only stuff up to CRC delimiter (not ACK, ACK delimiter, EOF)
    stuff_region_end = len(bits) - 10  # Approximate

    for i, bit in enumerate(bits):
        stuffed.append(bit)

        if i < stuff_region_end:
            if last_bit is not None and bit == last_bit:
                consecutive += 1
                if consecutive >= 5:
                    # Insert stuff bit (opposite)
                    stuffed.append(1 - bit)
                    consecutive = 1
                    last_bit = 1 - bit
                    continue
            else:
                consecutive = 1

        last_bit = bit

    return stuffed


if __name__ == "__main__":
    main()
