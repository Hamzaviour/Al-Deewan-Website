import urllib.request
import re
from playwright.sync_api import sync_playwright

def inspect():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        print("Navigating to https://brandedcutpieces.com.pk/ ...")
        try:
            page.goto("https://brandedcutpieces.com.pk/", timeout=60000)
            page.wait_for_timeout(3000)
            
            # Find all banner/hero images
            images = page.eval_on_selector_all("img", "elements => elements.map(e => ({src: e.src, alt: e.alt, width: e.naturalWidth, height: e.naturalHeight, class: e.className}))")
            print(f"Total images found: {len(images)}")
            banner_imgs = [img for img in images if 'banner' in img['src'].lower() or 'slider' in img['src'].lower() or img['width'] > 800]
            for b in banner_imgs[:10]:
                print(b)
                
            # Also evaluate slider structure
            slider_html = page.evaluate("() => { const s = document.querySelector('.slideshow, .hero-slider, .flickity-slider, .swiper-wrapper, [class*=\"slider\"], [class*=\"banner\"], [class*=\"hero\"]'); return s ? s.outerHTML.substring(0, 1000) : 'None'; }")
            print("\nSlider HTML snippet:\n", slider_html)
        except Exception as e:
            print("Error accessing site:", e)
        finally:
            browser.close()

if __name__ == "__main__":
    inspect()
