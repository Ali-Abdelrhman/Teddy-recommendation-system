-- Updated Targeted Data Discovery Queries
-- Based on available tables: pricing, inventory, priceHistory, priceCampaign, etc.

-- Query 1: Check PRICING table structure (main pricing data)
SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    IS_NULLABLE, 
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'dabdoob-master' 
AND TABLE_NAME = 'pricing'
ORDER BY ORDINAL_POSITION;

-- Query 2: Sample PRICING data to understand structure
SELECT * FROM pricing LIMIT 5;

-- Query 3: Check INVENTORY table structure
SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    IS_NULLABLE, 
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'dabdoob-master' 
AND TABLE_NAME = 'inventory'
ORDER BY ORDINAL_POSITION;

-- Query 4: Sample INVENTORY data
SELECT * FROM inventory LIMIT 5;

-- Query 5: Check priceCampaign table (for promotional pricing)
SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    IS_NULLABLE, 
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'dabdoob-master' 
AND TABLE_NAME = 'priceCampaign'
ORDER BY ORDINAL_POSITION;

-- Query 6: Check sku_country table (regional pricing/availability)
SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    IS_NULLABLE, 
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'dabdoob-master' 
AND TABLE_NAME = 'sku_country'
ORDER BY ORDINAL_POSITION;

-- Query 7: Sample sku_country data
SELECT * FROM sku_country WHERE sku_id IN (8, 9, 14, 15, 36) LIMIT 10;

-- Query 8: Check SKU table for color information
SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    IS_NULLABLE, 
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'dabdoob-master' 
AND TABLE_NAME = 'sku'
ORDER BY ORDINAL_POSITION;

-- Query 9: Sample SKU data for color information
SELECT 
    id, code, color, item_number, height, length, width, weight
FROM sku 
WHERE id IN (8, 9, 14, 15, 36)
LIMIT 5;