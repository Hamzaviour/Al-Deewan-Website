from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    # 1. Login to Admin
    page.goto("http://localhost:8080/admin.html")
    page.fill("#admin-passcode-input", "deewan2026")
    page.click(".auth-btn")
    page.wait_for_selector("#admin-app", state="visible")
    
    # 2. Test Homepage Headings Editor
    page.click("button[data-tab='headings']")
    time.sleep(0.5)
    page.fill("#heading-new-arrivals-title", "SUMMER 2026 EXCLUSIVE NEW ARRIVALS")
    page.fill("#heading-new-arrivals-sub", "Customized subtitle by store manager")
    page.click("#tab-headings button[type='submit']")
    time.sleep(0.8)
    page.screenshot(path="verification_screenshots/admin_headings_tab.png")
    print("Saved custom homepage headings in Admin!")
    
    # 3. Test Navigation Dropdown Editor
    page.click("button[data-tab='navigation']")
    time.sleep(0.5)
    page.click("button:has-text('+ Add Brand Link')")
    time.sleep(0.3)
    
    # Find last input in brand list and type custom brand
    last_row = page.locator("#brand-menu-list .menu-item-row").last
    last_row.locator(".menu-label").fill("Khaadi Luxe Edit")
    last_row.locator(".menu-url").fill("collections.html?brand=Khaadi")
    page.click("button:has-text('Save Brand Dropdown')")
    time.sleep(0.8)
    page.screenshot(path="verification_screenshots/admin_navigation_tab.png")
    print("Saved custom dropdown menus in Admin!")
    
    # 4. Verify Live Reflection on Homepage
    page.goto("http://localhost:8080/index.html", wait_until="domcontentloaded")
    time.sleep(1)
    
    heading_text = page.locator(".products-section .section-title").first.text_content()
    assert "SUMMER 2026 EXCLUSIVE NEW ARRIVALS" in heading_text, "Homepage heading should update dynamically"
    print("Verified custom heading on live index.html:", heading_text)
    
    dropdown_text = page.locator(".nav-dropdown-menu").first.text_content()
    assert "Khaadi Luxe Edit" in dropdown_text, "Dropdown should contain new custom brand"
    print("Verified custom brand in live dropdown menu!")
    
    page.screenshot(path="verification_screenshots/live_homepage_with_custom_headings.png")
    browser.close()

print("ALL HEADINGS & DROPDOWN MENU TESTS PASSED SUCCESSFULLY!")
