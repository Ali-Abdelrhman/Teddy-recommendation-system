#!/usr/bin/env python3
"""
Generate INSERT statements for temporary table approach
This creates manageable chunks of INSERT statements to avoid query size issues
"""

def load_required_sku_ids():
    """Load all 17,892 required SKU IDs"""
    try:
        with open(r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Scripts\required_sku_ids.txt", 'r') as f:
            sku_ids = []
            for line in f:
                line = line.strip()
                if line and line.isdigit():
                    sku_ids.append(int(line))
        return sku_ids
    except FileNotFoundError:
        print("❌ required_sku_ids.txt not found!")
        return []

def generate_insert_statements(sku_ids, chunk_size=1000):
    """Generate INSERT statements in manageable chunks"""
    
    insert_statements = []
    
    # Split SKU IDs into chunks
    for i in range(0, len(sku_ids), chunk_size):
        chunk = sku_ids[i:i+chunk_size]
        
        # Create VALUES string for this chunk
        values = ", ".join([f"({sku_id})" for sku_id in chunk])
        
        # Create INSERT statement
        insert_stmt = f"INSERT INTO temp_required_skus (sku_id) VALUES {values};"
        insert_statements.append(insert_stmt)
    
    return insert_statements

def generate_precise_query():
    """Generate the precise query with temp table approach"""
    
    sku_ids = load_required_sku_ids()
    
    if not sku_ids:
        print("❌ No SKU IDs loaded")
        return
    
    print(f"📋 Loaded {len(sku_ids)} SKU IDs")
    print(f"🔢 Range: {min(sku_ids)} - {max(sku_ids)}")
    
    # Generate INSERT statements in chunks
    insert_statements = generate_insert_statements(sku_ids, chunk_size=1000)
    
    print(f"📦 Generated {len(insert_statements)} INSERT chunks")
    
    # Create the complete query
    query = f"""-- PRECISE COMPREHENSIVE PRODUCT EXTRACTION QUERY
-- Uses temporary table approach for exact SKU matching
-- Total SKU IDs: {len(sku_ids)} (Range: {min(sku_ids)} - {max(sku_ids)})

-- Step 1: Create temporary table
DROP TEMPORARY TABLE IF EXISTS temp_required_skus;

CREATE TEMPORARY TABLE temp_required_skus (
    sku_id INT PRIMARY KEY,
    INDEX idx_sku_id (sku_id)
);

-- Step 2: Insert all required SKU IDs in chunks
"""
    
    # Add all INSERT statements
    for i, insert_stmt in enumerate(insert_statements):
        query += f"\n-- Chunk {i+1} of {len(insert_statements)}\n"
        query += insert_stmt + "\n"
    
    # Add the main query
    query += f"""
-- Step 3: Main extraction query
SELECT 
    -- Basic product info
    p.id as product_id,
    p.sku_id,
    p.name_en,
    p.name_ar,
    p.description_en,
    p.description_ar,
    p.slug,
    p.is_deleted,
    p.is_wrappable,
    p.is_customizable,
    p.is_international,
    p.is_digital,
    p.disable_cash,
    p.subcategory_id,
    p.brand_id,
    p.origincountry,
    p.allergicnote_en as product_allergicnote_en,
    p.allergicnote_ar as product_allergicnote_ar,
    p.howtouse_en,
    p.howtouse_ar,
    p.nutrition_en,
    p.nutrition_ar,
    
    -- Brand information
    b.name_en as brand_name_en,
    b.name_ar as brand_name_ar,
    b.slug as brand_slug,
    
    -- Category information
    cat.name_en as category_name_en,
    cat.name_ar as category_name_ar,
    cat.slug as category_slug,
    cat.color as category_color,
    
    -- SKU details with all metadata
    s.name_en as sku_name_en,
    s.name_ar as sku_name_ar,
    s.code as sku_code,
    s.color as sku_color,
    s.item_number,
    s.upc,
    s.height,
    s.length,
    s.width,
    s.weight,
    s.box_count,
    s.external_product_type,
    s.external_product_id,
    s.unit,
    s.ingredient_en,
    s.ingredient_ar,
    s.allergicnote_en as sku_allergicnote_en,
    s.allergicnote_ar as sku_allergicnote_ar,
    
    -- REAL PRICING DATA (Saudi Arabia - country_id = 1)
    sc.price as current_price,
    sc.old_price as original_price,
    sc.assembly_price,
    sc.country_id,
    sc.score as price_score

FROM temp_required_skus req
    INNER JOIN product p ON req.sku_id = p.sku_id
    LEFT JOIN brand b ON p.brand_id = b.id
    LEFT JOIN category cat ON p.subcategory_id = cat.id
    LEFT JOIN sku s ON p.sku_id = s.id
    LEFT JOIN sku_country sc ON p.sku_id = sc.sku_id 
        AND sc.country_id = 1 
        AND sc.is_disabled = 0

WHERE p.is_deleted = 0
    AND s.is_deleted = 0
    AND (cat.is_deleted = 0 OR cat.is_deleted IS NULL)

ORDER BY p.sku_id;

-- Step 4: Statistics query
SELECT 
    COUNT(*) as total_products_found,
    COUNT(sc.price) as products_with_pricing,
    COUNT(DISTINCT p.brand_id) as unique_brands,
    COUNT(DISTINCT p.subcategory_id) as unique_categories,
    MIN(sc.price) as min_price,
    MAX(sc.price) as max_price,
    AVG(sc.price) as avg_price
FROM temp_required_skus req
    INNER JOIN product p ON req.sku_id = p.sku_id
    LEFT JOIN sku s ON p.sku_id = s.id
    LEFT JOIN sku_country sc ON p.sku_id = sc.sku_id 
        AND sc.country_id = 1 
        AND sc.is_disabled = 0
WHERE p.is_deleted = 0
    AND s.is_deleted = 0;

-- Step 5: Cleanup
DROP TEMPORARY TABLE IF EXISTS temp_required_skus;
"""
    
    # Save the query
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Scripts\precise_complete_extraction_query.sql"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(query)
    
    print(f"✅ Precise extraction query generated!")
    print(f"📁 File: {output_file}")
    print(f"📊 Features:")
    print(f"  🎯 Exact SKU matching (no false positives)")
    print(f"  📦 {len(insert_statements)} INSERT chunks of 1000 SKUs each")
    print(f"  💰 Real pricing from sku_country table")
    print(f"  📈 Statistics validation")
    print(f"  🧹 Automatic cleanup")
    
    return output_file

def main():
    """Main execution"""
    print("🎯 Precise Query Generator (Temp Table Approach)")
    print("=" * 60)
    
    query_file = generate_precise_query()
    
    if query_file:
        print(f"\n🚀 Usage:")
        print(f"1. Run the entire SQL script in your MySQL database")
        print(f"2. It will create temp table, insert SKUs, extract data, show stats, and cleanup")
        print(f"3. Export the main query results as CSV")
        print(f"4. Process with convert_final_catalog.py")
        
        print(f"\n✅ Benefits of this approach:")
        print(f"  🎯 100% precise - only products from user events")
        print(f"  ⚡ Efficient - uses INNER JOIN with indexed temp table")
        print(f"  🔧 Manageable - avoids huge query size issues")
        print(f"  📊 Validated - includes statistics verification")

if __name__ == "__main__":
    main()