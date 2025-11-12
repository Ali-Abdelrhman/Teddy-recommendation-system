#!/usr/bin/env python3
"""
Remove sku_code and uri fields from product catalog
"""

import json
import os

def clean_catalog():
    """Remove sku_code and uri fields from catalog"""
    
    input_file = r"Recommendation Engine Demo\product_catalog_final_categories.ndjson"
    backup_file = r"Recommendation Engine Demo\product_catalog_final_categories_backup_before_cleanup.ndjson"
    
    # Create backup
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(backup_file, 'w', encoding='utf-8') as backupfile:
        backupfile.write(infile.read())
    
    # Process catalog
    updated_products = []
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            
            product = json.loads(line)
            
            # Remove uri field
            if 'uri' in product:
                del product['uri']
            
            # Remove sku_code from attributes
            if 'attributes' in product and 'sku_code' in product['attributes']:
                del product['attributes']['sku_code']
            
            updated_products.append(product)
    
    # Write cleaned catalog
    with open(input_file, 'w', encoding='utf-8') as outfile:
        for product in updated_products:
            json.dump(product, outfile, ensure_ascii=False, separators=(',', ':'))
            outfile.write('\n')

if __name__ == "__main__":
    clean_catalog()