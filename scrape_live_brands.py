import json
import urllib.request
import os
from playwright.sync_api import sync_playwright

os.makedirs('assets/images/brands', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    print("Navigating to https://brandedcutpieces.com.pk/ ...")
    try:
        page.goto("https://brandedcutpieces.com.pk/", wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(3000)
        
        # Scrape all image tags and potential brand items
        data = page.evaluate("""() => {
            const allImages = [];
            document.querySelectorAll('img').forEach(img => {
                const src = img.src || img.getAttribute('data-src') || '';
                const alt = img.alt || '';
                const parentA = img.closest('a');
                allImages.push({
                    src: src,
                    alt: alt,
                    href: parentA ? parentA.href : '',
                    class: img.className,
                    parentClass: img.parentElement ? img.parentElement.className : ''
                });
            });

            // Look specifically for brand slider/ticker elements
            const brandSlider = document.querySelector('.brand-slider, .brands, [class*="brand"], [class*="logo-bar"], [class*="halo-brand"]');
            
            return {
                allImages: allImages,
                brandSliderHtml: brandSlider ? brandSlider.outerHTML : ''
            };
        }""")
        
        print("Total images found:", len(data["allImages"]))
        
        with open("scraped_brands.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            
        print("Saved scraped_brands.json successfully!")
    except Exception as e:
        print("Scraping error:", e)
    browser.close()
