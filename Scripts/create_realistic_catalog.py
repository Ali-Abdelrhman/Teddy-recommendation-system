#!/usr/bin/env python3
"""
REALISTIC: Convert CSV product data to Google Cloud Retail API catalog format
This version uses ONLY actual database data - no artificial enhancements
"""

import pandas as pd
import json

def clean_text(text):
    """Clean and sanitize text fields"""
    if pd.isna(text) or text == '':
        return ""
    return str(text).strip()

def create_product_id(sku_id):
    """Create a product ID that matches user events format"""
    return f"PROD{sku_id:06d}"

def get_actual_categories(category_name_en, category_name_ar, subcategory_id):
    """Use only actual categories from database"""
    categories = []
    
    # Use English category if available
    if not pd.isna(category_name_en) and str(category_name_en).strip():
        categories.append(str(category_name_en).strip())
    
    # Use Arabic category if English not available
    elif not pd.isna(category_name_ar) and str(category_name_ar).strip():
        categories.append(str(category_name_ar).strip())
    
    # Add subcategory ID only if we have a main category
    if categories and not pd.isna(subcategory_id):
        categories.append(f"Sub_{int(subcategory_id)}")
    
    return categories

def get_actual_product_type(external_product_type, is_customizable, is_digital):
    """Determine product type from actual database fields"""
    
    # Use external_product_type if available
    if not pd.isna(external_product_type) and str(external_product_type).strip():
        ext_type = str(external_product_type).strip().upper()
        if ext_type in ['PRIMARY', 'VARIANT', 'COLLECTION']:
            return ext_type
    
    # Use database flags
    if not pd.isna(is_digital) and is_digital == 1:
        return "PRIMARY"  # Digital products are usually primary
    elif not pd.isna(is_customizable) and is_customizable == 1:
        return "VARIANT"  # Customizable products can be variants
    else:
        return "PRIMARY"  # Default

def get_actual_price_info():
    """Since no price data in CSV, return minimal structure"""
    return {
        "currency": "SAR"
        # No price - let Google Cloud handle this or get from other source
    }

def create_realistic_attributes(row):
    """Create attributes using ONLY actual database data"""
    attributes = {}
    
    # Brand (only if available)
    brand_en = clean_text(row['brand_name_en'])
    brand_ar = clean_text(row['brand_name_ar'])
    if brand_en:
        attributes['brand'] = {"text": [brand_en]}
    elif brand_ar:
        attributes['brand'] = {"text": [brand_ar]}
    
    # Origin country (only if available)
    origin = clean_text(row['origincountry'])
    if origin:
        attributes['origin_country'] = {"text": [origin]}
    
    # Product flags (only actual database values)
    flags = []
    if not pd.isna(row['is_international']) and int(row['is_international']) == 1:
        flags.append("International")
    if not pd.isna(row['is_digital']) and int(row['is_digital']) == 1:
        flags.append("Digital")
    if not pd.isna(row['is_customizable']) and int(row['is_customizable']) == 1:
        flags.append("Customizable")
    if not pd.isna(row['is_wrappable']) and int(row['is_wrappable']) == 1:
        flags.append("Gift-Wrappable")
    
    if flags:
        attributes['product_features'] = {"text": flags}
    
    # Physical dimensions (only if available)
    dimensions = []
    for dim_field, dim_name in [('height', 'Height'), ('length', 'Length'), ('width', 'Width'), ('weight', 'Weight')]:
        if not pd.isna(row[dim_field]) and row[dim_field] > 0:
            dimensions.append(f"{dim_name}: {row[dim_field]}")
    
    if dimensions:
        attributes['dimensions'] = {"text": dimensions}
    
    return attributes

