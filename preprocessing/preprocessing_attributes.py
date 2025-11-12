                        #!/usr/bin/env python3
"""
Attributes Preprocessing Script for GCP Retail API
==================================================

This script processes the raw Attributes.csv file from Dabdoob database queries
and transforms it into the format required by GCP Retail API custom attributes.

Input: Attributes.csv (normalized format - one row per product-attribute combination)
Output: Attributes_GCP_Ready.csv (denormalized format - one row per product with JSON arrays)

Author: Data Engineering Team
Date: October 21, 2025
"""

import pandas as pd
import json
import numpy as np
from pathlib import Path
import logging
from typing import Dict, List, Any

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AttributesPreprocessor:
    """Preprocessor for Dabdoob product attributes data"""
    
    def __init__(self, input_file: str, output_file: str):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.df = None
        self.processed_df = None
        
    def load_data(self) -> pd.DataFrame:
        """Load the raw attributes CSV file"""
        logger.info(f"Loading data from {self.input_file}")
        
        try:
            self.df = pd.read_csv(self.input_file)
            logger.info(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
            logger.info(f"Unique products: {self.df['product_id'].nunique()}")
            logger.info(f"Attribute types: {self.df['attribute_name'].unique()}")
            return self.df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def validate_data(self) -> bool:
        """Validate the input data quality"""
        logger.info("Validating data quality...")
        
        issues = []
        
        # Check for missing values
        missing_values = self.df.isnull().sum()
        if missing_values.any():
            issues.append(f"Missing values found: {missing_values[missing_values > 0].to_dict()}")
        
        # Check for duplicate combinations
        duplicates = self.df.duplicated(subset=['product_id', 'attribute_name', 'attribute_value']).sum()
        if duplicates > 0:
            issues.append(f"Found {duplicates} duplicate product-attribute combinations")
        
        # Check product ID format
        invalid_ids = self.df[~self.df['product_id'].str.match(r'PROD\d{6}')]['product_id'].unique()
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
        
        # Remove duplicates
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates(subset=['product_id', 'attribute_name', 'attribute_value'])
        removed_duplicates = initial_rows - len(self.df)
        if removed_duplicates > 0:
            logger.info(f"Removed {removed_duplicates} duplicate rows")
        
        # Clean attribute values
        self.df['attribute_value'] = self.df['attribute_value'].str.strip()
        self.df['attribute_value'] = self.df['attribute_value'].str.replace('"', '')
        
        # Standardize attribute names for GCP
        self.df['gcp_attribute_name'] = self.df['attribute_name'].str.lower().str.replace(' ', '_')
        
        # Sort for consistent processing
        self.df = self.df.sort_values(['product_id', 'attribute_name', 'attribute_value'])
        
        logger.info("Data cleaning completed ✓")
        return self.df
    
    def transform_attributes(self) -> pd.DataFrame:
        """Transform normalized attributes to GCP format (one row per product)"""
        logger.info("Transforming attributes to GCP format...")
        
        # Create a list to store transformed records
        transformed_records = []
        
        # Group by product and process each group
        for product_id, group in self.df.groupby('product_id'):
            record = {'product_id': product_id}
            
            # Process each attribute type
            for attr_name in group['attribute_name'].unique():
                attr_data = group[group['attribute_name'] == attr_name]
                values = sorted(attr_data['attribute_value'].unique().tolist())
                
                # Use GCP-friendly attribute names
                gcp_attr_name = attr_name.lower().replace(' ', '_')
                
                # Store as array if multiple values, single value otherwise
                if len(values) > 1:
                    record[gcp_attr_name] = json.dumps(values)  # Store as JSON string for CSV compatibility
                    record[f'{gcp_attr_name}_count'] = len(values)
                else:
                    record[gcp_attr_name] = values[0]
                    record[f'{gcp_attr_name}_count'] = 1
            
            transformed_records.append(record)
        
        # Convert to DataFrame
        self.processed_df = pd.DataFrame(transformed_records)
        
        logger.info(f"Transformed to {len(self.processed_df)} products with aggregated attributes")
        return self.processed_df
    
    def generate_summary_stats(self) -> Dict[str, Any]:
        """Generate summary statistics for the processed data"""
        logger.info("Generating summary statistics...")
        
        stats = {
            'total_products': len(self.processed_df),
            'attribute_coverage': {},
            'value_distributions': {}
        }
        
        # Analyze attribute coverage
        for col in self.processed_df.columns:
            if col not in ['product_id'] and not col.endswith('_count'):
                non_null_count = self.processed_df[col].notna().sum()
                coverage_pct = (non_null_count / len(self.processed_df)) * 100
                stats['attribute_coverage'][col] = {
                    'products_with_attribute': non_null_count,
                    'coverage_percentage': round(coverage_pct, 2)
                }
        
        # Analyze value distributions for key attributes
        if 'gender' in self.processed_df.columns:
            gender_dist = self.processed_df['gender'].value_counts().to_dict()
            stats['value_distributions']['gender'] = gender_dist
        
        if 'age' in self.processed_df.columns:
            # Parse age values from JSON arrays
            age_values = []
            for val in self.processed_df['age'].dropna():
                if val.startswith('['):
                    age_values.extend(json.loads(val))
                else:
                    age_values.append(val)
            age_dist = pd.Series(age_values).value_counts().to_dict()
            stats['value_distributions']['age'] = age_dist
        
        return stats
    
    def save_processed_data(self) -> None:
        """Save the processed data to CSV"""
        logger.info(f"Saving processed data to {self.output_file}")
        
        # Create output directory if it doesn't exist
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to CSV
        self.processed_df.to_csv(self.output_file, index=False)
        logger.info(f"Saved {len(self.processed_df)} products to {self.output_file}")
    
    def process(self) -> Dict[str, Any]:
        """Run the complete preprocessing pipeline"""
        logger.info("Starting attributes preprocessing pipeline...")
        
        # Load and validate data
        self.load_data()
        self.validate_data()
        
        # Clean and transform data
        self.clean_data()
        self.transform_attributes()
        
        # Generate summary
        summary = self.generate_summary_stats()
        
        # Save processed data
        self.save_processed_data()
        
        logger.info("Attributes preprocessing completed successfully! ✓")
        return summary

def main():
    """Main execution function"""
    
    # File paths
    input_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\RealDBData\Attributes.csv"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\RealDBData\Attributes_GCP_Ready.csv"
    
    # Initialize preprocessor
    preprocessor = AttributesPreprocessor(input_file, output_file)
    
    try:
        # Run preprocessing
        summary = preprocessor.process()
        
        # Print summary
        print("\n" + "="*60)
        print("ATTRIBUTES PREPROCESSING SUMMARY")
        print("="*60)
        print(f"Total products processed: {summary['total_products']}")
        print("\nAttribute Coverage:")
        for attr, stats in summary['attribute_coverage'].items():
            print(f"  {attr}: {stats['products_with_attribute']} products ({stats['coverage_percentage']}%)")
        
        print("\nValue Distributions:")
        for attr, dist in summary['value_distributions'].items():
            print(f"  {attr}: {dict(list(dist.items())[:5])}...")  # Show top 5
        
        print(f"\nProcessed file saved to: {output_file}")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise

if __name__ == "__main__":
    main()