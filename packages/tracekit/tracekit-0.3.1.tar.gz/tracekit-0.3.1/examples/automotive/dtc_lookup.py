#!/usr/bin/env python3
"""Example: Using the DTC database to look up diagnostic trouble codes.

This example demonstrates how to:
1. Look up specific DTC codes
2. Search for codes by keyword
3. Filter codes by category
4. Parse DTC code format
5. Get database statistics
"""

from tracekit.automotive.dtc import DTCDatabase


def main():
    print("=" * 80)
    print("DTC Database Example - Diagnostic Trouble Code Lookup")
    print("=" * 80)
    print()

    # Example 1: Look up a specific DTC code
    print("Example 1: Look up a specific DTC code")
    print("-" * 80)
    code = "P0420"
    info = DTCDatabase.lookup(code)
    if info:
        print(f"Code: {info.code}")
        print(f"Description: {info.description}")
        print(f"Category: {info.category}")
        print(f"Severity: {info.severity}")
        print(f"System: {info.system}")
        print("Possible Causes:")
        for i, cause in enumerate(info.possible_causes, 1):
            print(f"  {i}. {cause}")
    else:
        print(f"Code {code} not found in database")
    print()

    # Example 2: Search for codes by keyword
    print("Example 2: Search for codes by keyword")
    print("-" * 80)
    keyword = "oxygen"
    results = DTCDatabase.search(keyword)
    print(f"Found {len(results)} codes related to '{keyword}':")
    for dtc in results[:5]:  # Show first 5 results
        print(f"  {dtc.code}: {dtc.description}")
    if len(results) > 5:
        print(f"  ... and {len(results) - 5} more")
    print()

    # Example 3: Get all codes in a category
    print("Example 3: Get all codes in a category")
    print("-" * 80)
    category = "Chassis"
    chassis_codes = DTCDatabase.get_by_category(category)
    print(f"Found {len(chassis_codes)} {category} codes:")
    for dtc in chassis_codes[:5]:  # Show first 5
        print(f"  {dtc.code}: {dtc.description}")
    if len(chassis_codes) > 5:
        print(f"  ... and {len(chassis_codes) - 5} more")
    print()

    # Example 4: Get codes by system
    print("Example 4: Get codes by system")
    print("-" * 80)
    system = "ABS"
    abs_codes = DTCDatabase.get_by_system(system)
    print(f"Found {len(abs_codes)} {system} codes:")
    for dtc in abs_codes[:5]:  # Show first 5
        print(f"  {dtc.code}: {dtc.description}")
    if len(abs_codes) > 5:
        print(f"  ... and {len(abs_codes) - 5} more")
    print()

    # Example 5: Parse DTC code format
    print("Example 5: Parse DTC code format")
    print("-" * 80)
    codes_to_parse = ["P0420", "C0035", "B0001", "U0100", "P1234"]
    for code in codes_to_parse:
        parsed = DTCDatabase.parse_dtc(code)
        if parsed:
            category, code_type, fault_code = parsed
            print(f"{code}: Category={category}, Type={code_type}, Fault Code={fault_code}")
        else:
            print(f"{code}: Invalid format")
    print()

    # Example 6: Get database statistics
    print("Example 6: Get database statistics")
    print("-" * 80)
    stats = DTCDatabase.get_stats()
    print("DTC Database Statistics:")
    for category, count in sorted(stats.items()):
        print(f"  {category}: {count} codes")
    print()

    # Example 7: Look up multiple common codes
    print("Example 7: Common diagnostic trouble codes")
    print("-" * 80)
    common_codes = [
        "P0300",  # Random misfire
        "P0171",  # System too lean
        "C0035",  # Wheel speed sensor
        "B0001",  # Driver airbag
        "U0100",  # Lost communication with ECM
    ]
    for code in common_codes:
        info = DTCDatabase.lookup(code)
        if info:
            print(f"{info.code}: {info.description}")
            print(f"  Severity: {info.severity} | System: {info.system}")
    print()

    # Example 8: Search in possible causes
    print("Example 8: Search in possible causes")
    print("-" * 80)
    search_term = "wiring"
    results = DTCDatabase.search(search_term)
    print(f"Found {len(results)} codes with '{search_term}' in possible causes:")
    for dtc in results[:3]:  # Show first 3
        print(f"\n{dtc.code}: {dtc.description}")
        wiring_causes = [c for c in dtc.possible_causes if search_term.lower() in c.lower()]
        for cause in wiring_causes:
            print(f"  - {cause}")
    print()

    print("=" * 80)
    print("End of DTC Database Example")
    print("=" * 80)


if __name__ == "__main__":
    main()
