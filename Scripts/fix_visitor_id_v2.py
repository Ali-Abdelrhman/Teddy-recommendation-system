#!/usr/bin/env python3
"""
Fix visitor ID for Google Cloud Retail AI user events.
Based on error analysis, visitorId should be at root level, not in userInfo.
"""

import json
import sys

def fix_visitor_id_v2():
    input_file = "../RecommendationAI_NDJSON/user_events_combined.ndjson"
    output_file = "../RecommendationAI_NDJSON/user_events_fixed_v2.ndjson"
    
    print("=== Google Cloud Retail AI User Events Visitor ID Fix V2 ===")
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
                        # Add visitorId at the root level of the event
                        event['visitorId'] = user_id
                        fixed_events += 1
                    
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
                print()
                
    except FileNotFoundError:
        print(f"Error: Could not find input file: {input_file}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = fix_visitor_id_v2()
    sys.exit(0 if success else 1)