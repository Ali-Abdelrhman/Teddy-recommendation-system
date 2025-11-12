-- ULTRA SIMPLE TEST - Just basic product info
SELECT 
    p.sku_id,
    p.name_en,
    sc.price
FROM product p
    LEFT JOIN sku_country sc ON p.sku_id = sc.sku_id AND sc.country_id = 1
WHERE p.sku_id IN (8, 9, 14, 15)
ORDER BY p.sku_id;