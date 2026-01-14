# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 0.1.x   | Yes       |
| < 0.1   | No        |

---

## Reporting a Vulnerability

**We take security seriously.** If you discover a security vulnerability, please report it responsibly.

### How to Report

**Preferred**: [Private security advisory](https://github.com/lair-click-bats/tracekit/security/advisories/new) on GitHub

**Alternative**: Email security@lair-click-bats.dev

**Do not** report vulnerabilities through public issues unless already disclosed.

### What to Include

- Type of vulnerability
- Affected source fil es and locations
- Step-by-step reproduction
- Impact assessment
- Proof-of-concept (if available)
- Suggested fi x (if you have one)

### Response Timeline

- **Initial response**: Within 48 hours
- **Severity assessment**: Within 7 days
- **Patch release**: Depends on severity
  - Critical: 7 days
  - High: 14 days
  - Medium: 30 days
  - Low: 60 days
- **Public disclosure**: After patch release

---

## Security Measures

TraceKit implements the following security practices:

### Code Security

- Static analysis with `bandit` for Python security issues
- Dependency vulnerability scanning with `safety`
- No execution of untrusted code from input files
- Input validation for all file loaders

### CI/CD Security

- Automated security scanning in CI pipeline
- Dependency updates monitored
- No secrets in repository

### Data Handling

- File loaders validate format before parsing
- Memory limits enforced for large file processing
- No network operations in core library

---

## Threat Model

### Untrusted Inputs

TraceKit treats the following as untrusted:

- User-provided waveform files (may contain malformed data)
- User-provided file paths (path traversal risk)
- Protocol definitions (pattern matching only, no code execution)
- CSV/binary data imports

### Attack Vectors

1. **Malformed files**: Buffer overflows, memory exhaustion
2. **Path traversal**: Unsanitized file paths
3. **DoS**: Large files, complex patterns, memory exhaustion
4. **Dependency vulnerabilities**: Third-party package issues

---

## Security Best Practices

### For Users

**1. Validate inputs:**

```python
from pathlib import Path

# Good: Validate paths
if not Path(user_path).resolve().is_relative_to(safe_dir):
    raise ValueError("Path outside safe directory")

# Bad: Trust user input
loader.load(user_input_path)  # Don't do this without validation
```

**2. Set memory limits for large files:**

```python
from tracekit.loaders import load_with_limits

# Set maximum file size and sample count
trace = load_with_limits(
    filepath,
    max_file_size_mb=100,
    max_samples=10_000_000
)
```

**3. Run vulnerability scans:**

```bash
uv pip install safety pip-audit
safety check
pip-audit
```

### For Deployment

**Production checklist:**

- [ ] Validate all user-provided file paths
- [ ] Set file size limits for uploads
- [ ] Run vulnerability scans: `safety check`
- [ ] Keep dependencies updated: `uv pip install --upgrade tracekit`
- [ ] Use principle of least privilege for file system access
- [ ] Monitor memory usage during batch processing

**Docker example:**

```dockerfile
FROM python:3.12-slim
RUN uv pip install tracekit
USER nonroot  # Don't run as root
COPY --chown=nonroot:nonroot . /app
WORKDIR /app
```

---

## Dependency Security

### Automated Scanning

TraceKit uses:

- **Dependabot**: Automatic dependency updates (when enabled)
- **CI scanning**: Vulnerability monitoring in CI pipeline

### Manual Scanning

Check your installation:

```bash
uv pip install safety pip-audit
safety check
pip-audit
```

---

## Known Limitations

### Binary File Parsing

- **Risk**: Malformed binary files may cause excessive memory usage
- **Mitigation**: Use with trusted data sources or implement memory limits
- **User action**: Set `max_samples` and `max_file_size_mb` parameters

### Protocol Decoders

- **Risk**: Complex patterns may cause CPU exhaustion
- **Mitigation**: Pattern matching only, not arbitrary code execution
- **User action**: Set timeout limits for decoding operations

### Large File Processing

- **Risk**: Processing very large files may exhaust memory
- **Mitigation**: Use chunked processing APIs
- **User action**: Use streaming/chunked APIs for files >100MB

---

## Out of Scope

The following are **not** security vulnerabilities in TraceKit:

### 1. Resource Usage with Large Files

Processing large waveform files (>1GB) is **resource-intensive by design**, not a vulnerability.

**User's responsibility**: Set reasonable limits in your application
**TraceKit provides**: Chunked processing and streaming APIs

### 2. Invalid Measurement Results

Incorrect measurements from malformed input data is a **data quality issue**, not a security vulnerability.

**User's responsibility**: Validate input data quality
**TraceKit provides**: Data validation utilities

---

## Disclosure Policy

- We follow **coordinated disclosure**
- Security fixes are released ASAP
- CVEs assigned when applicable
- Public disclosure after patch + reasonable upgrade time
- Credits given to researchers who report responsibly

---

## Security Contact

- **GitHub Security Advisories**: [Create advisory](https://github.com/lair-click-bats/tracekit/security/advisories/new)
- **Email**: security@lair-click-bats.dev
- **Issues**: Use "security" label for non-sensitive issues

---

## Security Updates

Security updates are released as patch versions and announced in:

- GitHub Security Advisories
- CHANGELOG.md

Subscribe to repository notifications for security alerts.
