#!/usr/bin/env python3
"""
Process DBeaver export to add missing SKUs to our product catalog
"""

import json
import csv
import os
from pathlib import Path

def process_dbeaver_export():
    """Process the DBeaver CSV export and add missing products to catalog"""
    
    # Files
    dbeaver_export = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Database\missing_skus_complete.csv"
    current_catalog = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Recommendation Engine Demo\product_catalog_sku_based.ndjson"
    output_catalog = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Recommendation Engine Demo\product_catalog_sku_complete.ndjson"
    
    # Check if DBeaver export exists
    if not os.path.exists(dbeaver_export):
        print(f"❌ DBeaver export not found: {dbeaver_export}")
        print("📋 Instructions:")
        print("1. Run the query in DBeaver")
        print("2. Export results as CSV")
        print("3. Save as 'missing_skus_complete.csv' in the Database folder")
        print("4. Run this script again")
        return False
    
    print("🔍 Loading DBeaver export...")
    
    # Load new SKU data from DBeaver
    new_skus = {}
    
    try:
        with open(dbeaver_export, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    sku_id = row['sku_id']
                    
                    # Create product data
                    product_data = {
                        'sku_id': sku_id,
                        'title': row.get('name_en', f'Product {sku_id}'),
                        'description': row.get('description_en', f'High quality product SKU {sku_id}'),
                        'category_name': row.get('category_name', 'General'),
                        'category_name_ar': row.get('category_name_ar', ''),
                        'parent_category_name': row.get('parent_category_name', ''),
                        'brand_name': row.get('brand_name', 'Unknown'),
                        'price': row.get('price', '0'),
                        'original_price': row.get('original_price', '0'),
                        'currency_code': row.get('currency_code', 'SAR'),
                        'sku_code': row.get('sku_code', ''),
                        'upc': row.get('upc', ''),
                        'slug': row.get('slug', ''),
                        'product_id': row.get('product_id', ''),
                        'category_id': row.get('category_id', ''),
                        'brand_id': row.get('brand_id', ''),
                        'name_ar': row.get('name_ar', ''),
                        'description_ar': row.get('description_ar', '')
                    }
                    
                    new_skus[sku_id] = product_data
                    
                except (ValueError, KeyError) as e:
                    print(f"⚠️  Error processing row: {e}")
                    continue
        
        print(f"✅ Loaded {len(new_skus)} new SKUs from DBeaver export")
        
    except FileNotFoundError:
        print(f"❌ Could not find DBeaver export file")
        return False
    
    # Load existing catalog
    existing_skus = set()
    catalog_products = []
    
    with open(current_catalog, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                product = json.loads(line.strip())
                existing_skus.add(product['id'])
                catalog_products.append(product)
            except json.JSONDecodeError:
                continue
    
    print(f"✅ Loaded {len(catalog_products)} existing products from catalog")
    
    # Create enhanced catalog
    print("🔄 Creating enhanced catalog with new SKUs...")
    
    added_count = 0
    
    with open(output_catalog, 'w', encoding='utf-8') as outfile:
        # Write existing products
        for product in catalog_products:
            outfile.write(json.dumps(product, ensure_ascii=False) + '\n')
        
        # Add new products from DBeaver
        for sku_id, product_data in new_skus.items():
            if sku_id not in existing_skus:
                
                # Create GCP Retail API compatible product
                retail_product = {
                    "id": sku_id,
                    "title": product_data['title'],
                    "description": product_data['description'],
                    "categories": [product_data['category_name']] if product_data['category_name'] else ['General'],
                    "brands": [product_data['brand_name']] if product_data['brand_name'] else ['Unknown'],
                    "availability": "IN_STOCK",
                    "uri": f"https://dabdoob.com/product/{sku_id}",
                    "attributes": {
                        "sku_id": {"text": [sku_id]},
                        "category_id": {"text": [product_data['category_id']]},
                        "product_id": {"text": [product_data['product_id']]},
                        "brand_id": {"text": [product_data['brand_id']]}
                    }
                }
                
                # Add pricing if available
                if product_data['price'] and float(product_data['price']) > 0:
                    retail_product["priceInfo"] = {
                        "price": float(product_data['price']),
                        "currencyCode": product_data['currency_code']
                    }
                    if product_data['original_price'] and float(product_data['original_price']) > 0:
                        retail_product["priceInfo"]["originalPrice"] = float(product_data['original_price'])
                
                # Add optional attributes
                if product_data['category_name_ar']:
                    retail_product["attributes"]["category_name_ar"] = {"text": [product_data['category_name_ar']]}
                
                if product_data['name_ar']:
                    retail_product["attributes"]["name_ar"] = {"text": [product_data['name_ar']]}
                
                if product_data['description_ar']:
                    retail_product["attributes"]["description_ar"] = {"text": [product_data['description_ar']]}
                
                if product_data['sku_code']:
                    retail_product["attributes"]["sku_code"] = {"text": [product_data['sku_code']]}
                
                if product_data['upc']:
                    retail_product["attributes"]["upc"] = {"text": [product_data['upc']]}
                
                if product_data['parent_category_name']:
                    retail_product["attributes"]["parent_category"] = {"text": [product_data['parent_category_name']]}
                
                outfile.write(json.dumps(retail_product, ensure_ascii=False) + '\n')
                added_count += 1
    
    print(f"\n📊 Catalog Enhancement Summary:")
    print(f"  • Existing products: {len(catalog_products):,}")
    print(f"  • New products added: {added_count:,}")
    print(f"  • Total products: {len(catalog_products) + added_count:,}")
    print(f"  📁 Enhanced catalog: {output_catalog}")
    
    # Test coverage improvement
    test_coverage_improvement()
    
    return True

def test_coverage_improvement():
    """Test how much the coverage improved"""
    
    user_events_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\RecommendationAI_NDJSON\user_events_with_sku_ids.ndjson"
    enhanced_catalog = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Recommendation Engine Demo\product_catalog_sku_complete.ndjson"
    
    # Load enhanced catalog SKUs
    catalog_skus = set()
    with open(enhanced_catalog, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                product = json.loads(line.strip())
                catalog_skus.add(product['id'])
            except json.JSONDecodeError:
                continue
    
    # Test coverage
    total_events = 0
    covered_events = 0
    
    with open(user_events_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                event = json.loads(line.strip())
                total_events += 1
                
                event_covered = True
                for product_detail in event.get('productDetails', []):
                    sku_id = product_detail.get('product', {}).get('id', '')
                    if sku_id not in catalog_skus:
                        event_covered = False
                        break
                
                if event_covered:
                    covered_events += 1
                    
            except json.JSONDecodeError:
                continue
    
    coverage_percent = (covered_events / total_events) * 100 if total_events > 0 else 0
    
    print(f"\n🎯 Coverage Improvement Test:")
    print(f"  • Total events: {total_events:,}")
    print(f"  • Covered events: {covered_events:,}")
    print(f"  • New coverage: {coverage_percent:.1f}%")
    print(f"  • Improvement: +{coverage_percent - 24.3:.1f}%")

if __name__ == "__main__":
    process_dbeaver_export()