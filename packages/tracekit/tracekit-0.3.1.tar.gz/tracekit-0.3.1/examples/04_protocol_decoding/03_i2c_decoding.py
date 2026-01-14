#!/usr/bin/env python3
"""Example 03: I2C Protocol Decoding.

This example demonstrates I2C (Inter-Integrated Circuit) protocol
decoding including address detection, ACK/NAK analysis, and
multi-device communication.

Time: 20 minutes
Prerequisites: Digital signal concepts

Run:
    uv run python examples/04_protocol_decoding/03_i2c_decoding.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import numpy as np

from tracekit.analyzers.protocols.i2c import I2CDecoder, decode_i2c


def main() -> None:
    """Demonstrate I2C decoding capabilities."""
    print("=" * 60)
    print("TraceKit Example: I2C Protocol Decoding")
    print("=" * 60)

    # --- Basic I2C Decoding ---
    print("\n--- Basic I2C Decoding ---")

    demo_basic_i2c()

    # --- Multi-Byte Transactions ---
    print("\n--- Multi-Byte I2C Transactions ---")

    demo_multi_byte()

    # --- Read vs Write Operations ---
    print("\n--- I2C Read/Write Operations ---")

    demo_read_write()

    # --- Multi-Device Bus ---
    print("\n--- Multi-Device I2C Bus ---")

    demo_multi_device()

    # --- Error Detection ---
    print("\n--- I2C Error Detection ---")

    demo_error_detection()

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. I2C uses SDA (data) and SCL (clock) lines")
    print("  2. START: SDA falls while SCL high")
    print("  3. STOP: SDA rises while SCL high")
    print("  4. Address byte: 7-bit address + R/W bit")
    print("  5. ACK (low) = acknowledged, NAK (high) = not acknowledged")
    print("=" * 60)


def demo_basic_i2c() -> None:
    """Demonstrate basic I2C signal decoding."""
    sample_rate = 10e6  # 10 MHz (plenty for 400 kHz I2C)

    # Generate simple I2C write transaction
    # Write 0x42 to device at address 0x50
    address = 0x50
    data_byte = 0x42

    scl, sda = generate_i2c_write(
        address=address,
        data=[data_byte],
        sample_rate=sample_rate,
        clock_freq=400e3,
    )

    print("I2C Write Transaction:")
    print(f"  Device address: 0x{address:02X}")
    print(f"  Data: 0x{data_byte:02X}")
    print(f"  Sample rate: {sample_rate / 1e6:.0f} MHz")

    # Decode
    packets = decode_i2c(scl, sda, sample_rate=sample_rate)

    print(f"\nDecoded {len(packets)} transaction(s):")
    for i, pkt in enumerate(packets):
        addr = pkt.annotations["address"]
        is_read = pkt.annotations["read"]
        print(f"  [{i}] Address: 0x{addr:02X} {'Read' if is_read else 'Write'}")
        print(f"      Data: {pkt.data.hex()}")
        if pkt.errors:
            print(f"      Errors: {pkt.errors}")


def demo_multi_byte() -> None:
    """Demonstrate multi-byte I2C transactions."""
    sample_rate = 10e6
    address = 0x68  # Typical RTC address

    # Write multiple bytes (e.g., setting time registers)
    data_bytes = [0x00, 0x30, 0x15, 0x06, 0x25, 0x12, 0x24]  # Register + time data

    scl, sda = generate_i2c_write(
        address=address,
        data=data_bytes,
        sample_rate=sample_rate,
        clock_freq=100e3,  # Standard mode
    )

    print(f"Multi-byte write to RTC (0x{address:02X}):")
    print(f"  Data bytes: {[f'0x{b:02X}' for b in data_bytes]}")

    packets = decode_i2c(scl, sda, sample_rate=sample_rate)

    for pkt in packets:
        print("\nDecoded transaction:")
        print(f"  Address: 0x{pkt.annotations['address']:02X}")
        print(f"  Direction: {'Read' if pkt.annotations['read'] else 'Write'}")
        print(f"  Data ({len(pkt.data)} bytes): {pkt.data.hex()}")

        # Parse as register write
        if len(pkt.data) > 0:
            print(f"  Register address: 0x{pkt.data[0]:02X}")
            if len(pkt.data) > 1:
                print(f"  Register values: {[f'0x{b:02X}' for b in pkt.data[1:]]}")


def demo_read_write() -> None:
    """Demonstrate I2C read and write operations."""
    sample_rate = 10e6
    address = 0x50  # EEPROM address

    print("I2C Read/Write Operations:")
    print("-" * 40)

    # Write operation
    write_data = [0x00, 0x10, 0xAB, 0xCD]  # Address + data
    scl_w, sda_w = generate_i2c_write(
        address=address,
        data=write_data,
        sample_rate=sample_rate,
        clock_freq=400e3,
    )

    packets_w = decode_i2c(scl_w, sda_w, sample_rate=sample_rate)

    print(f"\n1. Write operation to 0x{address:02X}:")
    for pkt in packets_w:
        print(f"   Direction: {'Read' if pkt.annotations['read'] else 'Write'}")
        print(f"   Data: {pkt.data.hex()}")

    # Read operation
    scl_r, sda_r = generate_i2c_read(
        address=address,
        num_bytes=4,
        read_data=[0xDE, 0xAD, 0xBE, 0xEF],  # Simulated device response
        sample_rate=sample_rate,
        clock_freq=400e3,
    )

    packets_r = decode_i2c(scl_r, sda_r, sample_rate=sample_rate)

    print(f"\n2. Read operation from 0x{address:02X}:")
    for pkt in packets_r:
        print(f"   Direction: {'Read' if pkt.annotations['read'] else 'Write'}")
        print(f"   Data: {pkt.data.hex()}")


def demo_multi_device() -> None:
    """Demonstrate multi-device I2C bus communication."""
    sample_rate = 10e6
    clock_freq = 100e3

    # Simulate communication with multiple devices
    devices = [
        {"address": 0x50, "name": "EEPROM", "data": [0x00, 0x10]},
        {"address": 0x68, "name": "RTC", "data": [0x00]},
        {"address": 0x76, "name": "Sensor", "data": [0xF7]},
    ]

    print("Multi-device I2C bus:")
    print("-" * 40)

    all_scl = []
    all_sda = []
    idle_samples = int(sample_rate * 10e-6)  # 10us between transactions

    for dev in devices:
        scl, sda = generate_i2c_write(
            address=dev["address"],
            data=dev["data"],
            sample_rate=sample_rate,
            clock_freq=clock_freq,
        )
        all_scl.extend(scl.tolist())
        all_sda.extend(sda.tolist())

        # Add idle time between transactions
        all_scl.extend([1] * idle_samples)  # SCL high
        all_sda.extend([1] * idle_samples)  # SDA high

    scl_combined = np.array(all_scl, dtype=bool)
    sda_combined = np.array(all_sda, dtype=bool)

    packets = decode_i2c(scl_combined, sda_combined, sample_rate=sample_rate)

    print(f"\nDecoded {len(packets)} transactions:")
    for i, pkt in enumerate(packets):
        addr = pkt.annotations["address"]

        # Find device name
        dev_name = "Unknown"
        for dev in devices:
            if dev["address"] == addr:
                dev_name = dev["name"]
                break

        print(f"\n  Transaction {i + 1}: {dev_name}")
        print(f"    Address: 0x{addr:02X}")
        print(f"    Direction: {'Read' if pkt.annotations['read'] else 'Write'}")
        print(f"    Data: {pkt.data.hex()}")
        print(f"    Time: {pkt.timestamp * 1e6:.1f} us")


def demo_error_detection() -> None:
    """Demonstrate I2C error detection."""
    sample_rate = 10e6

    print("I2C Error Detection:")
    print("-" * 40)

    # Generate transaction with NAK (device not responding)
    address = 0x55  # Non-existent device
    scl, sda = generate_i2c_write(
        address=address,
        data=[0x00],
        sample_rate=sample_rate,
        clock_freq=400e3,
        simulate_nak=True,  # Device doesn't ACK
    )

    packets = decode_i2c(scl, sda, sample_rate=sample_rate)

    print("\n1. NAK on address (device not present):")
    print(f"   Target address: 0x{address:02X}")
    for pkt in packets:
        print(f"   ACKs received: {pkt.annotations.get('acks', [])}")
        if pkt.errors:
            print(f"   Errors: {pkt.errors}")
        else:
            print("   No errors detected (device responded)")

    # Using I2CDecoder class for more control
    print("\n2. Using I2CDecoder class:")
    decoder = I2CDecoder(address_format="auto")

    for pkt in decoder.decode(scl=scl, sda=sda, sample_rate=sample_rate):
        print(f"   Address: 0x{pkt.annotations['address']:02X}")
        print(f"   10-bit addressing: {pkt.annotations.get('address_10bit', False)}")
        print(f"   Transaction #: {pkt.annotations.get('transaction_num', 0)}")


# --- Signal Generation Helpers ---


def generate_i2c_write(
    address: int,
    data: list[int],
    sample_rate: float,
    clock_freq: float,
    simulate_nak: bool = False,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate I2C write transaction signals.

    Args:
        address: 7-bit device address
        data: List of data bytes to write
        sample_rate: Sample rate in Hz
        clock_freq: I2C clock frequency in Hz
        simulate_nak: If True, simulate NAK on address

    Returns:
        Tuple of (SCL, SDA) boolean arrays
    """
    # Calculate timing
    bit_samples = int(sample_rate / clock_freq)
    half_bit = bit_samples // 2

    # Build transaction
    scl_list = []
    sda_list = []

    # Start with idle (both high)
    idle_samples = bit_samples * 2
    scl_list.extend([1] * idle_samples)
    sda_list.extend([1] * idle_samples)

    # START condition: SDA falls while SCL high
    scl_list.extend([1] * half_bit)
    sda_list.extend([0] * half_bit)

    # Address byte (7-bit address + W bit = 0)
    address_byte = (address << 1) | 0  # Write

    # Send address byte
    _add_byte_to_signals(scl_list, sda_list, address_byte, bit_samples)

    # ACK bit (from slave)
    ack_value = 1 if simulate_nak else 0  # NAK=1, ACK=0
    _add_ack_bit(scl_list, sda_list, ack_value, bit_samples)

    # Data bytes
    for byte in data:
        _add_byte_to_signals(scl_list, sda_list, byte, bit_samples)
        _add_ack_bit(scl_list, sda_list, 0, bit_samples)  # ACK each byte

    # STOP condition: SDA rises while SCL high
    scl_list.extend([1] * half_bit)
    sda_list.extend([0] * half_bit)
    scl_list.extend([1] * half_bit)
    sda_list.extend([1] * half_bit)

    # Return to idle
    scl_list.extend([1] * idle_samples)
    sda_list.extend([1] * idle_samples)

    return np.array(scl_list, dtype=bool), np.array(sda_list, dtype=bool)


