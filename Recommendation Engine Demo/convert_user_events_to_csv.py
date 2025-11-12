import json
import csv
import os

def user_events_ndjson_to_csv(ndjson_file_path, csv_file_path):
    """
    Convert user events NDJSON file to CSV format
    """
    # Read all events from NDJSON
    events = []
    
    with open(ndjson_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                event = json.loads(line)
                events.append(event)
    
    if not events:
        print("No events found in the file")
        return
    
    # Define the CSV columns based on the event structure
    fieldnames = [
        'eventType',
        'userId',
        'directUserRequest',
        'eventTime',
        'sessionId',
        'visitorId',
        'productId',
        'quantity',
        'transactionId',
        'revenue',
        'currencyCode'
    ]
    
    # Write to CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write event data
        for event in events:
            row = {}
            
            # Basic event fields
            row['eventType'] = event.get('eventType', '')
            row['eventTime'] = event.get('eventTime', '')
            row['sessionId'] = event.get('sessionId', '')
            row['visitorId'] = event.get('visitorId', '')
            
            # User info
            user_info = event.get('userInfo', {})
            row['userId'] = user_info.get('userId', '')
            row['directUserRequest'] = user_info.get('directUserRequest', '')
            
            # Product details (assuming single product per event based on the sample)
            product_details = event.get('productDetails', [])
            if product_details and len(product_details) > 0:
                product = product_details[0].get('product', {})
                row['productId'] = product.get('id', '')
                row['quantity'] = product_details[0].get('quantity', '')
            else:
                row['productId'] = ''
                row['quantity'] = ''
            
            # Purchase transaction
            purchase_transaction = event.get('purchaseTransaction', {})
            row['transactionId'] = purchase_transaction.get('id', '')
            row['revenue'] = purchase_transaction.get('revenue', '')
            row['currencyCode'] = purchase_transaction.get('currencyCode', '')
            
            writer.writerow(row)
    
    print(f"Successfully converted {len(events)} user events to CSV format")
    print(f"CSV file saved as: {csv_file_path}")

if __name__ == "__main__":
    # File paths
    ndjson_file = "user_events_schema_correct.ndjson"
    csv_file = "user_events_schema_correct.csv"
    
    # Convert the file
    user_events_ndjson_to_csv(ndjson_file, csv_file)