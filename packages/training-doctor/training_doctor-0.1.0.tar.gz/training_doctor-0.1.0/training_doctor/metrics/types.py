from dataclasses import dataclass
from typing import Optional
from enum import Enum


class MetricType(Enum):
    """Standard metric types for training monitoring."""
    LOSS = "loss"
    TRAIN_LOSS = "train_loss"
    EVAL_LOSS = "eval_loss"
    LEARNING_RATE = "lr"
    GRADIENT_NORM = "grad_norm"
    THROUGHPUT = "throughput"
    GPU_UTILIZATION = "gpu_util"
    MEMORY_USAGE = "memory"
    PERPLEXITY = "perplexity"
    ACCURACY = "accuracy"
    CUSTOM = "custom"


@dataclass
class MetricPoint:
    """A single metric measurement at a point in time."""
    name: str
    value: float
    step: int
    timestamp: Optional[float] = None

    def is_nan(self) -> bool:
        """Check if the value is NaN."""
        import math
        return math.isnan(self.value)

    def is_inf(self) -> bool:
        """Check if the value is infinite."""
        import math
        return math.isinf(self.value)

    def is_valid(self) -> bool:
        """Check if the value is a valid finite number."""
        import math
        return math.isfinite(self.value)


KNOWN_METRIC_ALIASES = {
    "loss": MetricType.LOSS,
    "train_loss": MetricType.TRAIN_LOSS,
    "training_loss": MetricType.TRAIN_LOSS,
    "eval_loss": MetricType.EVAL_LOSS,
    "validation_loss": MetricType.EVAL_LOSS,
    "val_loss": MetricType.EVAL_LOSS,
    "lr": MetricType.LEARNING_RATE,
    "learning_rate": MetricType.LEARNING_RATE,
    "grad_norm": MetricType.GRADIENT_NORM,
    "gradient_norm": MetricType.GRADIENT_NORM,
    "throughput": MetricType.THROUGHPUT,
    "samples_per_second": MetricType.THROUGHPUT,
    "tokens_per_second": MetricType.THROUGHPUT,
    "gpu_util": MetricType.GPU_UTILIZATION,
    "gpu_utilization": MetricType.GPU_UTILIZATION,
    "memory": MetricType.MEMORY_USAGE,
    "memory_usage": MetricType.MEMORY_USAGE,
    "perplexity": MetricType.PERPLEXITY,
    "ppl": MetricType.PERPLEXITY,
    "accuracy": MetricType.ACCURACY,
    "acc": MetricType.ACCURACY,
}


def normalize_metric_name(name: str) -> str:
    """Normalize a metric name to its canonical form."""
    name_lower = name.lower().strip()
    if name_lower in KNOWN_METRIC_ALIASES:
        return KNOWN_METRIC_ALIASES[name_lower].value
    return name_lower
