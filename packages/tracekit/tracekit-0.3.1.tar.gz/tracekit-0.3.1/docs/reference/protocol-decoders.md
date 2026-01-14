# Protocol Decoders Reference

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

Complete reference for TraceKit's protocol decoders.

## Quick Reference

| Protocol   | Class               | Category   | Status |
| ---------- | ------------------- | ---------- | ------ |
| UART       | `UARTDecoder`       | Serial     | Full   |
| SPI        | `SPIDecoder`        | Serial     | Full   |
| I2C        | `I2CDecoder`        | Serial     | Full   |
| CAN        | `CANDecoder`        | Automotive | Full   |
| CAN-FD     | `CANFDDecoder`      | Automotive | Full   |
| LIN        | `LINDecoder`        | Automotive | Full   |
| FlexRay    | `FlexRayDecoder`    | Automotive | Full   |
| JTAG       | `JTAGDecoder`       | Debug      | Full   |
| SWD        | `SWDDecoder`        | Debug      | Full   |
| 1-Wire     | `OneWireDecoder`    | Serial     | Full   |
| I2S        | `I2SDecoder`        | Audio      | Full   |
| USB        | `USBDecoder`        | Serial     | Full   |
| HDLC       | `HDLCDecoder`       | Data Link  | Full   |
| Manchester | `ManchesterDecoder` | Encoding   | Full   |

## Serial Protocols

### UART / RS-232

Asynchronous serial communication.

```python
from tracekit.analyzers.protocols import UARTDecoder

decoder = UARTDecoder(
    baud_rate=115200,     # Required: bits per second
    data_bits=8,          # Optional: 7, 8, or 9 (default: 8)
    parity="none",        # Optional: "none", "even", "odd" (default: "none")
    stop_bits=1,          # Optional: 1 or 2 (default: 1)
    inverted=False,       # Optional: True for inverted logic
    idle_level="high",    # Optional: "high" or "low" (default: "high")
)

messages = decoder.decode(trace)

for msg in messages:
    print(f"Time: {msg.time}")
    print(f"Data: {msg.data}")
    print(f"Framing error: {msg.framing_error}")
    print(f"Parity error: {msg.parity_error}")
```

**Common Baud Rates**: 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600

### SPI

Synchronous serial with clock, data, and chip select.

```python
from tracekit.analyzers.protocols import SPIDecoder

decoder = SPIDecoder(
    clock=clock_trace,    # Required: Clock signal
    mosi=mosi_trace,      # Optional: Master Out Slave In
    miso=miso_trace,      # Optional: Master In Slave Out
    cs=cs_trace,          # Optional: Chip Select
    cpol=0,               # Clock polarity: 0 or 1 (default: 0)
    cpha=0,               # Clock phase: 0 or 1 (default: 0)
    bit_order="msb",      # "msb" or "lsb" (default: "msb")
    word_size=8,          # Bits per word (default: 8)
    cs_active="low",      # CS active level (default: "low")
)

transactions = decoder.decode()

for txn in transactions:
    print(f"Time: {txn.time}")
    print(f"MOSI: {txn.mosi_data.hex() if txn.mosi_data else 'N/A'}")
    print(f"MISO: {txn.miso_data.hex() if txn.miso_data else 'N/A'}")
```

**SPI Modes**:

| Mode | CPOL | CPHA | Clock Idle | Sample Edge |
| ---- | ---- | ---- | ---------- | ----------- |
| 0    | 0    | 0    | Low        | Rising      |
| 1    | 0    | 1    | Low        | Falling     |
| 2    | 1    | 0    | High       | Falling     |
| 3    | 1    | 1    | High       | Rising      |

### I2C

Two-wire interface with SDA and SCL.

```python
from tracekit.analyzers.protocols import I2CDecoder

decoder = I2CDecoder(
    sda=sda_trace,        # Required: Data line
    scl=scl_trace,        # Required: Clock line
    address_mode="7bit",  # "7bit" or "10bit" (default: "7bit")
    threshold=1.5,        # Voltage threshold (optional)
)

transactions = decoder.decode()

for txn in transactions:
    print(f"Address: 0x{txn.address:02X}")
    print(f"Direction: {txn.direction}")  # "read" or "write"
    print(f"Data: {txn.data.hex()}")
    print(f"ACKs: {txn.acks}")
    print(f"NAK at end: {txn.nak}")
```

**Special Conditions**:

- Start: SDA falls while SCL high
- Stop: SDA rises while SCL high
- Repeated Start: Start without preceding Stop
- ACK: SDA low during 9th clock
- NAK: SDA high during 9th clock

## Automotive Protocols

### CAN

Controller Area Network for vehicles and industrial.

```python
from tracekit.analyzers.protocols import CANDecoder

decoder = CANDecoder(
    bitrate=500000,       # Required: bits per second
    sample_point=0.75,    # Sample point (default: 0.75)
    extended_id=False,    # Support 29-bit IDs (default: False)
)

frames = decoder.decode(trace)

for frame in frames:
    print(f"ID: 0x{frame.id:03X}")
    print(f"Data: {frame.data.hex()}")
    print(f"DLC: {frame.dlc}")
    print(f"RTR: {frame.rtr}")
    print(f"CRC valid: {frame.crc_valid}")
```

