-- ========================================
-- DABDOOB CATEGORY HIERARCHY ANALYSIS
-- Extract Real Categories and Subcategories
-- ========================================

-- Query 1: Complete Category Table Structure Analysis
-- This shows us all available fields in the category table
SELECT
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE,
    COLUMN_DEFAULT,
    COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dabdoob-master'
AND TABLE_NAME = 'category'
ORDER BY ORDINAL_POSITION;

-- Query 2: Category Hierarchy Analysis
-- Understanding the complete category structure with parent-child relationships
SELECT
    c.id,
    c.name_en as category_name_en,
    c.name_ar as category_name_ar,
    c.color,
    c.displayorder,
    c.is_deleted,
    c.text_color,
    c.slug,
    c.is_hidden,
    parent.name_en as parent_category_name
FROM category c
LEFT JOIN category parent ON c.id = parent.id
WHERE c.is_deleted = 0
ORDER BY c.displayorder, c.name_en;

-- Query 3: Top-Level Categories 
-- These are the main categories
SELECT
    id,
    name_en,
    name_ar,
    displayorder,
    is_deleted,
    color,
    text_color
FROM category main
WHERE main.is_deleted = 0
ORDER BY main.displayorder, main.name_en;

-- Query 4: Complete Category Tree with Product Counts
-- Full hierarchy showing all categories with product counts
SELECT
    c.id as category_id,
    c.name_en as category_en,
    c.name_ar as category_ar,
    c.displayorder,
    c.color,
    COUNT(p.id) as product_count
FROM category c
LEFT JOIN product p ON c.id = p.subcategory_id AND p.is_deleted = 0
WHERE c.is_deleted = 0
GROUP BY c.id, c.name_en, c.name_ar, c.displayorder, c.color
ORDER BY c.displayorder, c.name_en;

-- Query 5: Products with Complete Category Information
-- Real product categorization for catalog generation
SELECT
    p.id as product_id,
    p.sku_id,
    p.name_en as product_name,
    c.id as category_id,
    c.name_en as category_name,
    c.name_ar as category_name_ar,
    c.color as category_color,
    b.name_en as brand_name,
    c.name_en as full_category_path
FROM product p
JOIN category c ON p.subcategory_id = c.id AND c.is_deleted = 0
LEFT JOIN brand b ON p.brand_id = b.id
WHERE p.is_deleted = 0
AND p.name_en IS NOT NULL
AND p.name_en != ''
ORDER BY c.displayorder, p.name_en
LIMIT 1000;

-- Query 6: Category Usage Statistics
-- Understanding which categories are most used
SELECT
    c.name_en as category,
    COUNT(p.id) as product_count,
    COUNT(DISTINCT p.brand_id) as brand_count,
    ROUND(AVG(sc.current_price), 2) as avg_price,
    c.color as category_color,
    c.displayorder
FROM category c
LEFT JOIN product p ON c.id = p.subcategory_id AND p.is_deleted = 0
LEFT JOIN sku_country sc ON p.sku_id = sc.sku_id AND sc.country_id = 1 AND sc.is_deleted = 0
WHERE c.is_deleted = 0
GROUP BY c.id, c.name_en, c.color, c.displayorder
HAVING COUNT(p.id) > 0
ORDER BY COUNT(p.id) DESC;

-- Query 7: Enhanced Product Catalog with Real Categories and SKU IDs
-- This is the main query for generating your product catalog
SELECT DISTINCT
    CONCAT('SKU', p.sku_id) as id,
    p.sku_id,
    p.id as product_id,
    p.name_en as title,
    COALESCE(p.description_en, CONCAT('Quality ', c.name_en, ' product')) as description,
    p.name_ar as title_ar,
    p.description_ar as description_ar,
    
    -- Real Category Information with Colors
    c.name_en as main_category,
    c.name_en as subcategory,
    CONCAT('[\"', c.name_en, '\"]') as categories_json,
    c.color as category_color,
    c.displayorder as category_order,
    
    -- Brand Information
    COALESCE(b.name_en, 'Misc') as brand_name,
    CONCAT('[\"', COALESCE(b.name_en, 'Misc'), '\"]') as brands_json,
    
    -- Pricing (Saudi Arabia as primary market)
    sc.current_price,
    sc.original_price,
    'SAR' as currency_code,
    
    -- Product Attributes
    p.is_wrappable,
    p.is_customizable,
    p.is_international,
    p.origincountry,
    
    -- Additional Details
    CONCAT('https://dabdoob.com/products/', p.slug) as product_url,
    
    -- Availability Status
    CASE 
        WHEN COALESCE(inv.available_quantity, 0) > 0 THEN 'IN_STOCK'
        WHEN COALESCE(inv.available_quantity, 0) = 0 THEN 'OUT_OF_STOCK'
        ELSE 'PREORDER'
    END as availability,
    
    -- Inventory Details
    COALESCE(inv.available_quantity, 0) as available_quantity

FROM product p
-- Category Information
INNER JOIN category c ON p.subcategory_id = c.id AND c.is_deleted = 0

-- Brand Information
LEFT JOIN brand b ON p.brand_id = b.id

-- Pricing (Focus on Saudi Arabia - country_id = 1)
INNER JOIN sku_country sc ON p.sku_id = sc.sku_id AND sc.country_id = 1 AND sc.is_deleted = 0

