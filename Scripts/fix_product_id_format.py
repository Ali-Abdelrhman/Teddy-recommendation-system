#!/usr/bin/env python3
"""
Fix the ID format mismatch by converting real product IDs to PROD format
"""

import json

def fix_product_id_format():
    """Convert real product IDs from numeric to PROD format to match user events"""
    
    input_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Recommendation Engine Demo\product_catalog_real_only.ndjson"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Recommendation Engine Demo\product_catalog_real_with_prod_ids.ndjson"
    
    print("🔄 Converting product IDs to PROD format...")
    
    converted_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            try:
                product = json.loads(line.strip())
                
                # Convert numeric ID to PROD format
                original_id = product['id']
                product_id_number = int(original_id)
                product['id'] = f"PROD{product_id_number:06d}"  # Format as PROD000123
                
                outfile.write(json.dumps(product, ensure_ascii=False) + '\n')
                converted_count += 1
                
                if converted_count <= 5:
                    print(f"  • {original_id} → {product['id']}")
                    
            except (json.JSONDecodeError, ValueError, KeyError):
                continue
    
    print(f"\n✅ Converted {converted_count} products to PROD format")
    print(f"📁 Output saved to: {output_file}")
    
    return converted_count

if __name__ == "__main__":
    fix_product_id_format()