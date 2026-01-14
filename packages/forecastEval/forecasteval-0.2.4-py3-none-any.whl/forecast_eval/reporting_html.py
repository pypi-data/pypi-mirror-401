from __future__ import annotations

import numpy as np
from typing import Dict, Any


def generate_html_report(results: Dict[str, Any], output_path: str = "forecast_evaluation_report.html") -> str:
    if not results:
        raise ValueError("No evaluation results yet. Call evaluate(...) first.")

    std = results.get("Standard_Metrics", {})
    g1 = results.get("Guideline_1_Baseline", {})
    g2 = results.get("Guideline_2_Stratification", {})
    g3 = results.get("Guideline_3_Statistical", {})

    mse_val = std.get("mse", np.nan)
    rmse_val = std.get("rmse", np.nan)
    mae_val = std.get("mae", np.nan)
    mape_val = std.get("mape", np.nan)
    nse_val = std.get("nse", np.nan)

    mase = g1.get("mase", np.nan)
    mae_skill = g1.get("mae_skill_score", np.nan)
    rmse_skill = g1.get("rmse_skill_score", np.nan)
    baseline_mae = g1.get("baseline_mae", np.nan)
    model_mae = g1.get("model_mae", np.nan)
    baseline_rmse = g1.get("baseline_rmse", np.nan)
    model_rmse = g1.get("model_rmse", np.nan)

    horizon_strat = g2.get("horizon_stratified", {})
    mae_strat = horizon_strat.get("mae", {}) if horizon_strat else {}
    rmse_strat = horizon_strat.get("rmse", {}) if horizon_strat else {}

    dm_mae = g3.get("diebold_mariano_mae", {}) if g3 else {}
    dm_rmse = g3.get("diebold_mariano_rmse", {}) if g3 else {}

    guideline_1_pass = (model_mae < baseline_mae) and (model_rmse < baseline_rmse)

    guideline_2_pass = None
    relative_variation = None
    if mae_strat:
        mae_values = list(mae_strat.values())
        if len(mae_values) > 1:
            mae_mean = float(np.mean(mae_values))
            mae_range = float(max(mae_values) - min(mae_values))
            relative_variation = (mae_range / mae_mean) if mae_mean > 0 else 0.0
            guideline_2_pass = relative_variation < 0.2

    guideline_3_pass = None
    if dm_mae and dm_rmse:
        mae_significant = bool(dm_mae.get("significant", False))
        rmse_significant = bool(dm_rmse.get("significant", False))
        mae_better = dm_mae.get("mean_loss_diff", 0) < 0
        rmse_better = dm_rmse.get("mean_loss_diff", 0) < 0
        guideline_3_pass = mae_significant and mae_better and rmse_significant and rmse_better

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Forecast Evaluation Report</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 20px;
      line-height: 1.6;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      background: white;
      border-radius: 15px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.3);
      overflow: hidden;
    }}
    .header {{
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 40px;
      text-align: center;
    }}
    .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
    .header p {{ font-size: 1.1em; opacity: 0.9; }}

    .content {{ padding: 40px; }}
    .section {{
      margin-bottom: 30px;
      border: 1px solid #e0e0e0;
      border-radius: 10px;
      overflow: hidden;
      transition: all 0.3s ease;
    }}
    .section:hover {{ box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
    .section-header {{
      background: #f8f9fa;
      padding: 20px;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      user-select: none;
    }}
    .section-header:hover {{ background: #e9ecef; }}
    .section-header h2 {{ color: #333; font-size: 1.5em; }}
    .section-header .toggle {{ font-size: 1.5em; font-weight: bold; color: #667eea; }}
    .section-content {{ padding: 25px; display: none; }}
    .section-content.active {{ display: block; }}

    .metric-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      margin: 20px 0;
    }}
    .metric-card {{
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 20px;
      border-radius: 10px;
      text-align: center;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    .metric-card h3 {{ font-size: 0.9em; opacity: 0.9; margin-bottom: 10px; }}
    .metric-card .value {{ font-size: 2em; font-weight: bold; }}

    .status-badge {{
      display: inline-block;
      padding: 8px 16px;
      border-radius: 20px;
      font-weight: bold;
      font-size: 0.9em;
      margin: 10px 5px;
    }}
    .status-pass {{ background: #28a745; color: white; }}
    .status-fail {{ background: #dc3545; color: white; }}
    .status-partial {{ background: #ffc107; color: #333; }}
    .status-na {{ background: #6c757d; color: white; }}

    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      background: white;
    }}
    th {{
      background: #667eea;
      color: white;
      padding: 12px;
      text-align: left;
    }}
    td {{
      padding: 12px;
      border-bottom: 1px solid #e0e0e0;
    }}
    tr:hover {{ background: #f8f9fa; }}

    .info-box {{
      background: #e7f3ff;
      border-left: 4px solid #2196F3;
      padding: 15px;
      margin: 20px 0;
      border-radius: 5px;
    }}
    .warning-box {{
      background: #fff3cd;
      border-left: 4px solid #ffc107;
      padding: 15px;
      margin: 20px 0;
      border-radius: 5px;
    }}
    .success-box {{
      background: #d4edda;
      border-left: 4px solid #28a745;
      padding: 15px;
      margin: 20px 0;
      border-radius: 5px;
    }}
    .danger-box {{
      background: #f8d7da;
      border-left: 4px solid #dc3545;
      padding: 15px;
      margin: 20px 0;
      border-radius: 5px;
    }}

    .guideline-summary {{
      display: flex;
      justify-content: space-around;
      flex-wrap: wrap;
      gap: 20px;
      margin: 30px 0;
    }}
    .guideline-card {{
      flex: 1;
      min-width: 250px;
      background: white;
      border: 2px solid #e0e0e0;
      border-radius: 10px;
      padding: 20px;
      text-align: center;
    }}
    .guideline-card h3 {{ color: #333; margin-bottom: 15px; }}
    .guideline-icon {{ font-size: 3em; margin: 10px 0; }}

    .footer {{
      background: #f8f9fa;
      padding: 20px;
      text-align: center;
      color: #666;
      border-top: 1px solid #e0e0e0;
    }}

    @media print {{
      body {{ background: white; }}
      .section-content {{ display: block !important; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>📊 Forecast Evaluation Report</h1>
      <p>Best-Practice Diagnostics for Time Series Forecasts</p>
      <p style="font-size: 0.9em; margin-top: 10px;">Generated on {np.datetime64("now")}</p>
    </div>

    <div class="content">

      <div class="section">
        <div class="section-header" onclick="toggleSection(this)">
          <h2>📋 Executive Summary</h2>
          <span class="toggle">+</span>
        </div>
        <div class="section-content">
          <div class="guideline-summary">

            <div class="guideline-card">
              <h3>Guideline 1</h3>
              <div class="guideline-icon">{"✅" if guideline_1_pass else "❌"}</div>
              <p><strong>Baseline Comparison</strong></p>
              <span class="status-badge {"status-pass" if guideline_1_pass else "status-fail"}">
                {"PASS" if guideline_1_pass else "FAIL"}
              </span>
            </div>

            <div class="guideline-card">
              <h3>Guideline 2</h3>
              <div class="guideline-icon">{"✅" if guideline_2_pass else ("❓" if guideline_2_pass is None else "⚠️")}</div>
              <p><strong>Stratified Reporting</strong></p>
              <span class="status-badge {"status-pass" if guideline_2_pass else ("status-na" if guideline_2_pass is None else "status-partial")}">
                {"PASS" if guideline_2_pass else ("NOT EVALUATED" if guideline_2_pass is None else "PARTIAL")}
              </span>
            </div>

            <div class="guideline-card">
              <h3>Guideline 3</h3>
              <div class="guideline-icon">{"✅" if guideline_3_pass else ("❓" if guideline_3_pass is None else "❌")}</div>
              <p><strong>Statistical Testing</strong></p>
              <span class="status-badge {"status-pass" if guideline_3_pass else ("status-na" if guideline_3_pass is None else "status-fail")}">
                {"PASS" if guideline_3_pass else ("NOT EVALUATED" if guideline_3_pass is None else "FAIL")}
              </span>
            </div>

          </div>

          {(
            '<div class="success-box"><strong>✓ RECOMMENDED FOR DEPLOYMENT</strong><br>Model meets best-practice evaluation standards.</div>'
            if guideline_1_pass and (guideline_3_pass or guideline_3_pass is None) else
            '<div class="warning-box"><strong>⚠ CONDITIONAL RECOMMENDATION</strong><br>Model shows promise but requires further validation.</div>'
            if guideline_1_pass else
            '<div class="danger-box"><strong>✗ NOT RECOMMENDED FOR DEPLOYMENT</strong><br>Model fails to outperform naive baseline.</div>'
          )}
        </div>
      </div>

      <div class="section">
        <div class="section-header" onclick="toggleSection(this)">
          <h2>📈 Standard Metrics</h2>
          <span class="toggle">+</span>
        </div>
        <div class="section-content">
          <p>Top-5 most commonly reported point forecast metrics:</p>
          <div class="metric-grid">
            <div class="metric-card"><h3>MAE</h3><div class="value">{mae_val:.4f}</div></div>
            <div class="metric-card"><h3>RMSE</h3><div class="value">{rmse_val:.4f}</div></div>
            <div class="metric-card"><h3>MSE</h3><div class="value">{mse_val:.4f}</div></div>
            <div class="metric-card"><h3>MAPE (%)</h3><div class="value">{mape_val:.2f}</div></div>
            <div class="metric-card"><h3>NSE</h3><div class="value">{nse_val:.4f}</div></div>
          </div>
          <div class="info-box">
            <strong>Note:</strong> These metrics alone are insufficient for rigorous evaluation.
          </div>
        </div>
      </div>

      <div class="section">
        <div class="section-header" onclick="toggleSection(this)">
          <h2>🎯 Guideline 1: Baseline Comparison (Gap 1)</h2>
          <span class="toggle">+</span>
        </div>
        <div class="section-content">

          <div class="metric-grid">
            <div class="metric-card">
              <h3>MASE</h3>
              <div class="value">{mase:.4f}</div>
              <p style="margin-top: 10px; font-size: 0.9em;">{"✓ Beat baseline" if mase < 1 else "✗ Lost to baseline"}</p>
            </div>
            <div class="metric-card">
              <h3>MAE Skill</h3>
              <div class="value">{mae_skill:.4f}</div>
              <p style="margin-top: 10px; font-size: 0.9em;">{mae_skill*100:.1f}% improvement</p>
            </div>
            <div class="metric-card">
              <h3>RMSE Skill</h3>
              <div class="value">{rmse_skill:.4f}</div>
              <p style="margin-top: 10px; font-size: 0.9em;">{rmse_skill*100:.1f}% improvement</p>
            </div>
          </div>

          <h3>Comparison Table</h3>
          <table>
            <tr><th>Metric</th><th>Baseline</th><th>Your Model</th><th>Improvement</th></tr>
            <tr>
              <td>MAE</td><td>{baseline_mae:.4f}</td><td>{model_mae:.4f}</td>
              <td style="font-weight: bold;">{((baseline_mae - model_mae) / baseline_mae * 100):.1f}%</td>
            </tr>
            <tr>
              <td>RMSE</td><td>{baseline_rmse:.4f}</td><td>{model_rmse:.4f}</td>
              <td style="font-weight: bold;">{((baseline_rmse - model_rmse) / baseline_rmse * 100):.1f}%</td>
            </tr>
          </table>

          {(
            '<div class="success-box"><strong>✓ PASS:</strong> Model outperforms baseline on TEST (MAE & RMSE).</div>'
            if guideline_1_pass else
            '<div class="danger-box"><strong>✗ FAIL:</strong> Model does not outperform baseline on TEST.</div>'
          )}

        </div>
      </div>
"""

    # Guideline 2
    if mae_strat:
        html_content += """
      <div class="section">
        <div class="section-header" onclick="toggleSection(this)">
          <h2>📊 Guideline 2: Stratified Performance (Gap 2)</h2>
          <span class="toggle">+</span>
        </div>
        <div class="section-content">
          <h3>Performance by Horizon</h3>
          <table>
            <tr><th>Horizon</th><th>MAE</th><th>RMSE</th></tr>
"""
        for h_name in sorted(mae_strat.keys()):
            html_content += f"""
            <tr>
              <td>{h_name}</td>
              <td>{mae_strat[h_name]:.4f}</td>
              <td>{rmse_strat.get(h_name, np.nan):.4f}</td>
            </tr>
"""

        html_content += """
          </table>
"""
        if relative_variation is not None:
            html_content += f"""
          <div class="metric-grid">
            <div class="metric-card"><h3>Variation</h3><div class="value">{relative_variation:.1%}</div></div>
          </div>
"""
            if relative_variation < 0.2:
                html_content += """<div class="success-box"><strong>✓ CONSISTENT:</strong> Variation < 20%.</div>"""
            elif relative_variation < 0.5:
                html_content += """<div class="warning-box"><strong>⚠ MODERATE:</strong> Variation 20-50%.</div>"""
            else:
                html_content += """<div class="danger-box"><strong>✗ HIGH:</strong> Variation > 50%.</div>"""

        html_content += """
        </div>
      </div>
"""
    else:
        html_content += """
      <div class="section">
        <div class="section-header" onclick="toggleSection(this)">
          <h2>📊 Guideline 2: Stratified Performance (Gap 2)</h2>
          <span class="toggle">+</span>
        </div>
        <div class="section-content">
          <div class="info-box"><strong>⊘ NOT EVALUATED:</strong> Horizon stratification not enabled.</div>
        </div>
      </div>
"""

    # Guideline 3
    if dm_mae or dm_rmse:
        html_content += """
      <div class="section">
        <div class="section-header" onclick="toggleSection(this)">
          <h2>🔬 Guideline 3: Statistical Testing (Gap 3)</h2>
          <span class="toggle">+</span>
        </div>
        <div class="section-content">
          <h3>Diebold-Mariano Test Results</h3>
          <table>
            <tr><th>Test</th><th>Statistic</th><th>p-value</th><th>Result</th></tr>
"""
        if dm_mae:
            html_content += f"""
            <tr>
              <td><strong>MAE</strong></td>
              <td>{dm_mae.get("statistic", np.nan):.4f}</td>
              <td>{dm_mae.get("p_value", np.nan):.4f}</td>
              <td>{dm_mae.get("conclusion", "N/A")}</td>
            </tr>
"""
        if dm_rmse:
            html_content += f"""
            <tr>
              <td><strong>RMSE</strong></td>
              <td>{dm_rmse.get("statistic", np.nan):.4f}</td>
              <td>{dm_rmse.get("p_value", np.nan):.4f}</td>
              <td>{dm_rmse.get("conclusion", "N/A")}</td>
            </tr>
"""
        html_content += """
          </table>
        </div>
      </div>
"""
    else:
        html_content += """
      <div class="section">
        <div class="section-header" onclick="toggleSection(this)">
          <h2>🔬 Guideline 3: Statistical Testing (Gap 3)</h2>
          <span class="toggle">+</span>
        </div>
        <div class="section-content">
          <div class="info-box"><strong>⊘ NOT EVALUATED:</strong> Statistical testing not enabled.</div>
        </div>
      </div>
"""

    # Close
    html_content += """
    </div>
    <div class="footer">
      <p>Generated by ForecastEvaluator | Following systematic literature review guidelines</p>
    </div>
  </div>

  <script>
    function toggleSection(header) {
      const content = header.nextElementSibling;
      const toggle = header.querySelector('.toggle');

      if (content.classList.contains('active')) {
        content.classList.remove('active');
        toggle.textContent = '+';
      } else {
        content.classList.add('active');
        toggle.textContent = '−';
      }
    }

    document.addEventListener('DOMContentLoaded', function() {
      const firstSection = document.querySelector('.section-header');
      if (firstSection) toggleSection(firstSection);
    });
  </script>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n✓ HTML report generated: {output_path}")
    print("  Open in browser to view interactive report.")
    return output_path
