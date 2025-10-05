"""
Simple nowcast placeholders (EWMA, state-space stubs).
"""
from __future__ import annotations
import pandas as pd

def ewma(series: pd.Series, alpha: float = 0.5) -> pd.Series:
    return series.ewm(alpha=alpha, adjust=False).mean()
