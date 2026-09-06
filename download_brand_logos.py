import os
import urllib.request
from playwright.sync_api import sync_playwright

os.makedirs('assets/images/brands', exist_ok=True)

sites = {
    'kayseria': 'https://kayseria.com/',
    'ideas': 'https://www.gulahmedshop.com/',
    'bonanza': 'https://bonanzasatrangi.com/',
    'bin_ilyas': 'https://binilyas.com/'
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    for name, url in sites.items():
        try:
            print(f"Visiting {url}...")
            page.goto(url, timeout=30000, wait_until='domcontentloaded')
            page.wait_for_timeout(2500)
            logo_src = page.evaluate("""() => {
                const img = document.querySelector('header img, .header img, .logo img, [class*="logo"] img, a[href="/"] img, .header__logo img, .site-header__logo img');
                return img ? (img.src || img.getAttribute('data-src') || img.currentSrc) : '';
            }""")
            print(f"{name} logo URL: {logo_src}")
            if logo_src:
                req = urllib.request.Request(logo_src, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=15) as resp, open(f'assets/images/brands/{name}.png', 'wb') as f:
                    f.write(resp.read())
                print(f"Saved assets/images/brands/{name}.png")
        except Exception as e:
            print(f"Error for {name}: {e}")
    browser.close()
