from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # Mobile viewport (iPhone 14 / modern Android)
    page = browser.new_page(viewport={"width": 390, "height": 844})
    
    page.goto("http://localhost:8080/index.html")
    time.sleep(0.5)
    
    # Click hamburger menu
    page.click("#mobile-menu-toggle")
    time.sleep(0.5)
    
    menu_items = page.locator("#mobile-nav-drawer .drawer-body a").all_inner_texts()
    print(f"Total menu items: {len(menu_items)}")
    for item in menu_items:
        clean_item = item.encode('ascii', 'replace').decode('ascii')
        print(f" - {clean_item}")
    
    # Assertions
    assert "UNSTITCHED" in menu_items, "UNSTITCHED should be present in menu"
    assert "UNSTITCHED 3PC" not in menu_items, "UNSTITCHED 3PC should NOT be in menu"
    assert not any("download" in item.lower() for item in menu_items), "Download App should NOT be in menu"
    
    page.screenshot(path="verification_screenshots/mobile_menu_drawer_updated.png")
    print("Mobile menu test passed perfectly!")
    
    browser.close()
