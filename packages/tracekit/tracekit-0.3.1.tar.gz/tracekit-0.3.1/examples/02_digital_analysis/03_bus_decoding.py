#!/usr/bin/env python3
"""Example 03: Bus Decoding.

This example demonstrates configurable bus decoding for parallel
digital buses including address, data, and control buses.

Time: 20 minutes
Prerequisites: Edge detection basics

Run:
    uv run python examples/02_digital_analysis/03_bus_decoding.py
"""

import numpy as np

from tracekit.analyzers.digital import (
    BusConfig,
    BusDecoder,
)


def main() -> None:
    """Demonstrate bus decoding capabilities."""
    print("=" * 60)
    print("TraceKit Example: Bus Decoding")
    print("=" * 60)

    # --- Basic 4-bit Bus ---
    print("\n--- Basic 4-bit Data Bus ---")

    demo_4bit_bus()

    # --- 8-bit Address/Data Bus ---
    print("\n--- 8-bit Address/Data Bus ---")

    demo_8bit_bus()

    # --- Clock-Synchronized Bus ---
    print("\n--- Clock-Synchronized Bus ---")

    demo_clocked_bus()

    # --- Active-Low Bus ---
    print("\n--- Active-Low Bus (Memory Chip Selects) ---")

    demo_active_low_bus()

    # --- Summary ---
    print("\n" + "=" * 60)
    print("Key Points:")
    print("  1. BusConfig defines bus width, bit order, and polarity")
    print("  2. BusDecoder samples channels at specified intervals")
    print("  3. Use lsb_first or msb_first for bit ordering")
    print("  4. active_low=True inverts the decoded values")
    print("  5. Clock-synchronized sampling ensures valid data")
    print("=" * 60)


def demo_4bit_bus() -> None:
    """Demonstrate basic 4-bit bus decoding."""
    # Create a 4-bit bus configuration
    config = BusConfig(
        name="data_bus",
        width=4,
        bit_order="lsb_first",
        active_low=False,
    )

    # Define which channels map to which bits
    config.bits = [
        {"channel": 0, "bit": 0, "name": "D0"},
        {"channel": 1, "bit": 1, "name": "D1"},
        {"channel": 2, "bit": 2, "name": "D2"},
        {"channel": 3, "bit": 3, "name": "D3"},
    ]

    print(f"Bus configuration: {config.name}")
    print(f"  Width: {config.width} bits")
    print(f"  Bit order: {config.bit_order}")

    # Create decoder
    sample_rate = 100e6  # 100 MHz
    decoder = BusDecoder(config, sample_rate)

    # Generate synthetic bit traces
    # Pattern: 0, 1, 2, 3, 4, 5 (each value held for 10 samples)
    samples_per_value = 10
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    # Build individual bit traces
    bit_traces = {i: np.zeros(len(values) * samples_per_value, dtype=int) for i in range(4)}

    for idx, val in enumerate(values):
        start = idx * samples_per_value
        end = start + samples_per_value
        for bit in range(4):
            bit_traces[bit][start:end] = (val >> bit) & 1

    # Decode at intervals
    transactions = decoder.sample_at_intervals(bit_traces, interval_samples=samples_per_value)

    print(f"\nDecoded {len(transactions)} transactions:")
    for txn in transactions[:8]:
        print(
            f"  t={txn.timestamp * 1e6:6.2f}us: "
            f"value={txn.value:2d} (0x{txn.value:X}) "
            f"bits={txn.raw_bits}"
        )

    if len(transactions) > 8:
        print(f"  ... ({len(transactions) - 8} more)")


def demo_8bit_bus() -> None:
    """Demonstrate 8-bit bus decoding with MSB-first ordering."""
    # Create 8-bit bus with MSB-first ordering
    config = BusConfig(
        name="address_bus",
        width=8,
        bit_order="msb_first",  # A7 is most significant
        active_low=False,
    )

    # Map channels to bits (A7 down to A0)
    config.bits = [{"channel": i, "bit": 7 - i, "name": f"A{7 - i}"} for i in range(8)]

    sample_rate = 50e6  # 50 MHz
    decoder = BusDecoder(config, sample_rate)

    # Generate address sequence (typical memory access pattern)
    addresses = [0x00, 0x10, 0x20, 0x30, 0x40, 0x80, 0xC0, 0xFF]
    samples_per_addr = 20

    bit_traces = {i: np.zeros(len(addresses) * samples_per_addr, dtype=int) for i in range(8)}

    for idx, addr in enumerate(addresses):
        start = idx * samples_per_addr
        end = start + samples_per_addr
        for bit in range(8):
            # MSB first: channel 0 = bit 7, channel 1 = bit 6, etc.
            bit_value = (addr >> (7 - bit)) & 1
            bit_traces[bit][start:end] = bit_value

    transactions = decoder.sample_at_intervals(bit_traces, interval_samples=samples_per_addr)

    print("\nDecoded address sequence:")
    for txn, expected in zip(transactions, addresses, strict=False):
        match = "OK" if txn.value == expected else "MISMATCH"
        print(
            f"  t={txn.timestamp * 1e6:6.2f}us: "
            f"0x{txn.value:02X} (expected 0x{expected:02X}) [{match}]"
        )


