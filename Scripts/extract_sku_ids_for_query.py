#!/usr/bin/env python3
"""
Extract unique SKU IDs from user events to create database queries
for missing product data.
"""

import json
import sys

def extract_sku_ids_for_query():
    user_events_file = "../RecommendationAI_NDJSON/user_events_schema_correct.ndjson"
    output_file = "../Scripts/required_sku_ids.txt"
    sql_output_file = "../Scripts/product_extraction_query.sql"
    
    print("=== Extracting SKU IDs for Database Query ===")
    
    # Extract all unique SKU IDs from user events
    sku_ids = set()
    event_count = 0
    
    try:
        with open(user_events_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    event = json.loads(line)
                    event_count += 1
                    
                    if 'productDetails' in event:
                        for product_detail in event['productDetails']:
                            if 'product' in product_detail and 'id' in product_detail['product']:
                                product_id = product_detail['product']['id']
                                if product_id.startswith('PROD'):
                                    sku_id = product_id[4:]  # Remove 'PROD' prefix
                                    try:
                                        sku_ids.add(int(sku_id))
                                    except ValueError:
                                        continue
                                        
                except json.JSONDecodeError:
                    continue
        
        print(f"Processed {event_count} user events")
        print(f"Found {len(sku_ids)} unique SKU IDs")
        
        # Save SKU IDs to file
        with open(output_file, 'w') as f:
            for sku_id in sorted(sku_ids):
                f.write(f"{sku_id}\n")
        
        print(f"SKU IDs saved to: {output_file}")
        
        # Create SQL query
        sku_list = ','.join(str(sku_id) for sku_id in sorted(sku_ids))
        
        sql_query = f"""-- Extract complete product data for user events
-- This query gets all products referenced in user events with full metadata

SELECT 
    p.id,
    p.sku_id,
    p.name_en,
    p.name_ar,
    p.description_en,
    p.description_ar,
    p.nutrition_en,
    p.nutrition_ar,
    p.subcategory_id,
    p.brand_id,
    p.upc,
    p.origincountry,
    p.allergicnote_en,
    p.allergicnote_ar,
    p.howtouse_en,
    p.howtouse_ar,
    p.slug,
    p.is_deleted,
    p.is_wrappable,
    p.is_customizable,
    p.is_international,
    p.is_digital,
    p.disable_cash,
    -- Brand information
    b.name_en as brand_name_en,
    b.name_ar as brand_name_ar,
    b.information_en as brand_info_en,
    b.information_ar as brand_info_ar,
    -- Category information  
    c.name_en as category_name_en,
    c.name_ar as category_name_ar,
    -- SKU information
    s.name_en as sku_name_en,
    s.name_ar as sku_name_ar,
    s.code as sku_code,
    s.color as sku_color,
    s.item_number,
    s.height,
    s.length,
    s.weight,
    s.width,
    s.box_count,
    s.ingredient_en,
    s.ingredient_ar,
    s.unit,
    s.external_product_type,
    s.external_product_id
FROM 
    product p
    LEFT JOIN brand b ON p.brand_id = b.id
    LEFT JOIN category c ON p.subcategory_id = c.id  
    LEFT JOIN sku s ON p.sku_id = s.id
WHERE 
    p.sku_id IN ({sku_list})
    AND p.is_deleted = 0
ORDER BY 
    p.sku_id;

-- Statistics query to verify data completeness
SELECT 
    COUNT(*) as total_products_found,
    COUNT(DISTINCT p.brand_id) as unique_brands,
    COUNT(DISTINCT p.subcategory_id) as unique_categories,
    COUNT(CASE WHEN p.name_en IS NOT NULL AND p.name_en != '' THEN 1 END) as products_with_english_names,
    COUNT(CASE WHEN p.name_ar IS NOT NULL AND p.name_ar != '' THEN 1 END) as products_with_arabic_names,
    COUNT(CASE WHEN p.description_en IS NOT NULL AND p.description_en != '' THEN 1 END) as products_with_descriptions
FROM 
    product p
WHERE 
    p.sku_id IN ({sku_list})
    AND p.is_deleted = 0;

-- Check for missing SKU IDs (products that don't exist in database)
WITH required_skus AS (
    SELECT unnest(ARRAY[{sku_list}]) as sku_id
),
existing_skus AS (
    SELECT sku_id FROM product WHERE sku_id IN ({sku_list}) AND is_deleted = 0
)
SELECT 
    r.sku_id as missing_sku_id
FROM 
    required_skus r
    LEFT JOIN existing_skus e ON r.sku_id = e.sku_id
WHERE 
    e.sku_id IS NULL
ORDER BY 
    r.sku_id;
"""

        # Save SQL query
        with open(sql_output_file, 'w', encoding='utf-8') as f:
            f.write(sql_query)
        
        print(f"SQL query saved to: {sql_output_file}")
        
        # Show statistics
        print(f"\n=== Statistics ===")
        print(f"SKU ID range: {min(sku_ids)} - {max(sku_ids)}")
        print(f"Total unique products needed: {len(sku_ids)}")
        
        # Show sample SKU IDs
        sample_skus = sorted(list(sku_ids))[:20]
        print(f"Sample SKU IDs: {sample_skus}")
        
        print(f"\n=== Next Steps ===")
        print(f"1. Run the SQL query in your database management tool")
        print(f"2. Export results as CSV: products_complete.csv")
        print(f"3. Use the CSV to create the proper Google Cloud catalog")
        
        return True
        
    except FileNotFoundError:
        print(f"Error: Could not find user events file: {user_events_file}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = extract_sku_ids_for_query()
    sys.exit(0 if success else 1)