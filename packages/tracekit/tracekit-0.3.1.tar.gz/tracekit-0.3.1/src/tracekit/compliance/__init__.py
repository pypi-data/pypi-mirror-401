"""EMC/EMI compliance testing module.

This module provides regulatory compliance testing capabilities including
limit masks, compliance testing, and report generation for FCC, CE/CISPR,
and MIL-STD standards.


Example:
    >>> import tracekit as tk
    >>> from tracekit.compliance import load_limit_mask, check_compliance, generate_compliance_report
    >>>
    >>> trace = tk.load('emissions.wfm')
    >>> mask = load_limit_mask('FCC_Part15_ClassB')
    >>> result = check_compliance(trace, mask)
    >>> generate_compliance_report(result, 'compliance_report.html')
"""

from tracekit.compliance.advanced import (
    ComplianceTestConfig,
    ComplianceTestRunner,
    ComplianceTestSuite,
    InterpolationMethod,
    LimitInterpolator,
    QPDetectorBand,
    QPDetectorParams,
    QuasiPeakDetector,
    interpolate_limit,
)
from tracekit.compliance.masks import (
    AVAILABLE_MASKS,
    LimitMask,
    create_custom_mask,
    load_limit_mask,
)
from tracekit.compliance.reporting import (
    ComplianceReportFormat,
    generate_compliance_report,
)
from tracekit.compliance.testing import (
    ComplianceResult,
    ComplianceViolation,
    DetectorType,
    check_compliance,
)

__all__ = [
    # Masks (EMC-001)
    "AVAILABLE_MASKS",
    "ComplianceReportFormat",
    "ComplianceResult",
    # Advanced Compliance (COMP-005, 006, 007)
    "ComplianceTestConfig",
    "ComplianceTestRunner",
    "ComplianceTestSuite",
    "ComplianceViolation",
    "DetectorType",
    "InterpolationMethod",
    "LimitInterpolator",
    "LimitMask",
    "QPDetectorBand",
    "QPDetectorParams",
    "QuasiPeakDetector",
    # Testing (EMC-002)
    "check_compliance",
    "create_custom_mask",
    # Reporting (EMC-003)
    "generate_compliance_report",
    "interpolate_limit",
    "load_limit_mask",
]
