#!/usr/bin/env python3
"""
Analyze how many user events match real database products vs synthetic products
"""

import json
from collections import Counter

def analyze_real_vs_synthetic_coverage():
    """Analyze user events coverage with real database products"""
    
    # Files
    user_events_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\RecommendationAI_NDJSON\user_events_with_sku_ids.ndjson"
    real_catalog_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Recommendation Engine Demo\product_catalog_sku_based.ndjson"
    
    print("🔍 Analyzing user events coverage with REAL database products...")
    
    # Load real database SKU IDs from your CSV
    real_database_skus = set()
    with open(real_catalog_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                product = json.loads(line.strip())
                real_database_skus.add(product['id'])
            except json.JSONDecodeError:
                continue
    
    print(f"✅ Real database products: {len(real_database_skus):,}")
    
    # Analyze user events
    total_events = 0
    events_with_real_products = 0
    events_with_synthetic_products = 0
    events_mixed = 0
    
    all_event_skus = set()
    real_event_skus = set()
    synthetic_event_skus = set()
    
    real_sku_counter = Counter()
    synthetic_sku_counter = Counter()
    
    with open(user_events_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                event = json.loads(line.strip())
                total_events += 1
                
                event_has_real = False
                event_has_synthetic = False
                
                for product_detail in event.get('productDetails', []):
                    sku_id = product_detail.get('product', {}).get('id', '')
                    if sku_id:
                        all_event_skus.add(sku_id)
                        
                        if sku_id in real_database_skus:
                            event_has_real = True
                            real_event_skus.add(sku_id)
                            real_sku_counter[sku_id] += 1
                        else:
                            event_has_synthetic = True
                            synthetic_event_skus.add(sku_id)
                            synthetic_sku_counter[sku_id] += 1
                
                # Categorize event
                if event_has_real and not event_has_synthetic:
                    events_with_real_products += 1
                elif event_has_synthetic and not event_has_real:
                    events_with_synthetic_products += 1
                elif event_has_real and event_has_synthetic:
                    events_mixed += 1
                    
            except json.JSONDecodeError:
                continue
    
    print(f"\n📊 USER EVENTS ANALYSIS:")
    print(f"  • Total user events: {total_events:,}")
    print(f"  • Events with ONLY real database products: {events_with_real_products:,} ({events_with_real_products/total_events*100:.1f}%)")
    print(f"  • Events with ONLY synthetic products: {events_with_synthetic_products:,} ({events_with_synthetic_products/total_events*100:.1f}%)")
    print(f"  • Events with mixed real/synthetic: {events_mixed:,} ({events_mixed/total_events*100:.1f}%)")
    
    print(f"\n📊 SKU ANALYSIS:")
    print(f"  • Total unique SKUs in events: {len(all_event_skus):,}")
    print(f"  • SKUs that match real database: {len(real_event_skus):,} ({len(real_event_skus)/len(all_event_skus)*100:.1f}%)")
    print(f"  • SKUs that are synthetic/missing: {len(synthetic_event_skus):,} ({len(synthetic_event_skus)/len(all_event_skus)*100:.1f}%)")
    
    print(f"\n✅ REAL DATABASE PRODUCTS IN EVENTS:")
    print("Sample real products with event counts:")
    for sku_id, count in real_sku_counter.most_common(10):
        print(f"  • SKU {sku_id}: {count} events")
    
    print(f"\n⚠️  SYNTHETIC/MISSING PRODUCTS IN EVENTS:")
    print("Sample synthetic/missing products with event counts:")
    for sku_id, count in synthetic_sku_counter.most_common(10):
        print(f"  • SKU {sku_id}: {count} events")
    
    # Summary
    real_events_total = events_with_real_products + events_mixed
    synthetic_events_total = events_with_synthetic_products + events_mixed
    
    print(f"\n🎯 SUMMARY:")
    print(f"  • Events involving real database products: {real_events_total:,} ({real_events_total/total_events*100:.1f}%)")
    print(f"  • Events involving synthetic products: {synthetic_events_total:,} ({synthetic_events_total/total_events*100:.1f}%)")
    print(f"  • Pure real database events: {events_with_real_products:,} ({events_with_real_products/total_events*100:.1f}%)")
    
    return {
        'total_events': total_events,
        'real_only_events': events_with_real_products,
        'synthetic_only_events': events_with_synthetic_products,
        'mixed_events': events_mixed,
        'real_skus': len(real_event_skus),
        'synthetic_skus': len(synthetic_event_skus)
    }

if __name__ == "__main__":
    analyze_real_vs_synthetic_coverage()