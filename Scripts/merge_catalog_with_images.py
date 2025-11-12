import pandas as pd
import json
import os
from pathlib import Path

def merge_catalog_with_images(catalog_file, images_csv, output_file):
    """
    Merge catalog NDJSON with image URLs from CSV file.
    Adds 'images' field with GCP-compatible format: [{"uri": "..."}]
    """
    
    print("Reading image data from CSV...")
    # Read image data
    images_df = pd.read_csv(images_csv)
    
    # Create a dictionary mapping sku_id to image_path
    # Handle multiple images per SKU by taking the first one (as per your query)
    image_dict = {}
    for _, row in images_df.iterrows():
        sku_id = str(row['sku_id'])  # Convert to string to match catalog IDs
        if sku_id not in image_dict:  # Only take the first image per SKU
            image_dict[sku_id] = row['image_path']
    
    print(f"Loaded {len(image_dict)} unique product images")
    
    # Process catalog file
    print("Processing catalog file...")
    processed_count = 0
    with_images_count = 0
    
    with open(catalog_file, 'r', encoding='utf-8') as input_file, \
         open(output_file, 'w', encoding='utf-8') as output_file_handle:
        
        for line_num, line in enumerate(input_file, 1):
            if line.strip():  # Skip empty lines
                try:
                    # Parse JSON
                    product = json.loads(line.strip())
                    
                    # Get product ID
                    product_id = str(product.get('id', ''))
                    
                    # Add image if available
                    if product_id in image_dict:
                        product['images'] = [{"uri": image_dict[product_id]}]
                        with_images_count += 1
                    else:
                        # Add empty images array for products without images
                        product['images'] = []
                    
                    # Write updated product
                    output_file_handle.write(json.dumps(product, ensure_ascii=False) + '\n')
                    processed_count += 1
                    
                    if processed_count % 1000 == 0:
                        print(f"Processed {processed_count} products...")
                        
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON on line {line_num}: {e}")
                    continue
    
    print(f"\nCompleted!")
    print(f"Total products processed: {processed_count}")
    print(f"Products with images: {with_images_count}")
    print(f"Products without images: {processed_count - with_images_count}")
    print(f"Output saved to: {output_file}")

def main():
    # File paths
    base_dir = Path(r"c:\Users\Ahmed\Downloads\Teddy recommendation system")
    catalog_file = base_dir / "ML_Recommendation_Engine" / "filtered_catalog_with_events.ndjson"
    images_csv = base_dir / "Test CSVs" / "cte_202511021815.csv"
    output_file = base_dir / "ML_Recommendation_Engine" / "catalog_with_images.ndjson"
    
    # Check if files exist
    if not catalog_file.exists():
        print(f"Error: Catalog file not found: {catalog_file}")
        return
    
    if not images_csv.exists():
        print(f"Error: Images CSV not found: {images_csv}")
        return
    
    print(f"Input catalog: {catalog_file}")
    print(f"Input images: {images_csv}")
    print(f"Output file: {output_file}")
    print("-" * 50)
    
    # Run the merge
    merge_catalog_with_images(catalog_file, images_csv, output_file)
    
    # Show sample of output
    print("\nSample of output (first 3 products):")
    with open(output_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 3:
                break
            product = json.loads(line.strip())
            print(f"ID {product['id']}: {len(product.get('images', []))} image(s)")
            if product.get('images'):
                print(f"  Image URI: {product['images'][0]['uri'][:80]}...")
            print()

if __name__ == "__main__":
    main()