#!/usr/bin/env python3
"""
Unit tests for MetricStore and RollingStats.

These tests verify the core data storage and statistical computation functionality.
"""

import math
import random
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from training_doctor.metrics.store import MetricStore, RollingStats


class TestRollingStats:
    """Unit tests for RollingStats class."""

    def test_empty_stats(self):
        """Empty stats should have sensible defaults."""
        stats = RollingStats()
        assert stats.count == 0
        assert stats.mean == 0.0
        assert stats.variance == 0.0
        assert stats.std == 0.0
        assert stats.min_value == float('inf')
        assert stats.max_value == float('-inf')

    def test_single_update(self):
        """Single value update."""
        stats = RollingStats()
        stats.update(5.0)

        assert stats.count == 1
        assert stats.mean == 5.0
        assert stats.variance == 0.0
        assert stats.std == 0.0
        assert stats.first_value == 5.0
        assert stats.last_value == 5.0
        assert stats.min_value == 5.0
        assert stats.max_value == 5.0

    def test_multiple_updates(self):
        """Multiple updates should compute correct statistics."""
        stats = RollingStats()
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        for v in values:
            stats.update(v)

        assert stats.count == 5
        assert stats.mean == 3.0
        assert stats.first_value == 1.0
        assert stats.last_value == 5.0
        assert stats.min_value == 1.0
        assert stats.max_value == 5.0
        # Variance of [1,2,3,4,5] = 2.5
        assert abs(stats.variance - 2.5) < 0.01
        assert abs(stats.std - math.sqrt(2.5)) < 0.01

    def test_nan_skipped(self):
        """NaN values should be silently skipped."""
        stats = RollingStats()
        stats.update(1.0)
        stats.update(float('nan'))
        stats.update(3.0)

        assert stats.count == 2
        assert stats.mean == 2.0
        assert stats.first_value == 1.0
        assert stats.last_value == 3.0

    def test_inf_skipped(self):
        """Inf values should be silently skipped."""
        stats = RollingStats()
        stats.update(1.0)
        stats.update(float('inf'))
        stats.update(float('-inf'))
        stats.update(5.0)

        assert stats.count == 2
        assert stats.mean == 3.0

    def test_negative_inf_skipped(self):
        """Negative Inf should be skipped."""
        stats = RollingStats()
        stats.update(-float('inf'))
        stats.update(5.0)

        assert stats.count == 1
        assert stats.mean == 5.0

    def test_all_identical_values(self):
        """All identical values should have variance=0, std=0."""
        stats = RollingStats()
        for _ in range(100):
            stats.update(5.0)

        assert stats.count == 100
        assert stats.mean == 5.0
        assert stats.variance == 0.0
        assert stats.std == 0.0

    def test_range_property(self):
        """Range should be max - min."""
        stats = RollingStats()
        stats.update(1.0)
        stats.update(10.0)
        stats.update(5.0)

        assert stats.range == 9.0

    def test_range_empty(self):
        """Empty stats should have range 0."""
        stats = RollingStats()
        assert stats.range == 0.0

    def test_change_property(self):
        """Change should be last - first."""
        stats = RollingStats()
        stats.update(10.0)
        stats.update(5.0)
        stats.update(3.0)

        assert stats.change == -7.0  # 3.0 - 10.0

    def test_change_single_value(self):
        """Change with single value should be 0."""
        stats = RollingStats()
        stats.update(5.0)
        assert stats.change == 0.0

    def test_relative_change(self):
        """Relative change should be (last - first) / |first|."""
        stats = RollingStats()
        stats.update(10.0)
        stats.update(15.0)

        assert stats.relative_change == 0.5  # (15-10)/10

    def test_relative_change_zero_first(self):
        """Relative change with first=0 should be 0."""
        stats = RollingStats()
        stats.update(0.0)
        stats.update(10.0)

        assert stats.relative_change == 0.0

    def test_relative_change_negative_first(self):
        """Relative change with negative first value."""
        stats = RollingStats()
        stats.update(-10.0)
        stats.update(-5.0)

        # (-5 - (-10)) / |-10| = 5/10 = 0.5
        assert abs(stats.relative_change - 0.5) < 0.01

    def test_welford_accuracy(self):
        """Welford's algorithm should be numerically stable."""
        stats = RollingStats()
        random.seed(42)

        # Large offset with small variance - classic test for numerical stability
        values = [1000000 + random.gauss(0, 0.1) for _ in range(1000)]
        for v in values:
            stats.update(v)

        # Mean should be close to 1000000
        assert abs(stats.mean - 1000000) < 1
        # Std should be close to 0.1
        assert abs(stats.std - 0.1) < 0.05


