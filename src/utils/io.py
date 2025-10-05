"""
Lightweight IO helpers for YAML/JSON/GeoJSON.
"""
from __future__ import annotations
import json, yaml, pathlib
from typing import Any, Dict

def read_yaml(path: str | pathlib.Path) -> Dict[str, Any]:
    p = pathlib.Path(path)
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def write_yaml(obj: Dict[str, Any], path: str | pathlib.Path) -> None:
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(obj, f, sort_keys=False)

def read_geojson(path: str | pathlib.Path) -> Dict[str, Any]:
    p = pathlib.Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def write_geojson(obj: Dict[str, Any], path: str | pathlib.Path) -> None:
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
