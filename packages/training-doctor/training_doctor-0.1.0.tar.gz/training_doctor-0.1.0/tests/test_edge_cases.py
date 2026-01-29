"""Edge case tests for train-check.

These tests verify the library handles unusual inputs correctly:
- Empty/minimal data
- NaN/Inf values
- Boundary conditions
- Extreme values
"""

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Try to import pytest, make it optional
try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False
    class DummyPytest:
        @staticmethod
        def approx(val, rel=0.01):
            return val
    pytest = DummyPytest()

from training_doctor import Doctor
from training_doctor.metrics.store import MetricStore, RollingStats


# Helper functions to replace fixtures
def make_empty_store():
    return MetricStore()

def make_store_with_nan():
    store = MetricStore()
    for step in range(100):
        if step % 10 == 0:
            store.log(step=step, loss=float('nan'))
        else:
            store.log(step=step, loss=4.0 - step * 0.02)
    return store


class TestEmptyAndMinimalData:
    """Tests for empty and minimal data scenarios."""

    def test_empty_store_no_crash(self):
        """Doctor should not crash with empty store."""
        doctor = Doctor()
        doctor.set_auto_print(False)
        # Should not raise any exception
        diagnoses = doctor.check()
        assert diagnoses == []

    def test_single_data_point(self):
        """Single data point should not trigger any detectors."""
        empty_store = make_empty_store()
        empty_store.log(step=0, loss=4.0)

        doctor = Doctor()
        doctor.set_auto_print(False)
        doctor._store = empty_store

        diagnoses = doctor.check()
        assert diagnoses == []

    def test_exactly_min_data_points(self):
        """Test at exactly min_data_points boundary."""
        store = MetricStore()
        # Most detectors require min_data_points=10
        for step in range(10):
            store.log(step=step, loss=4.0 - step * 0.1)

        doctor = Doctor()
        doctor.set_auto_print(False)
        doctor._store = store

        # Should not crash
        diagnoses = doctor.check()
        # May or may not have diagnoses, but should not crash

    def test_one_below_min_data_points(self):
        """Test at one below min_data_points."""
        store = MetricStore()
        for step in range(9):  # One below typical min of 10
            store.log(step=step, loss=4.0)

        doctor = Doctor()
        doctor.set_auto_print(False)
        doctor._store = store

        # Most detectors should not run
        diagnoses = doctor.check()
        assert diagnoses == []


class TestNaNAndInfValues:
    """Tests for NaN and Inf value handling."""

    def test_all_nan_values(self):
        """Store with all NaN values should not crash."""
        store = MetricStore()
        for step in range(100):
            store.log(step=step, loss=float('nan'))

        # RollingStats should have count=0 (NaN skipped)
        stats = store.compute_window_stats("loss", 50)
        assert stats.count == 0

    def test_fifty_percent_nan(self):
        """Store with 50% NaN values should work with remaining values."""
        store = MetricStore()
        for step in range(100):
            if step % 2 == 0:
                store.log(step=step, loss=float('nan'))
            else:
                store.log(step=step, loss=4.0 - step * 0.02)

        # Should have stats for non-NaN values
        stats = store.compute_window_stats("loss", 100)
        assert stats.count == 50  # Only non-NaN values counted

    def test_all_inf_values(self):
        """Store with all Inf values should not crash."""
        store = MetricStore()
        for step in range(100):
            store.log(step=step, loss=float('inf'))

        # RollingStats should skip Inf
        stats = store.compute_window_stats("loss", 50)
        assert stats.count == 0

    def test_mixed_nan_inf_valid(self):
        """Store with mix of NaN, Inf, and valid values."""
        store = MetricStore()
        for step in range(100):
            if step % 3 == 0:
                store.log(step=step, loss=float('nan'))
            elif step % 3 == 1:
                store.log(step=step, loss=float('inf'))
            else:
                store.log(step=step, loss=4.0 - step * 0.02)

        # Should only count valid values (step % 3 == 2, so 0,1,2,3,...99 gives 33 values)
        stats = store.compute_window_stats("loss", 100)
        assert stats.count == 33  # 100/3 = 33 valid values

    def test_nan_detection(self):
        """detect_nan_or_inf should find NaN values."""
        store_with_nan = make_store_with_nan()
        nan_points = store_with_nan.detect_nan_or_inf("loss", 100)
        assert len(nan_points) == 10  # Every 10th value is NaN

    def test_negative_inf(self):
        """Negative Inf should be handled like positive Inf."""
        store = MetricStore()
        for step in range(50):
            store.log(step=step, loss=float('-inf'))

        stats = store.compute_window_stats("loss", 50)
        assert stats.count == 0


