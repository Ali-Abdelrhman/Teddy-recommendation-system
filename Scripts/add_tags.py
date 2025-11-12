#!/usr/bin/env python3
"""
Add tags field to catalog based on CSV mapping
"""

import json
import csv

def add_tags_to_catalog():
    catalog_file = r"Recommendation Engine Demo\product_catalog_final_categories.ndjson"
    csv_file = r"Test CSVs\sample\samples\_SELECT_p_sku_id_GROUP_CONCAT_t_name_en_ORDER_BY_t_name_en_SEPAR_202510280556.csv"
    
    # Load tags mapping
    tags_mapping = {}
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sku_id = row['sku_id']
            tags = row['tags']
            if tags:
                tags_list = [tag.strip() for tag in tags.split(',')]
                tags_mapping[sku_id] = tags_list
    
    # Process catalog
    updated_products = []
    with open(catalog_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            
            product = json.loads(line)
            product_id = product.get('id', '')
            
            if product_id in tags_mapping:
                product['tags'] = tags_mapping[product_id]
            
            updated_products.append(product)
    
    # Write updated catalog
    with open(catalog_file, 'w', encoding='utf-8') as outfile:
        for product in updated_products:
            json.dump(product, outfile, ensure_ascii=False, separators=(',', ':'))
            outfile.write('\n')

if __name__ == "__main__":
    add_tags_to_catalog()