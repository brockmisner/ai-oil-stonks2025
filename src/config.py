from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
from .utils.io import read_yaml

class EIAConfig(BaseModel):
    week_cutoff_local: str
    release_time_local: str

class AreaConfig(BaseModel):
    aoi_geojson: str
    tanks_geojson: str

class SensorS1(BaseModel):
    product: str = "GRD"
    pols: List[str] = Field(default_factory=lambda: ["VV","VH"])
    orbit_directions: List[str] = Field(default_factory=lambda: ["ASCENDING","DESCENDING"])
    rtc: bool = True

class SensorS2(BaseModel):
    level: str = "L2A"
    use_scl: bool = True

class SensorLandsat(BaseModel):
    use_panchromatic: bool = True

class SarArc(BaseModel):
    annulus_inner_frac: float = 0.7
    annulus_outer_frac: float = 1.1
    azimuth_bins: int = 360

class OpticalShadow(BaseModel):
    threshold: str | float = "otsu"
    min_quality: float = 0.6

class FeatureConfig(BaseModel):
    sar_arc: SarArc = SarArc()
    optical_shadow: OpticalShadow = OpticalShadow()

class AISConfig(BaseModel):
    erddap_base_url: str
    dataset_id: str
    ports_geojson: str

class Sensors(BaseModel):
    sentinel1: SensorS1 = SensorS1()
    sentinel2: SensorS2 = SensorS2()
    landsat: SensorLandsat = SensorLandsat()

class RootConfig(BaseModel):
    eia: EIAConfig
    areas: dict[str, AreaConfig]
    sensors: Sensors = Sensors()
    features: FeatureConfig = FeatureConfig()
    ais: AISConfig

def load_config(path: str = "config/default.yaml") -> RootConfig:
    return RootConfig(**read_yaml(path))
