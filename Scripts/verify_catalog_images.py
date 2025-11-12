import json

# Verify the catalog with images
catalog_file = r"c:\Users\Ahmed\Downloads\Teddy recommendation system\ML_Recommendation_Engine\catalog_with_images.ndjson"

print("Verification of catalog with images:")
print("=" * 50)

total_products = 0
with_images = 0
without_images = 0

# Check first few products and count overall
with open(catalog_file, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if line.strip():
            product = json.loads(line.strip())
            total_products += 1
            
            if product.get('images') and len(product['images']) > 0:
                with_images += 1
                if i < 3:  # Show first 3 with images
                    print(f"Product ID {product['id']}: {product['title'][:50]}...")
                    print(f"  Images: {len(product['images'])}")
                    print(f"  URI: {product['images'][0]['uri']}")
                    print()
            else:
                without_images += 1
                if without_images <= 3:  # Show first 3 without images
                    print(f"Product ID {product['id']} (NO IMAGE): {product['title'][:50]}...")

print(f"Summary:")
print(f"Total products: {total_products}")
print(f"Products with images: {with_images}")
print(f"Products without images: {without_images}")
print(f"Coverage: {(with_images/total_products)*100:.2f}%")

# Verify GCP format
if with_images > 0:
    print(f"\nGCP Format Verification:")
    with open(catalog_file, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        product = json.loads(first_line)
        if 'images' in product and product['images']:
            img = product['images'][0]
            print(f"✓ Images field exists: {type(product['images'])} with {len(product['images'])} items")
            print(f"✓ Image format: {type(img)} with keys: {list(img.keys())}")
            print(f"✓ URI field exists: {'uri' in img}")
            print(f"✓ Format compatible with GCP: [{{\"uri\": \"...\"}}, ...]")