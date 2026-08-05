"""Evaluation utilities for performance reporting and dataset assessment."""

from app.evaluation.evaluator import (
    DatasetEvaluator,
    compute_accuracy,
    compute_confusion_matrix,
    compute_f1_score,
    compute_precision,
    compute_recall,
    generate_evaluation_report,
)

__all__ = [
    "DatasetEvaluator",
    "compute_accuracy",
    "compute_precision",
    "compute_recall",
    "compute_f1_score",
    "compute_confusion_matrix",
    "generate_evaluation_report",
]
