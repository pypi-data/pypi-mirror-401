# 04_protocol_decoding - Serial Protocol Decoding

> **Prerequisites**: [02_digital_analysis](../02_digital_analysis/)
> **Time**: 60 minutes

Learn to decode common serial communication protocols including
UART, SPI, I2C, and CAN.

## Learning Objectives

By completing these examples, you will learn how to:

1. **Decode UART** - Async serial communication
2. **Decode SPI** - Serial Peripheral Interface
3. **Decode I2C** - Inter-Integrated Circuit bus
4. **Decode CAN** - Controller Area Network
5. **Auto-detect protocols** - Automatic protocol inference

## Examples in This Section

### 01_uart_decoding.py

**What it does**: Decode UART/RS-232 serial data

**Concepts covered**:

- Baud rate configuration
- Data bits, parity, stop bits
- Frame detection
- Error handling
- ASCII and hex output

**Run it**:

```bash
uv run python examples/04_protocol_decoding/01_uart_decoding.py
```

**Expected output**: Decoded UART messages with timestamps

---

### 02_spi_decoding.py

**What it does**: Decode SPI bus transactions

**Concepts covered**:

- Clock polarity (CPOL)
- Clock phase (CPHA)
- MOSI/MISO data
- Chip select framing
- Multi-byte transactions

**Run it**:

```bash
uv run python examples/04_protocol_decoding/02_spi_decoding.py
```

**Expected output**: Decoded SPI transactions

---

### 03_i2c_decoding.py

**What it does**: Decode I2C bus transactions

**Concepts covered**:

- Start/stop conditions
- Address detection (7-bit and 10-bit)
- Read vs write operations
- ACK/NACK handling
- Clock stretching

**Run it**:

```bash
uv run python examples/04_protocol_decoding/03_i2c_decoding.py
```

**Expected output**: Decoded I2C transactions with addresses

---

### 04_can_decoding.py

**What it does**: Decode CAN bus frames

**Concepts covered**:

- Standard (11-bit) and extended (29-bit) IDs
- Data frame decoding
- Remote frames
- Error detection
- Bit timing

**Run it**:

```bash
uv run python examples/04_protocol_decoding/04_can_decoding.py
```

**Expected output**: Decoded CAN frames

---

### 05_auto_detection.py

**What it does**: Automatically detect and decode protocols

**Concepts covered**:

- Protocol inference
- Baud rate detection
- Parameter estimation
- Confidence scoring
- Multi-protocol support

**Run it**:

```bash
uv run python examples/04_protocol_decoding/05_auto_detection.py
```

**Expected output**: Detected protocol and decoded data

---

## Quick Reference

### UART Decoding

```python
from tracekit.protocols import UARTDecoder

decoder = UARTDecoder(
    baud_rate=115200,
    data_bits=8,
    parity="none",
    stop_bits=1
)

messages = decoder.decode(trace)

for msg in messages:
    print(f"[{msg.timestamp:.6f}s] {msg.data.hex()}")
    print(f"  ASCII: {msg.data.decode('ascii', errors='replace')}")
```

### SPI Decoding

```python
from tracekit.protocols import SPIDecoder

# Load multi-channel capture
channels = tk.load_all_channels("spi_capture.wfm")

decoder = SPIDecoder(
    clock=channels["CLK"],
    mosi=channels["MOSI"],
    miso=channels["MISO"],
    cs=channels["CS"],
    cpol=0,  # Clock polarity
    cpha=0   # Clock phase
)

transactions = decoder.decode()

for txn in transactions:
    print(f"MOSI: {txn.mosi_data.hex()}")
    print(f"MISO: {txn.miso_data.hex()}")
```

### I2C Decoding

```python
from tracekit.protocols import I2CDecoder

channels = tk.load_all_channels("i2c_capture.wfm")

decoder = I2CDecoder(
    sda=channels["SDA"],
    scl=channels["SCL"],
    address_bits=7
)

transactions = decoder.decode()

for txn in transactions:
    direction = "W" if txn.is_write else "R"
    print(f"0x{txn.address:02X} {direction}: {txn.data.hex()}")
```

### CAN Decoding

```python
from tracekit.protocols import CANDecoder

decoder = CANDecoder(
    bitrate=500000,
    extended_ids=False
)

frames = decoder.decode(trace)

for frame in frames:
    print(f"ID: 0x{frame.arbitration_id:03X}")
    print(f"Data: {frame.data.hex()}")
```

### Auto-Detection

```python
from tracekit.inference import infer_protocol

result = infer_protocol(trace)

print(f"Protocol: {result.protocol_type}")
print(f"Confidence: {result.confidence:.1%}")
print(f"Parameters: {result.parameters}")

# Use detected parameters
if result.protocol_type == "uart":
    decoder = UARTDecoder(**result.parameters)
    messages = decoder.decode(trace)
```

## Common Issues

**Issue**: UART decoding shows garbage

**Solution**: Verify baud rate matches transmitter. Try auto-detection:

```python
from tracekit.inference import detect_baud_rate
baud = detect_baud_rate(trace)
```

---

**Issue**: SPI data is inverted or shifted

**Solution**: Check CPOL/CPHA settings match device configuration.

---

**Issue**: I2C misses transactions

**Solution**: Ensure SDA/SCL channels are correctly identified. Check threshold levels.

---

**Issue**: CAN decoding fails

**Solution**: Verify bitrate and check for CAN-specific signal conditioning.

---

## Estimated Time

- **Quick review**: 20 minutes
- **Hands-on practice**: 60 minutes

## Next Steps

Continue your learning path:

- **[05_advanced](../05_advanced/)** - Advanced analysis techniques
- **[06_expert_api](../06_expert_api/)** - Expert mode features

## See Also

- [User Guide: Protocol Decoding](../../docs/user-guide.md#protocol-decoding)
- [CLI: decode command](../../docs/cli.md#decode)
- [Reference: Protocol Decoders](../../docs/reference/protocol-decoders.md)
