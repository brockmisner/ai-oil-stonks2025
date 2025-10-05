"""
Compute simple AIS-derived features: counts of arrivals/departures port-by-port.
In practice you'll parse AIS messages (or ERDDAP rows) and apply spatiotemporal joins to port polygons.
"""
from __future__ import annotations
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

def load_ports(ports_geojson: str) -> gpd.GeoDataFrame:
    return gpd.read_file(ports_geojson)

def count_port_calls(ais_df: pd.DataFrame, ports_gdf: gpd.GeoDataFrame,
                     lon_col: str = "lon", lat_col: str = "lat", time_col: str = "time") -> pd.DataFrame:
    gdf = gpd.GeoDataFrame(ais_df.copy(), geometry=gpd.points_from_xy(ais_df[lon_col], ais_df[lat_col]), crs="EPSG:4326")
    joined = gpd.sjoin(gdf, ports_gdf, how="inner", predicate="within")
    # Very naive: treat each vesselId transition into a port polygon as a 'call'
    joined = joined.sort_values([time_col])
    counts = joined.groupby(["name"]).agg(calls=("geometry","count")).reset_index()
    return counts
