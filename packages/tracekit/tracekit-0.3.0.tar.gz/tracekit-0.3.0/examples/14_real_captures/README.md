# Real Captures Examples

This directory contains examples for working with real oscilloscope captures.

## Prerequisites

Before running these examples, populate the real captures directory:

```bash
python scripts/prepare_real_captures.py /path/to/minimal_testset
```

This will:

- Copy real Tektronix WFM files organized by size
- Copy session (.tss) and settings (.set) files
- Extract UDP packet subsets from large captures

## Examples

| File                 | Description                        | Estimated Time |
| -------------------- | ---------------------------------- | -------------- |
| `01_wfm_analysis.py` | Load and analyze real WFM captures | 2-3 min        |

## Data Location

Real captures are stored in `test_data/real_captures/`:

```
test_data/real_captures/
  manifest.json           # File inventory with checksums
  waveforms/
    small/                # < 1.5 MB files
    medium/               # 1.5 - 6 MB files
    large/                # > 6 MB files
  sessions/               # Tektronix session files
  settings/               # Tektronix settings files
  packets/                # UDP packet segments
```

## Why Real Captures?

Real captures provide:

1. **Validation**: Ensure algorithms work on production data, not just synthetic test cases
2. **Edge Cases**: Real signals have noise, artifacts, and variations not present in synthetic data
3. **Performance Testing**: Benchmark with realistic file sizes and data patterns
4. **Demonstration**: Show the library working with actual oscilloscope output

## Running Examples

```bash
# Run a specific example
uv run python examples/07_real_captures/01_wfm_analysis.py

# Or run all examples
uv run python examples/run_all_examples.py
```
