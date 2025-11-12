-- ALTERNATIVE: More Precise Query Using Temporary Table
-- This approach creates a temp table with exact SKU IDs, then joins for perfect precision

-- Step 1: Create temporary table with required SKU IDs
DROP TEMPORARY TABLE IF EXISTS temp_required_skus;

CREATE TEMPORARY TABLE temp_required_skus (
    sku_id INT PRIMARY KEY
);

-- Step 2: Insert all required SKU IDs (this avoids the large IN clause issue)
-- You can run this in chunks if needed
INSERT INTO temp_required_skus (sku_id) VALUES 
(8),(9),(14),(15),(36),(52),(66),(71),(73),(75),(84),(85),(122),(130),(136),(140),(142),(144),(161),(170),(171),(174),(175),(180),(189),(238),(247),(271),(284),(309),(327),(330),(334);
-- Note: This is just a sample. You'll need to add all 17,892 SKU IDs
-- Or use a script to generate the full INSERT statement

-- Step 3: Main query with perfect precision
SELECT 
    -- Basic product info
    p.id as product_id,
    p.sku_id,
    p.name_en,
    p.name_ar,
    p.description_en,
    p.description_ar,
    p.slug,
    p.is_deleted,
    p.is_wrappable,
    p.is_customizable,
    p.is_international,
    p.is_digital,
    p.disable_cash,
    p.subcategory_id,
    p.brand_id,
    p.origincountry,
    p.allergicnote_en as product_allergicnote_en,
    p.allergicnote_ar as product_allergicnote_ar,
    p.howtouse_en,
    p.howtouse_ar,
    p.nutrition_en,
    p.nutrition_ar,
    
    -- Brand information
    b.name_en as brand_name_en,
    b.name_ar as brand_name_ar,
    b.slug as brand_slug,
    
    -- Category information (flat structure)
    cat.name_en as category_name_en,
    cat.name_ar as category_name_ar,
    cat.slug as category_slug,
    cat.color as category_color,
    
    -- SKU details with all metadata
    s.name_en as sku_name_en,
    s.name_ar as sku_name_ar,
    s.code as sku_code,
    s.color as sku_color,
    s.item_number,
    s.upc,
    s.height,
    s.length,
    s.width,
    s.weight,
    s.box_count,
    s.external_product_type,
    s.external_product_id,
    s.unit,
    s.ingredient_en,
    s.ingredient_ar,
    s.allergicnote_en as sku_allergicnote_en,
    s.allergicnote_ar as sku_allergicnote_ar,
    
    -- REAL PRICING DATA (Saudi Arabia - country_id = 1)
    sc.price as current_price,
    sc.old_price as original_price,
    sc.assembly_price,
    sc.country_id,
    sc.score as price_score

FROM temp_required_skus req
    INNER JOIN product p ON req.sku_id = p.sku_id
    LEFT JOIN brand b ON p.brand_id = b.id
    LEFT JOIN category cat ON p.subcategory_id = cat.id
    LEFT JOIN sku s ON p.sku_id = s.id
    LEFT JOIN sku_country sc ON p.sku_id = sc.sku_id 
        AND sc.country_id = 1 
        AND sc.is_disabled = 0

WHERE p.is_deleted = 0
    AND s.is_deleted = 0
    AND (cat.is_deleted = 0 OR cat.is_deleted IS NULL)

ORDER BY p.sku_id;