class TestBoundaryConditions:
    """Tests for boundary condition handling."""

    def test_loss_below_plateau_threshold(self):
        """Loss below plateau threshold (1.5) should not flag plateau."""
        store = MetricStore()
        random.seed(42)
        for step in range(300):
            # Plateau below threshold - converged model
            store.log(step=step, loss=1.4 + random.gauss(0, 0.001))
            store.log(step=step, grad_norm=random.gauss(1.0, 0.1))

        doctor = Doctor()
        doctor.set_auto_print(False)
        doctor._store = store

        # Should not trigger plateau (loss below min_loss_for_plateau=1.5)
        diagnoses = doctor.check()
        plateau_diagnoses = [d for d in diagnoses if 'plateau' in d.problem.lower()]
        assert len(plateau_diagnoses) == 0

    def test_relative_change_at_threshold(self):
        """Test relative change exactly at threshold (0.01 = 1%)."""
        store = MetricStore()
        # Create loss that changes by exactly 1% over 200 steps
        base_loss = 3.0
        for step in range(200):
            # Linear change of exactly 1% total
            loss = base_loss * (1 - 0.01 * (step / 199))
            store.log(step=step, loss=loss)

        stats = store.compute_window_stats("loss", 200)
        # Relative change should be very close to 1%
        assert abs(abs(stats.relative_change) - 0.01) < 0.001

    def test_cooldown_exactly_at_boundary(self):
        """Test cooldown at exactly N steps vs N-1 steps."""
        store = MetricStore()
        random.seed(42)

        # Create data that would trigger LR too high
        for step in range(400):
            if step < 100:
                loss = 4.0
            elif step < 200:
                loss = float('nan')  # Should trigger at ~step 200
            else:
                loss = 4.0
            store.log(step=step, loss=loss, lr=0.01)

        doctor = Doctor()
        doctor.set_auto_print(False)
        doctor._store = store

        # Run check multiple times
        store._current_step = 200
        d1 = doctor.check()

        # Check just before cooldown expires (cooldown=200)
        store._current_step = 399
        d2 = doctor.check()

        # Check exactly at cooldown
        store._current_step = 400
        d3 = doctor.check()

        # d2 should be empty (still in cooldown), d3 might have diagnoses

    def test_window_size_equals_data_points(self):
        """Window size exactly equals available data points."""
        store = MetricStore()
        for step in range(100):
            store.log(step=step, loss=4.0 - step * 0.02)

        # Window of exactly 100 when we have 100 points
        stats = store.compute_window_stats("loss", 100)
        assert stats.count == 100

    def test_window_larger_than_data(self):
        """Window larger than available data should use all data."""
        store = MetricStore()
        for step in range(50):
            store.log(step=step, loss=4.0 - step * 0.02)

        # Request window of 100 when we only have 50
        stats = store.compute_window_stats("loss", 100)
        assert stats.count == 50


