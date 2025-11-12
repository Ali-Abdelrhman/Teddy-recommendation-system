#!/usr/bin/env python3
"""
Google Cloud Recommendation AI Model Compatibility Analysis
===========================================================
Analyzes the compatibility of our dataset with different recommendation models.
"""

import json
import os
from collections import Counter

def analyze_model_compatibility():
    """Analyze compatibility with different Google Cloud recommendation models."""
    
    base_path = r"c:\Users\Ahmed\Downloads\Teddy recommendation system"
    ndjson_path = os.path.join(base_path, "RecommendationAI_NDJSON")
    
    products_file = os.path.join(ndjson_path, "products_expanded.ndjson")
    events_file = os.path.join(ndjson_path, "user_events_combined.ndjson")
    
    # Count products and events
    product_count = 0
    event_types = Counter()
    total_events = 0
    
    # Analyze products
    with open(products_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                product_count += 1
    
    # Analyze events
    with open(events_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    event = json.loads(line)
                    event_type = event.get('eventType')
                    event_types[event_type] += 1
                    total_events += 1
                except json.JSONDecodeError:
                    continue
    
    # Model requirements analysis
    models = {
        "recommended-for-you": {
            "name": "Recommended for You",
            "description": "Personalized recommendations based on user behavior",
            "requirements": {
                "min_products": 1000,
                "min_detail_page_view": 10000,
                "min_home_page_view": 10000, 
                "min_add_to_cart": 10000,
                "required_events": ["detail-page-view", "home-page-view", "add-to-cart"],
                "optional_events": ["purchase-complete"]
            }
        },
        "similar-items": {
            "name": "Similar Items",
            "description": "Content-based recommendations showing similar products",
            "requirements": {
                "min_products": 1000,
                "min_detail_page_view": 1000,
                "required_events": ["detail-page-view"],
                "optional_events": ["home-page-view", "add-to-cart", "purchase-complete"]
            }
        },
        "others-you-may-like": {
            "name": "Others You May Like", 
            "description": "Cross-sell recommendations",
            "requirements": {
                "min_products": 1000,
                "min_detail_page_view": 1000,
                "required_events": ["detail-page-view"],
                "optional_events": ["home-page-view", "add-to-cart", "purchase-complete"]
            }
        },
        "recently-viewed": {
            "name": "Recently Viewed",
            "description": "Shows recently viewed items",
            "requirements": {
                "min_products": 100,
                "min_detail_page_view": 100,
                "required_events": ["detail-page-view"],
                "optional_events": []
            }
        },
        "buy-it-again": {
            "name": "Buy It Again",
            "description": "Repurchase recommendations",
            "requirements": {
                "min_products": 100,
                "min_purchase_complete": 100,
                "required_events": ["purchase-complete"],
                "optional_events": ["detail-page-view"]
            }
        }
    }
    
    # Check compatibility for each model
    compatibility_results = {}
    
    for model_id, model_info in models.items():
        reqs = model_info["requirements"]
        compatible = True
        issues = []
        
        # Check product count
        if product_count < reqs.get("min_products", 0):
            compatible = False
            issues.append(f"Need {reqs['min_products']} products, have {product_count}")
        
        # Check required events
        for event_type in reqs.get("required_events", []):
            min_required = reqs.get(f"min_{event_type.replace('-', '_')}", 1)
            actual_count = event_types.get(event_type, 0)
            
            if actual_count < min_required:
                compatible = False
                issues.append(f"Need {min_required} {event_type} events, have {actual_count}")
        
        compatibility_results[model_id] = {
            "compatible": compatible,
            "issues": issues,
            "model_info": model_info
        }
    
    # Generate comprehensive report
    report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              GOOGLE CLOUD RECOMMENDATION AI MODEL COMPATIBILITY             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║ 📊 YOUR DATASET SUMMARY                                                      ║
║ ═══════════════════════                                                      ║
║ Products:                            {product_count:>15,} items              ║
║ User Events:                         {total_events:>15,} events             ║
║                                                                              ║
║ Event Breakdown:                                                             ║"""

    for event_type, count in event_types.most_common():
        percentage = (count / total_events) * 100
        report += f"\n║ • {event_type:<25} {count:>10,} ({percentage:>5.1f}%)           ║"

    report += f"""
║                                                                              ║
║ 🎯 MODEL COMPATIBILITY ANALYSIS                                             ║
║ ═══════════════════════════════                                              ║
║                                                                              ║"""

    for model_id, result in compatibility_results.items():
        model_name = result["model_info"]["name"]
        status = "✅ COMPATIBLE" if result["compatible"] else "❌ NOT COMPATIBLE"
        
        report += f"""
║ 📱 {model_name.upper():<25}                                     ║
║ ─────────────────────────────────────────────────────────────────────        ║
║ Status: {status:<20}                                     ║
║ Description: {result["model_info"]["description"]:<50} ║"""
        
        if result["issues"]:
            report += f"\n║ Issues: {len(result['issues'])} problems found                                        ║"
            for issue in result["issues"][:2]:  # Show max 2 issues
                report += f"\n║   • {issue:<70} ║"
        else:
            report += f"\n║ ✅ All requirements met!                                           ║"
        
        report += f"\n║                                                                              ║"

    # Summary and recommendations
    compatible_models = [k for k, v in compatibility_results.items() if v["compatible"]]
    
    report += f"""
║ 📈 SUMMARY & RECOMMENDATIONS                                                ║
║ ═══════════════════════════════                                              ║
║                                                                              ║
║ Compatible Models: {len(compatible_models)}/5                                                ║"""
    
    for model_id in compatible_models:
        model_name = compatibility_results[model_id]["model_info"]["name"]
        report += f"\n║ ✅ {model_name:<60} ║"
    
    report += f"""
║                                                                              ║
║ 🚀 IMPORT STRATEGY                                                           ║
║ ═══════════════════                                                          ║
║                                                                              ║
║ 1. Import both files to Google Cloud:                                       ║
║    • products_expanded.ndjson ({product_count:,} products)                             ║
║    • user_events_combined.ndjson ({total_events:,} events)                            ║
║                                                                              ║
║ 2. Enable compatible models in order of business priority:                  ║"""
    
    priority_order = ["recommended-for-you", "similar-items", "others-you-may-like", "recently-viewed", "buy-it-again"]
    for model_id in priority_order:
        if model_id in compatible_models:
            model_name = compatibility_results[model_id]["model_info"]["name"]
            report += f"\n║    ✅ {model_name} (Ready to enable)                              ║"
        else:
            model_name = compatibility_results[model_id]["model_info"]["name"]
            report += f"\n║    ⏳ {model_name} (Needs more data)                              ║"
    
    report += f"""
║                                                                              ║
║ 💡 PRO TIPS                                                                  ║
║ ══════════                                                                   ║
║ • Start with "Similar Items" - easiest to implement and test                ║
║ • "Recommended for You" will provide the best personalization              ║
║ • Monitor model performance and A/B test different recommendations          ║
║ • Consider collecting more diverse event types for future models           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎉 EXCELLENT NEWS!
Your dataset is compatible with {len(compatible_models)} out of 5 Google Cloud recommendation models!
Both files (products_expanded.ndjson + user_events_combined.ndjson) can be used 
for multiple recommendation scenarios.
"""

    print(report)
    
    # Save report
    report_file = os.path.join(ndjson_path, "model_compatibility_analysis.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📄 Full compatibility analysis saved to: {report_file}")
    
    return compatibility_results

if __name__ == "__main__":
    results = analyze_model_compatibility()