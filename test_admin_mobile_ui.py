from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # Mobile viewport (iPhone 14: 390x844)
    page = browser.new_page(viewport={"width": 390, "height": 844})
    
    # 1. Test Login Screen
    page.goto("http://localhost:8080/admin.html")
    time.sleep(0.5)
    
    login_text = page.locator("#auth-screen").inner_text()
    print("Checking for passcode hint...")
    assert "Default Passcode" not in login_text, "Default Passcode hint must be removed!"
    assert "deewan2026" not in login_text, "deewan2026 text must not be visible on login screen!"
    print("Passcode hint successfully removed from login screen!")
    page.screenshot(path="verification_screenshots/admin_mobile_login_no_hint.png")
    
    # 2. Login to Dashboard
    page.fill("#admin-passcode-input", "deewan2026")
    page.click("button[type='submit']")
    time.sleep(0.5)
    
    # 3. Verify Overview Dashboard on Mobile
    print("Admin dashboard loaded on mobile.")
    page.screenshot(path="verification_screenshots/admin_mobile_dashboard_overview.png")
    
    # 4. Test Mobile Hamburger Drawer Menu
    page.click("#admin-mobile-menu-btn")
    time.sleep(0.5)
    
    sidebar_open = page.locator("#admin-sidebar").is_visible()
    print(f"Mobile Sidebar Drawer Open? {sidebar_open}")
    assert sidebar_open, "Admin sidebar drawer should open on hamburger click!"
    page.screenshot(path="verification_screenshots/admin_mobile_sidebar_drawer.png")
    
    # 5. Click Delivery Tab in Drawer
    page.click("#admin-sidebar button[data-tab='delivery']")
    time.sleep(0.5)
    page.screenshot(path="verification_screenshots/admin_mobile_delivery_tab.png")
    
    # 6. Test Quick Tabs Strip (Click Articles)
    page.click(".quick-tab-pill:has-text('Articles')")
    time.sleep(0.5)
    page.screenshot(path="verification_screenshots/admin_mobile_articles_tab.png")
    
    # 7. Test Add Article Modal on Mobile
    page.click("#tab-products button:has-text('+ Add New Article')")
    time.sleep(0.5)
    modal_visible = page.locator("#product-modal").is_visible()
    print(f"Product modal visible? {modal_visible}")
    assert modal_visible, "Add article modal should be visible!"
    page.screenshot(path="verification_screenshots/admin_mobile_add_modal.png")
    
    browser.close()

print("\nALL ADMIN MOBILE RESPONSIVENESS AND UI/UX TESTS PASSED PERFECTLY!")
