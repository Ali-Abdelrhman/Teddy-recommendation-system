#!/usr/bin/env python3
"""
Create a product catalog that matches the product IDs used in user events.
The user events reference products as PROD{sku_id}, but the current catalog
uses a different ID scheme. This script creates a proper catalog based on
the actual source product data with matching IDs.
"""

import json
import csv
import sys
from collections import defaultdict

def create_matching_product_catalog():
    # File paths
    product_csv = "../Test CSVs/product_202510211556.csv"
    user_events_file = "../RecommendationAI_NDJSON/user_events_schema_correct.ndjson"
    output_file = "../RecommendationAI_NDJSON/products_matching_events.ndjson"
    
    print("=== Creating Product Catalog Matching User Events ===")
    print(f"Source product CSV: {product_csv}")
    print(f"User events file: {user_events_file}")
    print(f"Output catalog: {output_file}")
    
    # Step 1: Extract all product IDs referenced in user events
    print("\n=== Extracting Product IDs from User Events ===")
    event_product_ids = set()
    event_count = 0
    
    try:
        with open(user_events_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    event = json.loads(line)
                    event_count += 1
                    
                    if 'productDetails' in event:
                        for product_detail in event['productDetails']:
                            if 'product' in product_detail and 'id' in product_detail['product']:
                                product_id = product_detail['product']['id']
                                event_product_ids.add(product_id)
                                
                except json.JSONDecodeError:
                    continue
        
        print(f"Processed {event_count} user events")
        print(f"Found {len(event_product_ids)} unique product IDs")
        print("Sample product IDs from events:", list(event_product_ids)[:10])
        
    except FileNotFoundError:
        print(f"Error: Could not find user events file: {user_events_file}")
        return False
    
    # Step 2: Extract SKU IDs from the PROD prefixed IDs
    print("\n=== Extracting SKU IDs ===")
    sku_ids = set()
    for product_id in event_product_ids:
        if product_id.startswith('PROD'):
            sku_id = product_id[4:]  # Remove 'PROD' prefix
            try:
                sku_ids.add(int(sku_id))
            except ValueError:
                print(f"Warning: Invalid SKU ID format: {product_id}")
    
    print(f"Extracted {len(sku_ids)} SKU IDs")
    print("Sample SKU IDs:", sorted(list(sku_ids))[:10])
    
    # Step 3: Read product data from CSV
    print("\n=== Reading Product CSV Data ===")
    products_data = {}
    
    try:
        with open(product_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    sku_id = int(row['sku_id'])
                    products_data[sku_id] = {
                        'id': f"PROD{sku_id}",
                        'sku_id': sku_id,
                        'name_en': row.get('name_en', ''),
                        'name_ar': row.get('name_ar', ''),
                        'description_en': row.get('description_en', ''),
                        'description_ar': row.get('description_ar', ''),
                        'brand_id': row.get('brand_id', ''),
                        'subcategory_id': row.get('subcategory_id', ''),
                        'upc': row.get('upc', ''),
                        'is_deleted': row.get('is_deleted', '0')
                    }
                except (ValueError, KeyError) as e:
                    continue
        
        print(f"Loaded {len(products_data)} products from CSV")
        
    except FileNotFoundError:
        print(f"Error: Could not find product CSV: {product_csv}")
        return False
    
    # Step 4: Create Google Cloud Retail API compatible products
    print("\n=== Creating Google Cloud Retail Products ===")
    created_products = 0
    missing_products = 0
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for sku_id in sorted(sku_ids):
            if sku_id in products_data:
                product_data = products_data[sku_id]
                
                # Create Google Cloud Retail API compatible product
                retail_product = {
                    "id": f"PROD{sku_id}",
                    "title": product_data['name_en'] or f"Product {sku_id}",
                    "description": product_data['description_en'] or f"Description for product {sku_id}",
                    "brands": [product_data['brand_id']] if product_data['brand_id'] else ["Unknown"],
                    "categories": [f"Category_{product_data['subcategory_id']}"] if product_data['subcategory_id'] else ["General"],
                    "availability": "IN_STOCK",
                    "uri": f"https://dabdoob.com/product/{sku_id}",
                    "attributes": {
                        "sku_id": {
                            "text": [str(sku_id)]
                        }
                    }
                }
                
                # Add Arabic title if available
                if product_data['name_ar']:
                    retail_product["attributes"]["title_ar"] = {
                        "text": [product_data['name_ar']]
                    }
                
                # Add UPC if available
                if product_data['upc']:
                    retail_product["attributes"]["upc"] = {
                        "text": [product_data['upc']]
                    }
                
                outfile.write(json.dumps(retail_product) + '\n')
                created_products += 1
                
            else:
                print(f"Warning: SKU ID {sku_id} (PROD{sku_id}) not found in product CSV")
                missing_products += 1
    
    print(f"\n=== Catalog Creation Complete ===")
    print(f"Created products: {created_products}")
    print(f"Missing products: {missing_products}")
    print(f"Success rate: {created_products/(created_products+missing_products)*100:.1f}%")
    
    # Step 5: Verify created catalog
    print("\n=== Verification ===")
    with open(output_file, 'r', encoding='utf-8') as f:
        sample_products = []
        for i, line in enumerate(f):
            if i >= 3:
                break
            product = json.loads(line.strip())
            sample_products.append(product)
    
    print("Sample created products:")
    for i, product in enumerate(sample_products, 1):
        print(f"  Product {i}:")
        print(f"    ID: {product['id']}")
        print(f"    Title: {product['title']}")
        print(f"    Categories: {product['categories']}")
        print()
    
    return True

if __name__ == "__main__":
    success = create_matching_product_catalog()
    sys.exit(0 if success else 1)