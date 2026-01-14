# 09 - Power Analysis

This section covers power measurement and analysis capabilities in TraceKit.

## Examples

| File              | Description                        | Time   |
| ----------------- | ---------------------------------- | ------ |
| 01_basic_power.py | Instantaneous and average power    | 15 min |
| 02_ac_power.py    | AC power, power factor, reactive   | 20 min |
| 03_efficiency.py  | Efficiency calculations            | 15 min |
| 04_ripple.py      | Ripple analysis for power supplies | 15 min |

## Key Concepts

- **Instantaneous power**: P(t) = V(t) x I(t)
- **Average power**: Mean of instantaneous power
- **Power factor**: Real power / Apparent power
- **Reactive power**: Power stored/returned by reactive components
- **Ripple**: AC component on DC power supply output

## Power Measurements

| Measurement   | Function              | Description                 |
| ------------- | --------------------- | --------------------------- |
| Instantaneous | instantaneous_power() | P = V x I at each sample    |
| Average       | average_power()       | Mean power over time        |
| Energy        | energy()              | Integral of power           |
| Power Factor  | power_factor()        | cos(phi) for AC             |
| Apparent      | apparent_power()      | V_rms x I_rms               |
| Reactive      | reactive_power()      | VAR (volt-amperes reactive) |
| Ripple        | ripple()              | AC component on DC          |
| Efficiency    | efficiency()          | P_out / P_in                |

## Prerequisites

- 01_basics section completed
- Understanding of AC/DC power concepts

## Running Examples

```bash
uv run python examples/09_power/01_basic_power.py
```
