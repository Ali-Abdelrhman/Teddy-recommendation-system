-- CORRECTED query to get image previews with proper Product ID to SKU ID mapping
-- This maps: Product ID -> Product.sku_id -> Media.target_id (where target='sku')

with cte as (
    select 
        p.id as product_id,
        p.sku_id,
        concat('https://dabdoob-cdn-primary.fra1.cdn.digitaloceanspaces.com/media/', m.path) as image_path,
        row_number() over (partition by p.id order by m.image_order) as rn
    from product p 
    left join media m on m.target = 'sku' and m.target_id = p.sku_id
    where not m.is_deleted 
    and m.type = 'image'
    and p.sku_id is not null  -- Only products that have a SKU
)
select 
    product_id,
    sku_id,
    image_path
from cte 
where rn = 1;

-- Alternative: Get all images for products (not just first one)
-- Uncomment below if you want to see all images per product

/*
SELECT 
    p.id as product_id,
    p.sku_id,
    concat('https://dabdoob-cdn-primary.fra1.cdn.digitaloceanspaces.com/media/', m.path) as image_path,
    m.image_order
FROM product p 
LEFT JOIN media m ON m.target = 'sku' AND m.target_id = p.sku_id
WHERE NOT m.is_deleted 
AND m.type = 'image'
AND p.sku_id IS NOT NULL
ORDER BY p.id, m.image_order;
*/