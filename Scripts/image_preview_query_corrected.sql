-- Corrected query to get image previews for catalog data in GCP
-- Using correct database name 'dabdoob-master' instead of 'dabdoob_staging'

with cte as (
    select 
        s.id as sku_id,
        concat('https://dabdoob-cdn-primary.fra1.cdn.digitaloceanspaces.com/media/', m.path) as image_path,
        row_number() over (partition by s.id, sc.country_id order by m.image_order) as rn
    from sku s 
    left join sku_country sc on sc.sku_id = s.id 
    left join media m on m.target = 'sku' and m.target_id = s.id
    where not m.is_deleted 
    and m.type = 'image'
)
select 
    sku_id,
    image_path
from cte 
where rn = 1;

-- Alternative version without CTE (in case your MySQL version doesn't support window functions)
SELECT 
    s.id as sku_id,
    concat('https://dabdoob-cdn-primary.fra1.cdn.digitaloceanspaces.com/media/', m.path) as image_path
FROM sku s 
LEFT JOIN sku_country sc ON sc.sku_id = s.id 
LEFT JOIN media m ON m.target = 'sku' AND m.target_id = s.id
LEFT JOIN (
    SELECT 
        m2.target_id,
        MIN(m2.image_order) as min_order
    FROM media m2 
    WHERE m2.target = 'sku' 
    AND NOT m2.is_deleted 
    AND m2.type = 'image'
    GROUP BY m2.target_id
) first_image ON first_image.target_id = s.id AND m.image_order = first_image.min_order
WHERE NOT m.is_deleted 
AND m.type = 'image'
AND first_image.target_id IS NOT NULL;