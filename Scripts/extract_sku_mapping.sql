-- Simple query to map product_id to sku_id
-- Export this as CSV: product_id_to_sku_mapping.csv

SELECT 
    product_id,
    id as sku_id,
    code as sku_code
FROM sku 
WHERE is_deleted = 0
ORDER BY product_id ASC;

-- Alternative: Get one SKU per product (if multiple SKUs exist)
SELECT 
    product_id,
    MIN(id) as primary_sku_id,
    MIN(code) as primary_sku_code
FROM sku 
WHERE is_deleted = 0
GROUP BY product_id
ORDER BY product_id ASC;