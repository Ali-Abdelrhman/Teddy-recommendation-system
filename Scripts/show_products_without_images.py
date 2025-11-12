import json

catalog_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\ML_Recommendation_Engine\catalog_with_images.ndjson"

print("Products without images:")
print("=" * 50)

with open(catalog_file, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            product = json.loads(line.strip())
            if not product.get('images') or len(product['images']) == 0:
                print(f"Product ID: {product['id']}")
                print(f"Title: {product['title']}")
                print(f"Images field: {product['images']}")
                print(f"Availability: {product.get('availability', 'N/A')}")
                print("-" * 30)