import os
import json
import time
import urllib.request
import ssl
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_url(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            return resp.read()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    os.makedirs('data', exist_ok=True)
    os.makedirs('assets/images', exist_ok=True)
    os.makedirs('assets/brands', exist_ok=True)
    os.makedirs('assets/banners', exist_ok=True)
    
    print("1. Fetching all products...")
    all_products = []
    page = 1
    while True:
        url = f"https://brandedcutpieces.com.pk/products.json?limit=250&page={page}"
        print(f"Fetching products page {page}...")
        raw = fetch_url(url)
        if not raw:
            break
        data = json.loads(raw.decode('utf-8'))
        prods = data.get('products', [])
        if not prods:
            break
        all_products.extend(prods)
        print(f"Fetched {len(prods)} products (Total so far: {len(all_products)})")
        if len(prods) < 250:
            break
        page += 1
        time.sleep(0.5)
        
    with open('data/products.json', 'w', encoding='utf-8') as f:
        json.dump(all_products, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(all_products)} products to data/products.json")

    print("\n2. Fetching all collections...")
    cols_url = "https://brandedcutpieces.com.pk/collections.json?limit=250"
    cols_raw = fetch_url(cols_url)
    if cols_raw:
        cols_data = json.loads(cols_raw.decode('utf-8'))
        collections = cols_data.get('collections', [])
        with open('data/collections.json', 'w', encoding='utf-8') as f:
            json.dump(collections, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(collections)} collections to data/collections.json")

    print("\n3. Fetching static pages...")
    page_handles = [
        'contact', 'refunds', 'privacy-policy', 'customer-services',
        'order-tracking', 'download-app', 'shop-by-brand', 'thank-you'
    ]
    pages_content = {}
    for handle in page_handles:
        url = f"https://brandedcutpieces.com.pk/pages/{handle}"
        raw = fetch_url(url)
        if raw:
            soup = BeautifulSoup(raw.decode('utf-8', errors='ignore'), 'html.parser')
            # extract main content
            main_elem = soup.find('main') or soup.find('article') or soup.find('div', class_='main-content')
            pages_content[handle] = {
                'title': soup.title.string if soup.title else handle.replace('-', ' ').title(),
                'html': str(main_elem) if main_elem else '',
                'text': main_elem.get_text(separator='\n').strip() if main_elem else ''
            }
            print(f"Fetched page: {handle}")
        time.sleep(0.3)
        
    with open('data/pages.json', 'w', encoding='utf-8') as f:
        json.dump(pages_content, f, indent=2, ensure_ascii=False)
    print("Saved pages content to data/pages.json")

if __name__ == '__main__':
    main()
