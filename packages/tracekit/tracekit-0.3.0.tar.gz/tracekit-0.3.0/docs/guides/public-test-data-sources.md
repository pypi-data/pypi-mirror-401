# Public Test Data Sources

> **Version**: 0.1.0 | **Last Updated**: 2026-01-08

## Overview

This guide lists public, legally safe sources of oscilloscope waveform data that can be used with TraceKit for testing and validation.

## Recommended Approach

**Primary Recommendation**: Use [synthetic test data](synthetic-test-data.md) generated with `scripts/generate_synthetic_wfm.py` for:

- Legal safety
- Reproducibility
- Version control
- Complete control over test scenarios

**Supplementary**: Use public data sources below for additional validation and real-world testing.

## Official Tektronix Sources

### tm_data_types Library

- **Source**: https://github.com/tektronix/tm_data_types
- **License**: Apache 2.0
- **Status**: ✓ Safe
- **Format**: WFM, BIN, CSV

The official Tektronix library may include sample files in its test suite or documentation.

**Installation**:

```bash
pip install tm_data_types
```

**Check for samples**:

```bash
# Find sample files in package
python -c "import tm_data_types; import os; print(os.path.dirname(tm_data_types.__file__))"
find $(python -c "import tm_data_types; import os; print(os.path.dirname(tm_data_types.__file__))") -name "*.wfm"
```

### Tektronix Support Resources

- **Website**: https://www.tek.com/
- **Support**: https://www.tek.com/en/support
- **Downloads**: https://www.tek.com/en/support/software

Check for:

- Sample waveform files in driver packages
- SDK example data
- Application notes with sample files
- Tutorial datasets

**Note**: Always verify licensing terms before distribution.

### Tektronix Documentation

Official WFM format documentation:

- **Format Spec**: https://download.tek.com/manual/Waveform-File-Format-Manual-077022011.pdf
- **Reference Manual**: https://download.tek.com/manual/077022005Web_1.pdf

These may include small example files in appendices.

## Community Resources

### GitHub Repositories

#### WFM Reader Projects

1. **libtekwfm3**
   - URL: https://github.com/nosoxon/libtekwfm3
   - License: Check repository
   - Format: WFM v3
   - May include test files

2. **TekWFM2**
   - URL: https://github.com/vongostev/TekWFM2
   - License: Check repository
   - Format: WFM v1 & v2
   - May include sample files

3. **tektronix_wfmreader**
   - URL: https://github.com/MorganAskins/tektronix_wfmreader
   - License: Check repository
   - Format: Various WFM versions

**Note**: Always check and respect repository licenses before using files.

### Open Science Repositories

#### IEEE DataPort

- **URL**: https://ieee-dataport.org/
- **License**: Varies by dataset
- **Search**: "oscilloscope" OR "waveform" OR "signal capture"

Example datasets:

- Signal processing benchmarks
- Communication system captures
- Power electronics measurements

**Always check individual dataset licenses**.

#### Zenodo

- **URL**: https://zenodo.org/
- **License**: Varies by dataset
- **Search**: "oscilloscope waveform" OR "tektronix data"

Research datasets uploaded by academics, often with permissive licenses.

#### Figshare

- **URL**: https://figshare.com/
- **License**: Varies by dataset
- **Search**: "oscilloscope" OR "waveform measurement"

Academic data sharing platform with various oscilloscope datasets.

## Academic Datasets

### Signal Processing Benchmarks

Common signal processing test datasets:

