import json
import os
import re

def create_catalog_data():
    with open('data/products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    with open('data/collections.json', 'r', encoding='utf-8') as f:
        collections = json.load(f)
        
    print(f"Total raw products: {len(products)}")
    
    # Clean and structure products
    cleaned_products = []
    seen_titles = set()
    
    for p in products:
        title = p.get('title', '').strip()
        if not title or title in seen_titles:
            continue
        seen_titles.add(title)
        
        # Variants & pricing
        variants = p.get('variants', [])
        price = 0.0
        compare_at_price = 0.0
        sku = ''
        available = False
        
        if variants:
            v = variants[0]
            try:
                price = float(v.get('price', 0))
            except:
                price = 0.0
            try:
                compare_at_price = float(v.get('compare_at_price', 0)) if v.get('compare_at_price') else price * 1.6
            except:
                compare_at_price = price * 1.6
            sku = v.get('sku', '')
            available = v.get('available', True)
        
        # If compare_at_price is 0 or less than price, make it realistic sale discount
        if compare_at_price <= price and price > 0:
            compare_at_price = round(price * 1.65, -1)
            
        save_amount = max(0, compare_at_price - price)
        discount_percent = round((save_amount / compare_at_price) * 100) if compare_at_price > 0 else 0
        
        # Extract images
        images = []
        for img in p.get('images', []):
            src = img.get('src', '')
            if src:
                images.append(src)
                
        if not images and p.get('image'):
            images.append(p['image'].get('src', ''))
            
        if not images:
            continue
            
        # Determine brand / vendor
        vendor = p.get('vendor', '').strip()
        if not vendor:
            # guess from title
            first_word = title.split()[0]
            vendor = first_word
            
        # Determine category & collection
        tags = p.get('tags', [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',')]
            
        category = 'Unstitched'
        title_lower = title.lower()
        if 'stitched' in title_lower or 'ready to wear' in title_lower or 'kurti' in title_lower or '2pc' in title_lower:
            if 'unstitched' not in title_lower:
                category = 'Ready to Wear'
        if 'men' in title_lower or 'gents' in title_lower:
            category = 'Menswear'
        if '3pc' in title_lower:
            category_type = '3PC'
        elif '2pc' in title_lower:
            category_type = '2PC'
        else:
            category_type = '1PC / Kurti'
            
        cleaned_products.append({
            'id': p.get('id'),
            'title': title,
            'handle': p.get('handle', ''),
            'vendor': vendor,
            'product_type': p.get('product_type', category),
            'category': category,
            'category_type': category_type,
            'tags': tags,
            'price': price,
            'compare_at_price': compare_at_price,
            'save_amount': save_amount,
            'discount_percent': discount_percent,
            'sku': sku or f"BCP-{str(p.get('id', ''))[-4:] if p.get('id') else '8230'}",
            'available': available,
            'images': images,
            'featured_image': images[0],
            'body_html': p.get('body_html', ''),
            'published_at': p.get('published_at', '')
        })
        
    print(f"Total processed clean products: {len(cleaned_products)}")
    
    # Save full optimized catalog for frontend
    top_catalog = cleaned_products # All clean products with complete rich data
    
    os.makedirs('assets/js', exist_ok=True)
    with open('assets/js/catalog-data.js', 'w', encoding='utf-8') as f:
        f.write('// Branded Cut Pieces Catalog Data\n')
        f.write('window.CATALOG_PRODUCTS = ')
        json.dump(top_catalog, f, ensure_ascii=False)
        f.write(';\n\n')
        f.write('window.COLLECTIONS_DATA = ')
        json.dump(collections, f, ensure_ascii=False)
        f.write(';\n')
        
    print(f"Generated assets/js/catalog-data.js with {len(top_catalog)} rich products and {len(collections)} collections.")

if __name__ == '__main__':
    create_catalog_data()
