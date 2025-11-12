#!/usr/bin/env python3
"""
Validate that all user events match real products in the catalog
"""

import json
import os

def validate_perfect_alignment():
    """Ensure 100% alignment between user events and product catalog"""
    
    catalog_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\RecommendationAI_NDJSON\product_catalog_real_only.ndjson"
    events_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\RecommendationAI_NDJSON\user_events_real_products.ndjson"
    
    if not os.path.exists(catalog_file):
        print(f"❌ Catalog file not found: {catalog_file}")
        return False
    
    if not os.path.exists(events_file):
        print(f"❌ Events file not found: {events_file}")
        print("ℹ️  Run convert_real_events_csv.py first")
        return False
    
    print("🔍 Loading product catalog...")
    catalog_products = set()
    
    with open(catalog_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if line_num > 14990:  # Only use first 14,990 lines
                break
            try:
                product = json.loads(line.strip())
                catalog_products.add(product['id'])
            except (json.JSONDecodeError, KeyError):
                continue
    
    print(f"📊 Loaded {len(catalog_products):,} products from catalog")
    
    print("🔍 Loading user events...")
    event_products = set()
    events_count = 0
    
    with open(events_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                event = json.loads(line.strip())
                for detail in event.get('productDetails', []):
                    product_id = detail['product']['id']
                    event_products.add(product_id)
                events_count += 1
            except (json.JSONDecodeError, KeyError):
                continue
    
    print(f"📊 Loaded {events_count:,} user events")
    print(f"📊 Events reference {len(event_products):,} unique products")
    
    # Check perfect alignment
    missing_products = event_products - catalog_products
    orphaned_products = catalog_products - event_products
    
    coverage_percentage = (len(event_products & catalog_products) / len(catalog_products)) * 100
    
    print("\n" + "="*60)
    print("🎯 PERFECT ALIGNMENT VALIDATION")
    print("="*60)
    
    print(f"📦 Products in catalog: {len(catalog_products):,}")
    print(f"🎯 Products in events: {len(event_products):,}")
    print(f"✅ Products with events: {len(event_products & catalog_products):,}")
    print(f"📊 Coverage percentage: {coverage_percentage:.1f}%")
    
    if missing_products:
        print(f"\n❌ Missing from catalog: {len(missing_products):,} products")
        print("First 10 missing products:")
        for i, product_id in enumerate(list(missing_products)[:10]):
            print(f"  - {product_id}")
    else:
        print("\n✅ Perfect alignment: All event products exist in catalog!")
    
    if orphaned_products:
        print(f"\n⚠️  Products without events: {len(orphaned_products):,}")
    
    print(f"\n📈 Recommendation system readiness: {'✅ PERFECT' if not missing_products else '❌ NEEDS FIXING'}")
    
    return len(missing_products) == 0

if __name__ == "__main__":
    validate_perfect_alignment()