#!/usr/bin/env python3
"""
Correct fix for Google Cloud Retail AI user events.
Based on actual Google Cloud Retail API schema documentation.

Fixes:
1. Add visitorId at root level
2. Extract productDetails array from productEventDetail to root level
3. Extract purchaseTransaction from productEventDetail to root level
4. Remove the productEventDetail wrapper object
5. Ensure all required fields are properly formatted
"""

import json
import sys

def fix_user_events_correct():
    input_file = "../RecommendationAI_NDJSON/user_events_combined.ndjson"
    output_file = "../RecommendationAI_NDJSON/user_events_schema_correct.ndjson"
    
    print("=== Google Cloud Retail AI User Events Schema Correction ===")
    print("Based on official Google Cloud Retail API schema")
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    
    try:
        total_events = 0
        visitor_id_added = 0
        product_details_extracted = 0
        purchase_transaction_extracted = 0
        
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            for line_num, line in enumerate(infile, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    event = json.loads(line)
                    total_events += 1
                    
                    # Add visitorId at root level (not in userInfo)
                    if 'userInfo' in event and 'userId' in event['userInfo']:
                        user_id = event['userInfo']['userId']
                        event['visitorId'] = user_id
                        visitor_id_added += 1
                    
                    # Extract fields from productEventDetail and remove the wrapper
                    if 'productEventDetail' in event:
                        product_event_detail = event.pop('productEventDetail')
                        
                        # Extract productDetails to root level
                        if 'productDetails' in product_event_detail:
                            event['productDetails'] = product_event_detail['productDetails']
                            product_details_extracted += 1
                        
                        # Extract purchaseTransaction to root level
                        if 'purchaseTransaction' in product_event_detail:
                            event['purchaseTransaction'] = product_event_detail['purchaseTransaction']
                            purchase_transaction_extracted += 1
                    
                    # Also handle if someone previously changed it to productEventDetails
                    elif 'productEventDetails' in event:
                        product_event_details = event.pop('productEventDetails')
                        
                        # Extract productDetails to root level
                        if 'productDetails' in product_event_details:
                            event['productDetails'] = product_event_details['productDetails']
                            product_details_extracted += 1
                        
                        # Extract purchaseTransaction to root level
                        if 'purchaseTransaction' in product_event_details:
                            event['purchaseTransaction'] = product_event_details['purchaseTransaction']
                            purchase_transaction_extracted += 1
                    
                    # Write the fixed event
                    outfile.write(json.dumps(event) + '\n')
                    
                    # Progress indicator
                    if total_events % 10000 == 0:
                        print(f"Processed {total_events} events, visitorId: {visitor_id_added}, productDetails: {product_details_extracted}, purchaseTransaction: {purchase_transaction_extracted}")
                        
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON on line {line_num}: {e}")
                    continue
                except Exception as e:
                    print(f"Error processing line {line_num}: {e}")
                    continue
        
        print("\n=== Processing Complete ===")
        print(f"Total events processed: {total_events}")
        print(f"Events with visitorId added: {visitor_id_added}")
        print(f"ProductDetails fields extracted: {product_details_extracted}")
        print(f"PurchaseTransaction fields extracted: {purchase_transaction_extracted}")
        print(f"Success rate: {visitor_id_added/total_events*100:.1f}%" if total_events > 0 else "No events processed")
        
        # Show sample of fixed events
        print("\n=== Sample of Fixed Events ===")
        with open(output_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= 3:  # Show first 3 events
                    break
                event = json.loads(line.strip())
                print(f"Event {i+1}:")
                print(f"  eventType: {event.get('eventType', 'N/A')}")
                print(f"  userId: {event.get('userInfo', {}).get('userId', 'N/A')}")
                print(f"  visitorId: {event.get('visitorId', 'NOT FOUND')}")
                print(f"  productDetails (root): {'FOUND' if 'productDetails' in event else 'NOT FOUND'}")
                print(f"  purchaseTransaction (root): {'FOUND' if 'purchaseTransaction' in event else 'NOT FOUND'}")
                print(f"  productEventDetail wrapper: {'FOUND' if 'productEventDetail' in event else 'NOT FOUND'}")
                print(f"  productEventDetails wrapper: {'FOUND' if 'productEventDetails' in event else 'NOT FOUND'}")
                if 'productDetails' in event:
                    print(f"  productDetails length: {len(event['productDetails']) if isinstance(event['productDetails'], list) else 'NOT ARRAY'}")
                print()
        
        # Validation check
        print("=== Validation Check ===")
        with open(output_file, 'r', encoding='utf-8') as f:
            sample_events = []
            for i, line in enumerate(f):
                if i >= 10:  # Check first 10 events
                    break
                sample_events.append(json.loads(line.strip()))
        
        visitor_id_count = sum(1 for event in sample_events if 'visitorId' in event)
        product_details_root = sum(1 for event in sample_events if 'productDetails' in event)
        purchase_transaction_root = sum(1 for event in sample_events if 'purchaseTransaction' in event)
        old_wrapper_count = sum(1 for event in sample_events if 'productEventDetail' in event)
        wrong_wrapper_count = sum(1 for event in sample_events if 'productEventDetails' in event)
        
        print(f"Sample validation (first 10 events):")
        print(f"  Events with visitorId: {visitor_id_count}/10")
        print(f"  Events with productDetails at root: {product_details_root}/10")
        print(f"  Events with purchaseTransaction at root: {purchase_transaction_root}/10")
        print(f"  Events with old wrapper (productEventDetail): {old_wrapper_count}/10")
        print(f"  Events with wrong wrapper (productEventDetails): {wrong_wrapper_count}/10")
        
        if old_wrapper_count == 0 and wrong_wrapper_count == 0 and product_details_root > 0:
            print("✅ Schema is correctly formatted for Google Cloud Retail API")
        else:
            print("❌ Some schema issues still need correction")
                
    except FileNotFoundError:
        print(f"Error: Could not find input file: {input_file}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = fix_user_events_correct()
    sys.exit(0 if success else 1)