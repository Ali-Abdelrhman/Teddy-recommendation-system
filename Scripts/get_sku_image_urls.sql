-- Query to get SKU_ID with Dabdoob website product page URLs
-- This creates the product page URL using the product slug

SELECT 
    s.id as sku_id,
    CASE 
        WHEN p.slug IS NOT NULL AND p.slug != '' 
        THEN concat('https://dabdoob.com/products/', p.slug)
        ELSE concat('https://dabdoob.com/products/', s.id)  -- Fallback to SKU ID if no slug
    END as uri
FROM sku s 
LEFT JOIN product p ON p.sku_id = s.id
WHERE s.is_deleted = 0 
AND p.is_deleted = 0
AND p.id IS NOT NULL  -- Only SKUs that have products
ORDER BY s.id;

-- Alternative: If you need different URL format or domain
/*
SELECT 
    s.id as sku_id,
    concat('https://www.dabdoob.com/product/', s.id) as uri  -- Using SKU ID directly
FROM sku s 
WHERE s.is_deleted = 0
ORDER BY s.id;

-- OR using product ID instead of SKU ID:
SELECT 
    s.id as sku_id,
    concat('https://dabdoob.com/products/', p.id) as uri  -- Using product ID
FROM sku s 
LEFT JOIN product p ON p.sku_id = s.id
WHERE s.is_deleted = 0 AND p.is_deleted = 0
ORDER BY s.id;
*/