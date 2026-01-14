"""CAN Bus Reverse Engineering Example.

This example demonstrates the complete workflow for reverse engineering
a CAN bus protocol using TraceKit's automotive module.

Workflow:
1. Load CAN messages from log file
2. Generate message inventory
3. Analyze specific messages
4. Test hypotheses about signal encoding
5. Document discoveries
6. Export to DBC format
"""

from pathlib import Path

from tracekit.automotive.can.discovery import (
    DiscoveryDocument,
    MessageDiscovery,
    SignalDiscovery,
)

# This example uses synthetic data for demonstration
from tracekit.automotive.can.models import CANMessage, CANMessageList
from tracekit.automotive.can.session import CANSession
from tracekit.automotive.dbc.generator import DBCGenerator


def generate_synthetic_data() -> CANMessageList:
    """Generate synthetic CAN messages for demonstration."""
    import struct

    messages = CANMessageList()

    # Simulate engine RPM message (0x280)
    # Bytes 2-3 contain RPM as big-endian uint16 with scale 0.25
    for i in range(100):
        timestamp = i * 0.01
        rpm = 800 + (i * 12)  # RPM from 800 to 2000

        raw_rpm = int(rpm / 0.25)
        data = bytearray(8)
        data[0] = 0xAA  # Constant
        data[1] = 0xBB  # Constant
        data[2:4] = struct.pack(">H", raw_rpm)  # RPM
        data[4] = i % 256  # Counter
        data[5:8] = b"\xcc\xdd\xee"  # Constants

        messages.append(
            CANMessage(
                arbitration_id=0x280,
                timestamp=timestamp,
                data=bytes(data),
            )
        )

    # Simulate vehicle speed message (0x300)
    for i in range(50):
        timestamp = i * 0.02
        speed_kmh = 50 + (i * 0.5)

        data = bytearray(8)
        data[0] = int(speed_kmh * 100) >> 8  # Speed high byte
        data[1] = int(speed_kmh * 100) & 0xFF  # Speed low byte
        data[2:8] = b"\x00\x00\x00\x00\x00\x00"

        messages.append(
            CANMessage(
                arbitration_id=0x300,
                timestamp=timestamp,
                data=bytes(data),
            )
        )

    return messages


def main():
    """Run CAN reverse engineering example."""
    print("=" * 70)
    print("TraceKit CAN Bus Reverse Engineering Example")
    print("=" * 70)
    print()

    # Step 1: Load CAN messages
    print("Step 1: Loading CAN messages...")
    # In real use: session = CANSession.from_log("capture.blf")
    messages = generate_synthetic_data()
    session = CANSession(messages=messages)
    print(f"  Loaded {len(session)} messages")
    print(f"  Found {len(session.unique_ids())} unique CAN IDs")
    print()

    # Step 2: Generate inventory
    print("Step 2: Message Inventory")
    print("-" * 70)
    inventory = session.inventory()
    print(inventory.to_string(index=False))
    print()

    # Step 3: Analyze specific message (0x280)
    print("Step 3: Analyzing Message 0x280 (Engine Data)")
    print("-" * 70)
    msg_280 = session.message(0x280)
    analysis = msg_280.analyze()
    print(analysis.summary())
    print()

    # Step 4: Test hypothesis about RPM signal
    print("Step 4: Testing Hypothesis - RPM Signal")
    print("-" * 70)
    print("  Hypothesis: Bytes 2-3 contain engine RPM")
    print("  Encoding: Big-endian uint16, scale=0.25, unit=rpm")
    print()

    hypothesis = msg_280.test_hypothesis(
        signal_name="engine_rpm",
        start_byte=2,
        bit_length=16,
        byte_order="big_endian",
        scale=0.25,
        unit="rpm",
        expected_min=0,
        expected_max=8000,
    )

    print(hypothesis.summary())
    print()

    # Step 5: Document confirmed signals
    if hypothesis.is_valid:
        print("Step 5: Documenting Confirmed Signal")
        print("-" * 70)
        msg_280.document_signal(
            name="engine_rpm",
            start_bit=16,
            length=16,
            byte_order="big_endian",
            scale=0.25,
            unit="rpm",
            comment="Engine RPM - confirmed via statistical analysis",
        )
        print("  Signal 'engine_rpm' documented")
        print()

    # Step 6: Analyze second message (0x300)
    print("Step 6: Analyzing Message 0x300 (Vehicle Speed)")
    print("-" * 70)
    msg_300 = session.message(0x300)
    analysis_300 = msg_300.analyze()
    print(f"  Message count: {analysis_300.message_count}")
    print(f"  Frequency: {analysis_300.frequency_hz:.1f} Hz")
    print()

    # Test speed hypothesis
    msg_300.document_signal(
        name="vehicle_speed",
        start_bit=0,
        length=16,
        byte_order="big_endian",
        scale=0.01,
        unit="km/h",
        comment="Vehicle speed",
    )
    print("  Signal 'vehicle_speed' documented")
    print()

    # Step 7: Create discovery document
    print("Step 7: Creating Discovery Document")
    print("-" * 70)
    doc = DiscoveryDocument()
    doc.vehicle.make = "Unknown"
    doc.vehicle.model = "Test Vehicle"

    # Add message 0x280
    msg_disc_280 = MessageDiscovery(
        id=0x280,
        name="Engine_Status",
        length=8,
        cycle_time_ms=10.0,
        confidence=0.95,
        evidence=["Periodic at 100 Hz", "RPM signal validated"],
        signals=[
            SignalDiscovery(
                name="engine_rpm",
                start_bit=16,
                length=16,
                scale=0.25,
                unit="rpm",
                confidence=0.95,
                evidence=["Statistical analysis", "Value range matches expectations"],
            )
        ],
    )
    doc.add_message(msg_disc_280)

    # Save discovery document
    doc_path = Path("can_discoveries.tkcan")
    doc.save(doc_path)
    print(f"  Saved discovery document to {doc_path}")
    print()

    # Step 8: Export to DBC
    print("Step 8: Exporting to DBC Format")
    print("-" * 70)
    dbc_path = Path("discovered_signals.dbc")
    DBCGenerator.generate(doc, dbc_path, min_confidence=0.8)
    print(f"  Generated DBC file: {dbc_path}")
    print()

    # Show DBC content
    with open(dbc_path) as f:
        dbc_content = f.read()
    print("  DBC Content Preview:")
    print("  " + "\n  ".join(dbc_content.split("\n")[:15]))
    print()

    print("=" * 70)
    print("Reverse Engineering Complete!")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  - Analyzed {len(session)} CAN messages")
    print(f"  - Discovered {len(session.unique_ids())} unique message IDs")
    print("  - Documented 2 signals (engine_rpm, vehicle_speed)")
    print(f"  - Saved discoveries to {doc_path}")
    print(f"  - Generated standard DBC file: {dbc_path}")
    print()


if __name__ == "__main__":
    main()
