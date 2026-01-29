#!/usr/bin/env python3
"""
Unit tests for BaseDetector and metric types.

These tests verify the detector base class functionality and metric name handling.
"""

import math
from pathlib import Path
import sys
from typing import List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from training_doctor.metrics.store import MetricStore
from training_doctor.metrics.types import (
    MetricPoint, MetricType, KNOWN_METRIC_ALIASES, normalize_metric_name
)
from training_doctor.detectors.base import BaseDetector
from training_doctor.diagnosis import Diagnosis, Evidence, Severity


# Test implementation of BaseDetector
class TestDetector(BaseDetector):
    """A test detector that always finds an issue after enough data."""

    name = "test_detector"
    description = "Test detector for unit testing"
    min_data_points = 10
    cooldown_steps = 50
    check_interval = None

    def __init__(self, confidence: float = 0.8):
        super().__init__()
        self._confidence = confidence
        self._should_detect = True

    @property
    def required_metrics(self) -> List[str]:
        return ["loss"]

    def set_should_detect(self, should: bool):
        self._should_detect = should

    def set_confidence(self, conf: float):
        self._confidence = conf

    def detect(self, store: MetricStore) -> Optional[Diagnosis]:
        if not self._should_detect:
            return None

        return Diagnosis(
            problem="Test issue detected",
            explanation="This is a test diagnosis.",
            evidence=[Evidence(metric="loss", observation="Test observation")],
            suggestions=["Test suggestion"],
            confidence=self._confidence,
            severity=Severity.WARNING,
        )


class TestMetricPoint:
    """Unit tests for MetricPoint class."""

    def test_basic_creation(self):
        """Create a basic MetricPoint."""
        point = MetricPoint(name="loss", value=4.5, step=0)

        assert point.name == "loss"
        assert point.value == 4.5
        assert point.step == 0
        assert point.timestamp is None

    def test_with_timestamp(self):
        """Create MetricPoint with timestamp."""
        point = MetricPoint(name="loss", value=4.5, step=0, timestamp=1234567890.0)

        assert point.timestamp == 1234567890.0

    def test_is_nan(self):
        """Check NaN detection."""
        nan_point = MetricPoint(name="loss", value=float('nan'), step=0)
        normal_point = MetricPoint(name="loss", value=4.5, step=0)

        assert nan_point.is_nan() is True
        assert normal_point.is_nan() is False

    def test_is_inf(self):
        """Check Inf detection."""
        inf_point = MetricPoint(name="loss", value=float('inf'), step=0)
        neg_inf_point = MetricPoint(name="loss", value=float('-inf'), step=0)
        normal_point = MetricPoint(name="loss", value=4.5, step=0)

        assert inf_point.is_inf() is True
        assert neg_inf_point.is_inf() is True
        assert normal_point.is_inf() is False

    def test_is_valid(self):
        """Check valid (finite) detection."""
        valid_point = MetricPoint(name="loss", value=4.5, step=0)
        nan_point = MetricPoint(name="loss", value=float('nan'), step=0)
        inf_point = MetricPoint(name="loss", value=float('inf'), step=0)

        assert valid_point.is_valid() is True
        assert nan_point.is_valid() is False
        assert inf_point.is_valid() is False


