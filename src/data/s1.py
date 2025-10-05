"""
Sentinel-1 search and RTC queue stubs (ASF/HyP3).
"""
from __future__ import annotations
from datetime import date
from typing import List

def search_s1(aoi_geojson_path: str, start: str, end: str, pols=("VV","VH")) -> List[dict]:
    """
    Return a list of S1 scenes (stub). Replace with asf_search or Copernicus APIs.
    """
    return [{"scene_id":"S1_stub_001","start":start,"end":end,"pols":list(pols)}]

def queue_hyp3_rtc(scene_ids: list[str]) -> None:
    """
    Submit RTC jobs to HyP3 (stub).
    """
    raise NotImplementedError("Use hyp3_sdk to submit jobs")
