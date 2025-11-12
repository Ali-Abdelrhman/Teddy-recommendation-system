-- STEP-BY-STEP DIAGNOSTIC QUERIES
-- Run these one by one to identify the issue

-- Query 1: Test basic product table access
SELECT COUNT(*) as total_products FROM product WHERE is_deleted = 0;

-- Query 2: Test specific SKU IDs exist
SELECT sku_id, name_en FROM product WHERE sku_id IN (8, 9, 14, 15) AND is_deleted = 0;

-- Query 3: Test sku_country table access
SELECT COUNT(*) as total_sku_country FROM sku_country WHERE country_id = 1;

-- Query 4: Test pricing for specific SKUs
SELECT sku_id, price FROM sku_country WHERE sku_id IN (8, 9, 14, 15) AND country_id = 1;

-- Query 5: Test simple join
SELECT p.sku_id, p.name_en, sc.price 
FROM product p, sku_country sc 
WHERE p.sku_id = sc.sku_id 
    AND sc.country_id = 1 
    AND p.sku_id IN (8, 9, 14, 15);