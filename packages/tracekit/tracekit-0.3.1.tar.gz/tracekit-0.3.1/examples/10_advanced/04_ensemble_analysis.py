#!/usr/bin/env python3
"""Example: Enhanced field boundary detection using voting expert and ensemble methods.

This example demonstrates the new voting expert and ensemble inference capabilities
for improved message format detection.

Requirements addressed: Enhanced field detection (PSI-001)

References:
    IPART: IP Packet Analysis using Random Forests. IEEE ISSRE 2014.
    Discoverer: Automatic Protocol Reverse Engineering. USENIX Security 2007.
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

import numpy as np

from tracekit.inference import MessageFormatInferrer


def create_sample_protocol_messages(num_messages: int = 50) -> list[bytes]:
    """Create sample protocol messages with known structure.

    Structure:
    - 2 bytes: Magic header (0xAA55)
    - 2 bytes: Counter (0-65535)
    - 1 byte: Length
    - N bytes: Payload
    - 1 byte: XOR checksum

    Args:
        num_messages: Number of messages to generate

    Returns:
        List of protocol messages
    """
    rng = np.random.RandomState(42)
    messages = []

    for i in range(num_messages):
        payload_len = 8
        msg = bytearray([0xAA, 0x55])  # Magic header
        msg.extend(i.to_bytes(2, "big"))  # Counter
        msg.append(payload_len)  # Length
        msg.extend(rng.randint(0, 256, payload_len, dtype=np.uint8).tobytes())  # Payload

        # XOR checksum
        xor_sum = 0
        for b in msg:
            xor_sum ^= b
        msg.append(xor_sum)

        messages.append(bytes(msg))

    return messages


def main() -> None:
    """Demonstrate ensemble inference with voting experts."""
    print("=" * 70)
    print("Enhanced Field Boundary Detection - Voting Expert Ensemble")
    print("=" * 70)
    print()

    # Create sample messages
    print("Step 1: Generating sample protocol messages...")
    messages = create_sample_protocol_messages(num_messages=50)
    print(f"  Generated {len(messages)} messages")
    print(f"  Message size: {len(messages[0])} bytes")
    print()

    # Initialize inferrer
    inferrer = MessageFormatInferrer(min_samples=10)

    # Run basic inference (for comparison)
    print("Step 2: Running basic inference...")
    basic_schema = inferrer.infer_format(messages)
    print(f"  Detected {len(basic_schema.fields)} fields")
    print(f"  Boundaries: {basic_schema.field_boundaries}")
    print()

    # Run ensemble inference with voting experts
    print("Step 3: Running ensemble inference with voting experts...")
    ensemble_schema = inferrer.infer_format_ensemble(
        messages,
        min_field_confidence=0.5,
        min_boundary_confidence=0.6,
    )
    print(f"  Detected {len(ensemble_schema.fields)} fields")
    print(f"  Boundaries: {ensemble_schema.field_boundaries}")
    print()

    # Display detected fields
    print("Step 4: Analyzing detected fields...")
    print()
    print("Field Details (Ensemble Method):")
    print("-" * 70)

    for field in ensemble_schema.fields:
        print(f"\n{field.name}:")
        print(f"  Offset: {field.offset} bytes")
        print(f"  Size: {field.size} bytes")
        print(f"  Type: {field.field_type}")
        print(f"  Confidence: {field.confidence:.2%}")
        print(f"  Entropy: {field.entropy:.2f} bits")
        print(f"  Variance: {field.variance:.2f}")

        # Show evidence from experts
        if field.evidence:
            print("  Expert Evidence:")
            for expert, voted in field.evidence.items():
                if voted:
                    print(f"    - {expert}")

        # Show sample values
        if field.values_seen:
            print(f"  Sample values: {field.values_seen[:3]}")

    print()
    print("=" * 70)
    print("Analysis Complete")
    print("=" * 70)
    print()
    print("Key Observations:")
    print("  - Voting expert combines 5 detection strategies:")
    print("    1. Entropy-based detection")
    print("    2. Alignment-based detection (Smith-Waterman)")
    print("    3. Statistical variance detection")
    print("    4. Byte value distribution analysis")
    print("    5. N-gram frequency analysis")
    print()
    print("  - Ensemble method provides confidence scores for each field")
    print("  - Evidence tracking shows which experts voted for each field")
    print()


if __name__ == "__main__":
    main()
