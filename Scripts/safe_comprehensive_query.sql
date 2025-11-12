-- COMPREHENSIVE EXTRACTION QUERY - Safe approach
-- Gets all required data in manageable chunks

SELECT 
    p.sku_id,
    p.name_en,
    p.name_ar,
    p.description_en,
    p.description_ar,
    p.slug,
    p.is_wrappable,
    p.is_customizable,
    p.is_international,
    p.is_digital,
    p.origincountry,
    p.subcategory_id,
    p.brand_id,
    b.name_en as brand_name_en,
    b.name_ar as brand_name_ar,
    cat.name_en as category_name_en,
    cat.name_ar as category_name_ar,
    s.code as sku_code,
    s.color as sku_color,
    s.upc,
    s.height,
    s.length,
    s.width,
    s.weight,
    s.external_product_type,
    sc.price as current_price,
    sc.old_price as original_price
FROM product p
    LEFT JOIN brand b ON p.brand_id = b.id
    LEFT JOIN category cat ON p.subcategory_id = cat.id
    LEFT JOIN sku s ON p.sku_id = s.id
    LEFT JOIN sku_country sc ON p.sku_id = sc.sku_id AND sc.country_id = 1 AND sc.is_disabled = 0
WHERE p.is_deleted = 0
    AND s.is_deleted = 0
    AND p.sku_id >= 8
    AND p.sku_id <= 136243
ORDER BY p.sku_id;