# Pet Toy Industry Research Pipeline (India + US)

This repository now includes a practical workflow to collect and standardize SKU-level pet toy data (dogs + cats), classify toy types, and estimate monthly revenue.

## What this covers

- Target geographies: **India** and **US**
- Target marketplaces: **Amazon, Flipkart, Blinkit, SuperTails, and small brands**
- Output format: CSV (Excel-compatible)
- Row granularity: **one row per SKU**
- Required fields:
  - SKU name
  - SKU image URL
  - Marketplace and country
  - Toy type (plush/rope/tug/fetch/puzzle/chew/interactive/other)
  - Estimated monthly revenue

## Files

- `research/market_research_plan.md` - step-by-step collection and estimation plan
- `research/pet_toy_pipeline.py` - transform raw listings into classified/estimated output
- `data/raw_sku_input_template.csv` - input template for scraping output
- `data/pet_toy_sku_output_example.csv` - generated example output

## Quickstart

1. Put scraped SKU rows into `data/raw_sku_input_template.csv` (or another CSV with the same headers).
2. Run:

```bash
python research/pet_toy_pipeline.py \
  --input data/raw_sku_input_template.csv \
  --output data/pet_toy_sku_output_example.csv
```

3. Open `data/pet_toy_sku_output_example.csv` in Excel.

## Revenue estimation model (heuristic)

The script uses a configurable heuristic for directional estimates:

- If monthly units sold is known: `units * price`
- Otherwise estimate units from:
  - `review_count * reviews_to_sales_multiplier`
  - `best_seller_rank` adjustment
  - marketplace/country weighting

This is not audited financial data and should be used for market sizing and prioritization only.

## India execution (current build)

Use this command to run an India-only validation + estimation pass:

```bash
python research/run_india_pipeline.py \
  --input data/india_raw_scraped.csv \
  --output data/india_pet_toy_estimates.csv
```

This repository now includes an executed India sample file (`data/india_pet_toy_estimates.csv`).
