#!/usr/bin/env python3
"""
Pricing Preprocessing Script for GCP Retail API
===============================================

This script processes the raw Pricing.csv file from Dabdoob database queries
and prepares it for GCP Retail API ingestion, keeping only the latest price per product.

Input: Pricing.csv
Output: Pricing_GCP_Ready.csv

Author: Data Engineering Team
Date: October 21, 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PricingPreprocessor:
    """Preprocessor for Dabdoob product pricing data"""
    
    def __init__(self, input_file: str, output_file: str):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.df = None
        
    def load_data(self) -> pd.DataFrame:
        """Load the raw pricing CSV file"""
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
        
        # Check for missing values in critical fields
        critical_fields = ['product_id', 'price', 'currency_code']
        for field in critical_fields:
            if field in self.df.columns:
                missing_count = self.df[field].isnull().sum()
                if missing_count > 0:
                    issues.append(f"Missing {field}: {missing_count} rows")
        
        # Check for invalid prices
        if 'price' in self.df.columns:
            invalid_prices = (self.df['price'] <= 0).sum()
            if invalid_prices > 0:
                issues.append(f"Invalid prices (<=0): {invalid_prices} rows")
        
        # Check for invalid quality scores
        if 'quality_score' in self.df.columns:
            invalid_scores = ((self.df['quality_score'] < 0) | (self.df['quality_score'] > 10000)).sum()
            if invalid_scores > 0:
                issues.append(f"Suspicious quality scores: {invalid_scores} rows")
        
        # Check for product ID format
        if 'product_id' in self.df.columns:
            invalid_ids = self.df[~self.df['product_id'].str.match(r'PROD\d{6}', na=False)]['product_id'].unique()
            if len(invalid_ids) > 0:
                issues.append(f"Invalid product ID format: {invalid_ids[:5]}...")
        
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
        
        # Remove rows with invalid prices
        initial_rows = len(self.df)
        self.df = self.df[self.df['price'] > 0]
        removed_invalid_prices = initial_rows - len(self.df)
        if removed_invalid_prices > 0:
            logger.info(f"Removed {removed_invalid_prices} rows with invalid prices")
        
        # Convert price_date to datetime
        if 'price_date' in self.df.columns:
            self.df['price_date'] = pd.to_datetime(self.df['price_date'], errors='coerce')
            # Remove rows with invalid dates
            valid_dates = self.df['price_date'].notna()
            self.df = self.df[valid_dates]
            if not valid_dates.all():
                logger.info(f"Removed {(~valid_dates).sum()} rows with invalid dates")
        
        # Clean currency codes
        if 'currency_code' in self.df.columns:
            self.df['currency_code'] = self.df['currency_code'].str.upper().str.strip()
            # Standardize common currency codes
            currency_mapping = {
                'SAR': 'SAR',
                'USD': 'USD',
                'EUR': 'EUR',
                'AED': 'AED'
            }
            self.df['currency_code'] = self.df['currency_code'].map(currency_mapping).fillna(self.df['currency_code'])
        
        # Clean quality scores (handle outliers)
        if 'quality_score' in self.df.columns:
            # Cap quality scores at reasonable limits
            self.df['quality_score'] = self.df['quality_score'].clip(lower=0, upper=1000)
            
            # Handle the outlier we saw in the data (5387 -> reasonable value)
            outlier_threshold = 1000
            outliers = self.df['quality_score'] > outlier_threshold
            if outliers.any():
                logger.info(f"Found {outliers.sum()} outlier quality scores, capping at {outlier_threshold}")
                self.df.loc[outliers, 'quality_score'] = 100  # Set to default good score
        
        # Ensure original_price is not less than price
        if 'original_price' in self.df.columns and 'price' in self.df.columns:
            # If original_price is missing, set it to current price
            self.df['original_price'] = self.df['original_price'].fillna(self.df['price'])
            
            # If original_price is less than current price, set to current price
            invalid_original = self.df['original_price'] < self.df['price']
            if invalid_original.any():
                logger.info(f"Fixed {invalid_original.sum()} cases where original_price < price")
                self.df.loc[invalid_original, 'original_price'] = self.df.loc[invalid_original, 'price']
        
        # Fill missing country_id
        if 'country_id' in self.df.columns:
            self.df['country_id'] = self.df['country_id'].fillna(1)  # Default to first country
        
        logger.info("Data cleaning completed ✓")
        return self.df
    
    def deduplicate_prices(self) -> pd.DataFrame:
        """Keep only the latest price per product"""
        logger.info("Deduplicating prices (keeping latest per product)...")
        
        initial_rows = len(self.df)
        
        # Sort by product_id and price_date (latest first)
        self.df = self.df.sort_values(['product_id', 'price_date'], ascending=[True, False])
        
        # Keep only the latest price per product
        self.df = self.df.drop_duplicates(subset=['product_id'], keep='first')
        
        removed_duplicates = initial_rows - len(self.df)
        logger.info(f"Removed {removed_duplicates} duplicate/older price entries")
        logger.info(f"Kept latest prices for {len(self.df)} unique products")
        
        return self.df
    
    def enhance_data(self) -> pd.DataFrame:
        """Add calculated fields and enhancements"""
        logger.info("Enhancing data with calculated fields...")
        
        # Calculate discount percentage
        if 'price' in self.df.columns and 'original_price' in self.df.columns:
            self.df['discount_percentage'] = ((self.df['original_price'] - self.df['price']) / self.df['original_price'] * 100).round(2)
            # Ensure discount percentage is not negative
            self.df['discount_percentage'] = self.df['discount_percentage'].clip(lower=0)
        
        # Add price category
        if 'price' in self.df.columns:
            def categorize_price(price):
                if pd.isna(price):
                    return 'unknown'
                elif price < 10:
                    return 'budget'
                elif price < 50:
                    return 'affordable'
                elif price < 200:
                    return 'moderate'
                elif price < 500:
                    return 'premium'
                else:
                    return 'luxury'
            
            self.df['price_category'] = self.df['price'].apply(categorize_price)
        
        # Calculate price freshness (days since last update)
        if 'price_date' in self.df.columns:
            current_date = datetime.now()
            self.df['days_since_update'] = (current_date - self.df['price_date']).dt.days
        
        # Add pricing quality score
        def calculate_pricing_quality_score(row):
            score = 0
            
            # Currency standard (20 points)
            if row.get('currency_code') in ['SAR', 'USD', 'EUR']:
                score += 20
            
            # Price reasonableness (30 points)
            price = row.get('price', 0)
            if 1 <= price <= 10000:  # Reasonable price range
                score += 30
            elif price > 0:
                score += 15
            
            # Original price consistency (20 points)
            original_price = row.get('original_price', 0)
            if original_price >= price and original_price > 0:
                score += 20
            elif original_price > 0:
                score += 10
            
            # Data freshness (20 points)
            days_old = row.get('days_since_update', 0)
            if days_old <= 7:
                score += 20
            elif days_old <= 30:
                score += 15
            elif days_old <= 90:
                score += 10
            else:
                score += 5
            
            # Quality score validity (10 points)
            quality_score = row.get('quality_score', 0)
            if 50 <= quality_score <= 100:
                score += 10
            elif quality_score > 0:
                score += 5
            
            return min(score, 100)
        
        self.df['pricing_quality_score'] = self.df.apply(calculate_pricing_quality_score, axis=1)
        
        # Sort by product ID for consistent output
        self.df = self.df.sort_values('product_id')
        
        logger.info("Data enhancement completed ✓")
        return self.df
    
    def generate_summary_stats(self) -> Dict[str, Any]:
        """Generate summary statistics for the processed data"""
        logger.info("Generating summary statistics...")
        
        stats = {
            'total_products': len(self.df),
            'price_statistics': {},
            'currency_distribution': {},
            'quality_distribution': {},
            'freshness_analysis': {},
            'discount_analysis': {}
        }
        
        # Price statistics
        if 'price' in self.df.columns:
            stats['price_statistics'] = {
                'mean_price': round(self.df['price'].mean(), 2),
                'median_price': round(self.df['price'].median(), 2),
                'min_price': round(self.df['price'].min(), 2),
                'max_price': round(self.df['price'].max(), 2),
                'std_price': round(self.df['price'].std(), 2)
            }
        
        # Currency distribution
        if 'currency_code' in self.df.columns:
            stats['currency_distribution'] = self.df['currency_code'].value_counts().to_dict()
        
        # Quality score distribution
        if 'pricing_quality_score' in self.df.columns:
            stats['quality_distribution'] = {
                'mean_score': round(self.df['pricing_quality_score'].mean(), 2),
                'high_quality_prices': (self.df['pricing_quality_score'] >= 80).sum(),
                'medium_quality_prices': ((self.df['pricing_quality_score'] >= 60) & (self.df['pricing_quality_score'] < 80)).sum(),
                'low_quality_prices': (self.df['pricing_quality_score'] < 60).sum()
            }
        
        # Price freshness analysis
        if 'days_since_update' in self.df.columns:
            stats['freshness_analysis'] = {
                'avg_days_since_update': round(self.df['days_since_update'].mean(), 1),
                'fresh_prices_7d': (self.df['days_since_update'] <= 7).sum(),
                'recent_prices_30d': (self.df['days_since_update'] <= 30).sum(),
                'old_prices_90d_plus': (self.df['days_since_update'] > 90).sum()
            }
        
        # Discount analysis
        if 'discount_percentage' in self.df.columns:
            discounted_items = self.df[self.df['discount_percentage'] > 0]
            stats['discount_analysis'] = {
                'items_with_discount': len(discounted_items),
                'avg_discount_percentage': round(discounted_items['discount_percentage'].mean(), 2) if len(discounted_items) > 0 else 0,
                'max_discount_percentage': round(discounted_items['discount_percentage'].max(), 2) if len(discounted_items) > 0 else 0
            }
        
        # Price category distribution
        if 'price_category' in self.df.columns:
            stats['price_category_distribution'] = self.df['price_category'].value_counts().to_dict()
        
        return stats
    
    def save_processed_data(self) -> None:
        """Save the processed data to CSV"""
        logger.info(f"Saving processed data to {self.output_file}")
        
        # Create output directory if it doesn't exist
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to CSV
        self.df.to_csv(self.output_file, index=False)
        logger.info(f"Saved {len(self.df)} pricing records to {self.output_file}")
    
    def process(self) -> Dict[str, Any]:
        """Run the complete preprocessing pipeline"""
        logger.info("Starting pricing preprocessing pipeline...")
        
        # Load and validate data
        self.load_data()
        self.validate_data()
        
        # Clean and deduplicate data
        self.clean_data()
        self.deduplicate_prices()
        self.enhance_data()
        
        # Generate summary
        summary = self.generate_summary_stats()
        
        # Save processed data
        self.save_processed_data()
        
        logger.info("Pricing preprocessing completed successfully! ✓")
        return summary

def main():
    """Main execution function"""
    
    # File paths
    input_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\RealDBData\Pricing.csv"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\RealDBData\Pricing_GCP_Ready.csv"
    
    # Initialize preprocessor
    preprocessor = PricingPreprocessor(input_file, output_file)
    
    try:
        # Run preprocessing
        summary = preprocessor.process()
        
        # Print summary
        print("\n" + "="*60)
        print("PRICING PREPROCESSING SUMMARY")
        print("="*60)
        print(f"Total products with pricing: {summary['total_products']}")
        
        if 'price_statistics' in summary:
            ps = summary['price_statistics']
            print(f"\nPrice Statistics:")
            print(f"  Average Price: {ps['mean_price']} {list(summary.get('currency_distribution', {}).keys())[0] if summary.get('currency_distribution') else 'SAR'}")
            print(f"  Price Range: {ps['min_price']} - {ps['max_price']}")
            print(f"  Median Price: {ps['median_price']}")
        
        if 'currency_distribution' in summary:
            print(f"\nCurrency Distribution:")
            for currency, count in summary['currency_distribution'].items():
                print(f"  {currency}: {count} products")
        
        if 'quality_distribution' in summary:
            qd = summary['quality_distribution']
            print(f"\nPricing Quality Distribution:")
            print(f"  Mean Score: {qd['mean_score']}/100")
            print(f"  High Quality (80+): {qd['high_quality_prices']} products")
            print(f"  Medium Quality (60-79): {qd['medium_quality_prices']} products")
            print(f"  Low Quality (<60): {qd['low_quality_prices']} products")
        
        if 'freshness_analysis' in summary:
            fa = summary['freshness_analysis']
            print(f"\nPrice Freshness:")
            print(f"  Average age: {fa['avg_days_since_update']} days")
            print(f"  Fresh (≤7 days): {fa['fresh_prices_7d']} products")
            print(f"  Recent (≤30 days): {fa['recent_prices_30d']} products")
        
        if 'discount_analysis' in summary:
            da = summary['discount_analysis']
            print(f"\nDiscount Analysis:")
            print(f"  Products with discounts: {da['items_with_discount']}")
            if da['items_with_discount'] > 0:
                print(f"  Average discount: {da['avg_discount_percentage']}%")
                print(f"  Maximum discount: {da['max_discount_percentage']}%")
        
        print(f"\nProcessed file saved to: {output_file}")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise

if __name__ == "__main__":
    main()