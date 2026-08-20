from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    
    pages = ['index.html', 'collections.html', 'shop-by-brand.html', 'cart.html', 'contact.html', 'order-tracking.html', 'refunds.html']
    
    for fname in pages:
        page.goto('http://localhost:8080/' + fname, wait_until='domcontentloaded')
        
        info = page.evaluate('''() => {
            const footer = document.querySelector('footer, .site-footer');
            const footerRect = footer ? footer.getBoundingClientRect() : null;
            const footerBottom = footer ? footerRect.bottom + window.scrollY : 0;
            const scrollHeight = document.documentElement.scrollHeight;
            return {
                scrollHeight: scrollHeight,
                footerBottom: footerBottom,
                bodyPaddingBottom: window.getComputedStyle(document.body).paddingBottom
            };
        }''')
        print(f"{fname:<20} scrollHeight: {info['scrollHeight']}  footerBottom: {info['footerBottom']}  bodyPadding: {info['bodyPaddingBottom']}")
        
        # Capture bottom screenshot
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        page.screenshot(path=f"verification_screenshots/clean_bottom_{fname.replace('.html', '')}.png")
    
    browser.close()
print('All page scroll checks completed!')
