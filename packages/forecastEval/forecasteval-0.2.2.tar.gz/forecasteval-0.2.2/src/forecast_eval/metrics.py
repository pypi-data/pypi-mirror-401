from __future__ import annotations

import numpy as np

from .baselines import naive_baseline


# =========================================================================
# STANDARD METRICS (TOP-5)
# =========================================================================

def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Squared Error."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return float(np.mean((y_true - y_pred) ** 2))


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Root Mean Squared Error."""
    return float(np.sqrt(mse(y_true, y_pred)))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Error."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return float(np.mean(np.abs(y_true - y_pred)))


def mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Percentage Error (%)."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    epsilon = 1e-10
    return float(np.mean(np.abs((y_true - y_pred) / (y_true + epsilon))) * 100.0)


def nse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Nash-Sutcliffe Efficiency.
    NSE = 1 indicates perfect match.
    NSE = 0 indicates model is as good as mean baseline.
    NSE < 0 indicates model is worse than mean baseline.
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)

    numerator = np.sum((y_true - y_pred) ** 2)
    denominator = np.sum((y_true - np.mean(y_true)) ** 2)
    if denominator == 0:
        return float("nan")
    return float(1.0 - (numerator / denominator))


# =========================================================================
# GUIDELINE 1: BASELINE COMPARISON WITH SCALE-FREE METRICS (GAP 1)
# =========================================================================

def mase(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_train: np.ndarray,
    seasonal_period: int = 12,
    seasonal: bool = False,
) -> float:
    """
    Mean Absolute Scaled Error (MASE).

    MASE = MAE_model(TEST) / mean(|y_t − y_{t−m}|) on TRAIN (or m=1 if non-seasonal)
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    y_train = np.asarray(y_train, dtype=float)

    mae_forecast = mae(y_true, y_pred)

    if len(y_train) < 2:
        return float("nan")

    if seasonal and len(y_train) >= seasonal_period:
        naive_errors = np.abs(
            y_train[seasonal_period:] - y_train[:-seasonal_period]
        )
    else:
        naive_errors = np.abs(y_train[1:] - y_train[:-1])

    scaling_factor = float(np.mean(naive_errors)) if len(naive_errors) else 0.0
    if scaling_factor == 0:
        return float("nan")

    return float(mae_forecast / scaling_factor)


def skill_score(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_train: np.ndarray,
    metric: str = "mae",
    seasonal_period: int = 12,
    seasonal: bool = False,
) -> float:
    """
    Skill Score: SS = 1 - (Error_model / Error_baseline)
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    y_train = np.asarray(y_train, dtype=float)

    y_baseline = naive_baseline(
        y_train=y_train,
        n_forecast=len(y_true),
        seasonal_period=seasonal_period,
        seasonal=seasonal,
    )

    m = metric.lower().strip()
    if m == "mae":
        error_model = mae(y_true, y_pred)
        error_baseline = mae(y_true, y_baseline)
    elif m == "rmse":
        error_model = rmse(y_true, y_pred)
        error_baseline = rmse(y_true, y_baseline)
    else:
        raise ValueError(f"Unsupported metric: {metric}")

    if error_baseline == 0:
        return float("nan")

    return float(1.0 - (error_model / error_baseline))
