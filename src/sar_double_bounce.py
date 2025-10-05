"""
SAR double-bounce arc features (amplitude domain).

Idea:
- For a circular tank, bright returns concentrate along a semicircular arc where wall->roof double-bounce is strongest.
- We sample an annulus around the rim and summarize intensity by azimuth angle.
- From the per-azimuth profile we extract features: peak strength, width, concentration, asymmetry, etc.

This implementation operates on a 2D numpy array (gamma0 RTC amplitude suggested).
You pass pixel-space tank center (cx,cy) and radius r_px (pixels), plus annulus scale from config.
"""
from __future__ import annotations
import numpy as np

def annulus_azimuth_profile(img: np.ndarray, cx: float, cy: float, r_px: float,
                            r_in_frac: float = 0.7, r_out_frac: float = 1.1, azimuth_bins: int = 360):
    H, W = img.shape
    y_idx, x_idx = np.indices(img.shape)
    dx = x_idx - cx
    dy = y_idx - cy
    r = np.sqrt(dx*dx + dy*dy)
    theta = (np.degrees(np.arctan2(-dy, dx)) + 360.0) % 360.0  # 0 deg at +x axis, clockwise

    ring_mask = (r >= r_px*r_in_frac) & (r <= r_px*r_out_frac)
    vals = img[ring_mask]
    thetas = theta[ring_mask]
    if vals.size == 0:
        return np.zeros(azimuth_bins, dtype=float)

    # Bin by azimuth
    bins = np.linspace(0, 360, azimuth_bins+1)
    prof, _ = np.histogram(thetas, bins=bins, weights=vals)
    counts, _ = np.histogram(thetas, bins=bins)
    with np.errstate(invalid="ignore"):
        prof = np.divide(prof, np.maximum(counts, 1))
    return prof

def arc_features(az_prof: np.ndarray) -> dict[str, float]:
    """
    Extract simple, robust features from an azimuth profile.
    """
    if az_prof.size == 0:
        return {"peak":0.0,"mean":0.0,"std":0.0,"peak_to_mean":0.0,"arc_width_deg":0.0,"concentration":0.0}
    peak = float(az_prof.max())
    mean = float(az_prof.mean())
    std = float(az_prof.std())
    peak_to_mean = float(peak / (mean + 1e-6))

    # Arc width: contiguous region above (mean + 1*std). Compute longest run.
    thr = mean + std
    above = az_prof > thr
    # Handle circular wrap
    above2 = np.concatenate([above, above])
    # Find longest run of True
    max_run = 0
    run = 0
    for v in above2:
        if v:
            run += 1
            max_run = max(max_run, run)
        else:
            run = 0
    # Cap at array length
    max_run = min(max_run, az_prof.size)
    arc_width_deg = 360.0 * max_run / az_prof.size

    # Concentration: fraction of energy in top 25% azimuth bins
    k = max(1, az_prof.size // 4)
    top_idxs = np.argpartition(az_prof, -k)[-k:]
    concentration = float(az_prof[top_idxs].sum() / (az_prof.sum() + 1e-6))

    return {
        "peak": peak,
        "mean": mean,
        "std": std,
        "peak_to_mean": peak_to_mean,
        "arc_width_deg": float(arc_width_deg),
        "concentration": concentration
    }