def generate_i2c_read(
    address: int,
    num_bytes: int,
    read_data: list[int],
    sample_rate: float,
    clock_freq: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate I2C read transaction signals.

    Args:
        address: 7-bit device address
        num_bytes: Number of bytes to read
        read_data: Data that the slave will send
        sample_rate: Sample rate in Hz
        clock_freq: I2C clock frequency in Hz

    Returns:
        Tuple of (SCL, SDA) boolean arrays
    """
    bit_samples = int(sample_rate / clock_freq)
    half_bit = bit_samples // 2

    scl_list = []
    sda_list = []

    # Idle
    idle_samples = bit_samples * 2
    scl_list.extend([1] * idle_samples)
    sda_list.extend([1] * idle_samples)

    # START
    scl_list.extend([1] * half_bit)
    sda_list.extend([0] * half_bit)

    # Address byte with R bit = 1
    address_byte = (address << 1) | 1  # Read
    _add_byte_to_signals(scl_list, sda_list, address_byte, bit_samples)
    _add_ack_bit(scl_list, sda_list, 0, bit_samples)  # Slave ACKs

    # Read data bytes (slave drives SDA)
    for i, byte in enumerate(read_data[:num_bytes]):
        _add_byte_to_signals(scl_list, sda_list, byte, bit_samples)

        # Master ACKs all bytes except last
        if i < num_bytes - 1:
            _add_ack_bit(scl_list, sda_list, 0, bit_samples)  # ACK
        else:
            _add_ack_bit(scl_list, sda_list, 1, bit_samples)  # NAK on last byte

    # STOP
    scl_list.extend([1] * half_bit)
    sda_list.extend([0] * half_bit)
    scl_list.extend([1] * half_bit)
    sda_list.extend([1] * half_bit)

    # Idle
    scl_list.extend([1] * idle_samples)
    sda_list.extend([1] * idle_samples)

    return np.array(scl_list, dtype=bool), np.array(sda_list, dtype=bool)


def _add_byte_to_signals(
    scl_list: list[int],
    sda_list: list[int],
    byte: int,
    bit_samples: int,
) -> None:
    """Add a byte (8 bits, MSB first) to I2C signals."""
    half_bit = bit_samples // 2

    for bit_idx in range(8):
        bit_value = (byte >> (7 - bit_idx)) & 1

        # SCL low, set SDA
        scl_list.extend([0] * half_bit)
        sda_list.extend([bit_value] * half_bit)

        # SCL high, hold SDA (sample point)
        scl_list.extend([1] * half_bit)
        sda_list.extend([bit_value] * half_bit)


def _add_ack_bit(
    scl_list: list[int],
    sda_list: list[int],
    ack_value: int,
    bit_samples: int,
) -> None:
    """Add ACK/NAK bit to I2C signals."""
    half_bit = bit_samples // 2

    # SCL low, slave drives SDA
    scl_list.extend([0] * half_bit)
    sda_list.extend([ack_value] * half_bit)

    # SCL high (sample ACK)
    scl_list.extend([1] * half_bit)
    sda_list.extend([ack_value] * half_bit)


if __name__ == "__main__":
    main()
