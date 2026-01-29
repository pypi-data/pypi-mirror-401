#!/usr/bin/env python3
"""
False positive tests for train-check.

These tests ensure that healthy, normal training scenarios do NOT trigger warnings.
This is critical for user trust - too many false positives makes the tool useless.
"""

import math
import random
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from training_doctor import Doctor
from training_doctor.metrics.store import MetricStore


class TestHealthyTrainingScenarios:
    """Healthy training patterns that should NOT trigger any high-confidence warnings."""

    def test_perfect_exponential_decay(self):
        """Perfect exponential decay loss should not trigger any warnings."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)
        for step in range(2000):
            # Perfect exponential decay with minimal noise
            loss = 4.0 * math.exp(-step / 500) + 1.0 + random.gauss(0, 0.01)
            lr = 1e-4
            grad_norm = random.gauss(1.0, 0.1)
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()
        # Filter to high-confidence diagnoses only
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        assert len(high_conf) == 0, f"False positives: {[d.problem for d in high_conf]}"

    def test_loss_with_natural_batch_noise(self):
        """Loss with ±5% natural batch variation should not trigger warnings."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)
        for step in range(2000):
            base_loss = 4.0 * math.exp(-step / 500) + 1.0
            # 5% noise is normal for mini-batch training
            loss = base_loss * (1 + random.gauss(0, 0.05))
            lr = 1e-4
            grad_norm = random.gauss(1.0, 0.15)
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        assert len(high_conf) == 0, f"False positives: {[d.problem for d in high_conf]}"

    def test_brief_spike_that_recovers(self):
        """A brief, small loss spike that recovers immediately should not trigger warnings."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)
        for step in range(1500):
            base_loss = 4.0 * math.exp(-step / 400) + 1.2

            # Single small spike at step 500 that recovers in 1 step
            # 1.5x is noticeable but not severe (would need 3.5x to be a statistical outlier)
            if step == 500:
                loss = base_loss * 1.5  # Small spike
            else:
                loss = base_loss + random.gauss(0, 0.02)

            lr = 1e-4
            grad_norm = random.gauss(1.0, 0.1)
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        # A single small spike should not trigger lr_too_high
        assert len(high_conf) == 0, f"False positives: {[d.problem for d in high_conf]}"

    def test_legitimate_convergence_plateau(self):
        """Loss that converges and plateaus at a low value (< 1.5) should not warn."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)
        for step in range(3000):
            if step < 1000:
                # Initial learning
                base_loss = 4.0 * math.exp(-step / 300) + 1.2
            else:
                # Converged at ~1.2 (below plateau threshold of 1.5)
                base_loss = 1.2 + random.gauss(0, 0.02)

            loss = base_loss
            lr = 1e-4
            grad_norm = random.gauss(0.5, 0.1)  # Lower grads when converged
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        # Should not trigger plateau detector (loss < 1.5)
        plateau_warnings = [d for d in high_conf if 'plateau' in d.problem.lower()]
        assert len(plateau_warnings) == 0, f"False plateau: {plateau_warnings}"

    def test_normal_train_eval_gap(self):
        """Normal 5-10% train/eval gap should not trigger overfitting warning."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)
        for step in range(2000):
            train_loss = 3.0 * math.exp(-step / 500) + 0.8

            # Eval loss is 8% higher - this is normal, not overfitting
            eval_loss = train_loss * 1.08

            doctor.log(step=step, loss=train_loss, lr=1e-4)
            if step % 100 == 0:
                doctor.log(step=step, eval_loss=eval_loss)

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        overfit_warnings = [d for d in high_conf if 'overfit' in d.problem.lower()]
        assert len(overfit_warnings) == 0, f"False overfitting: {overfit_warnings}"

    def test_cosine_lr_decay_shape_change(self):
        """Cosine LR decay with smooth loss curve should not trigger warnings."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)
        total_steps = 3000
        for step in range(total_steps):
            # Cosine LR schedule
            progress = step / total_steps
            lr = 1e-4 * (0.5 * (1 + math.cos(math.pi * progress)))
            lr = max(lr, 1e-6)  # Min LR

            # Smooth loss curve that slows down with LR but never increases
            # Using a single smooth exponential with varying decay rate
            effective_decay = 500 + 300 * progress  # Decay gets slower over time
            base_loss = 4.0 * math.exp(-step / effective_decay) + 1.0

            loss = base_loss + random.gauss(0, 0.02)
            grad_norm = random.gauss(1.0, 0.1)
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        assert len(high_conf) == 0, f"False positives: {[d.problem for d in high_conf]}"


