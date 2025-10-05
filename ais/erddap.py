"""
Helpers to build ERDDAP queries for AIS-like datasets.
You will need to consult your ERDDAP instance for the datasetID and variable names.
"""
from __future__ import annotations
from urllib.parse import urlencode, urljoin

def build_erddap_url(base_url: str, dataset_id: str, constraints: dict, fmt: str = "csv") -> str:
    """
    Example:
      constraints = {
        "time>=": "2025-01-01T00:00:00Z",
        "time<=": "2025-01-08T00:00:00Z",
        "longitude>=": -97.6, "longitude<=": -97.2,
        "latitude>=": 27.7, "latitude<=": 27.9,
        "shiptype=": 80
      }
    """
    query = urlencode(constraints, doseq=True)
    return urljoin(base_url.rstrip("/") + "/", f"erddap/tabledap/{dataset_id}.{fmt}?{query}")
