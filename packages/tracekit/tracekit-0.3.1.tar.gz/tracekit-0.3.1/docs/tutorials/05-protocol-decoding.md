# Tutorial 5: Protocol Decoding

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08 | **Time**: 35 minutes

Learn to decode serial communication protocols from waveform captures.

## Prerequisites

- Completed [Tutorial 3: Digital Signal Analysis](03-digital-signals.md)
- Basic understanding of serial protocols (UART, SPI, I2C)

## Learning Objectives

By the end of this tutorial, you will be able to:

- Decode UART/RS-232 communications
- Decode SPI bus transactions
- Decode I2C bus transactions
- Handle protocol timing issues

## Overview of Protocol Decoders

TraceKit includes 16+ protocol decoders:

| Category   | Protocols                          |
| ---------- | ---------------------------------- |
| Serial     | UART, SPI, I2C                     |
| Automotive | CAN, LIN                           |
| Debug      | JTAG, SWD                          |
| Encoding   | Manchester, Miller                 |
| Other      | 1-Wire, MDIO, DMX512, DALI, Modbus |

## UART Decoding

UART (Universal Asynchronous Receiver/Transmitter) is common for debug consoles and device communication.

### Basic UART Decoding

```python
import tracekit as tk
from tracekit.protocols import UARTDecoder
# In practice, load captured UART data from a file
# uart_trace = tk.load("uart_capture.wfm")

# Create decoder
decoder = UARTDecoder(baud_rate=115200)

# Decode the signal
# messages = decoder.decode(uart_trace)

# print(f"Decoded {len(messages)} messages:")
# for msg in messages:
#     print(f"  Time: {msg.time * 1e6:.1f} us")
#     print(f"  Data: {msg.data}")
#     print(f"  Text: {msg.data.decode('utf-8', errors='replace')}")
```

### UART Configuration Options

```python
# Full configuration
decoder = UARTDecoder(
    baud_rate=9600,
    data_bits=8,        # 7, 8, or 9
    parity="none",      # "none", "even", "odd"
    stop_bits=1,        # 1 or 2
    inverted=False,     # True for inverted logic
)

messages = decoder.decode(uart_trace)
```

### Auto-Detecting Baud Rate

```python
from tracekit.inference import detect_baud_rate

# Unknown baud rate? Detect it
detected = detect_baud_rate(uart_trace)
print(f"Detected baud rate: {detected}")

# Then decode
decoder = UARTDecoder(baud_rate=detected)
messages = decoder.decode(uart_trace)
```

### Handling UART Errors

```python
# Decode with error detection
messages = decoder.decode(uart_trace)

for msg in messages:
    if msg.framing_error:
        print(f"Framing error at {msg.time * 1e6:.1f} us")
    if msg.parity_error:
        print(f"Parity error at {msg.time * 1e6:.1f} us")
```

## SPI Decoding

SPI (Serial Peripheral Interface) uses clock, data, and chip select lines.

### Basic SPI Decoding

```python
from tracekit.protocols import SPIDecoder
# In practice, load captured SPI signals from a file
# channels = tk.load_all_channels("spi_capture.wfm")
# spi_signals = {
#     "clk": channels["CH1"],
#     "mosi": channels["CH2"],
#     "miso": channels["CH3"],
#     "cs": channels["CH4"]
# }

# Create decoder with channel assignments
# decoder = SPIDecoder(
#     clock=spi_signals["clk"],
#     mosi=spi_signals["mosi"],
#     miso=spi_signals["miso"],
#     cs=spi_signals["cs"]
# )

# Decode transactions
# transactions = decoder.decode()

# print(f"Decoded {len(transactions)} SPI transactions:")
# for txn in transactions:
#     print(f"  Time: {txn.time * 1e6:.1f} us")
#     print(f"  MOSI: {txn.mosi_data.hex()}")
#     print(f"  MISO: {txn.miso_data.hex()}")
```

### SPI Mode Configuration

SPI has four modes based on clock polarity (CPOL) and phase (CPHA):

| Mode | CPOL | CPHA | Description                  |
| ---- | ---- | ---- | ---------------------------- |
| 0    | 0    | 0    | Idle low, sample on rising   |
| 1    | 0    | 1    | Idle low, sample on falling  |
| 2    | 1    | 0    | Idle high, sample on falling |
| 3    | 1    | 1    | Idle high, sample on rising  |

```python
# Specify SPI mode
decoder = SPIDecoder(
    clock=clk,
    mosi=mosi,
    cpol=0,  # Clock polarity
    cpha=0,  # Clock phase
    bit_order="msb"  # or "lsb"
)
```

### Finding the Right SPI Mode

```python
# Try all modes to find which works
for cpol in [0, 1]:
    for cpha in [0, 1]:
        decoder = SPIDecoder(
            clock=spi_signals["clk"],
            mosi=spi_signals["mosi"],
            cpol=cpol,
            cpha=cpha
        )
        txns = decoder.decode()
        if txns and txns[0].mosi_data[0] == 0xAA:  # Expected first byte
            print(f"Correct mode: CPOL={cpol}, CPHA={cpha}")
            break
```

## I2C Decoding

I2C uses two lines: SDA (data) and SCL (clock).

### Basic I2C Decoding

