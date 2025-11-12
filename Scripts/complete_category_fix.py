#!/usr/bin/env python3
"""
Complete Category Fix - Remove all Sub_ categories and fix remaining issues
"""

import json
import re
from pathlib import Path

def fix_all_categories():
    """Fix all remaining category issues"""
    input_file = Path("Recommendation Engine Demo/product_catalog_final_categories.ndjson")
    
    # Enhanced category mapping including all Sub_ categories and missing ones
    category_mapping = {
        # Existing mappings
        "Role Play Toys": "Playing Sets",
        "Electronic Learning Toys": "Educational Toys",
        "Card Games": "Board Games",
        "Remote Control Toys": "Cars & Vehicles",
        "Superhero Figures": "Characters & Heroes",
        "Action Figures": "Characters & Heroes",
        "Plush Toys": "Dolls & Collectables",
        "Fashion Dolls": "Dolls & Collectables",
        "Dress Up & Accessories": "Fashion & Cosmetics",
        "Dinosaur Toys": "Animal Figures",
        "Animal Playsets": "Animal Figures",
        "Building Sets": "Construction",
        "Battle Toys & Weapons": "Guns & Action Toys",
        "Baby Dolls": "Dolls & Collectables",
        
        # Complete Sub_ category mappings based on real database categories
        "Sub_2": "Arts & Crafts",
        "Sub_3": "Dolls & Collectables", 
        "Sub_4": "Cars & Vehicles",
        "Sub_5": "Construction",
        "Sub_6": "Fashion & Cosmetics",
        "Sub_7": "Educational Toys",
        "Sub_9": "Sports",
        "Sub_14": "Water Activities",
        "Sub_16": "Costumes",
        "Sub_18": "Slime,Clay & Sand",
        "Sub_19": "Outdoor Toys",
        "Sub_22": "Arabic Books",
        "Sub_26": "Puzzles",
        "Sub_27": "Kids Accessories",
        "Sub_28": "Babies",
        "Sub_34": "Cakes",
        "Sub_35": "Customizable",
        "Sub_36": "English Books",
        "Sub_46": "School Supplies",
        "Sub_49": "Dabdoob Eidiya",
        "Sub_51": "Pajama",
        "Sub_52": "Beachwear",
        "Sub_54": "Balloons Party Decoration",
        "Sub_55": "Cakes by Marble Slab",
        "Sub_56": "Animal Figures",
        "Sub_57": "Voucher",
        "Sub_58": "Playing Sets",
        "Sub_60": "Educational Toys",
        "Sub_62": "Arts & Crafts",
        "Sub_63": "Dolls & Collectables",
        "Sub_64": "Fashion & Cosmetics",
        "Sub_66": "Cars & Vehicles",
        "Sub_68": "Characters & Heroes",
        "Sub_72": "Water Activities",
        "Sub_73": "Construction",
        "Sub_74": "Kids Accessories",
        "Sub_75": "School Supplies",
        "Sub_76": "School Supplies",
        "Sub_77": "School Supplies",
        "Sub_79": "Outdoor Toys",
        "Sub_80": "Guns & Action Toys",
        "Sub_81": "Funko!",
        "Sub_82": "Pre-School",
        "Sub_84": "Board Games",
        "Sub_85": "Educational Toys",
        "Sub_86": "Guns & Action Toys",
        "Sub_87": "Sports",
        "Sub_89": "Cars & Vehicles",
        "Sub_90": "Cars & Vehicles",
        "Sub_91": "Cars & Vehicles",
        "Sub_93": "Animal Figures",
        "Sub_94": "Arts & Crafts",
        "Sub_98": "Puzzles",
        "Sub_99": "Cars & Vehicles",
        "Sub_111": "School Supplies",
        "Sub_113": "Babies",
        "Sub_114": "Customizable",
        "Sub_115": "Arabic Books",
        "Sub_116": "English Books",
        "Sub_117": "Outdoor Toys",
        "Sub_118": "Cakes",
        "Sub_120": "Beachwear",
        "Sub_121": "Balloons Party Decoration",
        "Sub_122": "Costumes",
        "Sub_123": "Ride-On And Scooters",
        "Sub_124": "Bundles",
        "Sub_127": "Special Prices",
        "Sub_128": "Construction",
        "Sub_130": "Arts & Crafts",
        "Sub_132": "Discounts",
        "Sub_133": "Socks",
        "Sub_134": "Dabdoob Eidiya",
        "Sub_135": "Pajama",
        "Sub_136": "Promotions",
        "Sub_137": "For MAMA",
        "Sub_138": "Fashion & Cosmetics",
        "Sub_139": "Arts & Crafts",
        "Sub_140": "Football Jerseys",
        "Sub_143": "vilebrequin",
        "Sub_144": "New Year Box",
        "Sub_145": "Promotion",
        "Sub_146": "Newborn Gifts",
        "Sub_147": "Drones & Planes",
        "Sub_148": "Cakes by Marble Slab",
        "Sub_149": "Voucher",
        "Sub_151": "Educational Toys",
        "Sub_152": "Pre-School",
        "Sub_153": "Pre-School",
        "Sub_154": "Playing Sets",
        "Sub_155": "Arts & Crafts",
        "Sub_156": "Dolls & Collectables",
        "Sub_157": "Fashion & Cosmetics",
        "Sub_158": "Cars & Vehicles",
        "Sub_160": "Characters & Heroes",
        "Sub_161": "Water Activities",
        "Sub_162": "Construction",
        "Sub_163": "Kids Accessories",
    }
    
    updated_count = 0
    total_count = 0
    
    # Read all products
    products = []
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                products.append(json.loads(line.strip()))
    
    # Update categories
    for product in products:
        total_count += 1
        original_categories = product.get('categories', [])
        updated_categories = []
        was_updated = False
        
        for category in original_categories:
            if category in category_mapping:
                updated_categories.append(category_mapping[category])
                was_updated = True
            else:
                updated_categories.append(category)
        
        # Remove duplicates while preserving order
        final_categories = []
        for cat in updated_categories:
            if cat not in final_categories:
                final_categories.append(cat)
        
        product['categories'] = final_categories
        
        if was_updated:
            updated_count += 1
    
    # Write back to file
    with open(input_file, 'w', encoding='utf-8') as file:
        for product in products:
            file.write(json.dumps(product, ensure_ascii=False) + '\n')
    
    print(f"✅ Updated {updated_count} products out of {total_count} total products")
    
    # Verify no Sub_ categories remain
    remaining_subs = []
    for product in products:
        for category in product.get('categories', []):
            if category.startswith('Sub_'):
                remaining_subs.append(category)
    
    unique_subs = list(set(remaining_subs))
    if unique_subs:
        print(f"⚠️  Remaining Sub_ categories: {unique_subs}")
    else:
        print("✅ No Sub_ categories remaining")

if __name__ == "__main__":
    fix_all_categories()