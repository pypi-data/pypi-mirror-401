from __future__ import annotations

__all__ = ["ForecastEvaluator"]

def __getattr__(name: str):
    if name == "ForecastEvaluator":
        from .evaluator import ForecastEvaluator
        return ForecastEvaluator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
