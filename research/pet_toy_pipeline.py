#!/usr/bin/env python3
"""Build a standardized pet toy SKU dataset with toy-type and monthly revenue estimates."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict


TOY_TYPE_KEYWORDS: Dict[str, tuple[str, ...]] = {
    "plush": ("plush", "soft toy", "stuffed"),
    "rope": ("rope", "braid"),
    "tug": ("tug", "pull"),
    "fetch": ("fetch", "ball", "frisbee", "launcher"),
    "puzzle": ("puzzle", "snuffle", "treat dispensing", "iq"),
    "chew": ("chew", "teether", "bite resistant"),
    "interactive": ("interactive", "electronic", "motion", "automatic"),
}


@dataclass
class EstimationConfig:
    review_to_sales_multiplier: float = 28.0
    rank_top_100_multiplier: float = 1.35
    rank_101_1000_multiplier: float = 1.1
    rank_1000_plus_multiplier: float = 0.85
    india_channel_weight: float = 0.95
    us_channel_weight: float = 1.0


def classify_toy_type(sku_name: str) -> str:
    text = (sku_name or "").lower()
    for toy_type, keywords in TOY_TYPE_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return toy_type
    return "other"


def safe_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def safe_int(value: str) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def rank_multiplier(best_seller_rank: int, cfg: EstimationConfig) -> float:
    if best_seller_rank <= 0:
        return 1.0
    if best_seller_rank <= 100:
        return cfg.rank_top_100_multiplier
    if best_seller_rank <= 1000:
        return cfg.rank_101_1000_multiplier
    return cfg.rank_1000_plus_multiplier


def country_multiplier(country: str, cfg: EstimationConfig) -> float:
    c = (country or "").strip().lower()
    if c == "india":
        return cfg.india_channel_weight
    if c in {"united states", "us", "usa"}:
        return cfg.us_channel_weight
    return 1.0


def estimate_monthly_units(row: Dict[str, str], cfg: EstimationConfig) -> float:
    observed_units = safe_float(row.get("monthly_units_estimate", ""))
    if observed_units > 0:
        return observed_units

    reviews = safe_float(row.get("review_count", ""))
    units = reviews * cfg.review_to_sales_multiplier
    units *= rank_multiplier(safe_int(row.get("best_seller_rank", "")), cfg)
    units *= country_multiplier(row.get("country", ""), cfg)
    return max(units, 0.0)


def transform_row(row: Dict[str, str], cfg: EstimationConfig) -> Dict[str, str]:
    sku_name = row.get("sku_name", "")
    toy_type = classify_toy_type(sku_name)
    monthly_units = estimate_monthly_units(row, cfg)
    price = safe_float(row.get("price", ""))
    estimated_revenue = monthly_units * price

    out = dict(row)
    out["toy_type"] = toy_type
    out["estimated_monthly_units"] = f"{monthly_units:.2f}"
    out["estimated_monthly_revenue"] = f"{estimated_revenue:.2f}"
    return out


def run(input_path: Path, output_path: Path) -> None:
    cfg = EstimationConfig()
    with input_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [transform_row(row, cfg) for row in reader]

    if not rows:
        raise ValueError("Input CSV had no data rows.")

    fieldnames = list(rows[0].keys())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path, help="Input CSV path")
    p.add_argument("--output", required=True, type=Path, help="Output CSV path")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.input, args.output)
