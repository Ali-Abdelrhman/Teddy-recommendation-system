#!/usr/bin/env python3
"""
Categories Preprocessing Script for GCP Retail API
==================================================

This script processes the raw Categeory.csv file from Dabdoob database queries
and prepares it for GCP Retail API ingestion.

Input: Categeory.csv
Output: Categeory_GCP_Ready.csv

Author: Data Engineering Team
Date: October 21, 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, List, Any
import re

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CategoriesPreprocessor:
    """Preprocessor for Dabdoob categories data"""
    
    def __init__(self, input_file: str, output_file: str):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.df = None
        
    def load_data(self) -> pd.DataFrame:
        """Load the raw categories CSV file"""
        logger.info(f"Loading data from {self.input_file}")
        
        try:
            self.df = pd.read_csv(self.input_file)
            logger.info(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
            logger.info(f"Unique categories: {len(self.df)}")
            return self.df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def validate_data(self) -> bool:
        """Validate the input data quality"""
        logger.info("Validating data quality...")
        
        issues = []
        
        # Check for missing values in critical fields
        critical_fields = ['id', 'category_name']
        for field in critical_fields:
            if field in self.df.columns:
                missing_count = self.df[field].isnull().sum()
                if missing_count > 0:
                    issues.append(f"Missing {field}: {missing_count} rows")
        
        # Check for duplicate category IDs
        if 'id' in self.df.columns:
            duplicates = self.df['id'].duplicated().sum()
            if duplicates > 0:
                issues.append(f"Found {duplicates} duplicate category IDs")
        
        # Check for duplicate category names
        if 'category_name' in self.df.columns:
            duplicates = self.df['category_name'].duplicated().sum()
            if duplicates > 0:
                issues.append(f"Found {duplicates} duplicate category names")
        
        if issues:
            logger.warning("Data quality issues found:")
            for issue in issues:
                logger.warning(f"  - {issue}")
        else:
            logger.info("Data validation passed ✓")
        
        return len(issues) == 0
    
    def clean_data(self) -> pd.DataFrame:
        """Clean and standardize the data"""
        logger.info("Cleaning data...")
        
        # Remove duplicate category IDs (keep first occurrence)
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates(subset=['id'], keep='first')
        removed_duplicates = initial_rows - len(self.df)
        if removed_duplicates > 0:
            logger.info(f"Removed {removed_duplicates} duplicate category IDs")
        
        # Clean category names
        if 'category_name' in self.df.columns:
            # Remove extra whitespace
            self.df['category_name'] = self.df['category_name'].astype(str).str.strip()
            # Standardize case (Title Case)
            self.df['category_name'] = self.df['category_name'].str.title()
            # Fix common issues
            self.df['category_name'] = self.df['category_name'].str.replace('&', 'And')
            # Remove empty category names
            self.df = self.df[self.df['category_name'].str.len() > 0]
        
        # Clean slugs
        if 'slug' in self.df.columns:
            self.df['slug'] = self.df['slug'].astype(str).str.strip().str.lower()
            # Ensure slugs don't have special characters except hyphens
            self.df['slug'] = self.df['slug'].str.replace(r'[^a-z0-9\-]', '-', regex=True)
            self.df['slug'] = self.df['slug'].str.replace(r'-+', '-', regex=True)
            self.df['slug'] = self.df['slug'].str.strip('-')
        
        # Clean display order
        if 'displayorder' in self.df.columns:
            self.df['displayorder'] = pd.to_numeric(self.df['displayorder'], errors='coerce')
            self.df['displayorder'] = self.df['displayorder'].fillna(999)  # Default to end
            self.df['displayorder'] = self.df['displayorder'].astype(int)
        
        # Clean full category path
        if 'full_category_path' in self.df.columns:
            self.df['full_category_path'] = self.df['full_category_path'].astype(str).str.strip()
            # For flat hierarchy, this should be same as category_name
            empty_paths = (self.df['full_category_path'].isnull()) | (self.df['full_category_path'] == '')
            self.df.loc[empty_paths, 'full_category_path'] = self.df.loc[empty_paths, 'category_name']
        
        # Clean colors - set defaults for missing colors
        default_colors = {
            'color': '#e0e0e0',  # Light gray default
            'text_color': '#333333'  # Dark gray text
        }
        
        for color_field, default_color in default_colors.items():
            if color_field in self.df.columns:
                # Fill empty colors with defaults
                empty_colors = (self.df[color_field].isnull()) | (self.df[color_field] == '')
                self.df.loc[empty_colors, color_field] = default_color
                
                # Ensure colors are in proper hex format
                def fix_color(color):
                    if pd.isna(color) or color == '':
                        return default_color
                    color = str(color).strip()
                    if not color.startswith('#'):
                        color = f'#{color}'
                    # Validate hex color (should be 7 characters including #)
                    if len(color) == 7 and re.match(r'^#[0-9A-Fa-f]{6}$', color):
                        return color.lower()
                    else:
                        return default_color
                
                self.df[color_field] = self.df[color_field].apply(fix_color)
        
        # Sort by display order and then by category name
        sort_columns = []
        if 'displayorder' in self.df.columns:
            sort_columns.append('displayorder')
        sort_columns.append('category_name')
        self.df = self.df.sort_values(sort_columns)
        
        logger.info("Data cleaning completed ✓")
        return self.df
    
    def enhance_data(self) -> pd.DataFrame:
        """Add calculated fields and enhancements"""
        logger.info("Enhancing data with calculated fields...")
        
        # Add category level (always 1 for flat hierarchy)
        self.df['category_level'] = 1
        
        # Add parent category (None for flat hierarchy)
        self.df['parent_category_id'] = None
        self.df['parent_category_name'] = None
        
        # Add category type based on name patterns
        def categorize_type(name):
            name_lower = str(name).lower()
            
            # Age-based categories
            if any(age in name_lower for age in ['babies', 'pre-school', 'newborn']):
                return 'age_based'
            
            # Gender-based categories
            if any(gender in name_lower for gender in ['boys', 'girls', 'mama']):
                return 'gender_based'
            
            # Activity-based categories
            if any(activity in name_lower for activity in ['sports', 'outdoor', 'water', 'educational']):
                return 'activity_based'
            
            # Product-type categories
            if any(product in name_lower for product in ['toys', 'games', 'books', 'clothes', 'accessories']):
                return 'product_based'
            
            # Special categories
            if any(special in name_lower for special in ['special', 'promotion', 'bundle', 'discount']):
                return 'promotional'
            
            return 'general'
        
        self.df['category_type'] = self.df['category_name'].apply(categorize_type)
        
        # Add category popularity score (based on display order - lower order = higher popularity)
        if 'displayorder' in self.df.columns:
            max_order = self.df['displayorder'].max()
            self.df['popularity_score'] = (max_order - self.df['displayorder'] + 1) * 10
            self.df['popularity_score'] = self.df['popularity_score'].clip(upper=100)
        
        # Add SEO-friendly URL path
        if 'slug' in self.df.columns:
            self.df['url_path'] = '/category/' + self.df['slug']
        
        # Add category quality score
        def calculate_category_quality_score(row):
            score = 0
            
            # Name quality (30 points)
            name = str(row.get('category_name', ''))
            if len(name) > 3 and name != 'nan':
                score += 20
                if len(name) <= 30:  # Not too long
                    score += 10
            
            # Slug quality (20 points)
            slug = str(row.get('slug', ''))
            if len(slug) > 2 and slug != 'nan':
                score += 15
                if '-' in slug:  # Well-formatted slug
                    score += 5
            
            # Color quality (20 points)
            color = str(row.get('color', ''))
            if color and color != '' and color.startswith('#'):
                score += 20
            
            # Path quality (20 points)
            path = str(row.get('full_category_path', ''))
            if path and path != 'nan' and len(path) > 2:
                score += 20
            
            # Display order (10 points)
            order = row.get('displayorder', 999)
            if order < 50:  # High priority categories
                score += 10
            elif order < 100:
                score += 5
            
            return min(score, 100)
        
        self.df['quality_score'] = self.df.apply(calculate_category_quality_score, axis=1)
        
        logger.info("Data enhancement completed ✓")
        return self.df
    
    def generate_summary_stats(self) -> Dict[str, Any]:
        """Generate summary statistics for the processed data"""
        logger.info("Generating summary statistics...")
        
        stats = {
            'total_categories': len(self.df),
            'category_types': {},
            'display_order_range': {},
            'quality_distribution': {},
            'color_usage': {}
        }
        
        # Category type distribution
        if 'category_type' in self.df.columns:
            stats['category_types'] = self.df['category_type'].value_counts().to_dict()
        
        # Display order analysis
        if 'displayorder' in self.df.columns:
            stats['display_order_range'] = {
                'min_order': int(self.df['displayorder'].min()),
                'max_order': int(self.df['displayorder'].max()),
                'avg_order': round(self.df['displayorder'].mean(), 1)
            }
        
        # Quality score distribution
        if 'quality_score' in self.df.columns:
            stats['quality_distribution'] = {
                'mean_score': round(self.df['quality_score'].mean(), 2),
                'high_quality_categories': (self.df['quality_score'] >= 80).sum(),
                'medium_quality_categories': ((self.df['quality_score'] >= 60) & (self.df['quality_score'] < 80)).sum(),
                'low_quality_categories': (self.df['quality_score'] < 60).sum()
            }
        
        # Color usage analysis
        if 'color' in self.df.columns:
            unique_colors = self.df['color'].nunique()
            default_color_count = (self.df['color'] == '#e0e0e0').sum()
            stats['color_usage'] = {
                'unique_colors': unique_colors,
                'categories_with_default_color': default_color_count,
                'categories_with_custom_color': len(self.df) - default_color_count
            }
        
        # Popular categories (top 10 by display order)
        if 'displayorder' in self.df.columns and 'category_name' in self.df.columns:
            top_categories = self.df.nsmallest(10, 'displayorder')[['category_name', 'displayorder']]
            stats['top_categories'] = top_categories.set_index('category_name')['displayorder'].to_dict()
        
        return stats
    
    def save_processed_data(self) -> None:
        """Save the processed data to CSV"""
        logger.info(f"Saving processed data to {self.output_file}")
        
        # Create output directory if it doesn't exist
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to CSV
        self.df.to_csv(self.output_file, index=False)
        logger.info(f"Saved {len(self.df)} categories to {self.output_file}")
    
    def process(self) -> Dict[str, Any]:
        """Run the complete preprocessing pipeline"""
        logger.info("Starting categories preprocessing pipeline...")
        
        # Load and validate data
        self.load_data()
        self.validate_data()
        
        # Clean and enhance data
        self.clean_data()
        self.enhance_data()
        
        # Generate summary
        summary = self.generate_summary_stats()
        
        # Save processed data
        self.save_processed_data()
        
        logger.info("Categories preprocessing completed successfully! ✓")
        return summary

def main():
    """Main execution function"""
    
    # File paths (note: keeping original filename with typo as in the source)
    input_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\RealDBData\Categeory.csv"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\RealDBData\Categeory_GCP_Ready.csv"
    
    # Initialize preprocessor
    preprocessor = CategoriesPreprocessor(input_file, output_file)
    
    try:
        # Run preprocessing
        summary = preprocessor.process()
        
        # Print summary
        print("\n" + "="*60)
        print("CATEGORIES PREPROCESSING SUMMARY")
        print("="*60)
        print(f"Total categories processed: {summary['total_categories']}")
        
        if 'category_types' in summary:
            print(f"\nCategory Types:")
            for cat_type, count in summary['category_types'].items():
                print(f"  {cat_type}: {count} categories")
        
        if 'display_order_range' in summary:
            dor = summary['display_order_range']
            print(f"\nDisplay Order Range:")
            print(f"  Min: {dor['min_order']}, Max: {dor['max_order']}, Avg: {dor['avg_order']}")
        
        if 'quality_distribution' in summary:
            qd = summary['quality_distribution']
            print(f"\nQuality Distribution:")
            print(f"  Mean Score: {qd['mean_score']}/100")
            print(f"  High Quality (80+): {qd['high_quality_categories']} categories")
            print(f"  Medium Quality (60-79): {qd['medium_quality_categories']} categories")
            print(f"  Low Quality (<60): {qd['low_quality_categories']} categories")
        
        if 'color_usage' in summary:
            cu = summary['color_usage']
            print(f"\nColor Usage:")
            print(f"  Unique Colors: {cu['unique_colors']}")
            print(f"  Custom Colors: {cu['categories_with_custom_color']} categories")
            print(f"  Default Colors: {cu['categories_with_default_color']} categories")
        
        if 'top_categories' in summary:
            print(f"\nTop 5 Priority Categories:")
            for cat_name, order in list(summary['top_categories'].items())[:5]:
                print(f"  {order}: {cat_name}")
        
        print(f"\nProcessed file saved to: {output_file}")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise

if __name__ == "__main__":
    main()