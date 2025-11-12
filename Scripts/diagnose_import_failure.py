#!/usr/bin/env python3
"""
Google Cloud User Events Import Troubleshoot
===========================================
Diagnoses and fixes common issues with user events import failures.
"""

import json
import os
from collections import Counter
import re
from datetime import datetime, timezone

def diagnose_user_events_import():
    """Diagnose potential issues with user events import."""
    
    base_path = r"c:\Users\Ahmed\Downloads\Teddy recommendation system"
    ndjson_path = os.path.join(base_path, "RecommendationAI_NDJSON")
    events_file = os.path.join(ndjson_path, "user_events_combined.ndjson")
    
    print("🔍 DIAGNOSING USER EVENTS IMPORT FAILURE")
    print("=" * 50)
    
    issues = []
    warnings = []
    total_events = 0
    
    # Check file exists
    if not os.path.exists(events_file):
        issues.append("❌ user_events_combined.ndjson file not found")
        return
    
    # Analyze events line by line
    with open(events_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
                
            try:
                event = json.loads(line)
                total_events += 1
                
                # Check required fields
                if 'eventType' not in event:
                    issues.append(f"Line {line_num}: Missing 'eventType'")
                elif event['eventType'] not in ['detail-page-view', 'home-page-view', 'add-to-cart', 'purchase-complete']:
                    issues.append(f"Line {line_num}: Invalid eventType '{event['eventType']}'")
                
                if 'userInfo' not in event:
                    issues.append(f"Line {line_num}: Missing 'userInfo'")
                elif 'userId' not in event['userInfo']:
                    issues.append(f"Line {line_num}: Missing 'userId' in userInfo")
                
                if 'eventTime' not in event:
                    issues.append(f"Line {line_num}: Missing 'eventTime'")
                else:
                    # Check eventTime format
                    try:
                        datetime.fromisoformat(event['eventTime'].replace('Z', '+00:00'))
                    except ValueError:
                        issues.append(f"Line {line_num}: Invalid eventTime format '{event['eventTime']}'")
                
                # Check product details
                if 'productEventDetail' in event:
                    if 'productDetails' not in event['productEventDetail']:
                        issues.append(f"Line {line_num}: Missing 'productDetails' in productEventDetail")
                    else:
                        for detail in event['productEventDetail']['productDetails']:
                            if 'product' not in detail or 'id' not in detail['product']:
                                issues.append(f"Line {line_num}: Missing product.id in productDetails")
                
                # Check purchase transaction for purchase-complete events
                if event.get('eventType') == 'purchase-complete':
                    if 'purchaseTransaction' not in event.get('productEventDetail', {}):
                        warnings.append(f"Line {line_num}: purchase-complete event missing purchaseTransaction")
                    else:
                        transaction = event['productEventDetail']['purchaseTransaction']
                        if 'id' not in transaction:
                            warnings.append(f"Line {line_num}: Missing transaction.id")
                        if 'revenue' not in transaction:
                            warnings.append(f"Line {line_num}: Missing transaction.revenue")
                        if 'currencyCode' not in transaction:
                            warnings.append(f"Line {line_num}: Missing transaction.currencyCode")
                
                # Stop after checking first 100 lines if too many issues
                if len(issues) > 100:
                    issues.append("... (stopping analysis, too many issues)")
                    break
                    
            except json.JSONDecodeError as e:
                issues.append(f"Line {line_num}: Invalid JSON - {str(e)}")
                if len(issues) > 100:
                    break
    
    # Generate diagnosis report
    print(f"📊 ANALYSIS RESULTS")
    print(f"Total events analyzed: {total_events:,}")
    print(f"Critical issues found: {len(issues)}")
    print(f"Warnings found: {len(warnings)}")
    print()
    
    if issues:
        print("❌ CRITICAL ISSUES (Must Fix):")
        for issue in issues[:20]:  # Show first 20 issues
            print(f"  {issue}")
        if len(issues) > 20:
            print(f"  ... and {len(issues) - 20} more issues")
        print()
    
    if warnings:
        print("⚠️  WARNINGS (Recommended to Fix):")
        for warning in warnings[:10]:  # Show first 10 warnings
            print(f"  {warning}")
        if len(warnings) > 10:
            print(f"  ... and {len(warnings) - 10} more warnings")
        print()
    
    # Common solutions
    print("🔧 COMMON SOLUTIONS:")
    print()
    
    if any("eventType" in issue for issue in issues):
        print("1. INVALID EVENT TYPES:")
        print("   • Allowed values: 'detail-page-view', 'home-page-view', 'add-to-cart', 'purchase-complete'")
        print("   • Check for typos or extra characters")
        print()
    
    if any("eventTime" in issue for issue in issues):
        print("2. INVALID EVENT TIME FORMAT:")
        print("   • Required format: YYYY-MM-DDTHH:MM:SSZ (ISO 8601)")
        print("   • Example: '2025-10-21T15:57:54Z'")
        print()
    
    if any("userId" in issue for issue in issues):
        print("3. MISSING USER ID:")
        print("   • Every event must have userInfo.userId")
        print("   • User IDs should be consistent strings/numbers")
        print()
    
    if any("product.id" in issue for issue in issues):
        print("4. MISSING PRODUCT IDS:")
        print("   • Every event must reference valid product IDs")
        print("   • Product IDs must match your products catalog")
        print()
    
    print("5. GOOGLE CLOUD SPECIFIC ISSUES:")
    print("   • Ensure products are imported BEFORE user events")
    print("   • Check Google Cloud Storage bucket permissions")
    print("   • Verify project ID and catalog name are correct")
    print("   • File size limit: 2GB per import operation")
    print()
    
    # Check if products were imported first
    print("🔍 IMPORT ORDER CHECK:")
    print("Google Cloud requires products to be imported BEFORE user events!")
    print("Run this command first:")
    print("gcloud retail products import \\")
    print("  --project=teddy-demo-2025 \\")
    print("  --location=global \\")
    print("  --catalog=default_catalog \\")
    print("  --data-file=\"gs://your-bucket/products_expanded.ndjson\"")
    print()
    print("Then import user events:")
    print("gcloud retail user-events import \\")
    print("  --project=teddy-demo-2025 \\")
    print("  --location=global \\")
    print("  --catalog=default_catalog \\")
    print("  --data-file=\"gs://your-bucket/user_events_combined.ndjson\"")
    print()
    
    return len(issues) == 0

def create_sample_valid_event():
    """Create a sample valid event for reference."""
    
    sample_event = {
        "eventType": "detail-page-view",
        "userInfo": {
            "userId": "user123",
            "directUserRequest": True
        },
        "productEventDetail": {
            "productDetails": [
                {
                    "product": {
                        "id": "PROD000001"
                    },
                    "quantity": 1
                }
            ]
        },
        "eventTime": "2025-10-22T10:00:00Z",
        "sessionId": "SESSION_123"
    }
    
    print("📋 SAMPLE VALID EVENT:")
    print(json.dumps(sample_event, indent=2))
    print()

if __name__ == "__main__":
    print("🚀 Starting User Events Import Diagnosis...")
    print()
    
    is_valid = diagnose_user_events_import()
    
    print()
    create_sample_valid_event()
    
    if is_valid:
        print("✅ No critical issues found! Import should work.")
    else:
        print("❌ Critical issues found. Fix these before importing.")
    
    print("\n💡 Next Steps:")
    print("1. Fix any critical issues in your data")
    print("2. Ensure products are imported first")
    print("3. Upload fixed file to Google Cloud Storage")
    print("4. Retry the import operation")