1. **ECG/Biomedical Signals**
   - PhysioNet (https://physionet.org/)
   - License: Various, mostly permissive
   - Format: Multiple (may need conversion)

2. **Audio Signals**
   - Freesound (https://freesound.org/)
   - License: Creative Commons
   - Format: WAV (convertible to WFM)

3. **Communication Signals**
   - GNU Radio datasets
   - RF capture repositories

### University Repositories

Check university research data repositories:

- MIT DSpace
- Stanford Digital Repository
- UC Berkeley DASH
- ETH Zurich Research Collection

Search for: "oscilloscope", "waveform", "signal measurement"

## Format Conversion

If you find suitable data in other formats:

### WAV to WFM

TraceKit can load WAV files directly, or convert to WFM:

```python
from tracekit.loaders.wav import load_wav
from tm_data_types import AnalogWaveform, RawSample, write_file
import numpy as np

# Load WAV
trace = load_wav("signal.wav")

# Convert to WFM
wf = AnalogWaveform()
wf.source_name = "WAV_IMPORT"

# Convert to 16-bit integer
y_int16 = (trace.data * 32767).astype(np.int16)
wf.y_axis_values = RawSample[np.int16](y_int16)

wf.x_axis_spacing = 1.0 / trace.metadata.sample_rate
wf.x_axis_units = "s"
wf.y_axis_units = "V"
wf.y_axis_offset = 0.0
wf.y_axis_spacing = 1.0 / 32767

write_file("signal.wfm", wf)
```

### CSV to WFM

Convert CSV data to WFM:

```python
import numpy as np
from tm_data_types import AnalogWaveform, RawSample, write_file

# Load CSV (time, voltage columns)
data = np.loadtxt("signal.csv", delimiter=",", skiprows=1)
t = data[:, 0]
y = data[:, 1]

# Calculate sample rate
dt = np.mean(np.diff(t))
sample_rate = 1.0 / dt

# Create WFM
wf = AnalogWaveform()
wf.source_name = "CSV_IMPORT"

# Convert to 16-bit
y_min, y_max = y.min(), y.max()
y_normalized = (y - y_min) / (y_max - y_min)
y_int16 = (y_normalized * 65535 - 32768).astype(np.int16)

wf.y_axis_values = RawSample[np.int16](y_int16)
wf.x_axis_spacing = dt
wf.x_axis_units = "s"
wf.y_axis_units = "V"
wf.y_axis_offset = y_min
wf.y_axis_spacing = (y_max - y_min) / 65535

write_file("signal.wfm", wf)
```

### TDMS to WFM

TraceKit supports TDMS directly, or convert to WFM:

```python
from tracekit.loaders.tdms import load_tdms
# Similar conversion process as above
```

## Licensing Considerations

### Safe Licenses

These licenses are generally safe for test data:

- **Public Domain** / CC0
- **MIT License**
- **Apache 2.0**
- **BSD Licenses**
- **Creative Commons Attribution (CC BY)**

### Licenses Requiring Consideration

These may have restrictions:

- **CC BY-SA**: Share-alike requirement
- **CC BY-NC**: Non-commercial only
- **GPL**: May require derivative work to be GPL
- **Custom licenses**: Review carefully

### Avoid

- **All Rights Reserved**: Cannot redistribute
- **Proprietary**: Legal issues
- **Unclear/No License**: Assume restricted

## Best Practices

### Before Using External Data

1. **Verify license**: Check and document licensing terms
2. **Check provenance**: Ensure legitimate source
3. **Test compatibility**: Verify format works with TraceKit
4. **Document source**: Record where data came from
5. **Archive license**: Keep copy of license terms

### In Your Project

```markdown
# test_data/public/README.md

## Public Test Data Sources

### file1.wfm

- Source: IEEE DataPort Dataset #12345
- License: CC BY 4.0
- URL: https://ieee-dataport.org/datasets/12345
- Downloaded: 2025-12-24
- Purpose: Real-world signal validation

### file2.wfm

- Source: Tektronix tm_data_types examples
- License: Apache 2.0
- URL: https://github.com/tektronix/tm_data_types
- Purpose: Format compatibility testing
```

### Attribution

If required by license:

```python
# tests/test_real_data.py
"""
Tests using public domain datasets.

Data sources:
- sine_real.wfm: From IEEE DataPort #12345 (CC BY 4.0)
  https://ieee-dataport.org/datasets/12345
"""
```

## Creating Your Own Public Dataset

### Why Share?

Benefits of publishing your own test dataset:

1. **Community contribution**: Help other developers
2. **Citation**: Academic credit for dataset creation
3. **Validation**: Others can verify your work
4. **Standard**: Become reference implementation

### How to Share

#### 1. Choose Repository

- **Zenodo**: DOI assignment, long-term preservation
- **IEEE DataPort**: Technical community
- **Figshare**: Academic sharing
- **GitHub**: Code integration (small files only)

#### 2. Select License

Recommended for test data:

- **CC0** (Public Domain): Maximum reusability
- **CC BY 4.0**: Require attribution
- **MIT**: Simple permissive license

#### 3. Document Thoroughly

Include:

- File format specifications
- Generation methodology
- Intended use cases
- Known limitations
- Contact information

#### 4. Example Publication

````markdown
# Synthetic Oscilloscope Test Dataset

## Description

Comprehensive synthetic waveform dataset for oscilloscope software testing.

## Contents

- 29 WFM files covering basic and advanced signal types
- File sizes from 1 KB to 2 MB
- Frequencies from 10 Hz to 100 kHz

## Format

Tektronix WFM#003 format, compatible with tm_data_types library.

## Generation

All files generated using scripts/generate_synthetic_wfm.py:

```bash
python scripts/generate_synthetic_wfm.py --generate-suite
```
````

## License

CC0 1.0 Universal (Public Domain)

## Citation

If you use this dataset, please cite:
[Author]. (2025). Synthetic Oscilloscope Test Dataset. Zenodo. DOI:10.5281/zenodo.XXXXXX

## Recommended Strategy

### Tiered Approach

1. **Primary**: Synthetic data (your own generation)
   - Legally safe
   - Fully controlled
   - Version controlled

2. **Secondary**: Official Tektronix samples
   - Format reference
   - Compatibility validation

3. **Tertiary**: Public repositories
   - Real-world validation
   - Edge case discovery
   - Specific domain testing

### Repository Organization

```
test_data/
├── README.md           # Strategy overview
├── synthetic/          # Your generated data (primary)
│   ├── basic/
│   ├── edge_cases/
│   └── advanced/
├── public/             # External public data (secondary)
│   ├── README.md       # Sources and licenses
│   ├── tektronix_samples/
│   └── ieee_dataport/
└── .gitignore          # Exclude large/private files
```

## Legal Disclaimer

**Important**: This guide provides general information only. Always:

1. Read and understand specific license terms
2. Consult legal counsel if uncertain
3. Document all data sources and licenses
4. Respect intellectual property rights
5. When in doubt, use synthetic data

## Summary

| Source                   | Legal Safety  | Availability | Coverage     | Recommendation |
| ------------------------ | ------------- | ------------ | ------------ | -------------- |
| **Synthetic (your own)** | ✓✓✓ Excellent | ✓✓✓ Always   | ✓✓✓ Complete | **PRIMARY**    |
| **Tektronix official**   | ✓✓ Good       | ✓ Sometimes  | ✓ Limited    | Secondary      |
| **Public repositories**  | ✓ Varies      | ✓✓ Often     | ✓✓ Varied    | Tertiary       |
| **Community projects**   | ⚠ Check       | ✓✓ Often     | ⚠ Varies     | Verify first   |
| **Proprietary**          | ✗ Avoid       | ✗ Restricted | ✗ N/A        | **DO NOT USE** |

## Support

For questions about test data sources:

1. Review [Test Data Strategy](../getting-started.md#prerequisites)
2. Check [Synthetic Data Guide](synthetic-test-data.md)
3. Consult [Migration Guide](test-data-migration.md)
4. File issue on GitHub

## References

- **tm_data_types**: https://github.com/tektronix/tm_data_types
- **Tektronix**: https://www.tek.com/
- **IEEE DataPort**: https://ieee-dataport.org/
- **Zenodo**: https://zenodo.org/
- **Creative Commons**: https://creativecommons.org/licenses/
