# Protocol Export Examples

> **Purpose**: Generate artifacts from TraceKit protocol definitions for use in external tools

## Overview

This section demonstrates exporting TraceKit protocol definitions to formats usable by external analysis tools, focusing on Wireshark Lua dissector generation.

## Examples

### `wireshark_dissector_example.py`

Generates Wireshark Lua dissectors from TraceKit protocol definitions.

**What it does:**

- Creates protocol definitions using TraceKit's Protocol DSL
- Generates Wireshark-compatible Lua dissector scripts
- Outputs ready-to-use dissector files

**Protocols demonstrated:**

- Simple test protocol (TCP port 8000)
- Modbus-like protocol (TCP port 502)
- Custom protocol with various field types (UDP port 5000)

**Output location:** `generated_dissectors/` (repo root)

**Running the example:**

```bash
cd /path/to/tracekit
uv run python examples/05_export/wireshark_dissector_example.py
```

**Expected output:**

```
Wireshark Dissector Generation Example
======================================================================

Generating simple.lua...
  Written to: generated_dissectors/simple.lua
  Protocol: Simple Test Protocol
  Fields: 5

Generating modbus.lua...
  Written to: generated_dissectors/modbus.lua
  Protocol: Modbus Protocol
  Fields: 6

Generating custom.lua...
  Written to: generated_dissectors/custom.lua
  Protocol: Custom Protocol Example
  Fields: 8

Generation complete!

======================================================================
INSTALLATION INSTRUCTIONS
======================================================================
[Instructions for installing dissectors in Wireshark...]
```

## Generated Output

All generated files are written to `generated_dissectors/` at the repository root:

```
tracekit/
├── generated_dissectors/    # ← Output directory
│   ├── simple.lua           # Generated dissector
│   ├── modbus.lua           # Generated dissector
│   └── custom.lua           # Generated dissector
└── examples/
    └── 05_export/
        └── wireshark_dissector_example.py
```

**Note:** The `generated_dissectors/` directory is gitignored - generated files are not tracked in version control.

## Using Generated Dissectors

### Wireshark Installation

Copy generated `.lua` files to your Wireshark plugins directory:

**Linux:**

```bash
cp generated_dissectors/*.lua ~/.local/lib/wireshark/plugins/
# or
cp generated_dissectors/*.lua ~/.config/wireshark/plugins/
```

**macOS:**

```bash
cp generated_dissectors/*.lua ~/.config/wireshark/plugins/
```

**Windows:**

```powershell
copy generated_dissectors\*.lua %APPDATA%\Wireshark\plugins\
```

### Activating Dissectors

1. Restart Wireshark, or
2. Reload Lua plugins: **Analyze → Reload Lua Plugins** (Ctrl+Shift+L)

### Using Dissectors

Dissectors automatically activate for configured ports:

- `simple` protocol → TCP port 8000
- `modbus` protocol → TCP port 502
- `custom` protocol → UDP port 5000

Or manually decode: Right-click packet → **Decode As** → select protocol

## Protocol DSL

The example uses TraceKit's Protocol DSL to define protocol structures:

```python
from tracekit.inference.protocol_dsl import FieldDefinition, ProtocolDefinition

protocol = ProtocolDefinition(
    name="myprotocol",
    description="My Custom Protocol",
    version="1.0",
    settings={"transport": "tcp", "port": 9000},
    fields=[
        FieldDefinition(
            name="header",
            field_type="uint16",
            size=2,
            description="Protocol Header",
        ),
        FieldDefinition(
            name="payload",
            field_type="bytes",
            size="remaining",
            description="Payload Data",
        ),
    ],
)
```

### Supported Field Types

- **Integer types**: `uint8`, `uint16`, `uint32`, `uint64`
- **Float types**: `float32`, `float64`
- **Variable types**: `bytes`, `string`
- **Size specifiers**: Fixed size, field reference (`"length"`), or `"remaining"`

### Features

- **Enumerations**: Named values for integer fields
- **Endianness**: Big or little endian
- **Transport**: TCP or UDP
- **Validation**: Optional protocol validation during generation

## See Also

- [Protocol DSL Documentation](../../docs/api/protocol_dsl.md)
- [Wireshark Lua API](https://wiki.wireshark.org/Lua)
- [Protocol Decoding Examples](../04_protocol_decoding/README.md)

## Prerequisites

- Python 3.12+
- TraceKit installed (`uv sync`)
- Wireshark (for using generated dissectors)

## Next Steps

- **Modify examples**: Edit protocol definitions to match your custom protocol
- **Test dissectors**: Capture network traffic and verify decoding in Wireshark
- **Iterate**: Refine protocol definitions based on real traffic analysis
