import json
import csv
import os

def ndjson_to_csv(ndjson_file_path, csv_file_path):
    """
    Convert NDJSON file to CSV format
    """
    # Read all products from NDJSON
    products = []
    
    with open(ndjson_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                product = json.loads(line)
                products.append(product)
    
    if not products:
        print("No products found in the file")
        return
    
    # Define the CSV columns based on the product structure
    fieldnames = [
        'id',
        'title',
        'availability',
        'description',
        'categories',
        'price',
        'originalPrice',
        'currencyCode',
        'brands',
        'uri',
        'color',
        'features',
        'age_group',
        'sku_code'
    ]
    
    # Write to CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write product data
        for product in products:
            row = {}
            
            # Basic fields
            row['id'] = product.get('id', '')
            row['title'] = product.get('title', '')
            row['availability'] = product.get('availability', '')
            row['description'] = product.get('description', '').replace('\r\n', ' ').replace('\n', ' ')
            
            # Categories (join list with semicolons)
            categories = product.get('categories', [])
            row['categories'] = '; '.join(categories) if categories else ''
            
            # Price information
            price_info = product.get('priceInfo', {})
            row['price'] = price_info.get('price', '')
            row['originalPrice'] = price_info.get('originalPrice', '')
            row['currencyCode'] = price_info.get('currencyCode', '')
            
            # Brands (join list with semicolons)
            brands = product.get('brands', [])
            row['brands'] = '; '.join(brands) if brands else ''
            
            # URI
            row['uri'] = product.get('uri', '')
            
            # Attributes
            attributes = product.get('attributes', {})
            
            # Color
            color_attr = attributes.get('color', {})
            color_list = color_attr.get('text', [])
            row['color'] = '; '.join(color_list) if color_list else ''
            
            # Features
            features_attr = attributes.get('features', {})
            features_list = features_attr.get('text', [])
            row['features'] = '; '.join(features_list) if features_list else ''
            
            # Age group
            age_attr = attributes.get('age_group', {})
            age_list = age_attr.get('text', [])
            row['age_group'] = '; '.join(age_list) if age_list else ''
            
            # SKU code
            sku_attr = attributes.get('sku_code', {})
            sku_list = sku_attr.get('text', [])
            row['sku_code'] = '; '.join(sku_list) if sku_list else ''
            
            writer.writerow(row)
    
    print(f"Successfully converted {len(products)} products to CSV format")
    print(f"CSV file saved as: {csv_file_path}")

if __name__ == "__main__":
    # File paths
    ndjson_file = "product_catalog_final_categories.ndjson"
    csv_file = "product_catalog_final_categories.csv"
    
    # Convert the file
    ndjson_to_csv(ndjson_file, csv_file)