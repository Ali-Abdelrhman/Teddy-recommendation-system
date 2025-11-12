#!/usr/bin/env python3
"""
Filter user events to only include products that exist in the catalog.
This approach ensures all recommendations will be for real products with proper data.
"""

import json
import csv
import sys
from collections import defaultdict

def filter_user_events_to_existing_products():
    # File paths
    product_csv = "../Test CSVs/product_202510211556.csv"
    user_events_file = "../RecommendationAI_NDJSON/user_events_schema_correct.ndjson"
    output_events_file = "../RecommendationAI_NDJSON/user_events_filtered_existing_products.ndjson"
    output_catalog_file = "../RecommendationAI_NDJSON/products_real_catalog.ndjson"
    
    print("=== Filtering User Events to Existing Products ===")
    print(f"Source product CSV: {product_csv}")
    print(f"User events file: {user_events_file}")
    print(f"Output filtered events: {output_events_file}")
    print(f"Output real catalog: {output_catalog_file}")
    
    # Step 1: Load existing products from CSV
    print("\n=== Loading Existing Products ===")
    existing_products = {}
    
    try:
        with open(product_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    sku_id = int(row['sku_id'])
                    product_id = f"PROD{sku_id}"
                    existing_products[product_id] = {
                        'sku_id': sku_id,
                        'name_en': row.get('name_en', ''),
                        'name_ar': row.get('name_ar', ''),
                        'description_en': row.get('description_en', ''),
                        'description_ar': row.get('description_ar', ''),
                        'brand_id': row.get('brand_id', ''),
                        'subcategory_id': row.get('subcategory_id', ''),
                        'upc': row.get('upc', '')
                    }
                except (ValueError, KeyError):
                    continue
        
        print(f"Loaded {len(existing_products)} existing products")
        print("Existing product IDs:", list(existing_products.keys()))
        
    except FileNotFoundError:
        print(f"Error: Could not find product CSV: {product_csv}")
        return False
    
    # Step 2: Create Google Cloud Retail catalog with existing products
    print("\n=== Creating Real Product Catalog ===")
    with open(output_catalog_file, 'w', encoding='utf-8') as catalog_file:
        for product_id, product_data in existing_products.items():
            retail_product = {
                "id": product_id,
                "title": product_data['name_en'] or f"Product {product_data['sku_id']}",
                "description": product_data['description_en'] or f"Description for product {product_data['sku_id']}",
                "brands": [product_data['brand_id']] if product_data['brand_id'] else ["Unknown"],
                "categories": [f"Category_{product_data['subcategory_id']}"] if product_data['subcategory_id'] else ["General"],
                "availability": "IN_STOCK",
                "uri": f"https://dabdoob.com/product/{product_data['sku_id']}",
                "attributes": {
                    "sku_id": {
                        "text": [str(product_data['sku_id'])]
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
            
            catalog_file.write(json.dumps(retail_product) + '\n')
    
    print(f"Created catalog with {len(existing_products)} real products")
    
    # Step 3: Filter user events to only include existing products
    print("\n=== Filtering User Events ===")
    total_events = 0
    filtered_events = 0
    product_references = defaultdict(int)
    
    with open(user_events_file, 'r', encoding='utf-8') as infile, \
         open(output_events_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            line = line.strip()
            if not line:
                continue
                
            try:
                event = json.loads(line)
                total_events += 1
                
                # Check if event references existing products
                has_existing_products = False
                if 'productDetails' in event:
                    filtered_product_details = []
                    
                    for product_detail in event['productDetails']:
                        if 'product' in product_detail and 'id' in product_detail['product']:
                            product_id = product_detail['product']['id']
                            product_references[product_id] += 1
                            
                            if product_id in existing_products:
                                filtered_product_details.append(product_detail)
                                has_existing_products = True
                    
                    # Only keep event if it has at least one existing product
                    if has_existing_products:
                        event['productDetails'] = filtered_product_details
                        outfile.write(json.dumps(event) + '\n')
                        filtered_events += 1
                
                if total_events % 10000 == 0:
                    print(f"Processed {total_events} events, kept {filtered_events}")
                    
            except json.JSONDecodeError:
                continue
    
    print(f"\n=== Filtering Complete ===")
    print(f"Total events processed: {total_events}")
    print(f"Events with existing products: {filtered_events}")
    print(f"Filtering rate: {filtered_events/total_events*100:.1f}%" if total_events > 0 else "No events processed")
    
    # Show product reference statistics
    print("\n=== Product Reference Statistics ===")
    existing_refs = {pid: count for pid, count in product_references.items() if pid in existing_products}
    missing_refs = {pid: count for pid, count in product_references.items() if pid not in existing_products}
    
    print(f"References to existing products: {sum(existing_refs.values())}")
    print(f"References to missing products: {sum(missing_refs.values())}")
    print(f"Existing products referenced: {len(existing_refs)}")
    print(f"Missing products referenced: {len(missing_refs)}")
    
    if existing_refs:
        print("Top existing products by references:")
        for pid, count in sorted(existing_refs.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {pid}: {count} references")
    
    # Sample verification
    print("\n=== Sample Verification ===")
    with open(output_events_file, 'r', encoding='utf-8') as f:
        sample_events = []
        for i, line in enumerate(f):
            if i >= 3:
                break
            sample_events.append(json.loads(line.strip()))
    
    print("Sample filtered events:")
    for i, event in enumerate(sample_events, 1):
        print(f"  Event {i}:")
        print(f"    Type: {event.get('eventType')}")
        print(f"    Products: {[pd['product']['id'] for pd in event.get('productDetails', [])]}")
        print()
    
    return True

if __name__ == "__main__":
    success = filter_user_events_to_existing_products()
    sys.exit(0 if success else 1)