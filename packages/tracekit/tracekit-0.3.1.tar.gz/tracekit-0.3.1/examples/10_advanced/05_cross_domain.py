#!/usr/bin/env python3
"""Example demonstrating cross-domain correlation.

This example shows how to use the cross-domain correlation module to find
relationships between analysis results from different domains and improve
overall confidence in the results.

Usage:
    uv run python examples/cross_domain_correlation_example.py
"""

from tracekit.core.cross_domain import correlate_results
from tracekit.reporting.config import AnalysisDomain


def main() -> None:
    """Demonstrate cross-domain correlation."""
    print("=" * 70)
    print("Cross-Domain Correlation Example")
    print("=" * 70)

    # Example 1: Frequency-Timing Correlation
    print("\nExample 1: Frequency-Timing Agreement")
    print("-" * 70)

    results = {
        AnalysisDomain.SPECTRAL: {
            "dominant_frequency": 1000.0,  # 1 kHz
            "peak_power": -3.0,
        },
        AnalysisDomain.TIMING: {
            "period": 0.001,  # 1 ms = 1 kHz
            "avg_period": 0.001,
        },
    }

    correlation = correlate_results(results)

    print(f"Insights found: {len(correlation.insights)}")
    print(f"Agreements: {correlation.agreements_detected}")
    print(f"Conflicts: {correlation.conflicts_detected}")
    print(f"Overall coherence: {correlation.overall_coherence:.2f}")

    for insight in correlation.insights:
        print(f"\n  {insight.insight_type.upper()}: {insight.description}")
        print(f"  Confidence impact: {insight.confidence_impact:+.2f}")

    if correlation.confidence_adjustments:
        print("\n  Confidence adjustments:")
        for domain, adjustment in correlation.confidence_adjustments.items():
            print(f"    {domain}: {adjustment:+.2f}")

    # Example 2: Conflict Detection
    print("\n\nExample 2: Frequency-Timing Conflict")
    print("-" * 70)

    results = {
        AnalysisDomain.SPECTRAL: {
            "dominant_frequency": 1000.0,  # 1 kHz
        },
        AnalysisDomain.TIMING: {
            "period": 0.01,  # 10 ms = 100 Hz (MISMATCH!)
        },
    }

    correlation = correlate_results(results)

    print(f"Insights found: {len(correlation.insights)}")
    print(f"Conflicts: {correlation.conflicts_detected}")
    print(f"Overall coherence: {correlation.overall_coherence:.2f}")

    for insight in correlation.insights:
        print(f"\n  {insight.insight_type.upper()}: {insight.description}")
        print(f"  Confidence impact: {insight.confidence_impact:+.2f}")
        print(f"  Details: {insight.details}")

    # Example 3: Multi-Domain Analysis
    print("\n\nExample 3: Multi-Domain Correlation")
    print("-" * 70)

    results = {
        AnalysisDomain.SPECTRAL: {
            "dominant_frequency": 1000.0,
        },
        AnalysisDomain.TIMING: {
            "period": 0.001,
        },
        AnalysisDomain.DIGITAL: {
            "edge_count": 2000,
        },
        AnalysisDomain.WAVEFORM: {
            "amplitude": 5.66,  # 2.83 * 2 for better signal
        },
        AnalysisDomain.STATISTICS: {
            "std": 2.0,
        },
    }

    correlation = correlate_results(results)

    print(f"Total insights: {len(correlation.insights)}")
    print(f"Agreements: {correlation.agreements_detected}")
    print(f"Overall coherence: {correlation.overall_coherence:.2f}")

    print("\nInsights:")
    for i, insight in enumerate(correlation.insights, 1):
        domains = " <-> ".join([d.value for d in insight.source_domains])
        print(f"  {i}. [{domains}] {insight.insight_type}: {insight.description}")

    print("\nConfidence adjustments:")
    for domain, adjustment in sorted(correlation.confidence_adjustments.items()):
        indicator = "[+]" if adjustment > 0 else "[-]" if adjustment < 0 else "[ ]"
        print(f"  {indicator} {domain}: {adjustment:+.2f}")

    print("\n" + "=" * 70)
    print("Example complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
