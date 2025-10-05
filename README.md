

---

## Snakemake pipeline (demo)

Run a full end‑to‑end **synthetic** week to test the pipeline wiring:

```bash
# Default week
make demo

# Or pick a week
make demo WEEK=2025-01-10
```

This produces:

```
outputs/<WEEK>/per_tank_features.csv
outputs/<WEEK>/site_aggregate.csv
```

You can now replace the **synthetic** step with real Sentinel‑1 RTC and your tank list by wiring
`src/preprocessing/sar.py` and `src/data/*.py`, then swapping the `synthetic_features` rule with your real feature extraction.

## Notebook: per‑tank profiles & aggregates

Open: `notebooks/per_tank_profiles.ipynb`

- Cell 1 synthesizes a SAR tank crop, extracts the **azimuth profile**, and prints features.
- Cell 2 loads (or creates) **per_tank_features.csv**, converts to per‑tank **volumes**, and sums to a site total.

