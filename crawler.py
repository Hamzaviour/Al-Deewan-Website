import os
import json
import time
import requests
from playwright.sync_api import sync_playwright

def inspect_site():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        print("Navigating to homepage...")
        page.goto('https://brandedcutpieces.com.pk/', timeout=30000, wait_until='domcontentloaded')
        time.sleep(3)
        
        # Save HTML
        html = page.content()
        with open('homepage.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Saved homepage.html (length: {})".format(len(html)))
        
        # Take full screenshot
        page.screenshot(path='homepage_full.png', full_page=True)
        print("Saved homepage_full.png")
        
        # Extract nav menu data (including dropdowns/megamenu)
        nav_data = page.evaluate('''() => {
            const items = [];
            document.querySelectorAll('header nav ul > li, .header__inline-menu > li, .site-nav > li').forEach(li => {
                const link = li.querySelector('a');
                if (!link) return;
                const text = link.innerText.trim();
                const href = link.getAttribute('href');
                const subLinks = [];
                li.querySelectorAll('ul a, .megamenu a, .dropdown a').forEach(sub => {
                    subLinks.push({ text: sub.innerText.trim(), href: sub.getAttribute('href') });
                });
                items.push({ text, href, subLinks });
            });
            return items;
        }''')
        print("Nav Menu Data:", json.dumps(nav_data, indent=2))
        
        # Extract all CSS links
        css_links = page.evaluate('''() => {
            return Array.from(document.querySelectorAll('link[rel="stylesheet"]')).map(l => l.href);
        }''')
        print("CSS Links Count:", len(css_links))
        
        # Extract banner slides
        hero_slides = page.evaluate('''() => {
            const slides = [];
            document.querySelectorAll('.slideshow, .swiper, .slick-slider, .banner, .hero, [class*="slider"], [class*="banner"]').forEach(slider => {
                slider.querySelectorAll('img').forEach(img => {
                    slides.push({
                        src: img.src || img.getAttribute('data-src') || img.currentSrc,
                        alt: img.alt
                    });
                });
            });
            return slides;
        }''')
        print("Hero / Slider Images:", json.dumps(hero_slides[:10], indent=2))
        
        # Inspect Product Page
        print("\nNavigating to a product page...")
        page.goto('https://brandedcutpieces.com.pk/products/almirah-unstitched-ladies-3pc-20', timeout=30000, wait_until='domcontentloaded')
        time.sleep(3)
        page.screenshot(path='product_page.png', full_page=True)
        with open('product_page.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
        print("Saved product_page.png and product_page.html")
        
        # Inspect Collection Page
        print("\nNavigating to collection page...")
        page.goto('https://brandedcutpieces.com.pk/collections/3pc', timeout=30000, wait_until='domcontentloaded')
        time.sleep(3)
        page.screenshot(path='collection_page.png', full_page=True)
        with open('collection_page.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
        print("Saved collection_page.png and collection_page.html")
        
        # Inspect Contact & Tracking Pages
        print("\nNavigating to contact page...")
        page.goto('https://brandedcutpieces.com.pk/pages/contact', timeout=30000, wait_until='domcontentloaded')
        time.sleep(2)
        page.screenshot(path='contact_page.png', full_page=True)
        
        print("\nNavigating to order tracking page...")
        page.goto('https://brandedcutpieces.com.pk/pages/order-tracking', timeout=30000, wait_until='domcontentloaded')
        time.sleep(2)
        page.screenshot(path='order_tracking_page.png', full_page=True)
        
        browser.close()

if __name__ == '__main__':
    inspect_site()
