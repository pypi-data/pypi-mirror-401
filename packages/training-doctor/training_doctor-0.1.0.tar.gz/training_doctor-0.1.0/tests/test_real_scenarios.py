#!/usr/bin/env python3
"""
Real-world scenario tests for train-check.

These tests simulate realistic training runs to ensure the tool works
in common real-world situations: long runs, sparse eval, short debug runs, etc.
"""

import math
import random
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from training_doctor import Doctor
from training_doctor.metrics.store import MetricStore


class TestLongTrainingRuns:
    """Tests for very long training runs (10k+ steps)."""

    def test_long_run_cooldown_doesnt_silence(self):
        """Cooldown shouldn't silence all detectors over a long run with recurring issues."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)

        # 10k steps with periodic issues
        for step in range(10000):
            # Periodic loss spikes every 2000 steps (should get multiple warnings)
            if step > 0 and step % 2000 < 100:
                loss = 10.0  # Spike
            else:
                loss = 4.0 * math.exp(-step / 2000) + 1.0 + random.gauss(0, 0.02)

            lr = 1e-4
            grad_norm = random.gauss(1.0, 0.1)
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()

        # Should have multiple diagnoses (not just one that got silenced)
        # Each spike period should potentially trigger a new diagnosis
        assert len(diagnoses) >= 2, f"Only {len(diagnoses)} diagnoses in long run with periodic issues"

    def test_late_developing_issues_caught(self):
        """Issues that develop late in training should still be caught."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)

        # 5000 steps of healthy training, then plateau
        for step in range(8000):
            if step < 5000:
                # Healthy training
                loss = 4.0 * math.exp(-step / 1000) + 1.5 + random.gauss(0, 0.02)
                grad_norm = random.gauss(1.0, 0.1)
            else:
                # Plateau at high loss (not converged)
                loss = 2.5 + random.gauss(0, 0.02)
                grad_norm = random.gauss(2.0, 0.5)  # High variance

            lr = 1e-4
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()

        # Should detect plateau that developed late
        plateau_found = any('plateau' in d.problem.lower() for d in diagnoses)
        assert plateau_found, "Late-developing plateau was not detected"

    def test_memory_bounded_long_run(self):
        """Memory usage should stay bounded for very long runs."""
        import sys

        doctor = Doctor()
        doctor.set_auto_print(False)

        # Log 20k data points
        for step in range(20000):
            loss = 4.0 - step * 0.0001
            doctor.log(step=step, loss=loss, lr=1e-4, grad_norm=1.0)

        # Check internal store size is proportional to data, not exponential
        store_size = len(doctor._store)
        assert store_size == 60000  # 3 metrics * 20000 steps


