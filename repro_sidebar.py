from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:8080/collections.html")
    
    # Check Menswear
    page.check("input[name='category'][value='Menswear']")
    page.screenshot(path="verification_screenshots/repro_menswear_empty.png")
    
    box = page.locator(".catalog-sidebar").bounding_box()
    print("Sidebar bounding box for Menswear (empty):", box)
    browser.close()
