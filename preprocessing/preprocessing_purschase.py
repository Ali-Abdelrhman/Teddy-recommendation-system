#!/usr/bin/env python3
"""
Purchase Events Preprocessing Script for GCP Retail API
=======================================================

This script processes the raw Purschase.csv file from Dabdoob database queries
and prepares it for GCP Retail API ingestion as user events.

Input: Purschase.csv
Output: Purschase_GCP_Ready.csv

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

class PurchaseEventsPreprocessor:
    """Preprocessor for Dabdoob purchase events data"""
    
    def __init__(self, input_file: str, output_file: str):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.df = None
        
    def load_data(self) -> pd.DataFrame:
        """Load the raw purchase events CSV file"""
        logger.info(f"Loading data from {self.input_file}")
        
        try:
            self.df = pd.read_csv(self.input_file)
            logger.info(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
            logger.info(f"Unique events: {self.df['event_id'].nunique()}")
            logger.info(f"Unique products: {self.df['product_id'].nunique()}")
            logger.info(f"Unique users: {self.df['visitor_id'].nunique()}")
            return self.df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def validate_data(self) -> bool:
        """Validate the input data quality"""
        logger.info("Validating data quality...")
        
        issues = []
        
        # Check for missing values in critical fields
        critical_fields = ['event_id', 'product_id', 'visitor_id', 'event_time', 'quantity', 'unit_price']
        for field in critical_fields:
            if field in self.df.columns:
                missing_count = self.df[field].isnull().sum()
                if missing_count > 0:
                    issues.append(f"Missing {field}: {missing_count} rows")
        
        # Check for duplicate event IDs
        if 'event_id' in self.df.columns:
            duplicates = self.df['event_id'].duplicated().sum()
            if duplicates > 0:
                issues.append(f"Found {duplicates} duplicate event IDs")
        
        # Check for invalid quantities
        if 'quantity' in self.df.columns:
            invalid_quantities = (self.df['quantity'] <= 0).sum()
            if invalid_quantities > 0:
                issues.append(f"Invalid quantities (<=0): {invalid_quantities} rows")
        
        # Check for invalid prices
        if 'unit_price' in self.df.columns:
            invalid_prices = (self.df['unit_price'] <= 0).sum()
            if invalid_prices > 0:
                issues.append(f"Invalid unit prices (<=0): {invalid_prices} rows")
        
        # Check product ID format
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
        
        # Remove duplicate event IDs (keep first occurrence)
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates(subset=['event_id'], keep='first')
        removed_duplicates = initial_rows - len(self.df)
        if removed_duplicates > 0:
            logger.info(f"Removed {removed_duplicates} duplicate event IDs")
        
        # Remove rows with invalid quantities or prices
        valid_quantity = self.df['quantity'] > 0
        valid_price = self.df['unit_price'] > 0
        valid_rows = valid_quantity & valid_price
        
        if not valid_rows.all():
            removed_invalid = (~valid_rows).sum()
            logger.info(f"Removed {removed_invalid} rows with invalid quantity/price")
            self.df = self.df[valid_rows]
        
        # Convert event_time to datetime
        if 'event_time' in self.df.columns:
            self.df['event_time'] = pd.to_datetime(self.df['event_time'], errors='coerce')
            # Remove rows with invalid timestamps
            valid_timestamps = self.df['event_time'].notna()
            if not valid_timestamps.all():
                removed_invalid_ts = (~valid_timestamps).sum()
                logger.info(f"Removed {removed_invalid_ts} rows with invalid timestamps")
                self.df = self.df[valid_timestamps]
        
        # Standardize event type
        if 'event_type' in self.df.columns:
            self.df['event_type'] = self.df['event_type'].str.lower().str.replace('-', '_')
            # Map to GCP standard event types
            event_type_mapping = {
                'purchase_complete': 'purchase-complete',
                'purchase': 'purchase-complete',
                'buy': 'purchase-complete',
                'order': 'purchase-complete'
            }
            self.df['event_type'] = self.df['event_type'].map(event_type_mapping).fillna(self.df['event_type'])
        
        # Clean visitor IDs (ensure they are strings)
        if 'visitor_id' in self.df.columns:
            self.df['visitor_id'] = self.df['visitor_id'].astype(str)
        
        # Clean session IDs
        if 'session_id' in self.df.columns:
            self.df['session_id'] = self.df['session_id'].astype(str)
        
        # Ensure revenue equals quantity * unit_price (or calculate if missing)
        if 'revenue' in self.df.columns and 'quantity' in self.df.columns and 'unit_price' in self.df.columns:
            calculated_revenue = self.df['quantity'] * self.df['unit_price']
            # Fix revenue mismatches
            revenue_mismatch = abs(self.df['revenue'] - calculated_revenue) > 0.01
            if revenue_mismatch.any():
                logger.info(f"Fixed {revenue_mismatch.sum()} revenue calculation mismatches")
                self.df.loc[revenue_mismatch, 'revenue'] = calculated_revenue[revenue_mismatch]
        elif 'quantity' in self.df.columns and 'unit_price' in self.df.columns:
            # Calculate revenue if missing
            self.df['revenue'] = self.df['quantity'] * self.df['unit_price']
            logger.info("Calculated missing revenue values")
        
        # Sort by event time for consistent output
        if 'event_time' in self.df.columns:
            self.df = self.df.sort_values('event_time', ascending=False)  # Most recent first
        
        logger.info("Data cleaning completed ✓")
        return self.df
    
    def enhance_data(self) -> pd.DataFrame:
        """Add calculated fields and enhancements"""
        logger.info("Enhancing data with calculated fields...")
        
        # Add time-based features
        if 'event_time' in self.df.columns:
            self.df['hour_of_day'] = self.df['event_time'].dt.hour
            self.df['day_of_week'] = self.df['event_time'].dt.dayofweek  # 0=Monday
            self.df['day_name'] = self.df['event_time'].dt.day_name()
            self.df['month'] = self.df['event_time'].dt.month
            
            # Calculate days since event
            current_date = datetime.now()
            self.df['days_ago'] = (current_date - self.df['event_time']).dt.days
        
        # Add purchase value categories
        if 'revenue' in self.df.columns:
            def categorize_purchase_value(revenue):
                if pd.isna(revenue):
                    return 'unknown'
                elif revenue < 20:
                    return 'low_value'
                elif revenue < 100:
                    return 'medium_value'
                elif revenue < 500:
                    return 'high_value'
                else:
                    return 'premium_value'
            
            self.df['purchase_value_category'] = self.df['revenue'].apply(categorize_purchase_value)
        
        # Add quantity categories
        if 'quantity' in self.df.columns:
            def categorize_quantity(qty):
                if pd.isna(qty):
                    return 'unknown'
                elif qty == 1:
                    return 'single_item'
                elif qty <= 3:
                    return 'few_items'
                elif qty <= 10:
                    return 'multiple_items'
                else:
                    return 'bulk_purchase'
            
            self.df['quantity_category'] = self.df['quantity'].apply(categorize_quantity)
        
        # Calculate average price per item (unit_price should already be per item)
        if 'unit_price' in self.df.columns:
            self.df['price_per_item'] = self.df['unit_price']  # Already per item
        
        # Add event quality score
        def calculate_event_quality_score(row):
            score = 0
            
            # Complete data (30 points)
            required_fields = ['event_id', 'product_id', 'visitor_id', 'event_time', 'quantity', 'unit_price', 'revenue']
            complete_fields = sum(1 for field in required_fields if pd.notna(row.get(field)))
            score += (complete_fields / len(required_fields)) * 30
            
            # Reasonable values (40 points)
            # Quantity reasonableness
            qty = row.get('quantity', 0)
            if 1 <= qty <= 20:
                score += 15
            elif qty > 0:
                score += 10
            
            # Price reasonableness
            price = row.get('unit_price', 0)
            if 0.1 <= price <= 1000:
                score += 15
            elif price > 0:
                score += 10
            
            # Revenue consistency
            revenue = row.get('revenue', 0)
            expected_revenue = qty * price
            if abs(revenue - expected_revenue) < 0.01:
                score += 10
            elif revenue > 0:
                score += 5
            
            # Session data (20 points)
            if pd.notna(row.get('session_id')):
                score += 10
            if pd.notna(row.get('visitor_id')):
                score += 10
            
            # Recency (10 points)
            days_ago = row.get('days_ago', 0)
            if days_ago <= 30:
                score += 10
            elif days_ago <= 90:
                score += 5
            
            return min(score, 100)
        
        self.df['event_quality_score'] = self.df.apply(calculate_event_quality_score, axis=1)
        
        logger.info("Data enhancement completed ✓")
        return self.df
    
    def generate_summary_stats(self) -> Dict[str, Any]:
        """Generate summary statistics for the processed data"""
        logger.info("Generating summary statistics...")
        
        stats = {
            'total_events': len(self.df),
            'unique_products': self.df['product_id'].nunique(),
            'unique_users': self.df['visitor_id'].nunique(),
            'unique_sessions': self.df['session_id'].nunique() if 'session_id' in self.df.columns else 0,
            'time_range': {},
            'purchase_statistics': {},
            'user_behavior': {},
            'quality_distribution': {}
        }
        
        # Time range analysis
        if 'event_time' in self.df.columns:
            stats['time_range'] = {
                'earliest_event': str(self.df['event_time'].min()),
                'latest_event': str(self.df['event_time'].max()),
                'date_span_days': (self.df['event_time'].max() - self.df['event_time'].min()).days
            }
        
        # Purchase statistics
        if 'revenue' in self.df.columns:
            stats['purchase_statistics'] = {
                'total_revenue': round(self.df['revenue'].sum(), 2),
                'average_order_value': round(self.df['revenue'].mean(), 2),
                'median_order_value': round(self.df['revenue'].median(), 2),
                'max_order_value': round(self.df['revenue'].max(), 2),
                'min_order_value': round(self.df['revenue'].min(), 2)
            }
        
        if 'quantity' in self.df.columns:
            stats['purchase_statistics'].update({
                'total_items_sold': int(self.df['quantity'].sum()),
                'average_items_per_order': round(self.df['quantity'].mean(), 2),
                'max_items_per_order': int(self.df['quantity'].max())
            })
        
        # User behavior analysis
        purchases_per_user = self.df.groupby('visitor_id').size()
        stats['user_behavior'] = {
            'average_purchases_per_user': round(purchases_per_user.mean(), 2),
            'max_purchases_per_user': purchases_per_user.max(),
            'single_purchase_users': (purchases_per_user == 1).sum(),
            'repeat_customers': (purchases_per_user > 1).sum()
        }
        
        # Quality distribution
        if 'event_quality_score' in self.df.columns:
            stats['quality_distribution'] = {
                'mean_score': round(self.df['event_quality_score'].mean(), 2),
                'high_quality_events': (self.df['event_quality_score'] >= 80).sum(),
                'medium_quality_events': ((self.df['event_quality_score'] >= 60) & (self.df['event_quality_score'] < 80)).sum(),
                'low_quality_events': (self.df['event_quality_score'] < 60).sum()
            }
        
        # Purchase value distribution
        if 'purchase_value_category' in self.df.columns:
            stats['purchase_value_distribution'] = self.df['purchase_value_category'].value_counts().to_dict()
        
        # Popular shopping times
        if 'hour_of_day' in self.df.columns:
            popular_hours = self.df['hour_of_day'].value_counts().head(3)
            stats['popular_shopping_hours'] = popular_hours.to_dict()
        
        return stats
    
    def save_processed_data(self) -> None:
        """Save the processed data to CSV"""
        logger.info(f"Saving processed data to {self.output_file}")
        
        # Create output directory if it doesn't exist
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to CSV
        self.df.to_csv(self.output_file, index=False)
        logger.info(f"Saved {len(self.df)} events to {self.output_file}")
    
    def process(self) -> Dict[str, Any]:
        """Run the complete preprocessing pipeline"""
        logger.info("Starting purchase events preprocessing pipeline...")
        
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
        
        logger.info("Purchase events preprocessing completed successfully! ✓")
        return summary

def main():
    """Main execution function"""
    
    # File paths
    input_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\RealDBData\Purschase.csv"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\RealDBData\Purschase_GCP_Ready.csv"
    
    # Initialize preprocessor
    preprocessor = PurchaseEventsPreprocessor(input_file, output_file)
    
    try:
        # Run preprocessing
        summary = preprocessor.process()
        
        # Print summary
        print("\n" + "="*60)
        print("PURCHASE EVENTS PREPROCESSING SUMMARY")
        print("="*60)
        print(f"Total events processed: {summary['total_events']}")
        print(f"Unique products: {summary['unique_products']}")
        print(f"Unique users: {summary['unique_users']}")
        print(f"Unique sessions: {summary['unique_sessions']}")
        
        if 'time_range' in summary:
            tr = summary['time_range']
            print(f"\nTime Range:")
            print(f"  From: {tr['earliest_event']}")
            print(f"  To: {tr['latest_event']}")
            print(f"  Span: {tr['date_span_days']} days")
        
        if 'purchase_statistics' in summary:
            ps = summary['purchase_statistics']
            print(f"\nPurchase Statistics:")
            print(f"  Total Revenue: {ps.get('total_revenue', 0)} SAR")
            print(f"  Average Order Value: {ps.get('average_order_value', 0)} SAR")
            print(f"  Total Items Sold: {ps.get('total_items_sold', 0)}")
            print(f"  Avg Items per Order: {ps.get('average_items_per_order', 0)}")
        
        if 'user_behavior' in summary:
            ub = summary['user_behavior']
            print(f"\nUser Behavior:")
            print(f"  Avg Purchases per User: {ub['average_purchases_per_user']}")
            print(f"  Single Purchase Users: {ub['single_purchase_users']}")
            print(f"  Repeat Customers: {ub['repeat_customers']}")
        
        if 'quality_distribution' in summary:
            qd = summary['quality_distribution']
            print(f"\nEvent Quality Distribution:")
            print(f"  Mean Score: {qd['mean_score']}/100")
            print(f"  High Quality (80+): {qd['high_quality_events']} events")
            print(f"  Medium Quality (60-79): {qd['medium_quality_events']} events")
            print(f"  Low Quality (<60): {qd['low_quality_events']} events")
        
        if 'popular_shopping_hours' in summary:
            print(f"\nPopular Shopping Hours:")
            for hour, count in summary['popular_shopping_hours'].items():
                print(f"  {hour}:00 - {count} purchases")
        
        print(f"\nProcessed file saved to: {output_file}")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise

if __name__ == "__main__":
    main()