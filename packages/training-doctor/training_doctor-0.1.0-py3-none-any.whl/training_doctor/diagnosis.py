from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional


class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Evidence:
    """A single piece of evidence supporting a diagnosis."""
    metric: str
    observation: str
    value: Optional[float] = None
    step: Optional[int] = None

    def __str__(self) -> str:
        parts = [f"{self.metric}: {self.observation}"]
        if self.value is not None:
            parts.append(f"(value={self.value:.4g})")
        if self.step is not None:
            parts.append(f"at step {self.step}")
        return " ".join(parts)


@dataclass
class Diagnosis:
    """A diagnosis representing a detected training issue."""
    problem: str
    explanation: str
    evidence: List[Evidence]
    suggestions: List[str]
    confidence: float
    severity: Severity
    detector_name: str = ""
    step: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        severity_icons = {
            Severity.INFO: "INFO",
            Severity.WARNING: "WARNING",
            Severity.CRITICAL: "CRITICAL"
        }
        icon = severity_icons.get(self.severity, "")

        lines = [
            f"{icon} {self.problem}",
            f"{self.explanation}",
            "",
            "Evidence:",
        ]
        for e in self.evidence:
            lines.append(f"  - {e}")

        lines.append("")
        lines.append("Suggested actions:")
        for s in self.suggestions:
            lines.append(f"  - {s}")

        lines.append("")
        lines.append(f"Confidence: {self.confidence:.2f}")

        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """Convert diagnosis to dictionary for JSON serialization."""
        return {
            "problem": self.problem,
            "explanation": self.explanation,
            "evidence": [
                {
                    "metric": e.metric,
                    "observation": e.observation,
                    "value": e.value,
                    "step": e.step,
                }
                for e in self.evidence
            ],
            "suggestions": self.suggestions,
            "confidence": self.confidence,
            "severity": self.severity.value,
            "detector_name": self.detector_name,
            "step": self.step,
            "metadata": self.metadata,
        }
