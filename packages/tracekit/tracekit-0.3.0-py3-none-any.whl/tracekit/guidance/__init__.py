"""TraceKit guidance module.

Provides guided analysis workflows and recommendations.
"""

from tracekit.guidance.recommender import (
    AnalysisHistory,
    Recommendation,
    suggest_next_steps,
)
from tracekit.guidance.wizard import (
    AnalysisWizard,
    WizardResult,
    WizardStep,
)

__all__ = [
    "AnalysisHistory",
    "AnalysisWizard",
    "Recommendation",
    "WizardResult",
    "WizardStep",
    "suggest_next_steps",
]
