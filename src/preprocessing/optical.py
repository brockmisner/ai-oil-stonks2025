"""
Optical preprocessing hooks: cloud masking, shadow masking, angle grids.
"""
from __future__ import annotations

def mask_clouds_and_shadows(*args, **kwargs):
    raise NotImplementedError("Wire to s2cloudless/Fmask or use S2 Scene Classification Layer")
