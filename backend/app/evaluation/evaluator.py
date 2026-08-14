from __future__ import annotations

from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

from app.detector.engine import DetectionEngine
from app.utils.feature_extractor import extract_features_from_text


def compute_accuracy(y_true: Sequence[str], y_pred: Sequence[str]) -> float:
    return float(accuracy_score(list(y_true), list(y_pred)))


def compute_precision(
    y_true: Sequence[str],
    y_pred: Sequence[str],
    positive_label: str = "ai",
) -> float:
    return float(
        precision_score(
            list(y_true),
            list(y_pred),
            labels=[positive_label],
            average="binary",
            pos_label=positive_label,
            zero_division=0,
        )
    )


def compute_recall(
    y_true: Sequence[str],
    y_pred: Sequence[str],
    positive_label: str = "ai",
) -> float:
    return float(
        recall_score(
            list(y_true),
            list(y_pred),
            labels=[positive_label],
            average="binary",
            pos_label=positive_label,
            zero_division=0,
        )
    )


def compute_f1_score(
    y_true: Sequence[str],
    y_pred: Sequence[str],
    positive_label: str = "ai",
) -> float:
    return float(
        f1_score(
            list(y_true),
            list(y_pred),
            labels=[positive_label],
            average="binary",
            pos_label=positive_label,
            zero_division=0,
        )
    )


def compute_confusion_matrix(
    y_true: Sequence[str],
    y_pred: Sequence[str],
    labels: Sequence[str] | None = None,
) -> np.ndarray:
    label_list = list(labels) if labels is not None else sorted(set(list(y_true)) | set(list(y_pred)))
    matrix = confusion_matrix(list(y_true), list(y_pred), labels=label_list)
    return np.asarray(matrix)


def generate_evaluation_report(
    y_true: Sequence[str],
    y_pred: Sequence[str],
    labels: Sequence[str] | None = None,
    positive_label: str = "ai",
) -> dict[str, object]:
    label_list = list(labels) if labels is not None else sorted(set(list(y_true)) | set(list(y_pred)))
    matrix = compute_confusion_matrix(y_true, y_pred, labels=label_list)
    report = {
        "accuracy": compute_accuracy(y_true, y_pred),
        "precision": compute_precision(y_true, y_pred, positive_label=positive_label),
        "recall": compute_recall(y_true, y_pred, positive_label=positive_label),
        "f1_score": compute_f1_score(y_true, y_pred, positive_label=positive_label),
        "labels": label_list,
        "confusion_matrix": matrix.tolist(),
        "positive_label": positive_label,
        "sample_count": len(list(y_true)),
    }
    return report


class DatasetEvaluator:
    """Evaluate essay predictions against dataset labels."""

    def __init__(self, detector: DetectionEngine | None = None) -> None:
        self.detector = detector or DetectionEngine()

    @staticmethod
    def _normalize_label(value: object) -> str:
        return str(value).strip().lower()

    def _predict_label(self, text: str, positive_label: str = "ai", threshold: float = 0.5) -> str:
        features = extract_features_from_text(text)
        decision = self.detector.analyze_with_highlights(text, features)
        score = float(decision.overall_score)
        if positive_label == "human":
            return "human" if score < threshold else "ai"
        return positive_label if score >= threshold else "human"

    def _collect_rows(self, dataset_dir: str | Path) -> list[dict[str, str]]:
        root = Path(dataset_dir)
        if not root.exists():
            return []

        rows: list[dict[str, str]] = []
        for file_path in sorted(root.rglob("*")):
            if not file_path.is_file():
                continue
            suffix = file_path.suffix.lower()
            if suffix not in {".txt", ".md", ".csv"}:
                continue

            if suffix == ".csv":
                try:
                    frame = pd.read_csv(file_path)
                except Exception:
                    continue
                if "text" in frame.columns and "source_label" in frame.columns:
                    for _, row in frame.iterrows():
                        text = str(row.get("text", "")).strip()
                        label = self._normalize_label(row.get("source_label", "unknown"))
                        if text:
                            rows.append({"text": text, "source_label": label})
                continue

            label = self._normalize_label(file_path.parent.name)
            if label not in {"human", "ai"}:
                label = self._normalize_label(file_path.stem)
            if label not in {"human", "ai"}:
                continue
            text = file_path.read_text(encoding="utf-8", errors="ignore")
            cleaned = " ".join(text.split())
            if cleaned:
                rows.append({"text": cleaned, "source_label": label})

        return rows

    def evaluate_dataset(
        self,
        dataset_dir: str | Path,
        positive_label: str = "ai",
        threshold: float = 0.5,
    ) -> dict[str, object]:
        rows = self._collect_rows(dataset_dir)
        if not rows:
            return {
                "accuracy": 0.0,
                "precision": 0.0,
                "recall": 0.0,
                "f1_score": 0.0,
                "labels": ["human", "ai"],
                "confusion_matrix": {"human": {"human": 0, "ai": 0}, "ai": {"human": 0, "ai": 0}},
                "positive_label": positive_label,
                "sample_count": 0,
            }

        y_true = [self._normalize_label(item["source_label"]) for item in rows]
        y_pred = [self._predict_label(item["text"], positive_label=positive_label, threshold=threshold) for item in rows]
        return generate_evaluation_report(y_true, y_pred, labels=["human", "ai"], positive_label=positive_label)


__all__ = [
    "DatasetEvaluator",
    "compute_accuracy",
    "compute_precision",
    "compute_recall",
    "compute_f1_score",
    "compute_confusion_matrix",
    "generate_evaluation_report",
]
