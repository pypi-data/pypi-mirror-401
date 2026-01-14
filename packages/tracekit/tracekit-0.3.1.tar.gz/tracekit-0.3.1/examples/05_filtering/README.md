# 05 - Signal Filtering

This section covers TraceKit's comprehensive filtering capabilities for signal conditioning.

## Examples

| File                | Description               | Time   |
| ------------------- | ------------------------- | ------ |
| 01_low_pass.py      | Low-pass filtering basics | 10 min |
| 02_high_pass.py     | High-pass and DC removal  | 10 min |
| 03_band_filters.py  | Band-pass and band-stop   | 15 min |
| 04_convenience.py   | Quick filtering functions | 10 min |
| 05_custom_design.py | Custom filter design      | 20 min |

## Key Concepts

- **IIR vs FIR filters**: Trade-offs between computational cost and phase response
- **Filter types**: Butterworth, Chebyshev, Bessel, Elliptic
- **Filter response**: Cutoff frequency, order, ripple, rolloff
- **Phase considerations**: Linear phase (FIR) vs minimum phase (IIR)

## Filter Types Available

| Filter       | Best For                            |
| ------------ | ----------------------------------- |
| Butterworth  | Flat passband, general purpose      |
| Chebyshev I  | Sharp rolloff, ripple in passband   |
| Chebyshev II | Sharp rolloff, ripple in stopband   |
| Bessel       | Constant group delay, pulse signals |
| Elliptic     | Sharpest rolloff, ripple both bands |

## Prerequisites

- 01_basics section completed
- Basic understanding of frequency domain

## Running Examples

```bash
uv run python examples/05_filtering/01_low_pass.py
```
