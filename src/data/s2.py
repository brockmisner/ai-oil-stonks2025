"""
Sentinel-2 discovery/fetch stubs.
"""
from __future__ import annotations

def search_s2(aoi_geojson_path: str, start: str, end: str) -> list[dict]:
    return [{"product_id":"S2_stub_001","start":start,"end":end}]
