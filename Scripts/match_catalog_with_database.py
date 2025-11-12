import pandas as pd
import json
from difflib import SequenceMatcher
import re

def clean_text(text):
    """Clean text for better matching"""
    if pd.isna(text) or text is None:
        return ""
    # Remove extra whitespace, newlines, and special characters
    text = re.sub(r'\s+', ' ', str(text))
    text = re.sub(r'[^\w\s]', ' ', text)
    return text.lower().strip()

def similarity(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, clean_text(a), clean_text(b)).ratio()

def find_best_match(catalog_item, database_df, threshold=0.7):
    """Find the best matching SKU_ID for a catalog item"""
    catalog_title = catalog_item['title']
    catalog_desc = catalog_item.get('description', '')
    
    best_match = None
    best_score = 0
    
    for _, row in database_df.iterrows():
        db_title = row['product_title_en']
        db_desc = row['product_description_en']
        
        # Calculate title similarity
        title_sim = similarity(catalog_title, db_title)
        
        # Calculate description similarity
        desc_sim = similarity(catalog_desc, db_desc)
        
        # Combined score (title is more important)
        combined_score = (title_sim * 0.7) + (desc_sim * 0.3)
        
        if combined_score > best_score and combined_score >= threshold:
            best_score = combined_score
            best_match = {
                'sku_id': row['sku_id'],
                'product_id': row['product_id'],
                'db_title': db_title,
                'db_desc': db_desc[:100] + '...' if len(str(db_desc)) > 100 else db_desc,
                'title_similarity': title_sim,
                'desc_similarity': desc_sim,
                'combined_score': combined_score
            }
    
    return best_match

def analyze_catalog_mapping():
    """Analyze catalog and find correct SKU_ID mappings"""
    
    # File paths
    database_csv = r"C:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\_SELECT_s_id_as_sku_id_s_code_as_sku_code_s_name_en_as_sku_name__202511021857.csv"
    catalog_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\ML_Recommendation_Engine\catalog_with_images.ndjson"
    
    print("Loading database CSV...")
    database_df = pd.read_csv(database_csv)
    print(f"Loaded {len(database_df)} products from database")
    
    print("\nAnalyzing catalog mappings...")
    
    corrections = []
    mismatches = []
    exact_matches = 0
    
    with open(catalog_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if line.strip():
                catalog_item = json.loads(line.strip())
                current_id = catalog_item['id']
                
                # Check if current ID exists in database
                db_match = database_df[database_df['sku_id'].astype(str) == current_id]
                
                if len(db_match) > 0:
                    # ID exists, check if title matches
                    db_row = db_match.iloc[0]
                    title_sim = similarity(catalog_item['title'], db_row['product_title_en'])
                    
                    if title_sim >= 0.8:  # High similarity, likely correct
                        exact_matches += 1
                        continue
                    else:
                        print(f"ID {current_id}: Title mismatch (similarity: {title_sim:.2f})")
                        print(f"  Catalog: {catalog_item['title'][:60]}...")
                        print(f"  Database: {db_row['product_title_en'][:60]}...")
                
                # Find best match
                best_match = find_best_match(catalog_item, database_df)
                
                if best_match:
                    if str(best_match['sku_id']) != current_id:
                        corrections.append({
                            'current_id': current_id,
                            'correct_sku_id': best_match['sku_id'],
                            'catalog_title': catalog_item['title'],
                            'db_title': best_match['db_title'],
                            'similarity_score': best_match['combined_score']
                        })
                        
                        if len(corrections) <= 10:  # Show first 10 mismatches
                            print(f"\nMISMATCH FOUND:")
                            print(f"  Current ID: {current_id}")
                            print(f"  Correct SKU_ID: {best_match['sku_id']}")
                            print(f"  Catalog Title: {catalog_item['title'][:50]}...")
                            print(f"  Database Title: {best_match['db_title'][:50]}...")
                            print(f"  Similarity Score: {best_match['combined_score']:.3f}")
                else:
                    mismatches.append({
                        'id': current_id,
                        'title': catalog_item['title'],
                        'reason': 'No good match found'
                    })
                
                if line_num % 1000 == 0:
                    print(f"Processed {line_num} products...")
    
    # Summary
    print(f"\n{'='*60}")
    print("ANALYSIS SUMMARY")
    print(f"{'='*60}")
    print(f"Total products analyzed: {line_num}")
    print(f"Exact matches (correct): {exact_matches}")
    print(f"Products needing correction: {len(corrections)}")
    print(f"Products with no match: {len(mismatches)}")
    
    # Save corrections to CSV
    if corrections:
        corrections_df = pd.DataFrame(corrections)
        corrections_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\Test CSVs\sku_id_corrections.csv"
        corrections_df.to_csv(corrections_file, index=False)
        print(f"\nCorrections saved to: {corrections_file}")
        
        # Show top corrections
        print(f"\nTop 20 corrections needed:")
        for i, corr in enumerate(corrections[:20]):
            print(f"{i+1:2d}. ID {corr['current_id']} -> {corr['correct_sku_id']} (score: {corr['similarity_score']:.3f})")
    
    return corrections, mismatches

if __name__ == "__main__":
    corrections, mismatches = analyze_catalog_mapping()
