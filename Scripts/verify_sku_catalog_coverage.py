#!/usr/bin/env python3
"""
Verify that the SKU-based catalog matches the converted user events
"""

import json
from collections import Counter

def verify_sku_catalog_coverage():
    """Check how well the SKU catalog covers the user events"""
    
    # Files
    user_events_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\RecommendationAI_NDJSON\user_events_with_sku_ids.ndjson"
    sku_catalog_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Recommendation Engine Demo\product_catalog_sku_based.ndjson"
    
    print("🔍 Loading SKU catalog...")
    
    # Load catalog SKU IDs
    catalog_sku_ids = set()
    with open(sku_catalog_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                product = json.loads(line.strip())
                catalog_sku_ids.add(product['id'])
            except json.JSONDecodeError:
                continue
    
    print(f"✅ Loaded {len(catalog_sku_ids)} SKU IDs from catalog")
    
    print("🔍 Analyzing user events SKU coverage...")
    
    # Analyze user events
    event_sku_ids = set()
    event_sku_counter = Counter()
    total_events = 0
    covered_events = 0
    
    with open(user_events_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                event = json.loads(line.strip())
                total_events += 1
                
                product_details = event.get('productDetails', [])
                event_has_coverage = True
                
                for product_detail in product_details:
                    sku_id = product_detail.get('product', {}).get('id', '')
                    if sku_id:
                        event_sku_ids.add(sku_id)
                        event_sku_counter[sku_id] += 1
                        
                        if sku_id not in catalog_sku_ids:
                            event_has_coverage = False
                
                if event_has_coverage and product_details:
                    covered_events += 1
                    
            except json.JSONDecodeError:
                continue
    
    # Calculate coverage
    covered_skus = event_sku_ids & catalog_sku_ids
    missing_skus = event_sku_ids - catalog_sku_ids
    
    print(f"\n📊 SKU Coverage Analysis:")
    print(f"  • Total user events: {total_events:,}")
    print(f"  • Events with full catalog coverage: {covered_events:,}")
    print(f"  • Coverage percentage: {(covered_events/total_events)*100:.1f}%")
    print(f"")
    print(f"  • Unique SKU IDs in events: {len(event_sku_ids):,}")
    print(f"  • SKU IDs covered by catalog: {len(covered_skus):,}")
    print(f"  • SKU IDs missing from catalog: {len(missing_skus):,}")
    print(f"  • SKU coverage percentage: {(len(covered_skus)/len(event_sku_ids))*100:.1f}%")
    
    if missing_skus:
        print(f"\n⚠️  Sample missing SKU IDs:")
        for sku_id in sorted(list(missing_skus))[:10]:
            count = event_sku_counter[sku_id]
            print(f"  • {sku_id} ({count} events)")
    
    # Show some successful matches
    print(f"\n✅ Sample matched SKU IDs:")
    for sku_id in sorted(list(covered_skus))[:10]:
        count = event_sku_counter[sku_id]
        print(f"  • {sku_id} ({count} events)")
    
    return covered_events, total_events

if __name__ == "__main__":
    verify_sku_catalog_coverage()