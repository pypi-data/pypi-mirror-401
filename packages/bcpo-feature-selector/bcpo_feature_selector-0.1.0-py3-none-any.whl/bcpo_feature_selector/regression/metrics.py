from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


@dataclass(frozen=True)
class RegressionMetricSpec:
    """Regression metric definition.

    BCPORegressorSelector minimizes a fitness value.

    Conventions:
    - `score` is a "bigger is better" value used only for reporting.
    - `loss` is a "smaller is better" value used for fitness.

    For r2 we convert to a loss via `1 - r2`.
    """

    name: str
    loss: Callable[[np.ndarray, np.ndarray], float]
    score: Callable[[np.ndarray, np.ndarray], float]


def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(mean_squared_error(y_true, y_pred))


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(mean_absolute_error(y_true, y_pred))


def r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(r2_score(y_true, y_pred))


def r2_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    r2_val = r2_score(y_true, y_pred)
    loss_val = 1.0 - r2_val
    return float(max(0.0, min(2.0, loss_val)))


def resolve_regression_metric(name: str) -> RegressionMetricSpec:
    """Resolve a known regression metric.

    Supported:
    - 'neg_mean_squared_error' (loss=mse)
    - 'neg_root_mean_squared_error' (loss=rmse)
    - 'neg_mean_absolute_error' (loss=mae)
    - 'r2' (fitness uses 1 - r2)
    """

    key = name.strip().lower()
    if key in {"neg_mean_squared_error"}:
        return RegressionMetricSpec(
            name="neg_mean_squared_error",
            loss=mse,
            score=lambda yt, yp: -mse(yt, yp),
        )
    if key in {"neg_root_mean_squared_error"}:
        return RegressionMetricSpec(
            name="neg_root_mean_squared_error",
            loss=rmse,
            score=lambda yt, yp: -rmse(yt, yp),
        )
    if key in {"neg_mean_absolute_error"}:
        return RegressionMetricSpec(
            name="neg_mean_absolute_error",
            loss=mae,
            score=lambda yt, yp: -mae(yt, yp),
        )
    if key in {"r2", "r2_score"}:
        return RegressionMetricSpec(name="r2", loss=r2_loss, score=r2)

    raise ValueError(
        f"Unknown regression metric '{name}'. Supported: neg_mean_squared_error, "
        f"neg_root_mean_squared_error, neg_mean_absolute_error, r2"
    )
