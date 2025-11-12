#!/usr/bin/env python3
"""
Enhanced Real Category Catalog Generator for Dabdoob
Processes real database extraction results and generates Google Cloud Retail API compatible NDJSON files
Uses SKU IDs as primary identifiers and includes category colors and enhanced attributes
"""

import json
import csv
import sys
from pathlib import Path
from datetime import datetime
import re

class EnhancedRealCatalogGenerator:
    def __init__(self, output_dir="GCP_Import_Ready"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Enhanced category mapping with colors
        self.category_colors = {}
        self.category_hierarchy = {}
        
        # Statistics
        self.stats = {
            'total_products': 0,
            'categories_processed': set(),
            'brands_processed': set(),
            'price_range': {'min': float('inf'), 'max': 0},
            'skipped_products': 0,
            'enhanced_attributes': 0
        }

    def process_category_mapping(self, csv_file_path):
        """Process category mapping with colors and display information"""
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    category_id = row.get('id', '')
                    category_name = row.get('displayName', '')
                    category_color = row.get('backgroundColor', '') or row.get('color', '')
                    hierarchy = row.get('categoryHierarchy', '[]')
                    
                    if category_name:
                        self.category_colors[category_name] = {
                            'color': category_color,
                            'hierarchy': hierarchy,
                            'id': category_id
                        }
                        
            print(f"✅ Loaded {len(self.category_colors)} categories with enhanced information")
            
        except FileNotFoundError:
            print(f"⚠️  Category mapping file not found: {csv_file_path}")
        except Exception as e:
            print(f"❌ Error processing category mapping: {e}")

    def clean_text(self, text):
        """Clean and validate text fields"""
        if not text or text.strip() == '':
            return None
        
        # Remove excessive whitespace and control characters
        text = re.sub(r'\s+', ' ', str(text).strip())
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        return text if len(text) > 0 else None

    def generate_product_id(self, sku_id, product_id=None):
        """Generate consistent product ID using SKU"""
        if sku_id:
            return f"SKU{sku_id}"
        elif product_id:
            return f"PROD{product_id:06d}"
        else:
            return None

    def process_price_info(self, current_price, original_price, currency='SAR'):
        """Process and validate pricing information"""
        try:
            price = float(current_price) if current_price else 0
            orig_price = float(original_price) if original_price else price
            
            if price <= 0:
                return None
                
            self.stats['price_range']['min'] = min(self.stats['price_range']['min'], price)
            self.stats['price_range']['max'] = max(self.stats['price_range']['max'], price)
            
            return {
                "price": price,
                "originalPrice": orig_price,
                "currencyCode": currency
            }
        except (ValueError, TypeError):
            return None

    def generate_enhanced_attributes(self, row):
        """Generate enhanced attributes including category colors and features"""
        attributes = {}
        
        # SKU Code
        if row.get('sku_id') or row.get('primary_sku'):
            sku_id = row.get('sku_id') or row.get('primary_sku')
            attributes['sku_code'] = {"text": [str(sku_id)]}
        
        # Category Color
        category = row.get('primary_category') or row.get('main_category')
        if category and category in self.category_colors:
            color = self.category_colors[category]['color']
            if color:
                attributes['category_color'] = {"text": [color]}
        
        # Features
        features = []
        if row.get('is_wrappable') == '1' or row.get('is_wrappable') == 1:
            features.append('Gift-Wrappable')
        if row.get('is_customizable') == '1' or row.get('is_customizable') == 1:
            features.append('Customizable')
        if row.get('is_international') == '1' or row.get('is_international') == 1:
            features.append('International')
            
        if features:
            attributes['features'] = {"text": features}
        
        # Origin Country
        origin = self.clean_text(row.get('origincountry'))
        if origin:
            attributes['origin_country'] = {"text": [origin]}
        
        # Category Information
        if category:
            attributes['category'] = {"text": [category]}
            
        # Availability Quantity
        available_qty = row.get('available_quantity')
        if available_qty:
            try:
                qty = int(float(available_qty))
                if qty > 0:
                    attributes['stock_level'] = {"text": [f"{qty} available"]}
            except (ValueError, TypeError):
                pass
        
        if attributes:
            self.stats['enhanced_attributes'] += 1
            
        return attributes

    def process_product_catalog(self, csv_file_path):
        """Process the main product catalog from database extraction"""
        products = []
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # Generate product ID (prefer SKU-based)
                    product_id = self.generate_product_id(
                        row.get('sku_id') or row.get('primary_sku'),
                        row.get('product_id') or row.get('id')
                    )
                    
                    if not product_id:
                        self.stats['skipped_products'] += 1
                        continue
                    
                    # Clean title and description
                    title = self.clean_text(row.get('title'))
                    description = self.clean_text(row.get('description'))
                    
                    if not title:
                        self.stats['skipped_products'] += 1
                        continue
                    
                    # Process category information
                    category = self.clean_text(row.get('primary_category') or row.get('main_category'))
                    if not category:
                        self.stats['skipped_products'] += 1
                        continue
                        
                    self.stats['categories_processed'].add(category)
                    
                    # Process brand
                    brand = self.clean_text(row.get('brand') or row.get('brand_name')) or 'Misc'
                    self.stats['brands_processed'].add(brand)
                    
                    # Process pricing
                    price_info = self.process_price_info(
                        row.get('price') or row.get('current_price'),
                        row.get('originalPrice') or row.get('original_price')
                    )
                    
                    if not price_info:
                        self.stats['skipped_products'] += 1
                        continue
                    
                    # Process availability
                    availability = row.get('availability', 'IN_STOCK')
                    if availability not in ['IN_STOCK', 'OUT_OF_STOCK', 'PREORDER']:
                        availability = 'IN_STOCK'
                    
                    # Generate product URI
                    uri = row.get('uri') or row.get('product_url') or f"https://dabdoob.com/sku/{product_id}"
                    
                    # Create product record
                    product = {
                        "id": product_id,
                        "title": title,
                        "availability": availability,
                        "categories": [category],
                        "priceInfo": price_info,
                        "brands": [brand],
                        "uri": uri
                    }
                    
                    # Add description if available
                    if description:
                        product["description"] = description
                    
                    # Add enhanced attributes
                    attributes = self.generate_enhanced_attributes(row)
                    if attributes:
                        product["attributes"] = attributes
                    
                    products.append(product)
                    self.stats['total_products'] += 1
                    
        except FileNotFoundError:
            print(f"❌ Product catalog file not found: {csv_file_path}")
            return []
        except Exception as e:
            print(f"❌ Error processing product catalog: {e}")
            return []
        
        return products

    def generate_categories_file(self):
        """Generate categories.ndjson file from processed category information"""
        categories_file = self.output_dir / "categories_enhanced.ndjson"
        
        try:
            with open(categories_file, 'w', encoding='utf-8') as file:
                for category_name, info in self.category_colors.items():
                    category_record = {
                        "id": info['id'],
                        "displayName": category_name
                    }
                    
                    # Add hierarchy information
                    try:
                        hierarchy = json.loads(info['hierarchy'])
                        if hierarchy:
                            category_record["categoryHierarchy"] = hierarchy
                    except:
                        category_record["categoryHierarchy"] = [category_name]
                    
                    file.write(json.dumps(category_record, ensure_ascii=False) + '\n')
                    
            print(f"✅ Generated enhanced categories file: {categories_file}")
            
        except Exception as e:
            print(f"❌ Error generating categories file: {e}")

    def save_products(self, products, filename="gcp_retail_products_enhanced.ndjson"):
        """Save products to NDJSON file"""
        if not products:
            print("⚠️  No products to save")
            return
            
        output_file = self.output_dir / filename
        
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                for product in products:
                    file.write(json.dumps(product, ensure_ascii=False) + '\n')
                    
            print(f"✅ Generated enhanced product catalog: {output_file}")
            print(f"📊 Total products: {len(products)}")
            
        except Exception as e:
            print(f"❌ Error saving products: {e}")

    def print_statistics(self):
        """Print processing statistics"""
        print("\n" + "="*60)
        print("📈 ENHANCED CATALOG GENERATION STATISTICS")
        print("="*60)
        print(f"Total Products Processed: {self.stats['total_products']}")
        print(f"Products Skipped: {self.stats['skipped_products']}")
        print(f"Categories Found: {len(self.stats['categories_processed'])}")
        print(f"Brands Found: {len(self.stats['brands_processed'])}")
        print(f"Enhanced Attributes: {self.stats['enhanced_attributes']}")
        
        if self.stats['price_range']['min'] != float('inf'):
            print(f"Price Range: {self.stats['price_range']['min']:.2f} - {self.stats['price_range']['max']:.2f} SAR")
        
        print(f"\nTop Categories by Name:")
        for i, category in enumerate(sorted(self.stats['categories_processed'])[:10], 1):
            color_info = self.category_colors.get(category, {}).get('color', 'No color')
            print(f"  {i}. {category} ({color_info})")
            
        print(f"\nTop Brands:")
        for i, brand in enumerate(sorted(self.stats['brands_processed'])[:10], 1):
            print(f"  {i}. {brand}")

def main():
    print("🚀 Enhanced Real Category Catalog Generator for Dabdoob")
    print("=" * 60)
    
    generator = EnhancedRealCatalogGenerator()
    
    # Process category mapping (if available)
    category_files = [
        "enhanced_category_mapping.csv",
        "category_mapping.csv", 
        "Cat mapping.csv"
    ]
    
    for cat_file in category_files:
        if Path(cat_file).exists():
            print(f"📂 Processing category mapping: {cat_file}")
            generator.process_category_mapping(cat_file)
            break
    
    # Process main product catalog
    product_files = [
        "enhanced_product_catalog.csv",
        "product_catalog_real.csv",
        "all prod with cat info.csv"
    ]
    
    products = []
    for prod_file in product_files:
        if Path(prod_file).exists():
            print(f"📂 Processing product catalog: {prod_file}")
            products = generator.process_product_catalog(prod_file)
            break
    
    if not products:
        print("❌ No product files found. Please ensure you have:")
        print("   - enhanced_product_catalog.csv (from Query 12)")
        print("   - enhanced_category_mapping.csv (from Query 11)")
        return
    
    # Generate outputs
    generator.save_products(products)
    generator.generate_categories_file()
    generator.print_statistics()
    
    print(f"\n✅ Enhanced catalog generation complete!")
    print(f"📁 Output files saved to: {generator.output_dir}")

if __name__ == "__main__":
    main()