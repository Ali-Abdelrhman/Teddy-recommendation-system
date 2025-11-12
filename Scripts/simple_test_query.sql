-- SIMPLE TEST QUERY - Start with this to verify the approach works
-- Test with just a few products first

SELECT 
    p.id as product_id,
    p.sku_id,
    p.name_en,
    p.description_en,
    p.slug,
    b.name_en as brand_name_en,
    cat.name_en as category_name_en,
    s.code as sku_code,
    s.color as sku_color,
    s.upc,
    sc.price as current_price,
    sc.old_price as original_price
FROM product p
    LEFT JOIN brand b ON p.brand_id = b.id
    LEFT JOIN category cat ON p.subcategory_id = cat.id
    LEFT JOIN sku s ON p.sku_id = s.id
    LEFT JOIN sku_country sc ON p.sku_id = sc.sku_id AND sc.country_id = 1 AND sc.is_disabled = 0
WHERE p.is_deleted = 0
    AND s.is_deleted = 0
    AND p.sku_id IN (8, 9, 14, 15, 36, 52, 66, 71, 73, 75)
ORDER BY p.sku_id;