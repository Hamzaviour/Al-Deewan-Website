from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:8080/collections.html")
    
    # 1. Check normal state with products
    box_normal = page.locator(".catalog-sidebar").bounding_box()
    print("Normal State (with products) Sidebar X:", box_normal['x'])
    assert abs(box_normal['x'] - 24) < 2, f"Sidebar should be at x=24, got {box_normal['x']}"
    
    # 2. Check empty state via Menswear checkbox
    page.check("input[name='category'][value='Menswear']")
    time.sleep(0.3)
    box_empty_cat = page.locator(".catalog-sidebar").bounding_box()
    print("Empty State (Menswear) Sidebar X:", box_empty_cat['x'])
    assert abs(box_empty_cat['x'] - box_normal['x']) < 2, f"Sidebar shifted! Normal: {box_normal['x']}, Empty: {box_empty_cat['x']}"
    page.screenshot(path="verification_screenshots/sidebar_fixed_menswear_empty.png")
    
    # Uncheck Menswear
    page.uncheck("input[name='category'][value='Menswear']")
    time.sleep(0.3)
    
    # 3. Check empty state via Max Price = 0
    page.evaluate("""() => {
        const slider = document.getElementById('price-slider');
        slider.value = 0;
        slider.dispatchEvent(new Event('input'));
    }""")
    time.sleep(0.3)
    box_price_zero = page.locator(".catalog-sidebar").bounding_box()
    print("Empty State (Max Price = 0) Sidebar X:", box_price_zero['x'])
    assert abs(box_price_zero['x'] - box_normal['x']) < 2, f"Sidebar shifted! Normal: {box_normal['x']}, Zero Price: {box_price_zero['x']}"
    page.screenshot(path="verification_screenshots/sidebar_fixed_price_zero.png")
    
    browser.close()

print("ALL SIDEBAR POSITIONING TESTS PASSED PERFECTLY!")
