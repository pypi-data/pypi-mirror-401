"""Example: Generate Wireshark dissectors from protocol definitions.

This example demonstrates how to export TraceKit protocol definitions as
Wireshark Lua dissectors for integration with Wireshark's protocol analysis.

The generated dissectors can be loaded into Wireshark to decode and analyze
custom protocols interactively.
"""

from pathlib import Path

from tracekit.export.wireshark import WiresharkDissectorGenerator
from tracekit.inference.protocol_dsl import FieldDefinition, ProtocolDefinition


def create_simple_protocol() -> ProtocolDefinition:
    """Create a simple protocol definition.

    Returns:
        Simple protocol with basic fields
    """
    return ProtocolDefinition(
        name="simple",
        description="Simple Test Protocol",
        version="1.0",
        settings={"transport": "tcp", "port": 8000},
        fields=[
            FieldDefinition(
                name="msg_type",
                field_type="uint8",
                size=1,
                description="Message Type",
                enum={0x01: "REQUEST", 0x02: "RESPONSE", 0x03: "ERROR"},
            ),
            FieldDefinition(
                name="sequence",
                field_type="uint16",
                size=2,
                description="Sequence Number",
            ),
            FieldDefinition(
                name="length",
                field_type="uint16",
                size=2,
                description="Payload Length",
            ),
            FieldDefinition(
                name="payload",
                field_type="bytes",
                size="length",
                description="Message Payload",
            ),
            FieldDefinition(
                name="checksum",
                field_type="uint32",
                size=4,
                description="CRC32 Checksum",
            ),
        ],
    )


def create_modbus_like_protocol() -> ProtocolDefinition:
    """Create a Modbus-like protocol definition.

    Returns:
        Modbus-like protocol definition
    """
    return ProtocolDefinition(
        name="modbus",
        description="Modbus Protocol",
        version="1.0",
        settings={"transport": "tcp", "port": 502},
        fields=[
            FieldDefinition(
                name="transaction_id",
                field_type="uint16",
                size=2,
                description="Transaction Identifier",
            ),
            FieldDefinition(
                name="protocol_id",
                field_type="uint16",
                size=2,
                description="Protocol Identifier",
                value=0,  # Always 0 for Modbus
            ),
            FieldDefinition(
                name="length",
                field_type="uint16",
                size=2,
                description="Length of following bytes",
            ),
            FieldDefinition(
                name="unit_id",
                field_type="uint8",
                size=1,
                description="Unit Identifier",
            ),
            FieldDefinition(
                name="function_code",
                field_type="uint8",
                size=1,
                description="Function Code",
                enum={
                    0x01: "Read Coils",
                    0x02: "Read Discrete Inputs",
                    0x03: "Read Holding Registers",
                    0x04: "Read Input Registers",
                    0x05: "Write Single Coil",
                    0x06: "Write Single Register",
                    0x0F: "Write Multiple Coils",
                    0x10: "Write Multiple Registers",
                },
            ),
            FieldDefinition(
                name="data",
                field_type="bytes",
                size="remaining",
                description="Function-specific data",
            ),
        ],
    )


def create_custom_protocol() -> ProtocolDefinition:
    """Create a custom protocol with various field types.

    Returns:
        Custom protocol demonstrating different features
    """
    return ProtocolDefinition(
        name="custom",
        description="Custom Protocol Example",
        version="2.0",
        endian="little",
        settings={"transport": "udp", "port": 5000},
        fields=[
            FieldDefinition(
                name="magic",
                field_type="uint32",
                size=4,
                description="Magic Number",
                value=0xDEADBEEF,
            ),
            FieldDefinition(
                name="version",
                field_type="uint8",
                size=1,
                description="Protocol Version",
            ),
            FieldDefinition(
                name="flags",
                field_type="uint8",
                size=1,
                description="Control Flags",
            ),
            FieldDefinition(
                name="timestamp",
                field_type="uint64",
                size=8,
                description="Unix Timestamp (microseconds)",
            ),
            FieldDefinition(
                name="sensor_count",
                field_type="uint16",
                size=2,
                description="Number of Sensor Readings",
            ),
            FieldDefinition(
                name="temperature",
                field_type="float32",
                size=4,
                description="Temperature (Celsius)",
            ),
            FieldDefinition(
                name="humidity",
                field_type="float32",
                size=4,
                description="Relative Humidity (%)",
            ),
            FieldDefinition(
                name="device_name",
                field_type="string",
                size=32,
                description="Device Name (null-terminated)",
            ),
        ],
    )


def generate_dissectors(output_dir: Path) -> None:
    """Generate Wireshark dissectors for example protocols.

    Args:
        output_dir: Directory to write dissector files
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create generator (disable validation for example)
    generator = WiresharkDissectorGenerator(validate=False)

    # Generate dissectors for each protocol
    protocols = [
        ("simple.lua", create_simple_protocol()),
        ("modbus.lua", create_modbus_like_protocol()),
        ("custom.lua", create_custom_protocol()),
    ]

    for filename, protocol in protocols:
        output_path = output_dir / filename
        print(f"Generating {filename}...")
        generator.generate(protocol, output_path)
        print(f"  Written to: {output_path}")
        print(f"  Protocol: {protocol.description}")
        print(f"  Fields: {len(protocol.fields)}")
        print()


def show_installation_instructions() -> None:
    """Show instructions for installing dissectors in Wireshark."""
    print("=" * 70)
    print("INSTALLATION INSTRUCTIONS")
    print("=" * 70)
    print()
    print("To use these dissectors in Wireshark:")
    print()
    print("1. Copy the .lua files to your Wireshark plugins directory:")
    print()
    print("   Linux:")
    print("     ~/.local/lib/wireshark/plugins/")
    print("     or")
    print("     ~/.config/wireshark/plugins/")
    print()
    print("   macOS:")
    print("     ~/.config/wireshark/plugins/")
    print()
    print("   Windows:")
    print("     %APPDATA%\\Wireshark\\plugins\\")
    print()
    print("2. Restart Wireshark or reload Lua plugins:")
    print("     Analyze > Reload Lua Plugins (Ctrl+Shift+L)")
    print()
    print("3. The dissectors will automatically decode packets on their")
    print("   configured ports (e.g., TCP port 8000 for 'simple' protocol)")
    print()
    print("4. You can also manually decode packets:")
    print("     Right-click packet > Decode As > select protocol")
    print()
    print("=" * 70)


def main() -> None:
    """Run the example."""
    print("Wireshark Dissector Generation Example")
    print("=" * 70)
    print()

    # Generate dissectors to current directory
    output_dir = Path("generated_dissectors")
    generate_dissectors(output_dir)

    print("Generation complete!")
    print()
    show_installation_instructions()


if __name__ == "__main__":
    main()
