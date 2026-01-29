#!/usr/bin/env python3
"""
Unit tests for individual detectors.

Each detector has specific behaviors and thresholds that should be tested.
"""

import math
import random
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from training_doctor.metrics.store import MetricStore
from training_doctor.detectors.learning_rate import LearningRateTooHighDetector, LearningRateTooLowDetector
from training_doctor.detectors.plateau import PlateauDetector
from training_doctor.detectors.overfitting import OverfittingDetector
from training_doctor.detectors.instability import GradientInstabilityDetector


class TestLearningRateTooHighDetector:
    """Unit tests for LearningRateTooHighDetector."""

    def test_detects_nan_loss(self):
        """Should detect NaN loss values."""
        detector = LearningRateTooHighDetector()
        store = MetricStore()

        for step in range(100):
            if step < 80:
                store.log(step=step, loss=4.0 - step * 0.02)
            else:
                store.log(step=step, loss=float('nan'))

        diag = detector.detect(store)
        assert diag is not None
        assert any('nan' in e.observation.lower() for e in diag.evidence)

    def test_requires_3_spikes_to_trigger(self):
        """Should require 3+ spikes before triggering (not just 2)."""
        detector = LearningRateTooHighDetector()

        # Test with only 2 spikes - should NOT trigger spike-based detection
        store = MetricStore()
        random.seed(42)
        for step in range(200):
            if step in [50, 100]:  # Only 2 spikes
                store.log(step=step, loss=50.0)
            else:
                store.log(step=step, loss=5.0 + random.gauss(0, 0.1))

        diag = detector.detect(store)
        # With only 2 spikes, should not have spike-based evidence
        if diag:
            spike_evidence = [e for e in diag.evidence if 'spike' in e.observation.lower()]
            assert len(spike_evidence) == 0 or 'spiked 2' not in spike_evidence[0].observation

    def test_triggers_with_3_spikes(self):
        """Should trigger with 3+ spikes within the check window."""
        detector = LearningRateTooHighDetector()

        store = MetricStore()
        random.seed(42)
        # Need enough data points and spikes within the last 100 steps (spike_check_window)
        for step in range(300):
            # 3 spikes all within the last 100 steps (200-299)
            if step in [220, 250, 280]:
                store.log(step=step, loss=50.0)
            else:
                store.log(step=step, loss=5.0 + random.gauss(0, 0.1))

        diag = detector.detect(store)
        assert diag is not None
        spike_evidence = [e for e in diag.evidence if 'spike' in e.observation.lower()]
        assert len(spike_evidence) >= 1

    def test_no_false_positive_on_healthy_cosine_decay(self):
        """Should NOT trigger on healthy cosine LR decay."""
        detector = LearningRateTooHighDetector()
        store = MetricStore()

        random.seed(42)
        total_steps = 1000
        for step in range(total_steps):
            progress = step / total_steps
            lr = 1e-4 * (0.5 * (1 + math.cos(math.pi * progress)))
            loss = 4.0 * math.exp(-step / 300) + 1.0 + random.gauss(0, 0.02)
            store.log(step=step, loss=loss, lr=lr, grad_norm=random.gauss(1.0, 0.1))

        diag = detector.detect(store)
        # Should not trigger or have low confidence
        if diag:
            assert diag.confidence < 0.5, f"False positive with confidence {diag.confidence}"

    def test_gradient_spikes_add_evidence(self):
        """Gradient spikes should add evidence when present."""
        detector = LearningRateTooHighDetector()
        store = MetricStore()

        random.seed(42)
        # Use more data and spikes within check window
        for step in range(300):
            # Loss spikes in last 100 steps
            if step in [220, 250, 280]:
                store.log(step=step, loss=50.0)
            else:
                store.log(step=step, loss=5.0 + random.gauss(0, 0.1))

            # Gradient spikes at same times
            if step in [220, 250, 280]:
                store.log(step=step, grad_norm=100.0)
            else:
                store.log(step=step, grad_norm=random.gauss(1.0, 0.1))

        diag = detector.detect(store)
        assert diag is not None
        # Should have gradient evidence
        grad_evidence = [e for e in diag.evidence if e.metric == 'grad_norm']
        assert len(grad_evidence) >= 1

    def test_slow_divergence_detection(self):
        """Should detect slow divergence (10%+ increase over 500 steps)."""
        detector = LearningRateTooHighDetector()
        store = MetricStore()

        random.seed(42)
        for step in range(600):
            if step < 100:
                loss = 4.0 - step * 0.01
            else:
                # Slow increase
                loss = 3.0 + (step - 100) * 0.005

            store.log(step=step, loss=loss + random.gauss(0, 0.02))

        diag = detector.detect(store)
        assert diag is not None
        diverge_evidence = [e for e in diag.evidence if 'diverg' in e.observation.lower()]
        assert len(diverge_evidence) >= 1


