# forecastEval

**forecastEval** is an open-source Python library that provides a lightweight and unified framework for rigorous evaluation of time-series forecasts.

The library is designed to address common shortcomings in forecasting practice, including insufficient baseline comparison, over-reliance on aggregated error metrics, and lack of statistical validation of performance differences.

---

## Key Features

- **Baseline-aware evaluation**
  - Automatic comparison against persistence (naïve) and seasonal naïve baselines
  - Mean Absolute Scaled Error (MASE) and skill scores for interpretable performance assessment

- **Horizon-stratified analysis**
  - User-defined forecast horizon windows
  - Detection of horizon-dependent performance degradation

- **Statistical validation**
  - Diebold–Mariano test for forecast comparison
  - Autocorrelation-adjusted variance estimation

- **Interpretative reporting**
  - Clear PASS / FAIL recommendations for model deployment
  - Human-readable console summaries

- **Interactive HTML reports**
  - Collapsible sections, visual summaries, and horizon-wise breakdowns

---

## Installation

```bash
pip install forecastEval
