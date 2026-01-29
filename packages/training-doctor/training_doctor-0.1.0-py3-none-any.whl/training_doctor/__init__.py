"""
training_doctor - A framework-agnostic library for monitoring deep learning training runs.

Train Check monitors your training metrics and tells you when you're wasting compute,
why it's happening, and what to change to fix it.

Basic Usage:
    from training_doctor import Doctor

    # Live monitoring
    doctor = Doctor()
    for step in training_loop:
        loss = model(batch)
        doctor.log(step=step, loss=loss.item(), lr=optimizer.param_groups[0]['lr'])
        for diagnosis in doctor.check():
            print(diagnosis)

    # Offline analysis
    doctor = Doctor()
    doctor.load("path/to/logs.csv")
    for diagnosis in doctor.analyze():
        print(diagnosis)
"""

__version__ = "0.1.0"

from .doctor import Doctor
from .diagnosis import Diagnosis, Evidence, Severity
from .metrics import MetricStore, MetricPoint, MetricType
from .detectors import (
    BaseDetector,
    LearningRateTooHighDetector,
    LearningRateTooLowDetector,
    PlateauDetector,
    OverfittingDetector,
    GradientInstabilityDetector,
)

__all__ = [
    # Main entry point
    "Doctor",
    # Diagnosis types
    "Diagnosis",
    "Evidence",
    "Severity",
    # Metrics
    "MetricStore",
    "MetricPoint",
    "MetricType",
    # Detectors
    "BaseDetector",
    "LearningRateTooHighDetector",
    "LearningRateTooLowDetector",
    "PlateauDetector",
    "OverfittingDetector",
    "GradientInstabilityDetector",
]
