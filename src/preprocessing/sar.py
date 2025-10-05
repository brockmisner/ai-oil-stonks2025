"""
Hooks for SAR preprocessing. In production you would:
- Request RTC (gamma0) via ASF HyP3 OR
- Run SNAP Graph (Apply Orbit, Thermal Noise Removal, Calibration, Terrain Flattening/RTC)

Here we just define interfaces/placeholders.
"""
from __future__ import annotations
from pathlib import Path

def ensure_rtc(input_path: str | Path, output_path: str | Path) -> None:
    """
    Placeholder for an RTC step. Wire this to HyP3 or SNAP 'gpt' in your environment.
    """
    raise NotImplementedError("Connect to HyP3 SDK or SNAP gpt here")
