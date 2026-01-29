import math
from typing import Optional, List

from ..diagnosis import Diagnosis, Evidence, Severity
from ..metrics.store import MetricStore
from .base import BaseDetector


class LearningRateTooHighDetector(BaseDetector):
    """Detects when the learning rate is too high, causing instability."""

    name = "lr_too_high"
    description = "Detects learning rate too high causing loss spikes, NaN, or divergence"
    min_data_points = 10
    cooldown_steps = 200

    def __init__(
        self,
        loss_spike_threshold: float = 3.5,  # Increased from 3.0 to reduce false positives
        nan_check_window: int = 50,
        spike_check_window: int = 100,
        min_spikes_to_report: int = 3,  # Need multiple spikes (increased from 2)
    ):
        super().__init__()
        self.loss_spike_threshold = loss_spike_threshold
        self.nan_check_window = nan_check_window
        self.spike_check_window = spike_check_window
        self.min_spikes_to_report = min_spikes_to_report

    @property
    def required_metrics(self) -> List[str]:
        return ["loss"]

    def detect(self, store: MetricStore) -> Optional[Diagnosis]:
        evidence = []
        confidence = 0.0

        # Check for NaN in loss
        nan_points = store.detect_nan_or_inf("loss", self.nan_check_window)
        if nan_points:
            evidence.append(Evidence(
                metric="loss",
                observation="NaN or Inf values detected",
                step=nan_points[-1].step,
            ))
            confidence += 0.5

        # Check for loss spikes (require multiple to avoid noise)
        spikes = store.detect_spikes("loss", self.spike_check_window, threshold_std=self.loss_spike_threshold)
        if len(spikes) >= self.min_spikes_to_report:
            evidence.append(Evidence(
                metric="loss",
                observation=f"Loss spiked {len(spikes)} times (>{self.loss_spike_threshold} std)",
                value=spikes[-1].value,
                step=spikes[-1].step,
            ))
            confidence += 0.3 + min(0.2, len(spikes) * 0.05)  # More spikes = higher confidence

        # Check for increasing loss trend (short window - rapid increase)
        trend = store.detect_trend("loss", window_size=20)
        if trend == "increasing":
            stats = store.compute_window_stats("loss", 20)
            if stats.relative_change > 0.3:  # Loss increased by >30%
                evidence.append(Evidence(
                    metric="loss",
                    observation=f"Loss increasing rapidly ({stats.relative_change:.1%} in 20 steps)",
                    value=stats.last_value,
                ))
                confidence += 0.3

        # Check for slow divergence (longer window - gradual increase)
        if store.count("loss") >= 500:
            long_stats = store.compute_window_stats("loss", 500)
            # Check if loss is higher at end than beginning of window
            if long_stats.relative_change > 0.10:  # Loss increased by >10% over 500 steps
                # Confirm with multiple windows to avoid noise
                mid_stats = store.compute_window_stats("loss", 250)
                recent_stats = store.compute_window_stats("loss", 100)
                # If both recent windows show loss going up, it's diverging
                if (mid_stats.relative_change > 0.03 and  # Require stronger signal in mid window
                    recent_stats.last_value > long_stats.first_value * 1.08):  # 8% higher
                    evidence.append(Evidence(
                        metric="loss",
                        observation=f"Loss slowly diverging ({long_stats.relative_change:.1%} over 500 steps)",
                        value=long_stats.last_value,
                    ))
                    confidence += 0.3  # Reduced from 0.4

        # Check gradient norm if available
        if store.has_metric("grad_norm"):
            grad_nans = store.detect_nan_or_inf("grad_norm", self.nan_check_window)
            if grad_nans:
                evidence.append(Evidence(
                    metric="grad_norm",
                    observation="NaN or Inf gradients detected",
                    step=grad_nans[-1].step,
                ))
                confidence += 0.3

            grad_spikes = store.detect_spikes("grad_norm", self.spike_check_window, threshold_std=3.0)
            if grad_spikes:
                evidence.append(Evidence(
                    metric="grad_norm",
                    observation=f"Gradient norm spiked {len(grad_spikes)} times",
                    value=grad_spikes[-1].value,
                    step=grad_spikes[-1].step,
                ))
                confidence += 0.2

        if not evidence:
            return None

        confidence = min(confidence, 1.0)

        # Get current LR for suggestions
        current_lr = store.get_latest_value("lr")
        lr_suggestion = ""
        if current_lr is not None:
            suggested_lr = current_lr * 0.3
            lr_suggestion = f"Reduce learning rate from {current_lr:.2e} to ~{suggested_lr:.2e}"
        else:
            lr_suggestion = "Reduce learning rate by 3-10x"

        # Determine severity
        if nan_points:
            severity = Severity.CRITICAL
        elif len(spikes) > 3:
            severity = Severity.CRITICAL
        else:
            severity = Severity.WARNING

        return Diagnosis(
            problem="Learning rate likely too high",
            explanation=(
                "Training is showing signs of instability typically caused by an excessive learning rate. "
                "The optimizer is taking steps that are too large, causing the loss to spike or diverge."
            ),
            evidence=evidence,
            suggestions=[
                lr_suggestion,
                "Consider using learning rate warmup if not already",
                "Try gradient clipping (e.g., max_grad_norm=1.0)",
                "If using Adam, try lower beta2 (e.g., 0.95 instead of 0.999)",
            ],
            confidence=confidence,
            severity=severity,
        )