-- Inventory Status
LEFT JOIN inventory inv ON p.sku_id = inv.sku_id AND inv.country_id = 1

WHERE p.is_deleted = 0
AND p.name_en IS NOT NULL
AND p.name_en != ''
AND p.sku_id IS NOT NULL
AND c.name_en IS NOT NULL
AND sc.current_price > 0

ORDER BY c.displayorder, p.name_en
LIMIT 20000;

-- Query 8: Category Distribution Analysis
-- Understanding your category structure for Google Cloud compatibility
SELECT
    'Category Distribution' as analysis_type,
    COUNT(DISTINCT c.id) as total_categories,
    COUNT(DISTINCT p.id) as total_products,
    ROUND(AVG(products_per_category.product_count), 1) as avg_products_per_category
FROM category c
LEFT JOIN product p ON c.id = p.subcategory_id AND p.is_deleted = 0
LEFT JOIN (
    SELECT subcategory_id, COUNT(*) as product_count
    FROM product 
    WHERE is_deleted = 0
    GROUP BY subcategory_id
) products_per_category ON c.id = products_per_category.subcategory_id
WHERE c.is_deleted = 0;

-- Query 9: Brand Distribution by Category
-- Understanding brand-category relationships
SELECT
    c.name_en as category,
    COUNT(DISTINCT b.id) as unique_brands,
    COUNT(DISTINCT p.id) as products,
    GROUP_CONCAT(DISTINCT b.name_en ORDER BY b.name_en SEPARATOR ', ') as brand_list
FROM category c
JOIN product p ON c.id = p.subcategory_id AND p.is_deleted = 0
JOIN brand b ON p.brand_id = b.id
WHERE c.is_deleted = 0
GROUP BY c.id, c.name_en
ORDER BY products DESC;

-- Query 10: Export Ready Category Mapping
-- For creating categories.ndjson file
SELECT
    c.id,
    c.name_en as displayName,
    CONCAT('[\"', c.name_en, '\"]') as categoryHierarchy
FROM category c
WHERE c.is_deleted = 0
AND c.name_en IS NOT NULL
ORDER BY c.displayorder;

-- Query 11: Enhanced Category Mapping with Visual Information
-- Complete category information including colors for UI/UX
SELECT
    c.id,
    c.name_en as displayName,
    c.name_ar as displayName_ar,
    c.color as backgroundColor,
    c.text_color as textColor,
    c.displayorder as sortOrder,
    c.slug as urlSlug,
    CONCAT('[\"', c.name_en, '\"]') as categoryHierarchy,
    COUNT(p.id) as productCount
FROM category c
LEFT JOIN product p ON c.id = p.subcategory_id AND p.is_deleted = 0
WHERE c.is_deleted = 0
AND c.name_en IS NOT NULL
GROUP BY c.id, c.name_en, c.name_ar, c.color, c.text_color, c.displayorder, c.slug
ORDER BY c.displayorder;

-- Query 12: SKU-Based Product Export for Google Cloud Retail
-- Using SKU IDs as primary identifiers as recommended
SELECT DISTINCT
    CONCAT('SKU', p.sku_id) as id,
    p.sku_id as primary_sku,
    p.name_en as title,
    CASE 
        WHEN p.description_en IS NOT NULL AND p.description_en != '' 
        THEN p.description_en 
        ELSE CONCAT('Quality ', c.name_en, ' product from ', COALESCE(b.name_en, 'Dabdoob'))
    END as description,
    
    -- Category Information
    c.name_en as primary_category,
    CONCAT('[\"', c.name_en, '\"]') as categories,
    c.color as category_color,
    
    -- Brand
    COALESCE(b.name_en, 'Misc') as brand,
    CONCAT('[\"', COALESCE(b.name_en, 'Misc'), '\"]') as brands,
    
    -- Pricing
    sc.current_price as price,
    sc.original_price as originalPrice,
    'SAR' as currencyCode,
    
    -- Availability
    CASE 
        WHEN COALESCE(inv.available_quantity, 0) > 0 THEN 'IN_STOCK'
        WHEN COALESCE(inv.available_quantity, 0) = 0 THEN 'OUT_OF_STOCK'
        ELSE 'PREORDER'
    END as availability,
    
    -- Product URL
    CONCAT('https://dabdoob.com/products/', p.slug) as uri,
    
    -- Additional Attributes as separate columns
    CAST(p.sku_id AS CHAR) as sku_code,
    CASE WHEN p.is_wrappable = 1 THEN 'Gift-Wrappable' ELSE 'Standard' END as features,
    COALESCE(c.color, '#000000') as category_color_attr,
    COALESCE(p.origincountry, 'International') as origin_country

FROM product p
INNER JOIN category c ON p.subcategory_id = c.id AND c.is_deleted = 0
LEFT JOIN brand b ON p.brand_id = b.id
INNER JOIN sku_country sc ON p.sku_id = sc.sku_id AND sc.country_id = 1 AND sc.is_deleted = 0
LEFT JOIN inventory inv ON p.sku_id = inv.sku_id AND inv.country_id = 1

WHERE p.is_deleted = 0
AND p.name_en IS NOT NULL
AND p.name_en != ''
AND p.sku_id IS NOT NULL
AND c.name_en IS NOT NULL
AND sc.current_price > 0

ORDER BY c.displayorder, c.name_en, p.name_en
LIMIT 50000;