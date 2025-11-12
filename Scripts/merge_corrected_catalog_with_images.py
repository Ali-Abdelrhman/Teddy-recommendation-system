import pandas as pd
import json

def merge_corrected_catalog_with_images():
    """
    Merge the corrected catalog with image URLs
    """
    
    print("Reading image data from CSV...")
    images_df = pd.read_csv(r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\cte_202511021815.csv")
    
    # Create image dictionary
    image_dict = {}
    for _, row in images_df.iterrows():
        sku_id = str(row['sku_id'])
        if sku_id not in image_dict:  # Take first image per SKU
            image_dict[sku_id] = row['image_path']
    
    print(f"Loaded {len(image_dict)} unique product images")
    
    # Process corrected catalog file
    catalog_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\ML_Recommendation_Engine\catalog_with_corrected_ids.ndjson"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\ML_Recommendation_Engine\final_catalog_with_correct_images.ndjson"
    
    print("Processing corrected catalog file...")
    processed_count = 0
    with_images_count = 0
    
    with open(catalog_file, 'r', encoding='utf-8') as input_file, \
         open(output_file, 'w', encoding='utf-8') as output_file_handle:
        
        for line_num, line in enumerate(input_file, 1):
            if line.strip():
                try:
                    product = json.loads(line.strip())
                    product_id = str(product.get('id', ''))
                    
                    # Add image if available
                    if product_id in image_dict:
                        product['images'] = [{"uri": image_dict[product_id]}]
                        with_images_count += 1
                    else:
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
    print(f"Image coverage: {(with_images_count/processed_count)*100:.2f}%")
    print(f"Final catalog saved to: {output_file}")

if __name__ == "__main__":
    merge_corrected_catalog_with_images()