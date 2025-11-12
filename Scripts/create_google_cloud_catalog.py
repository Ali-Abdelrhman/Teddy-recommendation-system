#!/usr/bin/env python3
"""
Convert CSV product data to Google Cloud Retail API catalog format
This script converts the extracted database products into NDJSON format
compatible with Google Cloud Retail API product catalog imports.
"""

import pandas as pd
import json
import re
from urllib.parse import quote

def clean_text(text):
    """Clean and sanitize text fields"""
    if pd.isna(text) or text == '':
        return ""
    return str(text).strip()

def create_product_id(sku_id):
    """Create a product ID that matches user events format"""
    return f"PROD{sku_id:06d}"

def create_categories(category_name_en, subcategory_id):
    """Create categories hierarchy"""
    categories = []
    
    # Clean category name
    category_clean = clean_text(category_name_en)
    if category_clean:
        categories.append(category_clean)
        
        # Add subcategory if available
        if not pd.isna(subcategory_id) and str(subcategory_id).strip():
            categories.append(f"Sub_{subcategory_id}")
    
    return categories

def create_attributes(row):
    """Create product attributes from available data"""
    attributes = {}
    
    # Brand information
    brand_name = clean_text(row['brand_name_en'])
    if brand_name:
        attributes['brand'] = {
            "text": [brand_name]
        }
    
    # Color information
    color = clean_text(row['sku_color'])
    if color and color != '#000000':
        attributes['color'] = {
            "text": [color]
        }
    
    # Origin country
    origin = clean_text(row['origincountry'])
    if origin:
        attributes['origin_country'] = {
            "text": [origin]
        }
    
    # Product type flags
    if not pd.isna(row['is_international']) and row['is_international'] == 1:
        attributes['product_type'] = {
            "text": ["International"]
        }
    elif not pd.isna(row['is_digital']) and row['is_digital'] == 1:
        attributes['product_type'] = {
            "text": ["Digital"]
        }
    
    # Age group (extracted from description)
    description = clean_text(row['description_en'])
    if description:
        age_match = re.search(r'(\d+)\s*(?:years?|months?)\s*(?:and\s*)?(?:above|up|over|\+)', description, re.IGNORECASE)
        if age_match:
            attributes['age_group'] = {
                "text": [f"{age_match.group(1)}+ years"]
            }
    
    return attributes

def convert_csv_to_google_catalog(csv_file_path, output_file_path):
    """Convert CSV product data to Google Cloud Retail API catalog format"""
    
    print(f"Reading CSV file: {csv_file_path}")
    df = pd.read_csv(csv_file_path)
    
    print(f"Processing {len(df)} products...")
    
    products = []
    
    for index, row in df.iterrows():
        # Skip deleted products
        if row.get('is_deleted', 0) == 1:
            continue
            
        # Create product ID matching user events format
        product_id = create_product_id(row['sku_id'])
        
        # Create basic product structure
        product = {
            "id": product_id,
            "primaryProductId": product_id,
            "type": "PRIMARY",
            "title": clean_text(row['name_en']) or f"Product {row['sku_id']}",
            "description": clean_text(row['description_en']),
            "categories": create_categories(row.get('category_name_en'), row.get('subcategory_id')),
            "availability": "IN_STOCK",
            "uri": f"https://dabdoob.com/products/{clean_text(row.get('slug', product_id.lower()))}",
            "attributes": create_attributes(row)
        }
        
        # Add pricing information (if available)
        # Note: Price data not in current CSV, using placeholder
        product["priceInfo"] = {
            "currency": "SAR",
            "price": 50.0,  # Placeholder price
            "originalPrice": 50.0
        }
        
        # Add brand information at product level
        brand_name = clean_text(row['brand_name_en'])
        if brand_name:
            product["brands"] = [brand_name]
        
        # Add UPC/barcode if available
        upc = clean_text(str(row['upc'])) if not pd.isna(row['upc']) else ""
        if upc and upc != 'nan':
            product["gtin"] = upc
        
        # Add product variants/SKU information
        sku_code = clean_text(row['sku_code'])
        if sku_code:
            variant_color = clean_text(row['sku_color']) if not pd.isna(row['sku_color']) else "Default"
            product["variants"] = [{
                "id": f"{product_id}_variant",
                "sku": sku_code,
                "attributes": {
                    "color": {
                        "text": [variant_color if variant_color else "Default"]
                    }
                }
            }]
        
        products.append(product)
        
        if (index + 1) % 1000 == 0:
            print(f"Processed {index + 1} products...")
    
    # Write to NDJSON format
    print(f"Writing {len(products)} products to: {output_file_path}")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for product in products:
            f.write(json.dumps(product, ensure_ascii=False) + '\n')
    
    print(f"✅ Successfully created Google Cloud catalog with {len(products)} products")
    
    # Create summary statistics
    summary = {
        "total_products": len(products),
        "products_with_brands": len([p for p in products if p.get('brands')]),
        "products_with_categories": len([p for p in products if p.get('categories')]),
        "products_with_descriptions": len([p for p in products if p.get('description')])
    }
    
    print("\n📊 Catalog Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    return summary

def main():
    """Main execution function"""
    csv_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\SampleDBUserData\Product_complete.csv"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\product_catalog_complete.ndjson"
    
    try:
        summary = convert_csv_to_google_catalog(csv_file, output_file)
        print(f"\n🎉 Conversion completed successfully!")
        print(f"📁 Output file: {output_file}")
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()