#!/usr/bin/env python3
"""
Enhanced Dabdoob Category Processor
Processes real database category data with visual information and generates Google Cloud Retail API compatible files
"""

import json
import csv
import sys
from pathlib import Path
from datetime import datetime

class DabdoobCategoryProcessor:
    def __init__(self, output_dir="GCP_Import_Ready"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Store category visual information
        self.category_visual_data = {}
        
        # Statistics
        self.stats = {
            'total_products': 0,
            'categories_with_colors': 0,
            'categories_processed': set(),
            'brands_processed': set(),
            'price_range': {'min': float('inf'), 'max': 0},
            'skipped_products': 0
        }

    def load_category_visual_info(self, csv_file="Cat_Info with visuals.csv"):
        """Load category visual information including colors and Arabic names"""
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    category_name = row.get('displayName', '').strip()
                    if category_name:
                        self.category_visual_data[category_name] = {
                            'id': row.get('id', ''),
                            'displayName_ar': row.get('displayName_ar', ''),
                            'backgroundColor': row.get('backgroundColor', ''),
                            'textColor': row.get('textColor', ''),
                            'sortOrder': row.get('sortOrder', ''),
                            'urlSlug': row.get('urlSlug', ''),
                            'categoryHierarchy': row.get('categoryHierarchy', '[]'),
                            'productCount': row.get('productCount', '0')
                        }
                        
                        if row.get('backgroundColor'):
                            self.stats['categories_with_colors'] += 1
                            
            print(f"✅ Loaded visual data for {len(self.category_visual_data)} categories")
            print(f"📊 Categories with colors: {self.stats['categories_with_colors']}")
            
        except FileNotFoundError:
            print(f"⚠️  Category visual file not found: {csv_file}")
        except Exception as e:
            print(f"❌ Error loading category visual data: {e}")

    def clean_and_validate(self, text):
        """Clean and validate text fields"""
        if not text or str(text).strip() in ['', 'NULL', 'None']:
            return None
        return str(text).strip()

    def process_product_catalog_csv(self, csv_file):
        """Process product catalog from CSV export (Query 7 or 12 results)"""
        products = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # Basic product information
                    product_id = self.clean_and_validate(row.get('id'))
                    title = self.clean_and_validate(row.get('title'))
                    sku_id = self.clean_and_validate(row.get('sku_id') or row.get('primary_sku'))
                    
                    if not product_id or not title:
                        self.stats['skipped_products'] += 1
                        continue
                    
                    # Category information
                    category = self.clean_and_validate(row.get('primary_category') or row.get('main_category'))
                    if not category:
                        self.stats['skipped_products'] += 1
                        continue
                        
                    self.stats['categories_processed'].add(category)
                    
                    # Brand information
                    brand = self.clean_and_validate(row.get('brand') or row.get('brand_name')) or 'Misc'
                    self.stats['brands_processed'].add(brand)
                    
                    # Pricing
                    try:
                        price = float(row.get('price') or row.get('current_price') or 0)
                        original_price = float(row.get('originalPrice') or row.get('original_price') or price)
                        
                        if price <= 0:
                            self.stats['skipped_products'] += 1
                            continue
                            
                        self.stats['price_range']['min'] = min(self.stats['price_range']['min'], price)
                        self.stats['price_range']['max'] = max(self.stats['price_range']['max'], price)
                        
                    except (ValueError, TypeError):
                        self.stats['skipped_products'] += 1
                        continue
                    
                    # Availability
                    availability = row.get('availability', 'IN_STOCK')
                    if availability not in ['IN_STOCK', 'OUT_OF_STOCK', 'PREORDER']:
                        availability = 'IN_STOCK'
                    
                    # Description
                    description = self.clean_and_validate(row.get('description'))
                    if not description:
                        description = f"Quality {category} product from Dabdoob"
                    
                    # Product URI
                    uri = self.clean_and_validate(row.get('uri') or row.get('product_url'))
                    if not uri:
                        uri = f"https://dabdoob.com/sku/{product_id}"
                    
                    # Create product record
                    product = {
                        "id": product_id,
                        "title": title,
                        "description": description,
                        "availability": availability,
                        "categories": [category],
                        "priceInfo": {
                            "price": price,
                            "originalPrice": original_price,
                            "currencyCode": "SAR"
                        },
                        "brands": [brand],
                        "uri": uri
                    }
                    
                    # Add enhanced attributes
                    attributes = {}
                    
                    # SKU Code
                    if sku_id:
                        attributes['sku_code'] = {"text": [str(sku_id)]}
                    
                    # Features
                    features = []
                    if row.get('is_wrappable') == '1' or row.get('features') == 'Gift-Wrappable':
                        features.append('Gift-Wrappable')
                    if row.get('is_customizable') == '1':
                        features.append('Customizable')
                    if row.get('is_international') == '1':
                        features.append('International')
                    if features:
                        attributes['features'] = {"text": features}
                    
                    # Category Color (from visual data)
                    if category in self.category_visual_data:
                        visual_info = self.category_visual_data[category]
                        if visual_info['backgroundColor']:
                            attributes['category_color'] = {"text": [visual_info['backgroundColor']]}
                        if visual_info['displayName_ar']:
                            attributes['category_ar'] = {"text": [visual_info['displayName_ar']]}
                    
                    # Origin Country
                    origin = self.clean_and_validate(row.get('origincountry') or row.get('origin_country'))
                    if origin:
                        attributes['origin_country'] = {"text": [origin]}
                    
                    # Add attributes if any exist
                    if attributes:
                        product["attributes"] = attributes
                    
                    products.append(product)
                    self.stats['total_products'] += 1
                    
        except FileNotFoundError:
            print(f"❌ Product file not found: {csv_file}")
            return []
        except Exception as e:
            print(f"❌ Error processing product file: {e}")
            return []
        
        return products

    def generate_enhanced_categories_file(self):
        """Generate categories.ndjson with visual information"""
        categories_file = self.output_dir / "categories_enhanced.ndjson"
        
        try:
            with open(categories_file, 'w', encoding='utf-8') as file:
                for category_name, visual_info in self.category_visual_data.items():
                    if not category_name or category_name == '':
                        continue
                        
                    category_record = {
                        "id": visual_info['id'],
                        "displayName": category_name
                    }
                    
                    # Add hierarchy
                    try:
                        hierarchy = json.loads(visual_info['categoryHierarchy'])
                        category_record["categoryHierarchy"] = hierarchy
                    except:
                        category_record["categoryHierarchy"] = [category_name]
                    
                    # Add visual attributes
                    if visual_info['backgroundColor']:
                        if "attributes" not in category_record:
                            category_record["attributes"] = {}
                        category_record["attributes"]["backgroundColor"] = {"text": [visual_info['backgroundColor']]}
                    
                    if visual_info['displayName_ar']:
                        if "attributes" not in category_record:
                            category_record["attributes"] = {}
                        category_record["attributes"]["displayName_ar"] = {"text": [visual_info['displayName_ar']]}
                    
                    file.write(json.dumps(category_record, ensure_ascii=False) + '\n')
                    
            print(f"✅ Generated enhanced categories file: {categories_file}")
            
        except Exception as e:
            print(f"❌ Error generating categories file: {e}")

    def save_products_to_ndjson(self, products, filename="gcp_retail_products_enhanced.ndjson"):
        """Save products to NDJSON format"""
        if not products:
            print("⚠️  No products to save")
            return
            
        output_file = self.output_dir / filename
        
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                for product in products:
                    file.write(json.dumps(product, ensure_ascii=False) + '\n')
                    
            print(f"✅ Generated product catalog: {output_file}")
            print(f"📊 Total products: {len(products)}")
            
        except Exception as e:
            print(f"❌ Error saving products: {e}")

    def generate_category_summary_report(self):
        """Generate a summary report of categories with visual information"""
        report_file = self.output_dir / "category_visual_summary.md"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as file:
                file.write("# Dabdoob Category Visual Summary\n\n")
                file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                file.write("## Categories with Visual Information\n\n")
                file.write("| ID | Category (EN) | Category (AR) | Color | Product Count |\n")
                file.write("|---|---|---|---|---|\n")
                
                # Sort by product count
                sorted_categories = sorted(
                    self.category_visual_data.items(),
                    key=lambda x: int(x[1]['productCount']) if x[1]['productCount'].isdigit() else 0,
                    reverse=True
                )
                
                for category_name, info in sorted_categories:
                    color_display = info['backgroundColor'] if info['backgroundColor'] else 'No color'
                    file.write(f"| {info['id']} | {category_name} | {info['displayName_ar']} | {color_display} | {info['productCount']} |\n")
                
                file.write(f"\n## Statistics\n\n")
                file.write(f"- Total categories with visual data: {len(self.category_visual_data)}\n")
                file.write(f"- Categories with colors: {self.stats['categories_with_colors']}\n")
                file.write(f"- Products processed: {self.stats['total_products']}\n")
                file.write(f"- Products skipped: {self.stats['skipped_products']}\n")
                
            print(f"✅ Generated category summary report: {report_file}")
            
        except Exception as e:
            print(f"❌ Error generating summary report: {e}")

    def print_processing_statistics(self):
        """Print detailed processing statistics"""
        print("\n" + "="*60)
        print("📈 DABDOOB CATEGORY PROCESSING STATISTICS")
        print("="*60)
        print(f"Total Products Processed: {self.stats['total_products']}")
        print(f"Products Skipped: {self.stats['skipped_products']}")
        print(f"Categories Found: {len(self.stats['categories_processed'])}")
        print(f"Categories with Visual Data: {len(self.category_visual_data)}")
        print(f"Categories with Colors: {self.stats['categories_with_colors']}")
        print(f"Brands Found: {len(self.stats['brands_processed'])}")
        
        if self.stats['price_range']['min'] != float('inf'):
            print(f"Price Range: {self.stats['price_range']['min']:.2f} - {self.stats['price_range']['max']:.2f} SAR")
        
        print(f"\nTop Categories by Product Count:")
        # Sort categories by product count from visual data
        sorted_cats = sorted(
            [(name, info) for name, info in self.category_visual_data.items() if name in self.stats['categories_processed']],
            key=lambda x: int(x[1]['productCount']) if x[1]['productCount'].isdigit() else 0,
            reverse=True
        )
        
        for i, (category, info) in enumerate(sorted_cats[:10], 1):
            color_info = info['backgroundColor'] if info['backgroundColor'] else 'No color'
            print(f"  {i}. {category} - {info['productCount']} products ({color_info})")

def main():
    print("🎨 Enhanced Dabdoob Category Processor with Visual Information")
    print("=" * 65)
    
    processor = DabdoobCategoryProcessor()
    
    # Load category visual information
    visual_files = [
        "Cat_Info with visuals.csv",
        "category_visual_info.csv"
    ]
    
    for visual_file in visual_files:
        if Path(visual_file).exists():
            print(f"📂 Loading category visual data: {visual_file}")
            processor.load_category_visual_info(visual_file)
            break
    else:
        print("⚠️  No category visual data file found. Looking for Cat_Info with visuals.csv")
    
    # Process product catalog
    product_files = [
        "enhanced_product_catalog.csv",
        "product_catalog_export.csv",
        "query7_results.csv",
        "query12_results.csv"
    ]
    
    products = []
    for prod_file in product_files:
        if Path(prod_file).exists():
            print(f"📂 Processing product catalog: {prod_file}")
            products = processor.process_product_catalog_csv(prod_file)
            break
    else:
        print("❌ No product catalog file found. Please export results from Query 7 or 12 as CSV.")
        print("   Expected files: enhanced_product_catalog.csv, query7_results.csv, or query12_results.csv")
        return
    
    if not products:
        print("❌ No products were processed successfully.")
        return
    
    # Generate outputs
    processor.save_products_to_ndjson(products)
    processor.generate_enhanced_categories_file()
    processor.generate_category_summary_report()
    processor.print_processing_statistics()
    
    print(f"\n✅ Enhanced catalog processing complete!")
    print(f"📁 Output files saved to: {processor.output_dir}")
    print(f"🎨 Category visual information included in outputs")

if __name__ == "__main__":
    main()