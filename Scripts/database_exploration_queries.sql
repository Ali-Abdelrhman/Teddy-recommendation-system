-- Database Structure Exploration Queries
-- Run these queries one by one to understand the available data

-- 1. Check if there are price-related tables or columns
SHOW TABLES LIKE '%price%';
SHOW TABLES LIKE '%cost%';
SHOW TABLES LIKE '%amount%';

-- 2. Check product table structure for any price columns
DESCRIBE product;

-- 3. Check if there are separate price/inventory tables
SHOW TABLES LIKE '%inventory%';
SHOW TABLES LIKE '%stock%';
SHOW TABLES LIKE '%retail%';

-- 4. Look for color-related tables or columns
SHOW TABLES LIKE '%color%';
SHOW TABLES LIKE '%variant%';
SHOW TABLES LIKE '%option%';

-- 5. Check SKU table structure (might have pricing)
DESCRIBE sku;

-- 6. Check if there are any tables with 'value', 'rate', or 'selling' in the name
SHOW TABLES LIKE '%value%';
SHOW TABLES LIKE '%rate%';
SHOW TABLES LIKE '%selling%';
SHOW TABLES LIKE '%sale%';

-- 7. Sample a few records to see what's available
SELECT 
    id, sku_id, name_en, brand_name_en, category_name_en,
    sku_color, sku_code, is_customizable, is_digital
FROM (
    SELECT p.id, p.sku_id, p.name_en, 
           b.name_en as brand_name_en,
           c.name_en as category_name_en,
           s.color as sku_color,
           s.code as sku_code,
           p.is_customizable,
           p.is_digital
    FROM product p
    LEFT JOIN brand b ON p.brand_id = b.id
    LEFT JOIN category c ON p.subcategory_id = c.id
    LEFT JOIN sku s ON p.sku_id = s.id
    WHERE p.is_deleted = 0
    LIMIT 5
) AS sample_data;