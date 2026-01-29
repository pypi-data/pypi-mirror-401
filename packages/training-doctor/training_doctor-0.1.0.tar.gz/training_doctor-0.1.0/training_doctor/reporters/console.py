from typing import List, TextIO
import sys

from ..diagnosis import Diagnosis, Severity


class ConsoleReporter:
    """Reporter that outputs diagnoses to the console."""

    SEVERITY_COLORS = {
        Severity.INFO: "\033[94m",      # Blue
        Severity.WARNING: "\033[93m",   # Yellow
        Severity.CRITICAL: "\033[91m",  # Red
    }
    RESET = "\033[0m"
    BOLD = "\033[1m"

    def __init__(self, stream: TextIO = None, use_color: bool = True):
        """Initialize the console reporter.

        Args:
            stream: Output stream (defaults to sys.stderr).
            use_color: Whether to use ANSI color codes.
        """
        self.stream = stream or sys.stderr
        self.use_color = use_color and self.stream.isatty()

    def _colorize(self, text: str, severity: Severity) -> str:
        """Add color codes to text based on severity."""
        if not self.use_color:
            return text
        color = self.SEVERITY_COLORS.get(severity, "")
        return f"{color}{text}{self.RESET}"

    def _bold(self, text: str) -> str:
        """Make text bold."""
        if not self.use_color:
            return text
        return f"{self.BOLD}{text}{self.RESET}"

    def report(self, diagnosis: Diagnosis) -> None:
        """Print a single diagnosis to the console."""
        severity_label = diagnosis.severity.value.upper()
        header = f"[{severity_label}] {diagnosis.problem}"
        header = self._colorize(header, diagnosis.severity)

        lines = [
            "",
            self._bold(header),
            diagnosis.explanation,
            "",
            "Evidence:",
        ]

        for evidence in diagnosis.evidence:
            lines.append(f"  - {evidence}")

        lines.append("")
        lines.append("Suggested actions:")
        for suggestion in diagnosis.suggestions:
            lines.append(f"  - {suggestion}")

        lines.append("")
        confidence_str = f"Confidence: {diagnosis.confidence:.0%}"
        if diagnosis.step is not None:
            confidence_str += f" | Step: {diagnosis.step}"
        lines.append(confidence_str)
        lines.append("")

        output = "\n".join(lines)
        print(output, file=self.stream)

    def report_all(self, diagnoses: List[Diagnosis]) -> None:
        """Print multiple diagnoses."""
        if not diagnoses:
            return

        for diagnosis in diagnoses:
            self.report(diagnosis)

    def report_summary(self, diagnoses: List[Diagnosis]) -> None:
        """Print a summary of all diagnoses."""
        if not diagnoses:
            print("No issues detected.", file=self.stream)
            return

        critical = sum(1 for d in diagnoses if d.severity == Severity.CRITICAL)
        warning = sum(1 for d in diagnoses if d.severity == Severity.WARNING)
        info = sum(1 for d in diagnoses if d.severity == Severity.INFO)

        summary = f"\nDiagnosis Summary: {critical} critical, {warning} warnings, {info} info"
        print(self._bold(summary), file=self.stream)
