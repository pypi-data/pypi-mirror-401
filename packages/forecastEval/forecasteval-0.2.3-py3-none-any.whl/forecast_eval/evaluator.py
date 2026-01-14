from __future__ import annotations

import numpy as np
from typing import Dict, List, Optional, Tuple, Any

from .baselines import naive_baseline
from .metrics import mse, rmse, mae, mape, nse, mase, skill_score
from .stats_tests import loss_series, diebold_mariano_test


class ForecastEvaluator:
    """
    Comprehensive forecast evaluation following best-practice guidelines.

    Attributes:
        seasonal_period (int): Seasonal period for seasonal naive baseline
        results (dict): Dictionary storing evaluation results
    """

    def __init__(self, seasonal_period: int = 12):
        self.seasonal_period = int(seasonal_period)
        self.results: Dict[str, Any] = {}

    def evaluate(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_train: np.ndarray,
        y_baseline: Optional[np.ndarray] = None,
        seasonal: bool = False,
        return_loss_series: bool = False,
        stratify_by_horizon: bool = False,
        horizon_indices: Optional[List[Tuple[int, int]]] = None,
    ) -> Dict[str, Any]:
        """
        Comprehensive forecast evaluation following best-practice guidelines.
        """

        y_true = np.asarray(y_true, dtype=float)
        y_pred = np.asarray(y_pred, dtype=float)
        y_train = np.asarray(y_train, dtype=float)

        if y_baseline is None:
            y_baseline = naive_baseline(
                y_train=y_train,
                n_forecast=len(y_true),
                seasonal_period=self.seasonal_period,
                seasonal=seasonal,
            )
        else:
            y_baseline = np.asarray(y_baseline, dtype=float)

        results: Dict[str, Any] = {}

        # ===== PART 1: STANDARD METRICS =====
        results["Standard_Metrics"] = {
            "mse": mse(y_true, y_pred),
            "rmse": rmse(y_true, y_pred),
            "mae": mae(y_true, y_pred),
            "mape": mape(y_true, y_pred),
            "nse": nse(y_true, y_pred),
        }

        # ===== GUIDELINE 1 =====
        results["Guideline_1_Baseline"] = {
            "mase": mase(y_true, y_pred, y_train, seasonal_period=self.seasonal_period, seasonal=seasonal),
            "mae_skill_score": skill_score(y_true, y_pred, y_train, metric="mae",
                                           seasonal_period=self.seasonal_period, seasonal=seasonal),
            "rmse_skill_score": skill_score(y_true, y_pred, y_train, metric="rmse",
                                            seasonal_period=self.seasonal_period, seasonal=seasonal),
            "baseline_mae": mae(y_true, y_baseline),
            "model_mae": mae(y_true, y_pred),
            "baseline_rmse": rmse(y_true, y_baseline),
            "model_rmse": rmse(y_true, y_pred),
        }

        # ===== GUIDELINE 2 =====
        results["Guideline_2_Stratification"] = {
            "horizon_stratified": {"mae": {}, "rmse": {}},
            "regime_stratified": {},
            "uncertainty_stratified": {},
        }

        if stratify_by_horizon and horizon_indices:
            for h_idx, (start, end) in enumerate(horizon_indices):
                y_true_h = y_true[start:end]
                y_pred_h = y_pred[start:end]

                if len(y_true_h) > 0:
                    horizon_name = f"horizon_{h_idx}_steps_{start}-{end-1}"
                    results["Guideline_2_Stratification"]["horizon_stratified"]["mae"][horizon_name] = mae(y_true_h, y_pred_h)
                    results["Guideline_2_Stratification"]["horizon_stratified"]["rmse"][horizon_name] = rmse(y_true_h, y_pred_h)

        # ===== GUIDELINE 3 =====
        if return_loss_series:
            loss_model = loss_series(y_true, y_pred, y_train)
            loss_base = loss_series(y_true, y_baseline, y_train)

            dm_results = {}
            if "mae" in loss_model and "mae" in loss_base:
                dm_results["diebold_mariano_mae"] = diebold_mariano_test(loss_model["mae"], loss_base["mae"])

            if "rmse" in loss_model and "rmse" in loss_base:
                dm_results["diebold_mariano_rmse"] = diebold_mariano_test(loss_model["rmse"], loss_base["rmse"])

            results["Guideline_3_Statistical"] = {
                "loss_series_model": loss_model,
                "loss_series_baseline": loss_base,
                **dm_results,
            }

        self.results = results
        return results

    def summary_report(self) -> str:
        from .reporting_text import summary_report as _summary_report
        return _summary_report(self.results)

    def generate_html_report(self, output_path: str = "forecast_evaluation_report.html") -> str:
        from .reporting_html import generate_html_report as _generate_html_report
        return _generate_html_report(self.results, output_path=output_path)
