import math
from typing import Optional, List

from ..diagnosis import Diagnosis, Evidence, Severity
from ..metrics.store import MetricStore
from .base import BaseDetector


class GradientInstabilityDetector(BaseDetector):
    """Detects gradient-related instabilities: NaN, explosion, vanishing."""

    name = "gradient_instability"
    description = "Detects NaN gradients, gradient explosion, or vanishing gradients"
    min_data_points = 20
    cooldown_steps = 100

    def __init__(
        self,
        explosion_threshold: float = 10.0,  # Lowered from 100 to catch spikes
        vanishing_threshold: float = 0.01,  # Raised from 1e-7 to catch gradual vanishing
        check_window: int = 100,  # Increased to catch intermittent issues
        spike_std_threshold: float = 3.0,  # For detecting relative spikes
    ):
        """Initialize gradient instability detector.

        Args:
            explosion_threshold: Gradient norm above this is considered exploding.
            vanishing_threshold: Gradient norm below this is considered vanishing.
            check_window: Number of steps to check.
            spike_std_threshold: Std deviations above mean to consider a spike.
        """
        super().__init__()
        self.explosion_threshold = explosion_threshold
        self.vanishing_threshold = vanishing_threshold
        self.check_window = check_window
        self.spike_std_threshold = spike_std_threshold

    @property
    def required_metrics(self) -> List[str]:
        return ["grad_norm"]

    def detect(self, store: MetricStore) -> Optional[Diagnosis]:
        evidence = []
        confidence = 0.0
        severity = Severity.WARNING

        # Check for NaN/Inf gradients
        nan_points = store.detect_nan_or_inf("grad_norm", self.check_window)
        if nan_points:
            evidence.append(Evidence(
                metric="grad_norm",
                observation=f"NaN/Inf gradients detected ({len(nan_points)} occurrences)",
                step=nan_points[-1].step,
            ))
            confidence += 0.6
            severity = Severity.CRITICAL

        # Check for exploding gradients (absolute threshold)
        recent_points = store.get_last("grad_norm", self.check_window)
        exploding = [p for p in recent_points if p.is_valid() and p.value > self.explosion_threshold]
        if exploding:
            evidence.append(Evidence(
                metric="grad_norm",
                observation=f"Exploding gradients (>{self.explosion_threshold}): {len(exploding)} occurrences",
                value=max(p.value for p in exploding),
                step=exploding[-1].step,
            ))
            confidence += 0.4
            if len(exploding) > 5:
                severity = Severity.CRITICAL

        # Check for gradient spikes (relative to recent history)
        grad_spikes = store.detect_spikes("grad_norm", self.check_window, threshold_std=self.spike_std_threshold)
        if len(grad_spikes) >= 2 and not exploding:  # Don't double-count with exploding
            evidence.append(Evidence(
                metric="grad_norm",
                observation=f"Gradient spikes detected: {len(grad_spikes)} times (>{self.spike_std_threshold} std)",
                value=max(p.value for p in grad_spikes),
                step=grad_spikes[-1].step,
            ))
            confidence += 0.3

        # Check for vanishing gradients
        vanishing = [p for p in recent_points if p.is_valid() and p.value < self.vanishing_threshold]
        if len(vanishing) > self.check_window // 3:  # Significant portion vanishing
            avg_vanishing = sum(p.value for p in vanishing) / len(vanishing)
            evidence.append(Evidence(
                metric="grad_norm",
                observation=f"Vanishing gradients (<{self.vanishing_threshold}): {len(vanishing)}/{len(recent_points)} steps",
                value=avg_vanishing,
            ))
            confidence += 0.4

        # Check for high variance in gradient norms
        stats = store.compute_window_stats("grad_norm", self.check_window)
        if stats.mean > 0 and stats.count >= 10:
            cv = stats.std / stats.mean
            if cv > 1.5:  # Coefficient of variation > 150% (lowered from 200%)
                evidence.append(Evidence(
                    metric="grad_norm",
                    observation=f"Highly unstable gradients (CV: {cv:.1f})",
                    value=cv,
                ))
                confidence += 0.2

        if not evidence:
            return None

        confidence = min(confidence, 1.0)

        # Determine suggestions based on the issue
        suggestions = []
        explanation_parts = []

        if nan_points:
            explanation_parts.append(
                "NaN gradients indicate numerical overflow, often from loss explosion or numerical instability."
            )
            suggestions.extend([
                "Enable gradient clipping (e.g., max_grad_norm=1.0)",
                "Reduce learning rate significantly",
                "Check for division by zero in loss computation",
            ])

        if exploding:
            explanation_parts.append(
                "Exploding gradients cause unstable updates that can derail training."
            )
            suggestions.extend([
                "Add gradient clipping if not present",
                "Reduce learning rate",
                "Use gradient scaling for mixed precision training",
            ])

        if vanishing:
            explanation_parts.append(
                "Vanishing gradients prevent learning, often in deep networks or with saturating activations."
            )
            suggestions.extend([
                "Check for dead ReLU neurons",
                "Use residual connections if not present",
                "Try different initialization",
                "Consider using LayerNorm or BatchNorm",
            ])

        if not suggestions:
            suggestions = [
                "Enable gradient clipping",
                "Reduce learning rate",
                "Check model architecture for instability sources",
            ]

        return Diagnosis(
            problem="Gradient instability detected",
            explanation=" ".join(explanation_parts) if explanation_parts else (
                "Training is experiencing gradient instability that may prevent proper learning."
            ),
            evidence=evidence,
            suggestions=suggestions,
            confidence=confidence,
            severity=severity,
        )


