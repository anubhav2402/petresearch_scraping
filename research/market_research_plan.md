# India + US Pet Toy SKU Research Plan

## Objective
Build a SKU-level dataset for cat and dog toys with monthly revenue estimates, across India and US channels.

## Scope
- Countries: India, US
- Channels:
  - India: Amazon.in, Flipkart, Blinkit, SuperTails, D2C/small brands
  - US: Amazon.com + leading pet/ecommerce channels
- Categories: cat and dog toys only

## Required SKU fields
- `country`
- `marketplace`
- `brand`
- `sku_name`
- `product_url`
- `image_url`
- `animal_type` (dog/cat)
- `price`
- `currency`
- `review_count`
- `rating`
- `best_seller_rank`
- `monthly_units_estimate` (optional if directly available)

## Estimation methodology
1. **Toy type classification** from SKU text:
   - plush, rope, tug, fetch, puzzle, chew, interactive, other
2. **Monthly units estimate**:
   - Primary: use observed monthly sales where available
   - Fallback: `review_count × review_to_sales_multiplier`
   - Apply BSR factor when available (improves top-SKU estimates)
3. **Monthly revenue estimate**:
   - `estimated_units × price`

## Recommended execution sequence
1. Collect top SKUs by pet toy category page and bestseller pages.
2. Deduplicate using normalized marketplace+SKU key.
3. Run pipeline classifier + estimator (`research/pet_toy_pipeline.py`).
4. QA checks:
   - missing images
   - missing prices
   - outlier revenues
5. Export final CSV and segment cuts (India vs US; dog vs cat; toy type).

## Notes
- Revenue outputs are directional estimates and should be triangulated with seller interviews, import data, or paid panels before strategic investment decisions.
