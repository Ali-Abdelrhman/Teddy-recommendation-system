-- Check Categories and Product Types
-- Based on your feedback about needing to check these fields

-- Query 1: Check category table structure for better categories
SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    IS_NULLABLE, 
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'dabdoob-master' 
AND TABLE_NAME = 'category'
ORDER BY ORDINAL_POSITION;

-- Query 2: Sample category data to see hierarchy
SELECT 
    id, name_en, name_ar, parent_id, level, sort_order
FROM category 
WHERE id IN (15, 21, 53, 126, 131) -- From our sample subcategory_ids
LIMIT 10;

-- Query 3: Check subcategory table if it exists
SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    IS_NULLABLE, 
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'dabdoob-master' 
AND TABLE_NAME = 'subcategory'
ORDER BY ORDINAL_POSITION;

-- Query 4: Sample subcategory data
SELECT * FROM subcategory LIMIT 10;

-- Query 5: Check product types - see what values are in external_product_type
SELECT 
    external_product_type,
    COUNT(*) as count
FROM sku 
WHERE external_product_type IS NOT NULL 
    AND external_product_type != ''
GROUP BY external_product_type
ORDER BY count DESC;

-- Query 6: Check is_customizable distribution
SELECT 
    is_customizable,
    COUNT(*) as count
FROM product 
GROUP BY is_customizable;

-- Query 7: Check is_digital distribution  
SELECT 
    is_digital,
    COUNT(*) as count
FROM product 
GROUP BY is_digital;

-- Query 8: Sample products with different type characteristics
SELECT 
    p.id, p.sku_id, p.name_en,
    p.is_customizable, p.is_digital,
    s.external_product_type
FROM product p
JOIN sku s ON p.sku_id = s.id
WHERE p.sku_id IN (8, 9, 14, 15, 36)
LIMIT 10;