class MixedPrecisionInstabilityDetector(BaseDetector):
    """Detects issues specific to mixed precision (FP16/BF16) training."""

    name = "mixed_precision_instability"
    description = "Detects instabilities commonly seen in mixed precision training"
    min_data_points = 50
    cooldown_steps = 200

    def __init__(self, check_window: int = 50):
        super().__init__()
        self.check_window = check_window

    @property
    def required_metrics(self) -> List[str]:
        return ["loss"]

    def detect(self, store: MetricStore) -> Optional[Diagnosis]:
        evidence = []
        confidence = 0.0

        # Check for loss scale issues (common in FP16)
        # Pattern: loss suddenly becoming very large or NaN after being stable
        loss_points = store.get_last("loss", self.check_window)

        if len(loss_points) < 20:
            return None

        # Split into first and second half
        mid = len(loss_points) // 2
        first_half = loss_points[:mid]
        second_half = loss_points[mid:]

        first_valid = [p for p in first_half if p.is_valid()]
        second_valid = [p for p in second_half if p.is_valid()]

        if not first_valid or not second_valid:
            return None

        first_mean = sum(p.value for p in first_valid) / len(first_valid)
        second_nan_count = sum(1 for p in second_half if not p.is_valid())

        # Pattern: stable loss followed by NaN outbreak
        if second_nan_count > len(second_half) * 0.2 and first_mean < 100:
            evidence.append(Evidence(
                metric="loss",
                observation=f"Sudden NaN outbreak after stable training",
                value=second_nan_count,
            ))
            confidence += 0.5

        # Check for loss scale oscillation pattern (large swings)
        if store.has_metric("grad_norm"):
            grad_stats = store.compute_window_stats("grad_norm", self.check_window)
            if grad_stats.mean > 0 and grad_stats.range > 10 * grad_stats.mean:
                evidence.append(Evidence(
                    metric="grad_norm",
                    observation=f"Extreme gradient norm range (possible loss scale issues)",
                    value=grad_stats.range,
                ))
                confidence += 0.3

        if not evidence:
            return None

        confidence = min(confidence, 1.0)

        return Diagnosis(
            problem="Possible mixed precision instability",
            explanation=(
                "Training shows patterns consistent with mixed precision (FP16/BF16) numerical issues. "
                "This can happen when the loss scale is too high or the model produces values "
                "outside the representable range."
            ),
            evidence=evidence,
            suggestions=[
                "If using FP16, try BF16 instead (if hardware supports)",
                "Reduce initial loss scale or use dynamic loss scaling",
                "Add gradient clipping before loss scaling",
                "Check for operations that produce large intermediate values",
                "Consider using FP32 for the first/last layers",
            ],
            confidence=confidence,
            severity=Severity.WARNING,
        )
