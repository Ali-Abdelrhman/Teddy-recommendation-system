#!/usr/bin/env python3
"""
Generate MySQL-compatible SQL query for extracting product data.
"""

import sys

def generate_mysql_query():
    # Read the SKU IDs
    sku_ids_file = "../Scripts/required_sku_ids.txt"
    sql_output_file = "../Scripts/product_extraction_query_mysql.sql"
    
    try:
        with open(sku_ids_file, 'r') as f:
            sku_ids = [line.strip() for line in f if line.strip()]
        
        print(f"Loaded {len(sku_ids)} SKU IDs")
        
        # Create comma-separated list for IN clause
        sku_list = ','.join(sku_ids)
        
        # Create MySQL-compatible query
        mysql_query = f"""-- Extract complete product data for user events (MySQL version)
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
    COUNT(CASE WHEN p.description_en IS NOT NULL AND p.description_en != '' THEN 1 END) as products_with_descriptions,
    MIN(p.sku_id) as min_sku_id,
    MAX(p.sku_id) as max_sku_id
FROM 
    product p
WHERE 
    p.sku_id IN ({sku_list})
    AND p.is_deleted = 0;

-- Check which SKU IDs exist in the database (to find missing ones)
SELECT 
    'Existing SKU IDs in database:' as note,
    COUNT(*) as found_count
FROM 
    product p
WHERE 
    p.sku_id IN ({sku_list})
    AND p.is_deleted = 0;

-- Query to find specific missing SKUs (if needed)
-- You can run this separately to see which specific SKUs are missing:
/*
CREATE TEMPORARY TABLE temp_required_skus (sku_id INT);
INSERT INTO temp_required_skus (sku_id) VALUES 
{chr(10).join(f"({sku_id}){',' if i < len(sku_ids)-1 else ';'}" for i, sku_id in enumerate(sku_ids[:100]))}
-- ... (continue for all SKU IDs or split into batches)

SELECT t.sku_id as missing_sku_id
FROM temp_required_skus t
LEFT JOIN product p ON t.sku_id = p.sku_id AND p.is_deleted = 0
WHERE p.sku_id IS NULL
ORDER BY t.sku_id;

DROP TEMPORARY TABLE temp_required_skus;
*/
"""

        # Save the MySQL query
        with open(sql_output_file, 'w', encoding='utf-8') as f:
            f.write(mysql_query)
        
        print(f"MySQL-compatible query saved to: {sql_output_file}")
        print(f"Query will search for {len(sku_ids)} SKU IDs")
        print(f"SKU ID range: {min(map(int, sku_ids))} - {max(map(int, sku_ids))}")
        
        return True
        
    except FileNotFoundError:
        print(f"Error: Could not find SKU IDs file: {sku_ids_file}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = generate_mysql_query()
    sys.exit(0 if success else 1)