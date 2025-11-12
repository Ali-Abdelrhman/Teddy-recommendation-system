#!/usr/bin/env python3
"""
Convert the extracted user events CSV to GCP Retail API format
"""

import json
import csv
import os
from datetime import datetime

def convert_user_events_csv_to_gcp():
    """Convert the DBeaver CSV export to GCP Retail API format"""
    
    csv_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Database\matching_user_events.csv"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\RecommendationAI_NDJSON\user_events_real_products.ndjson"
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        print("\n📋 Instructions:")
        print("1. Run the extract_matching_user_events.sql query in DBeaver")
        print("2. Export results as CSV")
        print("3. Save as 'matching_user_events.csv' in Database folder")
        print("4. Run this script again")
        return False
    
    print("🔄 Converting user events CSV to GCP Retail API format...")
    
    events_created = 0
    
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for row in reader:
                try:
                    event_type = row['eventType']
                    user_id = row['userId']
                    product_id = row['productId']
                    event_time = row['eventTime']
                    session_id = row['sessionId']
                    direct_request = row['directUserRequest']
                    
                    gcp_event = {
                        "eventType": event_type,
                        "userInfo": {
                            "userId": user_id,
                            "directUserRequest": bool(int(direct_request))
                        },
                        "eventTime": event_time,
                        "sessionId": session_id,
                        "visitorId": user_id,
                        "productDetails": [
                            {
                                "product": {
                                    "id": product_id
                                },
                                "quantity": 1
                            }
                        ]
                    }
                    
                    if event_type == "purchase-complete":
                        gcp_event["purchaseTransaction"] = {
                            "id": f"TXN_{session_id}_{product_id}",
                            "revenue": 10.0,
                            "currencyCode": "SAR"
                        }
                    
                    outfile.write(json.dumps(gcp_event, ensure_ascii=False) + '\n')
                    events_created += 1
                    
                except (KeyError, ValueError) as e:
                    print(f"⚠️  Error processing row: {e}")
                    continue
    
    print(f"✅ Created {events_created:,} user events")
    print(f"📁 Saved to: {output_file}")
    
    return True

if __name__ == "__main__":
    convert_user_events_csv_to_gcp()