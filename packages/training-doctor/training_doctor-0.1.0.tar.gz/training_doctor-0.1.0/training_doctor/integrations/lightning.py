from typing import Optional, Any, Dict

from ..doctor import Doctor
from ..reporters.console import ConsoleReporter


class LightningCallback:
    """Callback for PyTorch Lightning Trainer.

    Usage:
        from training_doctor.integrations import LightningCallback
        import pytorch_lightning as pl

        trainer = pl.Trainer(callbacks=[LightningCallback()])
        trainer.fit(model, datamodule)
    """

    def __init__(
        self,
        doctor: Optional[Doctor] = None,
        auto_print: bool = True,
    ):
        """Initialize the callback.

        Args:
            doctor: Doctor instance to use. Creates new one if None.
            auto_print: Whether to print diagnoses automatically.
        """
        self.doctor = doctor or Doctor()
        self.reporter = ConsoleReporter() if auto_print else None

    def on_train_batch_end(
        self,
        trainer,
        pl_module,
        outputs: Any,
        batch: Any,
        batch_idx: int,
    ) -> None:
        """Called at the end of each training batch."""
        step = trainer.global_step

        # Collect metrics from trainer's logged metrics
        metrics = self._extract_metrics(trainer)

        # Add loss from outputs if available
        if isinstance(outputs, dict) and "loss" in outputs:
            metrics["loss"] = float(outputs["loss"].detach().cpu().item())
        elif hasattr(outputs, "loss"):
            metrics["loss"] = float(outputs.loss.detach().cpu().item())

        if metrics:
            diagnoses = self.doctor.log(step, **metrics)
            self._report_diagnoses(diagnoses)

    def on_validation_end(self, trainer, pl_module) -> None:
        """Called at the end of validation."""
        step = trainer.global_step
        metrics = self._extract_metrics(trainer, prefix="val_")

        if metrics:
            diagnoses = self.doctor.log(step, **metrics)
            self._report_diagnoses(diagnoses)

    def on_train_epoch_end(self, trainer, pl_module) -> None:
        """Called at the end of each training epoch."""
        # Run a check at epoch end
        diagnoses = self.doctor.check()
        self._report_diagnoses(diagnoses)

    def on_train_start(self, trainer, pl_module) -> None:
        """Called at the start of training."""
        self.doctor.clear()

    def on_train_end(self, trainer, pl_module) -> None:
        """Called at the end of training."""
        if self.reporter:
            self.reporter.report_summary(self.doctor.diagnoses)

    def _extract_metrics(self, trainer, prefix: str = "") -> Dict[str, float]:
        """Extract numeric metrics from trainer's callback metrics."""
        metrics = {}

        # Get logged metrics
        logged = getattr(trainer, "logged_metrics", {})
        for key, value in logged.items():
            if self._is_numeric(value):
                metrics[f"{prefix}{key}"] = self._to_float(value)

        # Get callback metrics
        callback_metrics = getattr(trainer, "callback_metrics", {})
        for key, value in callback_metrics.items():
            if self._is_numeric(value):
                metrics[f"{prefix}{key}"] = self._to_float(value)

        return metrics

    def _is_numeric(self, value: Any) -> bool:
        """Check if a value is numeric."""
        if isinstance(value, (int, float)):
            return True
        # Check for tensor types
        if hasattr(value, "item"):
            return True
        return False

    def _to_float(self, value: Any) -> float:
        """Convert a value to float."""
        if hasattr(value, "item"):
            return float(value.item())
        return float(value)

    def _report_diagnoses(self, diagnoses) -> None:
        """Report diagnoses if reporter is configured."""
        if self.reporter and diagnoses:
            for diagnosis in diagnoses:
                self.reporter.report(diagnosis)

    @property
    def diagnoses(self):
        """Get all diagnoses from the doctor."""
        return self.doctor.diagnoses


# Try to create proper Lightning callback if pytorch_lightning is installed
try:
    from pytorch_lightning import Callback

    class TrainCheckLightningCallback(Callback, LightningCallback):
        """PyTorch Lightning Callback implementation."""

        def __init__(self, *args, **kwargs):
            LightningCallback.__init__(self, *args, **kwargs)

except ImportError:
    # pytorch_lightning not installed
    TrainCheckLightningCallback = LightningCallback
