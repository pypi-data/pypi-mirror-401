#!/usr/bin/env python3
"""Example: SPI Protocol Decoding.

This example demonstrates decoding SPI (Serial Peripheral Interface)
bus communication from multi-channel captures.

Time: 15 minutes
Prerequisites: UART decoding example

Run:
    uv run python examples/04_protocol_decoding/02_spi_decoding.py
"""
# mypy: disable-error-code="no-untyped-def,no-untyped-call,type-arg,attr-defined,arg-type,union-attr,call-arg,index,no-any-return,override,return-value,var-annotated,func-returns-value,unreachable,assignment,str-bytes-safe,misc,operator,call-overload"

from tracekit.protocols import SPIDecoder

from tracekit.testing import generate_spi_signal


def main() -> None:
    """Demonstrate SPI decoding."""
    print("=" * 60)
    print("TraceKit Example: SPI Protocol Decoding")
    print("=" * 60)

    # --- SPI Overview ---
    print("\n--- SPI Overview ---")
    print("SPI uses 4 signals:")
    print("  SCLK - Clock (master generates)")
    print("  MOSI - Master Out, Slave In")
    print("  MISO - Master In, Slave Out")
    print("  CS   - Chip Select (active low)")

    # --- Generate Test SPI Signal ---
    print("\n--- Generating Test SPI Signal ---")

    test_data = bytes([0xAA, 0x55, 0xDE, 0xAD, 0xBE, 0xEF])

    spi_signals = generate_spi_signal(
        clock_freq=1e6,  # 1 MHz clock
        data=test_data,
        sample_rate=50e6,  # 50 MSa/s
        cpol=0,  # Clock idle low
        cpha=0,  # Sample on rising edge
    )

    print("Generated SPI signal:")
    print("  Clock frequency: 1 MHz")
    print("  CPOL=0, CPHA=0 (Mode 0)")
    print(f"  Data: {test_data.hex()}")
    print(f"  Channels: {list(spi_signals.keys())}")

    # --- Basic SPI Decoding ---
    print("\n--- Basic SPI Decoding ---")

    decoder = SPIDecoder(
        clock=spi_signals["clk"],
        mosi=spi_signals["mosi"],
        miso=spi_signals.get("miso"),  # Optional
        cs=spi_signals.get("cs"),  # Optional
        cpol=0,
        cpha=0,
    )

    transactions = decoder.decode()

    print(f"Decoded {len(transactions)} transaction(s)")

    for i, txn in enumerate(transactions):
        print(f"\nTransaction {i + 1}:")
        print(f"  Time: {txn.time * 1e6:.2f} us")
        print(f"  MOSI data: {txn.mosi_data.hex() if txn.mosi_data else 'N/A'}")
        if txn.miso_data:
            print(f"  MISO data: {txn.miso_data.hex()}")

    # --- SPI Modes ---
    print("\n--- SPI Modes (CPOL/CPHA) ---")
    print("\n  Mode | CPOL | CPHA | Clock Idle | Sample Edge")
    print("  -----|------|------|------------|------------")
    print("    0  |  0   |  0   | Low        | Rising")
    print("    1  |  0   |  1   | Low        | Falling")
    print("    2  |  1   |  0   | High       | Falling")
    print("    3  |  1   |  1   | High       | Rising")

    # --- Finding Correct Mode ---
    print("\n--- Finding Correct SPI Mode ---")
    print("If mode is unknown, try all combinations:")

    print("\n  Testing all modes:")
    for cpol in [0, 1]:
        for cpha in [0, 1]:
            decoder_test = SPIDecoder(
                clock=spi_signals["clk"],
                mosi=spi_signals["mosi"],
                cpol=cpol,
                cpha=cpha,
            )
            try:
                txns = decoder_test.decode()
                if txns and txns[0].mosi_data:
                    first_byte = txns[0].mosi_data[0]
                    expected = test_data[0]
                    match = "MATCH" if first_byte == expected else "no match"
                    print(f"    CPOL={cpol}, CPHA={cpha}: first byte=0x{first_byte:02X} ({match})")
            except Exception as e:
                print(f"    CPOL={cpol}, CPHA={cpha}: Error - {e}")

    # --- Bit Order ---
    print("\n--- Bit Order ---")
    print("\nSPI can be MSB-first (most common) or LSB-first:")
    print('  decoder = SPIDecoder(..., bit_order="msb")  # Default')
    print('  decoder = SPIDecoder(..., bit_order="lsb")  # Less common')

    # --- Word Size ---
    print("\n--- Word Size ---")
    print("\nDefault is 8 bits, but some devices use different sizes:")
    print("  decoder = SPIDecoder(..., word_size=8)   # Standard")
    print("  decoder = SPIDecoder(..., word_size=16)  # 16-bit words")
    print("  decoder = SPIDecoder(..., word_size=12)  # 12-bit ADC")

    # --- Chip Select Behavior ---
    print("\n--- Chip Select ---")
    print("\nCS defines transaction boundaries:")
    print('  cs_active="low"   # Most common (active low)')
    print('  cs_active="high"  # Active high (rare)')
    print("\nWithout CS, decoder uses clock gaps to separate transactions")

    # --- Practical Example ---
    print("\n--- Practical Example: Reading SPI Flash ---")
    print("\nTypical SPI flash read sequence:")
    print("  MOSI: [0x03, 0x00, 0x00, 0x00]  # Read command + 24-bit address")
    print("  MISO: [0xFF, 0xFF, 0xFF, 0xFF, data...]  # Dummy + data")

    print("\nDecoding would show:")
    print("  Transaction 1:")
    print("    MOSI: 0x03 0x00 0x00 0x00 0x00 0x00...")
    print("    MISO: 0xFF 0xFF 0xFF 0xFF 0x48 0x65...")
    print("  The MISO data after address bytes is the actual flash content")

    # --- Tips ---
    print("\n--- Tips for SPI Analysis ---")
    print("\n1. Capture all 4 lines if possible (CLK, MOSI, MISO, CS)")
    print("2. Sample rate should be >= 4x clock frequency")
    print("3. If decoding fails, try all CPOL/CPHA combinations")
    print("4. Check bit order - some devices use LSB first")
    print("5. Long transactions may be split - check CS signal")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. SPI needs clock + at least one data line")
    print("  2. CPOL/CPHA (mode) must match device configuration")
    print("  3. Try all 4 modes if configuration unknown")
    print("  4. CS signal defines transaction boundaries")
    print("  5. Default is MSB-first, 8-bit words")
    print("=" * 60)


if __name__ == "__main__":
    main()
