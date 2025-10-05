"""
Geometry helpers: tank circles to masks, ring sampling of raster, etc.
"""
from __future__ import annotations
import numpy as np
from shapely.geometry import Point
from shapely.affinity import scale
from shapely import prepared

def circle_from_center_radius(lon: float, lat: float, radius_m: float, meters_per_degree: float = 111_320) -> Point.buffer:
    """
    Approximate a circle on a local tangent plane by buffering a Point in degrees.
    meters_per_degree ~ 111.32 km at equator; acceptable for small AOIs.
    """
    # Convert meters to degrees roughly (lat only; AOI small so okay for starter)
    deg = radius_m / meters_per_degree
    return Point(lon, lat).buffer(deg, resolution=64)

def raster_ring_indices(cx: float, cy: float, r_inner: float, r_outer: float, shape: tuple[int,int]):
    """
    Produce indices within an annulus (ring) centered at (cx,cy) in pixel coords.
    Returns a boolean mask shape (H,W) where True are ring pixels.
    """
    H, W = shape
    Y, X = np.ogrid[:H, :W]
    dist2 = (X - cx)**2 + (Y - cy)**2
    mask = (dist2 >= r_inner**2) & (dist2 <= r_outer**2)
    return mask
