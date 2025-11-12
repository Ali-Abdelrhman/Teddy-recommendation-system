#!/usr/bin/env python3
"""
FINAL: Convert complete database CSV to Google Cloud Retail API catalog
This version uses REAL pricing data and proper database structure
"""

import pandas as pd
import json
import re
import random

def clean_text(text):
    """Clean and sanitize text fields"""
    if pd.isna(text) or text == '':
        return ""
    return str(text).strip()

def create_product_id(sku_id):
    """Create a product ID that matches user events format"""
    return f"PROD{sku_id:06d}"

def extract_smart_color(description, title):
    """Extract color from product description intelligently"""
    if not description and not title:
        return "Multi-Color"
    
    text = f"{description} {title}".lower()
    
    # Enhanced color detection
    color_patterns = {
        'Red': ['red', 'crimson', 'cherry', 'burgundy', 'scarlet', 'maroon'],
        'Blue': ['blue', 'navy', 'azure', 'cyan', 'cobalt', 'sapphire'],
        'Green': ['green', 'emerald', 'lime', 'forest', 'olive', 'mint'],
        'Yellow': ['yellow', 'gold', 'golden', 'amber', 'lemon', 'sunny'],
        'Pink': ['pink', 'rose', 'magenta', 'fuchsia', 'blush', 'coral'],
        'Orange': ['orange', 'tangerine', 'peach', 'apricot'],
        'Purple': ['purple', 'violet', 'lavender', 'plum', 'indigo'],
        'Black': ['black', 'charcoal', 'ebony', 'midnight'],
        'White': ['white', 'ivory', 'pearl', 'snow', 'cream'],
        'Brown': ['brown', 'chocolate', 'coffee', 'tan', 'bronze'],
        'Gray': ['gray', 'grey', 'silver', 'slate', 'pewter'],
        'Multi-Color': ['multicolor', 'multi-color', 'rainbow', 'colorful', 'assorted', 'various', 'mixed']
    }
    
    # Check for color keywords
    for color, keywords in color_patterns.items():
        if any(keyword in text for keyword in keywords):
            return color
    
    # Color-specific product types
    if any(word in text for word in ['butterfly', 'flower', 'nature']):
        return 'Multi-Color'
    elif any(word in text for word in ['metal', 'steel', 'chrome']):
        return 'Silver'
    elif any(word in text for word in ['wood', 'wooden']):
        return 'Brown'
    
    return "Multi-Color"

def determine_product_type(external_type, is_customizable, is_digital, has_variants):
    """Determine product type from database fields"""
    
    # Use external type if meaningful
    if external_type and str(external_type).strip() and str(external_type).strip() != 'null':
        ext_type = str(external_type).strip()
        if ext_type.lower() in ['onecard']:
            return "PRIMARY"
        elif ext_type.lower() in ['doll', 'variant']:
            return "VARIANT"
    
    # Use flags
    if is_digital == 1:
        return "PRIMARY"
    elif is_customizable == 1:
        return "VARIANT"
    elif has_variants:
        return "PRIMARY"
    else:
        return "PRIMARY"

def create_enhanced_categories(category_en, category_ar, subcategory_id):
    """Create categories using actual database categories"""
    categories = []
    
    # Primary category
    if category_en and str(category_en).strip():
        categories.append(str(category_en).strip())
    elif category_ar and str(category_ar).strip():
        categories.append(str(category_ar).strip())
    
    # Add subcategory reference if available
    if categories and not pd.isna(subcategory_id):
        categories.append(f"Sub_{int(subcategory_id)}")
    
    return categories

