#!/usr/bin/env python3
"""
Real Category-Based Catalog Generator for Dabdoob
Converts real database category hierarchy to GCP Retail API format
"""
import pandas as pd
import json
import re
from datetime import datetime
import os

def clean_text(text):
    """Clean and sanitize text fields"""
    if pd.isna(text) or text == '':
        return ""
    return str(text).strip()

def create_product_id(sku_id):
    """Create a product ID that matches user events format"""
    if pd.isna(sku_id):
        return "PROD000000"
    return f"PROD{int(sku_id):06d}"

def parse_real_categories(main_category, subcategory):
    """Create categories from real database hierarchy"""
    categories = []
    
    # Add main category
    main_cat = clean_text(main_category)
    if main_cat:
        categories.append(main_cat)
    
    # Add subcategory
    sub_cat = clean_text(subcategory)
    if sub_cat and sub_cat != main_cat:
        categories.append(sub_cat)
    
    return categories

def create_real_attributes(row):
    """Create attributes from real database fields"""
    attributes = {}
    
    # Brand from database
    brand_name = clean_text(row.get('brand_name'))
    if brand_name:
        attributes['brand'] = {"text": [brand_name]}
    
    # Gift wrappable from database
    if not pd.isna(row.get('is_wrappable')) and int(row.get('is_wrappable', 0)) == 1:
        attributes['features'] = {"text": ["Gift-Wrappable"]}
    
    # International product flag
    if not pd.isna(row.get('is_international')) and int(row.get('is_international', 0)) == 1:
        if 'features' in attributes:
            attributes['features']['text'].append("International")
        else:
            attributes['features'] = {"text": ["International"]}
    
    # Customizable flag
    if not pd.isna(row.get('is_customizable')) and int(row.get('is_customizable', 0)) == 1:
        if 'features' in attributes:
            attributes['features']['text'].append("Customizable")
        else:
            attributes['features'] = {"text": ["Customizable"]}
    
    # Origin country
    origin_country = clean_text(row.get('origincountry'))
    if origin_country:
        attributes['origin_country'] = {"text": [origin_country]}
    
    # Extract color from product name or description (basic extraction)
    color = extract_color_from_text(
        clean_text(row.get('title', '')),
        clean_text(row.get('description', ''))
    )
    attributes['color'] = {"text": [color]}
    
    return attributes

def extract_color_from_text(title, description):
    """Extract color information from product text"""
    text = f"{title} {description}".lower()
    
    # Common color keywords
    colors = {
        'red': ['red', 'crimson', 'scarlet'],
        'blue': ['blue', 'navy', 'azure', 'cyan'],
        'green': ['green', 'emerald', 'lime'],
        'yellow': ['yellow', 'gold', 'golden'],
        'black': ['black', 'dark'],
        'white': ['white', 'cream'],
        'pink': ['pink', 'rose'],
        'purple': ['purple', 'violet'],
        'orange': ['orange', 'amber'],
        'brown': ['brown', 'chocolate'],
        'grey': ['grey', 'gray', 'silver'],
        'multi-color': ['multi', 'colorful', 'rainbow', 'mixed', 'assorted']
    }
    
    for color, keywords in colors.items():
        for keyword in keywords:
            if keyword in text:
                return color.title().replace('-', '-')
    
    return "Multi-Color"  # Default

