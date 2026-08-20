from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    # 1. Homepage Brand Ticker
    page.goto("http://localhost:8080/index.html")
    page.locator(".brand-slider-section").scroll_into_view_if_needed()
    time.sleep(0.5)
    page.screenshot(path="verification_screenshots/homepage_ticker_all_updated_logos.png")
    
    # 2. Shop By Brand Page
    page.goto("http://localhost:8080/shop-by-brand.html")
    time.sleep(0.5)
    page.screenshot(path="verification_screenshots/shop_by_brand_all_updated_logos.png")
    
    print("Screenshots captured successfully!")
    browser.close()
