from __future__ import annotations

import numpy as np


def naive_baseline(
    y_train: np.ndarray,
    n_forecast: int,
    seasonal_period: int = 12,
    seasonal: bool = False,
) -> np.ndarray:
    """
    Generate naive baseline forecast.

    If seasonal=True and enough history exists, uses seasonal naive (repeat last seasonal period).
    Otherwise uses persistence (repeat last observed value).
    """
    y_train = np.asarray(y_train, dtype=float)

    if n_forecast <= 0:
        return np.array([], dtype=float)

    if len(y_train) == 0:
        raise ValueError("y_train is empty; cannot build naive baseline.")

    if seasonal and len(y_train) >= seasonal_period:
        return np.tile(
            y_train[-seasonal_period:],
            int(np.ceil(n_forecast / seasonal_period)),
        )[:n_forecast]

    return np.full(n_forecast, y_train[-1], dtype=float)