class TestMetricNormalization:
    """Unit tests for metric name normalization."""

    def test_loss_aliases(self):
        """All loss aliases should normalize correctly."""
        assert normalize_metric_name("loss") == "loss"
        assert normalize_metric_name("LOSS") == "loss"
        assert normalize_metric_name("Loss") == "loss"

    def test_train_loss_aliases(self):
        """Train loss aliases should normalize."""
        assert normalize_metric_name("train_loss") == "train_loss"
        assert normalize_metric_name("training_loss") == "train_loss"
        assert normalize_metric_name("TRAINING_LOSS") == "train_loss"

    def test_eval_loss_aliases(self):
        """Eval loss aliases should normalize."""
        assert normalize_metric_name("eval_loss") == "eval_loss"
        assert normalize_metric_name("validation_loss") == "eval_loss"
        assert normalize_metric_name("val_loss") == "eval_loss"

    def test_lr_aliases(self):
        """Learning rate aliases should normalize."""
        assert normalize_metric_name("lr") == "lr"
        assert normalize_metric_name("LR") == "lr"
        assert normalize_metric_name("learning_rate") == "lr"
        assert normalize_metric_name("LEARNING_RATE") == "lr"

    def test_grad_norm_aliases(self):
        """Gradient norm aliases should normalize."""
        assert normalize_metric_name("grad_norm") == "grad_norm"
        assert normalize_metric_name("gradient_norm") == "grad_norm"

    def test_throughput_aliases(self):
        """Throughput aliases should normalize."""
        assert normalize_metric_name("throughput") == "throughput"
        assert normalize_metric_name("samples_per_second") == "throughput"
        assert normalize_metric_name("tokens_per_second") == "throughput"

    def test_gpu_util_aliases(self):
        """GPU utilization aliases should normalize."""
        assert normalize_metric_name("gpu_util") == "gpu_util"
        assert normalize_metric_name("gpu_utilization") == "gpu_util"

    def test_memory_aliases(self):
        """Memory aliases should normalize."""
        assert normalize_metric_name("memory") == "memory"
        assert normalize_metric_name("memory_usage") == "memory"

    def test_perplexity_aliases(self):
        """Perplexity aliases should normalize."""
        assert normalize_metric_name("perplexity") == "perplexity"
        assert normalize_metric_name("ppl") == "perplexity"

    def test_accuracy_aliases(self):
        """Accuracy aliases should normalize."""
        assert normalize_metric_name("accuracy") == "accuracy"
        assert normalize_metric_name("acc") == "accuracy"

    def test_unknown_metric(self):
        """Unknown metrics should normalize to lowercase."""
        assert normalize_metric_name("custom_metric") == "custom_metric"
        assert normalize_metric_name("CUSTOM_METRIC") == "custom_metric"
        assert normalize_metric_name("MyMetric") == "mymetric"

    def test_whitespace_handling(self):
        """Whitespace should be stripped."""
        assert normalize_metric_name("  loss  ") == "loss"
        assert normalize_metric_name("\tlr\n") == "lr"

    def test_all_known_aliases_covered(self):
        """All known aliases should be in the mapping."""
        expected_aliases = [
            "loss", "train_loss", "training_loss", "eval_loss",
            "validation_loss", "val_loss", "lr", "learning_rate",
            "grad_norm", "gradient_norm", "throughput",
            "samples_per_second", "tokens_per_second", "gpu_util",
            "gpu_utilization", "memory", "memory_usage", "perplexity",
            "ppl", "accuracy", "acc"
        ]

        for alias in expected_aliases:
            assert alias in KNOWN_METRIC_ALIASES, f"Missing alias: {alias}"


