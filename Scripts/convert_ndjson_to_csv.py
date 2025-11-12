#!/usr/bin/env python3
"""
Convert NDJSON catalog to CSV with no data loss and null filling
"""

import json
import csv
import pandas as pd
from collections import defaultdict

def convert_ndjson_to_csv():
    ndjson_file = r"Recommendation Engine Demo\product_catalog_final_categories.ndjson"
    csv_file = r"Recommendation Engine Demo\product_catalog_final_categories.csv"
    
    # Collect all possible fields
    all_fields = set()
    products = []
    
    # First pass: collect all fields
    with open(ndjson_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                product = json.loads(line)
                products.append(product)
                
                def collect_fields(obj, prefix=''):
                    for key, value in obj.items():
                        field_name = f"{prefix}{key}" if prefix else key
                        all_fields.add(field_name)
                        
                        if isinstance(value, dict):
                            collect_fields(value, f"{field_name}_")
                        elif isinstance(value, list) and value and isinstance(value[0], dict):
                            for item in value:
                                if isinstance(item, dict):
                                    collect_fields(item, f"{field_name}_")
                
                collect_fields(product)
    
    # Flatten products
    flattened_products = []
    for product in products:
        flat_product = {}
        
        def flatten(obj, prefix=''):
            for key, value in obj.items():
                field_name = f"{prefix}{key}" if prefix else key
                
                if isinstance(value, dict):
                    flatten(value, f"{field_name}_")
                elif isinstance(value, list):
                    if value and isinstance(value[0], str):
                        flat_product[field_name] = '; '.join(value)
                    elif value and isinstance(value[0], dict):
                        for i, item in enumerate(value):
                            if isinstance(item, dict):
                                flatten(item, f"{field_name}_{i}_")
                    else:
                        flat_product[field_name] = str(value)
                else:
                    flat_product[field_name] = value
        
        flatten(product)
        flattened_products.append(flat_product)
    
    # Create DataFrame
    df = pd.DataFrame(flattened_products)
    
    # Fill null values
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('')
        else:
            df[col] = df[col].fillna(0)
    
    # Save to CSV
    df.to_csv(csv_file, index=False, encoding='utf-8')

if __name__ == "__main__":
    convert_ndjson_to_csv()