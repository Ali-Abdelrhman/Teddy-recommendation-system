-- ENHANCED EXTRACTION: Get missing products with fallback data
-- This query will extract the 2,903 missing products with basic info

SELECT DISTINCT
    p.sku_id,
    
    -- Names with fallbacks
    COALESCE(p.name_en, p.name_ar, CONCAT('Product ', p.sku_id)) as name_en,
    COALESCE(p.name_ar, p.name_en, CONCAT('منتج ', p.sku_id)) as name_ar,
    
    -- Descriptions with fallbacks
    COALESCE(p.description_en, p.description_ar, 'Quality product available for purchase') as description_en,
    COALESCE(p.description_ar, p.description_en, 'منتج عالي الجودة متاح للشراء') as description_ar,
    
    -- Slug
    COALESCE(p.slug, CONCAT('product-', p.sku_id)) as slug,
    
    -- Product flags with defaults
    COALESCE(p.is_wrappable, 0) as is_wrappable,
    COALESCE(p.is_customizable, 0) as is_customizable,
    COALESCE(p.is_international, 0) as is_international,
    COALESCE(p.is_digital, 0) as is_digital,
    
    -- Origin with fallback
    COALESCE(p.origincountry, 'Saudi Arabia') as origincountry,
    
    -- Category info
    p.subcategory_id,
    
    -- Brand info with fallbacks
    COALESCE(b.id, 1) as brand_id,
    COALESCE(b.name_en, 'Generic Brand') as brand_name_en,
    COALESCE(b.name_ar, 'علامة تجارية عامة') as brand_name_ar,
    
    -- Category info with fallbacks
    COALESCE(c.name_en, 'General') as category_name_en,
    COALESCE(c.name_ar, 'عام') as category_name_ar,
    
    -- SKU info
    s.sku_code,
    COALESCE(s.sku_color, 'Multi-Color') as sku_color,
    s.upc,
    COALESCE(s.height, 0) as height,
    COALESCE(s.length, 0) as length,
    COALESCE(s.width, 0) as width,
    COALESCE(s.weight, 0) as weight,
    s.external_product_type,
    
    -- Pricing with smart fallbacks
    COALESCE(sc.current_price, sc.original_price, 25.0) as current_price,
    COALESCE(sc.original_price, sc.current_price * 1.2, 30.0) as original_price

FROM product p

-- Left joins to keep all products
LEFT JOIN brand b ON p.brand_id = b.id
LEFT JOIN category c ON p.subcategory_id = c.id  
LEFT JOIN sku s ON p.sku_id = s.product_id
LEFT JOIN sku_country sc ON s.id = sc.sku_id AND sc.country_id = 1

WHERE p.sku_id IN (
    -- Insert the 2,903 missing SKU IDs here
    209, 1259, 1293, 2433, 4160, 5184, 5292, 7010, 8715, 8727
    -- ... (all 2,903 missing IDs)
)

ORDER BY p.sku_id;