#!/usr/bin/env python3
"""
Analyze user event product IDs to understand the mismatch with real database products
"""

import json
from collections import Counter, defaultdict

def analyze_user_event_product_ids():
    """Analyze what product IDs are referenced in user events"""
    
    user_events_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\RecommendationAI_NDJSON\user_events_schema_correct.ndjson"
    clean_catalog_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Recommendation Engine Demo\product_catalog_real_only.ndjson"
    
    print("🔍 Analyzing user event product IDs...")
    
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
    
    # Analyze user event product IDs
    event_product_ids = set()
    event_product_counter = Counter()
    
    with open(user_events_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                event = json.loads(line.strip())
                product_details = event.get('productDetails', [])
                
                for product_detail in product_details:
                    product_id = product_detail.get('product', {}).get('id', '')
                    if product_id:
                        event_product_ids.add(product_id)
                        event_product_counter[product_id] += 1
                        
            except json.JSONDecodeError:
                continue
    
    print(f"📊 User Events Analysis:")
    print(f"  • Total unique product IDs in events: {len(event_product_ids)}")
    print(f"  • Product IDs that exist in real catalog: {len(event_product_ids & real_product_ids)}")
    print(f"  • Product IDs that DON'T exist in real catalog: {len(event_product_ids - real_product_ids)}")
    
    # Show some examples of event product IDs
    print(f"\n🔍 Sample user event product IDs:")
    sample_event_ids = sorted(list(event_product_ids))[:10]
    for pid in sample_event_ids:
        status = "✅ REAL" if pid in real_product_ids else "❌ NOT IN DB"
        count = event_product_counter[pid]
        print(f"  • {pid} - {count} events - {status}")
    
    # Check ID ranges
    event_id_numbers = []
    real_id_numbers = []
    
    for pid in event_product_ids:
        if pid.startswith('PROD'):
            try:
                num = int(pid[4:])  # Remove 'PROD' prefix
                event_id_numbers.append(num)
            except ValueError:
                pass
    
    for pid in real_product_ids:
        if pid.startswith('PROD'):
            try:
                num = int(pid[4:])  # Remove 'PROD' prefix
                real_id_numbers.append(num)
            except ValueError:
                pass
    
    if event_id_numbers and real_id_numbers:
        print(f"\n📈 ID Range Analysis:")
        print(f"  • User event product ID range: {min(event_id_numbers)} - {max(event_id_numbers)}")
        print(f"  • Real database product ID range: {min(real_id_numbers)} - {max(real_id_numbers)}")
        
        # Check overlap
        event_range = set(event_id_numbers)
        real_range = set(real_id_numbers)
        overlap = event_range & real_range
        print(f"  • Overlapping IDs: {len(overlap)}")
        print(f"  • Event IDs not in database: {len(event_range - real_range)}")
        print(f"  • Database IDs not in events: {len(real_range - event_range)}")

if __name__ == "__main__":
    analyze_user_event_product_ids()