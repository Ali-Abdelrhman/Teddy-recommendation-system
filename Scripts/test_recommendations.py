#!/usr/bin/env python3
"""
Test Google Cloud Retail AI recommendations after catalog upload
This script verifies that recommendations now return real products
instead of auto-generated entries.
"""

from google.cloud import retail_v2
import json

def test_recommendations(project_id, location, catalog_id, placement_id, visitor_id):
    """Test recommendations and verify real products are returned"""
    
    # Initialize the PredictionService client
    client = retail_v2.PredictionServiceClient()
    
    # Construct the placement path
    placement = client.placement_path(
        project=project_id,
        location=location,
        catalog=catalog_id,
        placement=placement_id
    )
    
    print(f"🔍 Testing recommendations for placement: {placement}")
    
    # Create prediction request
    user_event = retail_v2.UserEvent()
    user_event.event_type = "home-page-view"
    user_event.visitor_id = visitor_id
    
    request = retail_v2.PredictRequest()
    request.placement = placement
    request.user_event = user_event
    request.page_size = 10  # Request 10 recommendations
    
    try:
        # Get predictions
        response = client.predict(request=request)
        
        print(f"\n📋 Recommendation Results:")
        print("=" * 60)
        
        if not response.results:
            print("❌ No recommendations returned")
            return False
        
        real_products = 0
        auto_generated = 0
        
        for i, result in enumerate(response.results, 1):
            product = result.product
            
            # Check if this is a real product or auto-generated
            is_real = not product.id.startswith("auto-generated")
            
            if is_real:
                real_products += 1
                status = "✅ Real Product"
            else:
                auto_generated += 1
                status = "❌ Auto-Generated"
            
            print(f"{i:2d}. {status}")
            print(f"    ID: {product.id}")
            print(f"    Title: {product.title}")
            print(f"    Brand: {', '.join(product.brands) if product.brands else 'N/A'}")
            print(f"    Categories: {', '.join(product.categories) if product.categories else 'N/A'}")
            
            if product.price_info and product.price_info.price:
                print(f"    Price: {product.price_info.price:.2f} {product.price_info.currency_code}")
            
            print()
        
        # Summary
        total = len(response.results)
        print("📊 Summary:")
        print(f"  Total recommendations: {total}")
        print(f"  Real products: {real_products}")
        print(f"  Auto-generated: {auto_generated}")
        print(f"  Success rate: {(real_products / total * 100):.1f}%")
        
        if real_products == total:
            print("\n🎉 SUCCESS: All recommendations are real products!")
            return True
        elif real_products > 0:
            print(f"\n⚠️  PARTIAL: {real_products}/{total} recommendations are real products")
            return True
        else:
            print("\n❌ FAILED: No real products in recommendations")
            return False
            
    except Exception as e:
        print(f"❌ Error getting recommendations: {e}")
        return False

def main():
    """Main execution function"""
    
    # Configuration - Update these values
    PROJECT_ID = "dabdoob-master"  # Your project ID
    LOCATION = "global"           # Usually "global"
    CATALOG_ID = "default_catalog" # Default catalog
    PLACEMENT_ID = "recently_viewed_default"  # Common placement ID
    VISITOR_ID = "test_visitor_123"  # Test visitor ID
    
    print("🧪 Google Cloud Retail AI - Recommendation Test")
    print("=" * 60)
    print(f"Project: {PROJECT_ID}")
    print(f"Catalog: {CATALOG_ID}")
    print(f"Placement: {PLACEMENT_ID}")
    print(f"Visitor: {VISITOR_ID}")
    print("=" * 60)
    
    # Test recommendations
    success = test_recommendations(
        project_id=PROJECT_ID,
        location=LOCATION,
        catalog_id=CATALOG_ID,
        placement_id=PLACEMENT_ID,
        visitor_id=VISITOR_ID
    )
    
    if success:
        print("\n✅ Recommendation test completed successfully!")
    else:
        print("\n❌ Recommendation test failed. Check the catalog upload.")

if __name__ == "__main__":
    main()