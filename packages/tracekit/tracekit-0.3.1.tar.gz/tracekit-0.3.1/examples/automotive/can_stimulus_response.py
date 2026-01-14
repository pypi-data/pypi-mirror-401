#!/usr/bin/env python3
"""Example: CAN stimulus-response mapping.

This example demonstrates how to use stimulus-response analysis to identify
which CAN messages and signals change in response to user actions.

This is essential for reverse engineering CAN protocols when you can control
the vehicle/system and observe responses to specific actions.

Use case: "What messages change when I press the brake pedal?"
"""

import struct

from tracekit.automotive.can import CANMessage, CANSession


def create_baseline_session() -> CANSession:
    """Create baseline capture (vehicle idle, no user action).

    This represents the "normal" state of the CAN bus with no stimulus.
    """
    messages = []

    # Message 0x100 - Constant status message
    for i in range(100):
        msg = CANMessage(
            arbitration_id=0x100,
            timestamp=i * 0.01,
            data=bytes([0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x11, 0x22]),
        )
        messages.append(msg)

    # Message 0x200 - Engine at idle (800 RPM)
    for i in range(100):
        rpm = 800
        raw_rpm = int(rpm / 0.25)  # Scale: 0.25 RPM/bit
        data = bytearray(8)
        data[0:2] = struct.pack(">H", raw_rpm)  # RPM in bytes 0-1
        data[2:8] = bytes([0x00] * 6)
        msg = CANMessage(
            arbitration_id=0x200,
            timestamp=i * 0.01,
            data=bytes(data),
        )
        messages.append(msg)

    # Message 0x300 - Throttle position at 0%
    for i in range(100):
        throttle_pct = 0
        raw_throttle = int(throttle_pct / 0.4)  # Scale: 0.4%/bit
        msg = CANMessage(
            arbitration_id=0x300,
            timestamp=i * 0.01,
            data=bytes([raw_throttle, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
        )
        messages.append(msg)

    # Message 0x400 - Brake pedal NOT pressed
    for i in range(100):
        msg = CANMessage(
            arbitration_id=0x400,
            timestamp=i * 0.01,
            data=bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
        )
        messages.append(msg)

    return CANSession.from_messages(messages)


def create_brake_stimulus_session() -> CANSession:
    """Create stimulus capture (brake pedal pressed).

    This represents the CAN bus state when the brake is pressed.
    Changes from baseline:
    - Message 0x400: Brake flag changes from 0x00 to 0xFF
    - Message 0x500: New message appears (brake light control)
    """
    messages = []

    # Message 0x100 - Still constant
    for i in range(100):
        msg = CANMessage(
            arbitration_id=0x100,
            timestamp=i * 0.01,
            data=bytes([0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x11, 0x22]),
        )
        messages.append(msg)

    # Message 0x200 - Engine still at idle
    for i in range(100):
        rpm = 800
        raw_rpm = int(rpm / 0.25)
        data = bytearray(8)
        data[0:2] = struct.pack(">H", raw_rpm)
        data[2:8] = bytes([0x00] * 6)
        msg = CANMessage(
            arbitration_id=0x200,
            timestamp=i * 0.01,
            data=bytes(data),
        )
        messages.append(msg)

    # Message 0x300 - Throttle still at 0%
    for i in range(100):
        msg = CANMessage(
            arbitration_id=0x300,
            timestamp=i * 0.01,
            data=bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
        )
        messages.append(msg)

    # Message 0x400 - Brake pedal PRESSED (byte 0 changes)
    for i in range(100):
        msg = CANMessage(
            arbitration_id=0x400,
            timestamp=i * 0.01,
            data=bytes([0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
        )
        messages.append(msg)

    # Message 0x500 - NEW: Brake light control (only appears when brake pressed)
    for i in range(100):
        msg = CANMessage(
            arbitration_id=0x500,
            timestamp=i * 0.01,
            data=bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]),
        )
        messages.append(msg)

    return CANSession.from_messages(messages)


def create_throttle_stimulus_session() -> CANSession:
    """Create stimulus capture (throttle pressed to 50%).

    Changes from baseline:
    - Message 0x200: RPM increases to 3000
    - Message 0x300: Throttle position changes to 50%
    """
    messages = []

    # Message 0x100 - Still constant
    for i in range(100):
        msg = CANMessage(
            arbitration_id=0x100,
            timestamp=i * 0.01,
            data=bytes([0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x11, 0x22]),
        )
        messages.append(msg)

    # Message 0x200 - Engine at 3000 RPM
    for i in range(100):
        rpm = 3000
        raw_rpm = int(rpm / 0.25)
        data = bytearray(8)
        data[0:2] = struct.pack(">H", raw_rpm)
        data[2:8] = bytes([0x00] * 6)
        msg = CANMessage(
            arbitration_id=0x200,
            timestamp=i * 0.01,
            data=bytes(data),
        )
        messages.append(msg)

    # Message 0x300 - Throttle at 50%
    for i in range(100):
        throttle_pct = 50
        raw_throttle = int(throttle_pct / 0.4)
        msg = CANMessage(
            arbitration_id=0x300,
            timestamp=i * 0.01,
            data=bytes([raw_throttle, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
        )
        messages.append(msg)

    # Message 0x400 - Brake not pressed
    for i in range(100):
        msg = CANMessage(
            arbitration_id=0x400,
            timestamp=i * 0.01,
            data=bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
        )
        messages.append(msg)

    return CANSession.from_messages(messages)


def main():
    """Demonstrate stimulus-response analysis."""
    print("=== CAN Stimulus-Response Analysis ===\n")

    # Create baseline session
    baseline = create_baseline_session()
    print(f"Baseline session: {baseline}")
    print(f"  Messages: {sorted(baseline.unique_ids())}")
    print()

    # ===== Scenario 1: Brake Pedal Analysis =====
    print("--- Scenario 1: What changes when I press the brake? ---\n")

    brake_stimulus = create_brake_stimulus_session()
    print(f"Brake stimulus session: {brake_stimulus}")
    print(f"  Messages: {sorted(brake_stimulus.unique_ids())}")
    print()

    # Compare baseline to brake stimulus
    report = baseline.compare_to(brake_stimulus)
    print(report.summary())
    print()

    # Examine specific changes
    if 0x400 in report.byte_changes:
        print("Byte-level changes in message 0x400 (brake pedal):")
        for change in report.byte_changes[0x400]:
            print(f"  Byte {change.byte_position}:")
            print(f"    Baseline values: {[f'0x{v:02X}' for v in change.baseline_values]}")
            print(f"    Stimulus values: {[f'0x{v:02X}' for v in change.stimulus_values]}")
            print(f"    Change magnitude: {change.change_magnitude:.2f}")
        print()

    # ===== Scenario 2: Throttle Analysis =====
    print("--- Scenario 2: What changes when I press the throttle? ---\n")

    throttle_stimulus = create_throttle_stimulus_session()
    print(f"Throttle stimulus session: {throttle_stimulus}")
    print()

    report2 = baseline.compare_to(throttle_stimulus)
    print(report2.summary())
    print()

    # Show changed message IDs
    print("Messages that responded to throttle:")
    for msg_id in report2.changed_messages:
        print(f"  0x{msg_id:03X}")
        if msg_id in report2.byte_changes:
            for change in report2.byte_changes[msg_id]:
                if change.change_magnitude > 0.1:
                    print(
                        f"    Byte {change.byte_position}: mean changed by {change.mean_change:.1f}"
                    )
    print()

    # ===== Using StimulusResponseAnalyzer directly =====
    print("--- Using StimulusResponseAnalyzer directly ---\n")

    from tracekit.automotive.can.stimulus_response import StimulusResponseAnalyzer

    analyzer = StimulusResponseAnalyzer()

    # Find responsive messages
    responsive = analyzer.find_responsive_messages(baseline, brake_stimulus)
    print(f"Responsive messages (brake): {[f'0x{m:03X}' for m in responsive]}")

    responsive2 = analyzer.find_responsive_messages(baseline, throttle_stimulus)
    print(f"Responsive messages (throttle): {[f'0x{m:03X}' for m in responsive2]}")
    print()

    # Analyze specific message
    print("Detailed analysis of message 0x300 (throttle):")
    changes = analyzer.analyze_signal_changes(baseline, throttle_stimulus, 0x300)
    for change in changes:
        if change.change_magnitude > 0.05:
            print(f"  Byte {change.byte_position}:")
            print(f"    Change magnitude: {change.change_magnitude:.3f}")
            print(f"    Value range change: {change.value_range_change:.1f}")
            print(f"    Mean change: {change.mean_change:.1f}")

    print("\n=== Real-world workflow ===")
    print("1. Record baseline capture (no action)")
    print("2. Record stimulus capture (specific action)")
    print("3. Compare: baseline.compare_to(stimulus)")
    print("4. Identify responsive messages")
    print("5. Analyze byte-level changes")
    print("6. Test hypothesis with signal definitions")


if __name__ == "__main__":
    main()