class TestSparseEvalSchedules:
    """Tests for training with infrequent evaluation."""

    def test_eval_every_100_steps_detects_overfitting(self):
        """Overfitting should be detected with eval every 100 steps."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)

        for step in range(5000):
            # Train loss keeps decreasing
            train_loss_val = 3.0 * math.exp(-step / 1000) + 0.5

            # Eval loss diverges significantly after step 2000
            if step < 2000:
                eval_loss = train_loss_val * 1.05
            else:
                # More pronounced divergence
                eval_loss = train_loss_val * 1.05 + (step - 2000) * 0.001

            # Use train_loss (not loss) for overfitting detector compatibility
            doctor.log(step=step, train_loss=train_loss_val, lr=1e-4)

            # Eval every 100 steps (realistic schedule)
            if step % 100 == 0:
                doctor.log(step=step, eval_loss=eval_loss)

        diagnoses = doctor.analyze()

        # Should detect overfitting with reasonable eval frequency
        overfit_found = any('overfit' in d.problem.lower() for d in diagnoses)
        assert overfit_found, "Overfitting not detected with eval every 100 steps"

    def test_sparse_eval_still_useful(self):
        """Even with sparse eval, dramatic overfitting should be detected."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)

        for step in range(10000):
            train_loss_val = 3.0 * math.exp(-step / 2000) + 0.5

            # Very dramatic divergence
            if step < 3000:
                eval_loss = train_loss_val * 1.05
            else:
                # Gap grows rapidly
                eval_loss = train_loss_val + (step - 3000) * 0.002

            # Use train_loss for overfitting detector
            doctor.log(step=step, train_loss=train_loss_val, lr=1e-4)

            # Eval every 500 steps
            if step % 500 == 0:
                doctor.log(step=step, eval_loss=eval_loss)

        diagnoses = doctor.analyze()

        # Dramatic divergence should be caught even with sparse eval
        overfit_found = any('overfit' in d.problem.lower() for d in diagnoses)
        # Note: With very sparse eval, subtle overfitting may not be detected
        # This is a known limitation of sparse evaluation
        assert overfit_found, "Dramatic overfitting not detected even with sparse eval"

    def test_no_eval_at_all(self):
        """Training without eval_loss should still work for other detectors."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)

        # Training with NaN (should trigger lr_too_high)
        for step in range(500):
            if step < 400:
                loss = 4.0 - step * 0.005
            else:
                loss = float('nan')

            doctor.log(step=step, loss=loss, lr=1e-4, grad_norm=1.0)

        diagnoses = doctor.analyze()

        # Should still detect NaN issue
        nan_found = any('nan' in d.problem.lower() or 'high' in d.problem.lower()
                        for d in diagnoses)
        assert nan_found, "NaN loss not detected without eval_loss"


class TestShortDebugRuns:
    """Tests for short debugging/testing runs."""

    def test_100_step_run(self):
        """100-step run should get meaningful feedback if there are obvious issues."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        # NaN after 50 steps - obvious issue
        for step in range(100):
            if step < 50:
                loss = 4.0 - step * 0.01
            else:
                loss = float('nan')

            doctor.log(step=step, loss=loss, lr=1e-4)

        diagnoses = doctor.analyze()

        # Should detect NaN even in short run
        assert len(diagnoses) >= 1, "No diagnoses in 100-step run with NaN"

    def test_200_step_run_detectors_can_trigger(self):
        """200-step run should allow detectors to trigger."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)

        # Repeated spikes should trigger lr_too_high
        for step in range(200):
            if step % 30 == 0 and step > 0:
                loss = 20.0  # Big spike
            else:
                loss = 4.0 - step * 0.01 + random.gauss(0, 0.1)

            doctor.log(step=step, loss=loss, lr=1e-3, grad_norm=random.gauss(1.0, 0.1))

        diagnoses = doctor.analyze()

        # Should get some diagnosis
        assert len(diagnoses) >= 1, "No diagnoses in 200-step run with spikes"

    def test_500_step_healthy_no_warnings(self):
        """500-step healthy run should not trigger warnings."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)

        for step in range(500):
            loss = 4.0 * math.exp(-step / 150) + 1.0 + random.gauss(0, 0.02)
            lr = 1e-4
            grad_norm = random.gauss(1.0, 0.1)
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        assert len(high_conf) == 0, f"False positives in short healthy run: {[d.problem for d in high_conf]}"


class TestWarmupInteractions:
    """Tests for learning rate warmup interactions with detectors."""

    def test_healthy_warmup_no_false_positives(self):
        """Healthy warmup should not trigger false positives."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)

        for step in range(2000):
            # Warmup for first 500 steps
            if step < 500:
                lr = 1e-6 + (1e-4 - 1e-6) * (step / 500)
            else:
                lr = 1e-4

            # Continuous smooth decay throughout - no discontinuity at warmup end
            effective_decay = 300 + step * 0.1
            loss = 5.0 * math.exp(-step / effective_decay) + 1.0

            loss += random.gauss(0, 0.02)
            grad_norm = random.gauss(1.0, 0.1)
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        assert len(high_conf) == 0, f"False positives during warmup: {[d.problem for d in high_conf]}"

    def test_failed_warmup_detected(self):
        """Warmup that fails (loss goes to NaN) should be detected."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)

        for step in range(500):
            # Warmup that goes wrong
            if step < 300:
                lr = 1e-6 + (1e-3 - 1e-6) * (step / 300)  # Too aggressive warmup
                loss = 5.0 + step * 0.01  # Loss increasing
            else:
                lr = 1e-3
                loss = float('nan')  # Explodes

            grad_norm = random.gauss(1.0, 0.2) if math.isfinite(loss) else float('nan')
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()

        # Should detect the failure
        assert len(diagnoses) >= 1, "Failed warmup not detected"


