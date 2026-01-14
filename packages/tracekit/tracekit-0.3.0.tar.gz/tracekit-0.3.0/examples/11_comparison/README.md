# 11 - Comparison and Limit Testing

This section covers trace comparison and limit testing capabilities.

## Examples

| File                 | Description                | Time   |
| -------------------- | -------------------------- | ------ |
| 01_compare_traces.py | Compare two traces         | 15 min |
| 02_golden_ref.py     | Golden waveform comparison | 15 min |
| 03_limits.py         | Limit and mask testing     | 20 min |

## Key Concepts

- **Trace comparison**: Quantify similarity between signals
- **Golden reference**: Compare against known-good waveform
- **Limit testing**: Check if signal stays within bounds
- **Mask testing**: Pass/fail against eye mask or custom shape

## Comparison Functions

| Function            | Description                   |
| ------------------- | ----------------------------- |
| compare_traces()    | Point-by-point comparison     |
| correlation()       | Cross-correlation coefficient |
| difference()        | Compute trace difference      |
| similarity_score()  | Overall similarity metric     |
| compare_to_golden() | Test against reference        |
| check_limits()      | Upper/lower limit testing     |
| mask_test()         | Geometric mask testing        |

## Use Cases

1. **Regression testing**: Verify firmware updates don't change behavior
2. **Production testing**: Compare against golden reference
3. **Compliance**: Test against specification limits
4. **Signal integrity**: Eye diagram mask testing

## Prerequisites

- 01_basics section completed

## Running Examples

```bash
uv run python examples/11_comparison/01_compare_traces.py
```