class LearningRateTooLowDetector(BaseDetector):
    """Detects when the learning rate is too low, causing slow or no learning."""

    name = "lr_too_low"
    description = "Detects learning rate too low causing slow progress or no learning"
    min_data_points = 50
    cooldown_steps = 500

    def __init__(
        self,
        min_loss_decrease: float = 0.01,
        check_window: int = 100,
    ):
        super().__init__()
        self.min_loss_decrease = min_loss_decrease
        self.check_window = check_window

    @property
    def required_metrics(self) -> List[str]:
        return ["loss"]

    def detect(self, store: MetricStore) -> Optional[Diagnosis]:
        if store.count("loss") < self.check_window:
            return None

        evidence = []
        confidence = 0.0

        # Check for flat loss over window
        stats = store.compute_window_stats("loss", self.check_window)

        # Loss should be decreasing in healthy training
        if stats.count >= self.check_window:
            relative_decrease = -stats.relative_change  # Negate because decrease is negative

            if relative_decrease < self.min_loss_decrease:
                evidence.append(Evidence(
                    metric="loss",
                    observation=f"Loss barely changed over {self.check_window} steps ({stats.relative_change:.2%})",
                    value=stats.last_value,
                ))
                confidence += 0.4

            # Check variance - very low variance suggests no learning
            if stats.std < 0.001 * abs(stats.mean) if stats.mean != 0 else stats.std < 1e-6:
                evidence.append(Evidence(
                    metric="loss",
                    observation="Loss has extremely low variance (essentially flat)",
                    value=stats.std,
                ))
                confidence += 0.3

        # Check if gradient norms are very small
        if store.has_metric("grad_norm"):
            grad_stats = store.compute_window_stats("grad_norm", self.check_window)
            if grad_stats.mean < 1e-6:
                evidence.append(Evidence(
                    metric="grad_norm",
                    observation="Gradient norms extremely small",
                    value=grad_stats.mean,
                ))
                confidence += 0.3

        if not evidence:
            return None

        confidence = min(confidence, 1.0)

        # Get current LR for suggestions
        current_lr = store.get_latest_value("lr")
        lr_suggestion = ""
        if current_lr is not None:
            suggested_lr = current_lr * 3
            lr_suggestion = f"Increase learning rate from {current_lr:.2e} to ~{suggested_lr:.2e}"
        else:
            lr_suggestion = "Increase learning rate by 2-5x"

        return Diagnosis(
            problem="Learning rate may be too low",
            explanation=(
                "Training progress is very slow or stalled. The loss is barely changing, "
                "which often indicates the learning rate is too conservative. "
                "The model is learning very slowly or not at all."
            ),
            evidence=evidence,
            suggestions=[
                lr_suggestion,
                "Consider using a learning rate finder/range test",
                "Try a learning rate schedule with warmup to a higher peak",
                "Verify data is being loaded correctly (not constant/empty batches)",
            ],
            confidence=confidence,
            severity=Severity.WARNING,
        )