class TestExtremeValues:
    """Tests for extreme value handling."""

    def test_very_large_loss(self):
        """Very large loss values (1e10) should not crash."""
        store = MetricStore()
        for step in range(100):
            store.log(step=step, loss=1e10 - step * 1e7)

        doctor = Doctor()
        doctor.set_auto_print(False)
        doctor._store = store

        # Should not crash
        diagnoses = doctor.check()
        # May have diagnoses about issues, but should not crash

    def test_very_small_loss(self):
        """Very small loss values (1e-10) should not crash."""
        store = MetricStore()
        for step in range(100):
            store.log(step=step, loss=1e-10 + step * 1e-12)

        doctor = Doctor()
        doctor.set_auto_print(False)
        doctor._store = store

        diagnoses = doctor.check()
        # Should not crash

    def test_negative_loss(self):
        """Negative loss values (valid for some loss functions) should not crash."""
        store = MetricStore()
        for step in range(100):
            # Negative loss like in policy gradient
            store.log(step=step, loss=-10.0 + step * 0.1)

        doctor = Doctor()
        doctor.set_auto_print(False)
        doctor._store = store

        diagnoses = doctor.check()
        # Should not crash

    def test_very_large_lr(self):
        """Very large learning rate (1.0) should not crash."""
        store = MetricStore()
        for step in range(100):
            store.log(step=step, loss=4.0, lr=1.0)

        doctor = Doctor()
        doctor.set_auto_print(False)
        doctor._store = store

        diagnoses = doctor.check()
        # Should not crash

    def test_very_small_lr(self):
        """Very small learning rate (1e-12) should not crash."""
        store = MetricStore()
        for step in range(100):
            store.log(step=step, loss=4.0, lr=1e-12)

        doctor = Doctor()
        doctor.set_auto_print(False)
        doctor._store = store

        diagnoses = doctor.check()
        # Should not crash

    def test_zero_gradient_norm(self):
        """Exactly zero gradient norm should not crash."""
        store = MetricStore()
        for step in range(100):
            store.log(step=step, loss=4.0 - step * 0.02, grad_norm=0.0)

        doctor = Doctor()
        doctor.set_auto_print(False)
        doctor._store = store

        diagnoses = doctor.check()
        # Should not crash


class TestOutOfOrderAndDuplicateSteps:
    """Tests for step ordering edge cases."""

    def test_out_of_order_steps(self):
        """Out-of-order steps should be handled gracefully."""
        store = MetricStore()
        # Log steps out of order
        store.log(step=0, loss=4.0)
        store.log(step=5, loss=3.5)
        store.log(step=2, loss=3.8)
        store.log(step=10, loss=3.0)
        store.log(step=7, loss=3.3)

        # Should have all 5 points
        assert store.count("loss") == 5

    def test_duplicate_steps(self):
        """Duplicate steps should keep both values (append behavior)."""
        store = MetricStore()
        store.log(step=0, loss=4.0)
        store.log(step=0, loss=3.5)  # Duplicate step
        store.log(step=0, loss=3.0)  # Another duplicate

        # All values should be stored
        assert store.count("loss") == 3

    def test_negative_step_values(self):
        """Negative step values should not crash."""
        store = MetricStore()
        store.log(step=-10, loss=4.0)
        store.log(step=-5, loss=3.5)
        store.log(step=0, loss=3.0)

        assert store.count("loss") == 3


class TestRollingStatsEdgeCases:
    """Tests for RollingStats edge cases."""

    def test_rolling_stats_all_identical(self):
        """All identical values should have variance=0, std=0."""
        stats = RollingStats()
        for _ in range(100):
            stats.update(5.0)

        assert stats.variance == 0.0
        assert stats.std == 0.0
        assert stats.mean == 5.0

    def test_rolling_stats_two_values(self):
        """Two values should compute correct variance."""
        stats = RollingStats()
        stats.update(0.0)
        stats.update(10.0)

        assert stats.mean == 5.0
        assert stats.variance == 50.0  # Sample variance
        # std should be sqrt(50) = 7.07...
        assert abs(stats.std - 7.07) < 0.1

    def test_rolling_stats_single_value(self):
        """Single value should have variance=0."""
        stats = RollingStats()
        stats.update(5.0)

        assert stats.count == 1
        assert stats.mean == 5.0
        assert stats.variance == 0.0

    def test_rolling_stats_properties(self):
        """Test computed properties (range, change, relative_change)."""
        stats = RollingStats()
        stats.update(10.0)
        stats.update(5.0)
        stats.update(15.0)

        assert stats.range == 10.0  # 15 - 5
        assert stats.change == 5.0  # 15 - 10
        assert stats.relative_change == 0.5  # (15-10)/10


