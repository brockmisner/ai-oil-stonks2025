
"""
Aggregate per-tank features to volumes and site totals for a given week.
- Converts 'peak_to_mean' via per-tank lo/hi bounds into a height fraction.
- Maps height fraction → volume using tank geometry (diameter from radius_m) and a default shell height.

Outputs:
  outputs/{week}/site_aggregate.csv  with columns: week,total_volume_bbl,num_tanks
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd

from ..models.calibration import apply_to_dataframe

def aggregate(features_csv: str, tanks_geojson: str, out_csv: str, shell_height_m: float,
              index_col: str = "peak_to_mean", lo_col: str = "lo", hi_col: str = "hi") -> pd.DataFrame:
    df = pd.read_csv(features_csv)
    # Merge tanks geometry to get radius (diameter)
    g = json.loads(Path(tanks_geojson).read_text())
    geom_df = pd.DataFrame([
        {"tank_id": f["properties"].get("id", "tank_unknown"),
         "radius_m": float(f["properties"].get("radius_m", 50.0))}
        for f in g["features"]
    ])
    df = df.merge(geom_df, on="tank_id", how="left")
    df["diameter_m"] = df["radius_m"] * 2.0
    df["shell_height_m"] = float(shell_height_m)

    df_vol = apply_to_dataframe(df, index_col=index_col, lo_col=lo_col, hi_col=hi_col,
                                diameter_m_col="diameter_m", shell_height_m_col="shell_height_m",
                                out_col="volume_bbl")

    site_total = df_vol["volume_bbl"].sum()
    out = pd.DataFrame([{
        "week": df["week"].iloc[0] if "week" in df else "unknown",
        "total_volume_bbl": float(site_total),
        "num_tanks": int(len(df_vol))
    }])
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_csv, index=False)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", required=True)
    ap.add_argument("--tanks", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--shell-height", type=float, default=18.0)
    ap.add_argument("--index-col", default="peak_to_mean")
    ap.add_argument("--lo-col", default="lo")
    ap.add_argument("--hi-col", default="hi")
    args = ap.parse_args()
    aggregate(args.features, args.tanks, args.out,
              shell_height_m=args.shell_height,
              index_col=args.index_col, lo_col=args.lo_col, hi_col=args.hi_col)

if __name__ == "__main__":
    main()
