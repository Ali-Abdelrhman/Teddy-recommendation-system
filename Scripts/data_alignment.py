#!/usr/bin/env python3
"""
Data Alignment and Preprocessing Script
======================================
This script provides options to align products and user events data for Google Cloud import.
Two approaches: Filter events to match existing products OR Create minimal product entries.
"""

import json
import os
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataAligner:
    """Aligns products and user events data for Google Cloud compatibility."""
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.ndjson_path = os.path.join(base_path, "RecommendationAI_NDJSON")
        
        self.existing_products = set()
        self.event_products = set()
        self.filtered_events = []
        self.stats = {
            'original_events': 0,
            'filtered_events': 0,
            'missing_products': 0,
            'existing_products': 0
        }
    
    def load_existing_products(self):
        """Load existing product IDs from products.ndjson."""
        products_file = os.path.join(self.ndjson_path, "products.ndjson")
        
        logger.info("Loading existing product IDs...")
        
        with open(products_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        product = json.loads(line)
                        product_id = product.get('id')
                        if product_id:
                            self.existing_products.add(product_id)
                    except json.JSONDecodeError:
                        continue
        
        self.stats['existing_products'] = len(self.existing_products)
        logger.info(f"Loaded {len(self.existing_products)} existing products")
    
    def filter_events_to_existing_products(self):
        """Filter user events to only include products that exist in catalog."""
        events_file = os.path.join(self.ndjson_path, "user_events_combined.ndjson")
        
        logger.info("Filtering events to match existing products...")
        
        with open(events_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    event = json.loads(line)
                    self.stats['original_events'] += 1
                    
                    # Check if event has product details
                    product_details = event.get('productEventDetail', {}).get('productDetails', [])
                    
                    if not product_details:
                        # Events without products (like home-page-view) are always included
                        self.filtered_events.append(event)
                        self.stats['filtered_events'] += 1
                    else:
                        # Check if all products in the event exist in catalog
                        all_products_exist = True
                        for detail in product_details:
                            product_id = detail.get('product', {}).get('id')
                            if product_id and product_id not in self.existing_products:
                                all_products_exist = False
                                self.event_products.add(product_id)
                                break
                        
                        if all_products_exist:
                            self.filtered_events.append(event)
                            self.stats['filtered_events'] += 1
                
                except json.JSONDecodeError:
                    continue
        
        self.stats['missing_products'] = len(self.event_products)
        logger.info(f"Filtered {self.stats['filtered_events']} events from {self.stats['original_events']}")
        logger.info(f"Found {self.stats['missing_products']} unique missing products")
    
    def save_filtered_events(self, filename: str = "user_events_filtered.ndjson"):
        """Save filtered events to new file."""
        output_file = os.path.join(self.ndjson_path, filename)
        
        logger.info(f"Saving {len(self.filtered_events)} filtered events...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for event in self.filtered_events:
                f.write(json.dumps(event, ensure_ascii=False) + '\n')
        
        logger.info(f"Saved filtered events to: {output_file}")
        return output_file
    
    def create_minimal_products_for_missing(self):
        """Create minimal product entries for missing products."""
        logger.info("Creating minimal product entries for missing products...")
        
        # Load existing products file content
        products_file = os.path.join(self.ndjson_path, "products.ndjson")
        expanded_products_file = os.path.join(self.ndjson_path, "products_expanded.ndjson")
        
        # Copy existing products
        existing_products = []
        with open(products_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    existing_products.append(line)
        
        # Create minimal entries for missing products
        minimal_products = []
        for i, product_id in enumerate(sorted(self.event_products), 1):
            minimal_product = {
                "id": product_id,
                "type": "PRIMARY",
                "primaryProductId": product_id,
                "categories": ["General"],
                "title": f"Product {product_id[4:]}",  # Remove PROD prefix for title
                "description": f"Auto-generated product entry for {product_id}",
                "languageCode": "en",
                "brands": ["Unknown"],
                "uri": f"https://dabdoob.com/product/{product_id.lower()}/",
                "availability": "IN_STOCK",
                "attributes": {
                    "auto_generated": {"text": ["true"]},
                    "sku_code": {"text": [product_id]}
                },
                "images": []
            }
            minimal_products.append(json.dumps(minimal_product, ensure_ascii=False))
        
        # Save expanded products file
        with open(expanded_products_file, 'w', encoding='utf-8') as f:
            # Write existing products
            for product_line in existing_products:
                f.write(product_line + '\n')
            
            # Write minimal products
            for product_line in minimal_products:
                f.write(product_line + '\n')
        
        logger.info(f"Created {len(minimal_products)} minimal product entries")
        logger.info(f"Expanded products saved to: {expanded_products_file}")
        return expanded_products_file
    
    def generate_alignment_report(self, approach: str, output_files: list):
        """Generate data alignment report."""
        
        if approach == "filter":
            retention_rate = (self.stats['filtered_events'] / self.stats['original_events']) * 100
            status = "✅ READY FOR IMPORT" if retention_rate > 70 else "⚠️ LOW DATA RETENTION"
        else:
            retention_rate = 100.0
            status = "✅ READY FOR IMPORT"
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           DATA ALIGNMENT REPORT                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║ 📊 ALIGNMENT STATISTICS                                                      ║
║ ══════════════════════                                                       ║
║ Approach Used:                   {approach.upper():<20}                           ║
║ Original Events:                 {self.stats['original_events']:>15,}                          ║
║ Final Events:                    {self.stats['filtered_events']:>15,}                          ║
║ Data Retention:                  {retention_rate:>14.1f}%                          ║
║ Existing Products:               {self.stats['existing_products']:>15,}                          ║
║ Missing Products:                {self.stats['missing_products']:>15,}                          ║
║                                                                              ║
║ 📁 OUTPUT FILES                                                              ║
║ ══════════════                                                               ║"""

        for i, file_path in enumerate(output_files, 1):
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / (1024*1024)
            report += f"\n║ {i}. {file_name:<40} ({file_size:>5.1f} MB)               ║"

        report += f"""
║                                                                              ║
║ 🎯 IMPORT STATUS                                                             ║
║ ═══════════════                                                              ║
║ {status:<60} ║
║                                                                              ║
║ 🚀 NEXT STEPS                                                                ║
║ ═════════════                                                                ║"""

        if approach == "filter":
            report += """
║ 1. Use user_events_filtered.ndjson for import                               ║
║ 2. Upload filtered events to Google Cloud Storage                           ║
║ 3. Import using existing products.ndjson catalog                            ║"""
        else:
            report += """
║ 1. Use products_expanded.ndjson as your catalog                             ║
║ 2. Use user_events_combined.ndjson for events                               ║
║ 3. Upload both files to Google Cloud Storage                                ║"""

        report += f"""
║                                                                              ║
║ 📋 GOOGLE CLOUD COMMANDS                                                     ║
║ ════════════════════════                                                     ║
║ # Upload files                                                               ║
║ gsutil cp *.ndjson gs://your-bucket/                                         ║
║                                                                              ║
║ # Import products                                                            ║
║ gcloud retail products import \\                                             ║
║   --project=teddy-demo-2025 \\                                               ║
║   --location=global \\                                                       ║
║   --catalog=default_catalog \\                                               ║
║   --data-file="gs://your-bucket/products{"_expanded" if approach == "expand" else ""}.ndjson"                     ║
║                                                                              ║
║ # Import user events                                                         ║
║ gcloud retail user-events import \\                                          ║
║   --project=teddy-demo-2025 \\                                               ║
║   --location=global \\                                                       ║
║   --catalog=default_catalog \\                                               ║
║   --data-file="gs://your-bucket/user_events_{"filtered" if approach == "filter" else "combined"}.ndjson"          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return report
    
    def approach_filter_events(self):
        """Approach 1: Filter events to match existing products."""
        logger.info("=== APPROACH 1: FILTER EVENTS ===")
        
        self.load_existing_products()
        self.filter_events_to_existing_products()
        
        output_file = self.save_filtered_events()
        
        report = self.generate_alignment_report("filter", [output_file])
        
        # Save report
        report_file = os.path.join(self.ndjson_path, "data_alignment_filter_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(report)
        return output_file
    
    def approach_expand_products(self):
        """Approach 2: Create minimal products for missing items."""
        logger.info("=== APPROACH 2: EXPAND PRODUCTS ===")
        
        self.load_existing_products()
        
        # Get all products from events
        events_file = os.path.join(self.ndjson_path, "user_events_combined.ndjson")
        
        with open(events_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    event = json.loads(line)
                    self.stats['original_events'] += 1
                    
                    product_details = event.get('productEventDetail', {}).get('productDetails', [])
                    for detail in product_details:
                        product_id = detail.get('product', {}).get('id')
                        if product_id and product_id not in self.existing_products:
                            self.event_products.add(product_id)
                
                except json.JSONDecodeError:
                    continue
        
        self.stats['filtered_events'] = self.stats['original_events']  # All events kept
        self.stats['missing_products'] = len(self.event_products)
        
        expanded_products_file = self.create_minimal_products_for_missing()
        
        report = self.generate_alignment_report("expand", [expanded_products_file])
        
        # Save report
        report_file = os.path.join(self.ndjson_path, "data_alignment_expand_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(report)
        return expanded_products_file

def main():
    """Main function with user choice."""
    base_path = r"c:\Users\Ahmed\Downloads\Teddy recommendation system"
    aligner = DataAligner(base_path)
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        DATA ALIGNMENT OPTIONS                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║ You have 16,876 missing products referenced in events but not in catalog.   ║
║ Choose your approach:                                                        ║
║                                                                              ║
║ 1. FILTER EVENTS (Recommended for immediate import)                         ║
║    - Keep only events for products that exist in catalog                    ║
║    - Results in fewer events but guaranteed compatibility                    ║
║    - Ready for immediate Google Cloud import                                ║
║                                                                              ║
║ 2. EXPAND PRODUCTS (Recommended for maximum data retention)                 ║
║    - Create minimal product entries for missing products                    ║
║    - Keep all events, expand catalog to match                               ║
║    - Better for comprehensive recommendations                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    choice = input("Enter your choice (1 for Filter, 2 for Expand): ").strip()
    
    if choice == "1":
        print("\n🔄 Processing with FILTER EVENTS approach...")
        aligner.approach_filter_events()
        print("\n✅ Filter approach completed!")
        
    elif choice == "2":
        print("\n🔄 Processing with EXPAND PRODUCTS approach...")
        aligner.approach_expand_products()
        print("\n✅ Expand approach completed!")
        
    else:
        print("Invalid choice. Running both approaches for comparison...")
        print("\n🔄 Running Filter approach...")
        aligner.approach_filter_events()
        
        # Reset for second approach
        aligner.event_products = set()
        aligner.filtered_events = []
        aligner.stats = {'original_events': 0, 'filtered_events': 0, 'missing_products': 0, 'existing_products': len(aligner.existing_products)}
        
        print("\n🔄 Running Expand approach...")
        aligner.approach_expand_products()
        
        print("\n✅ Both approaches completed! Check the reports to decide which to use.")

if __name__ == "__main__":
    main()