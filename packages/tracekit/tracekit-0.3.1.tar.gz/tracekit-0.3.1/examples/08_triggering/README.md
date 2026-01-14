# 08 - Triggering and Event Detection

This section covers TraceKit's triggering and event detection capabilities.

## Examples

| File                | Description                  | Time   |
| ------------------- | ---------------------------- | ------ |
| 01_edge_trigger.py  | Edge-based triggering        | 15 min |
| 02_pulse_trigger.py | Pulse width triggering       | 15 min |
| 03_pattern.py       | Pattern and glitch detection | 15 min |

## Key Concepts

- **Edge trigger**: Detect rising/falling signal transitions
- **Pulse trigger**: Find pulses of specific width
- **Glitch detection**: Find abnormally short pulses
- **Runt detection**: Find pulses that don't reach threshold

## Trigger Types

| Trigger      | Function             | Use Case             |
| ------------ | -------------------- | -------------------- |
| Rising Edge  | find_rising_edges()  | Clock, data edges    |
| Falling Edge | find_falling_edges() | Clock, reset signals |
| Pulse Width  | find_pulses()        | Data bit timing      |
| Glitch       | find_glitches()      | Noise spikes         |
| Runt         | find_runt_pulses()   | Signal integrity     |
| Pattern      | EdgeTrigger          | Complex conditions   |

## Prerequisites

- 01_basics section completed
- 02_digital_analysis section helpful

## Running Examples

```bash
uv run python examples/08_triggering/01_edge_trigger.py
```