def create_comprehensive_attributes(row):
    """Create attributes from all available database fields"""
    attributes = {}
    
    # Brand
    brand = clean_text(row.get('brand_name_en')) or clean_text(row.get('brand_name_ar'))
    if brand:
        attributes['brand'] = {"text": [brand]}
    
    # Smart color extraction
    color = extract_smart_color(
        clean_text(row.get('description_en')), 
        clean_text(row.get('name_en'))
    )
    attributes['color'] = {"text": [color]}
    
    # Product features from database flags
    features = []
    if not pd.isna(row.get('is_international')) and int(row.get('is_international', 0)) == 1:
        features.append("International")
    if not pd.isna(row.get('is_digital')) and int(row.get('is_digital', 0)) == 1:
        features.append("Digital")
    if not pd.isna(row.get('is_customizable')) and int(row.get('is_customizable', 0)) == 1:
        features.append("Customizable")
    if not pd.isna(row.get('is_wrappable')) and int(row.get('is_wrappable', 0)) == 1:
        features.append("Gift-Wrappable")
    
    if features:
        attributes['features'] = {"text": features}
    
    # Physical dimensions
    dimensions = []
    for field, name in [('height', 'Height'), ('length', 'Length'), ('width', 'Width'), ('weight', 'Weight')]:
        if not pd.isna(row.get(field)) and float(row.get(field, 0)) > 0:
            dimensions.append(f"{name}: {row[field]}")
    
    if dimensions:
        attributes['dimensions'] = {"text": dimensions}
    
    # Origin country
    origin = clean_text(row.get('origincountry'))
    if origin:
        attributes['origin'] = {"text": [origin]}
    
    # Age group extraction
    description = clean_text(row.get('description_en', ''))
    if description:
        age_match = re.search(r'(\d+)\s*(?:years?|months?)\s*(?:and\s*)?(?:above|up|over|\+)', description, re.IGNORECASE)
        if age_match:
            age_val = int(age_match.group(1))
            if "month" in age_match.group(0).lower():
                if age_val >= 12:
                    attributes['age_group'] = {"text": [f"{age_val//12}+ years"]}
                else:
                    attributes['age_group'] = {"text": [f"{age_val}+ months"]}
            else:
                attributes['age_group'] = {"text": [f"{age_val}+ years"]}
    
    return attributes

