#!/usr/bin/env python3
"""
Images Preprocessing Script for GCP Retail API
==============================================

This script processes the raw Images.csv file from Dabdoob database queries
and prepares it for GCP Retail API ingestion with data quality improvements.

Input: Images.csv
Output: Images_GCP_Ready.csv

Author: Data Engineering Team
Date: October 21, 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, List, Any
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImagesPreprocessor:
    """Preprocessor for Dabdoob product images data"""
    
    def __init__(self, input_file: str, output_file: str):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.df = None
        
    def load_data(self) -> pd.DataFrame:
        """Load the raw images CSV file"""
        logger.info(f"Loading data from {self.input_file}")
        
        try:
            self.df = pd.read_csv(self.input_file)
            logger.info(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
            logger.info(f"Unique products: {self.df['product_id'].nunique()}")
            return self.df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def validate_data(self) -> bool:
        """Validate the input data quality"""
        logger.info("Validating data quality...")
        
        issues = []
        
        # Check for missing values
        critical_fields = ['product_id', 'image_uri']
        for field in critical_fields:
            if field in self.df.columns:
                missing_count = self.df[field].isnull().sum()
                if missing_count > 0:
                    issues.append(f"Missing {field}: {missing_count} rows")
        
        # Check for duplicates
        if len(self.df.columns) >= 2:
            duplicates = self.df.duplicated(subset=['product_id', 'image_uri']).sum()
            if duplicates > 0:
                issues.append(f"Found {duplicates} duplicate product-image combinations")
        
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
        
        # Remove duplicates
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates(subset=['product_id', 'image_uri'], keep='first')
        removed = initial_rows - len(self.df)
        if removed > 0:
            logger.info(f"Removed {removed} duplicate entries")
        
        # Clean URLs
        if 'image_uri' in self.df.columns:
            self.df['image_uri'] = self.df['image_uri'].astype(str).str.strip()
            # Ensure HTTPS
            def fix_url(url):
                if pd.isna(url) or url == 'nan':
                    return None
                url = str(url).strip()
                if url and not url.startswith(('http://', 'https://')):
                    return f"https://{url}"
                return url if url else None
            
            self.df['image_uri'] = self.df['image_uri'].apply(fix_url)
            self.df = self.df[self.df['image_uri'].notna()]
        
        # Clean dimensions
        for dim in ['width', 'height']:
            if dim in self.df.columns:
                self.df[dim] = pd.to_numeric(self.df[dim], errors='coerce')
                self.df[dim] = self.df[dim].apply(lambda x: x if x >= 50 else np.nan)
        
        # Clean image order
        if 'image_order' in self.df.columns:
            self.df['image_order'] = pd.to_numeric(self.df['image_order'], errors='coerce')
            self.df['image_order'] = self.df['image_order'].fillna(0)
            self.df['image_order'] = self.df['image_order'].apply(lambda x: max(0, x))
        
        # Sort data
        sort_cols = ['product_id']
        if 'image_order' in self.df.columns:
            sort_cols.append('image_order')
        self.df = self.df.sort_values(sort_cols)
        
        logger.info("Data cleaning completed ✓")
        return self.df
    
    def enhance_data(self) -> pd.DataFrame:
        """Add calculated fields"""
        logger.info("Enhancing data...")
        
        # Add file extension
        if 'image_uri' in self.df.columns:
            self.df['file_extension'] = self.df['image_uri'].apply(
                lambda x: Path(urlparse(str(x)).path).suffix.lower() if pd.notna(x) else None
            )
        
        # Calculate aspect ratio
        if 'width' in self.df.columns and 'height' in self.df.columns:
            self.df['aspect_ratio'] = self.df.apply(
                lambda row: round(row['width'] / row['height'], 2) 
                if pd.notna(row['width']) and pd.notna(row['height']) and row['height'] > 0 
                else None, axis=1
            )
        
        # Add quality score
        def calc_quality(row):
            score = 0
            
            # URL quality (40 points)
            url = str(row.get('image_uri', ''))
            if url.startswith('https://'):
                score += 25
            elif url.startswith('http://'):
                score += 15
            
            if 'cdn' in url.lower():
                score += 15
            
            # Dimensions (40 points)
            width = row.get('width')
            height = row.get('height')
            if pd.notna(width) and pd.notna(height):
                if width >= 800 and height >= 600:
                    score += 40
                elif width >= 400 and height >= 300:
                    score += 30
                elif width >= 200 and height >= 150:
                    score += 20
                else:
                    score += 10
            
            # Format (20 points)
            ext = row.get('file_extension', '').lower()
            if ext in ['.jpg', '.jpeg', '.png', '.webp']:
                score += 20
            elif ext in ['.gif']:
                score += 10
            
            return min(score, 100)
        
        self.df['quality_score'] = self.df.apply(calc_quality, axis=1)
        
        logger.info("Data enhancement completed ✓")
        return self.df
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics"""
        logger.info("Generating summary...")
        
        return {
            'total_images': len(self.df),
            'unique_products': self.df['product_id'].nunique(),
            'avg_images_per_product': round(len(self.df) / self.df['product_id'].nunique(), 2),
            'quality_stats': {
                'mean_score': round(self.df['quality_score'].mean(), 2),
                'high_quality': (self.df['quality_score'] >= 80).sum(),
                'medium_quality': ((self.df['quality_score'] >= 60) & (self.df['quality_score'] < 80)).sum(),
                'low_quality': (self.df['quality_score'] < 60).sum()
            }
        }
    
    def save_data(self) -> None:
        """Save processed data"""
        logger.info(f"Saving to {self.output_file}")
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(self.output_file, index=False)
        logger.info(f"Saved {len(self.df)} images")
    
    def process(self) -> Dict[str, Any]:
        """Run full pipeline"""
        logger.info("Starting images preprocessing...")
        
        self.load_data()
        self.validate_data()
        self.clean_data()
        self.enhance_data()
        summary = self.generate_summary()
        self.save_data()
        
        logger.info("Images preprocessing completed! ✓")
        return summary

def main():
    """Main function"""
    input_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\RealDBData\Images.csv"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\RealDBData\Images_GCP_Ready.csv"
    
    preprocessor = ImagesPreprocessor(input_file, output_file)
    
    try:
        summary = preprocessor.process()
        
        print("\n" + "="*60)
        print("IMAGES PREPROCESSING SUMMARY")
        print("="*60)
        print(f"Total images: {summary['total_images']}")
        print(f"Unique products: {summary['unique_products']}")
        print(f"Avg images per product: {summary['avg_images_per_product']}")
        
        qs = summary['quality_stats']
        print(f"\nQuality Distribution:")
        print(f"  Mean Score: {qs['mean_score']}/100")
        print(f"  High Quality (80+): {qs['high_quality']}")
        print(f"  Medium Quality (60-79): {qs['medium_quality']}")
        print(f"  Low Quality (<60): {qs['low_quality']}")
        
        print(f"\nProcessed file: {output_file}")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise

if __name__ == "__main__":
    main()