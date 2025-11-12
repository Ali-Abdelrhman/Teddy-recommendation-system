# 🔍 **Missing Tables Sample Data Queries**

> **Purpose**: Check data quality and relationships in the key tables for GCP extraction

---

## 🎯 **Query 1: Product Attribute Values Sample**

```sql
-- Check how products link to attributes and their values
SELECT 
    pav.product_id,
    pav.attributevalue_id,
    a.name_en as attribute_name,
    av.name_en as attribute_value,
    av.color as attribute_color,
    p.name_en as product_name
FROM product_attributevalue pav
JOIN attributevalue av ON pav.attributevalue_id = av.id AND av.is_deleted = 0
JOIN attribute a ON av.attribute_id = a.id AND a.is_deleted = 0
JOIN product p ON pav.product_id = p.id AND p.is_deleted = 0
WHERE p.name_en IS NOT NULL
    AND p.name_en != ''
    AND a.name_en IS NOT NULL
    AND av.name_en IS NOT NULL
ORDER BY pav.product_id, a.id
LIMIT 15;
```

---

## 🎯 **Query 2: Price History Sample**

```sql
-- Check pricing data structure and currency
SELECT 
    ph.id,
    ph.sku_id,
    ph.price,
    ph.old_price,
    ph.admin_id,
    ph.CDate as price_update_date,
    s.product_id,
    s.name_en as sku_name,
    s.code as sku_code,
    p.name_en as product_name
FROM priceHistory ph
JOIN sku s ON ph.sku_id = s.id AND s.is_deleted = 0
JOIN product p ON s.product_id = p.id AND p.is_deleted = 0
WHERE ph.price > 0
    AND p.name_en IS NOT NULL
    AND p.name_en != ''
ORDER BY ph.CDate DESC
LIMIT 10;
```

---

## 🎯 **Query 3: Invoice Data Sample**

```sql
-- Check invoice structure and user data
SELECT 
    i.id as invoice_id,
    i.user_id,
    i.status,
    i.subtotal,
    i.delivery,
    i.tax,
    i.pay as total_amount,
    i.CDate as invoice_date,
    i.source,
    i.paymentStatus,
    i.deliveryStatus
FROM invoice i
WHERE i.CDate >= DATE_SUB(NOW(), INTERVAL 30 DAY)
    AND i.user_id IS NOT NULL
ORDER BY i.CDate DESC
LIMIT 10;
```

---

## 🎯 **Query 4: Invoice Items Sample (FAST VERSION)**

```sql
-- Check basic invoice items data (simplified for speed)
SELECT 
    ii.id as item_id,
    ii.invoice_id,
    ii.sku_id,
    ii.price as item_price,
    ii.cost as item_cost,
    ii.old_price,
    ii.tax as item_tax
FROM invoiceItem ii
WHERE ii.price > 0
ORDER BY ii.id DESC
LIMIT 15;
```

---

## 🎯 **Query 4B: Test Invoice-SKU Relationship (ULTRA FAST)**

```sql
-- Ultra simple test - just get recent invoice items
SELECT 
    ii.sku_id,
    ii.price
FROM invoiceItem ii
WHERE ii.price > 0
ORDER BY ii.id DESC
LIMIT 20;
```

---

## 🎯 **Query 5: Check Product Attributes Coverage**

```sql
-- See which products have attributes assigned
SELECT 
    COUNT(DISTINCT pav.product_id) as products_with_attributes,
    COUNT(DISTINCT p.id) as total_products,
    ROUND((COUNT(DISTINCT pav.product_id) / COUNT(DISTINCT p.id)) * 100, 2) as coverage_percentage,
    COUNT(pav.product_id) as total_attribute_assignments
FROM product p
LEFT JOIN product_attributevalue pav ON p.id = pav.product_id
WHERE p.is_deleted = 0
    AND p.name_en IS NOT NULL
    AND p.name_en != '';
```

---

## 🎯 **Query 6: Check Pricing Coverage**

