-- FINAL Comprehensive Product Data Query
-- Using actual pricing from sku_country table and smart color extraction

SELECT 
    -- Basic product info
    p.id,
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
    p.subcategory_id,
    
    -- Brand information
    b.name_en as brand_name_en,
    b.name_ar as brand_name_ar,
    
    -- Category information (need to check hierarchy)
    cat.name_en as category_name_en,
    cat.name_ar as category_name_ar,
    
    -- SKU details
    s.code as sku_code,
    s.color as sku_color,
    s.item_number,
    s.height,
    s.length,
    s.width,
    s.weight,
    s.external_product_type,
    s.external_product_id,
    
    -- ACTUAL PRICING DATA (from sku_country for Saudi Arabia - country_id = 1)
    sc.price as current_price,
    sc.old_price as original_price,
    sc.assembly_price,
    sc.country_id,
    
    -- INVENTORY DATA (from inventory table - though structure shows it's more like purchase orders)
    inv.quantity as inventory_quantity,
    inv.cost as inventory_cost

FROM product p
    -- Join brand
    LEFT JOIN brand b ON p.brand_id = b.id
    
    -- Join category (need to verify if this is correct relationship)
    LEFT JOIN category cat ON p.subcategory_id = cat.id
    
    -- Join SKU for physical properties and type info
    LEFT JOIN sku s ON p.sku_id = s.id
    
    -- Join sku_country for ACTUAL PRICING (Saudi Arabia = country_id 1)
    LEFT JOIN sku_country sc ON p.sku_id = sc.sku_id 
        AND sc.country_id = 1 
        AND sc.is_disabled = 0
    
    -- Join inventory for cost information (though this seems to be purchase orders)
    LEFT JOIN inventory inv ON p.sku_id = inv.sku_id
        AND inv.is_deleted = 0

WHERE p.is_deleted = 0
    AND p.sku_id IN (
        -- All SKU IDs from our user events (replace with actual list)
        8, 9, 14, 15, 36, 52, 66, 71, 73, 75, 84, 85, 122, 130, 136, 140, 142, 144, 161, 170, 171, 174, 175, 180, 189, 238, 247, 271, 284, 309, 327, 330, 334
        -- This should be the full list of 17,892 SKU IDs
    )

ORDER BY p.sku_id;