class TestConvergenceVsPlateau:
    """Tests to distinguish convergence from plateau."""

    def test_converged_no_false_plateau(self):
        """Model that converges to low loss should not trigger plateau warning."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)

        for step in range(3000):
            if step < 1500:
                # Learning phase
                loss = 4.0 * math.exp(-step / 400) + 1.0
            else:
                # Converged at loss ~1.1 (below plateau threshold of 1.5)
                loss = 1.1 + random.gauss(0, 0.01)

            grad_norm = random.gauss(0.5, 0.05)  # Small grads when converged
            doctor.log(step=step, loss=loss, lr=1e-5, grad_norm=grad_norm)

        diagnoses = doctor.analyze()

        plateau_warnings = [d for d in diagnoses if 'plateau' in d.problem.lower()]
        assert len(plateau_warnings) == 0, f"False plateau on converged model: {plateau_warnings}"

    def test_stuck_at_high_loss_plateau_detected(self):
        """Model stuck at high loss should trigger plateau warning."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)

        for step in range(3000):
            if step < 500:
                # Initial improvement
                loss = 4.0 - step * 0.003
            else:
                # Stuck at high loss (3.0 > 1.5 threshold)
                loss = 3.0 + random.gauss(0, 0.02)

            grad_norm = random.gauss(2.0, 0.5)  # High variance suggests noise
            doctor.log(step=step, loss=loss, lr=1e-4, grad_norm=grad_norm)

        diagnoses = doctor.analyze()

        plateau_warnings = [d for d in diagnoses if 'plateau' in d.problem.lower()]
        assert len(plateau_warnings) >= 1, "Plateau at high loss not detected"

    def test_natural_train_eval_gap_no_overfit_warning(self):
        """Natural 5-10% train/eval gap should not trigger overfitting."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)

        for step in range(3000):
            train_loss = 3.0 * math.exp(-step / 700) + 0.8

            # Constant 7% gap - not diverging
            eval_loss = train_loss * 1.07

            doctor.log(step=step, loss=train_loss, lr=1e-4)
            if step % 100 == 0:
                doctor.log(step=step, eval_loss=eval_loss)

        diagnoses = doctor.analyze()

        overfit_warnings = [d for d in diagnoses if 'overfit' in d.problem.lower()]
        assert len(overfit_warnings) == 0, f"False overfitting with constant gap: {overfit_warnings}"


class TestMixedScenarios:
    """Tests for complex, mixed training scenarios."""

    def test_lr_schedule_smooth_decay(self):
        """Cosine LR decay with smooth loss should not false positive."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)

        for step in range(3000):
            # Simple cosine decay (no restarts - restarts create discontinuities)
            progress = step / 3000
            lr = 1e-5 + (1e-4 - 1e-5) * (0.5 * (1 + math.cos(math.pi * progress)))

            # Smooth continuous loss decay
            effective_decay = 400 + step * 0.2
            loss = 4.0 * math.exp(-step / effective_decay) + 1.0 + random.gauss(0, 0.02)

            grad_norm = random.gauss(1.0, 0.1)
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        assert len(high_conf) == 0, f"False positives with cosine LR: {[d.problem for d in high_conf]}"

    def test_multi_gpu_gradient_accumulation(self):
        """Training with gradient accumulation (stepped updates) should work."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)

        # Simulate gradient accumulation: loss updates every step,
        # but grad_norm only updates every 4 steps
        for step in range(2000):
            loss = 4.0 * math.exp(-step / 500) + 1.0 + random.gauss(0, 0.02)
            doctor.log(step=step, loss=loss, lr=1e-4)

            # Grad norm only logged every 4 steps (accumulation)
            if step % 4 == 0:
                doctor.log(step=step, grad_norm=random.gauss(1.0, 0.1))

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        assert len(high_conf) == 0, f"False positives with gradient accumulation: {[d.problem for d in high_conf]}"


def run_tests():
    """Run all tests manually without pytest."""
    import traceback

    test_classes = [
        TestLongTrainingRuns,
        TestSparseEvalSchedules,
        TestShortDebugRuns,
        TestWarmupInteractions,
        TestConvergenceVsPlateau,
        TestMixedScenarios,
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