class TestMetricStore:
    """Unit tests for MetricStore class."""

    def test_empty_store(self):
        """Empty store should return sensible defaults."""
        store = MetricStore()

        assert len(store) == 0
        assert store.current_step == 0
        assert store.get_metrics() == []
        assert not store.has_metric("loss")
        assert store.get("loss") == []
        assert store.get_latest_value("loss") is None

    def test_basic_logging(self):
        """Basic metric logging."""
        store = MetricStore()
        store.log(step=0, loss=4.0)
        store.log(step=1, loss=3.5)

        assert len(store) == 2
        assert store.current_step == 1
        assert store.has_metric("loss")
        assert "loss" in store.get_metrics()

    def test_multiple_metrics(self):
        """Logging multiple metrics at once."""
        store = MetricStore()
        store.log(step=0, loss=4.0, lr=1e-4, grad_norm=1.0)

        assert len(store) == 3
        assert store.has_metric("loss")
        assert store.has_metric("lr")
        assert store.has_metric("grad_norm")

    def test_get_points(self):
        """Get all points for a metric."""
        store = MetricStore()
        store.log(step=0, loss=4.0)
        store.log(step=1, loss=3.5)
        store.log(step=2, loss=3.0)

        points = store.get("loss")
        assert len(points) == 3
        assert points[0].value == 4.0
        assert points[1].value == 3.5
        assert points[2].value == 3.0

    def test_get_last(self):
        """Get last N points."""
        store = MetricStore()
        for i in range(10):
            store.log(step=i, loss=float(i))

        last_3 = store.get_last("loss", 3)
        assert len(last_3) == 3
        assert last_3[0].value == 7.0
        assert last_3[1].value == 8.0
        assert last_3[2].value == 9.0

    def test_get_last_fewer_than_n(self):
        """Get last N when fewer than N points exist."""
        store = MetricStore()
        store.log(step=0, loss=1.0)
        store.log(step=1, loss=2.0)

        last_10 = store.get_last("loss", 10)
        assert len(last_10) == 2

    def test_get_latest_value(self):
        """Get most recent value."""
        store = MetricStore()
        store.log(step=0, loss=4.0)
        store.log(step=1, loss=3.5)
        store.log(step=2, loss=3.0)

        assert store.get_latest_value("loss") == 3.0

    def test_get_window(self):
        """Get points within step window."""
        store = MetricStore()
        for i in range(10):
            store.log(step=i, loss=float(i))

        window = store.get_window("loss", start_step=3, end_step=7)
        assert len(window) == 4
        assert window[0].step == 3
        assert window[-1].step == 6

    def test_get_window_open_end(self):
        """Get window with open end (to current step)."""
        store = MetricStore()
        for i in range(10):
            store.log(step=i, loss=float(i))

        window = store.get_window("loss", start_step=5)
        assert len(window) == 5
        assert window[0].step == 5
        assert window[-1].step == 9

    def test_out_of_order_steps(self):
        """Out of order steps should be stored correctly."""
        store = MetricStore()
        store.log(step=5, loss=5.0)
        store.log(step=3, loss=3.0)
        store.log(step=7, loss=7.0)

        points = store.get("loss")
        assert len(points) == 3
        # Points stored in logging order
        assert points[0].step == 5
        assert points[1].step == 3
        assert points[2].step == 7

        # Current step should be max seen
        assert store.current_step == 7

    def test_duplicate_steps(self):
        """Duplicate steps should both be stored."""
        store = MetricStore()
        store.log(step=5, loss=5.0)
        store.log(step=5, loss=5.5)  # Same step, different value

        points = store.get("loss")
        assert len(points) == 2
        assert points[0].value == 5.0
        assert points[1].value == 5.5

    def test_count(self):
        """Count points for a metric."""
        store = MetricStore()
        for i in range(15):
            store.log(step=i, loss=float(i))

        assert store.count("loss") == 15
        assert store.count("nonexistent") == 0

    def test_get_stats(self):
        """Get rolling stats for a metric."""
        store = MetricStore()
        store.log(step=0, loss=1.0)
        store.log(step=1, loss=2.0)
        store.log(step=2, loss=3.0)

        stats = store.get_stats("loss")
        assert stats.count == 3
        assert stats.mean == 2.0

    def test_compute_window_stats(self):
        """Compute stats over last N points."""
        store = MetricStore()
        for i in range(100):
            store.log(step=i, loss=float(i))

        stats = store.compute_window_stats("loss", 10)
        # Last 10 values: 90-99
        assert stats.count == 10
        assert stats.mean == 94.5
        assert stats.first_value == 90.0
        assert stats.last_value == 99.0

    def test_compute_window_stats_larger_than_data(self):
        """Window larger than data should use all data."""
        store = MetricStore()
        store.log(step=0, loss=1.0)
        store.log(step=1, loss=2.0)
        store.log(step=2, loss=3.0)

        stats = store.compute_window_stats("loss", 100)
        assert stats.count == 3
        assert stats.mean == 2.0

    def test_detect_trend_increasing(self):
        """Detect increasing trend."""
        store = MetricStore()
        for i in range(20):
            store.log(step=i, loss=float(i))

        trend = store.detect_trend("loss", window_size=10)
        assert trend == "increasing"

    def test_detect_trend_decreasing(self):
        """Detect decreasing trend."""
        store = MetricStore()
        for i in range(20):
            store.log(step=i, loss=float(20 - i))

        trend = store.detect_trend("loss", window_size=10)
        assert trend == "decreasing"

    def test_detect_trend_stable(self):
        """Detect stable (no clear trend)."""
        store = MetricStore()
        random.seed(42)
        for i in range(20):
            store.log(step=i, loss=5.0 + random.gauss(0, 0.001))

        trend = store.detect_trend("loss", window_size=10)
        assert trend == "stable"

    def test_detect_trend_insufficient_data(self):
        """Insufficient data returns unknown."""
        store = MetricStore()
        store.log(step=0, loss=1.0)
        store.log(step=1, loss=2.0)

        trend = store.detect_trend("loss", window_size=10)
        assert trend == "unknown"

    def test_detect_nan_or_inf(self):
        """Detect NaN and Inf values."""
        store = MetricStore()
        store.log(step=0, loss=1.0)
        store.log(step=1, loss=float('nan'))
        store.log(step=2, loss=2.0)
        store.log(step=3, loss=float('inf'))
        store.log(step=4, loss=3.0)

        invalid = store.detect_nan_or_inf("loss", window_size=10)
        assert len(invalid) == 2
        assert invalid[0].step == 1  # NaN
        assert invalid[1].step == 3  # Inf

    def test_detect_nan_vs_inf(self):
        """Distinguish between NaN and Inf detection."""
        store = MetricStore()
        store.log(step=0, loss=float('nan'))
        store.log(step=1, loss=float('inf'))
        store.log(step=2, loss=float('-inf'))

        invalid = store.detect_nan_or_inf("loss", window_size=10)
        assert len(invalid) == 3

        # Check individual values
        assert math.isnan(invalid[0].value)
        assert math.isinf(invalid[1].value) and invalid[1].value > 0
        assert math.isinf(invalid[2].value) and invalid[2].value < 0

    def test_detect_spikes(self):
        """Detect statistical outliers."""
        store = MetricStore()
        random.seed(42)
        for i in range(100):
            if i == 50:
                store.log(step=i, loss=100.0)  # Spike
            else:
                store.log(step=i, loss=5.0 + random.gauss(0, 0.1))

        spikes = store.detect_spikes("loss", window_size=100, threshold_std=3.0)
        assert len(spikes) >= 1
        assert any(s.step == 50 for s in spikes)

    def test_detect_spikes_insufficient_data(self):
        """Spikes detection with insufficient data."""
        store = MetricStore()
        store.log(step=0, loss=1.0)
        store.log(step=1, loss=2.0)

        spikes = store.detect_spikes("loss", window_size=10)
        assert spikes == []

    def test_clear(self):
        """Clear all stored metrics."""
        store = MetricStore()
        store.log(step=0, loss=1.0)
        store.log(step=1, loss=2.0)

        store.clear()

        assert len(store) == 0
        assert store.current_step == 0
        assert not store.has_metric("loss")

    def test_iteration(self):
        """Iterate over metric data."""
        store = MetricStore()
        store.log(step=0, loss=1.0, lr=1e-4)
        store.log(step=1, loss=2.0, lr=1e-4)

        metrics = dict(store)
        assert "loss" in metrics
        assert "lr" in metrics
        assert len(metrics["loss"]) == 2
        assert len(metrics["lr"]) == 2


