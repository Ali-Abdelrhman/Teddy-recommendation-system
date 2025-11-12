-- ALTERNATIVE SIMPLE APPROACH - No complex joins
-- Just get basic product data first

SELECT 
    sku_id,
    name_en,
    description_en,
    brand_id,
    subcategory_id
FROM product 
WHERE is_deleted = 0 
    AND sku_id >= 8 
    AND sku_id <= 75
ORDER BY sku_id;