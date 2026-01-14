from __future__ import annotations

import numpy as np
from typing import Dict, List

from scipy import stats


def loss_series(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_train: np.ndarray,
    metrics: List[str] | None = None,
) -> Dict[str, np.ndarray]:
    """
    Export per-timestep loss series for statistical testing.
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    y_train = np.asarray(y_train, dtype=float)

    if metrics is None:
        metrics = ["mae", "rmse", "mase"]

    loss_dict: Dict[str, np.ndarray] = {}

    for metric in metrics:
        m = metric.lower().strip()

        if m == "mae":
            loss_dict["mae"] = np.abs(y_true - y_pred)

        elif m == "rmse":
            # Store per-step squared error for DM test
            loss_dict["rmse"] = (y_true - y_pred) ** 2

        elif m == "mase":
            forecast_error = np.abs(y_true - y_pred)
            if len(y_train) >= 2:
                naive_errors = np.abs(y_train[1:] - y_train[:-1])
                scaling = float(np.mean(naive_errors)) if len(naive_errors) else 0.0
                loss_dict["mase"] = (forecast_error / scaling) if scaling > 0 else forecast_error
            else:
                loss_dict["mase"] = forecast_error

        elif m == "mape":
            epsilon = 1e-10
            loss_dict["mape"] = np.abs((y_true - y_pred) / (y_true + epsilon))

        elif m == "nse":
            loss_dict["nse"] = (y_true - y_pred) ** 2

    return loss_dict


def diebold_mariano_test(
    loss_series_1: np.ndarray,
    loss_series_2: np.ndarray,
    h: int = 1,
) -> Dict:
    """
    Diebold-Mariano test for equal predictive accuracy.

    d_t = loss_1(t) - loss_2(t)
    H0: E[d_t] = 0
    """
    l1 = np.asarray(loss_series_1, dtype=float)
    l2 = np.asarray(loss_series_2, dtype=float)

    if len(l1) != len(l2):
        raise ValueError("loss_series_1 and loss_series_2 must have the same length.")

    d = l1 - l2
    mean_d = float(np.mean(d))
    n = int(len(d))

    if n < 2:
        return {
            "statistic": 0.0,
            "p_value": 1.0,
            "mean_loss_diff": mean_d,
            "conclusion": "Insufficient sample size for DM test.",
            "significant": False,
        }

    var_d = float(np.var(d, ddof=1))

    # Autocorrelation adjustment for multi-step forecasts
    if h > 1:
        gamma = []
        for k in range(1, h):
            if len(d) > k:
                gamma_k = float(np.mean((d[:-k] - mean_d) * (d[k:] - mean_d)))
                gamma.append(gamma_k)
        var_d = var_d + 2.0 * float(np.sum(gamma))

    if var_d > 0:
        dm_stat = mean_d / float(np.sqrt(var_d / n))
    else:
        dm_stat = 0.0

    p_value = float(2.0 * (1.0 - stats.t.cdf(np.abs(dm_stat), df=n - 1)))

    if p_value < 0.05:
        if mean_d < 0:
            conclusion = "Model 1 significantly BETTER than Model 2 (p < 0.05)"
            significant = True
        else:
            conclusion = "Model 1 significantly WORSE than Model 2 (p < 0.05)"
            significant = True
    else:
        conclusion = "No significant difference detected (p ≥ 0.05)"
        significant = False

    return {
        "statistic": float(dm_stat),
        "p_value": float(p_value),
        "mean_loss_diff": float(mean_d),
        "conclusion": conclusion,
        "significant": significant,
    }