def convert_real_catalog_to_ndjson(csv_file_path, output_file_path):
    """Convert real database catalog to GCP Retail API NDJSON format"""
    
    if not os.path.exists(csv_file_path):
        print(f"❌ Error: CSV file not found: {csv_file_path}")
        print(f"📋 Please run the SQL query first and export results to CSV")
        return 0
    
    # Read the real database data
    print(f"📊 Reading real category data from: {csv_file_path}")
    df = pd.read_csv(csv_file_path)
    print(f"🔄 Processing {len(df)} products with real categories...")
    
    products = []
    category_stats = {}
    brand_stats = {}
    pricing_stats = []
    
    for index, row in df.iterrows():
        # Create product ID
        product_id = create_product_id(row.get('sku_id'))
        
        # Basic product information
        title = clean_text(row.get('title'))
        description = clean_text(row.get('description'))
        
        if not title:
            continue  # Skip products without names
        
        # Real categories from database
        categories = parse_real_categories(
            row.get('main_category'),
            row.get('subcategory')
        )
        
        # Track category usage
        if categories:
            main_cat = categories[0]
            category_stats[main_cat] = category_stats.get(main_cat, 0) + 1
        
        # Brand from database
        brands = []
        brand_name = clean_text(row.get('brand_name'))
        if brand_name:
            brands.append(brand_name)
            brand_stats[brand_name] = brand_stats.get(brand_name, 0) + 1
        
        # Real pricing from database
        current_price = row.get('current_price')
        original_price = row.get('original_price')
        currency_code = row.get('currency_code', 'SAR')
        
        if pd.isna(current_price) or current_price <= 0:
            current_price = 25.0  # Minimal fallback
        else:
            current_price = float(current_price)
            pricing_stats.append(current_price)
        
        if pd.isna(original_price) or original_price <= current_price:
            original_price = current_price * 1.2  # 20% discount
        else:
            original_price = float(original_price)
        
        # Availability from database
        availability = clean_text(row.get('availability', 'IN_STOCK'))
        
        # Product URL
        product_url = clean_text(row.get('product_url', ''))
        if not product_url:
            product_url = f"https://dabdoob.com/products/{product_id.lower()}"
        
        # Real attributes from database
        attributes = create_real_attributes(row)
        
        # Create the product object
        product = {
            "id": product_id,
            "title": title,
            "availability": availability,
            "description": description,
            "categories": categories,
            "priceInfo": {
                "price": current_price,
                "originalPrice": original_price,
                "currencyCode": currency_code
            },
            "brands": brands,
            "uri": product_url,
            "attributes": attributes
        }
        
        products.append(product)
    
    # Write NDJSON file
    print(f"💾 Writing {len(products)} products to: {output_file_path}")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for product in products:
            f.write(json.dumps(product, ensure_ascii=False) + '\n')
    
    # Print statistics
    print(f"\n📈 REAL DATABASE CATALOG STATISTICS")
    print(f"=" * 50)
    print(f"✅ Total Products: {len(products):,}")
    print(f"🏷️  Categories: {len(category_stats)}")
    print(f"🏢 Brands: {len(brand_stats)}")
    
    if pricing_stats:
        print(f"💰 Price Range: {min(pricing_stats):.2f} - {max(pricing_stats):.2f} SAR")
        print(f"💰 Average Price: {sum(pricing_stats)/len(pricing_stats):.2f} SAR")
    
    print(f"\n🏆 TOP CATEGORIES:")
    for cat, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  📂 {cat}: {count:,} products")
    
    print(f"\n🏆 TOP BRANDS:")
    for brand, count in sorted(brand_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  🏢 {brand}: {count:,} products")
    
    return len(products)

def create_categories_ndjson(csv_file_path, categories_output_path):
    """Create categories.ndjson from real database data"""
    
    if not os.path.exists(csv_file_path):
        print(f"❌ Categories CSV not found: {csv_file_path}")
        return 0
    
    print(f"📂 Creating categories from: {csv_file_path}")
    df = pd.read_csv(csv_file_path)
    
    categories = []
    for index, row in df.iterrows():
        category_id = str(row.get('id', ''))
        display_name = clean_text(row.get('displayName', ''))
        hierarchy_str = clean_text(row.get('categoryHierarchy', ''))
        
        if category_id and display_name:
            try:
                # Parse the hierarchy string
                hierarchy = json.loads(hierarchy_str)
                category = {
                    "id": category_id,
                    "displayName": display_name,
                    "categoryHierarchy": hierarchy
                }
                categories.append(category)
            except:
                # Fallback for malformed hierarchy
                category = {
                    "id": category_id,
                    "displayName": display_name,
                    "categoryHierarchy": [display_name]
                }
                categories.append(category)
    
    # Write categories NDJSON
    with open(categories_output_path, 'w', encoding='utf-8') as f:
        for category in categories:
            f.write(json.dumps(category, ensure_ascii=False) + '\n')
    
    print(f"✅ Created {len(categories)} categories in: {categories_output_path}")
    return len(categories)

def main():
    """Main execution"""
    print("🎯 REAL DABDOOB CATEGORY-BASED CATALOG GENERATOR")
    print("=" * 60)
    
    # File paths
    base_path = r"c:\Users\Ahmed\Downloads\Teddy recommendation system"
    products_csv = os.path.join(base_path, "extracted_real_products_with_categories.csv")
    categories_csv = os.path.join(base_path, "extracted_real_categories.csv")
    
    products_output = os.path.join(base_path, "Recommendation Engine Demo", "product_catalog_real_categories.ndjson")
    categories_output = os.path.join(base_path, "Recommendation Engine Demo", "categories_real.ndjson")
    
    print(f"📋 INSTRUCTIONS:")
    print(f"1. Run the SQL queries from 'extract_real_categories_hierarchy.sql'")
    print(f"2. Export Query 7 results to: {products_csv}")
    print(f"3. Export Query 10 results to: {categories_csv}")
    print(f"4. Then run this script")
    
    if os.path.exists(products_csv):
        # Generate product catalog
        product_count = convert_real_catalog_to_ndjson(products_csv, products_output)
        
        # Generate categories
        if os.path.exists(categories_csv):
            category_count = create_categories_ndjson(categories_csv, categories_output)
            print(f"\n🎉 SUCCESS! Generated:")
            print(f"  📦 {product_count:,} products with real categories")
            print(f"  📂 {category_count} category definitions")
        else:
            print(f"\n⚠️  Categories CSV not found. Only products generated.")
            print(f"📂 Please export Query 10 results to: {categories_csv}")
    else:
        print(f"\n⚠️  Products CSV not found.")
        print(f"📦 Please export Query 7 results to: {products_csv}")

if __name__ == "__main__":
    main()