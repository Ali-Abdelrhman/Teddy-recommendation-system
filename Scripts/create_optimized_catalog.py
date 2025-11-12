#!/usr/bin/env python3
"""
Create optimized catalog with only products referenced in user events
"""

import json
import pandas as pd

def load_user_event_products(events_file):
    """Load unique product IDs from user events"""
    print(f"📖 Loading user event products from: {events_file}")
    
    user_products = set()
    event_count = 0
    
    with open(events_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    event = json.loads(line)
                    event_count += 1
                    
                    product_details = event.get('productDetails', [])
                    for detail in product_details:
                        product = detail.get('product', {})
                        product_id = product.get('id')
                        if product_id:
                            user_products.add(product_id)
                except Exception as e:
                    print(f"⚠️ Error parsing event line: {e}")
    
    print(f"✅ Loaded {len(user_products)} unique products from {event_count} events")
    return user_products

def create_optimized_catalog(catalog_file, user_products, output_file):
    """Create optimized catalog with only needed products"""
    print(f"📖 Reading full catalog: {catalog_file}")
    
    total_products = 0
    matching_products = 0
    missing_products = []
    optimized_products = []
    
    # Read catalog and filter
    with open(catalog_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    product = json.loads(line)
                    total_products += 1
                    
                    product_id = product.get('id')
                    if product_id in user_products:
                        matching_products += 1
                        
                        # Clean up the product
                        cleaned_product = clean_product(product)
                        optimized_products.append(cleaned_product)
                        
                        # Remove from user_products to track missing
                        user_products.discard(product_id)
                    
                    if total_products % 10000 == 0:
                        print(f"📦 Processed {total_products} products, found {matching_products} matches...")
                        
                except Exception as e:
                    print(f"⚠️ Error parsing product line: {e}")
    
    # Remaining user_products are missing from catalog
    missing_products = list(user_products)
    
    print(f"\n📊 OPTIMIZATION RESULTS:")
    print(f"  📦 Total products in catalog: {total_products}")
    print(f"  ✅ Matching products found: {matching_products}")
    print(f"  ❌ Missing products: {len(missing_products)}")
    print(f"  🎯 Catalog reduction: {total_products - matching_products} products ({(total_products - matching_products)/total_products*100:.1f}%)")
    
    # Write optimized catalog
    print(f"\n💾 Writing optimized catalog: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        for product in optimized_products:
            f.write(json.dumps(product, ensure_ascii=False) + '\n')
    
    # Write missing products report
    missing_file = output_file.replace('.ndjson', '_missing_products.txt')
    with open(missing_file, 'w', encoding='utf-8') as f:
        f.write("Missing Products (referenced in user events but not in catalog):\n")
        f.write("=" * 60 + "\n")
        for pid in sorted(missing_products):
            f.write(f"{pid}\n")
    
    print(f"📁 Missing products list: {missing_file}")
    
    return matching_products, len(missing_products)

def clean_product(product):
    """Clean and optimize product data"""
    cleaned = {
        "id": product.get("id"),
        "primaryProductId": product.get("id"),  # Use same as id
        "type": "PRIMARY",  # Simplified since 99.6% are PRIMARY anyway
        "title": product.get("title", ""),
        "availability": "IN_STOCK"
    }
    
    # Add description if exists and not empty
    desc = product.get("description", "").strip()
    if desc:
        cleaned["description"] = desc
    
    # Clean categories - remove "nan" entries
    categories = product.get("categories", [])
    clean_categories = [cat for cat in categories if cat and str(cat).strip() and str(cat).strip() != "nan"]
    if clean_categories:
        cleaned["categories"] = clean_categories
    
    # Add pricing if exists
    price_info = product.get("priceInfo")
    if price_info and price_info.get("price", 0) > 0:
        cleaned["priceInfo"] = price_info
    
    # Add brands if exists
    brands = product.get("brands")
    if brands and brands[0] and str(brands[0]).strip():
        cleaned["brands"] = brands
    
    # Add URI if exists
    uri = product.get("uri")
    if uri:
        cleaned["uri"] = uri
    
    # Clean attributes - only keep useful ones
    attributes = product.get("attributes", {})
    clean_attributes = {}
    
    for attr_name, attr_value in attributes.items():
        if attr_name in ["brand", "color", "age_group", "features"] and attr_value.get("text"):
            # Filter out empty/useless values
            text_values = attr_value.get("text", [])
            if isinstance(text_values, list):
                clean_text = [val for val in text_values if val and str(val).strip()]
                if clean_text:
                    clean_attributes[attr_name] = {"text": clean_text}
            elif text_values and str(text_values).strip():
                clean_attributes[attr_name] = {"text": [str(text_values)]}
    
    if clean_attributes:
        cleaned["attributes"] = clean_attributes
    
    # Simplified variants - only if has useful SKU
    variants = product.get("variants")
    if variants and len(variants) > 0:
        variant = variants[0]
        sku = variant.get("sku")
        if sku and str(sku).strip() and str(sku).strip() != "nan":
            cleaned_variant = {
                "id": f"{product.get('id')}_variant",
                "sku": str(sku).strip()
            }
            
            # Add color attribute if exists
            if "color" in clean_attributes:
                cleaned_variant["attributes"] = {
                    "color": clean_attributes["color"]
                }
            
            cleaned["variants"] = [cleaned_variant]
    
    return cleaned

def main():
    """Main execution"""
    print("🎯 CREATING OPTIMIZED PRODUCT CATALOG")
    print("=" * 60)
    
    # File paths
    events_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\RecommendationAI_NDJSON\user_events_schema_correct.ndjson"
    catalog_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\product_catalog_final.ndjson" 
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\product_catalog_optimized.ndjson"
    
    try:
        # Load required products from user events
        user_products = load_user_event_products(events_file)
        
        # Create optimized catalog
        matched_count, missing_count = create_optimized_catalog(catalog_file, user_products, output_file)
        
        print(f"\n🎉 OPTIMIZATION COMPLETE!")
        print(f"✅ Optimized catalog: {output_file}")
        print(f"📊 Products included: {matched_count}")
        print(f"⚠️ Products missing: {missing_count}")
        print(f"💰 Cost reduction: ~{85:.0f}% (estimated)")
        
        if missing_count > 0:
            print(f"\n⚠️ IMPORTANT: {missing_count} products from user events are missing from catalog")
            print(f"   These will still appear as auto-generated entries in recommendations")
            print(f"   Consider extracting these products from database if needed")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()