class TestLearningRateTooLowDetector:
    """Unit tests for LearningRateTooLowDetector."""

    def test_detects_flat_loss(self):
        """Should detect flat loss (barely changing)."""
        detector = LearningRateTooLowDetector()
        store = MetricStore()

        random.seed(42)
        for step in range(150):
            # Flat loss
            store.log(step=step, loss=4.0 + random.gauss(0, 0.001))

        diag = detector.detect(store)
        assert diag is not None
        assert 'barely changed' in diag.evidence[0].observation.lower()

    def test_no_trigger_on_improving_loss(self):
        """Should NOT trigger when loss is decreasing."""
        detector = LearningRateTooLowDetector()
        store = MetricStore()

        random.seed(42)
        for step in range(150):
            # Clear improvement
            store.log(step=step, loss=4.0 * math.exp(-step / 50) + 1.0)

        diag = detector.detect(store)
        assert diag is None

    def test_small_gradient_detection(self):
        """Should detect very small gradients."""
        detector = LearningRateTooLowDetector()
        store = MetricStore()

        for step in range(150):
            store.log(step=step, loss=4.0, grad_norm=1e-8)

        diag = detector.detect(store)
        assert diag is not None
        grad_evidence = [e for e in diag.evidence if e.metric == 'grad_norm']
        assert len(grad_evidence) >= 1

    def test_respects_min_data_points(self):
        """Should not trigger with insufficient data."""
        detector = LearningRateTooLowDetector()
        store = MetricStore()

        # Only 30 points (less than check_window=100)
        for step in range(30):
            store.log(step=step, loss=4.0)

        diag = detector.detect(store)
        assert diag is None


class TestPlateauDetector:
    """Unit tests for PlateauDetector."""

    def test_detects_plateau_at_high_loss(self):
        """Should detect plateau when loss is stuck at high value."""
        detector = PlateauDetector()
        store = MetricStore()

        random.seed(42)
        for step in range(500):
            if step < 100:
                loss = 4.0 - step * 0.01
            else:
                # Stuck at 3.0 (above threshold of 1.5)
                loss = 3.0 + random.gauss(0, 0.02)

            store.log(step=step, loss=loss, grad_norm=random.gauss(2.0, 0.5))

        diag = detector.detect(store)
        assert diag is not None
        assert 'plateau' in diag.problem.lower()

    def test_no_trigger_if_converged_low(self):
        """Should NOT trigger if loss is at low value (converged)."""
        detector = PlateauDetector()
        store = MetricStore()

        random.seed(42)
        for step in range(500):
            if step < 200:
                loss = 4.0 * math.exp(-step / 100)
            else:
                # Converged at 1.2 (below threshold 1.5)
                loss = 1.2 + random.gauss(0, 0.01)

            store.log(step=step, loss=loss, grad_norm=random.gauss(0.5, 0.05))

        diag = detector.detect(store)
        # Should not trigger OR have low confidence
        if diag:
            assert diag.confidence < 0.5 or 'converged' in str(diag.evidence).lower()

    def test_high_gradient_variance_adds_confidence(self):
        """High gradient variance during plateau should increase confidence."""
        detector = PlateauDetector()
        store = MetricStore()

        random.seed(42)
        for step in range(500):
            loss = 3.0 + random.gauss(0, 0.02)
            # High variance gradients
            grad_norm = random.gauss(2.0, 0.8)  # CV > 0.3
            store.log(step=step, loss=loss, grad_norm=grad_norm)

        diag = detector.detect(store)
        assert diag is not None
        grad_evidence = [e for e in diag.evidence if 'gradient' in e.observation.lower()]
        assert len(grad_evidence) >= 1

    def test_requires_200_steps_plateau(self):
        """Should require 200 steps of flat loss."""
        detector = PlateauDetector()
        store = MetricStore()

        # Only 150 steps of plateau (less than 200)
        random.seed(42)
        for step in range(150):
            store.log(step=step, loss=3.0 + random.gauss(0, 0.01))

        diag = detector.detect(store)
        # Should not have enough data to trigger plateau
        if diag:
            assert diag.confidence < 0.5


