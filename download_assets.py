import os
import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def download_file(url, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not url.startswith('http'):
        url = 'https:' + url if url.startswith('//') else 'https://brandedcutpieces.com.pk' + url
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            content = resp.read()
            with open(filepath, 'wb') as f:
                f.write(content)
            print(f"Downloaded: {filepath} ({len(content)} bytes)")
            return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def main():
    os.makedirs('assets/css', exist_ok=True)
    os.makedirs('assets/js', exist_ok=True)
    os.makedirs('assets/images', exist_ok=True)
    os.makedirs('assets/brands', exist_ok=True)
    
    # Read homepage.html to extract all css links and images
    with open('homepage.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    css_urls = re.findall(r'href=["\']([^"\']+\.css[^"\']*)["\']', html)
    print(f"Found {len(css_urls)} CSS URLs")
    for css_url in set(css_urls):
        filename = css_url.split('/')[-1].split('?')[0]
        if not filename.endswith('.css'):
            filename += '.css'
        download_file(css_url, f"assets/css/{filename}")
        
    img_urls = re.findall(r'src=["\']([^"\']+(?:\.png|\.jpg|\.jpeg|\.webp|\.svg)[^"\']*)["\']', html)
    print(f"Found {len(img_urls)} image URLs")
    for img_url in list(set(img_urls))[:60]:
        filename = img_url.split('/')[-1].split('?')[0]
        download_file(img_url, f"assets/images/{filename}")

if __name__ == '__main__':
    main()
