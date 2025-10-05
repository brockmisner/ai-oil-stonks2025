# cushing-free-pipeline

**Free-data** starter pipeline to estimate **floating-roof crude tank fill levels** at Cushing (and beyond) from **Sentinel-1/2 + Landsat + NAIP**, with optional **U.S. coastal AIS**-based tanker features for national inventory nowcasts.

> ⚠️ Educational starter. Not investment advice. Expect to customize geometry, quality filters, and calibration before using in production.

## What you get

- A clean repo layout with:
  - SAR and optical preprocessing hooks (Sentinel-1 RTC via ASF HyP3 or your own SNAP chain).
  - Feature extraction:
    - **SAR double-bounce arc** metrics (engineered features).
    - **Optical shadow** metrics (angle-aware, quality-scored).
  - Per-tank **height fraction → volume** mapping and **aggregate** to Cushing.
  - Optional **AIS/ERDDAP** port-call feature builder for U.S. crude import/export proxies.
  - **Typer** CLI with small, runnable examples (including a synthetic image test to verify SAR arc features).
  - Config-driven setup using YAML + Pydantic.

## Quickstart

```bash
# 1) Python (>=3.10) & virtual env
python -m venv .venv && source .venv/bin/activate

# 2) Install requirements
pip install -r requirements.txt

# 3) Copy env and edit credentials/URLs if you plan to fetch real data
cp .env.example .env

# 4) Validate config and run a tiny synthetic test (no external data needed)
python -m src.cli.nowcast validate-config
python -m src.cli.nowcast demo-sar-arc

# 5) (Later) Fetch real data (stubs require you to fill API keys/endpoints):
# python -m src.cli.nowcast s1-queue --start 2025-01-01 --end 2025-01-08
# python -m src.cli.nowcast s2-fetch --start 2025-01-01 --end 2025-01-08
# python -m src.cli.nowcast ais-portcalls --start 2025-01-01 --end 2025-01-08
```

## Repo layout

```
.
├── config/
│   └── default.yaml         # AOIs, ports, EIA timing, sensor options
├── data/
│   ├── aois/cushing_aoi.geojson   # Approximate AOI polygon (edit as needed)
│   ├── ports/ports.geojson        # Example port polygons (edit/expand)
│   └── tanks/tanks_sample.geojson # Sample tank circles (center+radius_m)
├── src/
│   ├── ais/
│   │   ├── erddap.py              # Build ERDDAP queries for AIS (U.S. coastal)
│   │   └── ports.py               # Port call/dwell/arrivals metrics
│   ├── cli/nowcast.py             # Typer CLI
│   ├── data/
│   │   ├── s1.py                  # Sentinel-1 search/HyP3 stubs
│   │   ├── s2.py                  # Sentinel-2 search/fetch stubs
│   │   └── landsat.py             # Landsat/HLS stubs
│   ├── features/
│   │   ├── sar_double_bounce.py   # Engineered arc metrics (implemented)
│   │   ├── optical_shadow.py      # Shadow metrics (basic baseline)
│   │   └── aggregate.py           # Tank→site aggregation
│   ├── preprocessing/
│   │   ├── sar.py                 # RTC/angle normalization hooks
│   │   └── optical.py             # Cloud/shadow QA hooks
│   ├── utils/
│   │   ├── geometry.py            # Tank circles to masks, ring sampling, etc.
│   │   └── io.py                  # YAML/JSON/GeoJSON helpers
│   ├── config.py                  # Pydantic models + loader
│   └── models/
│       ├── calibration.py         # Per-tank min/max → height fraction → volume
│       └── nowcast.py             # Simple state-space / EWMA placeholders
├── tests/
│   └── test_sar_features.py       # Synthetic image unit test
├── .env.example
├── requirements.txt
├── LICENSE
└── README.md
```

## Notes

- **AOIs & ports** here are rough placeholders; edit to your exact polygons.
- **Fetching**: Network code is stubbed so you can wire in ASF HyP3, Copernicus, or ERDDAP endpoints without changing the outer pipeline.
- **Models**: Focus is on transparent, physics-aided features and simple calibration/baselines. Swap in your own ML after you verify feature stability.

— Generated on 2025-10-05