class TestOverfittingDetector:
    """Unit tests for OverfittingDetector."""

    def test_detects_train_down_eval_up(self):
        """Should detect when train decreases but eval increases."""
        detector = OverfittingDetector()
        store = MetricStore()

        random.seed(42)
        for step in range(1000):
            train_loss = 3.0 * math.exp(-step / 300) + 0.5

            if step < 400:
                eval_loss = train_loss * 1.05
            else:
                eval_loss = train_loss * 1.05 + (step - 400) * 0.002

            store.log(step=step, train_loss=train_loss)
            if step % 50 == 0:
                store.log(step=step, eval_loss=eval_loss)

        diag = detector.detect(store)
        assert diag is not None
        assert 'overfit' in diag.problem.lower()

    def test_handles_sparse_eval(self):
        """Should handle sparse eval_loss (logged every 100+ steps)."""
        detector = OverfittingDetector()
        store = MetricStore()

        random.seed(42)
        for step in range(2000):
            train_loss = 3.0 * math.exp(-step / 500) + 0.5

            if step < 800:
                eval_loss = train_loss * 1.05
            else:
                eval_loss = train_loss + (step - 800) * 0.002

            store.log(step=step, train_loss=train_loss)
            # Very sparse eval
            if step % 200 == 0:
                store.log(step=step, eval_loss=eval_loss)

        diag = detector.detect(store)
        assert diag is not None

    def test_requires_train_decreasing_and_eval_increasing(self):
        """Should require train decreasing AND eval increasing for high confidence."""
        detector = OverfittingDetector()

        # Case 1: Both decreasing proportionally (not overfitting)
        store1 = MetricStore()
        for step in range(500):
            train_loss = 3.0 * math.exp(-step / 200)
            eval_loss = train_loss * 1.05  # Both going down together
            store1.log(step=step, train_loss=train_loss)
            if step % 50 == 0:
                store1.log(step=step, eval_loss=eval_loss)

        diag1 = detector.detect(store1)
        # May detect gap ratio but should be low confidence without eval increasing
        if diag1:
            # Check that the main overfitting signal (eval increasing) is not present
            eval_increasing_evidence = [e for e in diag1.evidence
                                         if 'eval' in e.metric.lower() and 'increas' in e.observation.lower()]
            assert len(eval_increasing_evidence) == 0

        # Case 2: Train flat, eval increasing (should trigger)
        store2 = MetricStore()
        for step in range(500):
            train_loss = 1.0  # Flat and low
            eval_loss = 1.0 + step * 0.005  # Increasing
            store2.log(step=step, train_loss=train_loss)
            if step % 50 == 0:
                store2.log(step=step, eval_loss=eval_loss)

        diag2 = detector.detect(store2)
        # Eval is clearly increasing, so should detect something
        assert diag2 is not None

    def test_gap_ratio_detection(self):
        """Should detect large gap between train and eval."""
        detector = OverfittingDetector()
        store = MetricStore()

        for step in range(500):
            train_loss = 0.5  # Very low train loss
            eval_loss = 2.0   # Much higher eval loss (4x gap)
            store.log(step=step, train_loss=train_loss)
            if step % 50 == 0:
                store.log(step=step, eval_loss=eval_loss)

        diag = detector.detect(store)
        assert diag is not None
        gap_evidence = [e for e in diag.evidence if 'gap' in e.observation.lower() or 'higher' in e.observation.lower()]
        assert len(gap_evidence) >= 1