```python
from tracekit.protocols import I2CDecoder
# In practice, load captured I2C signals from a file
# channels = tk.load_all_channels("i2c_capture.wfm")
# i2c_signals = {
#     "sda": channels["CH1"],
#     "scl": channels["CH2"]
# }

# Create decoder
# decoder = I2CDecoder(
#     sda=i2c_signals["sda"],
#     scl=i2c_signals["scl"]
# )

# Decode transactions
# transactions = decoder.decode()

# print(f"Decoded {len(transactions)} I2C transactions:")
# for txn in transactions:
#     print(f"  Address: 0x{txn.address:02X} ({txn.direction})")
#     print(f"  Data: {txn.data.hex()}")
#     print(f"  ACK/NAK: {txn.acks}")
```

### I2C Address Formats

```python
# I2C addresses can be 7-bit or 10-bit
decoder = I2CDecoder(
    sda=sda,
    scl=scl,
    address_mode="7bit"  # or "10bit"
)

# Address in transactions includes R/W bit
for txn in transactions:
    # txn.address is 7-bit address
    # txn.direction is "read" or "write"
    print(f"0x{txn.address:02X} {txn.direction}")
```

### Handling I2C Bus Errors

```python
for txn in transactions:
    if txn.arbitration_lost:
        print(f"Arbitration lost at {txn.time * 1e6:.1f} us")
    if any(not ack for ack in txn.acks):
        print(f"NAK received at {txn.time * 1e6:.1f} us")
```

## CAN Bus Decoding

For automotive and industrial applications:

```python
from tracekit.protocols import CANDecoder
# In practice, load captured CAN signal from a file
# can_trace = tk.load("can_capture.wfm")

# Decode
# decoder = CANDecoder(bitrate=500000)
# frames = decoder.decode(can_trace)

# for frame in frames:
#     print(f"ID: 0x{frame.id:03X}, Data: {frame.data.hex()}")
```

## Protocol Inference

When protocol parameters are unknown:

```python
from tracekit.inference import infer_protocol

# Try to identify the protocol
result = infer_protocol(trace)

print(f"Detected protocol: {result.protocol}")
print(f"Confidence: {result.confidence * 100:.0f}%")
print(f"Parameters: {result.parameters}")

# Use detected parameters
if result.protocol == "uart":
    decoder = UARTDecoder(**result.parameters)
    messages = decoder.decode(trace)
```

## Multi-Channel Analysis

Correlate multiple protocol channels:

```python
# Load multi-channel capture
channels = tk.load_all_channels("capture.wfm")

# Decode each protocol
uart_decoder = UARTDecoder(baud_rate=115200)
uart_msgs = uart_decoder.decode(channels["CH1"])

i2c_decoder = I2CDecoder(
    sda=channels["CH2"],
    scl=channels["CH3"]
)
i2c_txns = i2c_decoder.decode()

# Correlate by time
print("Timeline:")
all_events = []
for msg in uart_msgs:
    all_events.append((msg.time, "UART", msg.data))
for txn in i2c_txns:
    all_events.append((txn.time, "I2C", f"0x{txn.address:02X}"))

for time, proto, data in sorted(all_events):
    print(f"  {time * 1e6:8.1f} us: [{proto}] {data}")
```

## Complete Decoding Example

```python
import tracekit as tk
from tracekit.protocols import UARTDecoder
from tracekit.inference import detect_baud_rate, detect_uart_params

# Load captured waveform
trace = tk.load("uart_capture.wfm")

# Auto-detect parameters
print("=== Protocol Analysis ===")
print(f"Signal duration: {trace.duration * 1e3:.2f} ms")

# Detect baud rate
baud = detect_baud_rate(trace)
print(f"Detected baud rate: {baud}")

# Detect other parameters
params = detect_uart_params(trace)
print(f"Data bits: {params.data_bits}")
print(f"Parity: {params.parity}")
print(f"Stop bits: {params.stop_bits}")

# Decode with detected parameters
decoder = UARTDecoder(
    baud_rate=baud,
    data_bits=params.data_bits,
    parity=params.parity,
    stop_bits=params.stop_bits
)

messages = decoder.decode(trace)

print(f"\n=== Decoded Messages ({len(messages)}) ===")
for msg in messages:
    try:
        text = msg.data.decode("utf-8")
        print(f"  [{msg.time * 1e3:.2f} ms] {repr(text)}")
    except UnicodeDecodeError:
        print(f"  [{msg.time * 1e3:.2f} ms] {msg.data.hex()}")
```

## Exercise

Decode an unknown protocol capture:

```python
# In practice, load a real captured signal
# mystery = tk.load("mystery_uart.wfm")

# Tasks:
# 1. Detect the baud rate
# 2. Try different parity settings
# 3. Successfully decode the message

# from tracekit.inference import detect_baud_rate
# baud = detect_baud_rate(mystery)
# print(f"Detected baud rate: {baud}")

# Try different configurations
# for parity in ["none", "even", "odd"]:
#     decoder = UARTDecoder(baud_rate=baud, parity=parity)
#     try:
#         messages = decoder.decode(mystery)
#         for msg in messages:
#             print(f"[{parity}] {msg.data.decode('utf-8', errors='ignore')}")
#     except:
#         pass

# Your code here...
```

## Next Steps

- [Tutorial 6: Report Generation](06-report-generation.md)

## See Also

- [Protocol Decoders Reference](../reference/protocol-decoders.md)
- [Protocol Inference API](../api/analysis.md#protocol-inference)
- [Troubleshooting Protocol Issues](../guides/troubleshooting.md#protocol-decoding-issues)