def demo_clocked_bus() -> None:
    """Demonstrate clock-synchronized bus decoding."""
    # 8-bit data bus with clock
    config = BusConfig(
        name="sync_data",
        width=8,
        bit_order="lsb_first",
        active_low=False,
    )
    config.bits = [{"channel": i, "bit": i, "name": f"D{i}"} for i in range(8)]

    sample_rate = 1e9  # 1 GHz (high oversampling)
    decoder = BusDecoder(config, sample_rate)

    # Simulate data with clock at 10 MHz
    clock_period_samples = int(sample_rate / 10e6)  # 100 samples per clock
    num_clocks = 10

    # Generate clock and data
    total_samples = num_clocks * clock_period_samples
    clock = np.zeros(total_samples, dtype=int)
    bit_traces = {i: np.zeros(total_samples, dtype=int) for i in range(8)}

    # Data values change on falling clock edge, sample on rising edge
    data_values = [0x55, 0xAA, 0x0F, 0xF0, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC]

    for clk_idx in range(num_clocks):
        start = clk_idx * clock_period_samples
        mid = start + clock_period_samples // 2

        # Clock high for first half
        clock[start:mid] = 1

        # Data valid during entire clock period
        data = data_values[clk_idx]
        for bit in range(8):
            bit_traces[bit][start : start + clock_period_samples] = (data >> bit) & 1

    # Find rising edges of clock for sampling points
    clock_rising = np.where((clock[:-1] == 0) & (clock[1:] == 1))[0] + 1

    print(f"Clock frequency: 10 MHz ({clock_period_samples} samples/period)")
    print(f"Found {len(clock_rising)} rising clock edges")

    # Sample data at clock rising edges
    print("\nClock-synchronized bus values:")
    for edge_idx, sample_point in enumerate(clock_rising):
        # Read all 8 bits at this sample point
        value = 0
        for bit in range(8):
            if sample_point < len(bit_traces[bit]):
                value |= bit_traces[bit][sample_point] << bit

        expected = data_values[edge_idx]
        match = "OK" if value == expected else "ERROR"
        print(f"  Clock {edge_idx}: 0x{value:02X} (expected 0x{expected:02X}) [{match}]")


def demo_active_low_bus() -> None:
    """Demonstrate active-low bus signals (common in chip selects)."""
    # Memory chip select signals (active low)
    config = BusConfig(
        name="chip_select",
        width=4,
        bit_order="lsb_first",
        active_low=True,  # Signal is active when low
    )

    config.bits = [
        {"channel": 0, "bit": 0, "name": "/CS0"},  # Slash indicates active-low
        {"channel": 1, "bit": 1, "name": "/CS1"},
        {"channel": 2, "bit": 2, "name": "/CS2"},
        {"channel": 3, "bit": 3, "name": "/CS3"},
    ]

    sample_rate = 100e6
    decoder = BusDecoder(config, sample_rate)

    # Generate chip select pattern
    # Active-low: 0 means selected, 1 means not selected
    # We'll select chips 0, 1, 2, 3 in sequence
    samples_per_select = 50

    # Pattern: select CS0, CS1, CS2, CS3, then none
    # Remember: in hardware, pulled LOW = selected
    raw_patterns = [
        0b1110,  # CS0 active (bit 0 = 0 in hardware)
        0b1101,  # CS1 active
        0b1011,  # CS2 active
        0b0111,  # CS3 active
        0b1111,  # None active (all high)
    ]

    bit_traces = {i: np.zeros(len(raw_patterns) * samples_per_select, dtype=int) for i in range(4)}

    for idx, pattern in enumerate(raw_patterns):
        start = idx * samples_per_select
        end = start + samples_per_select
        for bit in range(4):
            bit_traces[bit][start:end] = (pattern >> bit) & 1

    transactions = decoder.sample_at_intervals(bit_traces, interval_samples=samples_per_select)

    print("\nChip select decoding (active-low):")
    print("  Raw value shows which /CS line is LOW (selected)")

    chip_names = {
        0b0001: "CS0 selected",
        0b0010: "CS1 selected",
        0b0100: "CS2 selected",
        0b1000: "CS3 selected",
        0b0000: "None selected",
    }

    for txn in transactions:
        # After active_low inversion, a 1 means the signal was low (selected)
        decoded = txn.value
        desc = chip_names.get(decoded, f"Multiple/Unknown: {decoded:04b}")
        print(f"  t={txn.timestamp * 1e6:6.2f}us: decoded={decoded:04b} -> {desc}")


if __name__ == "__main__":
    main()
