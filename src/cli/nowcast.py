"""
Typer CLI to glue pieces together. Includes a demo that synthesizes a circular tank ROI
with a bright arc to validate SAR features without external data.
"""
from __future__ import annotations
import typer, numpy as np
from rich import print
from ..config import load_config
from ..features.sar_double_bounce import annulus_azimuth_profile, arc_features
from ..features.optical_shadow import shadow_metrics

app = typer.Typer(help="Cushing free-data pipeline CLI")

@app.command()
def validate_config(path: str = "config/default.yaml"):
    cfg = load_config(path)
    print("[green]Loaded config[/green]:", cfg.model_dump())

@app.command()
def demo_sar_arc(radius_px: int = 50, peak_angle_deg: float = 45.0, noise: float = 0.1):
    """
    Create a synthetic tank disk with a bright semicircular arc and compute arc features.
    """
    H = W = 2*radius_px + 20
    cx = cy = H//2
    y,x = np.indices((H,W))
    dist2 = (x-cx)**2 + (y-cy)**2
    img = np.random.normal(0.5, noise, size=(H,W)).astype("float32")
    disk = dist2 <= radius_px**2
    img[~disk] = 0.0

    # Paint a bright arc at given azimuth (thick near rim)
    r_in = int(radius_px*0.8); r_out = int(radius_px*1.05)
    theta = (np.degrees(np.arctan2(-(y-cy), (x-cx))) + 360) % 360
    arc_mask = (dist2 >= r_in**2) & (dist2 <= r_out**2) & (np.abs(((theta - peak_angle_deg + 180) % 360) - 180) < 25)
    img[arc_mask] += 0.5  # brighten

    prof = annulus_azimuth_profile(img, cx, cy, r_px=radius_px, r_in_frac=0.7, r_out_frac=1.1, azimuth_bins=360)
    feats = arc_features(prof)
    print("[cyan]Arc features[/cyan]:", feats)

@app.command()
def demo_optical_shadow(radius_px: int = 50, dark_frac: float = 0.3, noise: float = 0.05):
    """
    Create a synthetic optical tank crop with a dark (shadow-like) sector.
    """
    H = W = 2*radius_px + 20
    cx = cy = H//2
    y,x = np.indices((H,W))
    dist2 = (x-cx)**2 + (y-cy)**2
    img = np.random.normal(0.6, noise, size=(H,W)).astype("float32")
    disk = dist2 <= radius_px**2
    img[~disk] = 1.0

    # Darken a wedge to simulate shadow
    theta = (np.degrees(np.arctan2(-(y-cy), (x-cx))) + 360) % 360
    wedge = (dist2 <= radius_px**2) & (theta>300) | ((theta<20) & (dist2 <= radius_px**2))
    img[wedge] -= 0.3

    m = shadow_metrics(img, cx, cy, r_px=radius_px, threshold="otsu")
    print("[cyan]Shadow metrics[/cyan]:", m)

if __name__ == "__main__":
    app()
