"""
Aggregate per-tank features/volumes into site totals.
"""
from __future__ import annotations
import pandas as pd

def sum_volumes(per_tank: pd.DataFrame, vol_col: str = "volume_bbl") -> float:
    return float(per_tank[vol_col].sum())

def weekly_change(series: pd.Series) -> pd.Series:
    return series.diff()