class TestDetectTrendEdgeCases:
    """Tests for detect_trend edge cases."""

    def test_trend_with_two_points(self):
        """Trend detection with < 3 points should return unknown."""
        store = MetricStore()
        store.log(step=0, loss=4.0)
        store.log(step=1, loss=3.5)

        trend = store.detect_trend("loss", window_size=10)
        assert trend == "unknown"

    def test_trend_constant_values(self):
        """Constant values should return stable."""
        store = MetricStore()
        for step in range(100):
            store.log(step=step, loss=5.0)

        trend = store.detect_trend("loss", window_size=50)
        assert trend == "stable"

    def test_trend_all_nan(self):
        """All NaN values should return unknown."""
        store = MetricStore()
        for step in range(100):
            store.log(step=step, loss=float('nan'))

        trend = store.detect_trend("loss", window_size=50)
        assert trend == "unknown"


class TestDetectSpikesEdgeCases:
    """Tests for detect_spikes edge cases."""

    def test_spikes_with_four_points(self):
        """Spike detection with < 5 points should return empty."""
        store = MetricStore()
        for step in range(4):
            store.log(step=step, loss=4.0 if step != 2 else 100.0)

        spikes = store.detect_spikes("loss", window_size=10)
        assert spikes == []

    def test_spikes_all_identical(self):
        """All identical values should have no spikes (std=0)."""
        store = MetricStore()
        for step in range(100):
            store.log(step=step, loss=5.0)

        spikes = store.detect_spikes("loss", window_size=50)
        assert spikes == []

    def test_spikes_with_nan_mixed(self):
        """Spike detection should ignore NaN values and still find obvious spikes."""
        store = MetricStore()
        random.seed(42)
        for step in range(100):
            if step % 20 == 0:  # Only every 20th is NaN (5 total)
                store.log(step=step, loss=float('nan'))
            elif step == 50:
                store.log(step=step, loss=100.0)  # Massive spike (20x normal)
            else:
                # Normal values with slight noise so std isn't zero
                store.log(step=step, loss=5.0 + random.gauss(0, 0.1))

        spikes = store.detect_spikes("loss", window_size=100, threshold_std=3.0)
        # Should detect the spike at step 50
        assert len(spikes) >= 1


def run_tests():
    """Run all tests manually without pytest."""
    import traceback

    test_classes = [
        TestEmptyAndMinimalData,
        TestNaNAndInfValues,
        TestBoundaryConditions,
        TestExtremeValues,
        TestOutOfOrderAndDuplicateSteps,
        TestRollingStatsEdgeCases,
        TestDetectTrendEdgeCases,
        TestDetectSpikesEdgeCases,
    ]

    passed = 0
    failed = 0
    errors = []

    for test_class in test_classes:
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                try:
                    method = getattr(instance, method_name)
                    method()
                    print(f'PASS: {test_class.__name__}.{method_name}')
                    passed += 1
                except AssertionError as e:
                    print(f'FAIL: {test_class.__name__}.{method_name}: {e}')
                    failed += 1
                    errors.append((test_class.__name__, method_name, str(e)))
                except Exception as e:
                    print(f'ERROR: {test_class.__name__}.{method_name}: {type(e).__name__}: {e}')
                    failed += 1
                    errors.append((test_class.__name__, method_name, f'{type(e).__name__}: {e}'))

    print(f'\n========================================')
    print(f'Results: {passed} passed, {failed} failed')

    if errors:
        print(f'\nFailure details:')
        for cls, method, err in errors[:10]:  # Show first 10 failures
            print(f'  {cls}.{method}:')
            print(f'    {err[:200]}')

    return failed == 0


if __name__ == "__main__":
    if HAS_PYTEST:
        import pytest
        pytest.main([__file__, "-v"])
    else:
        success = run_tests()
        sys.exit(0 if success else 1)
