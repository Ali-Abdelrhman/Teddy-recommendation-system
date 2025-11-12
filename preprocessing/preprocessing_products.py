#!/usr/bin/env python3
"""
Products Preprocessing Script for GCP Retail API
================================================

This script processes the raw Products.csv file from Dabdoob database queries
and prepares it for GCP Retail API ingestion with data quality improvements.

Input: Products.csv
Output: Products_GCP_Ready.csv

Author: Data Engineering Team
Date: October 21, 2025
"""

import pandas as pd
import json
import numpy as np
from pathlib import Path
import logging
import re
from typing import Dict, List, Any
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProductsPreprocessor:
    """Preprocessor for Dabdoob products data"""
    
    def __init__(self, input_file: str, output_file: str):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.df = None
        self.processed_df = None
        
    def load_data(self) -> pd.DataFrame:
        """Load the raw products CSV file"""
        logger.info(f"Loading data from {self.input_file}")
        
        try:
            self.df = pd.read_csv(self.input_file)
            logger.info(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
            logger.info(f"Unique products: {self.df['id'].nunique()}")
            return self.df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def validate_data(self) -> bool:
        """Validate the input data quality"""
        logger.info("Validating data quality...")
        
        issues = []
        
        # Check for missing values in critical fields
        critical_fields = ['id', 'title', 'description']
        for field in critical_fields:
            if field in self.df.columns:
                missing_count = self.df[field].isnull().sum()
                if missing_count > 0:
                    issues.append(f"Missing {field}: {missing_count} rows")
        
        # Check for duplicate product IDs
        duplicates = self.df['id'].duplicated().sum()
        if duplicates > 0:
            issues.append(f"Found {duplicates} duplicate product IDs")
        
        # Check product ID format
        if 'id' in self.df.columns:
            invalid_ids = self.df[~self.df['id'].str.match(r'PROD\d{6}', na=False)]['id'].unique()
            if len(invalid_ids) > 0:
                issues.append(f"Invalid product ID format: {invalid_ids[:5]}...")
        
        # Check URL format
        if 'uri' in self.df.columns:
            invalid_urls = self.df[self.df['uri'].notna() & ~self.df['uri'].str.contains('https?://', na=False)]['uri'].nunique()
            if invalid_urls > 0:
                issues.append(f"Invalid URLs found: {invalid_urls} products")
        
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
        
        # Remove duplicate product IDs (keep first occurrence)
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates(subset=['id'], keep='first')
        removed_duplicates = initial_rows - len(self.df)
        if removed_duplicates > 0:
            logger.info(f"Removed {removed_duplicates} duplicate product IDs")
        
        # Clean text fields
        text_fields = ['title', 'description']
        for field in text_fields:
            if field in self.df.columns:
                # Remove extra whitespace
                self.df[field] = self.df[field].astype(str).str.strip()
                # Remove newlines and normalize spaces
                self.df[field] = self.df[field].str.replace('\n', ' ').str.replace('\r', ' ')
                self.df[field] = self.df[field].str.replace(r'\s+', ' ', regex=True)
                # Remove empty strings
                self.df[field] = self.df[field].replace('', np.nan)
        
        # Clean and validate categories
        if 'categories' in self.df.columns:
            self.df['categories'] = self.df['categories'].fillna('["General"]')
            # Ensure categories are in proper JSON array format
            def fix_categories(cat_str):
                try:
                    # Try to parse as JSON first
                    categories = json.loads(cat_str)
                    if isinstance(categories, list):
                        return json.dumps(categories)
                    else:
                        return json.dumps([str(categories)])
                except:
                    # If not valid JSON, wrap in array
                    return json.dumps([str(cat_str).strip('"[]')])
            
            self.df['categories'] = self.df['categories'].apply(fix_categories)
        
        # Clean and validate brands
        if 'brands' in self.df.columns:
            self.df['brands'] = self.df['brands'].fillna('["Unknown"]')
            # Ensure brands are in proper JSON array format
            def fix_brands(brand_str):
                try:
                    brands = json.loads(brand_str)
                    if isinstance(brands, list):
                        return json.dumps(brands)
                    else:
                        return json.dumps([str(brands)])
                except:
                    return json.dumps([str(brand_str).strip('"[]')])
            
            self.df['brands'] = self.df['brands'].apply(fix_brands)
        
        # Clean boolean fields
        boolean_fields = ['is_wrappable', 'is_customizable']
        for field in boolean_fields:
            if field in self.df.columns:
                self.df[field] = self.df[field].astype(str).str.lower()
                self.df[field] = self.df[field].map({'true': True, 'false': False, '1': True, '0': False})
                self.df[field] = self.df[field].fillna(False)
        
        # Clean availability field
        if 'availability' in self.df.columns:
            self.df['availability'] = self.df['availability'].fillna('IN_STOCK')
            # Ensure valid availability values
            valid_availability = ['IN_STOCK', 'OUT_OF_STOCK', 'PREORDER', 'BACKORDER']
            self.df['availability'] = self.df['availability'].apply(
                lambda x: x if x in valid_availability else 'IN_STOCK'
            )
        
        # Sort by product ID for consistent output
        self.df = self.df.sort_values('id')
        
        logger.info("Data cleaning completed ✓")
        return self.df
    
    def enhance_data(self) -> pd.DataFrame:
        """Add calculated fields and enhancements"""
        logger.info("Enhancing data with calculated fields...")
        
        # Add title length (useful for quality scoring)
        if 'title' in self.df.columns:
            self.df['title_length'] = self.df['title'].str.len()
        
        # Add description length
        if 'description' in self.df.columns:
            self.df['description_length'] = self.df['description'].str.len()
        
        # Extract domain from URI
        if 'uri' in self.df.columns:
            def extract_domain(url):
                try:
                    if pd.isna(url):
                        return None
                    parsed = urlparse(url)
                    return parsed.netloc
                except:
                    return None
            
            self.df['domain'] = self.df['uri'].apply(extract_domain)
        
        # Add data quality score
        def calculate_quality_score(row):
            score = 0
            # Title quality (max 30 points)
            if pd.notna(row.get('title')) and len(str(row.get('title', ''))) > 10:
                score += 30
            elif pd.notna(row.get('title')):
                score += 15
            
            # Description quality (max 30 points)
            if pd.notna(row.get('description')) and len(str(row.get('description', ''))) > 50:
                score += 30
            elif pd.notna(row.get('description')):
                score += 15
            
            # Categories (max 20 points)
            if pd.notna(row.get('categories')):
                try:
                    cats = json.loads(row.get('categories', '[]'))
                    if len(cats) > 0 and cats[0] != 'General':
                        score += 20
                    elif len(cats) > 0:
                        score += 10
                except:
                    score += 5
            
            # Brands (max 20 points)
            if pd.notna(row.get('brands')):
                try:
                    brands = json.loads(row.get('brands', '[]'))
                    if len(brands) > 0 and brands[0] != 'Unknown':
                        score += 20
                    elif len(brands) > 0:
                        score += 10
                except:
                    score += 5
            
            return min(score, 100)  # Cap at 100
        
        self.df['quality_score'] = self.df.apply(calculate_quality_score, axis=1)
        
        logger.info("Data enhancement completed ✓")
        return self.df
    
    def generate_summary_stats(self) -> Dict[str, Any]:
        """Generate summary statistics for the processed data"""
        logger.info("Generating summary statistics...")
        
        stats = {
            'total_products': len(self.df),
            'data_quality': {},
            'field_coverage': {},
            'quality_distribution': {}
        }
        
        # Field coverage analysis
        for col in self.df.columns:
            non_null_count = self.df[col].notna().sum()
            coverage_pct = (non_null_count / len(self.df)) * 100
            stats['field_coverage'][col] = {
                'non_null_count': non_null_count,
                'coverage_percentage': round(coverage_pct, 2)
            }
        
        # Quality score distribution
        if 'quality_score' in self.df.columns:
            stats['quality_distribution'] = {
                'mean_score': round(self.df['quality_score'].mean(), 2),
                'median_score': round(self.df['quality_score'].median(), 2),
                'high_quality_products': (self.df['quality_score'] >= 80).sum(),
                'medium_quality_products': ((self.df['quality_score'] >= 60) & (self.df['quality_score'] < 80)).sum(),
                'low_quality_products': (self.df['quality_score'] < 60).sum()
            }
        
        # Availability distribution
        if 'availability' in self.df.columns:
            stats['availability_distribution'] = self.df['availability'].value_counts().to_dict()
        
        return stats
    
    def save_processed_data(self) -> None:
        """Save the processed data to CSV"""
        logger.info(f"Saving processed data to {self.output_file}")
        
        # Create output directory if it doesn't exist
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to CSV
        self.df.to_csv(self.output_file, index=False)
        logger.info(f"Saved {len(self.df)} products to {self.output_file}")
    
    def process(self) -> Dict[str, Any]:
        """Run the complete preprocessing pipeline"""
        logger.info("Starting products preprocessing pipeline...")
        
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
        
        logger.info("Products preprocessing completed successfully! ✓")
        return summary

def main():
    """Main execution function"""
    
    # File paths
    input_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\RealDBData\Products.csv"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\RealDBData\Products_GCP_Ready.csv"
    
    # Initialize preprocessor
    preprocessor = ProductsPreprocessor(input_file, output_file)
    
    try:
        # Run preprocessing
        summary = preprocessor.process()
        
        # Print summary
        print("\n" + "="*60)
        print("PRODUCTS PREPROCESSING SUMMARY")
        print("="*60)
        print(f"Total products processed: {summary['total_products']}")
        
        print("\nKey Field Coverage:")
        key_fields = ['title', 'description', 'categories', 'brands', 'uri']
        for field in key_fields:
            if field in summary['field_coverage']:
                stats = summary['field_coverage'][field]
                print(f"  {field}: {stats['non_null_count']} products ({stats['coverage_percentage']}%)")
        
        if 'quality_distribution' in summary:
            print("\nQuality Score Distribution:")
            qd = summary['quality_distribution']
            print(f"  Mean Score: {qd['mean_score']}/100")
            print(f"  High Quality (80+): {qd['high_quality_products']} products")
            print(f"  Medium Quality (60-79): {qd['medium_quality_products']} products")
            print(f"  Low Quality (<60): {qd['low_quality_products']} products")
        
        if 'availability_distribution' in summary:
            print("\nAvailability Distribution:")
            for status, count in summary['availability_distribution'].items():
                print(f"  {status}: {count} products")
        
        print(f"\nProcessed file saved to: {output_file}")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise

if __name__ == "__main__":
    main()