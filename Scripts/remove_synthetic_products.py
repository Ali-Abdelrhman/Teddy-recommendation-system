#!/usr/bin/env python3
"""
Remove synthetic products from the catalog and create a clean version
that only contains real database products.
"""

import json
import re
from pathlib import Path

def remove_synthetic_products():
    """Remove synthetic products from the catalog"""
    
    input_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Recommendation Engine Demo\product_catalog_final_categories.ndjson"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Recommendation Engine Demo\product_catalog_real_only.ndjson"
    
    synthetic_patterns = [
        r"Premium Quality Product \d+",
        r"Popular Choice Product \d+",
        r"Best Value Product \d+",
        r"Top Rated Product \d+",
        r"Customer Favorite Product \d+"
    ]
    
    real_products = []
    synthetic_count = 0
    
    print("🔍 Analyzing product catalog...")
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line_num, line in enumerate(infile, 1):
            try:
                product = json.loads(line.strip())
                title = product.get('title', '')
                
                # Check if this is a synthetic product
                is_synthetic = any(re.match(pattern, title) for pattern in synthetic_patterns)
                
                if is_synthetic:
                    synthetic_count += 1
                    print(f"⚠️  Synthetic product found at line {line_num}: {title}")
                else:
                    real_products.append(product)
                    
            except json.JSONDecodeError:
                print(f"❌ Error parsing line {line_num}")
                continue
    
    print(f"\n📊 Summary:")
    print(f"  • Real products: {len(real_products)}")
    print(f"  • Synthetic products removed: {synthetic_count}")
    print(f"  • Total products processed: {len(real_products) + synthetic_count}")
    
    # Save clean catalog
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for product in real_products:
            outfile.write(json.dumps(product, ensure_ascii=False) + '\n')
    
    print(f"\n✅ Clean catalog saved to: {output_file}")
    return len(real_products), synthetic_count

if __name__ == "__main__":
    remove_synthetic_products()