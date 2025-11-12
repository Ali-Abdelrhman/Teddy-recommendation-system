#!/usr/bin/env python3
"""
User Events Data Cleaning and NDJSON Conversion Script
======================================================
This script processes CSV user events data, performs quality cleaning,
and converts to NDJSON format for Google Cloud Recommendation AI import.

Author: GitHub Copilot
Date: October 22, 2025
"""

import pandas as pd
import json
import os
from datetime import datetime
import re
from typing import Dict, List, Any
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('user_events_preprocessing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class UserEventsPreprocessor:
    """Handles cleaning and conversion of user events data to NDJSON format."""
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.csv_path = os.path.join(base_path, "Test CSVs", "SampleDBUserData")
        self.ndjson_path = os.path.join(base_path, "RecommendationAI_NDJSON")
        
        # Data quality stats
        self.stats = {
            'input_events': 0,
            'cleaned_events': 0,
            'removed_events': 0,
            'existing_events': 0,
            'final_events': 0
        }
        
    def load_existing_events(self) -> List[Dict]:
        """Load existing user_events.ndjson file."""
        existing_file = os.path.join(self.ndjson_path, "user_events.ndjson")
        existing_events = []
        
        if os.path.exists(existing_file):
            logger.info(f"Loading existing events from {existing_file}")
            with open(existing_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            event = json.loads(line)
                            existing_events.append(event)
                        except json.JSONDecodeError as e:
                            logger.warning(f"Skipping invalid JSON line: {e}")
            
            self.stats['existing_events'] = len(existing_events)
            logger.info(f"Loaded {len(existing_events)} existing events")
        else:
            logger.info("No existing user_events.ndjson file found")
            
        return existing_events
    
    def load_csv_data(self) -> pd.DataFrame:
        """Load and combine all CSV files."""
        csv_files = [
            "detail-page-view events.csv",
            "home-page-view events.csv", 
            "home-page-view from activity table.csv",
            "wishlist products for add-to-cart events.csv"
        ]
        
        all_data = []
        
        for file in csv_files:
            file_path = os.path.join(self.csv_path, file)
            if os.path.exists(file_path):
                logger.info(f"Loading {file}")
                try:
                    df = pd.read_csv(file_path)
                    logger.info(f"  - Loaded {len(df)} rows from {file}")
                    all_data.append(df)
                except Exception as e:
                    logger.error(f"Error loading {file}: {e}")
            else:
                logger.warning(f"File not found: {file}")
        
        if not all_data:
            raise FileNotFoundError("No CSV files found to process")
        
        # Combine all dataframes
        combined_df = pd.concat(all_data, ignore_index=True)
        self.stats['input_events'] = len(combined_df)
        logger.info(f"Combined total: {len(combined_df)} events")
        
        return combined_df
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate the CSV data."""
        logger.info("Starting data cleaning...")
        initial_count = len(df)
        
        # 1. Remove rows with missing essential data
        logger.info("Removing rows with missing essential data...")
        before = len(df)
        df = df.dropna(subset=['eventType', 'userId', 'eventTime', 'sessionId'])
        logger.info(f"  - Removed {before - len(df)} rows with missing essential fields")
        
        # 2. Clean userId - remove quotes and handle guest users
        logger.info("Cleaning user IDs...")
        df['userId'] = df['userId'].astype(str).str.strip().str.replace('"', '')
        
        # 3. Clean productId - handle empty strings for home-page-view
        logger.info("Cleaning product IDs...")
        df['productId'] = df['productId'].astype(str).str.strip().str.replace('"', '')
        
        # For home-page-view events, empty productId is expected
        home_page_mask = df['eventType'] == 'home-page-view'
        df.loc[home_page_mask, 'productId'] = ''
        
        # For other events, remove rows with empty/invalid productId
        non_home_page_mask = ~home_page_mask
        invalid_product_mask = (df['productId'].isin(['', 'nan', 'None', 'NULL'])) & non_home_page_mask
        
        before = len(df)
        df = df[~invalid_product_mask]
        logger.info(f"  - Removed {before - len(df)} rows with invalid product IDs")
        
        # 4. Validate product ID format (should start with PROD)
        logger.info("Validating product ID format...")
        valid_product_mask = (
            (df['eventType'] == 'home-page-view') |  # Home page views don't need product ID
            (df['productId'].str.startswith('PROD') & (df['productId'].str.len() == 10))
        )
        
        before = len(df)
        df = df[valid_product_mask]
        logger.info(f"  - Removed {before - len(df)} rows with invalid product ID format")
        
        # 5. Clean eventTime format
        logger.info("Cleaning event times...")
        df['eventTime'] = pd.to_datetime(df['eventTime']).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # 6. Clean sessionId
        logger.info("Cleaning session IDs...")
        df['sessionId'] = df['sessionId'].astype(str).str.strip()
        
        # 7. Ensure directUserRequest is numeric
        df['directUserRequest'] = pd.to_numeric(df['directUserRequest'], errors='coerce').fillna(1).astype(int)
        
        # 8. Remove duplicates
        logger.info("Removing duplicates...")
        before = len(df)
        df = df.drop_duplicates(subset=['eventType', 'userId', 'productId', 'eventTime'], keep='first')
        logger.info(f"  - Removed {before - len(df)} duplicate events")
        
        # 9. Sort by eventTime (newest first)
        df = df.sort_values('eventTime', ascending=False)
        
        self.stats['cleaned_events'] = len(df)
        self.stats['removed_events'] = initial_count - len(df)
        
        logger.info(f"Data cleaning complete:")
        logger.info(f"  - Initial events: {initial_count}")
        logger.info(f"  - Cleaned events: {len(df)}")
        logger.info(f"  - Removed events: {initial_count - len(df)}")
        
        return df
    
    def convert_to_ndjson_format(self, df: pd.DataFrame) -> List[Dict]:
        """Convert cleaned CSV data to NDJSON format for Google Cloud."""
        logger.info("Converting to NDJSON format...")
        
        ndjson_events = []
        
        for _, row in df.iterrows():
            event_type = row['eventType']
            
            # Base event structure
            event = {
                "eventType": event_type,
                "userInfo": {
                    "userId": str(row['userId']),
                    "directUserRequest": bool(row['directUserRequest'])
                },
                "eventTime": row['eventTime'],
                "sessionId": row['sessionId']
            }
            
            # Add product details for events that require them
            if event_type in ['detail-page-view', 'add-to-cart'] and row['productId']:
                event["productEventDetail"] = {
                    "productDetails": [
                        {
                            "product": {
                                "id": row['productId']
                            }
                        }
                    ]
                }
                
                # Add quantity for add-to-cart events
                if event_type == 'add-to-cart':
                    event["productEventDetail"]["productDetails"][0]["quantity"] = 1
            
            ndjson_events.append(event)
        
        logger.info(f"Converted {len(ndjson_events)} events to NDJSON format")
        return ndjson_events
    
    def merge_with_existing_events(self, new_events: List[Dict], existing_events: List[Dict]) -> List[Dict]:
        """Merge new events with existing events, avoiding duplicates."""
        logger.info("Merging with existing events...")
        
        # Create a set of existing event signatures for deduplication
        existing_signatures = set()
        for event in existing_events:
            # Create a signature based on event type, user, product (if exists), and time
            product_id = ""
            if "productEventDetail" in event and "productDetails" in event["productEventDetail"]:
                if event["productEventDetail"]["productDetails"]:
                    product_id = event["productEventDetail"]["productDetails"][0].get("product", {}).get("id", "")
            
            signature = f"{event['eventType']}|{event['userInfo']['userId']}|{product_id}|{event['eventTime']}"
            existing_signatures.add(signature)
        
        # Filter new events to avoid duplicates
        merged_events = existing_events.copy()
        added_count = 0
        
        for event in new_events:
            # Create signature for new event
            product_id = ""
            if "productEventDetail" in event and "productDetails" in event["productEventDetail"]:
                if event["productEventDetail"]["productDetails"]:
                    product_id = event["productEventDetail"]["productDetails"][0].get("product", {}).get("id", "")
            
            signature = f"{event['eventType']}|{event['userInfo']['userId']}|{product_id}|{event['eventTime']}"
            
            if signature not in existing_signatures:
                merged_events.append(event)
                existing_signatures.add(signature)
                added_count += 1
        
        logger.info(f"Added {added_count} new unique events")
        logger.info(f"Total events after merge: {len(merged_events)}")
        
        return merged_events
    
    def save_ndjson(self, events: List[Dict], filename: str = "user_events_combined.ndjson"):
        """Save events to NDJSON file."""
        output_path = os.path.join(self.ndjson_path, filename)
        
        # Create directory if it doesn't exist
        os.makedirs(self.ndjson_path, exist_ok=True)
        
        logger.info(f"Saving {len(events)} events to {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for event in events:
                f.write(json.dumps(event, ensure_ascii=False) + '\n')
        
        self.stats['final_events'] = len(events)
        logger.info(f"Successfully saved to {output_path}")
        
        return output_path
    
    def generate_summary_report(self) -> str:
        """Generate a summary report of the preprocessing."""
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                    USER EVENTS PREPROCESSING SUMMARY         ║
╠══════════════════════════════════════════════════════════════╣
║ Input Events:           {self.stats['input_events']:>10,}                    ║
║ Existing Events:        {self.stats['existing_events']:>10,}                    ║
║ Cleaned Events:         {self.stats['cleaned_events']:>10,}                    ║
║ Removed Events:         {self.stats['removed_events']:>10,}                    ║
║ Final Combined Events:  {self.stats['final_events']:>10,}                    ║
║                                                              ║
║ Data Quality:           {((self.stats['cleaned_events']/self.stats['input_events'])*100) if self.stats['input_events'] > 0 else 0:.1f}% retained          ║
║ Total Growth:           {self.stats['final_events'] - self.stats['existing_events']:>+10,} events              ║
║                                                              ║
║ Status: ✅ SUCCESS - Ready for Google Cloud Import          ║
╚══════════════════════════════════════════════════════════════╝
        """
        return report
    
    def process(self):
        """Main processing pipeline."""
        try:
            logger.info("Starting user events preprocessing pipeline...")
            
            # Step 1: Load existing events
            existing_events = self.load_existing_events()
            
            # Step 2: Load CSV data
            df = self.load_csv_data()
            
            # Step 3: Clean data
            cleaned_df = self.clean_data(df)
            
            # Step 4: Convert to NDJSON format
            new_ndjson_events = self.convert_to_ndjson_format(cleaned_df)
            
            # Step 5: Merge with existing events
            final_events = self.merge_with_existing_events(new_ndjson_events, existing_events)
            
            # Step 6: Save combined NDJSON
            output_file = self.save_ndjson(final_events)
            
            # Step 7: Generate summary
            summary = self.generate_summary_report()
            logger.info(summary)
            
            # Save summary to file
            summary_file = os.path.join(self.ndjson_path, "preprocessing_summary.txt")
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary)
                f.write(f"\n\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                f.write(f"\nOutput file: {output_file}")
            
            logger.info(f"Summary saved to: {summary_file}")
            logger.info("✅ Preprocessing completed successfully!")
            
            return output_file
            
        except Exception as e:
            logger.error(f"❌ Error during preprocessing: {e}")
            raise

def main():
    """Main function to run the preprocessing."""
    base_path = r"c:\Users\Ahmed\Downloads\Teddy recommendation system"
    
    processor = UserEventsPreprocessor(base_path)
    output_file = processor.process()
    
    print(f"\n🎯 Processing complete! Output file: {output_file}")
    print("📊 Check the log file and summary for detailed statistics.")

if __name__ == "__main__":
    main()