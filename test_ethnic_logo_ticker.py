from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    # 1. Check Homepage Brand Ticker
    page.goto("http://localhost:8080/index.html")
    page.locator(".brand-slider-section").scroll_into_view_if_needed()
    time.sleep(0.5)
    
    ethnic_cards = page.locator(".brand-card:has-text('ETHNIC')")
    count = ethnic_cards.count()
    print(f"Ethnic cards found in homepage ticker: {count}")
    assert count >= 2, "Ethnic should be present in both sets of marquee"
    
    img_src = ethnic_cards.first.locator("img").get_attribute("src")
    print(f"Ethnic logo src: {img_src}")
    assert "ethnic_circle_logo.png" in img_src
    
    page.screenshot(path="verification_screenshots/homepage_brand_ticker_ethnic.png")
    
    # 2. Check Shop By Brand page
    page.goto("http://localhost:8080/shop-by-brand.html")
    time.sleep(0.5)
    
    ethnic_brand = page.locator(".brand-card:has-text('Ethnic')").first
    img_src_brand = ethnic_brand.locator("img").get_attribute("src")
    print(f"Shop-by-brand Ethnic logo src: {img_src_brand}")
    assert "ethnic_circle_logo.png" in img_src_brand
    
    page.screenshot(path="verification_screenshots/shop_by_brand_ethnic_logo.png")
    
    browser.close()

print("ALL ETHNIC LOGO & BRAND TICKER TESTS PASSED PERFECTLY!")
