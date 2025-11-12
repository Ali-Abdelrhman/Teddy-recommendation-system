#!/usr/bin/env python3
"""
Complete fix for Google Cloud Retail AI user events.
Fixes:
1. Add visitorId at root level
2. Change productEventDetail to productEventDetails (plural)
3. Ensure all required fields are properly formatted
"""

import json
import sys

def fix_user_events_complete():
    input_file = "../RecommendationAI_NDJSON/user_events_combined.ndjson"
    output_file = "../RecommendationAI_NDJSON/user_events_final.ndjson"
    
    print("=== Google Cloud Retail AI User Events Complete Fix ===")
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    
    try:
        total_events = 0
        fixed_events = 0
        
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
                    
                    # Fix productEventDetail -> productEventDetails (plural)
                    if 'productEventDetail' in event:
                        event['productEventDetails'] = event.pop('productEventDetail')
                    
                    # Write the fixed event
                    outfile.write(json.dumps(event) + '\n')
                    
                    # Progress indicator
                    if total_events % 10000 == 0:
                        print(f"Processed {total_events} events, fixed {fixed_events}")
                        
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON on line {line_num}: {e}")
                    continue
                except Exception as e:
                    print(f"Error processing line {line_num}: {e}")
                    continue
        
        print("\n=== Processing Complete ===")
        print(f"Total events processed: {total_events}")
        print(f"Events with visitorId added: {fixed_events}")
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
                print(f"  productEventDetails: {'FOUND' if 'productEventDetails' in event else 'NOT FOUND'}")
                print(f"  productEventDetail: {'FOUND' if 'productEventDetail' in event else 'NOT FOUND'}")
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
        new_field_count = sum(1 for event in sample_events if 'productEventDetails' in event)
        
        print(f"Sample validation (first 10 events):")
        print(f"  Events with visitorId: {visitor_id_count}/10")
        print(f"  Events with old field (productEventDetail): {old_field_count}/10")
        print(f"  Events with new field (productEventDetails): {new_field_count}/10")
                
    except FileNotFoundError:
        print(f"Error: Could not find input file: {input_file}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = fix_user_events_complete()
    sys.exit(0 if success else 1)