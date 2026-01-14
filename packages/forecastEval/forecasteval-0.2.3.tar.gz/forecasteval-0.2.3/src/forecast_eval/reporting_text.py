from __future__ import annotations

import numpy as np
from typing import Dict, Any


def summary_report(results: Dict[str, Any]) -> str:
    if not results:
        return "No evaluation results yet. Call evaluate(...) before summary_report()."

    line = "=" * 80
    subline = "-" * 80
    report = "\n" + line + "\n"
    report += "FORECAST EVALUATION REPORT\n"
    report += "Best-Practice Diagnostics for Time Series Forecasts\n"
    report += "Following systematic literature review guidelines\n"
    report += line + "\n\n"

    # =====================================================================
    # PART 1: STANDARD METRICS OVERVIEW
    # =====================================================================

    std = results.get("Standard_Metrics", {})
    mse_val = std.get("mse", np.nan)
    rmse_val = std.get("rmse", np.nan)
    mae_val = std.get("mae", np.nan)
    mape_val = std.get("mape", np.nan)
    nse_val = std.get("nse", np.nan)

    report += "PART 1: STANDARD METRICS OVERVIEW\n"
    report += subline + "\n"
    report += "These are the TOP-5 most commonly reported point forecast metrics.\n"
    report += "They provide a baseline understanding of model accuracy before applying\n"
    report += "best-practice guidelines for rigorous evaluation.\n\n"

    report += "Interpretation Guide:\n"
    report += "  • Lower is better for: MSE, RMSE, MAE, MAPE\n"
    report += "  • Higher is better for: NSE\n"
    report += "  • RMSE penalizes large errors more than MAE\n"
    report += "  • MAPE can be misleading with values near zero\n"
    report += "  • NSE compares model to predicting the mean\n\n"

    report += f"MSE  (Mean Squared Error):           {mse_val:.4f}\n"
    report += f"RMSE (Root Mean Squared Error):      {rmse_val:.4f}\n"
    report += f"MAE  (Mean Absolute Error):          {mae_val:.4f}\n"
    report += f"MAPE (Mean Absolute % Error):        {mape_val:.4f}%\n"
    report += f"NSE  (Nash-Sutcliffe Efficiency):    {nse_val:.4f}\n\n"

    if not np.isnan(nse_val):
        report += "NSE Interpretation: "
        if nse_val > 0.75:
            report += "EXCELLENT (NSE > 0.75) - Model explains >75% of variance.\n"
        elif nse_val > 0.5:
            report += "GOOD (NSE > 0.5) - Model explains >50% of variance.\n"
        elif nse_val > 0:
            report += "ACCEPTABLE (NSE > 0) - Model better than mean, but modest performance.\n"
        else:
            report += "POOR (NSE ≤ 0) - Model performs worse than simply predicting the mean.\n"

    if not np.isnan(mape_val):
        report += "MAPE Interpretation: "
        if mape_val < 10:
            report += "HIGHLY ACCURATE (<10%) - Forecast errors are very small.\n"
        elif mape_val < 20:
            report += "GOOD ACCURACY (10-20%) - Reasonable forecasting performance.\n"
        elif mape_val < 50:
            report += "MODERATE ACCURACY (20-50%) - Significant but acceptable errors.\n"
        else:
            report += "POOR ACCURACY (>50%) - Large forecasting errors detected.\n"

    report += "\n"
    report += "IMPORTANT: These metrics alone are insufficient for rigorous evaluation.\n"
    report += "The following guidelines address critical gaps in forecast evaluation.\n\n"
    report += line + "\n\n"

    # =====================================================================
    # PART 2: GUIDELINE-BASED EVALUATION
    # =====================================================================

    report += "PART 2: GUIDELINE-BASED EVALUATION\n"
    report += line + "\n\n"

    # ----- GUIDELINE 1 -----
    g1 = results.get("Guideline_1_Baseline", {})
    mase = g1.get("mase", np.nan)
    mae_skill = g1.get("mae_skill_score", np.nan)
    rmse_skill = g1.get("rmse_skill_score", np.nan)
    baseline_mae = g1.get("baseline_mae", np.nan)
    model_mae = g1.get("model_mae", np.nan)
    baseline_rmse = g1.get("baseline_rmse", np.nan)
    model_rmse = g1.get("model_rmse", np.nan)

    report += "GUIDELINE 1 – BASELINE COMPARISON WITH SCALE-FREE METRICS\n"
    report += "(Addresses Gap 1: Missing Baseline Comparisons)\n"
    report += subline + "\n\n"

    report += "WHY THIS MATTERS:\n"
    report += "59.6% of reviewed papers (112/188) fail to compare against naive baselines.\n"
    report += "Without this check, models may appear accurate while offering no improvement\n"
    report += "over trivial forecasting rules such as persistence or seasonal naive methods.\n\n"

    report += "This guideline evaluates baseline superiority using TWO complementary views:\n"
    report += "  1. MASE (scale-free error, based on naive in-sample differences)\n"
    report += "  2. Direct TEST-set comparison against a naive baseline (skill scores)\n\n"

    report += subline + "\n"
    report += "MASE ANALYSIS (SCALE-BASED REFERENCE)\n"
    report += subline + "\n\n"
    report += f"MASE (Mean Absolute Scaled Error): {mase:.4f}\n\n"

    report += (
        "Definition:\n"
        "MASE = MAE_model(TEST) / mean(|y_t − y_{t−m}|) on TRAIN\n\n"
        "Interpretation:\n"
        "  • Scale-free measure (comparable across datasets)\n"
        "  • Uses naive in-sample differences as a reference scale\n"
        "  • MASE < 1 means forecast errors are smaller than typical naive training errors\n"
        "  • MASE does NOT directly compare forecasts to the baseline on the TEST set\n\n"
    )

    if mase < 1:
        report += (
            "MASE Assessment:\n"
            f"  ✓ MASE = {mase:.4f} < 1.0\n"
            "  Forecast errors are small relative to naive in-sample variability.\n\n"
        )
    else:
        report += (
            "MASE Assessment:\n"
            f"  ⚠ MASE = {mase:.4f} ≥ 1.0\n"
            "  Forecast errors are large relative to naive in-sample variability.\n"
            "  This alone does NOT imply failure against the TEST baseline.\n\n"
        )

    report += subline + "\n"
    report += "SKILL SCORE ANALYSIS (TEST-SET BASELINE SUPERIORITY)\n"
    report += subline + "\n\n"

    report += (
        "Skill Scores directly compare your model to the naive baseline on the TEST set:\n"
        "SS = 1 − (Error_model / Error_baseline)\n"
        "  • SS > 0  → model beats baseline\n"
        "  • SS = 0  → model equals baseline\n"
        "  • SS < 0  → model worse than baseline\n\n"
    )

    report += f"MAE of naive baseline:  {baseline_mae:.4f}\n"
    report += f"MAE of your model:      {model_mae:.4f}\n"
    report += f"MAE Skill Score:        {mae_skill:.4f} ({mae_skill*100:.1f}% improvement)\n\n"

    report += f"RMSE of naive baseline: {baseline_rmse:.4f}\n"
    report += f"RMSE of your model:     {model_rmse:.4f}\n"
    report += f"RMSE Skill Score:       {rmse_skill:.4f} ({rmse_skill*100:.1f}% improvement)\n\n"

    guideline_1_pass = (model_mae < baseline_mae) and (model_rmse < baseline_rmse)
    strong_pass = guideline_1_pass and (mae_skill > 0.20) and (rmse_skill > 0.20)

    report += subline + "\n"
    report += "GUIDELINE 1 CONCLUSION\n"
    report += subline + "\n\n"
    report += "► OVERALL ASSESSMENT: "

    if strong_pass:
        report += "★★★ STRONGLY PASS\n\n"
        report += (
            "RESULT:\n"
            "The model CLEARLY outperforms the naive baseline on the TEST set.\n\n"
            "EVIDENCE:\n"
            f"  • MAE:  {model_mae:.4f} < {baseline_mae:.4f}\n"
            f"  • RMSE: {model_rmse:.4f} < {baseline_rmse:.4f}\n"
            f"  • MAE Skill:  {mae_skill*100:.1f}% improvement\n"
            f"  • RMSE Skill: {rmse_skill*100:.1f}% improvement\n\n"
            "RECOMMENDATION:\n"
            "Proceed with confidence to statistical significance testing (Guideline 3).\n\n"
        )
    elif guideline_1_pass:
        report += "★★ PASS\n\n"
        report += (
            "RESULT:\n"
            "The model outperforms the naive baseline on the TEST set.\n\n"
            "RECOMMENDATION:\n"
            "Proceed to statistical testing to confirm robustness.\n\n"
        )
    else:
        report += "✗ FAIL\n\n"
        report += (
            "RESULT:\n"
            "The model does NOT outperform the naive baseline on the TEST set.\n\n"
            "RECOMMENDATION:\n"
            "Do NOT deploy. Improve the model before further evaluation.\n\n"
        )

    report += line + "\n\n"

    # ----- GUIDELINE 2 -----
    g2 = results.get("Guideline_2_Stratification", {})
    horizon_strat = g2.get("horizon_stratified", {})
    mae_strat = horizon_strat.get("mae", {}) if horizon_strat else {}
    rmse_strat = horizon_strat.get("rmse", {}) if horizon_strat else {}

    guideline_2_pass = None

    report += "GUIDELINE 2 – STRATIFIED PERFORMANCE REPORTING\n"
    report += "(Addresses Gap 2: Over-Reliance on Aggregate Metrics)\n"
    report += subline + "\n\n"

    if not (mae_strat or rmse_strat):
        report += "⊘ NOT EVALUATED: Horizon stratification was not enabled.\n\n"
        report += "To evaluate Guideline 2, re-run with:\n"
        report += "  stratify_by_horizon=True\n"
        report += "  horizon_indices=[(0, h1), (h1, h2), (h2, h3), ...]\n\n"
        report += line + "\n\n"
    else:
        report += "GUIDELINE 2a: HORIZON STRATIFICATION\n"
        report += subline + "\n\n"

        horizon_keys = sorted(mae_strat.keys())
        mae_values = [mae_strat[h] for h in horizon_keys]

        report += "PERFORMANCE BY HORIZON:\n"
        report += subline + "\n\n"
        for h in horizon_keys:
            report += f"{h}:\n"
            report += f"  MAE:  {mae_strat[h]:.4f}\n"
            report += f"  RMSE: {rmse_strat.get(h, np.nan):.4f}\n\n"

        report += subline + "\n"
        report += "VARIATION ANALYSIS\n"
        report += subline + "\n\n"

        if len(mae_values) > 1:
            mae_mean = float(np.mean(mae_values))
            mae_std = float(np.std(mae_values))
            cv = (mae_std / mae_mean) if mae_mean > 0 else 0.0

            best_horizon = horizon_keys[int(np.argmin(mae_values))]
            worst_horizon = horizon_keys[int(np.argmax(mae_values))]

            report += "MAE Statistics across horizons:\n"
            report += f"  Minimum:    {min(mae_values):.4f} (at {best_horizon})\n"
            report += f"  Maximum:    {max(mae_values):.4f} (at {worst_horizon})\n"
            report += f"  Mean:       {mae_mean:.4f}\n"
            report += f"  Std Dev:    {mae_std:.4f}\n"
            report += f"  Coefficient of Variation: {cv:.2%}\n\n"

            if cv < 0.2:
                guideline_2_pass = True
                report += "INTERPRETATION:\n"
                report += "CONSISTENT PERFORMANCE (variation < 20%)\n\n"
            else:
                guideline_2_pass = False
                report += "INTERPRETATION:\n"
                report += "⚠ SIGNIFICANT VARIATION detected across horizons.\n"
                report += f"Worst horizon: {worst_horizon}\n\n"

            # Trend analysis (linear trend)
            x = np.arange(len(mae_values), dtype=float)
            y = np.array(mae_values, dtype=float)
            b, a = np.polyfit(x, y, 1)

            first = y[0]
            last = y[-1]
            rel_change = ((last - first) / first) if first > 0 else np.nan

            report += "HORIZON TREND ANALYSIS:\n"
            report += f"  Linear slope (MAE per horizon step): {b:.4f}\n"
            if not np.isnan(rel_change):
                report += f"  Change first→last horizon: {rel_change*100:.1f}%\n"
            report += "\n"
        else:
            guideline_2_pass = None
            report += "INCOMPLETE – Only one horizon provided; cannot assess variation.\n\n"

        report += line + "\n\n"

    # ----- GUIDELINE 3 -----
    g3 = results.get("Guideline_3_Statistical", {})
    guideline_3_pass = None

    report += "GUIDELINE 3 – STATISTICAL SIGNIFICANCE TESTING\n"
    report += "(Addresses Gap 3: Absence of Statistical Rigour)\n"
    report += subline + "\n\n"

    if not g3:
        report += "⊘ NOT EVALUATED: Statistical testing was not enabled (return_loss_series=False)\n\n"
        report += "To evaluate Guideline 3, re-run with:\n"
        report += "  return_loss_series=True\n\n"
        report += line + "\n\n"
    else:
        dm_mae = g3.get("diebold_mariano_mae", {})
        dm_rmse = g3.get("diebold_mariano_rmse", {})

        if dm_mae:
            report += "DM Test (MAE):\n"
            report += f"  statistic: {dm_mae.get('statistic', np.nan):.4f}\n"
            report += f"  p-value:   {dm_mae.get('p_value', np.nan):.4f}\n"
            report += f"  concl.:    {dm_mae.get('conclusion', 'N/A')}\n\n"

        if dm_rmse:
            report += "DM Test (RMSE / squared loss):\n"
            report += f"  statistic: {dm_rmse.get('statistic', np.nan):.4f}\n"
            report += f"  p-value:   {dm_rmse.get('p_value', np.nan):.4f}\n"
            report += f"  concl.:    {dm_rmse.get('conclusion', 'N/A')}\n\n"

        mae_significant = bool(dm_mae.get("significant", False)) if dm_mae else False
        rmse_significant = bool(dm_rmse.get("significant", False)) if dm_rmse else False
        mae_better = (dm_mae.get("mean_loss_diff", 0.0) < 0) if dm_mae else False
        rmse_better = (dm_rmse.get("mean_loss_diff", 0.0) < 0) if dm_rmse else False

        guideline_3_pass = mae_significant and mae_better and rmse_significant and rmse_better

        report += "GUIDELINE 3 CONCLUSION:\n"
        if guideline_3_pass:
            report += "★★★ STRONGLY PASS – significant and better vs baseline.\n\n"
        else:
            report += "⚠ FAIL/PARTIAL – insufficient significance evidence.\n\n"

        report += line + "\n\n"

    # =====================================================================
    # PART 3: FINAL RECOMMENDATION
    # =====================================================================

    report += line + "\n"
    report += "PART 3: GAPS ADDRESSED & FINAL RECOMMENDATION\n"
    report += line + "\n\n"

    gap1_addressed = bool(guideline_1_pass)
    gap2_addressed = bool(guideline_2_pass) if guideline_2_pass is not None else False
    gap3_addressed = bool(guideline_3_pass) if guideline_3_pass is not None else False

    gaps_addressed_count = sum([gap1_addressed, gap2_addressed, gap3_addressed])
    gaps_evaluated_count = 1 + (1 if guideline_2_pass is not None else 0) + (1 if guideline_3_pass is not None else 0)

    report += "SYSTEMATIC REVIEW GAPS SUMMARY\n"
    report += subline + "\n\n"
    report += f"Gap 1 (Baseline): {'✓' if gap1_addressed else '✗'}\n"
    report += f"Gap 2 (Stratification): {'✓' if gap2_addressed else '✗/⊘'}\n"
    report += f"Gap 3 (Statistical): {'✓' if gap3_addressed else '✗/⊘'}\n\n"

    report += subline + "\n"
    report += "FINAL DEPLOYMENT RECOMMENDATION\n"
    report += subline + "\n\n"

    if gap1_addressed and (gap3_addressed or guideline_3_pass is None):
        report += "✓✓✓ STRONGLY RECOMMENDED FOR DEPLOYMENT\n"
        report += f"  • {gaps_addressed_count}/{gaps_evaluated_count} evaluated gaps addressed\n\n"
    elif gap1_addressed and not gap3_addressed and guideline_3_pass is not None:
        report += "⚠ CONDITIONALLY RECOMMENDED WITH CAVEATS\n"
        report += f"  • {gaps_addressed_count}/{gaps_evaluated_count} evaluated gaps addressed\n\n"
    else:
        report += "✗ NOT RECOMMENDED FOR DEPLOYMENT\n\n"

    report += line + "\n"
    report += "END OF EVALUATION REPORT\n"
    report += line + "\n"

    return report
