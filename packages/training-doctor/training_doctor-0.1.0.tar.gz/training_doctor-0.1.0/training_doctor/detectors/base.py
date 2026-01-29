from abc import ABC, abstractmethod
from typing import List, Optional

from ..diagnosis import Diagnosis
from ..metrics.store import MetricStore


class BaseDetector(ABC):
    """Abstract base class for all training issue detectors."""

    # Minimum number of data points needed before detection can run
    min_data_points: int = 10

    # How often to run detection (in steps). None means every check.
    check_interval: Optional[int] = None

    # Cooldown period after a diagnosis (in steps) to avoid spam
    cooldown_steps: int = 100

    def __init__(self):
        self._last_diagnosis_step: Optional[int] = None
        self._last_diagnosis_confidence: float = 0.0
        self._diagnosis_count: int = 0

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for this detector."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what this detector checks."""
        pass

    @property
    def required_metrics(self) -> List[str]:
        """List of metric names required for this detector.

        Override this to specify which metrics must be present.
        Empty list means detector can run with any available metrics.
        """
        return []

    def can_run(self, store: MetricStore) -> bool:
        """Check if the detector has enough data to run."""
        # Check minimum data points
        if len(store) < self.min_data_points:
            return False

        # Check required metrics are present
        for metric in self.required_metrics:
            if not store.has_metric(metric):
                return False

        return True

    def should_run(self, store: MetricStore) -> bool:
        """Check if the detector should run based on interval and cooldown."""
        if not self.can_run(store):
            return False

        current_step = store.current_step

        # Check cooldown
        if self._last_diagnosis_step is not None:
            steps_since_last = current_step - self._last_diagnosis_step
            if steps_since_last < self.cooldown_steps:
                return False

        # Check interval
        if self.check_interval is not None:
            if current_step % self.check_interval != 0:
                return False

        return True

    @abstractmethod
    def detect(self, store: MetricStore) -> Optional[Diagnosis]:
        """Run detection logic and return a diagnosis if an issue is found.

        Args:
            store: The MetricStore containing all logged metrics.

        Returns:
            A Diagnosis object if an issue is detected, None otherwise.
        """
        pass

    def check(self, store: MetricStore) -> Optional[Diagnosis]:
        """Run the detector if conditions are met.

        This is the main entry point called by the Doctor.
        """
        # Check basic preconditions (can_run + interval)
        if not self.can_run(store):
            return None

        current_step = store.current_step

        # Check interval (but not cooldown - we handle that specially)
        if self.check_interval is not None:
            if current_step % self.check_interval != 0:
                return None

        # Check if we're in cooldown
        in_cooldown = False
        if self._last_diagnosis_step is not None:
            steps_since_last = current_step - self._last_diagnosis_step
            if steps_since_last < self.cooldown_steps:
                in_cooldown = True

        # Run detection
        diagnosis = self.detect(store)

        if diagnosis is not None:
            # If in cooldown, only report if confidence is significantly higher
            if in_cooldown:
                confidence_improvement = diagnosis.confidence - self._last_diagnosis_confidence
                if confidence_improvement < 0.2:  # Need 20% higher confidence to break cooldown
                    return None

            diagnosis.detector_name = self.name
            diagnosis.step = current_step
            self._last_diagnosis_step = current_step
            self._last_diagnosis_confidence = diagnosis.confidence
            self._diagnosis_count += 1

        return diagnosis

    def reset(self) -> None:
        """Reset detector state."""
        self._last_diagnosis_step = None
        self._last_diagnosis_confidence = 0.0
        self._diagnosis_count = 0

    @property
    def diagnosis_count(self) -> int:
        """Number of diagnoses this detector has made."""
        return self._diagnosis_count
