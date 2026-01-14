from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np
from sklearn.base import ClassifierMixin
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


@dataclass(frozen=True)
class MetricSpec:
    """A metric definition used by BCPO classification selector."""

    name: str
    func: Callable[[np.ndarray, np.ndarray, Optional[np.ndarray]], float]


def _safe_proba_positive(estimator: ClassifierMixin,
                         X: np.ndarray) -> Optional[np.ndarray]:
    if hasattr(estimator, "predict_proba"):
        proba = estimator.predict_proba(X)
        if proba.ndim == 2 and proba.shape[1] >= 2:
            return proba[:, 1]
    if hasattr(estimator, "decision_function"):
        scores = estimator.decision_function(X)
        return np.asarray(scores)
    return None


def accuracy(y_true: np.ndarray, y_pred: np.ndarray,
             y_score: Optional[np.ndarray] = None) -> float:
    return float(accuracy_score(y_true, y_pred))


def f1(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_score: Optional[np.ndarray] = None,
    *,
    average: str = "binary",
) -> float:
    return float(f1_score(y_true, y_pred, average=average))


def precision(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_score: Optional[np.ndarray] = None,
    *,
    average: str = "binary",
) -> float:
    return float(precision_score(y_true, y_pred,
                 average=average, zero_division=0))


def recall(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_score: Optional[np.ndarray] = None,
    *,
    average: str = "binary",
) -> float:
    return float(recall_score(y_true, y_pred,
                 average=average, zero_division=0))


def roc_auc(y_true: np.ndarray, y_pred: np.ndarray,
            y_score: Optional[np.ndarray]) -> float:
    if y_score is None:
        raise ValueError(
            "roc_auc requires predict_proba or decision_function "
            "on the estimator"
        )
    return float(roc_auc_score(y_true, y_score))


def resolve_metric(name: str, *, average: str = "binary") -> MetricSpec:
    """Resolve a known classification metric name."""

    key = name.strip().lower()
    if key in {"acc", "accuracy"}:
        return MetricSpec(name="accuracy", func=accuracy)
    if key in {"f1", "f1_score"}:
        return MetricSpec(
            name="f1",
            func=lambda yt, yp, ys: f1(yt, yp, ys, average=average)
        )
    if key in {"precision", "prec", "ppv"}:
        return MetricSpec(
            name="precision",
            func=lambda yt, yp, ys: precision(yt, yp, ys, average=average)
        )
    if key in {"recall", "rec", "tpr", "sensitivity"}:
        return MetricSpec(
            name="recall",
            func=lambda yt, yp, ys: recall(yt, yp, ys, average=average)
        )
    if key in {"auc", "roc_auc", "roc-auc"}:
        return MetricSpec(name="roc_auc", func=roc_auc)

    raise ValueError(
        f"Unknown metric '{name}'. Supported: accuracy, f1, precision, "
        "recall, roc_auc"
    )
