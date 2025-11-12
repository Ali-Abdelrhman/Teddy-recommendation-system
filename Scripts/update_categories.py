#!/usr/bin/env python3
"""
Category Replacement Script for Dabdoob Product Catalog
Updates predicted categories with real database categories
"""

import json
import csv
from pathlib import Path

def load_category_mapping():
    """Load the real category mapping from database"""
    mapping = {}
    
    # Create mapping for common predicted categories to real categories
    predicted_to_real = {
        # Role Play / Medical / Toys
        "Role Play Toys": "Playing Sets",
        "Medical Toys": "Playing Sets",
        "Role Playing": "Playing Sets",
        
        # Electronic / Learning
        "Electronic Learning Toys": "Educational Toys",
        "Electronic Toys": "Educational Toys",
        "Learning Toys": "Educational Toys",
        
        # Card / Board Games
        "Card Games": "Board Games",
        "Puzzle Games": "Board Games",
        
        # Vehicle related
        "Remote Control Toys": "Cars & Vehicles",
        "RC Vehicles": "Cars & Vehicles",
        "Vehicle Toys": "Cars & Vehicles",
        
        # Figures / Characters
        "Superhero Figures": "Characters & Heroes",
        "Action Figures": "Characters & Heroes",
        "Character Figures": "Characters & Heroes",
        
        # Plush / Soft toys
        "Plush Toys": "Dolls & Collectables",
        "Soft Toys": "Dolls & Collectables",
        "Stuffed Animals": "Animal Figures",
        
        # Fashion / Dress up
        "Fashion Dolls": "Dolls & Collectables",
        "Dress Up & Accessories": "Fashion & Cosmetics",
        "Fashion Accessories": "Fashion & Cosmetics",
        
        # Animals / Dinosaurs
        "Dinosaur Toys": "Animal Figures",
        "Animal Playsets": "Animal Figures",
        "Pet Toys": "Animal Figures",
        
        # Building / Construction
        "Building Sets": "Construction",
        "Construction Toys": "Construction",
        "Building Blocks": "Construction",
        
        # Battle / Action
        "Battle Toys & Weapons": "Guns & Action Toys",
        "War Toys": "Guns & Action Toys",
        "Action Toys": "Guns & Action Toys",
        
        # Subcategories (Sub_XXX) - map to main categories
        "Sub_128": "Construction",
        "Sub_89": "Cars & Vehicles", 
        "Sub_99": "Cars & Vehicles",
        "Sub_90": "Cars & Vehicles",
        "Sub_139": "Arts & Crafts",
        "Sub_91": "Cars & Vehicles",
        "Sub_27": "Kids Accessories",
        "Sub_46": "School Supplies",
        "Sub_76": "School Supplies",
        "Sub_130": "Arts & Crafts",
    }
    
    return predicted_to_real

def update_product_catalog():
    """Update the product catalog with real categories"""
    input_file = Path("product_catalog_final_categories.ndjson")
    output_file = Path("product_catalog_real_categories.ndjson")
    
    if not input_file.exists():
        # Check in different locations
        possible_paths = [
            Path("Recommendation Engine Demo/product_catalog_final_categories.ndjson"),
            Path("../Recommendation Engine Demo/product_catalog_final_categories.ndjson"),
            Path("c:/Users/Ahmed/Downloads/Teddy recommendation system/Recommendation Engine Demo/product_catalog_final_categories.ndjson")
        ]
        
        for path in possible_paths:
            if path.exists():
                input_file = path
                break
        else:
            print("❌ Could not find product_catalog_final_categories.ndjson")
            return
    
    category_mapping = load_category_mapping()
    
    updated_products = []
    stats = {
        'total_products': 0,
        'categories_updated': 0,
        'categories_unchanged': 0,
        'mappings_used': {}
    }
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    product = json.loads(line.strip())
                    stats['total_products'] += 1
                    
                    # Update categories
                    original_categories = product.get('categories', [])
                    updated_categories = []
                    category_updated = False
                    
                    for category in original_categories:
                        if category in category_mapping:
                            new_category = category_mapping[category]
                            updated_categories.append(new_category)
                            category_updated = True
                            
                            # Track mapping usage
                            if category not in stats['mappings_used']:
                                stats['mappings_used'][category] = 0
                            stats['mappings_used'][category] += 1
                        else:
                            # Keep original if no mapping found
                            updated_categories.append(category)
                    
                    # Update the product
                    product['categories'] = updated_categories
                    
                    if category_updated:
                        stats['categories_updated'] += 1
                    else:
                        stats['categories_unchanged'] += 1
                    
                    updated_products.append(product)
        
        # Save updated catalog
        with open(output_file, 'w', encoding='utf-8') as file:
            for product in updated_products:
                file.write(json.dumps(product, ensure_ascii=False) + '\n')
        
        # Print statistics
        print(f"✅ Updated product catalog saved to: {output_file}")
        print(f"📊 Total products: {stats['total_products']}")
        print(f"📊 Products with updated categories: {stats['categories_updated']}")
        print(f"📊 Products unchanged: {stats['categories_unchanged']}")
        
        print(f"\n🔄 Category mappings used:")
        for old_cat, count in stats['mappings_used'].items():
            new_cat = category_mapping[old_cat]
            print(f"  {old_cat} → {new_cat} ({count} products)")
            
    except Exception as e:
        print(f"❌ Error updating catalog: {e}")

if __name__ == "__main__":
    update_product_catalog()