def convert_complete_csv_to_catalog(csv_file_path, output_file_path):
    """Convert complete database CSV to Google Cloud catalog"""
    
    print(f"📖 Reading complete database CSV: {csv_file_path}")
    df = pd.read_csv(csv_file_path)
    
    print(f"🔄 Processing {len(df)} products with complete database data...")
    
    products = []
    pricing_stats = []
    categories_stats = {}
    colors_stats = {}
    
    for index, row in df.iterrows():
        # Skip deleted products
        if not pd.isna(row.get('is_deleted')) and int(row.get('is_deleted', 0)) == 1:
            continue
            
        # Create product ID
        product_id = create_product_id(row['sku_id'])
        
        # Get real categories from database
        categories = create_enhanced_categories(
            row.get('category_name_en'),
            row.get('category_name_ar'), 
            row.get('subcategory_id')
        )
        
        # Get real pricing from database
        current_price = row.get('current_price')
        original_price = row.get('original_price')
        
        if pd.isna(current_price) or current_price <= 0:
            current_price = 25.0  # Minimal fallback
        else:
            current_price = float(current_price)
            pricing_stats.append(current_price)
        
        if pd.isna(original_price) or original_price <= 0:
            original_price = current_price * 1.2  # 20% markup as fallback
        else:
            original_price = float(original_price)
        
        # Determine product type
        has_variants = bool(clean_text(row.get('sku_code')))
        product_type = determine_product_type(
            row.get('external_product_type'),
            row.get('is_customizable', 0),
            row.get('is_digital', 0),
            has_variants
        )
        
        # Create comprehensive product
        product = {
            "id": product_id,
            "primaryProductId": product_id,
            "type": product_type,
            "title": clean_text(row.get('name_en')) or clean_text(row.get('name_ar')) or f"Product {row['sku_id']}",
            "availability": "IN_STOCK"
        }
        
        # Add description
        desc = clean_text(row.get('description_en')) or clean_text(row.get('description_ar'))
        if desc:
            product["description"] = desc
        
        # Add categories
        if categories:
            product["categories"] = categories
            for cat in categories:
                categories_stats[cat] = categories_stats.get(cat, 0) + 1
        
        # Add real pricing
        product["priceInfo"] = {
            "currency": "SAR",
            "price": current_price,
            "originalPrice": original_price
        }
        
        # Add brand
        brand = clean_text(row.get('brand_name_en')) or clean_text(row.get('brand_name_ar'))
        if brand:
            product["brands"] = [brand]
        
        # Add UPC
        upc = clean_text(str(row.get('upc', '')))
        if upc and upc != 'nan':
            product["gtin"] = upc
        
        # Add slug-based URI
        slug = clean_text(row.get('slug'))
        if slug:
            product["uri"] = f"https://dabdoob.com/products/{slug}"
        
        # Add comprehensive attributes
        attributes = create_comprehensive_attributes(row)
        if attributes:
            product["attributes"] = attributes
            
            # Track color stats
            if 'color' in attributes:
                color = attributes['color']['text'][0]
                colors_stats[color] = colors_stats.get(color, 0) + 1
        
        # Add variants
        sku_code = clean_text(row.get('sku_code'))
        if sku_code:
            variant = {
                "id": f"{product_id}_variant",
                "sku": sku_code
            }
            
            # Add variant attributes
            variant_attrs = {}
            if 'color' in attributes:
                variant_attrs['color'] = attributes['color']
            
            if variant_attrs:
                variant["attributes"] = variant_attrs
            
            product["variants"] = [variant]
        
        products.append(product)
        
        if (index + 1) % 1000 == 0:
            print(f"📦 Processed {index + 1} products...")
    
    # Write final catalog
    print(f"💾 Writing {len(products)} complete products to: {output_file_path}")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for product in products:
            f.write(json.dumps(product, ensure_ascii=False) + '\n')
    
    # Statistics
    print(f"\n✅ COMPLETE catalog created with REAL database data!")
    print(f"📊 Final Statistics:")
    print(f"  📦 Total products: {len(products)}")
    print(f"  💰 Products with pricing: {len(pricing_stats)}")
    if pricing_stats:
        print(f"  💰 Price range: {min(pricing_stats):.2f} - {max(pricing_stats):.2f} SAR")
        print(f"  💰 Average price: {sum(pricing_stats)/len(pricing_stats):.2f} SAR")
    print(f"  🏷️  Categories: {len(categories_stats)} unique")
    print(f"  🎨 Colors: {len(colors_stats)} unique")
    
    # Top categories
    if categories_stats:
        print(f"\n🏆 Top Categories:")
        sorted_cats = sorted(categories_stats.items(), key=lambda x: x[1], reverse=True)[:10]
        for cat, count in sorted_cats:
            print(f"    {cat}: {count} products")
    
    # Top colors  
    if colors_stats:
        print(f"\n🌈 Color Distribution:")
        sorted_colors = sorted(colors_stats.items(), key=lambda x: x[1], reverse=True)[:10]
        for color, count in sorted_colors:
            print(f"    {color}: {count} products")
    
    return len(products)

def main():
    """Main execution"""
    print("🎯 FINAL Complete Database Catalog Converter")
    print("=" * 60)
    
    # This will be the CSV from your database query
    csv_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\SampleDBUserData\sample\Final products.csv"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\product_catalog_final.ndjson"
    
    print(f"📋 Expected Input: Complete database CSV with:")
    print(f"  💰 Real pricing from sku_country table")
    print(f"  🏷️  Categories from category table")
    print(f"  🏢 Brands from brand table")
    print(f"  📦 Complete SKU metadata")
    
    print(f"\n⚠️  Please:")
    print(f"1. Run the final_complete_extraction_query.sql in your database")
    print(f"2. Export results as CSV to: {csv_file}")
    print(f"3. Then run this script again")
    
    try:
        if pd.io.common.file_exists(csv_file):
            product_count = convert_complete_csv_to_catalog(csv_file, output_file)
            print(f"\n🎉 SUCCESS: Final catalog with {product_count} products!")
            print(f"📁 Output: {output_file}")
            print(f"\n🚀 Ready for Google Cloud upload!")
        else:
            print(f"\n📄 Waiting for database CSV: {csv_file}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()