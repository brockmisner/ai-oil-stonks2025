
"""
Generate synthetic per-tank SAR + optical features for a given week.
This lets you exercise the pipeline end-to-end without any external data.

Outputs a CSV with columns:
  tank_id, week, radius_m, peak, mean, std, peak_to_mean, arc_width_deg, concentration,
  shadow_fraction, rim_dark_ratio, lo, hi
"""
from __future__ import annotations
import argparse, json, random, math
from pathlib import Path
import pandas as pd

def generate_synthetic_features(tanks_geojson: str, out_csv: str, week: str) -> pd.DataFrame:
    g = json.loads(Path(tanks_geojson).read_text())
    rows = []
    rng = random.Random(42)  # deterministic for demo
    for feat in g["features"]:
        pid = feat["properties"].get("id", "tank_unknown")
        radius_m = float(feat["properties"].get("radius_m", 50.0))
        roof_type = feat["properties"].get("roof_type", "floating")

        # Synthetic "height fraction" (0 empty .. 1 full)
        frac = rng.uniform(0.1, 0.9)
        # Map to SAR index (peak_to_mean) with plausible bounds
        lo, hi = 1.15, 2.60
        idx = lo + frac * (hi - lo)

        # Build a consistent feature set
        peak = idx * 0.6 + rng.uniform(0.0, 0.2)
        mean = peak / idx
        std = mean * rng.uniform(0.05, 0.25)
        arc_width_deg = 20 + (1.0 - frac) * 80 + rng.uniform(-5, 5)  # wider arc when low
        concentration = 0.25 + (0.5 - abs(frac - 0.5)) * 0.3 + rng.uniform(-0.03, 0.03)

        # Optical shadow proxies (rough)
        shadow_fraction = (1.0 - frac) * 0.6 + rng.uniform(-0.05, 0.05)
        rim_dark_ratio = 1.0 + (1.0 - frac) * 0.6 + rng.uniform(-0.05, 0.05)

        rows.append({
            "tank_id": pid,
            "week": week,
            "radius_m": radius_m,
            "roof_type": roof_type,
            "peak": peak,
            "mean": mean,
            "std": std,
            "peak_to_mean": idx,
            "arc_width_deg": arc_width_deg,
            "concentration": concentration,
            "shadow_fraction": shadow_fraction,
            "rim_dark_ratio": rim_dark_ratio,
            "lo": lo,
            "hi": hi
        })
    df = pd.DataFrame(rows)
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tanks", required=True, help="Path to tanks GeoJSON (points with radius_m)")
    ap.add_argument("--out", required=True, help="Output CSV path")
    ap.add_argument("--week", required=True, help="Week label, e.g., 2025-01-03")
    args = ap.parse_args()
    generate_synthetic_features(args.tanks, args.out, args.week)

if __name__ == "__main__":
    main()
