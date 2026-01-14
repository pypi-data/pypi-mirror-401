# Technical Reference

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

Technical reference documentation for TraceKit.

## Reference Documents

| Document                                        | Description                      |
| ----------------------------------------------- | -------------------------------- |
| [Standards Compliance](standards-compliance.md) | IEEE and JEDEC standard coverage |
| [Supported Formats](supported-formats.md)       | File format specifications       |
| [Protocol Decoders](protocol-decoders.md)       | Protocol decoder reference       |

## Standards Compliance

TraceKit implements measurements according to industry standards:

### IEEE Standards

| Standard       | Coverage | Description                                    |
| -------------- | -------- | ---------------------------------------------- |
| IEEE 181-2011  | Full     | Pulse measurements (rise/fall time, overshoot) |
| IEEE 1057-2017 | Partial  | Digitizer characterization                     |
| IEEE 1241-2010 | Full     | ADC testing (SNR, SINAD, ENOB)                 |
| IEEE 2414-2020 | Partial  | Jitter measurements                            |

### JEDEC Standards

| Standard      | Coverage | Description           |
| ------------- | -------- | --------------------- |
| JEDEC JESD65B | Partial  | Timing specifications |

See [Standards Compliance](standards-compliance.md) for detailed coverage.

## Supported File Formats

### Oscilloscope Formats

| Format        | Extension | Vendor    | Status  |
| ------------- | --------- | --------- | ------- |
| Tektronix WFM | `.wfm`    | Tektronix | Full    |
| Rigol WFM     | `.wfm`    | Rigol     | Full    |
| LeCroy TRC    | `.trc`    | LeCroy    | Partial |
| Keysight      | `.bin`    | Keysight  | Planned |

### Logic Analyzer Formats

| Format | Extension    | Source   | Status  |
| ------ | ------------ | -------- | ------- |
| Sigrok | `.sr`        | Sigrok   | Full    |
| VCD    | `.vcd`       | Standard | Full    |
| Saleae | `.logicdata` | Saleae   | Planned |

### Generic Formats

| Format | Extension      | Description              |
| ------ | -------------- | ------------------------ |
| CSV    | `.csv`         | Comma-separated values   |
| NumPy  | `.npz`         | NumPy compressed archive |
| HDF5   | `.h5`, `.hdf5` | Hierarchical data format |
| MATLAB | `.mat`         | MATLAB data file         |
| WAV    | `.wav`         | Audio waveform           |
| JSON   | `.json`        | JSON with base64 data    |

See [Supported Formats](supported-formats.md) for detailed specifications.

## Protocol Decoders

TraceKit includes 16+ protocol decoders:

### Serial Protocols

| Protocol | Class         | Description                 |
| -------- | ------------- | --------------------------- |
| UART     | `UARTDecoder` | Async serial ()             |
| SPI      | `SPIDecoder`  | Serial Peripheral Interface |
| I2C      | `I2CDecoder`  | Inter-Integrated Circuit    |

### Automotive

| Protocol | Class        | Description                |
| -------- | ------------ | -------------------------- |
| CAN      | `CANDecoder` | Controller Area Network    |
| LIN      | `LINDecoder` | Local Interconnect Network |

### Debug Interfaces

| Protocol | Class         | Description             |
| -------- | ------------- | ----------------------- |
| JTAG     | `JTAGDecoder` | Joint Test Action Group |
| SWD      | `SWDDecoder`  | Serial Wire Debug       |

### Other Protocols

| Protocol   | Class               | Description                  |
| ---------- | ------------------- | ---------------------------- |
| 1-Wire     | `OneWireDecoder`    | Dallas 1-Wire                |
| MDIO       | `MDIODecoder`       | Management Data I/O          |
| HDLC       | `HDLCDecoder`       | High-Level Data Link         |
| Manchester | `ManchesterDecoder` | Manchester encoding          |
| Miller     | `MillerDecoder`     | Miller encoding              |
| DMX512     | `DMX512Decoder`     | DMX lighting                 |
| DALI       | `DALIDecoder`       | Digital Addressable Lighting |
| Modbus     | `ModbusDecoder`     | Modbus RTU/ASCII             |
| NMEA       | `NMEADecoder`       | NMEA 0183 GPS                |

See [Protocol Decoders](protocol-decoders.md) for detailed usage.

## Measurement Functions

### Time-Domain

| Function               | IEEE Reference    | Description          |
| ---------------------- | ----------------- | -------------------- |
| `measure_rise_time()`  | IEEE 181-2011 5.2 | 10-90% rise time     |
| `measure_fall_time()`  | IEEE 181-2011 5.2 | 90-10% fall time     |
| `measure_overshoot()`  | IEEE 181-2011 5.4 | Overshoot percentage |
| `measure_frequency()`  | -                 | Signal frequency     |
| `measure_period()`     | -                 | Signal period        |
| `measure_duty_cycle()` | -                 | Duty cycle           |

### Amplitude

| Function              | Description                   |
| --------------------- | ----------------------------- |
| `measure_amplitude()` | Peak-to-peak amplitude        |
| `measure_rms()`       | RMS voltage                   |
| `measure_mean()`      | DC level                      |
| `analyze_amplitude()` | Complete amplitude statistics |

### Spectral

| Function          | IEEE Reference | Description                    |
| ----------------- | -------------- | ------------------------------ |
| `measure_snr()`   | IEEE 1241-2010 | Signal-to-noise ratio          |
| `measure_sinad()` | IEEE 1241-2010 | Signal-to-noise and distortion |
| `measure_thd()`   | -              | Total harmonic distortion      |
| `measure_enob()`  | IEEE 1241-2010 | Effective number of bits       |

### Jitter

| Function                   | IEEE Reference | Description                |
| -------------------------- | -------------- | -------------------------- |
| `measure_period_jitter()`  | IEEE 2414-2020 | Period jitter (RMS, pk-pk) |
| `measure_cycle_to_cycle()` | IEEE 2414-2020 | Cycle-to-cycle jitter      |
| `measure_tie()`            | IEEE 2414-2020 | Time Interval Error        |

## See Also

- [API Reference](../api/index.md) - Complete API documentation
- [User Guide](../user-guide.md) - Usage guide
- [Examples](../examples-reference.md) - Code examples
