#!/usr/bin/env python3
"""
Process the complete product catalog from DBeaver with all fields
"""

import json
import csv
import os
from decimal import Decimal

def process_complete_catalog():
    """Process the complete catalog CSV with all fields"""
    
    # Files
    complete_catalog_csv = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Database\complete_product_catalog.csv"
    output_catalog = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Recommendation Engine Demo\product_catalog_complete.ndjson"
    
    if not os.path.exists(complete_catalog_csv):
        print(f"❌ Complete catalog CSV not found: {complete_catalog_csv}")
        print("\n📋 Instructions:")
        print("1. Run the complete_catalog_query.sql in DBeaver")
        print("2. Export results as 'complete_product_catalog.csv'")
        print("3. Save in the Database folder")
        print("4. Run this script again")
        return False
    
    print("🔍 Processing complete product catalog with all fields...")
    
    products_created = 0
    
    with open(complete_catalog_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        with open(output_catalog, 'w', encoding='utf-8') as outfile:
            for row in reader:
                try:
                    sku_id = row.get('sku_id', '')
                    if not sku_id:
                        continue
                    
                    # Create comprehensive GCP Retail API product
                    product = {
                        "id": str(sku_id),
                        "title": row.get('product_name', f'Product {sku_id}'),
                        "description": row.get('description', ''),
                        "categories": [],
                        "brands": [],
                        "availability": row.get('availability', 'IN_STOCK'),
                        "uri": row.get('product_url', f'https://dabdoob.com/product/{sku_id}'),
                        "attributes": {}
                    }
                    
                    # Add categories
                    category_name = row.get('category_name', '')
                    parent_category = row.get('parent_category_name', '')
                    if parent_category and category_name:
                        product["categories"] = [parent_category, category_name]
                    elif category_name:
                        product["categories"] = [category_name]
                    else:
                        product["categories"] = ["General"]
                    
                    # Add brands
                    brand_name = row.get('brand_name', '')
                    if brand_name:
                        product["brands"] = [brand_name]
                    else:
                        product["brands"] = ["Unknown"]
                    
                    # Add pricing
                    price = row.get('price', '')
                    original_price = row.get('original_price', '')
                    currency = row.get('currency_code', 'SAR')
                    
                    if price and float(price) > 0:
                        product["priceInfo"] = {
                            "price": float(price),
                            "currencyCode": currency
                        }
                        if original_price and float(original_price) > float(price):
                            product["priceInfo"]["originalPrice"] = float(original_price)
                    
                    # Add comprehensive attributes
                    attributes = {}
                    
                    # Basic identifiers
                    if row.get('sku_code'):
                        attributes["sku_code"] = {"text": [row['sku_code']]}
                    if row.get('product_id'):
                        attributes["product_id"] = {"text": [row['product_id']]}
                    if row.get('upc'):
                        attributes["upc"] = {"text": [row['upc']]}
                    
                    # Categories in Arabic
                    if row.get('category_name_ar'):
                        attributes["category_name_ar"] = {"text": [row['category_name_ar']]}
                    if row.get('parent_category_name_ar'):
                        attributes["parent_category_name_ar"] = {"text": [row['parent_category_name_ar']]}
                    
                    # Product names in Arabic
                    if row.get('product_name_ar'):
                        attributes["product_name_ar"] = {"text": [row['product_name_ar']]}
                    if row.get('description_ar'):
                        attributes["description_ar"] = {"text": [row['description_ar']]}
                    
                    # Brand information
                    if row.get('brand_name_ar'):
                        attributes["brand_name_ar"] = {"text": [row['brand_name_ar']]}
                    if row.get('brand_description'):
                        attributes["brand_description"] = {"text": [row['brand_description']]}
                    
                    # Product attributes
                    if row.get('color'):
                        attributes["color"] = {"text": [row['color']]}
                    if row.get('size'):
                        attributes["size"] = {"text": [row['size']]}
                    if row.get('weight'):
                        attributes["weight"] = {"text": [row['weight']]}
                    if row.get('dimensions'):
                        attributes["dimensions"] = {"text": [row['dimensions']]}
                    if row.get('age_group'):
                        attributes["age_group"] = {"text": [row['age_group']]}
                    if row.get('material'):
                        attributes["material"] = {"text": [row['material']]}
                    if row.get('features'):
                        attributes["features"] = {"text": [row['features']]}
                    
                    # Inventory
                    if row.get('stock_quantity'):
                        attributes["stock_quantity"] = {"text": [row['stock_quantity']]}
                    
                    # Product flags
                    if row.get('is_gift_wrappable'):
                        attributes["is_gift_wrappable"] = {"text": [row['is_gift_wrappable']]}
                    if row.get('is_customizable'):
                        attributes["is_customizable"] = {"text": [row['is_customizable']]}
                    if row.get('is_featured'):
                        attributes["is_featured"] = {"text": [row['is_featured']]}
                    if row.get('is_bestseller'):
                        attributes["is_bestseller"] = {"text": [row['is_bestseller']]}
                    
                    # Ratings and reviews
                    if row.get('rating_average'):
                        attributes["rating_average"] = {"text": [row['rating_average']]}
                    if row.get('review_count'):
                        attributes["review_count"] = {"text": [row['review_count']]}
                    
                    # SEO
                    if row.get('meta_title'):
                        attributes["meta_title"] = {"text": [row['meta_title']]}
                    if row.get('meta_description'):
                        attributes["meta_description"] = {"text": [row['meta_description']]}
                    
                    # Timestamps
                    if row.get('created_at'):
                        attributes["created_at"] = {"text": [row['created_at']]}
                    if row.get('updated_at'):
                        attributes["updated_at"] = {"text": [row['updated_at']]}
                    
                    product["attributes"] = attributes
                    
                    # Add images if available
                    primary_image = row.get('primary_image_url', '')
                    all_images = row.get('all_image_urls', '')
                    
                    if primary_image:
                        product["images"] = [{"uri": primary_image, "height": 400, "width": 400}]
                        if all_images and '|' in all_images:
                            additional_images = all_images.split('|')
                            for img_url in additional_images:
                                if img_url != primary_image:
                                    product["images"].append({"uri": img_url, "height": 400, "width": 400})
                    
                    # Write product to file
                    outfile.write(json.dumps(product, ensure_ascii=False) + '\n')
                    products_created += 1
                    
                except (ValueError, KeyError) as e:
                    print(f"⚠️  Error processing row: {e}")
                    continue
    
    print(f"\n✅ Complete catalog created:")
    print(f"  • Products with full data: {products_created:,}")
    print(f"  📁 Saved to: {output_catalog}")
    
    return products_created

if __name__ == "__main__":
    process_complete_catalog()