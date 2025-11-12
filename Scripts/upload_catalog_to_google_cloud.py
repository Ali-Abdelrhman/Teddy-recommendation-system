#!/usr/bin/env python3
"""
Upload complete product catalog to Google Cloud Retail API
This script uploads the full product catalog to replace the incomplete one
that was causing auto-generated product entries in recommendations.
"""

import json
import time
from google.cloud import retail_v2
from google.api_core import exceptions

def upload_product_catalog(project_id, location, catalog_id, branch_id, ndjson_file_path):
    """Upload product catalog to Google Cloud Retail API"""
    
    # Initialize the ProductService client
    client = retail_v2.ProductServiceClient()
    
    # Construct the parent path
    parent = client.branch_path(
        project=project_id,
        location=location,
        catalog=catalog_id,
        branch=branch_id
    )
    
    print(f"🚀 Starting catalog upload to: {parent}")
    
    # Read and process the NDJSON file
    products_uploaded = 0
    products_failed = 0
    
    try:
        with open(ndjson_file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                
                try:
                    # Parse the JSON product
                    product_data = json.loads(line.strip())
                    
                    # Create Product object
                    product = retail_v2.Product()
                    
                    # Set basic fields
                    product.id = product_data['id']
                    product.primary_product_id = product_data.get('primaryProductId', product_data['id'])
                    product.type_ = getattr(retail_v2.Product.Type, product_data.get('type', 'PRIMARY'))
                    product.title = product_data['title']
                    product.description = product_data.get('description', '')
                    product.categories = product_data.get('categories', [])
                    product.availability = getattr(retail_v2.Product.Availability, product_data.get('availability', 'IN_STOCK'))
                    product.uri = product_data.get('uri', '')
                    
                    # Set price info
                    if 'priceInfo' in product_data:
                        price_info = retail_v2.PriceInfo()
                        price_info.currency_code = product_data['priceInfo'].get('currency', 'SAR')
                        price_info.price = product_data['priceInfo'].get('price', 0.0)
                        price_info.original_price = product_data['priceInfo'].get('originalPrice', 0.0)
                        product.price_info = price_info
                    
                    # Set brands
                    if 'brands' in product_data:
                        product.brands = product_data['brands']
                    
                    # Set GTIN
                    if 'gtin' in product_data:
                        product.gtin = product_data['gtin']
                    
                    # Set attributes
                    if 'attributes' in product_data:
                        for attr_name, attr_value in product_data['attributes'].items():
                            if 'text' in attr_value:
                                attribute = retail_v2.Product.Attribute()
                                attribute.text = attr_value['text']
                                product.attributes[attr_name] = attribute
                    
                    # Upload the product
                    request = retail_v2.CreateProductRequest(
                        parent=parent,
                        product=product,
                        product_id=product.id
                    )
                    
                    response = client.create_product(request=request)
                    products_uploaded += 1
                    
                    if products_uploaded % 100 == 0:
                        print(f"📦 Uploaded {products_uploaded} products...")
                    
                except json.JSONDecodeError as e:
                    print(f"❌ JSON error in line {line_num}: {e}")
                    products_failed += 1
                    continue
                except exceptions.AlreadyExists:
                    # Product already exists, try to update it
                    try:
                        # Construct the product name for update
                        product_name = client.product_path(
                            project=project_id,
                            location=location,
                            catalog=catalog_id,
                            branch=branch_id,
                            product=product.id
                        )
                        
                        update_request = retail_v2.UpdateProductRequest(
                            product=product
                        )
                        update_request.product.name = product_name
                        
                        response = client.update_product(request=update_request)
                        products_uploaded += 1
                        
                        if products_uploaded % 100 == 0:
                            print(f"📦 Updated {products_uploaded} products...")\n                        
                    except Exception as update_error:
                        print(f"❌ Failed to update product {product.id}: {update_error}")
                        products_failed += 1
                except Exception as e:
                    print(f"❌ Error uploading product {product_data.get('id', 'unknown')}: {e}")
                    products_failed += 1
                    continue
                
                # Add small delay to avoid rate limiting
                if products_uploaded % 50 == 0:
                    time.sleep(0.1)
    
    except FileNotFoundError:
        print(f"❌ File not found: {ndjson_file_path}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    print(f"\n✅ Catalog upload completed!")
    print(f"📊 Products uploaded/updated: {products_uploaded}")
    print(f"❌ Products failed: {products_failed}")
    print(f"📈 Success rate: {(products_uploaded / (products_uploaded + products_failed) * 100):.1f}%")
    
    return True

def main():
    """Main execution function"""
    
    # Configuration - Update these values with your project details
    PROJECT_ID = "dabdoob-master"  # Replace with your actual project ID
    LOCATION = "global"           # Usually "global" for Retail API
    CATALOG_ID = "default_catalog" # Default catalog ID
    BRANCH_ID = "0"               # Default branch
    
    # Path to the generated catalog file
    catalog_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\product_catalog_complete.ndjson"
    
    print("🎯 Google Cloud Retail API - Product Catalog Upload")
    print("=" * 60)
    print(f"Project ID: {PROJECT_ID}")
    print(f"Location: {LOCATION}")
    print(f"Catalog: {CATALOG_ID}")
    print(f"Branch: {BRANCH_ID}")
    print(f"File: {catalog_file}")
    print("=" * 60)
    
    # Confirm upload
    response = input("\n⚠️  This will replace the existing product catalog. Continue? (y/N): ")
    if response.lower() != 'y':
        print("❌ Upload cancelled.")
        return
    
    # Upload the catalog
    success = upload_product_catalog(
        project_id=PROJECT_ID,
        location=LOCATION,
        catalog_id=CATALOG_ID,
        branch_id=BRANCH_ID,
        ndjson_file_path=catalog_file
    )
    
    if success:
        print("\n🎉 Catalog upload completed successfully!")
        print("💡 Your Google Cloud Retail AI recommendations should now use real products instead of auto-generated entries.")
        print("🔄 It may take a few minutes for the changes to take effect.")
    else:
        print("\n❌ Catalog upload failed. Please check the logs above for details.")

if __name__ == "__main__":
    main()