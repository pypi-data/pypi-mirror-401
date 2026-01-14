#!/usr/bin/env python3
"""Demo: Audit Trail with HMAC Chain Verification (LOG-009)

This example demonstrates TraceKit's tamper-evident audit logging
using HMAC signatures to create a verifiable chain of audit entries.

Requirements demonstrated:

Usage:
    uv run python examples/audit_trail_demo.py

Note:
    The secret keys used in this example are EXAMPLE VALUES for demonstration
    purposes only. In production, use cryptographically secure random keys
    stored securely (e.g., environment variables, secrets manager).
"""

import json
import tempfile
from pathlib import Path

import tracekit as tk

# Example secret key for demonstration - DO NOT use in production!
# In production, load from environment variable or secrets manager:
#   secret_key = os.environ.get("AUDIT_SECRET_KEY").encode()
EXAMPLE_SECRET_KEY = b"EXAMPLE-ONLY-replace-in-production-abc123"
EXAMPLE_TEST_KEY = b"EXAMPLE-test-key-not-for-production"


def main() -> None:
    """Demonstrate audit trail functionality."""
    print("=== TraceKit Audit Trail Demo (LOG-009) ===\n")

    # 1. Create an audit trail with a secret key
    print("1. Creating audit trail with secret key...")
    audit = tk.AuditTrail(secret_key=EXAMPLE_SECRET_KEY)
    print("   Created audit trail\n")

    # 2. Record some analysis operations
    print("2. Recording analysis operations...")
    audit.record_action(
        "load_trace",
        {"file": "oscilloscope_capture.wfm", "size_mb": 150, "channels": 4},
        user="alice",
    )
    print("   Recorded: load_trace")

    audit.record_action(
        "compute_fft",
        {"samples": 1000000, "window": "hann", "frequency_range": "1Hz-10MHz"},
        user="alice",
    )
    print("   Recorded: compute_fft")

    audit.record_action(
        "measure_thd",
        {"fundamental_freq": 1000.0, "thd_db": -65.3, "harmonics": 10},
        user="alice",
    )
    print("   Recorded: measure_thd")

    audit.record_action(
        "export_results",
        {"format": "csv", "file": "thd_results.csv", "rows": 100},
        user="alice",
    )
    print("   Recorded: export_results\n")

    # 3. Verify audit trail integrity
    print("3. Verifying audit trail integrity...")
    is_valid = audit.verify_integrity()
    print(f"   {'[OK]' if is_valid else '[!!]'} Integrity check: {is_valid}\n")

    # 4. Query audit entries
    print("4. Querying audit entries...")
    all_entries = audit.get_entries()
    print(f"   Total entries: {len(all_entries)}")

    fft_entries = audit.get_entries(action_type="compute_fft")
    print(f"   FFT entries: {len(fft_entries)}")
    if fft_entries:
        print(f"   - Window type: {fft_entries[0].details['window']}")

    measure_entries = audit.get_entries(action_type="measure_thd")
    if measure_entries:
        print(f"   - THD result: {measure_entries[0].details['thd_db']} dB")
    print()

    # 5. Export audit log
    print("5. Exporting audit log...")
    with tempfile.TemporaryDirectory() as tmpdir:
        json_path = Path(tmpdir) / "audit.json"
        csv_path = Path(tmpdir) / "audit.csv"

        audit.export_audit_log(str(json_path), format="json")
        print(f"   JSON export: {json_path.name}")

        audit.export_audit_log(str(csv_path), format="csv")
        print(f"   CSV export: {csv_path.name}")

        # Show a snippet of the JSON export
        with json_path.open() as f:
            data = json.load(f)
        print(f"   - Version: {data['version']}")
        print(f"   - Hash algorithm: {data['hash_algorithm']}")
        print(f"   - Entries: {len(data['entries'])}")
    print()

    # 6. Demonstrate tamper detection
    print("6. Demonstrating tamper detection...")
    print("   Creating test audit trail...")
    test_audit = tk.AuditTrail(secret_key=EXAMPLE_TEST_KEY)
    test_audit.record_action("action1", {"value": 100})
    test_audit.record_action("action2", {"value": 200})
    test_audit.record_action("action3", {"value": 300})

    print(f"   Before tampering: {test_audit.verify_integrity()}")

    # Tamper with middle entry
    print("   Tampering with entry 2...")
    test_audit._entries[1].details["value"] = 999

    is_valid_after = test_audit.verify_integrity()
    print(f"   After tampering: {is_valid_after}")
    print(f"   {'[OK]' if not is_valid_after else '[!!]'} Tampering detected!\n")

    # 7. Global audit trail
    print("7. Using global audit trail...")
    # Record to global trail (singleton)
    tk.record_audit("global_action", {"test": "data", "priority": "high"})
    tk.record_audit("another_action", {"test": "more_data"})

    global_audit = tk.get_global_audit_trail()
    global_entries = global_audit.get_entries()
    print(f"   Global trail entries: {len(global_entries)}")
    print(f"   Latest entry: {global_entries[-1].action}\n")

    # 8. Show HMAC chain structure
    print("8. HMAC chain structure...")
    print("   Entry -> Previous Hash -> HMAC")
    for i, entry in enumerate(audit.get_entries()[:3]):
        prev_hash = (
            entry.previous_hash[:16] + "..."
            if len(entry.previous_hash) > 16
            else entry.previous_hash
        )
        hmac_hash = entry.hmac[:16] + "..."
        print(f"   {i + 1}. {entry.action:20s} -> {prev_hash:20s} -> {hmac_hash}")
    print()

    print("=== Demo Complete ===")
    print("\nKey features demonstrated:")
    print("  - Tamper-evident logging with HMAC signatures")
    print("  - Chain verification (any modification breaks the chain)")
    print("  - Export to JSON and CSV formats")
    print("  - Query API with filtering")
    print("  - Global audit trail singleton")
    print("  - Automatic capture of user, host, and timestamp")


if __name__ == "__main__":
    main()
