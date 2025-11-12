#!/usr/bin/env python3
"""
Filter user events to only include events for real products (remove events for synthetic products)
"""

import json
import pandas as pd
from pathlib import Path

def filter_user_events_to_real_products():
    """Filter user events to only reference real products from the clean catalog"""
    
    # Files
    clean_catalog_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Recommendation Engine Demo\product_catalog_real_only.ndjson"
    user_events_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\RecommendationAI_NDJSON\user_events_schema_correct.ndjson"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\RecommendationAI_NDJSON\user_events_real_products_only.ndjson"
    
    print("🔍 Loading real product IDs from clean catalog...")
    
    # Load real product IDs
    real_product_ids = set()
    with open(clean_catalog_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                product = json.loads(line.strip())
                real_product_ids.add(product['id'])
            except json.JSONDecodeError:
                continue
    
    print(f"✅ Loaded {len(real_product_ids)} real product IDs")
    
    # Filter user events
    print("🔄 Filtering user events to real products only...")
    
    total_events = 0
    kept_events = 0
    filtered_events = 0
    
    with open(user_events_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            try:
                event = json.loads(line.strip())
                total_events += 1
                
                # Check if ALL product IDs in this event exist in real products
                product_details = event.get('productDetails', [])
                if not product_details:
                    filtered_events += 1
                    continue
                
                # Check if all products in this event are real
                all_real = True
                for product_detail in product_details:
                    product_id = product_detail.get('product', {}).get('id', '')
                    if product_id not in real_product_ids:
                        all_real = False
                        break
                
                if all_real:
                    outfile.write(json.dumps(event, ensure_ascii=False) + '\n')
                    kept_events += 1
                else:
                    filtered_events += 1
                    
            except json.JSONDecodeError:
                continue
    
    print(f"\n📊 User Events Filtering Summary:")
    print(f"  • Total events processed: {total_events:,}")
    print(f"  • Events kept (real products): {kept_events:,}")
    print(f"  • Events filtered out (synthetic): {filtered_events:,}")
    print(f"  • Keep percentage: {(kept_events/total_events)*100:.1f}%")
    
    print(f"\n✅ Filtered user events saved to: {output_file}")
    
    return kept_events, filtered_events

if __name__ == "__main__":
    filter_user_events_to_real_products()