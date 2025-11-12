# Data Sampling Queries for Recommended for You Model

This document contains SQL queries to sample data from various tables to assess data quality and prepare for generating the required user events for the "Recommended for You" model.

## 🎯 Required Event Types
- **detail-page-view**: 10,000+ events (product page visits)
- **home-page-view**: 10,000+ events (homepage visits)  
- **add-to-cart**: 10,000+ events (cart additions)

---

## 📊 Data Sampling Queries

### 1. Activity Table Analysis (127G - Most Promising)
```sql
-- Sample recent activity data to understand event types
SELECT 
    action,
    target,
    COUNT(*) as event_count
FROM activity 
WHERE time >= DATE_SUB(NOW(), INTERVAL 90 DAY)
GROUP BY action, target
ORDER BY event_count DESC
LIMIT 20;
```

```sql
-- Sample detailed activity records
SELECT 
    id,
    admin_id,
    action,
    target,
    target_id,
    country_id,
    time,
    body,
    raw
FROM activity 
WHERE time >= DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY time DESC
LIMIT 50;
```

### 2. Hit Table Analysis (522M - Page Views)
```sql
-- Sample hit data to understand page tracking
SELECT 
    target,
    COUNT(*) as hit_count
FROM hit 
WHERE time >= DATE_SUB(NOW(), INTERVAL 90 DAY)
GROUP BY target
ORDER BY hit_count DESC
LIMIT 20;
```

```sql
-- Sample detailed hit records for product pages
SELECT 
    id,
    device_id,
    user_id,
    target,
    target_id,
    time
FROM hit 
WHERE time >= DATE_SUB(NOW(), INTERVAL 7 DAY)
    AND target LIKE '%product%'
ORDER BY time DESC
LIMIT 50;
```

```sql
-- Sample home page hits
SELECT 
    id,
    device_id,
    user_id,
    target,
    target_id,
    time
FROM hit 
WHERE time >= DATE_SUB(NOW(), INTERVAL 7 DAY)
    AND (target LIKE '%home%' OR target LIKE '%index%' OR target = '/')
ORDER BY time DESC
LIMIT 50;
```

### 3. Search Table Analysis (80K - Product Interest)
```sql
-- Sample search data to understand user product interest
SELECT 
    term,
    COUNT(*) as search_count
FROM search 
WHERE CDate >= DATE_SUB(NOW(), INTERVAL 90 DAY)
GROUP BY term
ORDER BY search_count DESC
LIMIT 30;
```

```sql
-- Sample recent search records
SELECT 
    id,
    device_id,
    user_id,
    term,
    CDate,
    country_id
FROM search 
WHERE CDate >= DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY CDate DESC
LIMIT 50;
```

### 4. Wishlist Analysis (2M - Add-to-Cart Behavior)
```sql
-- Sample wishlist data for add-to-cart events
SELECT 
    id,
    name,
    user_id,
    country_id,
    is_deleted,
    is_default,
    CDate,
    UDate
FROM wishlist 
WHERE is_deleted = 0
    AND CDate >= DATE_SUB(NOW(), INTERVAL 90 DAY)
ORDER BY CDate DESC
LIMIT 50;
```

### 5. Product Favorite Analysis (32K - Product Interest)
```sql
-- Sample product favorites for interest signals
SELECT 
    product_id,
    COUNT(*) as favorite_count
FROM productfavorite 
WHERE CDate >= DATE_SUB(NOW(), INTERVAL 90 DAY)
GROUP BY product_id
ORDER BY favorite_count DESC
LIMIT 30;
```

```sql
-- Sample recent product favorites
SELECT 
    id,
    product_id,
    user_id,
    CDate
FROM productfavorite 
WHERE CDate >= DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY CDate DESC
LIMIT 50;
```

### 6. Homepage Configuration Analysis (64K)
```sql
-- Sample homepage data
SELECT 
    id,
    home_id,
    display_order,
    title_text_en,
    title_text_ar,
    target,
    target_list,
    is_deleted,
    is_visible,
    CDate,
    UDate
FROM homepage 
WHERE is_deleted = 0
    AND is_visible = 1
ORDER BY CDate DESC
LIMIT 20;
```

### 7. Landing Page Analysis (16K)
```sql
-- Sample landing page data
SELECT 
    id,
    country_id,
    name_en,
    name_ar,
    type,
    target,
    target_id,
    is_deleted,
    CDate,
    UDate
FROM landing 
WHERE is_deleted = 0
    AND CDate >= DATE_SUB(NOW(), INTERVAL 90 DAY)
ORDER BY CDate DESC
LIMIT 30;
```

---

## 🔍 Data Quality Assessment Queries

### User Activity Summary
```sql
-- Count total users with activity in last 90 days
SELECT 
    COUNT(DISTINCT admin_id) as active_users_activity,
    COUNT(*) as total_activity_events,
    MIN(time) as earliest_event,
    MAX(time) as latest_event
FROM activity 
WHERE time >= DATE_SUB(NOW(), INTERVAL 90 DAY);
```

### Hit Data Summary
```sql
-- Count total users with hits in last 90 days
SELECT 
    COUNT(DISTINCT user_id) as active_users_hits,
    COUNT(*) as total_hit_events,
    MIN(time) as earliest_hit,
    MAX(time) as latest_hit
FROM hit 
WHERE time >= DATE_SUB(NOW(), INTERVAL 90 DAY);
```

### Search Activity Summary
```sql
-- Count search activity
SELECT 
    COUNT(DISTINCT user_id) as searching_users,
    COUNT(*) as total_searches,
    COUNT(DISTINCT term) as unique_search_terms,
    MIN(CDate) as earliest_search,
    MAX(CDate) as latest_search
FROM search 
WHERE CDate >= DATE_SUB(NOW(), INTERVAL 90 DAY);
```

### Wishlist Activity Summary
```sql
-- Count wishlist activity
SELECT 
    COUNT(DISTINCT user_id) as users_with_wishlists,
    COUNT(*) as total_wishlists,
    MIN(CDate) as earliest_wishlist,
    MAX(CDate) as latest_wishlist
FROM wishlist 
WHERE is_deleted = 0
    AND CDate >= DATE_SUB(NOW(), INTERVAL 90 DAY);
```

---

## 📝 Instructions

1. **Run these queries** in your database to sample the data
2. **Export the results** as CSV or JSON files
3. **Send me the sample data** so I can analyze:
   - Data quality and completeness
   - Event type mapping possibilities
   - User behavior patterns
   - Time distribution of events

4. **Based on the sample data**, I will provide:
   - Specific queries to generate `detail-page-view` events
   - Specific queries to generate `home-page-view` events  
   - Specific queries to generate `add-to-cart` events
   - Data transformation scripts for NDJSON format

## 🎯 Expected Outcomes

From these tables, we should be able to generate:
- **10,000+ detail-page-view events** from `hit` table (product page visits)
- **10,000+ home-page-view events** from `hit` table (homepage visits)
- **10,000+ add-to-cart events** from `wishlist` + `productfavorite` tables

This will make your dataset compatible with the "Recommended for You" model requirements!