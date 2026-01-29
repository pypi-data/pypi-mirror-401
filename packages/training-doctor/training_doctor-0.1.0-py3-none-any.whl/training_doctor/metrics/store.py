import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Iterator

from .types import MetricPoint, normalize_metric_name


@dataclass
class RollingStats:
    """Efficiently computed rolling statistics for a metric."""
    count: int = 0
    mean: float = 0.0
    variance: float = 0.0
    min_value: float = float('inf')
    max_value: float = float('-inf')
    last_value: float = 0.0
    first_value: float = 0.0
    _m2: float = 0.0  # For Welford's algorithm

    def update(self, value: float) -> None:
        """Update statistics with a new value using Welford's online algorithm."""
        if not math.isfinite(value):
            return

        self.count += 1
        if self.count == 1:
            self.first_value = value

        delta = value - self.mean
        self.mean += delta / self.count
        delta2 = value - self.mean
        self._m2 += delta * delta2

        if self.count > 1:
            self.variance = self._m2 / (self.count - 1)

        self.min_value = min(self.min_value, value)
        self.max_value = max(self.max_value, value)
        self.last_value = value

    @property
    def std(self) -> float:
        """Standard deviation."""
        return math.sqrt(self.variance) if self.variance > 0 else 0.0

    @property
    def range(self) -> float:
        """Range (max - min)."""
        if self.count == 0:
            return 0.0
        return self.max_value - self.min_value

    @property
    def change(self) -> float:
        """Change from first to last value."""
        if self.count < 2:
            return 0.0
        return self.last_value - self.first_value

    @property
    def relative_change(self) -> float:
        """Relative change from first to last value."""
        if self.count < 2 or self.first_value == 0:
            return 0.0
        return (self.last_value - self.first_value) / abs(self.first_value)


class MetricStore:
    """Time-series storage for training metrics with efficient querying."""

    def __init__(self):
        self._data: Dict[str, List[MetricPoint]] = defaultdict(list)
        self._stats: Dict[str, RollingStats] = defaultdict(RollingStats)
        self._current_step: int = 0

    def log(self, step: int, **metrics: float) -> None:
        """Log metrics at a given step."""
        self._current_step = max(self._current_step, step)

        for name, value in metrics.items():
            normalized_name = normalize_metric_name(name)
            point = MetricPoint(name=normalized_name, value=value, step=step)
            self._data[normalized_name].append(point)
            self._stats[normalized_name].update(value)

    def get(self, metric: str) -> List[MetricPoint]:
        """Get all points for a metric."""
        return self._data.get(normalize_metric_name(metric), [])

    def get_last(self, metric: str, n: int = 1) -> List[MetricPoint]:
        """Get the last N points for a metric up to current_step."""
        points = self.get(metric)
        # Filter to points at or before current step
        visible_points = [p for p in points if p.step <= self._current_step]
        return visible_points[-n:] if visible_points else []

    def get_window(self, metric: str, start_step: int, end_step: Optional[int] = None) -> List[MetricPoint]:
        """Get points within a step window."""
        points = self.get(metric)
        end = end_step if end_step is not None else self._current_step + 1
        return [p for p in points if start_step <= p.step < end]

    def get_stats(self, metric: str) -> RollingStats:
        """Get rolling statistics for a metric."""
        return self._stats.get(normalize_metric_name(metric), RollingStats())

    def compute_window_stats(self, metric: str, window_size: int) -> RollingStats:
        """Compute statistics over the last N points."""
        points = self.get_last(metric, window_size)
        stats = RollingStats()
        for p in points:
            stats.update(p.value)
        return stats

    def has_metric(self, metric: str) -> bool:
        """Check if a metric exists."""
        return normalize_metric_name(metric) in self._data

    def get_metrics(self) -> List[str]:
        """Get all metric names."""
        return list(self._data.keys())

    @property
    def current_step(self) -> int:
        """Get the current (latest) step."""
        return self._current_step

    def count(self, metric: str) -> int:
        """Get the number of points for a metric."""
        return len(self.get(metric))

    def get_latest_value(self, metric: str) -> Optional[float]:
        """Get the most recent value for a metric."""
        points = self.get_last(metric, 1)
        return points[0].value if points else None

    def detect_trend(self, metric: str, window_size: int = 10) -> str:
        """Detect trend direction: 'increasing', 'decreasing', 'stable', or 'unknown'."""
        points = self.get_last(metric, window_size)
        if len(points) < 3:
            return "unknown"

        values = [p.value for p in points if math.isfinite(p.value)]
        if len(values) < 3:
            return "unknown"

        # Simple linear regression slope
        n = len(values)
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n

        numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return "stable"

        slope = numerator / denominator
        # Normalize slope by the mean to get relative change
        relative_slope = slope / abs(y_mean) if y_mean != 0 else slope

        if relative_slope > 0.01:
            return "increasing"
        elif relative_slope < -0.01:
            return "decreasing"
        else:
            return "stable"

    def detect_nan_or_inf(self, metric: str, window_size: int = 10) -> List[MetricPoint]:
        """Find NaN or Inf values in recent history."""
        points = self.get_last(metric, window_size)
        return [p for p in points if not p.is_valid()]

    def detect_spikes(
        self, metric: str, window_size: int = 20, threshold_std: float = 3.0
    ) -> List[MetricPoint]:
        """Detect values that are statistical outliers."""
        points = self.get_last(metric, window_size)
        if len(points) < 5:
            return []

        values = [p.value for p in points if p.is_valid()]
        if len(values) < 5:
            return []

        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = math.sqrt(variance) if variance > 0 else 0

        if std == 0:
            return []

        spikes = []
        for p in points:
            if p.is_valid() and abs(p.value - mean) > threshold_std * std:
                spikes.append(p)

        return spikes

    def clear(self) -> None:
        """Clear all stored metrics."""
        self._data.clear()
        self._stats.clear()
        self._current_step = 0

    def __len__(self) -> int:
        """Total number of data points across all metrics."""
        return sum(len(points) for points in self._data.values())

    def __iter__(self) -> Iterator[Tuple[str, List[MetricPoint]]]:
        """Iterate over (metric_name, points) pairs."""
        return iter(self._data.items())
