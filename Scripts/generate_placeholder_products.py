#!/usr/bin/env python3
"""
Generate smart placeholder products for missing IDs
This creates realistic-looking products to prevent auto-generated entries
"""

import json
import random

def generate_placeholder_product(product_id):
    """Generate a realistic placeholder product"""
    
    # Extract SKU number for deterministic generation
    sku_num = int(product_id[4:])
    random.seed(sku_num)  # Deterministic based on ID
    
    # Product name templates
    name_templates = [
        "Premium Quality Product",
        "Essential Daily Item", 
        "Popular Choice Product",
        "Customer Favorite Item",
        "Best Value Product",
        "High Quality Item",
        "Recommended Product",
        "Top Rated Item"
    ]
    
    # Categories
    categories = [
        "General Products",
        "Popular Items", 
        "Best Sellers",
        "Customer Favorites",
        "Essential Products"
    ]
    
    # Brands
    brands = [
        "Premium Brand",
        "Quality Plus",
        "Best Choice", 
        "Excellence",
        "Superior"
    ]
    
    # Colors
    colors = ["Multi-Color", "Black", "White", "Blue", "Red", "Green"]
    
    # Generate realistic pricing based on SKU number
    base_price = 10 + (sku_num % 100)  # Range: 10-109 SAR
    if sku_num % 7 == 0:  # Some expensive items
        base_price *= 3
    elif sku_num % 3 == 0:  # Some mid-range items  
        base_price *= 1.5
    
    current_price = round(base_price + random.uniform(-5, 15), 2)
    original_price = round(current_price * 1.2, 2)
    
    # Generate product
    product = {
        "id": product_id,
        "primaryProductId": product_id,
        "type": "PRIMARY",
        "title": f"{random.choice(name_templates)} {sku_num}",
        "availability": "IN_STOCK",
        "description": f"High quality product designed for everyday use. Product ID: {product_id}. Excellent value and customer satisfaction guaranteed.",
        "categories": [random.choice(categories)],
        "priceInfo": {
            "currency": "SAR",
            "price": current_price,
            "originalPrice": original_price
        },
        "brands": [random.choice(brands)],
        "uri": f"https://dabdoob.com/products/product-{sku_num}",
        "attributes": {
            "brand": {"text": [random.choice(brands)]},
            "color": {"text": [random.choice(colors)]},
            "features": {"text": ["High Quality", "Customer Recommended"]}
        },
        "variants": [{
            "id": f"{product_id}_variant",
            "sku": f"SKU-{sku_num}",
            "attributes": {
                "color": {"text": [random.choice(colors)]}
            }
        }]
    }
    
    return product

def create_placeholder_catalog():
    """Create placeholder catalog for missing products"""
    
    print("🔧 CREATING PLACEHOLDER PRODUCTS")
    print("=" * 50)
    
    # Load missing product IDs
    missing_ids = []
    with open('c:/Users/Ahmed/Downloads/Teddy recommendation system/product_catalog_optimized_missing_products.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('PROD') and len(line) == 10:
                missing_ids.append(line)
    
    print(f"📋 Generating placeholders for {len(missing_ids)} missing products...")
    
    # Generate placeholder products
    placeholder_products = []
    for product_id in missing_ids:
        product = generate_placeholder_product(product_id)
        placeholder_products.append(product)
    
    # Write placeholder catalog
    output_file = 'c:/Users/Ahmed/Downloads/Teddy recommendation system/product_catalog_placeholders.ndjson'
    with open(output_file, 'w', encoding='utf-8') as f:
        for product in placeholder_products:
            f.write(json.dumps(product, ensure_ascii=False) + '\n')
    
    print(f"✅ Created {len(placeholder_products)} placeholder products")
    print(f"📁 Output: {output_file}")
    
    # Sample product
    if placeholder_products:
        print(f"\n📝 Sample placeholder product:")
        sample = placeholder_products[0]
        print(f"  ID: {sample['id']}")
        print(f"  Title: {sample['title']}")
        print(f"  Price: {sample['priceInfo']['price']} SAR")
        print(f"  Brand: {sample['brands'][0]}")
    
    return output_file

if __name__ == "__main__":
    create_placeholder_catalog()