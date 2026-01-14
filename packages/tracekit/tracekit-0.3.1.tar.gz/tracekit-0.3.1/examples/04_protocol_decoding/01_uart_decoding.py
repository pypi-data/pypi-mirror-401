#!/usr/bin/env python3
"""Example: UART Protocol Decoding.

This example demonstrates decoding UART (RS-232) serial
communication from captured waveforms.

Time: 15 minutes
Prerequisites: Digital signal concepts

Run:
    uv run python examples/04_protocol_decoding/01_uart_decoding.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

from tracekit.protocols import UARTDecoder

from tracekit.inference import detect_baud_rate
from tracekit.testing import generate_uart_signal


def main() -> None:
    """Demonstrate UART decoding."""
    print("=" * 60)
    print("TraceKit Example: UART Protocol Decoding")
    print("=" * 60)

    # --- Generate Test UART Signal ---
    print("\n--- Generating Test UART Signal ---")

    test_message = b"Hello, TraceKit!\r\n"
    baud_rate = 115200

    uart_trace = generate_uart_signal(
        baud_rate=baud_rate,
        data=test_message,
        sample_rate=10e6,  # 10 MSa/s (plenty for 115200 baud)
        data_bits=8,
        parity="none",
        stop_bits=1,
    )

    print("Generated UART signal:")
    print(f"  Baud rate: {baud_rate}")
    print(f"  Message: {test_message}")
    print(f"  Samples: {len(uart_trace.data)}")
    print(f"  Duration: {uart_trace.duration * 1e3:.2f} ms")

    # --- Basic UART Decoding ---
    print("\n--- Basic UART Decoding ---")

    decoder = UARTDecoder(baud_rate=baud_rate)
    messages = decoder.decode(uart_trace)

    print(f"Decoded {len(messages)} byte(s)")
    print("\nDecoded data:")
    decoded_bytes = bytes(msg.data[0] for msg in messages)
    print(f"  Raw bytes: {decoded_bytes}")
    try:
        print(f"  As text: {decoded_bytes.decode('utf-8')!r}")
    except UnicodeDecodeError:
        print("  (Not valid UTF-8)")

    # --- Timing Information ---
    print("\n--- Timing Information ---")
    print("\nFirst 5 bytes with timing:")
    for i, msg in enumerate(messages[:5]):
        print(
            f"  Byte {i + 1}: 0x{msg.data[0]:02X} ('{chr(msg.data[0])}') at {msg.time * 1e3:.3f} ms"
        )

    # --- Baud Rate Detection ---
    print("\n--- Automatic Baud Rate Detection ---")

    # Generate signal with "unknown" baud rate
    mystery_signal = generate_uart_signal(
        baud_rate=19200,  # Different baud rate
        data=b"Mystery",
        sample_rate=1e6,
    )

    detected_baud = detect_baud_rate(mystery_signal)
    print("Unknown signal baud rate detection:")
    print(f"  Detected: {detected_baud}")
    print("  Actual: 19200")

    # Decode with detected rate
    decoder2 = UARTDecoder(baud_rate=detected_baud)
    messages2 = decoder2.decode(mystery_signal)
    decoded2 = bytes(msg.data[0] for msg in messages2)
    print(f"  Decoded message: {decoded2.decode('utf-8', errors='replace')!r}")

    # --- Different UART Configurations ---
    print("\n--- UART Configuration Options ---")

    print("\nCommon baud rates: 9600, 19200, 38400, 57600, 115200, 230400")

    print("\nConfiguration examples:")
    print("  Standard 8N1:")
    print('    UARTDecoder(baud_rate=115200, data_bits=8, parity="none", stop_bits=1)')
    print("\n  With even parity:")
    print('    UARTDecoder(baud_rate=9600, data_bits=8, parity="even", stop_bits=1)')
    print("\n  7 data bits, odd parity:")
    print('    UARTDecoder(baud_rate=9600, data_bits=7, parity="odd", stop_bits=2)')
    print("\n  Inverted logic (RS-232):")
    print("    UARTDecoder(baud_rate=115200, inverted=True)")

    # --- Error Detection ---
    print("\n--- Error Detection ---")

    print("\nUART decoder detects:")
    print("  - Framing errors (wrong stop bit)")
    print("  - Parity errors (when parity enabled)")
    print("  - Break conditions (long low state)")

    print("\nExample error checking:")
    print("  for msg in messages:")
    print("      if msg.framing_error:")
    print('          print(f"Framing error at {msg.time}")')
    print("      if msg.parity_error:")
    print('          print(f"Parity error at {msg.time}")')

    # --- Practical Tips ---
    print("\n--- Practical Tips ---")

    print("\n1. Sample rate should be at least 8x baud rate")
    print(f"   For {baud_rate} baud, minimum {baud_rate * 8 / 1e6:.1f} MSa/s")

    print("\n2. If decoding fails, check:")
    print("   - Correct baud rate")
    print("   - Signal polarity (inverted=True for RS-232)")
    print("   - Threshold level for noisy signals")

    print("\n3. For multi-byte messages, combine bytes:")
    print("   message = bytes(msg.data[0] for msg in messages)")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. UARTDecoder needs baud_rate parameter")
    print("  2. detect_baud_rate() can find unknown rates")
    print("  3. Configure data_bits, parity, stop_bits as needed")
    print("  4. Check msg.framing_error and msg.parity_error")
    print("  5. Sample rate >= 8x baud rate recommended")
    print("=" * 60)


if __name__ == "__main__":
    main()
