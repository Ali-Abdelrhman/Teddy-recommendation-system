# Perfect User Events Extraction Guide

## Overview
This guide will help you extract user events that have 100% alignment with your real product catalog (14,990 products).

## Prerequisites
- DBeaver connected to your database
- Product catalog truncated to 14,990 lines (✅ Already done)
- SQL query file created (✅ Already done)

## Step-by-Step Process

### 1. Execute Database Query

1. **Open DBeaver** and connect to your database
2. **Open the SQL file**: `extract_matching_user_events.sql`
3. **Execute the query** - this will return user events for products in your catalog
4. **Export results as CSV**:
   - Right-click on results
   - Choose "Export Data"
   - Select CSV format
   - Save as: `Database/matching_user_events.csv`

Expected columns in CSV:
- eventType
- userId
- productId
- eventTime
- sessionId
- directUserRequest

### 2. Convert to GCP Format

Run the conversion script:
```powershell
cd "c:\Users\Ahmed\Downloads\Teddy recommendation system"
python Scripts\convert_real_events_csv.py
```

This will create: `RecommendationAI_NDJSON/user_events_real_products.ndjson`

### 3. Validate Perfect Alignment

Run the validation script:
```powershell
python Scripts\validate_perfect_alignment.py
```

This will verify 100% alignment between events and catalog.

## Expected Results

✅ **Perfect Alignment Achieved When:**
- All event products exist in the 14,990 product catalog
- No missing products reported
- Coverage percentage shows optimal distribution
- Ready for GCP Retail API import

## Quality Metrics

Your final dataset will have:
- **Product Catalog**: 14,990 real database products (no synthetic data)
- **User Events**: Database-extracted events with perfect product matching
- **Data Quality**: 100% authentic, 0% synthetic
- **Coverage**: Perfect alignment for recommendation training

## Troubleshooting

**If CSV export is empty:**
- Check database connection
- Verify SKU_IDs exist in hit/invoice tables
- Adjust date ranges in SQL query if needed

**If validation shows missing products:**
- Re-run the SQL query with broader criteria
- Check for SKU_ID format consistency

## Final Files

After completion, you'll have:
1. `product_catalog_real_only.ndjson` - 14,990 real products
2. `user_events_real_products.ndjson` - Perfect matching events
3. `matching_user_events.csv` - Raw database export

These files are ready for GCP Retail API import and recommendation system training.