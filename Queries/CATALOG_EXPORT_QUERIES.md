# Database Queries for Catalog Export

## Query 1: Basic Product Information
```sql
SELECT 
    s.id,
    p.name_en as title,
    CASE 
        WHEN SUM(i.cost) > 0 THEN 'IN_STOCK' 
        ELSE 'OUT_OF_STOCK' 
    END as availability,
    p.description_en as description
FROM sku s
JOIN product p ON s.product_id = p.id
LEFT JOIN inventory i ON s.id = i.sku_id
WHERE p.is_deleted = 0 AND s.is_deleted = 0
GROUP BY s.id, p.name_en, p.description_en;
```

## Query 2: Categories
```sql
SELECT 
    s.id,
    c.name_en as categories
FROM sku s
JOIN product p ON s.product_id = p.id
JOIN subcategory sc ON p.subcategory_id = sc.id
JOIN category c ON sc.category_id = c.id
WHERE p.is_deleted = 0 AND s.is_deleted = 0;
```

## Query 3: Price Information
```sql
SELECT 
    sc.sku_id as id,
    sc.price,
    sc.old_price as originalPrice,
    co.currencyIso as currencyCode
FROM sku_country sc
JOIN country co ON sc.country_id = co.id
WHERE sc.is_disabled = 0;
```

## Query 4: Brands
```sql
SELECT 
    s.id,
    b.name_en as brands
FROM sku s
JOIN product p ON s.product_id = p.id
JOIN brand b ON p.brand_id = b.id
WHERE p.is_deleted = 0 AND s.is_deleted = 0;
```

## Query 5: Attributes
```sql
SELECT 
    s.id,
    av.name_en as attribute_value,
    a.name_en as attribute_name
FROM sku s
JOIN product p ON s.product_id = p.id
JOIN product_attributevalue pav ON p.id = pav.product_id
JOIN attributevalue av ON pav.attributevalue_id = av.id
JOIN attribute a ON av.attribute_id = a.id
WHERE p.is_deleted = 0 AND s.is_deleted = 0 AND a.is_deleted = 0;
```

## Query 6: Tags
```sql
SELECT 
    s.id,
    t.name_en as tags
FROM sku s
JOIN product p ON s.product_id = p.id
JOIN tag_product tp ON p.id = tp.product_id
JOIN tag t ON tp.tag_id = t.id
WHERE p.is_deleted = 0 AND s.is_deleted = 0 AND t.is_deleted = 0;
```

## Query 7: Product URLs
```sql
SELECT 
    s.id,
    CONCAT('https://dabdoob.com/ar-SA/product/', p.slug, '-', p.id, '/?default_sku=', s.id) as uri
FROM sku s
JOIN product p ON s.product_id = p.id
WHERE p.is_deleted = 0 AND s.is_deleted = 0;
```