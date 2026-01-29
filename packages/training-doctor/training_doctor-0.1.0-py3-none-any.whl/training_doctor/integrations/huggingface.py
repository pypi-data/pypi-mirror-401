from typing import Optional, Dict, Any

from ..doctor import Doctor
from ..reporters.console import ConsoleReporter


class HuggingFaceCallback:
    """Callback for HuggingFace Transformers Trainer.

    Usage:
        from training_doctor.integrations import HuggingFaceCallback
        from transformers import Trainer

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            callbacks=[HuggingFaceCallback()]
        )
        trainer.train()
    """

    def __init__(
        self,
        doctor: Optional[Doctor] = None,
        auto_print: bool = True,
        check_interval: int = 100,
    ):
        """Initialize the callback.

        Args:
            doctor: Doctor instance to use. Creates new one if None.
            auto_print: Whether to print diagnoses automatically.
            check_interval: How often to run detection (in steps).
        """
        self.doctor = doctor or Doctor()
        self.reporter = ConsoleReporter() if auto_print else None
        self.check_interval = check_interval
        self._step_count = 0

    def on_log(self, args, state, control, logs: Optional[Dict[str, Any]] = None, **kwargs):
        """Called when the trainer logs metrics."""
        if logs is None:
            return

        step = state.global_step
        self._step_count += 1

        # Extract metrics
        metrics = {}
        for key, value in logs.items():
            if isinstance(value, (int, float)):
                metrics[key] = float(value)

        if metrics:
            diagnoses = self.doctor.log(step, **metrics)

            if self.reporter and diagnoses:
                for diagnosis in diagnoses:
                    self.reporter.report(diagnosis)

    def on_train_begin(self, args, state, control, **kwargs):
        """Called at the beginning of training."""
        self.doctor.clear()

    def on_train_end(self, args, state, control, **kwargs):
        """Called at the end of training."""
        if self.reporter:
            self.reporter.report_summary(self.doctor.diagnoses)

    def on_evaluate(self, args, state, control, metrics: Optional[Dict[str, Any]] = None, **kwargs):
        """Called after evaluation."""
        if metrics is None:
            return

        step = state.global_step
        eval_metrics = {}

        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                # Prefix eval metrics
                if not key.startswith("eval_"):
                    key = f"eval_{key}"
                eval_metrics[key] = float(value)

        if eval_metrics:
            diagnoses = self.doctor.log(step, **eval_metrics)

            if self.reporter and diagnoses:
                for diagnosis in diagnoses:
                    self.reporter.report(diagnosis)

    @property
    def diagnoses(self):
        """Get all diagnoses from the doctor."""
        return self.doctor.diagnoses


# For backwards compatibility with transformers TrainerCallback interface
try:
    from transformers import TrainerCallback

    class TrainCheckCallback(TrainerCallback, HuggingFaceCallback):
        """HuggingFace TrainerCallback implementation."""

        def __init__(self, *args, **kwargs):
            HuggingFaceCallback.__init__(self, *args, **kwargs)

except ImportError:
    # transformers not installed, use standalone version
    TrainCheckCallback = HuggingFaceCallback