**Common Bitrates**: 125000, 250000, 500000, 1000000

### LIN

Local Interconnect Network for low-speed automotive.

```python
from tracekit.analyzers.protocols import LINDecoder

decoder = LINDecoder(
    bitrate=19200,        # Required: bits per second
    version="2.1",        # LIN version: "1.3", "2.0", "2.1" (default: "2.1")
)

frames = decoder.decode(trace)

for frame in frames:
    print(f"ID: 0x{frame.id:02X}")
    print(f"Data: {frame.data.hex()}")
    print(f"Checksum valid: {frame.checksum_valid}")
```

## Debug Interfaces

### JTAG

Joint Test Action Group (IEEE 1149.1).

```python
from tracekit.analyzers.protocols import JTAGDecoder

decoder = JTAGDecoder(
    tck=tck_trace,        # Test Clock
    tms=tms_trace,        # Test Mode Select
    tdi=tdi_trace,        # Test Data In
    tdo=tdo_trace,        # Test Data Out (optional)
)

commands = decoder.decode()

for cmd in commands:
    print(f"State: {cmd.state}")
    print(f"IR: {cmd.instruction}")
    print(f"DR: {cmd.data}")
```

### SWD

Serial Wire Debug for ARM Cortex.

```python
from tracekit.analyzers.protocols import SWDDecoder

decoder = SWDDecoder(
    swclk=swclk_trace,    # Clock
    swdio=swdio_trace,    # Bidirectional data
)

transactions = decoder.decode()

for txn in transactions:
    print(f"Type: {txn.type}")  # "read" or "write"
    print(f"AP/DP: {txn.ap_dp}")
    print(f"Address: {txn.address}")
    print(f"Data: 0x{txn.data:08X}")
    print(f"ACK: {txn.ack}")
```

## Encoding Protocols

### Manchester

Self-clocking encoding where each bit has a transition.

```python
from tracekit.analyzers.protocols import ManchesterDecoder

decoder = ManchesterDecoder(
    bitrate=1000000,      # Bit rate
    convention="ieee",    # "ieee" or "thomas" (default: "ieee")
)

# IEEE: 0 = low-to-high, 1 = high-to-low
# Thomas: 0 = high-to-low, 1 = low-to-high

data = decoder.decode(trace)
print(f"Decoded: {data.hex()}")
```

## Other Protocols

### 1-Wire

Dallas/Maxim 1-Wire protocol.

```python
from tracekit.analyzers.protocols import OneWireDecoder

decoder = OneWireDecoder(
    overdrive=False,      # Overdrive mode (default: False)
)

transactions = decoder.decode(trace)

for txn in transactions:
    print(f"ROM: {txn.rom_code.hex() if txn.rom_code else 'Skip'}")
    print(f"Command: 0x{txn.command:02X}")
    print(f"Data: {txn.data.hex()}")
```

### HDLC

High-Level Data Link Control.

```python
from tracekit.analyzers.protocols import HDLCDecoder

decoder = HDLCDecoder()

frames = decoder.decode(trace)

for frame in frames:
    print(f"Address: {frame.address}")
    print(f"Control: 0x{frame.control:02X}")
    print(f"Info: {frame.info.hex()}")
    print(f"FCS valid: {frame.fcs_valid}")
```

## Protocol Auto-Detection

TraceKit can attempt to identify unknown protocols:

```python
from tracekit.inference import detect_protocol

result = detect_protocol(trace)

print(f"Detected: {result.protocol}")
print(f"Confidence: {result.confidence * 100:.0f}%")
print(f"Parameters: {result.parameters}")

# Use detected parameters
if result.protocol == "uart":
    from tracekit.analyzers.protocols import UARTDecoder
    decoder = UARTDecoder(**result.parameters)
```

## Error Handling

All decoders report protocol-specific errors:

```python
messages = decoder.decode(trace)

for msg in messages:
    if hasattr(msg, 'errors') and msg.errors:
        for error in msg.errors:
            print(f"Error: {error.type} at {error.time}")
            print(f"  Details: {error.description}")
```

## Custom Decoders

Create custom protocol decoders:

```python
from tracekit.analyzers.protocols import BaseDecoder, register_decoder

class MyProtocolDecoder(BaseDecoder):
    name = "my_protocol"

    def __init__(self, bitrate=1000000, **kwargs):
        super().__init__(**kwargs)
        self.bitrate = bitrate

    def decode(self, trace):
        # Implement decoding logic
        messages = []
        # ... parse trace ...
        return messages

# Register for use
register_decoder(MyProtocolDecoder)
```

## See Also

- [Tutorial 5: Protocol Decoding](../tutorials/05-protocol-decoding.md)
- [Protocol Inference API](../api/analysis.md#protocol-inference)
- [Troubleshooting Protocol Issues](../guides/troubleshooting.md#protocol-decoding-issues)
