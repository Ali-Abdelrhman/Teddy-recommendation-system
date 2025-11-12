#!/usr/bin/env python3
"""
Final fix for Google Cloud Retail AI user events.
Based on actual Google Cloud Retail API schema documentation.

Fixes:
1. Add visitorId at root level
2. Change productEventDetail to productDetails (correct API field name)
3. Ensure all required fields are properly formatted
"""

import json
import sys

def fix_user_events_final():
    input_file = "../RecommendationAI_NDJSON/user_events_combined.ndjson"
    output_file = "../RecommendationAI_NDJSON/user_events_corrected.ndjson"
    
    print("=== Google Cloud Retail AI User Events Final Fix ===")
    print("Based on official Google Cloud Retail API schema")
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    
    try:
        total_events = 0
        fixed_events = 0
        field_renamed = 0
        
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
                        fixed_events += 1
                    
                    # Fix productEventDetail -> productDetails (correct API field name)
                    if 'productEventDetail' in event:
                        event['productDetails'] = event.pop('productEventDetail')
                        field_renamed += 1
                    elif 'productEventDetails' in event:
                        # Also fix if someone previously changed it to productEventDetails
                        event['productDetails'] = event.pop('productEventDetails')
                        field_renamed += 1
                    
                    # Write the fixed event
                    outfile.write(json.dumps(event) + '\n')
                    
                    # Progress indicator
                    if total_events % 10000 == 0:
                        print(f"Processed {total_events} events, fixed {fixed_events}, renamed {field_renamed} fields")
                        
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON on line {line_num}: {e}")
                    continue
                except Exception as e:
                    print(f"Error processing line {line_num}: {e}")
                    continue
        
        print("\n=== Processing Complete ===")
        print(f"Total events processed: {total_events}")
        print(f"Events with visitorId added: {fixed_events}")
        print(f"Fields renamed to productDetails: {field_renamed}")
        print(f"Success rate: {fixed_events/total_events*100:.1f}%" if total_events > 0 else "No events processed")
        
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
                print(f"  productDetails: {'FOUND' if 'productDetails' in event else 'NOT FOUND'}")
                print(f"  productEventDetail: {'FOUND' if 'productEventDetail' in event else 'NOT FOUND'}")
                print(f"  productEventDetails: {'FOUND' if 'productEventDetails' in event else 'NOT FOUND'}")
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
        old_field_count = sum(1 for event in sample_events if 'productEventDetail' in event)
        wrong_field_count = sum(1 for event in sample_events if 'productEventDetails' in event)
        correct_field_count = sum(1 for event in sample_events if 'productDetails' in event)
        
        print(f"Sample validation (first 10 events):")
        print(f"  Events with visitorId: {visitor_id_count}/10")
        print(f"  Events with old field (productEventDetail): {old_field_count}/10")
        print(f"  Events with wrong field (productEventDetails): {wrong_field_count}/10")
        print(f"  Events with correct field (productDetails): {correct_field_count}/10")
        
        if old_field_count == 0 and wrong_field_count == 0 and correct_field_count > 0:
            print("✅ Field names are correctly formatted for Google Cloud Retail API")
        else:
            print("❌ Some field names still need correction")
                
    except FileNotFoundError:
        print(f"Error: Could not find input file: {input_file}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = fix_user_events_final()
    sys.exit(0 if success else 1)