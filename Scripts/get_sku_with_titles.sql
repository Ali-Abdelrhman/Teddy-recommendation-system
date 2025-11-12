-- Query to get SKU_ID with corresponding product title and description
-- This will help verify if the catalog has the correct SKU_IDs

SELECT 
    s.id as sku_id,
    s.code as sku_code,
    s.name_en as sku_name_en,
    s.name_ar as sku_name_ar,
    s.color as sku_color,
    p.id as product_id,
    p.name_en as product_title_en,
    p.name_ar as product_title_ar,
    p.description_en as product_description_en,
    p.description_ar as product_description_ar,
    p.upc,
    b.name_en as brand_name_en,
    c.name_en as category_name_en,
    s.is_deleted as sku_deleted,
    p.is_deleted as product_deleted
FROM 
    sku s
    LEFT JOIN product p ON p.sku_id = s.id
    LEFT JOIN brand b ON p.brand_id = b.id
    LEFT JOIN category c ON p.subcategory_id = c.id
WHERE 
    s.is_deleted = 0  -- Only active SKUs
    AND p.is_deleted = 0  -- Only active products
    AND p.id IS NOT NULL  -- Only SKUs that have products
ORDER BY 
    s.id;

-- Alternative: If you want to focus on SKUs that have images
-- Uncomment the query below to only get SKUs that have images in the media table

/*
SELECT 
    s.id as sku_id,
    s.code as sku_code,
    s.name_en as sku_name_en,
    p.id as product_id,
    p.name_en as product_title_en,
    p.description_en as product_description_en,
    b.name_en as brand_name_en,
    COUNT(m.id) as image_count
FROM 
    sku s
    LEFT JOIN product p ON p.sku_id = s.id
    LEFT JOIN brand b ON p.brand_id = b.id
    LEFT JOIN media m ON m.target = 'sku' AND m.target_id = s.id AND m.type = 'image' AND NOT m.is_deleted
WHERE 
    s.is_deleted = 0
    AND p.is_deleted = 0
    AND p.id IS NOT NULL
    AND m.id IS NOT NULL  -- Only SKUs with images
GROUP BY 
    s.id, s.code, s.name_en, p.id, p.name_en, p.description_en, b.name_en
ORDER BY 
    s.id;
*/