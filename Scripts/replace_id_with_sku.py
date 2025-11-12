#!/usr/bin/env python3
"""
Replace product ID with SKU ID in product catalog
Replaces the "id" field value with the SKU code from attributes while keeping the same field name
"""

import json
import os

def replace_id_with_sku():
    """Replace product ID with SKU ID in the product catalog"""
    
    # File paths
    input_file = r"Recommendation Engine Demo\product_catalog_final_categories.ndjson"
    output_file = r"Recommendation Engine Demo\product_catalog_final_categories.ndjson"
    backup_file = r"Recommendation Engine Demo\product_catalog_final_categories_backup.ndjson"
    
    # Statistics
    total_products = 0
    updated_products = 0
    skipped_products = 0
    
    print("🔄 Starting ID replacement with SKU codes...")
    print("=" * 80)
    
    # Create backup
    if os.path.exists(input_file):
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(backup_file, 'w', encoding='utf-8') as backupfile:
            backupfile.write(infile.read())
        print(f"✅ Backup created: {backup_file}")
    
    # Process the file
    updated_products_list = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            for line_num, line in enumerate(infile, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    product = json.loads(line)
                    total_products += 1
                    
                    # Get current ID and SKU code
                    current_id = product.get('id', '')
                    sku_code = None
                    
                    # Extract SKU code from attributes
                    if 'attributes' in product and 'sku_code' in product['attributes']:
                        sku_list = product['attributes']['sku_code'].get('text', [])
                        if sku_list and len(sku_list) > 0:
                            sku_code = sku_list[0]  # Take first SKU if multiple
                    
                    if sku_code and sku_code != current_id:
                        # Replace ID with SKU code
                        old_id = product['id']
                        product['id'] = sku_code
                        updated_products += 1
                        
                        # Show progress for first 10 and every 1000th update
                        if updated_products <= 10 or updated_products % 1000 == 0:
                            print(f"Line {line_num}: '{old_id}' → '{sku_code}' for product: {product.get('title', 'Unknown')[:50]}...")
                    
                    elif not sku_code:
                        skipped_products += 1
                        if skipped_products <= 5:
                            print(f"⚠️  Line {line_num}: No SKU code found for product: {product.get('title', 'Unknown')[:50]}...")
                    
                    updated_products_list.append(product)
                    
                except json.JSONDecodeError as e:
                    print(f"❌ Error parsing line {line_num}: {e}")
                    continue
        
        # Write updated products back to file
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for product in updated_products_list:
                json.dump(product, outfile, ensure_ascii=False, separators=(',', ':'))
                outfile.write('\n')
        
        print("=" * 80)
        print("📊 ID REPLACEMENT WITH SKU CODES RESULTS")
        print("=" * 80)
        print(f"Total products processed: {total_products}")
        print(f"Products updated with SKU IDs: {updated_products}")
        print(f"Products skipped (no SKU): {skipped_products}")
        print(f"Products unchanged: {total_products - updated_products - skipped_products}")
        
        if updated_products > 0:
            print(f"\n✅ ID replacement complete!")
            print(f"📁 Updated file: {output_file}")
            print(f"💾 Backup saved: {backup_file}")
        else:
            print(f"\n⚠️  No products were updated")
            
    except FileNotFoundError:
        print(f"❌ Error: File not found: {input_file}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    replace_id_with_sku()