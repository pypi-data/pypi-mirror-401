"""Example: UDS (Unified Diagnostic Services) protocol decoding.

This example demonstrates how to use TraceKit's UDS decoder to analyze
diagnostic messages from automotive ECUs per ISO 14229.

UDS is the primary diagnostic protocol in modern vehicles for:
- ECU programming and flashing
- Security access and authentication
- Diagnostic Trouble Code (DTC) management
- Memory read/write operations
- Routine control and testing
"""

from __future__ import annotations

from tracekit.automotive.can.models import CANMessage
from tracekit.automotive.uds import UDSDecoder


def main() -> None:
    """Demonstrate UDS protocol decoding."""
    print("=== UDS (ISO 14229) Diagnostic Services Decoder Demo ===\n")

    # Example 1: Diagnostic Session Control (0x10)
    print("1. Diagnostic Session Control")
    print("-" * 50)

    # Request: Switch to programming session
    request = bytes([0x02, 0x10, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00])
    msg = CANMessage(arbitration_id=0x7DF, timestamp=1.0, data=request)
    service = UDSDecoder.decode_service(msg)
    print(f"Request:  {service}")

    # Positive response
    response = bytes([0x02, 0x50, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00])
    msg = CANMessage(arbitration_id=0x7E8, timestamp=1.1, data=response)
    service = UDSDecoder.decode_service(msg)
    print(f"Response: {service}")
    print()


def demonstrate_security_access():
    """Demonstrate SecurityAccess service (0x27)."""
    print("=== Security Access Sequence ===")

    # Request seed (sub-function 0x01)
    msg = CANMessage(
        arbitration_id=0x7E0,
        timestamp=1.0,
        data=bytes([0x02, 0x27, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]),
    )
    print(f"Request: {UDSDecoder.decode_service(msg)}")

    # Positive response with seed
    msg = CANMessage(
        arbitration_id=0x7E8,
        timestamp=1.1,
        data=bytes([0x06, 0x67, 0x01, 0x12, 0x34, 0x56, 0x78, 0x00]),
    )
    result = UDSDecoder.decode_service(msg)
    print(f"Response: {result}")
    print(f"Seed data: {result.data.hex().upper()}")


if __name__ == "__main__":
    main()
