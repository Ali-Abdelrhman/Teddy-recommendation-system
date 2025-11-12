#!/usr/bin/env python3
"""
Products and User Events Compatibility Analysis
==============================================
This script analyzes the compatibility between products.ndjson and user_events_combined.ndjson
to ensure they're properly aligned for Google Cloud Recommendation AI import.
"""

import json
import os
from collections import Counter, defaultdict
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CompatibilityAnalyzer:
    """Analyzes compatibility between products and user events files."""
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.ndjson_path = os.path.join(base_path, "RecommendationAI_NDJSON")
        
        # Analysis results
        self.products = {}
        self.user_events_products = set()
        self.stats = {
            'products_count': 0,
            'events_count': 0,
            'events_with_products': 0,
            'unique_event_products': 0,
            'matched_products': 0,
            'missing_products': set(),
            'orphaned_products': set(),
            'category_coverage': defaultdict(int),
            'brand_coverage': defaultdict(int),
            'product_popularity': Counter(),
            'issues': []
        }
    
    def load_products_file(self) -> bool:
        """Load and analyze the products.ndjson file."""
        products_file = os.path.join(self.ndjson_path, "products.ndjson")
        
        if not os.path.exists(products_file):
            logger.error(f"Products file not found: {products_file}")
            return False
        
        logger.info(f"Loading products from {products_file}")
        
        try:
            with open(products_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        product = json.loads(line)
                        product_id = product.get('id')
                        
                        if not product_id:
                            self.stats['issues'].append(f"Products line {line_num}: Missing product ID")
                            continue
                        
                        self.products[product_id] = product
                        self.stats['products_count'] += 1
                        
                        # Analyze categories
                        categories = product.get('categories', [])
                        for category in categories:
                            self.stats['category_coverage'][category] += 1
                        
                        # Analyze brands
                        brands = product.get('brands', [])
                        for brand in brands:
                            self.stats['brand_coverage'][brand] += 1
                            
                    except json.JSONDecodeError as e:
                        self.stats['issues'].append(f"Products line {line_num}: Invalid JSON - {e}")
                    except Exception as e:
                        self.stats['issues'].append(f"Products line {line_num}: Error - {e}")
        
        except Exception as e:
            logger.error(f"Error reading products file: {e}")
            return False
        
        logger.info(f"Loaded {self.stats['products_count']} products")
        return True
    
    def analyze_user_events_file(self) -> bool:
        """Analyze the user_events_combined.ndjson file for product references."""
        events_file = os.path.join(self.ndjson_path, "user_events_combined.ndjson")
        
        if not os.path.exists(events_file):
            logger.error(f"User events file not found: {events_file}")
            return False
        
        logger.info(f"Analyzing user events from {events_file}")
        
        try:
            with open(events_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        event = json.loads(line)
                        self.stats['events_count'] += 1
                        
                        # Extract product IDs from events
                        product_details = event.get('productEventDetail', {}).get('productDetails', [])
                        
                        if product_details:
                            self.stats['events_with_products'] += 1
                            
                            for detail in product_details:
                                product_id = detail.get('product', {}).get('id')
                                if product_id:
                                    self.user_events_products.add(product_id)
                                    self.stats['product_popularity'][product_id] += 1
                        
                        # Progress reporting
                        if self.stats['events_count'] % 10000 == 0:
                            logger.info(f"Processed {self.stats['events_count']:,} events...")
                            
                    except json.JSONDecodeError as e:
                        self.stats['issues'].append(f"Events line {line_num}: Invalid JSON - {e}")
                    except Exception as e:
                        self.stats['issues'].append(f"Events line {line_num}: Error - {e}")
        
        except Exception as e:
            logger.error(f"Error reading user events file: {e}")
            return False
        
        self.stats['unique_event_products'] = len(self.user_events_products)
        logger.info(f"Found {self.stats['unique_event_products']} unique products in {self.stats['events_count']} events")
        return True
    
    def perform_compatibility_analysis(self):
        """Perform cross-reference analysis between products and events."""
        logger.info("Performing compatibility analysis...")
        
        # Find products referenced in events but missing from products file
        products_set = set(self.products.keys())
        self.stats['missing_products'] = self.user_events_products - products_set
        
        # Find products in catalog but never referenced in events
        self.stats['orphaned_products'] = products_set - self.user_events_products
        
        # Count matched products
        self.stats['matched_products'] = len(self.user_events_products & products_set)
        
        logger.info(f"Compatibility analysis complete:")
        logger.info(f"  - Products in catalog: {len(products_set):,}")
        logger.info(f"  - Products in events: {len(self.user_events_products):,}")
        logger.info(f"  - Matched products: {self.stats['matched_products']:,}")
        logger.info(f"  - Missing products: {len(self.stats['missing_products']):,}")
        logger.info(f"  - Orphaned products: {len(self.stats['orphaned_products']):,}")
    
    def validate_product_data_quality(self):
        """Validate the quality of product data."""
        logger.info("Validating product data quality...")
        
        quality_issues = []
        
        for product_id, product in self.products.items():
            # Check required fields
            required_fields = ['id', 'title', 'categories', 'availability']
            for field in required_fields:
                if field not in product or not product[field]:
                    quality_issues.append(f"Product {product_id}: Missing or empty '{field}'")
            
            # Check title length
            title = product.get('title', '')
            if len(title) < 10:
                quality_issues.append(f"Product {product_id}: Title too short ('{title}')")
            elif len(title) > 200:
                quality_issues.append(f"Product {product_id}: Title too long ({len(title)} chars)")
            
            # Check categories
            categories = product.get('categories', [])
            if not categories:
                quality_issues.append(f"Product {product_id}: No categories assigned")
            
            # Check images
            images = product.get('images', [])
            if not images:
                quality_issues.append(f"Product {product_id}: No images provided")
            
            # Check availability
            availability = product.get('availability', '')
            valid_availability = ['IN_STOCK', 'OUT_OF_STOCK', 'PREORDER', 'BACKORDER']
            if availability not in valid_availability:
                quality_issues.append(f"Product {product_id}: Invalid availability '{availability}'")
        
        self.stats['quality_issues'] = quality_issues[:100]  # Limit to first 100 issues
        logger.info(f"Found {len(quality_issues)} product quality issues")
    
    def generate_compatibility_report(self) -> str:
        """Generate comprehensive compatibility report."""
        
        # Calculate percentages
        if self.stats['unique_event_products'] > 0:
            match_percentage = (self.stats['matched_products'] / self.stats['unique_event_products']) * 100
        else:
            match_percentage = 0
        
        if self.stats['products_count'] > 0:
            orphan_percentage = (len(self.stats['orphaned_products']) / self.stats['products_count']) * 100
        else:
            orphan_percentage = 0
        
        # Determine overall compatibility status
        if len(self.stats['missing_products']) == 0 and len(self.stats['quality_issues']) < 10:
            status = "✅ EXCELLENT COMPATIBILITY"
            color = "🟢"
        elif len(self.stats['missing_products']) < 100 and len(self.stats['quality_issues']) < 50:
            status = "🟡 GOOD COMPATIBILITY - MINOR ISSUES"
            color = "🟡"
        else:
            status = "🔴 COMPATIBILITY ISSUES FOUND"
            color = "🔴"
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PRODUCTS & USER EVENTS COMPATIBILITY ANALYSIS             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║ 📊 FILE OVERVIEW                                                             ║
║ ═══════════════                                                              ║
║ Products in Catalog:             {self.stats['products_count']:>15,}                          ║
║ Total User Events:               {self.stats['events_count']:>15,}                          ║
║ Events with Products:            {self.stats['events_with_products']:>15,}                          ║
║ Unique Products in Events:       {self.stats['unique_event_products']:>15,}                          ║
║                                                                              ║
║ 🔗 COMPATIBILITY ANALYSIS                                                    ║
║ ══════════════════════════                                                   ║
║ Matched Products:                {self.stats['matched_products']:>10,} ({match_percentage:>5.1f}%)                    ║
║ Missing Products:                {len(self.stats['missing_products']):>10,}                          ║
║ Orphaned Products:               {len(self.stats['orphaned_products']):>10,} ({orphan_percentage:>5.1f}%)                    ║
║                                                                              ║"""

        # Add missing products section
        if self.stats['missing_products']:
            report += """
║ ⚠️  MISSING PRODUCTS (Referenced in events but not in catalog)               ║
║ ═══════════════════════════════════════════════════════════════              ║"""
            for i, product_id in enumerate(list(self.stats['missing_products'])[:10]):
                count = self.stats['product_popularity'][product_id]
                report += f"\n║ {product_id:<20} (Referenced {count:>3} times)                         ║"
            if len(self.stats['missing_products']) > 10:
                report += f"\n║ ... and {len(self.stats['missing_products']) - 10} more missing products                                ║"
        
        # Add most popular products
        report += """
║                                                                              ║
║ 🔥 TOP 10 MOST REFERENCED PRODUCTS                                          ║
║ ═══════════════════════════════════                                          ║"""
        
        for product_id, count in self.stats['product_popularity'].most_common(10):
            status_symbol = "✅" if product_id in self.products else "❌"
            product_name = self.products.get(product_id, {}).get('title', 'MISSING FROM CATALOG')[:30]
            report += f"\n║ {status_symbol} {product_id:<15} {count:>4}x - {product_name:<25} ║"
        
        # Add category analysis
        report += """
║                                                                              ║
║ 📂 CATEGORY DISTRIBUTION                                                     ║
║ ═══════════════════════                                                      ║"""
        
        for category, count in Counter(self.stats['category_coverage']).most_common(10):
            report += f"\n║ {category:<30} {count:>10,} products                      ║"
        
        # Add quality issues if any
        if self.stats.get('quality_issues'):
            report += """
║                                                                              ║
║ ⚠️  PRODUCT QUALITY ISSUES                                                   ║
║ ═══════════════════════════                                                  ║"""
            for issue in self.stats['quality_issues'][:10]:
                report += f"\n║ {issue[:76]:<76} ║"
            if len(self.stats['quality_issues']) > 10:
                report += f"\n║ ... and {len(self.stats['quality_issues']) - 10} more quality issues                                    ║"
        
        # Final status
        report += f"""
║                                                                              ║
║ 🎯 OVERALL COMPATIBILITY STATUS                                             ║
║ ═══════════════════════════════                                              ║
║ {color} {status:<61} ║
║                                                                              ║"""

        # Recommendations
        recommendations = []
        
        if self.stats['missing_products']:
            recommendations.append("Add missing products to catalog before import")
        
        if len(self.stats['orphaned_products']) > self.stats['products_count'] * 0.5:
            recommendations.append("Consider generating more user events for better coverage")
        
        if self.stats.get('quality_issues'):
            recommendations.append("Fix product data quality issues")
        
        if not recommendations:
            recommendations.append("Files are ready for Google Cloud import!")
        
        report += """
║ 📋 RECOMMENDATIONS                                                           ║
║ ═══════════════════                                                          ║"""
        
        for i, rec in enumerate(recommendations[:5], 1):
            report += f"\n║ {i}. {rec:<73} ║"
        
        report += """
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        
        return report
    
    def analyze(self):
        """Main analysis function."""
        try:
            logger.info("Starting products and user events compatibility analysis...")
            
            # Load products file
            if not self.load_products_file():
                return False
            
            # Analyze user events
            if not self.analyze_user_events_file():
                return False
            
            # Perform compatibility analysis
            self.perform_compatibility_analysis()
            
            # Validate product data quality
            self.validate_product_data_quality()
            
            # Generate report
            report = self.generate_compatibility_report()
            
            # Save report
            report_file = os.path.join(self.ndjson_path, "compatibility_analysis.txt")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            # Display report
            print(report)
            
            logger.info(f"Analysis complete! Report saved to: {report_file}")
            
            # Return analysis results
            return {
                'compatible': len(self.stats['missing_products']) == 0,
                'missing_products': len(self.stats['missing_products']),
                'quality_issues': len(self.stats.get('quality_issues', [])),
                'match_percentage': (self.stats['matched_products'] / max(self.stats['unique_event_products'], 1)) * 100
            }
            
        except Exception as e:
            logger.error(f"❌ Error during analysis: {e}")
            return False

def main():
    """Main function to run the compatibility analysis."""
    base_path = r"c:\Users\Ahmed\Downloads\Teddy recommendation system"
    
    analyzer = CompatibilityAnalyzer(base_path)
    results = analyzer.analyze()
    
    if results:
        if results['compatible']:
            print(f"\n🎉 Compatibility analysis complete! Files are ready for Google Cloud import.")
        else:
            print(f"\n⚠️  Found {results['missing_products']} missing products and {results['quality_issues']} quality issues.")
            print("Review the analysis report for detailed recommendations.")

if __name__ == "__main__":
    main()