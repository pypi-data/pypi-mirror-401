import math
from typing import Optional, List

from ..diagnosis import Diagnosis, Evidence, Severity
from ..metrics.store import MetricStore
from .base import BaseDetector


class PlateauDetector(BaseDetector):
    """Detects when training has plateaued - loss stagnation with ongoing training activity."""

    name = "plateau"
    description = "Detects loss plateau while training is still active"
    min_data_points = 100
    cooldown_steps = 500

    def __init__(
        self,
        plateau_window: int = 200,  # Increased from 100
        min_relative_change: float = 0.01,  # Tightened - must be REALLY flat
        high_variance_threshold: float = 0.2,  # Increased - need higher variance to trigger
        min_loss_for_plateau: float = 1.5,  # Don't flag plateau if loss is already low
    ):
        """Initialize plateau detector.

        Args:
            plateau_window: Number of steps to check for plateau.
            min_relative_change: Minimum expected relative change in loss.
            high_variance_threshold: Threshold for detecting high gradient variance.
            min_loss_for_plateau: Don't flag plateau if loss is below this (converged).
        """
        super().__init__()
        self.plateau_window = plateau_window
        self.min_relative_change = min_relative_change
        self.high_variance_threshold = high_variance_threshold
        self.min_loss_for_plateau = min_loss_for_plateau

    @property
    def required_metrics(self) -> List[str]:
        return ["loss"]

    def detect(self, store: MetricStore) -> Optional[Diagnosis]:
        if store.count("loss") < self.plateau_window:
            return None

        loss_stats = store.compute_window_stats("loss", self.plateau_window)

        # Don't flag plateau if loss is already low (model has converged)
        if loss_stats.last_value < self.min_loss_for_plateau:
            return None

        evidence = []
        confidence = 0.0

        relative_change = abs(loss_stats.relative_change)

        # Must be REALLY flat to trigger
        if relative_change < self.min_relative_change and loss_stats.count >= self.plateau_window:
            evidence.append(Evidence(
                metric="loss",
                observation=f"Loss plateaued for {self.plateau_window} steps (change: {loss_stats.relative_change:.2%})",
                value=loss_stats.last_value,
            ))
            confidence += 0.3  # Reduced from 0.4

            # Check if loss is still high (not converged)
            all_loss_stats = store.get_stats("loss")
            if loss_stats.last_value > 0.7 * all_loss_stats.first_value:  # Stricter: 70% not 50%
                evidence.append(Evidence(
                    metric="loss",
                    observation="Loss still at high level (not converged)",
                    value=loss_stats.last_value,
                ))
                confidence += 0.2

        # Check gradient variance (high variance during plateau suggests under-batching)
        # Only add this if we already have plateau evidence
        if evidence and store.has_metric("grad_norm"):
            grad_stats = store.compute_window_stats("grad_norm", self.plateau_window)
            if grad_stats.mean > 0:
                cv = grad_stats.std / grad_stats.mean  # Coefficient of variation
                if cv > self.high_variance_threshold:
                    evidence.append(Evidence(
                        metric="grad_norm",
                        observation=f"High gradient variance during plateau (CV: {cv:.2f})",
                        value=grad_stats.std,
                    ))
                    confidence += 0.4  # Increased - this is strong signal

        # Require substantial evidence
        if not evidence or confidence < 0.5:
            return None

        confidence = min(confidence, 1.0)

        # Determine likely cause and suggestions
        suggestions = []
        explanation_parts = [
            "Loss has stopped decreasing but training is still active. "
        ]

        if store.has_metric("grad_norm"):
            grad_stats = store.compute_window_stats("grad_norm", self.plateau_window)
            if grad_stats.mean > 0 and grad_stats.std / grad_stats.mean > self.high_variance_threshold:
                explanation_parts.append(
                    "High gradient variance suggests the effective batch size may be too small, "
                    "causing noisy updates that cancel out progress."
                )
                suggestions.extend([
                    "Increase batch size or gradient accumulation steps",
                    "Target effective batch size of 500k-1M tokens for LLMs",
                ])

        suggestions.extend([
            "Reduce learning rate (current phase may need lower LR)",
            "Check if model capacity is sufficient for the task",
            "Verify data quality and diversity",
        ])

        return Diagnosis(
            problem="Training plateau detected",
            explanation=" ".join(explanation_parts),
            evidence=evidence,
            suggestions=suggestions,
            confidence=confidence,
            severity=Severity.WARNING,
        )


class EarlyPlateauDetector(BaseDetector):
    """Detects early plateau - when loss stops improving too soon in training."""

    name = "early_plateau"
    description = "Detects plateau occurring too early in training"
    min_data_points = 200
    cooldown_steps = 1000

    def __init__(
        self,
        early_threshold_steps: int = 1000,
        plateau_window: int = 100,
        min_relative_change: float = 0.02,
    ):
        super().__init__()
        self.early_threshold_steps = early_threshold_steps
        self.plateau_window = plateau_window
        self.min_relative_change = min_relative_change

    @property
    def required_metrics(self) -> List[str]:
        return ["loss"]

    def detect(self, store: MetricStore) -> Optional[Diagnosis]:
        current_step = store.current_step

        # Only check for early plateau in the first portion of training
        if current_step > self.early_threshold_steps:
            return None

        if store.count("loss") < self.plateau_window:
            return None

        evidence = []
        confidence = 0.0

        loss_stats = store.compute_window_stats("loss", self.plateau_window)
        relative_change = abs(loss_stats.relative_change)

        if relative_change < self.min_relative_change:
            evidence.append(Evidence(
                metric="loss",
                observation=f"Loss plateaued early at step {current_step}",
                value=loss_stats.last_value,
                step=current_step,
            ))
            confidence += 0.5

            # Earlier plateau = higher confidence something is wrong
            early_ratio = 1 - (current_step / self.early_threshold_steps)
            confidence += early_ratio * 0.3

        if not evidence:
            return None

        confidence = min(confidence, 1.0)

        return Diagnosis(
            problem="Early training plateau",
            explanation=(
                f"Training has plateaued very early (step {current_step}). "
                "This often indicates a fundamental issue with the training setup: "
                "learning rate, batch size, or data pipeline problems."
            ),
            evidence=evidence,
            suggestions=[
                "Check that data batches are not constant/empty",
                "Verify learning rate is not too low",
                "Ensure gradient accumulation is working correctly",
                "Check for frozen/uninitialized model parameters",
            ],
            confidence=confidence,
            severity=Severity.WARNING,
        )
