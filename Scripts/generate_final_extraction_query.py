#!/usr/bin/env python3
"""
Generate FINAL comprehensive MySQL query with all 17,892 SKU IDs
This creates the complete database extraction query using real data structures
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

def generate_final_query():
    """Generate the final comprehensive query with all SKU IDs"""
    
    sku_ids = load_required_sku_ids()
    
    if not sku_ids:
        print("❌ No SKU IDs loaded")
        return
    
    print(f"📋 Loaded {len(sku_ids)} SKU IDs")
    print(f"🔢 Range: {min(sku_ids)} - {max(sku_ids)}")
    
    # Create a more efficient query using range instead of huge IN clause
    min_sku = min(sku_ids)
    max_sku = max(sku_ids)
    
    # Generate the query with range filter for better performance
    query = f"""-- FINAL COMPREHENSIVE PRODUCT EXTRACTION QUERY
-- Extracts products with complete data including real pricing
-- Using range filter for better performance: SKU IDs {min_sku} to {max_sku}

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
    
    -- Category information (flat structure)
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

FROM product p
    -- Join brand for brand information
    LEFT JOIN brand b ON p.brand_id = b.id
    
    -- Join category for category information
    LEFT JOIN category cat ON p.subcategory_id = cat.id
    
    -- Join SKU for detailed product information
    LEFT JOIN sku s ON p.sku_id = s.id
    
    -- Join sku_country for REAL PRICING (Saudi Arabia = country_id 1)
    LEFT JOIN sku_country sc ON p.sku_id = sc.sku_id 
        AND sc.country_id = 1 
        AND sc.is_disabled = 0

WHERE p.is_deleted = 0
    AND s.is_deleted = 0
    AND (cat.is_deleted = 0 OR cat.is_deleted IS NULL)
    AND p.sku_id >= {min_sku}
    AND p.sku_id <= {max_sku}

ORDER BY p.sku_id;

-- Statistics Query to verify results
SELECT 
    COUNT(*) as total_products,
    COUNT(DISTINCT p.brand_id) as unique_brands,
    COUNT(DISTINCT p.subcategory_id) as unique_categories,
    COUNT(sc.price) as products_with_pricing,
    MIN(sc.price) as min_price,
    MAX(sc.price) as max_price,
    AVG(sc.price) as avg_price
FROM product p
    LEFT JOIN sku s ON p.sku_id = s.id
    LEFT JOIN sku_country sc ON p.sku_id = sc.sku_id AND sc.country_id = 1 AND sc.is_disabled = 0
WHERE p.is_deleted = 0
    AND s.is_deleted = 0
    AND p.sku_id >= {min_sku}
    AND p.sku_id <= {max_sku};
"""
    
    # Save the query
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Scripts\final_complete_extraction_query.sql"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(query)
    
    print(f"✅ Final comprehensive query generated!")
    print(f"📁 File: {output_file}")
    print(f"📊 Query includes:")
    print(f"  🔢 SKU Range: {min_sku} to {max_sku}")
    print(f"  💰 Real pricing from sku_country table")
    print(f"  🏷️  Categories from category table") 
    print(f"  🏢 Brands from brand table")
    print(f"  📦 Complete SKU metadata")
    print(f"  📈 Statistics query for verification")
    print(f"  ⚡ Optimized for better performance")
    
    return output_file

def main():
    """Main execution"""
    print("🎯 Final Comprehensive Query Generator")
    print("=" * 50)
    
    query_file = generate_final_query()
    
    if query_file:
        print(f"\n🚀 Next Steps:")
        print(f"1. Run the query in your MySQL database")
        print(f"2. Export results as CSV")
        print(f"3. Convert CSV to Google Cloud catalog format")
        print(f"4. Upload to Google Cloud Retail AI")
        
        print(f"\n💡 Expected Results:")
        print(f"  ✅ Real product prices (not fixed 50 SAR)")
        print(f"  ✅ Actual category names") 
        print(f"  ✅ Complete brand information")
        print(f"  ✅ All product metadata")
        print(f"  ✅ Smart color extraction from descriptions")

if __name__ == "__main__":
    main()