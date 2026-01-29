from typing import List, Optional, Type, Dict, Any, Union
from pathlib import Path

from .diagnosis import Diagnosis
from .metrics.store import MetricStore
from .detectors.base import BaseDetector


class Doctor:
    """Main orchestrator for training diagnostics.

    The Doctor manages metric collection, runs detectors, and produces diagnoses.
    It supports both live monitoring during training and offline analysis of logs.
    """

    def __init__(self, detectors: Optional[List[BaseDetector]] = None):
        """Initialize the Doctor.

        Args:
            detectors: Optional list of detectors to use. If None, uses default set.
        """
        self._store = MetricStore()
        self._detectors: List[BaseDetector] = []
        self._diagnoses: List[Diagnosis] = []
        self._auto_print: bool = False

        if detectors is not None:
            for detector in detectors:
                self.add_detector(detector)
        else:
            self._register_default_detectors()

    def _register_default_detectors(self) -> None:
        """Register the default set of detectors."""
        # Import here to avoid circular imports
        from .detectors.learning_rate import (
            LearningRateTooHighDetector,
            LearningRateTooLowDetector,
        )

        default_detectors = [
            LearningRateTooHighDetector(),
            LearningRateTooLowDetector(),
        ]

        # These will be added as we implement them
        try:
            from .detectors.plateau import PlateauDetector
            default_detectors.append(PlateauDetector())
        except ImportError:
            pass

        try:
            from .detectors.overfitting import OverfittingDetector
            default_detectors.append(OverfittingDetector())
        except ImportError:
            pass

        try:
            from .detectors.instability import GradientInstabilityDetector
            default_detectors.append(GradientInstabilityDetector())
        except ImportError:
            pass

        for detector in default_detectors:
            self.add_detector(detector)

    def add_detector(self, detector: BaseDetector) -> "Doctor":
        """Add a detector to the Doctor.

        Args:
            detector: The detector instance to add.

        Returns:
            Self for method chaining.
        """
        self._detectors.append(detector)
        return self

    def remove_detector(self, name: str) -> "Doctor":
        """Remove a detector by name.

        Args:
            name: The name of the detector to remove.

        Returns:
            Self for method chaining.
        """
        self._detectors = [d for d in self._detectors if d.name != name]
        return self

    def log(self, step: int, **metrics: float) -> List[Diagnosis]:
        """Log metrics and run detection.

        This is the main method for live monitoring. Call this during training
        to log metrics and check for issues.

        Args:
            step: Current training step.
            **metrics: Metric name-value pairs (e.g., loss=2.5, lr=0.001).

        Returns:
            List of new diagnoses detected at this step.
        """
        self._store.log(step, **metrics)
        return self.check()

    def check(self) -> List[Diagnosis]:
        """Run all detectors and return new diagnoses.

        Returns:
            List of diagnoses from this check.
        """
        new_diagnoses = []

        for detector in self._detectors:
            diagnosis = detector.check(self._store)
            if diagnosis is not None:
                new_diagnoses.append(diagnosis)
                self._diagnoses.append(diagnosis)
                if self._auto_print:
                    print(diagnosis)
                    print()

        return new_diagnoses

    def analyze(self) -> List[Diagnosis]:
        """Run full analysis on loaded data.

        Use this for offline analysis after loading logs.
        Unlike check(), this runs detection at every recorded step.

        Returns:
            All diagnoses found during analysis.
        """
        # Reset detectors for fresh analysis
        for detector in self._detectors:
            detector.reset()

        self._diagnoses.clear()

        # Get all unique steps
        all_steps = set()
        for metric, points in self._store:
            for point in points:
                all_steps.add(point.step)

        # Run detection at each step (simulating live monitoring)
        # We update the store's current_step to simulate progression
        for step in sorted(all_steps):
            self._store._current_step = step
            self.check()

        return list(self._diagnoses)

    def load(self, path: Union[str, Path], format: Optional[str] = None) -> "Doctor":
        """Load metrics from a file or directory.

        Args:
            path: Path to log file or directory.
            format: Format hint ('csv', 'wandb', 'tensorboard'). Auto-detected if None.

        Returns:
            Self for method chaining.
        """
        path = Path(path)

        if format is None:
            format = self._detect_format(path)

        if format == "csv":
            from .loaders.csv import CSVLoader
            loader = CSVLoader()
        elif format == "wandb":
            from .loaders.wandb import WandBLoader
            loader = WandBLoader()
        elif format == "tensorboard":
            from .loaders.tensorboard import TensorBoardLoader
            loader = TensorBoardLoader()
        else:
            raise ValueError(f"Unknown format: {format}")

        loader.load(path, self._store)
        return self

    def _detect_format(self, path: Path) -> str:
        """Auto-detect the log format from the path."""
        if path.suffix == ".csv":
            return "csv"
        if path.is_dir():
            # Check for W&B or TensorBoard markers
            if (path / "wandb-metadata.json").exists():
                return "wandb"
            if any(path.glob("events.out.tfevents.*")):
                return "tensorboard"
            # Check subdirectories
            if any(path.glob("**/events.out.tfevents.*")):
                return "tensorboard"
        raise ValueError(f"Cannot auto-detect format for: {path}")

    def set_auto_print(self, enabled: bool = True) -> "Doctor":
        """Enable or disable automatic printing of diagnoses.

        Args:
            enabled: Whether to print diagnoses automatically.

        Returns:
            Self for method chaining.
        """
        self._auto_print = enabled
        return self

    @property
    def store(self) -> MetricStore:
        """Access the underlying metric store."""
        return self._store

    @property
    def diagnoses(self) -> List[Diagnosis]:
        """Get all diagnoses made so far."""
        return list(self._diagnoses)

    @property
    def detectors(self) -> List[BaseDetector]:
        """Get all registered detectors."""
        return list(self._detectors)

    def clear(self) -> "Doctor":
        """Clear all metrics and diagnoses.

        Returns:
            Self for method chaining.
        """
        self._store.clear()
        self._diagnoses.clear()
        for detector in self._detectors:
            detector.reset()
        return self

    def summary(self) -> Dict[str, Any]:
        """Get a summary of the current state.

        Returns:
            Dictionary with metrics and diagnosis counts.
        """
        return {
            "total_steps": self._store.current_step,
            "total_data_points": len(self._store),
            "metrics": self._store.get_metrics(),
            "diagnoses_count": len(self._diagnoses),
            "diagnoses_by_severity": {
                "critical": sum(1 for d in self._diagnoses if d.severity.value == "critical"),
                "warning": sum(1 for d in self._diagnoses if d.severity.value == "warning"),
                "info": sum(1 for d in self._diagnoses if d.severity.value == "info"),
            },
            "detectors": [d.name for d in self._detectors],
        }
