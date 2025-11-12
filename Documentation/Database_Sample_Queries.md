# 📋 **Database Sample Data Queries**

> **Purpose**: Extract sample data from key Dabdoob tables to understand data structure for GCP Retail API integration

---

## 🎯 **Query 1: Product Table Sample Data**

```sql
-- Get 10 sample products with complete English data
SELECT 
    id,
    sku_id,
    name_en,
    name_ar,
    description_en,
    description_ar,
    nutrition_en,
    nutrition_ar,
    subcategory_id,
    brand_id,
    is_wrappable,
    is_deleted,
    upc,
    skucount,
    origincountry,
    allergicnote_ar,
    allergicnote_en,
    is_shortdistance,
    is_customizable,
    slug,
    howtouse_ar,
    howtouse_en,
    is_international,
    disable_cash,
    is_digital
FROM product 
WHERE is_deleted = 0 
    AND name_en IS NOT NULL 
    AND name_en != '' 
    AND description_en IS NOT NULL 
    AND description_en != ''
    AND brand_id IS NOT NULL
    AND subcategory_id IS NOT NULL
ORDER BY id 
LIMIT 10;
```

---

## 🎯 **Query 2: Brand Table Sample Data**

```sql
-- Get 10 sample brands with complete English data
SELECT 
    id,
    name_en,
    name_ar,
    information_en,
    information_ar,
    is_deleted,
    displayorder,
    slug,
    origincountry,
    title_en,
    title_ar,
    description_en,
    description_ar,
    note_en,
    note_ar,
    brand_type_id
FROM brand 
WHERE is_deleted = 0 
    AND name_en IS NOT NULL 
    AND name_en != ''
ORDER BY id 
LIMIT 10;
```

---

## 🎯 **Query 3: Category Table Sample Data**

```sql
-- Get 10 sample categories with complete English data
SELECT 
    id,
    name_en,
    name_ar,
    color,
    displayorder,
    is_deleted,
    text_color,
    slug,
    is_hidden
FROM category 
WHERE is_deleted = 0 
    AND is_hidden = 0
    AND name_en IS NOT NULL 
    AND name_en != ''
ORDER BY displayorder 
LIMIT 10;
```

---

## 🎯 **Query 4: SKU Table Sample Data**

```sql
-- Get 10 sample SKUs with complete data linked to valid products
SELECT 
    id,
    product_id,
    name_en,
    name_ar,
    code,
    color,
    `limit`,
    is_deleted,
    item_number,
    upc,
    height,
    length,
    weight,
    width,
    box_count,
    box_name_ar,
    box_name_en,
    ref_sku_id,
    allergicnote_ar,
    allergicnote_en,
    ingredient_ar,
    ingredient_en,
    slug,
    minorder,
    unit,
    external_product_type,
    external_product_id,
    assembly_enabled,
    assembly_provider
FROM sku 
WHERE is_deleted = 0 
    AND product_id IS NOT NULL
    AND name_en IS NOT NULL 
    AND name_en != ''
ORDER BY id 
LIMIT 10;
```

---

## 🎯 **Query 5: Attribute Table Sample Data**

```sql
-- Get 10 sample attributes with complete English data
SELECT 
    id,
    name_en,
    name_ar,
    appFilterOp,
    appFilterItemsOp,
    secondary_id,
    is_deleted,
    target,
    slug,
    type,
    options
FROM attribute 
WHERE is_deleted = 0 
    AND name_en IS NOT NULL 
    AND name_en != ''
ORDER BY id 
LIMIT 10;
```

---

## 🎯 **Query 6: Attribute Value Table Sample Data**

```sql
-- Get 10 sample attribute values with complete English data
SELECT 
    id,
    attribute_id,
    name_en,
    name_ar,
    color,
    is_deleted,
    icon,
    slug
FROM attributevalue 
WHERE is_deleted = 0 
    AND name_en IS NOT NULL 
    AND name_en != ''
    AND attribute_id IS NOT NULL
ORDER BY id 
LIMIT 10;
```

---

## 🎯 **Query 7: Media Table Sample Data**

```sql
-- Get 10 sample media records for products with valid targets
SELECT 
    id,
    storage,
    type,
    path,
    target,
    target_id,
    image_order,
    resize,
    is_deleted,
    blurhash,
    format,
    height,
    metadata,
    size,
    width,
    skip_for_metadata,
    blur_data_url
FROM media 
WHERE is_deleted = 0 
    AND target IS NOT NULL
    AND target_id IS NOT NULL
    AND path IS NOT NULL
    AND path != ''
    AND type = 'image'
ORDER BY id 
LIMIT 10;
```

---

## 🔍 **Key Insights Needed:**

### **For Product Mapping:**
- How `subcategory_id` and `brand_id` link to actual names
- What values are in `origincountry`, `allergicnote_en/ar`
- How `sku_id` relates to the SKU table

### **For Category Hierarchy:**
- How to build hierarchical categories (parent-child relationships)
- What `displayorder` indicates for sorting

### **For SKU Variants:**
- How `product_id` links to products
- What `color`, `code`, and `item_number` contain
- How pricing is handled (not visible in SKU table)

### **For Attributes:**
- How `attribute_id` links attribute to attributevalue
- What `target` field indicates (product, sku, etc.)
- Format of `options` JSON field

### **For Media:**
- How `target` and `target_id` link to products/SKUs
- What `type` values exist (image, video, etc.)
- How to construct full image URLs from `path`

---

## 📋 **Next Steps:**

1. **Run all filtered queries** and export results
2. **Analyze data patterns** and relationships  
3. **Build GCP extraction queries** based on findings
4. **Map real data** to GCP Retail API format
5. **Test data extraction** with small sample first

---

## 🎯 **Filtering Strategy Applied:**

### **✅ Quality Filters Added:**
- **English names required**: `name_en IS NOT NULL AND name_en != ''`
- **Complete descriptions**: Products must have descriptions
- **Valid relationships**: Foreign keys must not be NULL
- **Active records only**: `is_deleted = 0` and `is_hidden = 0`
- **Image filtering**: Only actual image files with valid paths

### **🔍 Data Completeness Focus:**
- Products with both `brand_id` and `subcategory_id`
- SKUs linked to valid `product_id`
- Attributes with proper `attribute_id` links
- Media records with valid `target` and `target_id`

> **Note**: These filtered queries will give us high-quality sample data with complete English names and all required relationships for building the GCP Retail API format mapping.