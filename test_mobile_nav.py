from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 375, "height": 812})
    
    # 1. Test shop-by-brand.html mobile menu open
    page.goto("http://localhost:8080/shop-by-brand.html", wait_until="domcontentloaded")
    time.sleep(1)
    
    # Click mobile menu hamburger toggle
    toggle = page.locator("#mobile-menu-toggle")
    toggle.click()
    time.sleep(0.5)
    
    drawer = page.locator("#mobile-nav-drawer")
    is_active = drawer.evaluate("el => el.classList.contains('active')")
    is_visible = drawer.is_visible()
    print("shop-by-brand.html -> mobile nav drawer is_active:", is_active, "is_visible:", is_visible)
    page.screenshot(path="verification_screenshots/shop_by_brand_mobile_nav_opened.png")
    
    # Close drawer
    page.locator(".drawer-close").first.click()
    time.sleep(0.5)
    
    # 2. Check bottom scroll on shop-by-brand.html
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(0.5)
    page.screenshot(path="verification_screenshots/shop_by_brand_mobile_bottom.png")
    
    # 3. Test contact.html mobile menu open
    page.goto("http://localhost:8080/contact.html", wait_until="domcontentloaded")
    time.sleep(1)
    page.locator("#mobile-menu-toggle").click()
    time.sleep(0.5)
    c_active = page.locator("#mobile-nav-drawer").evaluate("el => el.classList.contains('active')")
    print("contact.html -> mobile nav drawer is_active:", c_active)
    page.screenshot(path="verification_screenshots/contact_mobile_nav_opened.png")
    
    # 4. Test collections.html mobile menu open
    page.goto("http://localhost:8080/collections.html", wait_until="domcontentloaded")
    time.sleep(1)
    page.locator("#mobile-menu-toggle").click()
    time.sleep(0.5)
    col_active = page.locator("#mobile-nav-drawer").evaluate("el => el.classList.contains('active')")
    print("collections.html -> mobile nav drawer is_active:", col_active)
    
    browser.close()

print("All mobile tests completed successfully!")
