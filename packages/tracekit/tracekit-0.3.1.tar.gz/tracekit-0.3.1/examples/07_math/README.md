# 07 - Math Operations

This section covers mathematical operations on waveform traces.

## Examples

| File                | Description                     | Time   |
| ------------------- | ------------------------------- | ------ |
| 01_arithmetic.py    | Add, subtract, multiply, divide | 10 min |
| 02_calculus.py      | Differentiate and integrate     | 15 min |
| 03_scaling.py       | Scale, offset, invert, absolute | 10 min |
| 04_interpolation.py | Resample, interpolate, align    | 15 min |

## Key Concepts

- **Arithmetic operations**: Combine traces mathematically
- **Calculus**: Compute derivatives and integrals
- **Scaling**: Adjust amplitude and offset
- **Resampling**: Change sample rate, align time bases

## Common Use Cases

| Operation       | Use Case                              |
| --------------- | ------------------------------------- |
| add()           | Combine signals, average measurements |
| subtract()      | Remove baseline, compute difference   |
| multiply()      | Power calculation (V x I), modulation |
| divide()        | Impedance (V/I), gain measurement     |
| differentiate() | Slew rate, edge detection             |
| integrate()     | Charge, energy, area under curve      |
| resample()      | Match sample rates, reduce data       |
| align_traces()  | Time-align multi-channel data         |

## Prerequisites

- 01_basics section completed

## Running Examples

```bash
uv run python examples/07_math/01_arithmetic.py
```
