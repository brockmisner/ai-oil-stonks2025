
# Snakemake pipeline (free-data starter)
configfile: "config/default.yaml"

import os

# User-configurable "week" (YYYY-MM-DD is the Friday cutoff date)
week = config.get("week", "2025-01-03")
OUTDIR = f"outputs/{week}"

rule all:
    input:
        f"{OUTDIR}/per_tank_features.csv",
        f"{OUTDIR}/site_aggregate.csv"

rule synthetic_features:
    input:
        tanks = "data/tanks/tanks_sample.geojson"
    output:
        features = f"{OUTDIR}/per_tank_features.csv"
    shell:
        "python -m src.pipelines.synthetic_week --tanks {input.tanks} --out {output.features} --week {week}"

rule aggregate:
    input:
        features = f"{OUTDIR}/per_tank_features.csv",
        tanks    = "data/tanks/tanks_sample.geojson"
    output:
        agg   = f"{OUTDIR}/site_aggregate.csv"
    params:
        shell_height = 18.0,   # default meters; edit to your site
        index_col    = "peak_to_mean",
        lo_col       = "lo",
        hi_col       = "hi"
    shell:
        "python -m src.pipelines.aggregate_week "
        "--features {input.features} --tanks {input.tanks} "
        "--out {output.agg} --shell-height {params.shell_height} "
        f"--index-col {{params.index_col}} --lo-col {{params.lo_col}} --hi-col {{params.hi_col}}"