class TestGradientInstabilityDetector:
    """Unit tests for GradientInstabilityDetector."""

    def test_detects_nan_gradients(self):
        """Should detect NaN gradients."""
        detector = GradientInstabilityDetector()
        store = MetricStore()

        for step in range(100):
            if step < 80:
                store.log(step=step, loss=4.0, grad_norm=1.0)
            else:
                store.log(step=step, loss=4.0, grad_norm=float('nan'))

        diag = detector.detect(store)
        assert diag is not None
        nan_evidence = [e for e in diag.evidence if 'nan' in e.observation.lower()]
        assert len(nan_evidence) >= 1

    def test_explosion_threshold(self):
        """Should detect gradient explosion (> 10.0)."""
        detector = GradientInstabilityDetector()
        store = MetricStore()

        random.seed(42)
        for step in range(200):
            if step < 150:
                grad_norm = random.gauss(1.0, 0.1)
            else:
                grad_norm = 50.0  # Explosion

            store.log(step=step, loss=4.0, grad_norm=grad_norm)

        diag = detector.detect(store)
        assert diag is not None
        explode_evidence = [e for e in diag.evidence if 'explod' in e.observation.lower() or 'high' in e.observation.lower()]
        assert len(explode_evidence) >= 1

    def test_vanishing_threshold(self):
        """Should detect vanishing gradients (< 0.01)."""
        detector = GradientInstabilityDetector()
        store = MetricStore()

        for step in range(200):
            if step < 100:
                grad_norm = random.gauss(1.0, 0.1)
            else:
                grad_norm = 0.001  # Vanishing

            store.log(step=step, loss=4.0, grad_norm=grad_norm)

        diag = detector.detect(store)
        assert diag is not None
        vanish_evidence = [e for e in diag.evidence if 'vanish' in e.observation.lower() or 'small' in e.observation.lower()]
        assert len(vanish_evidence) >= 1

    def test_high_variance_detection(self):
        """Should detect high gradient variance."""
        detector = GradientInstabilityDetector()
        store = MetricStore()

        random.seed(42)
        for step in range(200):
            # Very high variance
            grad_norm = random.gauss(5.0, 3.0)  # CV = 0.6
            grad_norm = max(0.01, grad_norm)  # Keep positive
            store.log(step=step, loss=4.0, grad_norm=grad_norm)

        diag = detector.detect(store)
        # High variance should be detected
        if diag:
            var_evidence = [e for e in diag.evidence if 'variance' in e.observation.lower() or 'unstable' in e.observation.lower()]
            assert len(var_evidence) >= 1 or diag.confidence >= 0.3

    def test_confidence_capped_at_one(self):
        """Confidence should be capped at 1.0."""
        detector = GradientInstabilityDetector()
        store = MetricStore()

        # Multiple severe issues
        for step in range(100):
            store.log(step=step, loss=4.0, grad_norm=float('nan'))

        diag = detector.detect(store)
        assert diag is not None
        assert diag.confidence <= 1.0


def run_tests():
    """Run all tests manually without pytest."""
    import traceback

    test_classes = [
        TestLearningRateTooHighDetector,
        TestLearningRateTooLowDetector,
        TestPlateauDetector,
        TestOverfittingDetector,
        TestGradientInstabilityDetector,
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
