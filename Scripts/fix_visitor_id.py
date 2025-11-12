#!/usr/bin/env python3
"""
Fix User Events: Convert userId to visitorId for Google Cloud Retail API compatibility

Google Cloud Retail API requires 'visitorId' field but our events use 'userId'.
This script fixes the format to ensure successful import.
"""

import json
import os
from pathlib import Path

def fix_user_events():
    """Fix user events by converting userId to visitorId"""
    
    # Paths
    base_dir = Path("c:/Users/Ahmed/Downloads/Teddy recommendation system")
    input_file = base_dir / "RecommendationAI_NDJSON" / "user_events_combined.ndjson"
    output_file = base_dir / "RecommendationAI_NDJSON" / "user_events_fixed.ndjson"
    
    print("🔧 Fixing User Events Format...")
    print(f"📥 Input: {input_file}")
    print(f"📤 Output: {output_file}")
    
    # Statistics
    total_events = 0
    fixed_events = 0
    error_events = 0
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            for line_num, line in enumerate(infile, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Parse the event
                    event = json.loads(line)
                    total_events += 1
                    
                    # Check if userInfo exists and has userId
                    if 'userInfo' in event and 'userId' in event['userInfo']:
                        # Convert userId to visitorId
                        user_id = event['userInfo']['userId']
                        event['userInfo']['visitorId'] = user_id
                        
                        # Keep userId for reference (optional, can remove if needed)
                        # del event['userInfo']['userId']  # Uncomment to remove userId completely
                        
                        fixed_events += 1
                    
                    # Write the fixed event
                    outfile.write(json.dumps(event, ensure_ascii=False) + '\n')
                    
                    if total_events % 10000 == 0:
                        print(f"⚙️ Processed {total_events:,} events... (Fixed: {fixed_events:,})")
                
                except json.JSONDecodeError as e:
                    error_events += 1
                    print(f"❌ Error parsing line {line_num}: {e}")
                    continue
                except Exception as e:
                    error_events += 1
                    print(f"❌ Unexpected error on line {line_num}: {e}")
                    continue
    
    except FileNotFoundError:
        print(f"❌ Input file not found: {input_file}")
        return False
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False
    
    # Final statistics
    print("\n" + "="*60)
    print("🎯 USER EVENTS FIX COMPLETE!")
    print("="*60)
    print(f"📊 Total Events Processed: {total_events:,}")
    print(f"✅ Events Fixed: {fixed_events:,}")
    print(f"❌ Errors: {error_events:,}")
    print(f"📁 Output File: {output_file}")
    
    if total_events > 0:
        success_rate = (fixed_events / total_events) * 100
        print(f"📈 Success Rate: {success_rate:.1f}%")
    
    return True

def validate_fixed_events():
    """Validate the fixed events file"""
    
    base_dir = Path("c:/Users/Ahmed/Downloads/Teddy recommendation system")
    fixed_file = base_dir / "RecommendationAI_NDJSON" / "user_events_fixed.ndjson"
    
    print("\n🔍 Validating Fixed Events...")
    
    events_with_visitor_id = 0
    events_without_visitor_id = 0
    total_validated = 0
    
    try:
        with open(fixed_file, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    event = json.loads(line)
                    total_validated += 1
                    
                    # Check for visitorId
                    if 'userInfo' in event and 'visitorId' in event['userInfo']:
                        events_with_visitor_id += 1
                    else:
                        events_without_visitor_id += 1
                        if events_without_visitor_id <= 5:  # Show first 5 problematic events
                            print(f"⚠️ Line {line_num}: Missing visitorId - {json.dumps(event, indent=2)}")
                
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON on line {line_num}")
                
                # Sample check for first 10,000 events
                if total_validated >= 10000:
                    break
    
    except FileNotFoundError:
        print(f"❌ Fixed file not found: {fixed_file}")
        return False
    
    print("\n📊 Validation Results:")
    print(f"✅ Events with visitorId: {events_with_visitor_id:,}")
    print(f"❌ Events without visitorId: {events_without_visitor_id:,}")
    print(f"📋 Total Validated: {total_validated:,}")
    
    if events_without_visitor_id == 0:
        print("🎉 All events have visitorId! Ready for Google Cloud import.")
        return True
    else:
        print(f"⚠️ {events_without_visitor_id} events still missing visitorId")
        return False

def show_sample_events():
    """Show sample of fixed events"""
    
    base_dir = Path("c:/Users/Ahmed/Downloads/Teddy recommendation system")
    fixed_file = base_dir / "RecommendationAI_NDJSON" / "user_events_fixed.ndjson"
    
    print("\n📋 Sample of Fixed Events:")
    print("-" * 40)
    
    try:
        with open(fixed_file, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                if i >= 3:  # Show first 3 events
                    break
                
                line = line.strip()
                if line:
                    event = json.loads(line)
                    print(f"Event {i+1}:")
                    print(json.dumps(event, indent=2, ensure_ascii=False))
                    print("-" * 40)
    
    except Exception as e:
        print(f"❌ Error showing samples: {e}")

if __name__ == "__main__":
    print("🚀 Starting User Events Fix Process...")
    
    # Fix the events
    if fix_user_events():
        # Validate the fix
        if validate_fixed_events():
            # Show samples
            show_sample_events()
            print("\n✅ Process completed successfully!")
            print("📋 Next step: Upload user_events_fixed.ndjson to Google Cloud Storage")
        else:
            print("\n⚠️ Some events still have issues - review the validation results")
    else:
        print("\n❌ Fix process failed - check the error messages")