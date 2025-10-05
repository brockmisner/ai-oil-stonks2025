
SHELL := /bin/bash
WEEK ?= 2025-01-03

.PHONY: demo tests clean

demo:
	@echo ">>> Running demo pipeline for week=$(WEEK)"
	snakemake -j1 --config week=$(WEEK)

tests:
	python -m pytest -q

clean:
	rm -rf outputs
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