```sql
-- See which products have pricing data
SELECT 
    COUNT(DISTINCT CASE WHEN ph.sku_id IS NOT NULL THEN s.product_id END) as products_with_pricing,
    COUNT(DISTINCT p.id) as total_products,
    ROUND((COUNT(DISTINCT CASE WHEN ph.sku_id IS NOT NULL THEN s.product_id END) / COUNT(DISTINCT p.id)) * 100, 2) as pricing_coverage_percentage
FROM product p
LEFT JOIN sku s ON p.sku_id = s.id AND s.is_deleted = 0
LEFT JOIN priceHistory ph ON s.id = ph.sku_id AND ph.price > 0
WHERE p.is_deleted = 0
    AND p.name_en IS NOT NULL
    AND p.name_en != '';
```

---

## 🎯 **Query 7: Check Current Pricing Table Sample**

```sql
-- Check current pricing table as alternative to priceHistory
SELECT 
    pr.id as pricing_id,
    pr.sku_id,
    pr.quantity as base_price,
    pr.discount as discount_percentage,
    CASE 
        WHEN pr.discount > 0 THEN ROUND(pr.quantity * (100 - pr.discount) / 100, 2)
        ELSE pr.quantity
    END as final_price,
    pr.CDate as pricing_date,
    s.product_id,
    s.name_en as sku_name,
    s.code as sku_code,
    p.name_en as product_name
FROM pricing pr
JOIN sku s ON pr.sku_id = s.id AND s.is_deleted = 0
JOIN product p ON s.product_id = p.id AND p.is_deleted = 0
WHERE pr.is_deleted = 0
    AND pr.quantity > 0
    AND p.name_en IS NOT NULL
    AND p.name_en != ''
ORDER BY pr.CDate DESC
LIMIT 10;
```

---

## 🎯 **Query 8: Check Recent Purchase Activity (FAST VERSION)**

```sql
-- Simple recent invoice count (no JOINs)
SELECT 
    DATE(i.CDate) as purchase_date,
    COUNT(*) as invoices_count
FROM invoice i
WHERE i.CDate >= DATE_SUB(NOW(), INTERVAL 7 DAY)
    AND i.user_id IS NOT NULL
GROUP BY DATE(i.CDate)
ORDER BY purchase_date DESC;
```

---

## 🎯 **Query 9: Check SKU Country Pricing Table Sample**

```sql
-- Check sku_country table for better pricing data
SELECT 
    sc.id as pricing_id,
    sc.sku_id,
    sc.country_id,
    sc.price,
    sc.old_price,
    sc.is_disabled,
    sc.score,
    sc.assembly_price,
    sc.CDate as pricing_date,
    s.product_id,
    s.name_en as sku_name,
    s.code as sku_code,
    p.name_en as product_name
FROM sku_country sc
JOIN sku s ON sc.sku_id = s.id AND s.is_deleted = 0
JOIN product p ON s.product_id = p.id AND p.is_deleted = 0
WHERE sc.is_disabled = 0
    AND sc.price > 0
    AND p.name_en IS NOT NULL
    AND p.name_en != ''
ORDER BY sc.CDate DESC
LIMIT 15;
```

---

## 🔍 **What I'm Looking For:**

### **Product Attributes:**
- How many products have attributes assigned?
- What attribute types are most common (Gender, Age, Size)?
- Data quality of attribute values

### **Pricing Data:**
- Current vs old pricing structure
- Price history frequency (daily, weekly?)
- Currency handling (all SAR?)

### **Invoice Data:**
- Recent purchase activity levels
- User ID format and validity
- Invoice status meanings

### **Invoice Items:**
- Product quantity per purchase
- Price vs cost differences
- SKU to product mapping accuracy

---

## 📋 **Key Questions:**

1. **Do most products have attributes?** (Gender, Age, Size coverage)
2. **Is pricing data recent and complete?** (Last 30 days activity)
3. **Are there enough purchase events?** (For GCP model training)
4. **Data quality issues?** (NULL values, missing relationships)

---

> **Run these 6 queries and share the results** - this will help me verify the data quality and adjust the final extraction queries accordingly!