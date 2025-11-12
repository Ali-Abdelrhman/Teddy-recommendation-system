-- FINAL COMPREHENSIVE PRODUCT EXTRACTION QUERY
-- Extracts products with complete data including real pricing
-- Using range filter for better performance: SKU IDs 8 to 136243

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
    AND p.sku_id >= 8
    AND p.sku_id <= 136243

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
    AND p.sku_id >= 8
    AND p.sku_id <= 136243;
