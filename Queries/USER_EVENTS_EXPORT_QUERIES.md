# User Events Export Queries 

## Query 1: Purchase Events (from invoice and invoiceItem)
```sql
SELECT DISTINCT
    'purchase' as eventType,
    CAST(i.user_id AS CHAR) as visitorId,
    CONCAT('SESSION_', i.device_id, '_', DATE_FORMAT(i.CDate, '%Y%m%d%H')) as sessionId,
    DATE_FORMAT(i.CDate, '%Y-%m-%dT%H:%i:%sZ') as eventTime,
    JSON_OBJECT(
        'userId', CAST(i.user_id AS CHAR),
        'directUserRequest', true
    ) as userInfo,
    JSON_ARRAY(
        JSON_OBJECT(
            'product', JSON_OBJECT('id', CAST(ii.sku_id AS CHAR)),
            'quantity', COALESCE(JSON_EXTRACT(ii.sku, '$.quantity'), 1)
        )
    ) as productDetails
FROM invoice i
JOIN invoiceItem ii ON i.id = ii.invoice_id
WHERE i.user_id IS NOT NULL 
    AND ii.sku_id IS NOT NULL
    AND i.status = 1
    AND i.CDate >= DATE_SUB(NOW(), INTERVAL 90 DAY);
```

## Query 2: Add to Cart Events (from hit table where target='product')
```sql
SELECT DISTINCT
    'add-to-cart' as eventType,
    CAST(h.user_id AS CHAR) as visitorId,
    CONCAT('SESSION_', h.device_id, '_', DATE_FORMAT(h.time, '%Y%m%d%H')) as sessionId,
    DATE_FORMAT(h.time, '%Y-%m-%dT%H:%i:%sZ') as eventTime,
    JSON_OBJECT(
        'userId', CAST(h.user_id AS CHAR),
        'directUserRequest', true
    ) as userInfo,
    JSON_ARRAY(
        JSON_OBJECT(
            'product', JSON_OBJECT('id', CAST(h.target_id AS CHAR)),
            'quantity', 1
        )
    ) as productDetails
FROM hit h
WHERE h.target = 'product'
    AND h.user_id IS NOT NULL 
    AND h.target_id IS NOT NULL
    AND h.time >= DATE_SUB(NOW(), INTERVAL 90 DAY);
```

## Query 3: Product View Events (from hit table - all product related targets)
```sql
SELECT DISTINCT
    'detail-page-view' as eventType,
    CAST(h.user_id AS CHAR) as visitorId,
    CONCAT('SESSION_', h.device_id, '_', DATE_FORMAT(h.time, '%Y%m%d%H')) as sessionId,
    DATE_FORMAT(h.time, '%Y-%m-%dT%H:%i:%sZ') as eventTime,
    JSON_OBJECT(
        'userId', CAST(h.user_id AS CHAR),
        'directUserRequest', true
    ) as userInfo,
    JSON_ARRAY(
        JSON_OBJECT(
            'product', JSON_OBJECT('id', CAST(h.target_id AS CHAR)),
            'quantity', 1
        )
    ) as productDetails
FROM hit h
WHERE h.target IN ('sku', 'product', 'item')
    AND h.user_id IS NOT NULL 
    AND h.target_id IS NOT NULL
    AND h.time >= DATE_SUB(NOW(), INTERVAL 90 DAY);
```