class TestBaseDetector:
    """Unit tests for BaseDetector class."""

    def test_can_run_insufficient_data(self):
        """can_run returns False with insufficient data."""
        store = MetricStore()
        for i in range(5):  # Less than min_data_points=10
            store.log(step=i, loss=float(i))

        detector = TestDetector()
        assert detector.can_run(store) is False

    def test_can_run_sufficient_data(self):
        """can_run returns True with sufficient data."""
        store = MetricStore()
        for i in range(20):
            store.log(step=i, loss=float(i))

        detector = TestDetector()
        assert detector.can_run(store) is True

    def test_can_run_missing_required_metric(self):
        """can_run returns False when required metric is missing."""
        store = MetricStore()
        for i in range(20):
            store.log(step=i, other_metric=float(i))  # Not 'loss'

        detector = TestDetector()
        assert detector.can_run(store) is False

    def test_should_run_interval(self):
        """should_run respects check_interval."""
        store = MetricStore()
        for i in range(101):  # 0 to 100 inclusive
            store.log(step=i, loss=float(i))

        detector = TestDetector()
        detector.check_interval = 10

        # At step 100, should run (100 % 10 == 0)
        assert store.current_step == 100
        assert detector.should_run(store) is True

        # Manually set current step to 95
        store._current_step = 95
        assert detector.should_run(store) is False

    def test_cooldown_prevents_immediate_refire(self):
        """Cooldown prevents immediate re-triggering."""
        store = MetricStore()
        for i in range(20):
            store.log(step=i, loss=float(i))

        detector = TestDetector()

        # First check should return diagnosis
        diag1 = detector.check(store)
        assert diag1 is not None

        # Immediate second check should return None (cooldown)
        diag2 = detector.check(store)
        assert diag2 is None

    def test_cooldown_expires(self):
        """After cooldown period, detector can fire again."""
        store = MetricStore()
        for i in range(20):
            store.log(step=i, loss=float(i))

        detector = TestDetector()
        detector.cooldown_steps = 10

        # First diagnosis
        diag1 = detector.check(store)
        assert diag1 is not None

        # Add more data to exceed cooldown
        for i in range(20, 35):  # 15 more steps
            store.log(step=i, loss=float(i))

        # Now should be able to fire again
        diag2 = detector.check(store)
        assert diag2 is not None

    def test_high_confidence_breaks_cooldown(self):
        """High confidence diagnosis can break cooldown."""
        store = MetricStore()
        for i in range(20):
            store.log(step=i, loss=float(i))

        detector = TestDetector(confidence=0.5)

        # First diagnosis at 0.5 confidence
        diag1 = detector.check(store)
        assert diag1 is not None
        assert diag1.confidence == 0.5

        # Increase confidence by more than 20%
        detector.set_confidence(0.9)  # 0.9 - 0.5 = 0.4 > 0.2

        # Should fire despite cooldown
        diag2 = detector.check(store)
        assert diag2 is not None
        assert diag2.confidence == 0.9

    def test_low_confidence_improvement_blocked(self):
        """Low confidence improvement doesn't break cooldown."""
        store = MetricStore()
        for i in range(20):
            store.log(step=i, loss=float(i))

        detector = TestDetector(confidence=0.5)

        # First diagnosis at 0.5 confidence
        diag1 = detector.check(store)
        assert diag1 is not None

        # Small confidence increase (less than 20%)
        detector.set_confidence(0.6)  # 0.6 - 0.5 = 0.1 < 0.2

        # Should be blocked by cooldown
        diag2 = detector.check(store)
        assert diag2 is None

    def test_reset_clears_state(self):
        """reset() clears all detector state."""
        store = MetricStore()
        for i in range(20):
            store.log(step=i, loss=float(i))

        detector = TestDetector()

        # Trigger a diagnosis
        diag1 = detector.check(store)
        assert diag1 is not None
        assert detector.diagnosis_count == 1
        assert detector._last_diagnosis_step is not None

        # Reset
        detector.reset()

        # State should be cleared
        assert detector.diagnosis_count == 0
        assert detector._last_diagnosis_step is None
        assert detector._last_diagnosis_confidence == 0.0

        # Should be able to fire immediately
        diag2 = detector.check(store)
        assert diag2 is not None

    def test_diagnosis_count_increments(self):
        """diagnosis_count increments with each diagnosis."""
        store = MetricStore()
        for i in range(20):
            store.log(step=i, loss=float(i))

        detector = TestDetector()
        detector.cooldown_steps = 5  # Short cooldown for testing

        assert detector.diagnosis_count == 0

        detector.check(store)
        assert detector.diagnosis_count == 1

        # Add data and check again after cooldown
        for i in range(20, 30):
            store.log(step=i, loss=float(i))
        detector.check(store)
        assert detector.diagnosis_count == 2

    def test_no_detection_returns_none(self):
        """When detection logic returns None, check returns None."""
        store = MetricStore()
        for i in range(20):
            store.log(step=i, loss=float(i))

        detector = TestDetector()
        detector.set_should_detect(False)

        diag = detector.check(store)
        assert diag is None
        assert detector.diagnosis_count == 0

    def test_diagnosis_step_set(self):
        """Diagnosis has step set correctly."""
        store = MetricStore()
        for i in range(100):
            store.log(step=i, loss=float(i))

        detector = TestDetector()
        diag = detector.check(store)

        assert diag is not None
        assert diag.step == 99  # current_step

    def test_diagnosis_detector_name_set(self):
        """Diagnosis has detector_name set correctly."""
        store = MetricStore()
        for i in range(20):
            store.log(step=i, loss=float(i))

        detector = TestDetector()
        diag = detector.check(store)

        assert diag is not None
        assert diag.detector_name == "test_detector"


class TestMetricTypes:
    """Tests for MetricType enum."""

    def test_all_types_have_values(self):
        """All MetricType values should be strings."""
        for metric_type in MetricType:
            assert isinstance(metric_type.value, str)

    def test_type_values_are_lowercase(self):
        """All type values should be lowercase."""
        for metric_type in MetricType:
            assert metric_type.value == metric_type.value.lower()


def run_tests():
    """Run all tests manually without pytest."""
    import traceback

    test_classes = [
        TestMetricPoint,
        TestMetricNormalization,
        TestBaseDetector,
        TestMetricTypes,
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
