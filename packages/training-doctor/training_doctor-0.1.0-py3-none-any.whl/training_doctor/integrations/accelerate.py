from typing import Optional, Dict, Any

from ..doctor import Doctor
from ..reporters.console import ConsoleReporter


class AccelerateTracker:
    """Integration for HuggingFace Accelerate.

    Usage:
        from training_doctor.integrations import AccelerateTracker
        from accelerate import Accelerator

        accelerator = Accelerator()
        tracker = AccelerateTracker()

        for step, batch in enumerate(dataloader):
            loss = model(batch)
            accelerator.backward(loss)
            optimizer.step()

            # Log metrics to training_doctor
            tracker.log(
                step=step,
                loss=loss.item(),
                lr=optimizer.param_groups[0]['lr']
            )
    """

    def __init__(
        self,
        doctor: Optional[Doctor] = None,
        auto_print: bool = True,
        check_every: int = 100,
    ):
        """Initialize the tracker.

        Args:
            doctor: Doctor instance to use. Creates new one if None.
            auto_print: Whether to print diagnoses automatically.
            check_every: How often to run full detection (in steps).
        """
        self.doctor = doctor or Doctor()
        self.reporter = ConsoleReporter() if auto_print else None
        self.check_every = check_every
        self._step_count = 0

    def log(self, step: int, **metrics: float) -> None:
        """Log metrics and check for issues.

        Args:
            step: Current training step.
            **metrics: Metric name-value pairs.
        """
        self._step_count += 1
        diagnoses = self.doctor.log(step, **metrics)

        if self.reporter and diagnoses:
            for diagnosis in diagnoses:
                self.reporter.report(diagnosis)

    def check(self) -> None:
        """Manually trigger a check."""
        diagnoses = self.doctor.check()
        if self.reporter and diagnoses:
            for diagnosis in diagnoses:
                self.reporter.report(diagnosis)

    def summary(self) -> None:
        """Print a summary of all diagnoses."""
        if self.reporter:
            self.reporter.report_summary(self.doctor.diagnoses)

    @property
    def diagnoses(self):
        """Get all diagnoses from the doctor."""
        return self.doctor.diagnoses


class AccelerateCallback:
    """Callback-style integration for Accelerate with automatic metric extraction.

    Usage:
        from training_doctor.integrations import AccelerateCallback
        from accelerate import Accelerator

        accelerator = Accelerator()
        callback = AccelerateCallback(accelerator)

        for step, batch in enumerate(dataloader):
            loss = model(batch)
            accelerator.backward(loss)
            optimizer.step()

            callback.on_step_end(step, loss=loss.item())
    """

    def __init__(
        self,
        accelerator: Any = None,
        doctor: Optional[Doctor] = None,
        auto_print: bool = True,
    ):
        """Initialize the callback.

        Args:
            accelerator: Accelerator instance (optional, for future extensions).
            doctor: Doctor instance to use. Creates new one if None.
            auto_print: Whether to print diagnoses automatically.
        """
        self.accelerator = accelerator
        self.doctor = doctor or Doctor()
        self.reporter = ConsoleReporter() if auto_print else None

    def on_step_end(self, step: int, **metrics: float) -> None:
        """Called at the end of each training step.

        Args:
            step: Current training step.
            **metrics: Metric name-value pairs.
        """
        diagnoses = self.doctor.log(step, **metrics)

        if self.reporter and diagnoses:
            for diagnosis in diagnoses:
                self.reporter.report(diagnosis)

    def on_train_begin(self) -> None:
        """Called at the beginning of training."""
        self.doctor.clear()

    def on_train_end(self) -> None:
        """Called at the end of training."""
        if self.reporter:
            self.reporter.report_summary(self.doctor.diagnoses)

    def on_evaluate(self, step: int, **metrics: float) -> None:
        """Called after evaluation.

        Args:
            step: Current training step.
            **metrics: Evaluation metrics (will be prefixed with eval_).
        """
        eval_metrics = {f"eval_{k}": v for k, v in metrics.items()}
        diagnoses = self.doctor.log(step, **eval_metrics)

        if self.reporter and diagnoses:
            for diagnosis in diagnoses:
                self.reporter.report(diagnosis)

    @property
    def diagnoses(self):
        """Get all diagnoses from the doctor."""
        return self.doctor.diagnoses
