# Configuration Examples

> **Version**: 1.0.0 | **Last Updated**: 2026-01-06

This directory contains example YAML configuration files for TraceKit's
configuration-driven features.

## Files

### packet_format_example.yaml

Defines packet structure for binary data loading.

**Use case**: Loading proprietary binary packet captures

**Key sections**:

- Header format
- Payload structure
- Field definitions
- Endianness settings

```yaml
# Example usage
packet_format:
  header_size: 16
  fields:
    - name: timestamp
      offset: 0
      type: uint64
      endian: little
    - name: channel
      offset: 8
      type: uint8
```

### device_mapping_example.yaml

Maps device identifiers to human-readable names.

**Use case**: Protocol decoding with known device addresses

**Key sections**:

- I2C address mappings
- SPI device assignments
- CAN node identifiers

```yaml
# Example usage
devices:
  i2c:
    0x50: 'EEPROM'
    0x68: 'RTC'
  can:
    0x100: 'Engine_ECU'
    0x200: 'Transmission_ECU'
```

### bus_config_example.yaml

Configures bus protocol parameters.

**Use case**: Multi-channel bus analysis

**Key sections**:

- Channel assignments
- Timing parameters
- Protocol variants

```yaml
# Example usage
spi_bus:
  clock_channel: D0
  mosi_channel: D1
  miso_channel: D2
  cs_channel: D3
  cpol: 0
  cpha: 0
  bit_order: msb_first
```

### protocol_definition_example.yaml

Defines custom protocol decoders using DSL.

**Use case**: Decoding proprietary or uncommon protocols

**Key sections**:

- Frame structure
- Field types
- Validation rules
- Checksum algorithms

```yaml
# Example usage
protocol:
  name: custom_serial
  sync_pattern: [0xAA, 0x55]
  fields:
    - name: length
      type: uint8
    - name: payload
      type: bytes
      length_field: length
    - name: checksum
      type: crc16
```

### universal_report_config.yaml

Configures report generation settings.

**Use case**: Customizing report appearance and content

**Key sections**:

- Branding (logo, company)
- Section selection
- Plot settings
- Output formats

```yaml
# Example usage
report:
  title: 'Signal Analysis Report'
  author: 'Engineering Team'
  sections:
    - summary
    - measurements
    - plots
  theme: corporate
```

## Using Configuration Files

### From Python

```python
import tracekit as tk

# Load with configuration
trace = tk.load("capture.bin", config="configs/packet_format_example.yaml")

# Or specify config directly
from tracekit.config import load_config

config = load_config("configs/bus_config_example.yaml")
decoder = tk.create_decoder(config)
```

### From CLI

```bash
# Use config file
uv run tracekit decode capture.wfm --config configs/bus_config_example.yaml

# Generate report with config
uv run tracekit report capture.wfm --config configs/universal_report_config.yaml
```

## Creating Custom Configurations

1. Copy the appropriate example file
2. Modify for your use case
3. Validate with TraceKit:

```bash
uv run tracekit config --validate my_config.yaml
```

## Configuration Schema

Full schema documentation available in the API reference:

- [Config Schema](../../docs/api/config.md)
- [Protocol DSL Reference](../../docs/reference/protocol-decoders.md)

## See Also

- [User Guide](../../docs/user-guide.md)
- [CLI Reference](../../docs/cli.md)
