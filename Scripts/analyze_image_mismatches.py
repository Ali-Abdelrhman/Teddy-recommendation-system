import pandas as pd
import json

def analyze_image_mismatches():
    """
    Analyze potential causes of image-product mismatches
    """
    print("Analyzing Image-Product Mapping Issues")
    print("=" * 50)
    
    # Load image data
    images_df = pd.read_csv(r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\cte_202511021815.csv")
    catalog_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\ML_Recommendation_Engine\catalog_with_images.ndjson"
    
    print(f"Total images in database: {len(images_df)}")
    print(f"Unique SKU IDs with images: {images_df['sku_id'].nunique()}")
    
    # Check for SKUs with multiple images
    sku_counts = images_df['sku_id'].value_counts()
    multiple_images = sku_counts[sku_counts > 1]
    
    print(f"SKUs with multiple images: {len(multiple_images)}")
    print(f"Max images per SKU: {sku_counts.max()}")
    
    if len(multiple_images) > 0:
        print("\nTop SKUs with most images:")
        print(multiple_images.head(10))
        
        # Show examples of SKUs with multiple images
        print("\nExample: SKU with multiple images:")
        example_sku = multiple_images.index[0]
        example_images = images_df[images_df['sku_id'] == example_sku]
        print(f"SKU ID: {example_sku}")
        for i, (_, row) in enumerate(example_images.iterrows()):
            print(f"  Image {i+1}: {row['image_path'][-50:]}")
    
    # Check for potential issues in catalog
    print(f"\nAnalyzing catalog mapping...")
    sample_products = []
    
    with open(catalog_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i < 10:  # Check first 10 products
                product = json.loads(line.strip())
                sample_products.append({
                    'id': product['id'],
                    'title': product['title'][:50],
                    'has_image': len(product.get('images', [])) > 0,
                    'image_url': product['images'][0]['uri'][-50:] if product.get('images') else 'NO IMAGE'
                })
    
    print("\nFirst 10 products with their image mappings:")
    for p in sample_products:
        print(f"ID {p['id']}: {p['title']}...")
        print(f"  Image: {p['image_url']}")
        print()

def suggest_solutions():
    """
    Suggest potential solutions for image mismatches
    """
    print("\n" + "=" * 50)
    print("POTENTIAL SOLUTIONS FOR IMAGE MISMATCHES")
    print("=" * 50)
    
    print("\n1. IMAGE ORDER ISSUE:")
    print("   - Current: Taking first image by image_order")
    print("   - Solution: Take image with specific criteria (newest, highest quality, etc.)")
    
    print("\n2. SKU ID MISMATCH:")
    print("   - Issue: Product ID in catalog might not match SKU ID in image table")
    print("   - Solution: Check if we need to map through product table")
    
    print("\n3. OUTDATED IMAGES:")
    print("   - Issue: Images might be for old versions of products")
    print("   - Solution: Filter by date or use more recent images")
    
    print("\n4. PRODUCT VARIANTS:")
    print("   - Issue: One SKU might have multiple product variants")
    print("   - Solution: Match by product attributes (color, size, etc.)")

if __name__ == "__main__":
    analyze_image_mismatches()
    suggest_solutions()