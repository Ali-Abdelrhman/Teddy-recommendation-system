#!/usr/bin/env python3
"""
Create a product catalog using SKU_IDs that match the converted user events
"""

import json
import csv
from collections import defaultdict

def create_sku_product_catalog():
    """Create a product catalog using SKU_IDs from the comprehensive product database"""
    
    # Files
    products_csv = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\sample\samples\all prod with cat info.csv"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Recommendation Engine Demo\product_catalog_sku_based.ndjson"
    
    print("🔍 Loading comprehensive product data with categories...")
    
    # Load product data directly from the comprehensive CSV
    products_data = {}
    
    with open(products_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                sku_id = row['sku_id']
                product_name = row['product_name']
                category_name = row['category_name']
                brand_name = row['brand_name']
                category_name_ar = row['category_name_ar']
                full_category_path = row['full_category_path']
                
                # Store product data with SKU_ID as key
                products_data[sku_id] = {
                    'title': product_name,
                    'description': f"High quality {product_name}. Category: {category_name}. Brand: {brand_name}.",
                    'categories': [category_name] if category_name else ['General'],
                    'brands': [brand_name] if brand_name else ['Unknown'],
                    'availability': 'IN_STOCK',
                    'uri': f'https://dabdoob.com/product/{sku_id}',
                    'category_id': row.get('category_id', ''),
                    'category_name_ar': category_name_ar,
                    'full_category_path': full_category_path,
                    'product_id': row.get('product_id', '')
                }
                        
            except (ValueError, KeyError) as e:
                continue
    
    print(f"✅ Loaded {len(products_data)} products with comprehensive data")
    
    # Create Google Cloud Retail API compatible products
    print("🔄 Creating GCP Retail API compatible catalog...")
    
    created_products = 0
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for sku_id, product_data in products_data.items():
            
            # Create Google Cloud Retail API compatible product
            retail_product = {
                "id": str(sku_id),  # Use SKU_ID as the product ID
                "title": product_data['title'],
                "description": product_data['description'],
                "categories": product_data['categories'],
                "brands": product_data['brands'],
                "availability": product_data['availability'],
                "uri": product_data['uri'],
                "attributes": {}
            }
            
            # Add attributes
            retail_product["attributes"] = {
                "sku_id": {"text": [str(sku_id)]},
                "category_id": {"text": [product_data['category_id']]},
                "full_category_path": {"text": [product_data['full_category_path']]},
                "product_id": {"text": [product_data['product_id']]}
            }
            
            # Add Arabic category name if available
            if product_data['category_name_ar']:
                retail_product["attributes"]["category_name_ar"] = {"text": [product_data['category_name_ar']]}
            
            # Write to file
            outfile.write(json.dumps(retail_product, ensure_ascii=False) + '\n')
            created_products += 1
    
    print(f"\n📊 Catalog Creation Summary:")
    print(f"  • Total SKU-based products created: {created_products:,}")
    print(f"  📁 Catalog saved to: {output_file}")
    
    return created_products

if __name__ == "__main__":
    create_sku_product_catalog()