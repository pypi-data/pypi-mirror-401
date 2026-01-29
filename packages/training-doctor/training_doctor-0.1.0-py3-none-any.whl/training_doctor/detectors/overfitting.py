from typing import Optional, List

from ..diagnosis import Diagnosis, Evidence, Severity
from ..metrics.store import MetricStore
from .base import BaseDetector


class OverfittingDetector(BaseDetector):
    """Detects overfitting - train loss decreasing while eval loss increases."""

    name = "overfitting"
    description = "Detects train/eval loss divergence indicating overfitting"
    min_data_points = 50
    cooldown_steps = 500

    def __init__(
        self,
        check_window: int = 50,
        divergence_threshold: float = 0.1,
        min_eval_increase: float = 0.05,
    ):
        """Initialize overfitting detector.

        Args:
            check_window: Number of steps to analyze.
            divergence_threshold: Minimum gap increase to trigger.
            min_eval_increase: Minimum eval loss increase to consider.
        """
        super().__init__()
        self.check_window = check_window
        self.divergence_threshold = divergence_threshold
        self.min_eval_increase = min_eval_increase

    @property
    def required_metrics(self) -> List[str]:
        return ["train_loss", "eval_loss"]

    def can_run(self, store: MetricStore) -> bool:
        """Check if we have both train and eval loss."""
        has_train = store.has_metric("train_loss") or store.has_metric("loss")
        has_eval = store.has_metric("eval_loss")
        return has_train and has_eval and super().can_run(store)

    def detect(self, store: MetricStore) -> Optional[Diagnosis]:
        # Get train loss (try train_loss first, fall back to loss)
        train_metric = "train_loss" if store.has_metric("train_loss") else "loss"

        if store.count(train_metric) < self.check_window:
            return None

        eval_points = store.get("eval_loss")
        if len(eval_points) < 6:  # Need enough eval points
            return None

        evidence = []
        confidence = 0.0

        # Focus on recent eval points - overfitting shows up later in training
        # Compare middle third vs last third of eval points
        n = len(eval_points)
        third = n // 3

        if third < 2:
            # Not enough points, fall back to halves
            mid = n // 2
            middle_section = eval_points[:mid]
            recent_section = eval_points[mid:]
        else:
            middle_section = eval_points[third:2*third]
            recent_section = eval_points[2*third:]

        middle_eval_avg = sum(p.value for p in middle_section) / len(middle_section)
        recent_eval_avg = sum(p.value for p in recent_section) / len(recent_section)

        # Eval loss increasing in recent period?
        eval_change = (recent_eval_avg - middle_eval_avg) / middle_eval_avg if middle_eval_avg > 0 else 0

        # Get train loss at similar time points
        middle_step = middle_section[len(middle_section)//2].step
        recent_step = recent_section[len(recent_section)//2].step

        train_at_middle = store.get_window(train_metric, max(0, middle_step - 50), middle_step + 50)
        train_at_recent = store.get_window(train_metric, max(0, recent_step - 50), recent_step + 50)

        if train_at_middle and train_at_recent:
            middle_train_avg = sum(p.value for p in train_at_middle) / len(train_at_middle)
            recent_train_avg = sum(p.value for p in train_at_recent) / len(train_at_recent)
            train_change = (recent_train_avg - middle_train_avg) / middle_train_avg if middle_train_avg > 0 else 0

            # Classic overfitting: train goes down (or flat), eval goes up
            train_decreasing = train_change < -0.02  # Train decreased by >2%
            eval_increasing = eval_change > self.min_eval_increase

            if train_decreasing and eval_increasing:
                evidence.append(Evidence(
                    metric=train_metric,
                    observation=f"Train loss decreasing ({train_change:.1%})",
                    value=recent_train_avg,
                ))
                evidence.append(Evidence(
                    metric="eval_loss",
                    observation=f"Eval loss increasing ({eval_change:.1%})",
                    value=recent_eval_avg,
                ))
                confidence += 0.6

        # Check the current gap between train and eval
        train_stats = store.compute_window_stats(train_metric, 100)
        if train_stats.last_value > 0 and recent_section:
            recent_eval = recent_section[-1].value
            gap_ratio = (recent_eval - train_stats.last_value) / train_stats.last_value
            if gap_ratio > self.divergence_threshold:
                evidence.append(Evidence(
                    metric="train_eval_gap",
                    observation=f"Eval loss {gap_ratio:.0%} higher than train loss",
                    value=gap_ratio,
                ))
                confidence += 0.3

        if not evidence:
            return None

        confidence = min(confidence, 1.0)

        return Diagnosis(
            problem="Overfitting detected",
            explanation=(
                "The model is memorizing training data rather than learning generalizable patterns. "
                "Training loss is decreasing but validation loss is increasing, "
                "indicating the model performs worse on unseen data."
            ),
            evidence=evidence,
            suggestions=[
                "Add or increase dropout",
                "Use weight decay (L2 regularization)",
                "Reduce model size if feasible",
                "Add more training data or data augmentation",
                "Implement early stopping based on eval loss",
                "Consider using a lower learning rate",
            ],
            confidence=confidence,
            severity=Severity.WARNING,
        )


class TrainEvalMismatchDetector(BaseDetector):
    """Detects unusual train/eval loss patterns that indicate data issues."""

    name = "train_eval_mismatch"
    description = "Detects suspicious train/eval patterns suggesting data issues"
    min_data_points = 30
    cooldown_steps = 500

    @property
    def required_metrics(self) -> List[str]:
        return ["eval_loss"]

    def can_run(self, store: MetricStore) -> bool:
        has_train = store.has_metric("train_loss") or store.has_metric("loss")
        has_eval = store.has_metric("eval_loss")
        return has_train and has_eval and super().can_run(store)

    def detect(self, store: MetricStore) -> Optional[Diagnosis]:
        train_metric = "train_loss" if store.has_metric("train_loss") else "loss"

        train_stats = store.get_stats(train_metric)
        eval_stats = store.get_stats("eval_loss")

        if train_stats.count < 10 or eval_stats.count < 3:
            return None

        evidence = []
        confidence = 0.0

        # Check if eval loss is significantly lower than train loss (unusual)
        if eval_stats.mean < train_stats.mean * 0.8:
            evidence.append(Evidence(
                metric="train_eval_comparison",
                observation="Eval loss unexpectedly lower than train loss",
                value=eval_stats.mean / train_stats.mean if train_stats.mean > 0 else 0,
            ))
            confidence += 0.5

        # Check if both are nearly identical (possible data leak)
        if train_stats.mean > 0:
            ratio = abs(eval_stats.mean - train_stats.mean) / train_stats.mean
            if ratio < 0.01 and train_stats.count > 50:
                evidence.append(Evidence(
                    metric="train_eval_comparison",
                    observation="Train and eval loss suspiciously similar (possible data leak)",
                    value=ratio,
                ))
                confidence += 0.4

        if not evidence:
            return None

        confidence = min(confidence, 1.0)

        return Diagnosis(
            problem="Unusual train/eval pattern",
            explanation=(
                "The relationship between training and evaluation loss is unusual. "
                "This could indicate data leakage, incorrect evaluation setup, "
                "or the same data being used for both train and eval."
            ),
            evidence=evidence,
            suggestions=[
                "Verify train and eval datasets are properly separated",
                "Check for data leakage in preprocessing",
                "Ensure eval is run on held-out data",
                "Review data loading and splitting logic",
            ],
            confidence=confidence,
            severity=Severity.WARNING,
        )
