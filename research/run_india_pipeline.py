#!/usr/bin/env python3
"""India-only runner for pet toy SKU estimation pipeline."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from pet_toy_pipeline import run as run_pipeline

ALLOWED_MARKETPLACES = {"Amazon.in", "Flipkart", "Blinkit", "SuperTails", "HeadsUpForTails", "SmallBrand"}
ALLOWED_ANIMALS = {"dog", "cat"}


def validate_india_input(path: Path) -> None:
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise ValueError("India input CSV has no rows.")

    for idx, row in enumerate(rows, start=2):
        country = (row.get("country") or "").strip().lower()
        marketplace = (row.get("marketplace") or "").strip()
        animal = (row.get("animal_type") or "").strip().lower()

        if country != "india":
            raise ValueError(f"Row {idx}: country must be India.")
        if marketplace not in ALLOWED_MARKETPLACES:
            raise ValueError(
                f"Row {idx}: marketplace '{marketplace}' is not supported for India run."
            )
        if animal not in ALLOWED_ANIMALS:
            raise ValueError(f"Row {idx}: animal_type must be dog/cat.")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    validate_india_input(args.input)
    run_pipeline(args.input, args.output)
