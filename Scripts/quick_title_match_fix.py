import pandas as pd
import json
from difflib import SequenceMatcher

def simple_title_match():
    """
    Simple and fast script to match titles and fix SKU_IDs
    """
    
    # File paths
    database_csv = r"C:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\_SELECT_s_id_as_sku_id_s_code_as_sku_code_s_name_en_as_sku_name__202511021857.csv"
    catalog_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\ML_Recommendation_Engine\catalog_with_images.ndjson"
    output_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\ML_Recommendation_Engine\catalog_with_corrected_ids.ndjson"
    
    print("Loading database CSV...")
    db_df = pd.read_csv(database_csv)
    
    # Create title lookup dictionary: title -> sku_id
    print("Creating title lookup...")
    title_lookup = {}
    for _, row in db_df.iterrows():
        title = str(row['product_title_en']).strip().lower()
        title_lookup[title] = row['sku_id']
    
    print(f"Loaded {len(title_lookup)} titles from database")
    
    # Process catalog
    print("Processing catalog...")
    corrections_made = 0
    exact_matches = 0
    no_matches = 0
    
    with open(catalog_file, 'r', encoding='utf-8') as input_f, \
         open(output_file, 'w', encoding='utf-8') as output_f:
        
        for line_num, line in enumerate(input_f, 1):
            if line.strip():
                product = json.loads(line.strip())
                catalog_title = str(product['title']).strip().lower()
                current_id = product['id']
                
                # Check for exact title match
                if catalog_title in title_lookup:
                    correct_sku_id = str(title_lookup[catalog_title])
                    
                    if current_id != correct_sku_id:
                        # ID needs correction
                        product['id'] = correct_sku_id
                        corrections_made += 1
                        
                        if corrections_made <= 10:  # Show first 10 corrections
                            print(f"CORRECTION {corrections_made}:")
                            print(f"  Title: {product['title'][:50]}...")
                            print(f"  Old ID: {current_id} -> New ID: {correct_sku_id}")
                    else:
                        exact_matches += 1
                else:
                    # Try fuzzy matching for close titles
                    best_match = None
                    best_score = 0
                    
                    for db_title, sku_id in title_lookup.items():
                        similarity = SequenceMatcher(None, catalog_title, db_title).ratio()
                        if similarity > best_score and similarity >= 0.9:  # Very high threshold
                            best_score = similarity
                            best_match = (db_title, sku_id)
                    
                    if best_match:
                        correct_sku_id = str(best_match[1])
                        if current_id != correct_sku_id:
                            product['id'] = correct_sku_id
                            corrections_made += 1
                            
                            if corrections_made <= 10:
                                print(f"FUZZY CORRECTION {corrections_made}:")
                                print(f"  Title: {product['title'][:50]}...")
                                print(f"  Old ID: {current_id} -> New ID: {correct_sku_id}")
                                print(f"  Similarity: {best_score:.3f}")
                    else:
                        no_matches += 1
                        if no_matches <= 5:  # Show first 5 no-matches
                            print(f"NO MATCH: {product['title'][:50]}... (ID: {current_id})")
                
                # Write the product (corrected or original)
                output_f.write(json.dumps(product, ensure_ascii=False) + '\n')
                
                if line_num % 1000 == 0:
                    print(f"Processed {line_num} products...")
    
    # Summary
    print(f"\n{'='*50}")
    print("CORRECTION SUMMARY")
    print(f"{'='*50}")
    print(f"Total products processed: {line_num}")
    print(f"Exact matches (no change needed): {exact_matches}")
    print(f"Corrections made: {corrections_made}")
    print(f"No matches found: {no_matches}")
    print(f"\nCorrected catalog saved to: {output_file}")
    
    return corrections_made

if __name__ == "__main__":
    corrections = simple_title_match()
    
    if corrections > 0:
        print(f"\n✅ SUCCESS: Made {corrections} corrections!")
        print("Now you can re-run the image merging script with the corrected catalog.")
    else:
        print("\n✅ No corrections needed - all IDs are already correct!")