class TestEdgeCaseHealthyPatterns:
    """Edge cases that look suspicious but are actually healthy."""

    def test_noisy_but_improving_loss(self):
        """Moderately noisy loss that is clearly improving should not trigger warnings."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)
        for step in range(2000):
            # 5% noise with faster decay so improvement is clear over 200 steps
            base_loss = 4.0 * math.exp(-step / 300) + 1.0
            loss = base_loss * (1 + random.gauss(0, 0.05))

            lr = 1e-4
            grad_norm = random.gauss(1.0, 0.15)  # Moderate variance
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        # Should not trigger plateau or lr_too_high
        assert len(high_conf) == 0, f"False positives: {[d.problem for d in high_conf]}"

    def test_stepped_lr_with_smooth_loss(self):
        """Step LR decay with smooth loss improvement should not trigger warnings."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)
        for step in range(2000):
            # Continuous smooth loss curve that slows down over time
            # The decay rate increases (slows decay) as LR drops
            effective_decay = 200 + step * 0.15  # Decay gets slower over time
            base_loss = 4.0 * math.exp(-step / effective_decay) + 0.5

            loss = base_loss + random.gauss(0, 0.02)

            # Step LR decay
            if step < 500:
                lr = 1e-3
            elif step < 1000:
                lr = 1e-4
            elif step < 1500:
                lr = 1e-5
            else:
                lr = 1e-6

            grad_norm = random.gauss(1.0, 0.1)
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        # Step LR with smooth loss is healthy
        assert len(high_conf) == 0, f"False positives: {[d.problem for d in high_conf]}"

    def test_oscillating_but_trending_down(self):
        """Loss that oscillates but trends downward should not warn."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)
        for step in range(2000):
            # Downward trend with oscillation
            trend = 4.0 * math.exp(-step / 600) + 1.0
            oscillation = 0.2 * math.sin(step / 20)  # Regular oscillation
            loss = trend + oscillation + random.gauss(0, 0.02)

            lr = 1e-4
            grad_norm = random.gauss(1.0, 0.1)
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        assert len(high_conf) == 0, f"False positives: {[d.problem for d in high_conf]}"

    def test_warmup_phase_behavior(self):
        """Normal warmup phase behavior should not trigger warnings."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)
        for step in range(2000):
            # Warmup for first 500 steps
            if step < 500:
                lr = 1e-6 + (1e-4 - 1e-6) * (step / 500)
                # Loss decreases during warmup but more slowly
                base_loss = 5.0 * math.exp(-step / 800) + 1.0
                noise = random.gauss(0, 0.03)  # Moderate noise during warmup
            else:
                lr = 1e-4
                # Smooth transition to regular decay
                base_loss = 3.2 * math.exp(-(step - 500) / 500) + 1.0
                noise = random.gauss(0, 0.02)

            loss = base_loss + noise
            grad_norm = random.gauss(1.0, 0.12)
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        assert len(high_conf) == 0, f"False positives: {[d.problem for d in high_conf]}"

    def test_occasional_bad_batch(self):
        """Occasional bad batch causing brief spike should not trigger."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)
        for step in range(2000):
            base_loss = 3.5 * math.exp(-step / 500) + 1.0

            # Occasional bad batch - 1 in 500 steps
            if step % 500 == 250:  # Just 4 spikes total
                loss = base_loss * 1.5  # 50% spike, not huge
            else:
                loss = base_loss + random.gauss(0, 0.02)

            lr = 1e-4
            grad_norm = random.gauss(1.0, 0.1)
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        # 4 small spikes (50%) should not trigger lr_too_high (needs 3+ @ 3.5 std)
        assert len(high_conf) == 0, f"False positives: {[d.problem for d in high_conf]}"

    def test_different_optimizers_signatures(self):
        """Different optimizer signatures (Adam vs SGD) should not trigger warnings."""
        # Adam-like: smooth loss decrease, small gradients
        doctor_adam = Doctor()
        doctor_adam.set_auto_print(False)

        random.seed(42)
        for step in range(1500):
            loss = 4.0 * math.exp(-step / 400) + 1.0 + random.gauss(0, 0.02)
            grad_norm = random.gauss(0.5, 0.05)  # Adam has smaller effective grads
            doctor_adam.log(step=step, loss=loss, lr=1e-3, grad_norm=grad_norm)

        diagnoses_adam = doctor_adam.analyze()
        high_conf_adam = [d for d in diagnoses_adam if d.confidence > 0.5]

        # SGD-like: noisier loss, larger gradients
        doctor_sgd = Doctor()
        doctor_sgd.set_auto_print(False)

        random.seed(42)
        for step in range(1500):
            loss = 4.0 * math.exp(-step / 400) + 1.0 + random.gauss(0, 0.05)  # More noise
            grad_norm = random.gauss(2.0, 0.3)  # Larger gradients
            doctor_sgd.log(step=step, loss=loss, lr=1e-2, grad_norm=grad_norm)

        diagnoses_sgd = doctor_sgd.analyze()
        high_conf_sgd = [d for d in diagnoses_sgd if d.confidence > 0.5]

        assert len(high_conf_adam) == 0, f"Adam false positives: {[d.problem for d in high_conf_adam]}"
        assert len(high_conf_sgd) == 0, f"SGD false positives: {[d.problem for d in high_conf_sgd]}"


class TestRealisticHealthyRuns:
    """Real-world healthy training patterns from common scenarios."""

    def test_transformer_pretraining_pattern(self):
        """Typical transformer pretraining loss curve."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)
        total_steps = 5000
        for step in range(total_steps):
            # Warmup then cosine decay
            if step < 500:
                lr = 1e-7 + (3e-4 - 1e-7) * (step / 500)
            else:
                progress = (step - 500) / (total_steps - 500)
                lr = 3e-4 * (0.5 * (1 + math.cos(math.pi * progress)))
                lr = max(lr, 1e-5)

            # Smooth exponential decay throughout
            # Early training has faster decay, slows down over time
            effective_decay = 400 + step * 0.3  # Decay rate increases over time
            base_loss = 10.0 * math.exp(-step / effective_decay) + 2.5

            loss = base_loss + random.gauss(0, 0.03)
            grad_norm = random.gauss(1.0, 0.12)
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        assert len(high_conf) == 0, f"False positives: {[d.problem for d in high_conf]}"

    def test_image_classification_finetuning(self):
        """Typical image classification finetuning pattern."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)
        for step in range(1000):
            # Step LR decay at 60% and 80%
            if step < 600:
                lr = 1e-3
            elif step < 800:
                lr = 1e-4
            else:
                lr = 1e-5

            # Continuous smooth exponential decay
            # Decay slows over time as model converges
            effective_decay = 100 + step * 0.2
            base_loss = 2.5 * math.exp(-step / effective_decay) + 0.3

            loss = base_loss + random.gauss(0, 0.02)
            grad_norm = random.gauss(0.8, 0.1)
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

            # Log eval every 100 steps
            if step % 100 == 0:
                eval_loss = loss * 1.05  # Slight gap
                doctor.log(step=step, eval_loss=eval_loss)

        diagnoses = doctor.analyze()
        high_conf = [d for d in diagnoses if d.confidence > 0.5]

        assert len(high_conf) == 0, f"False positives: {[d.problem for d in high_conf]}"

    def test_rl_training_pattern(self):
        """RL training is very noisy - should not trigger despite high variance."""
        doctor = Doctor()
        doctor.set_auto_print(False)

        random.seed(42)
        for step in range(3000):
            # RL losses are extremely noisy
            base_reward = -100 + step * 0.03  # Slow improvement
            loss = -base_reward + random.gauss(0, 20)  # Very high variance!

            lr = 3e-4
            grad_norm = random.gauss(5.0, 2.0)  # RL often has large gradients
            doctor.log(step=step, loss=loss, lr=lr, grad_norm=grad_norm)

        diagnoses = doctor.analyze()
        # RL is so noisy we just check there's no critical issues
        critical = [d for d in diagnoses if d.severity.value == 'critical']

        # RL noise should not trigger critical warnings
        assert len(critical) == 0, f"Critical false positives in RL: {[d.problem for d in critical]}"


def run_tests():
    """Run all tests manually without pytest."""
    import traceback

    test_classes = [
        TestHealthyTrainingScenarios,
        TestEdgeCaseHealthyPatterns,
        TestRealisticHealthyRuns,
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
