#!/usr/bin/env python3
"""
Convert user events from PROD-format product IDs to SKU_IDs using database mapping
"""

import json
import csv
import re
from pathlib import Path

def convert_user_events_to_sku_ids():
    """Convert user events from PROD IDs to SKU_IDs"""
    
    # Files
    user_events_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\RecommendationAI_NDJSON\user_events_schema_correct.ndjson"
    sku_mapping_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\sample\samples\_SELECT_product_id_MIN_id_as_primary_sku_id_MIN_code_as_primary__202510280353.csv"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\RecommendationAI_NDJSON\user_events_with_sku_ids.ndjson"
    
    print("🔍 Loading SKU ID mapping from database...")
    
    # Load PROD ID to SKU_ID mapping
    prod_to_sku_mapping = {}
    
    try:
        with open(sku_mapping_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    product_id = int(row['product_id'])
                    sku_id = row['primary_sku_id']
                    
                    # Create mapping from PROD format to SKU_ID
                    prod_id = f"PROD{product_id:06d}"
                    prod_to_sku_mapping[prod_id] = sku_id
                    
                except (ValueError, KeyError):
                    continue
        
        print(f"✅ Loaded {len(prod_to_sku_mapping)} PROD → SKU_ID mappings")
        
        # Show some examples
        print("\n📋 Sample mappings:")
        for i, (prod_id, sku_id) in enumerate(list(prod_to_sku_mapping.items())[:5]):
            print(f"  • {prod_id} → {sku_id}")
            
    except FileNotFoundError:
        print(f"❌ Could not find SKU mapping file: {sku_mapping_file}")
        return False
    
    print("\n🔄 Converting user events to use SKU_IDs...")
    
    # Convert user events
    total_events = 0
    converted_events = 0
    missing_mappings = 0
    missing_prod_ids = set()
    
    with open(user_events_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            try:
                event = json.loads(line.strip())
                total_events += 1
                
                # Convert product IDs in productDetails
                product_details = event.get('productDetails', [])
                converted_this_event = True
                
                for product_detail in product_details:
                    prod_id = product_detail.get('product', {}).get('id', '')
                    
                    if prod_id in prod_to_sku_mapping:
                        # Convert PROD ID to SKU_ID
                        sku_id = prod_to_sku_mapping[prod_id]
                        product_detail['product']['id'] = sku_id
                    else:
                        # Keep track of missing mappings
                        missing_mappings += 1
                        missing_prod_ids.add(prod_id)
                        converted_this_event = False
                
                # Only write event if all products were successfully converted
                if converted_this_event and product_details:
                    outfile.write(json.dumps(event, ensure_ascii=False) + '\n')
                    converted_events += 1
                    
            except json.JSONDecodeError:
                continue
    
    print(f"\n📊 User Events Conversion Summary:")
    print(f"  • Total events processed: {total_events:,}")
    print(f"  • Events successfully converted: {converted_events:,}")
    print(f"  • Events with missing SKU mappings: {total_events - converted_events:,}")
    print(f"  • Unique PROD IDs without SKU mapping: {len(missing_prod_ids)}")
    
    if missing_prod_ids:
        print(f"\n⚠️  Sample missing PROD IDs:")
        for prod_id in sorted(list(missing_prod_ids))[:10]:
            print(f"  • {prod_id}")
    
    print(f"\n✅ Converted user events saved to: {output_file}")
    
    # Also create a real products catalog with SKU_IDs
    print("\n🔄 Creating product catalog with SKU_IDs...")
    create_sku_product_catalog(prod_to_sku_mapping)
    
    return converted_events

def create_sku_product_catalog(prod_to_sku_mapping):
    """Create a product catalog using SKU_IDs instead of PROD IDs"""
    
    input_catalog = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Recommendation Engine Demo\product_catalog_final_categories.ndjson"
    output_catalog = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Recommendation Engine Demo\product_catalog_with_sku_ids.ndjson"
    
    # Reverse mapping: SKU_ID to PROD
    sku_to_prod_mapping = {sku: prod for prod, sku in prod_to_sku_mapping.items()}
    
    catalog_products = 0
    converted_products = 0
    
    with open(input_catalog, 'r', encoding='utf-8') as infile, \
         open(output_catalog, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            try:
                product = json.loads(line.strip())
                catalog_products += 1
                
                # Check if this is a real product with SKU mapping
                prod_id = product.get('id', '')
                
                if prod_id in prod_to_sku_mapping:
                    # Convert to SKU_ID
                    sku_id = prod_to_sku_mapping[prod_id]
                    product['id'] = sku_id
                    
                    outfile.write(json.dumps(product, ensure_ascii=False) + '\n')
                    converted_products += 1
                    
            except json.JSONDecodeError:
                continue
    
    print(f"  • Total catalog products: {catalog_products:,}")
    print(f"  • Products with SKU_IDs: {converted_products:,}")
    print(f"  📁 SKU catalog saved to: {output_catalog}")

if __name__ == "__main__":
    convert_user_events_to_sku_ids()