class TestMetricNormalization:
    """Tests for metric name normalization."""

    def test_case_insensitivity(self):
        """Metric names should be case insensitive."""
        store = MetricStore()
        store.log(step=0, LOSS=1.0)
        store.log(step=1, Loss=2.0)
        store.log(step=2, loss=3.0)

        # All should refer to same metric
        assert store.count("loss") == 3
        assert store.count("LOSS") == 3
        assert store.count("Loss") == 3

    def test_common_aliases(self):
        """Common metric aliases should normalize."""
        store = MetricStore()

        # These should all normalize to 'loss'
        store.log(step=0, loss=1.0)
        store.log(step=1, train_loss=2.0)

        # These should all normalize to 'lr'
        store.log(step=0, lr=1e-4)
        store.log(step=1, learning_rate=2e-4)

        assert store.has_metric("loss")
        assert store.has_metric("train_loss")
        assert store.has_metric("lr")
        assert store.has_metric("learning_rate")


def run_tests():
    """Run all tests manually without pytest."""
    import traceback

    test_classes = [
        TestRollingStats,
        TestMetricStore,
        TestMetricNormalization,
    ]

    passed = 0
    failed = 0

    for test_class in test_classes:
        instance = test_class()
        for method_name in sorted(dir(instance)):
            if method_name.startswith('test_'):
                try:
                    method = getattr(instance, method_name)
                    method()
                    print(f"PASS: {test_class.__name__}.{method_name}")
                    passed += 1
                except Exception as e:
                    print(f"FAIL: {test_class.__name__}.{method_name}")
                    print(f"  Error: {e}")
                    traceback.print_exc()
                    failed += 1

    print(f"\n{'=' * 40}")
    print(f"Results: {passed} passed, {failed} failed")

    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
