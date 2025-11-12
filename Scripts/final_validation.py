#!/usr/bin/env python3
"""
Final Validation and Google Cloud Upload Preparation Script
==========================================================
This script validates the processed user events NDJSON file
and prepares it for Google Cloud Recommendation AI import.
"""

import json
import os
from collections import Counter, defaultdict
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_ndjson_file(file_path: str):
    """Validate the NDJSON file and generate comprehensive statistics."""
    
    logger.info(f"Validating NDJSON file: {file_path}")
    
    stats = {
        'total_events': 0,
        'event_types': Counter(),
        'users': set(),
        'products': set(),
        'sessions': set(),
        'date_range': {'earliest': None, 'latest': None},
        'validation_errors': [],
        'sample_events': defaultdict(list)
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    event = json.loads(line)
                    stats['total_events'] += 1
                    
                    # Validate required fields
                    required_fields = ['eventType', 'userInfo', 'eventTime', 'sessionId']
                    for field in required_fields:
                        if field not in event:
                            stats['validation_errors'].append(f"Line {line_num}: Missing required field '{field}'")
                    
                    # Extract event type
                    event_type = event.get('eventType', 'unknown')
                    stats['event_types'][event_type] += 1
                    
                    # Extract user ID
                    user_info = event.get('userInfo', {})
                    user_id = user_info.get('userId')
                    if user_id:
                        stats['users'].add(user_id)
                    
                    # Extract product ID (if exists)
                    product_details = event.get('productEventDetail', {}).get('productDetails', [])
                    if product_details:
                        for detail in product_details:
                            product_id = detail.get('product', {}).get('id')
                            if product_id:
                                stats['products'].add(product_id)
                    
                    # Extract session ID
                    session_id = event.get('sessionId')
                    if session_id:
                        stats['sessions'].add(session_id)
                    
                    # Track date range
                    event_time = event.get('eventTime')
                    if event_time:
                        if stats['date_range']['earliest'] is None or event_time < stats['date_range']['earliest']:
                            stats['date_range']['earliest'] = event_time
                        if stats['date_range']['latest'] is None or event_time > stats['date_range']['latest']:
                            stats['date_range']['latest'] = event_time
                    
                    # Store sample events (first 3 of each type)
                    if len(stats['sample_events'][event_type]) < 3:
                        stats['sample_events'][event_type].append(event)
                    
                    # Progress reporting
                    if stats['total_events'] % 10000 == 0:
                        logger.info(f"Processed {stats['total_events']:,} events...")
                        
                except json.JSONDecodeError as e:
                    stats['validation_errors'].append(f"Line {line_num}: Invalid JSON - {e}")
                except Exception as e:
                    stats['validation_errors'].append(f"Line {line_num}: Error - {e}")
    
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        return None
    
    # Convert sets to counts for final stats
    stats['unique_users'] = len(stats['users'])
    stats['unique_products'] = len(stats['products'])
    stats['unique_sessions'] = len(stats['sessions'])
    
    # Remove the actual sets to save memory
    del stats['users']
    del stats['products'] 
    del stats['sessions']
    
    return stats

def generate_comprehensive_report(stats: dict, output_path: str):
    """Generate a comprehensive validation report."""
    
    report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     GOOGLE CLOUD RECOMMENDATION AI - FINAL VALIDATION        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║ 📊 EVENT STATISTICS                                                          ║
║ ═══════════════════                                                          ║
║ Total Events:                    {stats['total_events']:>15,}                          ║
║ Unique Users:                    {stats['unique_users']:>15,}                          ║
║ Unique Products:                 {stats['unique_products']:>15,}                          ║
║ Unique Sessions:                 {stats['unique_sessions']:>15,}                          ║
║                                                                              ║
║ 📈 EVENT TYPE BREAKDOWN                                                      ║
║ ═══════════════════════                                                      ║"""

    for event_type, count in stats['event_types'].most_common():
        percentage = (count / stats['total_events']) * 100
        report += f"\n║ {event_type:<20} {count:>10,} ({percentage:>5.1f}%)                        ║"
    
    report += f"""
║                                                                              ║
║ 📅 DATE RANGE                                                               ║
║ ══════════════                                                               ║
║ Earliest Event:                  {stats['date_range']['earliest'] or 'N/A':>20}                     ║
║ Latest Event:                    {stats['date_range']['latest'] or 'N/A':>20}                     ║
║                                                                              ║
║ ✅ RECOMMENDATION AI REQUIREMENTS CHECK                                      ║
║ ═══════════════════════════════════════                                      ║"""

    # Check requirements
    detail_page_count = stats['event_types'].get('detail-page-view', 0)
    home_page_count = stats['event_types'].get('home-page-view', 0)
    add_to_cart_count = stats['event_types'].get('add-to-cart', 0)
    purchase_count = stats['event_types'].get('purchase-complete', 0)
    
    total_required_events = detail_page_count + home_page_count + add_to_cart_count
    
    detail_check = "✅ PASS" if detail_page_count >= 10000 else "❌ FAIL"
    home_check = "✅ PASS" if home_page_count >= 10000 else "❌ FAIL"
    cart_check = "✅ PASS" if add_to_cart_count >= 10000 else "❌ FAIL"
    total_check = "✅ PASS" if total_required_events >= 30000 else "❌ FAIL"
    
    report += f"""
║ Detail-page-view (≥10K):         {detail_page_count:>10,} {detail_check:>15}             ║
║ Home-page-view (≥10K):           {home_page_count:>10,} {home_check:>15}             ║
║ Add-to-cart (≥10K):              {add_to_cart_count:>10,} {cart_check:>15}             ║
║ Total Interactive Events:        {total_required_events:>10,} {total_check:>15}             ║
║ Purchase Events (Bonus):         {purchase_count:>10,} ✅ BONUS               ║
║                                                                              ║"""

    if stats['validation_errors']:
        report += f"""
║ ⚠️  VALIDATION ISSUES                                                        ║
║ ══════════════════════                                                       ║
║ Total Errors:                    {len(stats['validation_errors']):>15,}                          ║"""
        for i, error in enumerate(stats['validation_errors'][:5]):  # Show first 5 errors
            report += f"\n║ {error[:76]:<76} ║"
        if len(stats['validation_errors']) > 5:
            report += f"\n║ ... and {len(stats['validation_errors']) - 5} more errors                                      ║"
    else:
        report += """
║ ✅ DATA VALIDATION                                                           ║
║ ═══════════════════                                                          ║
║ No validation errors found - File is perfect! 🎯                           ║"""

    # Overall status
    if (detail_page_count >= 10000 and home_page_count >= 10000 and 
        add_to_cart_count >= 10000 and len(stats['validation_errors']) == 0):
        status = "🎉 READY FOR GOOGLE CLOUD IMPORT"
        color = "✅"
    elif total_required_events >= 30000 and len(stats['validation_errors']) == 0:
        status = "⚠️  MOSTLY READY - MINOR ISSUES"
        color = "🟡"
    else:
        status = "❌ NEEDS FIXES BEFORE IMPORT"
        color = "🔴"

    report += f"""
║                                                                              ║
║ 🎯 FINAL STATUS                                                              ║
║ ═══════════════                                                              ║
║ {color} {status:<61} ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📁 FILE INFORMATION
═══════════════════
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
File Size: {os.path.getsize(output_path) / (1024*1024):.1f} MB
Ready for: Google Cloud Recommendation AI Import

🚀 NEXT STEPS
═════════════
1. Upload to Google Cloud Storage
2. Import into Recommendation AI using:
   gcloud retail user-events import --data-file="gs://your-bucket/user_events_combined.ndjson"
3. Enable "Recommended for You" model in your catalog

📋 COMMAND REFERENCE
═══════════════════
# Upload to Cloud Storage
gsutil cp user_events_combined.ndjson gs://your-bucket/

# Import to Recommendation AI
gcloud retail user-events import \\
  --project=teddy-demo-2025 \\
  --location=global \\
  --catalog=default_catalog \\
  --data-file="gs://your-bucket/user_events_combined.ndjson"
"""

    return report

def main():
    """Main validation function."""
    base_path = r"c:\Users\Ahmed\Downloads\Teddy recommendation system"
    ndjson_file = os.path.join(base_path, "RecommendationAI_NDJSON", "user_events_combined.ndjson")
    
    if not os.path.exists(ndjson_file):
        logger.error(f"NDJSON file not found: {ndjson_file}")
        return
    
    # Validate the file
    logger.info("Starting comprehensive validation...")
    stats = validate_ndjson_file(ndjson_file)
    
    if stats is None:
        logger.error("Validation failed!")
        return
    
    # Generate report
    report = generate_comprehensive_report(stats, ndjson_file)
    
    # Save report
    report_file = os.path.join(base_path, "RecommendationAI_NDJSON", "final_validation_report.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Display report
    print(report)
    
    logger.info(f"Validation complete! Report saved to: {report_file}")

if __name__ == "__main__":
    main()