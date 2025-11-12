#!/usr/bin/env python3
"""
Database-Driven Category Validation and Update Script
Uses actual database categories from CSV files to validate and update product categories
"""

import json
import csv
from pathlib import Path

def load_database_categories():
    """Load real categories from database CSV files"""
    database_categories = set()
    
    # Load from Cat mapping.csv (real database categories)
    cat_mapping_file = Path("Test CSVs/sample/samples/Cat mapping.csv")
    if cat_mapping_file.exists():
        with open(cat_mapping_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                category_name = row.get('displayName', '').strip()
                if category_name:
                    database_categories.add(category_name)
        print(f"✅ Loaded {len(database_categories)} real database categories")
    else:
        print("❌ Cat mapping.csv not found")
        return set()
    
    return database_categories

def find_best_category_match(invalid_category, database_categories):
    """Find the best matching database category for an invalid category"""
    
    # Manual mappings for common mismatches
    manual_mappings = {
        # Character/Hero related
        "Characters & Heroes": "Characters & Heroes",  # This one should be valid
        "Character Toys": "Characters & Heroes",
        "Hero Figures": "Characters & Heroes",
        "Marvel Characters": "Characters & Heroes",
        
        # Vehicle related  
        "Vehicle Toys": "Cars & Vehicles",
        "Car Toys": "Cars & Vehicles",
        "Transport Toys": "Cars & Vehicles",
        
        # Doll related
        "Fashion Dolls": "Dolls & Collectables",
        "Baby Dolls": "Dolls & Collectables",
        "Doll Accessories": "Dolls & Collectables",
        
        # Building/Construction
        "Building Toys": "Construction",
        "LEGO Sets": "Construction",
        "Block Sets": "Construction",
        
        # Educational
        "Learning Toys": "Educational Toys",
        "STEM Toys": "Educational Toys",
        "Science Toys": "Educational Toys",
        
        # Arts and Crafts
        "Craft Kits": "Arts & Crafts",
        "Art Supplies": "Arts & Crafts",
        "Creative Toys": "Arts & Crafts",
        
        # Gaming
        "Puzzle Games": "Puzzles",
        "Card Games": "Board Games",
        "Strategy Games": "Board Games",
        
        # Outdoor
        "Playground Equipment": "Outdoor Toys",
        "Garden Toys": "Outdoor Toys",
        "Beach Toys": "Water Activities",
        
        # Action
        "Action Toys": "Guns & Action Toys",
        "Battle Toys": "Guns & Action Toys",
        "War Games": "Guns & Action Toys",
        
        # Babies
        "Baby Toys": "Babies",
        "Infant Toys": "Babies",
        "Newborn Items": "Babies",
        
        # Pre-school
        "Toddler Toys": "Pre-School",
        "Early Learning": "Pre-School",
        
        # Animals
        "Pet Toys": "Animal Figures",
        "Zoo Animals": "Animal Figures",
        "Farm Animals": "Animal Figures",
        
        # Sports
        "Sporting Goods": "Sports",
        "Exercise Toys": "Sports",
        "Athletic Equipment": "Sports",
        
        # Fashion
        "Accessories": "Fashion & Cosmetics",
        "Jewelry": "Fashion & Cosmetics",
        "Makeup": "Fashion & Cosmetics",
        
        # School
        "School Items": "School Supplies",
        "Stationery": "School Supplies",
        "Educational Supplies": "School Supplies",
    }
    
    # Check manual mappings first
    if invalid_category in manual_mappings:
        return manual_mappings[invalid_category]
    
    # Try partial string matching
    invalid_lower = invalid_category.lower()
    
    for db_category in database_categories:
        db_lower = db_category.lower()
        
        # Check if invalid category contains database category name
        if db_lower in invalid_lower or invalid_lower in db_lower:
            return db_category
        
        # Check for common word matches
        invalid_words = set(invalid_lower.replace('&', ' ').replace(',', ' ').split())
        db_words = set(db_lower.replace('&', ' ').replace(',', ' ').split())
        
        # If more than half the words match, consider it a match
        common_words = invalid_words.intersection(db_words)
        if len(common_words) > 0 and len(common_words) >= len(invalid_words) * 0.5:
            return db_category
    
    # Default fallbacks based on common patterns
    fallback_mappings = {
        'toys': 'Playing Sets',
        'game': 'Board Games',
        'doll': 'Dolls & Collectables',
        'car': 'Cars & Vehicles',
        'art': 'Arts & Crafts',
        'craft': 'Arts & Crafts',
        'book': 'English Books',
        'puzzle': 'Puzzles',
        'sport': 'Sports',
        'outdoor': 'Outdoor Toys',
        'water': 'Water Activities',
        'baby': 'Babies',
        'school': 'School Supplies',
        'costume': 'Costumes',
        'animal': 'Animal Figures',
        'character': 'Characters & Heroes',
        'hero': 'Characters & Heroes',
        'action': 'Guns & Action Toys',
        'construction': 'Construction',
        'building': 'Construction',
        'educational': 'Educational Toys',
        'learning': 'Educational Toys',
    }
    
    for keyword, category in fallback_mappings.items():
        if keyword in invalid_lower:
            return category
    
    # Ultimate fallback
    return 'Playing Sets'  # Most general category

def validate_and_update_categories():
    """Validate all product categories against database and update invalid ones"""
    
    # Load real database categories
    database_categories = load_database_categories()
    if not database_categories:
        print("❌ No database categories loaded. Cannot proceed.")
        return
    
    print(f"📊 Database categories: {sorted(database_categories)}")
    
    # Load product catalog
    catalog_file = Path("Recommendation Engine Demo/product_catalog_final_categories.ndjson")
    if not catalog_file.exists():
        print(f"❌ Product catalog not found: {catalog_file}")
        return
    
    # Statistics
    stats = {
        'total_products': 0,
        'products_updated': 0,
        'invalid_categories_found': set(),
        'category_mappings': {},
        'valid_categories_used': set(),
    }
    
    # Process products
    updated_products = []
    
    with open(catalog_file, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            if not line.strip():
                continue
                
            try:
                product = json.loads(line.strip())
                stats['total_products'] += 1
                
                original_categories = product.get('categories', [])
                updated_categories = []
                product_updated = False
                
                for category in original_categories:
                    if category in database_categories:
                        # Category is valid
                        updated_categories.append(category)
                        stats['valid_categories_used'].add(category)
                    else:
                        # Category is invalid - find best match
                        stats['invalid_categories_found'].add(category)
                        best_match = find_best_category_match(category, database_categories)
                        updated_categories.append(best_match)
                        
                        # Track the mapping
                        if category not in stats['category_mappings']:
                            stats['category_mappings'][category] = best_match
                        
                        product_updated = True
                        print(f"Line {line_num}: '{category}' → '{best_match}' for product: {product.get('title', 'Unknown')[:50]}...")
                
                # Remove duplicates while preserving order
                final_categories = []
                for cat in updated_categories:
                    if cat not in final_categories:
                        final_categories.append(cat)
                
                product['categories'] = final_categories
                
                if product_updated:
                    stats['products_updated'] += 1
                
                updated_products.append(product)
                
            except json.JSONDecodeError as e:
                print(f"❌ Error parsing line {line_num}: {e}")
                continue
    
    # Save updated catalog
    with open(catalog_file, 'w', encoding='utf-8') as file:
        for product in updated_products:
            file.write(json.dumps(product, ensure_ascii=False) + '\n')
    
    # Print comprehensive statistics
    print("\n" + "="*80)
    print("📊 DATABASE-DRIVEN CATEGORY VALIDATION RESULTS")
    print("="*80)
    print(f"Total products processed: {stats['total_products']}")
    print(f"Products updated: {stats['products_updated']}")
    print(f"Invalid categories found: {len(stats['invalid_categories_found'])}")
    print(f"Valid database categories used: {len(stats['valid_categories_used'])}")
    
    if stats['invalid_categories_found']:
        print(f"\n❌ Invalid categories that were updated:")
        for invalid_cat in sorted(stats['invalid_categories_found']):
            mapped_to = stats['category_mappings'].get(invalid_cat, 'Unknown')
            print(f"   '{invalid_cat}' → '{mapped_to}'")
    
    print(f"\n✅ Valid database categories in use:")
    for valid_cat in sorted(stats['valid_categories_used']):
        print(f"   ✓ {valid_cat}")
    
    unused_categories = database_categories - stats['valid_categories_used']
    if unused_categories:
        print(f"\n📝 Unused database categories:")
        for unused_cat in sorted(unused_categories):
            print(f"   • {unused_cat}")
    
    print(f"\n✅ Category validation and update complete!")
    print(f"📁 Updated file: {catalog_file}")

if __name__ == "__main__":
    print("🔍 Database-Driven Category Validation Script")
    print("=" * 50)
    validate_and_update_categories()