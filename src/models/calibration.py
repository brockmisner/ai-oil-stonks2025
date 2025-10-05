"""
Per-tank calibration: convert relative features → height fraction → volume.

Baseline:
- For each tank, maintain 'low' and 'high' reference values for a chosen index (e.g., SAR peak_to_mean).
- Map current index to [0..1] via min-max with small margins.
- Volume = capacity_bbl * height_fraction (if linear assumption).

This is intentionally simple; replace with your physics mapping or Bayesian model.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

def height_fraction(index_value: float, lo: float, hi: float, eps: float = 1e-6) -> float:
    if hi <= lo + eps:
        return 0.5
    v = (index_value - lo) / (hi - lo)
    return float(np.clip(v, 0.0, 1.0))

def volume_from_fraction(diameter_m: float, shell_height_m: float, frac: float, bbl_per_m3: float = 6.28981) -> float:
    r = diameter_m / 2.0
    m3 = np.pi * (r**2) * shell_height_m * frac
    return float(m3 * bbl_per_m3)

def apply_to_dataframe(df: pd.DataFrame, index_col: str, lo_col: str, hi_col: str,
                       diameter_m_col: str, shell_height_m_col: str, out_col: str = "volume_bbl") -> pd.DataFrame:
    out = df.copy()
    out[out_col] = [
        volume_from_fraction(
            d, h, height_fraction(idx, lo, hi)
        )
        for idx, lo, hi, d, h in zip(out[index_col], out[lo_col], out[hi_col], out[diameter_m_col], out[shell_height_m_col])
    ]
    return out