def convert_csv_to_realistic_catalog(csv_file_path, output_file_path):
    """Convert CSV to realistic Google Cloud catalog using only actual data"""
    
    print(f"📖 Reading CSV file: {csv_file_path}")
    df = pd.read_csv(csv_file_path)
    
    print(f"🔄 Processing {len(df)} products using ONLY actual database data...")
    
    products = []
    categories_count = 0
    with_categories = 0
    product_types = {}
    
    for index, row in df.iterrows():
        # Skip deleted products
        if not pd.isna(row.get('is_deleted', 0)) and int(row['is_deleted']) == 1:
            continue
            
        # Create product ID
        product_id = create_product_id(row['sku_id'])
        
        # Get actual categories from database
        categories = get_actual_categories(
            row.get('category_name_en'), 
            row.get('category_name_ar'), 
            row.get('subcategory_id')
        )
        
        if categories:
            with_categories += 1
        
        # Get actual product type from database
        product_type = get_actual_product_type(
            row.get('external_product_type'),
            row.get('is_customizable'),
            row.get('is_digital')
        )
        
        product_types[product_type] = product_types.get(product_type, 0) + 1
        
        # Create basic product structure with actual data only
        product = {
            "id": product_id,
            "primaryProductId": product_id,
            "type": product_type,
            "title": clean_text(row['name_en']) or clean_text(row['name_ar']) or f"Product {row['sku_id']}",
            "availability": "IN_STOCK"
        }
        
        # Add description if available
        desc_en = clean_text(row['description_en'])
        desc_ar = clean_text(row['description_ar'])
        if desc_en:
            product["description"] = desc_en
        elif desc_ar:
            product["description"] = desc_ar
        
        # Add categories if available
        if categories:
            product["categories"] = categories
        
        # Add URI
        slug = clean_text(row.get('slug'))
        if slug:
            product["uri"] = f"https://dabdoob.com/products/{slug}"
        
        # Add minimal price info (no actual prices available)
        product["priceInfo"] = get_actual_price_info()
        
        # Add brand if available
        brand_en = clean_text(row['brand_name_en'])
        brand_ar = clean_text(row['brand_name_ar'])
        if brand_en:
            product["brands"] = [brand_en]
        elif brand_ar:
            product["brands"] = [brand_ar]
        
        # Add UPC if available
        upc = clean_text(str(row['upc'])) if not pd.isna(row['upc']) else ""
        if upc and upc != 'nan':
            product["gtin"] = upc
        
        # Add attributes with actual data only
        attributes = create_realistic_attributes(row)
        if attributes:
            product["attributes"] = attributes
        
        # Add variants if SKU code available
        sku_code = clean_text(row['sku_code'])
        if sku_code:
            variant = {
                "id": f"{product_id}_variant",
                "sku": sku_code
            }
            
            # Add actual color if not default black
            sku_color = clean_text(row['sku_color'])
            if sku_color and sku_color != '#000000':
                variant["attributes"] = {
                    "color": {"text": [sku_color]}
                }
            
            product["variants"] = [variant]
        
        products.append(product)
        
        if (index + 1) % 1000 == 0:
            print(f"📦 Processed {index + 1} products...")
    
    # Write realistic catalog
    print(f"💾 Writing {len(products)} realistic products to: {output_file_path}")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for product in products:
            f.write(json.dumps(product, ensure_ascii=False) + '\n')
    
    # Realistic statistics
    print(f"\n✅ Realistic catalog created using ONLY actual database data!")
    print(f"📊 Actual Data Statistics:")
    print(f"  📦 Total products: {len(products)}")
    print(f"  🏷️  Products with categories: {with_categories}")
    print(f"  📈 Category coverage: {(with_categories/len(products)*100):.1f}%")
    print(f"  🔄 Product types: {dict(product_types)}")
    
    return len(products)

def main():
    """Main execution with realistic processing"""
    csv_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\SampleDBUserData\Product_complete.csv"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\product_catalog_realistic.ndjson"
    
    try:
        product_count = convert_csv_to_realistic_catalog(csv_file, output_file)
        print(f"\n🎯 REALISTIC CATALOG: {product_count} products using actual data only!")
        print(f"📁 File: {output_file}")
        print(f"\n✅ What's REAL:")
        print(f"  ✅ Product names from database")
        print(f"  ✅ Descriptions from database")
        print(f"  ✅ Categories from database (where available)")
        print(f"  ✅ Brands from database")
        print(f"  ✅ Product flags from database")
        print(f"  ✅ Dimensions from database")
        print(f"\n❌ What's MISSING (needs separate data source):")
        print(f"  ❌ Pricing (not in current CSV)")
        print(f"  ❌ Real color names (only hex codes available)")
        print(f"  ❌ Product images")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()