"""
Landsat (and HLS) stubs.
"""
from __future__ import annotations

def search_landsat(aoi_geojson_path: str, start: str, end: str) -> list[dict]:
    return [{"product_id":"L8_stub_001","start":start,"end":end}]
